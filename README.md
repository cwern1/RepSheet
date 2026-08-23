# Repsheet

Minimal CrossFit workout generator. Pick equipment, style, and duration —
get a WOD in huge type you can read from across the room.

Runs as a single Cloudflare Python Worker: the static frontend is served from
the edge, and `POST /api/generate` calls Workers AI (gpt-oss-120b via the
Responses API, low reasoning effort) through the native `env.AI` binding — no
API keys anywhere. Output is prompted as JSON and validated with Pydantic,
with one retry on malformed shapes.

**Live:** https://repsheet.wodgenerator.workers.dev

## Layout

- `wrangler.jsonc` — the whole deployment as config (worker, static assets, AI binding)
- `src/entry.py` — Worker entrypoint + FastAPI route for `/api/generate`
- `src/generator.py` — prompt, JSON schema, Workers AI call, equipment validation
- `static/` — vanilla HTML/CSS/JS, no build step

Every piece of equipment you tick is guaranteed to appear in the workout —
enforced in the prompt and re-checked server-side (one corrective retry).
Malformed model output is retried once before surfacing an error.

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
