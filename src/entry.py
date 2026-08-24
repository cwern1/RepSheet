import asgi
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, field_validator
from workers import WorkerEntrypoint

from generator import (
    MODEL,
    STYLES,
    EquipmentNotUsed,
    UpstreamError,
    Workout,
    generate_workout,
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
    # Experiment (model-comparison branch): per-request model override for the
    # A/B harness. None → the production MODEL.
    model: str | None = Field(None, max_length=80)
    # Experiment: reasoning effort for gpt-oss models. None → "medium".
    effort: str | None = None

    @field_validator("effort")
    @classmethod
    def effort_allowed(cls, v: str | None) -> str | None:
        if v is not None and v not in ("low", "medium", "high"):
            raise ValueError("effort must be low, medium or high")
        return v

    @field_validator("style")
    @classmethod
    def style_allowed(cls, v: str) -> str:
        if v not in STYLES:
            raise ValueError(f"style must be one of: {', '.join(STYLES)}")
        return v


@app.post("/api/generate")
async def generate(req: GenerateRequest, request: Request) -> Workout:
    env = request.scope["env"]
    try:
        return await generate_workout(
            env.AI, req.equipment, req.style, req.duration, req.custom,
            req.avoid, req.nonce, req.model or MODEL, req.effort or "medium",
        )
    except (UpstreamError, EquipmentNotUsed) as e:
        raise HTTPException(502, str(e))
    except Exception as e:
        # JS-side errors (Workers AI outages, rate limits) surface as generic
        # FFI exceptions — map anything unexpected to a readable upstream error.
        raise HTTPException(502, f"Workout generation failed: {e}")
