import hashlib
from datetime import datetime, timedelta, timezone

import asgi
from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel, Field, field_validator
from workers import DurableObject, WorkerEntrypoint

from generator import (
    ENGINES,
    STYLES,
    EquipmentNotUsed,
    UpstreamError,
    Workout,
    generate_workout,
    to_js,
)


class ClaudeBudget(DurableObject):
    """Exact per-UTC-day counts of Claude calls: all users, and per client IP.

    One named instance ("global"). A Durable Object runs one request at a time
    and the SQL calls below are synchronous, so check-and-increment can't race —
    unlike GENERATE_LIMITER, which is per-machine and only approximate. The
    per-IP cap stops one client from spending everyone's daily budget.
    """

    def __init__(self, ctx, env):
        super().__init__(ctx, env)
        sql = self.ctx.storage.sql
        sql.exec(
            "CREATE TABLE IF NOT EXISTS usage (day TEXT PRIMARY KEY, calls INTEGER NOT NULL)"
        )
        sql.exec(
            "CREATE TABLE IF NOT EXISTS ip_usage (day TEXT NOT NULL, ip TEXT NOT NULL,"
            " calls INTEGER NOT NULL, PRIMARY KEY (day, ip))"
        )

    async def try_spend(self, limit: int, ip_hash: str, ip_limit: int) -> bool:
        day = datetime.now(timezone.utc).date()
        today = day.isoformat()
        sql = self.ctx.storage.sql
        sql.exec("INSERT INTO usage (day, calls) VALUES (?, 0) ON CONFLICT DO NOTHING", today)
        sql.exec("INSERT INTO ip_usage (day, ip, calls) VALUES (?, ?, 0) ON CONFLICT DO NOTHING",
                 today, ip_hash)
        calls = sql.exec("SELECT calls FROM usage WHERE day = ?", today).one().calls
        ip_calls = sql.exec("SELECT calls FROM ip_usage WHERE day = ? AND ip = ?",
                            today, ip_hash).one().calls
        if calls >= limit or ip_calls >= ip_limit:
            return False
        sql.exec("UPDATE usage SET calls = calls + 1 WHERE day = ?", today)
        sql.exec("UPDATE ip_usage SET calls = calls + 1 WHERE day = ? AND ip = ?",
                 today, ip_hash)
        if calls == 0:
            # First call of a new day: drop history older than a month.
            cutoff = (day - timedelta(days=31)).isoformat()
            sql.exec("DELETE FROM usage WHERE day < ?", cutoff)
            sql.exec("DELETE FROM ip_usage WHERE day < ?", cutoff)
        return True


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request, self.env)


app = FastAPI(title="Repsheet")


class GenerateRequest(BaseModel):
    equipment: list[str] = Field(default_factory=list, max_length=20)
    style: str
    duration: int = Field(ge=5, le=60)
    # Free-text tuning from the Customize sheet: injuries, intensity, movements
    # the athlete wants in. Empty when unused.
    custom: str = Field("", max_length=500)
    # Movements from the last few workouts this session, so a regenerate can be
    # told what "different" means. max_length caps the item count, not item size
    # — generate_workout truncates the strings themselves.
    avoid: list[str] = Field(default_factory=list, max_length=40)
    # Entropy for the server's programming-angle pick; see _variation_brief.
    nonce: int | None = None
    # Model choice from the UI: "sonnet" (Claude, default) or "oss" (gpt-oss).
    # A fixed set, never a model id — the public endpoint must not be able to
    # pick an arbitrary (paid) model.
    engine: str = "sonnet"

    @field_validator("engine")
    @classmethod
    def engine_allowed(cls, v: str) -> str:
        if v not in ENGINES:
            raise ValueError(f"engine must be one of: {', '.join(ENGINES)}")
        return v

    @field_validator("style")
    @classmethod
    def style_allowed(cls, v: str) -> str:
        if v not in STYLES:
            raise ValueError(f"style must be one of: {', '.join(STYLES)}")
        return v


@app.post("/api/generate")
async def generate(req: GenerateRequest, request: Request, response: Response) -> Workout:
    env = request.scope["env"]
    # Throttle before the AI call. CF-Connecting-IP is set by Cloudflare on
    # every edge request (and by wrangler dev locally).
    ip = request.headers.get("cf-connecting-ip", "unknown")
    outcome = await env.GENERATE_LIMITER.limit(to_js({"key": ip}))
    if not outcome.success:
        raise HTTPException(
            429, "Too many workouts in a short time — wait a minute and try again."
        )
    budget = env.CLAUDE_BUDGET.getByName("global")
    limit = int(env.CLAUDE_DAILY_LIMIT)
    ip_limit = int(env.CLAUDE_DAILY_LIMIT_PER_IP)
    # Only a hash is stored — the budget needs to tell clients apart, not know them.
    ip_hash = hashlib.sha256(ip.encode()).hexdigest()[:32]

    async def spend() -> bool:
        return await budget.try_spend(limit, ip_hash, ip_limit)

    try:
        workout, engine = await generate_workout(
            env.AI, req.equipment, req.style, req.duration, req.custom,
            req.avoid, req.nonce, req.engine, spend,
        )
    except (UpstreamError, EquipmentNotUsed) as e:
        raise HTTPException(502, str(e))
    except Exception as e:
        # JS-side errors (Workers AI outages, rate limits) surface as generic
        # FFI exceptions — map anything unexpected to a readable upstream error.
        raise HTTPException(502, f"Workout generation failed: {e}")
    # Which engine actually answered — differs from req.engine after a fallback.
    response.headers["X-Repsheet-Engine"] = engine
    return workout
