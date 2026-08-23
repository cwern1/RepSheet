# Repsheet

Minimal CrossFit workout generator. Pick equipment, style, and duration —
get a WOD in huge type you can read from across the room.

Runs as a single Cloudflare Python Worker: the static frontend is served from
the edge, and `POST /api/generate` calls Workers AI (gpt-oss-120b via the
Responses API, medium reasoning effort) through the native `env.AI` binding —
no API keys anywhere. Output is prompted as JSON and validated with Pydantic,
with one retry on malformed shapes.

**Live:** https://repsheet.wodgenerator.workers.dev

## Features

- Equipment chips (incl. Bodyweight and Running as first-class items) — every
  ticked item is guaranteed to appear, enforced in the prompt and re-checked
  server-side with one corrective retry; unticked equipment never appears.
- Styles: AMRAP, For Time, EMOM, Chipper, Intervals — each with a structural
  blueprint in the prompt (round math, time-honest volume budgets, load rules
  in kg, hard caps on grinding movements).
- Regenerate gives a genuinely different workout: every request carries a randomly
  drawn programming angle (movement pattern + stimulus) plus the movements from the
  last few workouts to steer away from. Measured across five successive regenerates,
  mean movement overlap between consecutive workouts fell from ~73% to ~10%.
- "Customize" sheet for free-text prompt tuning — injuries, intensity, movements
  you want in. Appended to the request as a delimited athlete request; the
  equipment list, style blueprint and JSON format still win. Persisted, and the
  button stays lit so a saved note never shapes a workout invisibly.
- Full-screen workout view with fit-to-width poster type (shrinks instead of
  wrapping), screen wake lock while a workout is open ("Prevent lockscreen"
  pill), and a generation overlay with rotating gym-prep messages.
- Installable on the iOS Home Screen (manifest + touch icons, safe-area
  aware); light/dark theme follows the system.

## Layout

- `wrangler.jsonc` — the whole deployment as config (worker, static assets, AI binding)
- `src/entry.py` — Worker entrypoint + FastAPI route for `/api/generate`
- `src/generator.py` — prompt, JSON schema, Workers AI call, equipment validation
- `static/` — vanilla HTML/CSS/JS, no build step

## Develop & deploy

Tooling: [uv](https://docs.astral.sh/uv/) ≥ 0.12 manages Python; Cloudflare's
wrangler runs on Node. **Use Node 22** — Node 26 breaks the Pyodide toolchain
(`--experimental-wasm-stack-switching` was removed):

```
export PATH=/opt/homebrew/opt/node@22/bin:$PATH
```

One-time auth: `uv run pywrangler login`

Local dev (AI calls hit the real Workers AI, pennies at most):

```
uv run pywrangler dev        # http://localhost:8787
```

Deploy:

```
uv run pywrangler deploy
```

Cost: Workers AI free tier is 10k neurons/day; a generated workout is a few
hundred output tokens, so personal use stays comfortably inside it.
