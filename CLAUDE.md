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

Every generation is a **real**, paid model call — there is no local mock. Without an
`engine` field this hits the default, **Claude** (~5 s, spends prepaid AI Gateway
credits); add `"engine":"oss"` for gpt-oss (~14 s, Workers AI on the Workers Paid plan,
fractions of a cent). Don't loop over either.

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
- `src/generator.py` — the substance. Things that surprise people:
  - **Two engines, picked per request** (`engine` field, chips in the UI):
    `"sonnet"` (default) = `anthropic/claude-sonnet-5.5` at effort `medium` with
    `SYSTEM_PROMPT_CLAUDE` and relaxed quality checks; `"oss"` = `@cf/openai/gpt-oss-120b`
    with `SYSTEM_PROMPT` and strict checks. Never edit one prompt to suit the other.
    Benchmarks: `experiments/` on the `sonnet-prompt-v2` branch.
  - Claude goes through the **same `env.AI` binding** but is billed via AI Gateway
    Unified Billing (prepaid credits, `{gateway: {id: "default"}}`), in the
    **Anthropic Messages** shape (`system`, `messages`, `output_config.effort`). gpt-oss
    uses the **OpenAI Responses API** shape (`input`, `reasoning: {effort}`, results in
    `output[]`). Neither is chat-completions.
  - **Fallback:** when the Claude call itself fails (out of credits — `2021`, gateway
    errors), `generate_workout` regenerates on gpt-oss. Model-quality failures are not
    retried on the other engine. The `X-Repsheet-Engine` response header says which
    engine answered.
  - **Daily Claude budget:** every Claude call (retries included) first asks the
    `ClaudeBudget` Durable Object (`src/entry.py`) to spend one of
    `CLAUDE_DAILY_LIMIT` for the UTC day, and one of `CLAUDE_DAILY_LIMIT_PER_IP` for
    that client (`wrangler.jsonc` `vars`; IPs stored only as hashes); refused → gpt-oss.
    This is the money guard — `GENERATE_LIMITER` is per-machine and leaky by design.
    Locally the count persists in `.wrangler/state`, so once it's spent your dev server
    serves gpt-oss for the rest of the day; test with
    `uv run pywrangler dev --var CLAUDE_DAILY_LIMIT:2` (or `CLAUDE_DAILY_LIMIT_PER_IP:2`).
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
| engines | `ENGINES` in `generator.py` | `ENGINES` / `ENGINE_LABELS` |

## Editing SYSTEM_PROMPT

There are two prompts: `SYSTEM_PROMPT_CLAUDE` (default engine) and `SYSTEM_PROMPT`
(gpt-oss, the fallback). `SYSTEM_PROMPT` in `src/generator.py` is the product — nearly all the domain knowledge
lives there, and it has been tuned by hand over many iterations. Read it fully before
changing it, and prefer adding a narrow rule over rewriting a section.

Prompt changes are behavioural: they can only be judged by **generating several workouts
across different styles and durations and reading them as a coach would**. One good
sample proves nothing. Say plainly when a change is under-tested rather than declaring it
done.

### How variation works

Identical inputs used to give near-identical workouts — the model has no memory
between calls, so the old "vary between workouts" line was unenforceable. Two
mechanisms replace it, both in the **user** message:

- **Programming angle.** One `PATTERN_ANGLES` + one `STIMULUS_ANGLES` entry per request,
  chosen by `_variation_brief()`. Seeded from the client's `nonce` — Workers restricts
  entropy during global-scope evaluation, and a fixed nonce pins the angle, which is the
  only way to test the conflict cases. Keep these tuples free of *structural* angles
  ("make it a couplet"): those fight the style blueprints.
- **Avoid-list.** `static/app.js` keeps the last 3 workouts' movement names in
  `state.recent` (in memory only — never persisted) and sends them as `avoid`.
- **Movement count.** `_movement_count()` draws a target from the same seeded
  rng (after the angles, so nonce pins are unchanged) and the user message
  states it. It is deliberately decoupled from the equipment count: before it
  existed, both prompts' "couplet or triplet" default plus the coverage rule
  produced exactly one movement per ticked item. The count is the one
  structural dial allowed because it is style-aware (`_COUNT_DRAWS`; EMOM picks
  only station counts whose rotation divides the minutes, Chipper 6–8). Both
  prompts tell the model to take depth from one rich implement (barbell,
  dumbbells, kettlebell, bodyweight, pull-up bar) rather than spread thin —
  the CrossFit Open is the benchmark (22.3, 25.3, 24.1). Watch for the
  cross-implement repeat this invites (DB Push Press + KB Push Press);
  `_quality_problems` flags it on both engines and the corrective retry fixes it.

Precedence, encoded in the prompt and worth re-testing after any edit:
**equipment rules > style blueprint > athlete request > programming angle.** The angle
is always the first thing sacrificed.

Two failure modes to watch when tuning: an angle that turns every movement into the same
pattern (a four-station pressing EMOM), and an angle that quietly overrides a `custom`
restriction. Both are guarded in the prompt; neither guard is absolute.

## Tests (not yet written)

A pytest suite is intended but doesn't exist. When adding it: it can only cover the pure
helpers (`_missing_equipment`, `_extract_text`, the `Workout`/`Movement` models), and it
will need `sys.modules` shims for `js`, `pyodide.ffi`, `asgi` and `workers` because those
are imported at module scope. Add `pytest` to the `dev` dependency group and run it with
`uv run --group dev pytest`. Until that exists, curl plus Brave is the whole test story.
