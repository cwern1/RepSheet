import asgi
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from workers import WorkerEntrypoint

from generator import (
    STYLES,
    EquipmentNotUsed,
    UpstreamError,
    Workout,
    generate_workout,
    to_js,
)


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

    @field_validator("style")
    @classmethod
    def style_allowed(cls, v: str) -> str:
        if v not in STYLES:
            raise ValueError(f"style must be one of: {', '.join(STYLES)}")
        return v


@app.post("/api/generate")
async def generate(req: GenerateRequest, request: Request) -> Workout:
    env = request.scope["env"]
    # Throttle before the AI call. CF-Connecting-IP is set by Cloudflare on
    # every edge request (and by wrangler dev locally).
    ip = request.headers.get("cf-connecting-ip", "unknown")
    outcome = await env.GENERATE_LIMITER.limit(to_js({"key": ip}))
    if not outcome.success:
        raise HTTPException(
            429, "Too many workouts in a short time — wait a minute and try again."
        )
    try:
        return await generate_workout(
            env.AI, req.equipment, req.style, req.duration, req.custom,
            req.avoid, req.nonce,
        )
    except (UpstreamError, EquipmentNotUsed) as e:
        raise HTTPException(502, str(e))
    except Exception as e:
        # JS-side errors (Workers AI outages, rate limits) surface as generic
        # FFI exceptions — map anything unexpected to a readable upstream error.
        raise HTTPException(502, f"Workout generation failed: {e}")
