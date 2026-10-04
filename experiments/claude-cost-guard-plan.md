# Plan: cost guard for a paid Claude model

Status: **parked** (2026-10-04). Only worth building if the Opus 5.5 benchmark on
this branch shows Claude is better enough to pay for. Nothing below is implemented.

## Why the existing rate limit isn't enough

`GENERATE_LIMITER` (6/min per IP) slows a client down but sets no budget:
6 × 60 × 24 ≈ 8,600 requests/day from **one** IP. At ~$0.07 per Opus generation,
that's about **$600/day per script**, multiplied by however many IPs an abuser
has. The fix is a ceiling in **money**, not requests per minute.

Cost reference (Opus 5.5 via Cloudflare, Oct 2026): $4 / 1M input, $20 / 1M
output, plus a 5% fee on credit purchases. System prompt ≈ 3.8k tokens.
- Typical generation: ~$0.05–0.08.
- Worst case for one call (5k in + `max_tokens` 8k out): ~$0.18.
- Worst case for one request: up to 4 calls (shape retry × corrective retry),
  so ~$0.70.

## Layer 1: prepaid credits, auto top-up off (dashboard only, no code)

1. Cloudflare dashboard → AI → AI Gateway → Credits Available → Manage.
2. Load a small balance ($10–20).
3. Leave **auto top-up off**.

When credits run out, Claude calls fail with
`AiGatewayError: 2021: Insufficient AI Gateway credits` (seen on 2026-10-04).
With layer 2 in place, that error also triggers the gpt-oss fallback, so users
never see it.

Caveat from Cloudflare's docs: the balance "may go negative", and the card on
file is charged monthly. So this is a near-hard cap. Keep the balance small and
let layer 2 be the real limit.

## Layer 2: global daily Claude budget, with fallback to gpt-oss

**Behaviour:** count Claude **calls** (not requests, so retries count) per UTC
day across all users. Once the count reaches `CLAUDE_DAILY_LIMIT`, the rest of
the day's requests silently use `@cf/openai/gpt-oss-120b`, the current
production model. Users always get a workout, and daily Claude spend is capped
at about `limit × $0.18`.

**Why a Durable Object:** it's one single-threaded instance, so check-and-increment
is exact even under concurrent requests. KV is eventually consistent and would
overshoot. The per-IP rate-limit binding is per-location and approximate.

### Config (`wrangler.jsonc`)

```jsonc
"vars": { "CLAUDE_DAILY_LIMIT": "150" },   // ≈ $11/day worst case; a number, not a secret
"durable_objects": {
  "bindings": [{ "name": "CLAUDE_BUDGET", "class_name": "ClaudeBudget" }]
},
"migrations": [{ "tag": "v1", "new_sqlite_classes": ["ClaudeBudget"] }]
```

### Code sketch (verify the Python DO API against current docs before writing)

`src/entry.py`: the DO class must be exported from the main module.

```python
from workers import DurableObject

class ClaudeBudget(DurableObject):
    async def try_spend(self, limit: int) -> bool:
        key = f"calls:{utc_date_string()}"
        used = await self.ctx.storage.get(key) or 0
        if used >= limit:
            return False
        await self.ctx.storage.put(key, used + 1)
        return True
```

Call site: inside `_request` in `generator.py`, right before the
`anthropic/` branch's `ai.run`.

```python
stub = env.CLAUDE_BUDGET.get(env.CLAUDE_BUDGET.idFromName("global"))
if not await stub.try_spend(int(env.CLAUDE_DAILY_LIMIT)):
    model = MODEL  # fall back to gpt-oss for this call
```

Design points:
- **Thread the choice through.** Once a request falls back, its retries should
  use gpt-oss too. The simplest way is for `generate_workout` to decide the model
  once per call via a small `pick_model(env)` helper, and to pass `env` (or the
  stub) down, since today only `env.AI` is passed.
- **Fail closed.** If the DO call itself throws, use gpt-oss rather than Claude.
- **Make the fallback observable.** Add `print()` a log line (Workers
  observability is on) and/or an `X-Model` response header, so the dashboard and
  testing can tell which model answered.
- **Clean up old days.** Old date keys are harmless (a few bytes each); optionally
  delete yesterday's key on first write of a new day.
- **Keep both retries.** CLAUDE.md requires that `_request_with_shape_retry` and
  the corrective retry survive any refactor.

### Testing

1. Locally, with `CLAUDE_DAILY_LIMIT` set to `"2"`, send 3 generations with the Claude
   model. The first two should be Claude, and the third should come back as gpt-oss
   (check the `X-Model` header or the log). Watch for corrective retries eating
   budget: a retry on request 1 can make request 2 fall back. That's correct
   behaviour.
2. Restart `pywrangler dev` to confirm the count persists in `.wrangler/state`.
3. Deploy. The first deploy applies the `v1` migration. Then send one prod request
   and confirm it's served by Claude in the AI Gateway logs.

### Open questions for later

- Is there a per-IP daily cap too (same DO, key `ip:{date}:{ip}`)? That stops one
  person from exhausting everyone's Claude budget. This was layer 3 in the
  original discussion, and it's cheap to add here.
- Should the daily limit reset at UTC midnight, or at local midnight (Europe/Berlin)?
- Does AI Gateway now offer a native spend limit or budget alert? Check
  before building. If it does, it could replace layer 1's caveat.
