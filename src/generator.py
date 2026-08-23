"""Workout generation via the Workers AI binding (gpt-oss-120b, Responses API)."""

import json
import random

from js import Object
from pydantic import BaseModel, ValidationError
from pyodide.ffi import JsProxy, to_js as raw_to_js

MODEL = "@cf/openai/gpt-oss-120b"

STYLES = ["AMRAP", "For Time", "EMOM", "Chipper", "Intervals"]

SYSTEM_PROMPT = """\
You are an elite CrossFit programmer. You write a single WOD (workout of the day)
and nothing else: no warm-up, no cool-down, no coaching chatter.

EQUIPMENT — hard rules:
- Every item the athlete lists MUST be used by at least one movement.
- Equipment NOT listed must never appear. If the list is empty, program a pure
  bodyweight WOD.
- "Bodyweight" appears in the list like any other item. When it is listed,
  program at least one bodyweight movement (burpees, sit-ups, air squats,
  push-ups, lunges, running) and tag those movements ["Bodyweight"]. When it is
  NOT listed, program ZERO bodyweight movements — every single movement must
  use a listed implement.
- Tag each movement's `equipment` field with the exact item names from the
  athlete's list that it uses.
- Only program movements that are physically possible with what is listed. There
  is never a squat rack or bench: every barbell movement must start from the
  floor or the hang (no back squats, no bench press). If "Bodyweight" is the
  only item (or the list is empty), use only floor movements and running — no
  pull-ups, no hangs.
- Use only well-known, real CrossFit movements. Never invent hybrid movements.
- Program for a fit amateur: no elite-skill gymnastics (no muscle-ups, no
  handstand push-ups or walks). Pull-ups, dips, and toes-to-bar are fine.
- A movement's name must match its equipment tag: a burpee over the bar is
  "Bar-Facing Burpee", calories on the Assault Bike are "Assault Bike", not
  "Row".
- Never program timed holds (plank, L-sit, wall sit) anywhere — every movement
  is countable reps, calories, or distance.

STYLE BLUEPRINTS — follow the requested style exactly:
- AMRAP: `format_line` "AMRAP {target} min". The movement list is ONE round that
  the athlete repeats as many times as possible; one round should take a fit
  amateur 2–4 minutes. `scheme` must be null — an AMRAP never has a fixed number
  of rounds.
- For Time: fixed total work, `format_line` "For Time · cap {target+3} min".
  Either `scheme` "5 Rounds" with per-round reps on each movement, OR a rep
  ladder: then set EVERY movement's `reps` to the ladder itself ("21-15-9") and
  `scheme` to null. Budget honestly: a fit amateur sustains about 15 reps per
  minute, so total reps across ALL rounds ≈ 15 × target minutes, within ±30%
  (10 min ≈ 150 reps, 20 min ≈ 300). A single short pass is far too little —
  use multiple rounds to reach the budget, and never use "1 Round" as a scheme
  (a single pass means `scheme` null).
- EMOM: `format_line` "EMOM {target}". The number of movements MUST divide the
  total minutes evenly; put the rotation in `scheme` (e.g. "4 stations × 5
  rounds"). Each minute's work must take 35–45 seconds for a fit amateur —
  never more than 15 cal in a single minute.
- Chipper: one long list done once, top to bottom, big rep counts trending
  downward. `format_line` "Chipper · cap {target} min", 6–8 movements.
- Intervals: `format_line` states the exact structure, e.g. "5 × 3 min on /
  1 min rest", and it must fill the target duration exactly. EVERY interval
  repeats the SAME work: the movement list is one interval's work, and
  together the movements must nearly fill the "on" window — about 15 reps or
  12 cal per minute of window (a 3-min window ≈ 45 reps or 35 cal total).
  Never alternate different work between intervals. Pacing goes in `notes`.

LOADS:
- Every movement that uses a loaded implement (barbell, dumbbells, kettlebell,
  wall ball, sandbag) MUST have `load_kg`, always with the unit: "40 kg",
  never "40". Machines and bodyweight movements get null.
- Kilograms only, rounded to standard plate math (40, 50, 60 kg; bells 12.5,
  16, 20, 22.5, 24 kg; wall balls 6 or 9 kg). Moderate loads a fit amateur can
  cycle for the given reps. Dumbbells: "2×22.5 kg" when both hands are loaded, "22.5 kg" for
  single-bell movements like the dumbbell snatch — and use ONE dumbbell weight
  for the entire workout; nobody swaps pairs mid-WOD.

FORMAT:
- `reps` strings are terse: "21", "15 cal", "400 m", "12/leg", "12/arm".
  Nothing wordier — never "reps", "calories", or "max effort" spelled out. A
  limb suffix ONLY on genuinely unilateral movements (lunges → "/leg",
  single-arm work → "/arm"); ordinary two-handed movements like wall balls,
  swings, or thrusters get a bare number. "cal" exists only on machines
  (Rower, Assault Bike, Ski Erg) — jump rope work is counted in reps.
- `title`: a punchy one-or-two-word name in the spirit of classic benchmark WODs
  ("Grace", "Iron Lungs", "Dead Air"). It must NOT contain the style name, the
  word "workout", or ANY equipment word — "Sandbag Surge" and "Barbell Burn"
  are wrong. Never use these overused titles: Forge, Pulse, Furnace, Fury,
  Iron, Momentum, Sprint, Cyclone, Brute, Surge, Blitz, Burn. The athlete's
  message includes an inspiration word — let it color the title (theme, mood,
  or wordplay) without using it verbatim.
- `notes`: only a rest scheme or one genuinely necessary instruction; otherwise
  null. Never restate the format or duration, and never contradict the
  structure (no pacing claims that don't match the prescribed work).
- 3–8 movements. Vary movement selection between workouts; do not default to
  the same classic pairings every time.
"""


class Movement(BaseModel):
    reps: str
    name: str
    load_kg: str | None
    equipment: list[str]


class Workout(BaseModel):
    title: str
    format_line: str
    scheme: str | None
    movements: list[Movement]
    notes: str | None
    equipment_used: list[str]


class UpstreamError(Exception):
    pass


class EquipmentNotUsed(Exception):
    def __init__(self, missing: list[str]):
        self.missing = missing
        super().__init__(f"Equipment not used: {', '.join(missing)}")


def to_js(obj):
    return raw_to_js(obj, dict_converter=Object.fromEntries)


def _missing_equipment(workout: Workout, equipment: list[str]) -> list[str]:
    used = {e.lower() for m in workout.movements for e in m.equipment}
    used |= {e.lower() for e in workout.equipment_used}
    return [e for e in equipment if e.lower() not in used]


JSON_INSTRUCTION = (
    "\nOUTPUT: Respond with ONLY the workout as a single JSON object matching this "
    "schema — no prose, no markdown fences:\n"
)


def _extract_text(result) -> str:
    """Pull the assistant text out of a Responses API result."""
    if isinstance(result, str):
        return result
    if text := result.get("output_text"):
        return text
    for item in result.get("output", []):
        if item.get("type") == "message":
            for part in item.get("content", []):
                if part.get("type") == "output_text":
                    return part["text"]
    raise KeyError("no assistant text in model output")


async def _request(ai, messages: list[dict]) -> Workout:
    # gpt-oss models speak the OpenAI Responses API through the binding:
    # `input` instead of `messages`, output as an `output[]` item list.
    result = await ai.run(
        MODEL,
        to_js(
            {
                "input": messages,
                "reasoning": {"effort": "low"},
                "max_output_tokens": 2000,
            }
        ),
    )
    if isinstance(result, JsProxy):
        result = result.to_py()
    text = _extract_text(result).strip()
    if text.startswith("```"):
        text = text.strip("`").removeprefix("json").strip()
    return Workout.model_validate(json.loads(text))


async def _request_with_shape_retry(ai, messages: list[dict]) -> Workout:
    try:
        return await _request(ai, messages)
    except (json.JSONDecodeError, ValidationError, KeyError, TypeError, AttributeError):
        try:
            return await _request(ai, messages)
        except (json.JSONDecodeError, ValidationError, KeyError, TypeError, AttributeError):
            raise UpstreamError("The model returned a malformed workout twice")


# Per-request title inspiration: breaks the model's habit of converging on the
# same few names when sampling from an identical prompt.
TITLE_SEEDS = [
    "thunderstorm", "furnace room", "last lap", "high tide", "gravel road",
    "december", "wolf pack", "power outage", "freight train", "heat wave",
    "quicksand", "avalanche", "second wind", "rust", "jet lag", "wildfire",
    "undertow", "scrapyard", "monsoon", "vertigo", "moonshot", "flash flood",
    "tumbleweed", "afterburner", "gridlock", "riptide", "sawdust", "blackout",
    "switchback", "landslide", "crosswind", "furlough", "magma", "static",
    "detour", "overtime", "ricochet", "downpour", "turbine", "fault line",
]


async def generate_workout(ai, equipment: list[str], style: str, duration_min: int) -> Workout:
    equipment_text = ", ".join(equipment) if equipment else "none (bodyweight only)"
    user_prompt = (
        f"Equipment available (use ALL of it): {equipment_text}\n"
        f"Style: {style}\n"
        f"Target duration: about {duration_min} minutes\n"
        f"Title inspiration word: {random.choice(TITLE_SEEDS)}"
    )
    system = SYSTEM_PROMPT + JSON_INSTRUCTION + json.dumps(Workout.model_json_schema())
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_prompt},
    ]

    workout = await _request_with_shape_retry(ai, messages)
    missing = _missing_equipment(workout, equipment)
    if not missing:
        return workout

    # One corrective retry: tell the model exactly what it left out.
    messages += [
        {"role": "assistant", "content": workout.model_dump_json()},
        {
            "role": "user",
            "content": (
                f"You did not use: {', '.join(missing)}. Regenerate the workout "
                "using ALL listed equipment, and no equipment outside the list."
            ),
        },
    ]
    workout = await _request_with_shape_retry(ai, messages)
    missing = _missing_equipment(workout, equipment)
    if missing:
        raise EquipmentNotUsed(missing)
    return workout
