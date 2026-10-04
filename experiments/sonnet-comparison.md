# Round 3: Claude Sonnet 5.5 vs gpt-oss-120b (2026-10-04)

Branch `claude-opus-benchmark`. Raw data and judge artifacts are in `harness/round3/`.

## Setup

- **Baseline:** `@cf/openai/gpt-oss-120b` at reasoning effort `low`, the current
  production model. It uses the Responses API through Workers AI.
- **Candidate:** `anthropic/claude-sonnet-5.5` at `output_config.effort: "low"`. It
  uses the Anthropic Messages shape through the same `env.AI` binding, with
  `{gateway: {id: "default"}}`, paid from AI Gateway Unified Billing credits.
  Sonnet 5.5 isn't listed in Cloudflare's model catalog (2026-10-04), but the
  binding serves it.
- **Prompt and checks:** the same `SYSTEM_PROMPT`, validators and both retries as
  production. There were no Claude-specific prompt changes.
- **Cases and transport:** the same 50 fixed cases as rounds 1–2, with pinned
  nonces, run through `pywrangler dev` at concurrency 3 and timed on the client.
  Cases were **interleaved per model**, so both models ran in the same time
  window.
- **Analysis:** deterministic re-validation via `harness/analyze.py`, then blind
  A/B judging by 5 Fable 5.1 agents (10 cases each, primed with the full
  `SYSTEM_PROMPT`, no access to the mapping).

## Results

| | gpt-oss-120b @ low | **Claude Sonnet 5.5 @ low** |
|---|---|---|
| Succeeded | 49 / 50 | 49 / 50 |
| Clean (no deterministic violations) | 35 / 49 (71%) | **46 / 49 (94%)** |
| Total violations | 18 | **3** |
| Median latency | 12.4 s | **2.4 s** |
| Mean latency | 14.9 s | **3.9 s** |
| p90 latency | 27.5 s | **7.8 s** |
| Judge: mean rank (1 = best) | 1.74 | **1.26** |
| Judge: mean score / 10 | 4.84 | **6.22** |
| Judge: case wins | 13 | **37** |

Sonnet won the judged comparison in every style:

| Style | Sonnet wins | gpt-oss wins |
|---|---|---|
| Chipper | 8 | 0 |
| AMRAP | 9 | 5 |
| For Time | 8 | 3 |
| EMOM | 7 | 3 |
| Intervals | 5 | 2 |

Excluding the two failed cases, Sonnet wins 36 / 48, with a mean score of 6.33 vs 4.96.

### gpt-oss-120b weaknesses, unchanged from round 2

- Chipper reps over the ceilings (4 cases).
- EMOM minutes that overflow.
- Interval work that doesn't fit its window (3 cases).
- Two badly underfilled time budgets.

Its hard failure was the perennial case 1 (bodyweight EMOM 7): it kept adding
pull-ups, and the corrective retry couldn't stop it.

### Sonnet 5.5 weaknesses (from the judges' notes where it lost)

- **Underfills.** Intervals sometimes use less than ¾ of the window, and a
  couple of For Time pieces come in short (~21 of 30 min, ~11.5 of 15).
- **Format slips.** It sometimes drops `/leg` on lunges.
- **Soft coverage.** Twice it had three hinges, or no dedicated upper-body movement.
- **Soft request handling.** It used a Hand-Release Push-up when Push-up was on the
  avoid list, and burpees for "bad knee".

These are craft gaps, not rule breaks. Deterministic violations: one EMOM 30
station count that doesn't divide, one case with two barbell loads, one short
chipper.

## Finding: Sonnet "self-corrects" in plain text, which breaks parsing

On 6 of the ~55 Sonnet calls, the model emitted a JSON workout, then a line like
*"Wait — that violates the structure; corrected version below."*, then a second,
corrected JSON object. `_extract_json` slices from the first `{` to the last `}`,
spanning both objects, so `json.loads` fails with "Extra data" and the shape retry
fires:

- 4 of those requests recovered on retry.
- Case 28 hit it twice and failed ("malformed workout twice"). That is Sonnet's
  only failure.
- The retries are also most of Sonnet's slow tail (11–17 s requests).

**Fix options, cheapest first:**
1. **Parse the *last* complete JSON object** in the text, using
   `json.JSONDecoder.raw_decode` in a loop. The corrected version is the one we
   want, and it's usually better.
2. **Use Anthropic structured output** (`output_config.format` with the `Workout`
   JSON schema). The schema field exists in Cloudflare's input schema but is
   undocumented there. Untested.

Either should bring Sonnet to ~50/50 and cut its p90 further. This was not
re-run, to avoid spending more credits; the numbers above include the failure.

## Cost

Not measured. The wrangler OAuth token can't read AI Gateway logs (auth
error 10000), and the Cloudflare catalog lists no Sonnet 5.5 price. Rough
estimate: ~5k input tokens (the system prompt is ~3.8k) plus well under 1k
output tokens per call. At Sonnet-class pricing that's on the order of
**$0.02–0.03 per workout**, versus a small fraction of a cent for gpt-oss-120b.
That's roughly 10× more per workout, but small in absolute terms. **Check the AI
Gateway dashboard for the real figure** from this run (~55 Sonnet calls).

## Caveats

- **Self-preference risk.** The judges are Claude models, and one contestant is
  Claude. Blinding hides the label, not the style. The deterministic checks don't
  share this bias, and they point the same way, by a wide margin (94% vs 71%
  clean).
- **One sample per case.** Single draws at fixed nonces. The gap is large enough
  that this is unlikely to flip, but per-case judgments are noisy.
- **Tuning bias.** `SYSTEM_PROMPT` was tuned against gpt-oss-120b. Sonnet won
  without any prompt changes, so a Sonnet-specific pass could widen the gap.
- **Opus 5.5 not tested.** The Claude path is model-agnostic, so testing it is one
  line in `harness/run_sonnet.py`.

## Recommendation

Sonnet 5.5 @ low is **better, ~5× faster, and more reliable** than the current
production model. This is the first candidate in three rounds to beat gpt-oss-120b
on quality *and* speed. Before switching production:

1. Fix the double-JSON parsing (option 1 above) and re-run the 50 cases once to
   confirm 50/50.
2. Build the cost guard from `claude-cost-guard-plan.md`: prepaid credits with
   auto top-up off, plus a Durable Object daily budget with fallback to
   gpt-oss-120b. The public endpoint must not be able to spend unboundedly.
3. Read the real per-workout cost from the AI Gateway dashboard and set
   `CLAUDE_DAILY_LIMIT` from it.
