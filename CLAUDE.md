# Repsheet — working notes for Claude

Single Cloudflare **Python** Worker. `README.md` covers what the product is; this file
covers what an agent gets wrong.

## Hard rules

- **Never install npm packages.** No `npm install`, no `npx`, no `package.json`. Python
  deps go through `uv`; wrangler is invoked only as `uv run pywrangler …`. Node exists
  solely as the runtime under Cloudflare's CLI.
- **Node 22, always.** Prefix the PATH before any pywrangler command — Node 26 removed
  `--experimental-wasm-stack-switching` and breaks the Pyodide toolchain:
  ```
  export PATH=/opt/homebrew/opt/node@22/bin:$PATH
  ```
- **`static/` has no build step.** Edit `index.html` / `app.js` / `style.css` directly.
  Never add a bundler, a framework, or a transpiler.
- **Deploy freely; commit only when asked.** `uv run pywrangler deploy` does not need
  permission — ship a finished change so Chris can try it on his phone, since iOS is
  only reachable through the deployed site, not `localhost`. Git commits wait for him
  to ask.
- **Don't re-add CI.** `.github/workflows/deploy.yml` was deleted deliberately in
  `cd98ff5` — Chris does not want to manage a Cloudflare API token. Deploys are manual,
  from this machine, over the `pywrangler login` OAuth session.

## Dev server

```
export PATH=/opt/homebrew/opt/node@22/bin:$PATH
uv run pywrangler dev        # http://localhost:8787
```

**Check whether one is already running before you start another:**

```
lsof -nP -iTCP:8787 -sTCP:LISTEN
```

Two instances share `.wrangler/state`. The second one silently takes a free port
(8788), looks healthy, then dies on its first reload with
`SQLITE_BUSY … NOSENTRY database is locked`. Reuse the running server instead of
starting a second, and don't kill Chris's without asking.

## Testing — locally, no npm

There is no test suite. Verification is manual, in two halves:

**Backend / prompt changes — curl.** This exercises the whole worker path (FastAPI
validation → `env.AI` → prompt → JSON parse → Pydantic → equipment re-check) with no
browser at all:

```
curl -s -X POST http://localhost:8787/api/generate \
  -H 'Content-Type: application/json' \
  -d '{"equipment":["Kettlebell","Bodyweight"],"style":"AMRAP","duration":12,"custom":""}'
```

A generation takes **~14 s** and is a **real** Workers AI call — there is no local mock.
Free tier is 10k neurons/day, so it costs pennies, but don't loop over it.

Worth curling deliberately: an unticked-equipment case (nothing outside the list may
appear), each of the five styles, and a `custom` string that contradicts the equipment
list (it must be silently ignored, never acknowledged in the output).

**UI changes — Brave, by hand.** No browser automation is installed and none should be
added. Open it and hand off to Chris to look:

```
open -a "Brave Browser" http://localhost:8787
```

Mention explicitly what to check. The layout is mobile-first — the honest test is Brave's
device toolbar at iPhone width (390×844), not a desktop window.

## Architecture

- `wrangler.jsonc` — the entire deployment as config. `assets` serves `./static/` from the
  edge; `run_worker_first: ["/api/*"]` means only the API touches Python. The `ai` binding
  is why there are **no API keys anywhere** — don't introduce `.dev.vars` or `wrangler secret`.
- `src/entry.py` — `WorkerEntrypoint` → `asgi.fetch` → FastAPI. One route,
  `POST /api/generate`. Everything non-2xx surfaces as a 502 with a readable `detail`.
- `src/generator.py` — the substance. Two things surprise people:
  - The model is called with the **OpenAI Responses API** shape through the binding
    (`input`, `reasoning: {effort}`, results in `output[]`) — *not* chat-completions.
  - **Two independent retries.** `_request_with_shape_retry` retries once on malformed
    JSON; separately, `generate_workout` checks `_missing_equipment()` and does one
    *corrective* retry that tells the model exactly what it left out before raising
    `EquipmentNotUsed`. Preserve both when refactoring.

## Two virtualenvs — don't conflate them

`.venv/` is **host tooling** (CPython 3.12, provides `pywrangler`). `.venv-workers/` and
`python_modules/` mirror the **Worker runtime** (CPython 3.13 / Pyodide, locked separately
in `pylock.toml`).

`src/*.py` **cannot be imported by the host interpreter** — `import asgi`,
`from workers import …` and `from js import Object` exist only inside the Worker. Don't
try to run or lint them under `.venv/python`.

## Invariants kept in sync by hand

These drift silently; change both sides together.

| | `src/` | `static/app.js` |
|---|---|---|
| styles | `STYLES` in `generator.py` | `STYLES` |
| custom-text cap | `max_length=500` on `GenerateRequest.custom` | `CUSTOM_MAX = 500` |
| duration range | `ge=5, le=60` on `GenerateRequest.duration` | `DURATIONS` |

## Editing SYSTEM_PROMPT

`SYSTEM_PROMPT` in `src/generator.py` is the product — nearly all the domain knowledge
lives there, and it has been tuned by hand over many iterations. Read it fully before
changing it, and prefer adding a narrow rule over rewriting a section.

Prompt changes are behavioural: they can only be judged by **generating several workouts
across different styles and durations and reading them as a coach would**. One good
sample proves nothing. Say plainly when a change is under-tested rather than declaring it
done.

## Tests (not yet written)

A pytest suite is intended but doesn't exist. When adding it: it can only cover the pure
helpers (`_missing_equipment`, `_extract_text`, the `Workout`/`Movement` models), and it
will need `sys.modules` shims for `js`, `pyodide.ffi`, `asgi` and `workers` because those
are imported at module scope. Add `pytest` to the `dev` dependency group and run it with
`uv run --group dev pytest`. Until that exists, curl plus Brave is the whole test story.
