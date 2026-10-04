# Model comparison round 2 — the fast class, re-tested

Experiment run 2026-08-26 on branch `model-comparison-2`. Question: with the
baseline now at reasoning effort **"low"** (~14 s) and the robustness-passed
prompt/validators (`7e79825`), is there a Workers AI model that generates
equal-or-better workouts faster — in particular, do the round-1 rejects
Gemma-4-26B and GLM deserve another look, and what about the newly added
`qwen3-30b-a3b-fp8`?

## What changed since round 1 (`model-comparison.md`, 2026-08-24/25)

- Baseline runs at `reasoning: {effort: "low"}` — the production default since
  `89f0e11`. Round 1 measured it at "medium".
- The prompt/validator robustness pass (vocabulary reverse index,
  canonicalization, tighter validators) landed on main; every model in this run
  benefits from it, so round-1 numbers are not directly comparable.
- **Gemma-4-26B gets `chat_template_kwargs: {enable_thinking: false}`.** Its
  round-1 rejection (~50 s warm) was a thinking-mode artifact: with thinking
  off it answers in ~2–4 s. GLM-4.7-flash stays rejected — round 1 measured
  2.5–3+ min *with* thinking already off.
- **qwen3-30b-a3b-fp8** (MoE, ~3B active params, cheapest text model in the
  catalog) is new. Its vLLM reasoning parser routes the whole answer into
  `message.reasoning`/`reasoning_content` with `content: null` even with
  thinking disabled — `_extract_text` now falls back to those fields.
- Judging was done by five parallel Claude (Fable 5) agents, one batch of 10
  cases each, blind (shuffled A–D, no access to the mapping), primed with the
  full SYSTEM_PROMPT rules.

Method is otherwise identical to round 1: same 50 fixed cases with pinned
nonces, full production path through `pywrangler dev`, concurrency 3,
client wall-clock, deterministic re-validation via `analyze.py`. Raw data in
`harness/results2.jsonl`, judge artifacts in `harness/round2/`.

## Models

| model | role | transport | price (in/out) |
|---|---|---|---|
| `@cf/openai/gpt-oss-120b` @ effort low | baseline (current prod) | Responses API | $0.35 / $0.75 per M tok |
| `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | round-1 fast candidate, re-run | chat completions | $0.29 / $2.25 per M tok |
| `@cf/qwen/qwen3-30b-a3b-fp8` | new candidate | chat completions + JSON-schema mode, thinking off | $0.051 / $0.34 per M tok |
| `@cf/google/gemma-4-26b-a4b-it` | round-1 reject, re-tested | chat completions + JSON-schema mode, thinking off | $0.10 / $0.30 per M tok |

## Results summary

| model | ok | med time | mean | p90 | min–max | clean workouts | violations | hard failures |
|---|---|---|---|---|---|---|---|---|
| gpt-oss-120b @ low | 50/50 | 17.1s | 18.2s | 28.5s | 5.0–47.6s | 36/50 (72%) | 22 | 0 |
| llama-3.3-70b-fast | 47/50 | 7.6s | 7.7s | 12.8s | 2.5–17.2s | 39/47 (83%) | 14 | 3 |
| qwen3-30b-a3b | 41/50 | 3.1s | 3.3s | 4.7s | 1.5–6.1s | 11/41 (27%) | 47 | 9 |
| gemma-4-26b | 48/50 | 4.3s | 9.3s | 16.4s | 1.8–81.3s | 35/48 (73%) | 21 | 2 |

Timing notes: the baseline's 17.1 s median (vs ~14 s single-request) includes
concurrency-3 contention; relative gaps are the honest signal. Gemma's mean is
dragged by five cold-start outliers (16–81 s); its warm behavior is the 4.3 s
median. Qwen's tail is astonishingly flat: p90 4.7 s, max 6.1 s *including*
corrective retries.

## Blind judge results (5 × Fable 5 agents, per-case ranking)

| model | mean rank (1=best) | mean score /10 | case wins |
|---|---|---|---|
| gpt-oss-120b @ low | 1.80 | 6.0 | 24 |
| llama-3.3-70b-fast | 2.32 | 5.0 | 15 |
| gemma-4-26b | 2.34 | 5.1 | 10 |
| qwen3-30b-a3b | 3.54 | 3.1 | 1 |

## Conclusions

1. **gpt-oss-120b at effort low is still the best programmer** — best rank
   (1.80), most case wins (24), the only model with zero unrecoverable
   failures. The quality gap to the fast class did not close: judges kept
   seeing the same craft edge (honest time fit, pattern balance, load sanity).
2. **Gemma-4-26B is rehabilitated and joins llama-3.3 as a viable fast base.**
   Round 1's ~50 s was thinking tokens, nothing else. With thinking off it is
   statistically tied with llama-3.3 on judge rank (2.34 vs 2.32, slightly
   higher mean score), matches the baseline's deterministic clean rate
   (73% vs 72%), runs 4.3 s median warm — and is the second-cheapest model
   tested. Weaknesses: chipper rep ceilings, occasional EMOM structure slips,
   two coverage failures, and a cold-start tail (5 of 48 runs took 16–81 s)
   that a latency-sensitive UI would feel.
3. **llama-3.3-70b-fast improved under the robustness-passed prompt**: 83%
   deterministic clean rate (was 67%), now above the baseline's, at 7.6 s
   median. But it failed 3 cases outright (equipment coverage, including its
   perennial 4-machines EMOM 30) and the judges still place it half a rank
   behind baseline — the arithmetic-and-balance gap is unchanged.
4. **qwen3-30b-a3b is disqualified despite being the fastest thing we have
   ever measured** (3.1 s median, 6.1 s max). It hallucinates pull-up-bar and
   ring movements onto bodyweight-only equipment lists so persistently that
   the corrective retry cannot save it: 9 hard failures, 27% clean, judge rank
   3.54 with a single case win. One case also leaked chain-of-thought into the
   `scheme` field.
5. Cost remains a non-factor — every candidate lands at small fractions of a
   cent per workout.

## Recommendation

Unchanged from round 1 in substance: **keep gpt-oss-120b in production** —
nothing matches its programming quality, and effort "low" already banked the
easy 2.3× speedup.

If a fast mode is ever wanted, the base model choice is now a genuine
two-horse race, and the calculus shifted:

- **gemma-4-26b** — 4.3 s warm, near-baseline clean rate, cheapest viable,
  but cold-start spikes and slightly more structural slips.
- **llama-3.3-fast** — 7.6 s, best deterministic clean rate of the whole
  field, no cold-start tail, but pricier output tokens and stubborn hard
  failures on wide equipment lists.

Either would need the same prompt-tuning pass round 1 prescribed (blueprint
arithmetic wording, coverage emphasis) before adoption. The prefetch-a-second-
workout UX route from round 1 still sidesteps the tradeoff entirely and keeps
120b quality; it remains the better first move if regenerate latency is the
pain.

## Violation breakdown (deterministic, `analyze.py`)

**gpt-oss-120b @ low** — 22 violations: 8 × chipper reps over ceiling,
4 × EMOM minute overflows, 4 × interval window overflow, 2 × repeated base
lift, and singles (two dumbbell loads, 9 movements, short chipper ×2).

**llama-3.3-70b-fast** — 14 violations: 6 × repeated base lift, 2 × EMOM token
minute, 2 × movement-count overflow (10 and 12 movements), 3 × chipper volume,
1 × interval overflow. Failures: case 2 (invented "Burpee Pull-up"), cases 6
and 29 (equipment coverage on wide lists).

**qwen3-30b-a3b** — 47 violations dominated by repeated base lifts (12),
duplicate movements (4), oversized AMRAP rounds (7), for-time cap blowouts
(4). Failures (9): pull-up/ring/chin-up movements without the equipment in
cases 1, 11, 26, 27, 28, 38, 46; wall-ball coverage in 25; rower contradiction
in 47.

**gemma-4-26b** — 21 violations: 4 × chipper reps over ceiling, 2 × duplicate
movement, 2 × EMOM token minute, 2 × repeated base lift, 1 × EMOM divisibility,
plus scattered interval/chipper volume slips. Failures: case 15 (invented
"Dumbbell Goblet Squat"), case 47 (rower contradiction).
