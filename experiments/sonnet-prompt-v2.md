# Round 4: a less rigid prompt for Sonnet 5.5, at low and medium effort (2026-10-04)

Branch `sonnet-prompt-v2`. Raw data and judge artifacts are in
`harness/round4/`. **All 150 workouts, side by side with judge notes, are in
`round4-workouts.md`.**

## Question

Does a principles-first prompt, with the hard rules kept but the rigid
arithmetic dropped, get better workouts out of Claude Sonnet 5.5? And does a
higher reasoning effort help?

## What changed (`src/generator.py`)

**Production is untouched.** `gpt-oss-120b` still gets `SYSTEM_PROMPT` with
the strict checks. A request without the new `prompt` field behaves exactly as
on `main`, and that path was smoke-tested on this branch. The new prompt is
opt-in per request (`"prompt": "v2"`).

### `SYSTEM_PROMPT_CLAUDE` ("v2")
- **Kept hard:**
  - Equipment rules: only listed items, every item used, Bodyweight and Running
    count as items.
  - Physical reality: no rack, no bench.
  - Athlete level: fit amateur; no muscle-ups, handstands or pistols.
  - Style shape, and honest duration.
  - kg, with realistic kit and one load per implement.
  - JSON output.
- **Replaced** the gpt-oss hand-holding with the `crossfit-wod` skill's
  design process:
  - stimulus and one limiter first;
  - couplet or triplet by default;
  - deliberate interference;
  - amateur load bands;
  - a per-movement cycle-time table, transition cost and fatigue multiplier
    for the time math.
- **Movement list is a palette, not a closed world.** Any standard, well-known
  movement doable with the kit is allowed.
- **Asks for a coaching `notes` line** (pacing, what will bite).
- **Dropped:** the "VARIETY — you are weakest here" section, the same-last-word
  test, the chipper and EMOM numeric caps, the For Time "15 reps/min" formula,
  and the worked examples.

### Relaxed checks for v2
`_quality_problems(strict=False)` drops the closed-vocabulary,
seasoning, same-last-word and chipper/EMOM-ceiling checks. It keeps:
duplicates, token reps, one load per implement, the avoid list, and the time
budget and window checks. Equipment checks are unchanged for every prompt.

### Parse fix (all models)
`_extract_json` now takes the **last** complete workout object, so Sonnet's
occasional *"Wait — corrected version below"* replies parse. This fixed
round 3's only Sonnet failure: the v1 control went 50/50.

## Setup

- **The same 50 fixed cases as rounds 1–3**, interleaved per condition,
  concurrency 3, through `pywrangler dev`.
- **Conditions:**
  - `sonnet-low-v1`: production prompt and strict checks (the control).
  - `sonnet-low-v2`
  - `sonnet-medium-v2`
- **Judging:** 5 blind Fable 5.1 judges, 3 candidates per case (A/B/C
  shuffled), scored against a new product-level rubric (`round4/RUBRIC.md`).
  The rubric deliberately does **not** reference either prompt, so the v1
  closed list can't decide the outcome.

## Results

| | low · v1 (control) | low · v2 | **medium · v2** |
|---|---|---|---|
| Succeeded | 50/50 | 50/50 | 50/50 |
| Judge mean rank (1 = best) | 2.68 | 1.76 | **1.56** |
| Judge mean score /10 | 5.04 | 5.96 | **6.36** |
| Judge case wins | 3 | 21 | **26** |
| Workouts scored ≤ 4 | 12 | 8 | **0** |
| Product-relevant check violations¹ | 3 | 6 | **2** |
| Couplets or triplets | 9/50 | 26/50 | 27/50 |
| Mean movements per workout | 4.6 | 4.1 | 4.1 |
| Coaching note present | 8/50 | 50/50 | 50/50 |
| Movements outside the old list | 0 | 0 | 0 |
| Median latency | **2.3 s** | 4.5 s | 4.7 s |
| p90 latency | **7.2 s** | 10.4 s | 21.5 s |
| Max latency | 20.4 s | 15.4 s | 33.8 s |

¹ Time budget or window misses and two-loads breaches only. v2 also "breaks"
v1-only rules it was allowed to break: chipper sets over 50 reps (medium did
this 10 times, low 2), and the same lift on two implements (low v2, 4 times).

### Head to head (judge rank)

| Comparison | Wins |
|---|---|
| medium · v2 vs low · v1 | 43/50 for medium · v2 |
| low · v2 vs low · v1 | 41/50 for low · v2 |
| medium · v2 vs low · v2 | 29/50 for medium · v2 |

### Wins by style

| Style | low · v1 | low · v2 | medium · v2 |
|---|---|---|---|
| AMRAP | 2 | **7** | 5 |
| For Time | 0 | 3 | **8** |
| EMOM | 1 | **7** | 2 |
| Chipper | 0 | 1 | **7** |
| Intervals | 0 | 3 | **4** |

## What the judges saw

- **v1's main failure is underfilled time budgets.** Chippers and For Time
  pieces with roughly 8 minutes of work for a 15–20 minute cap, and ~25 minutes
  for 45. That's the old "≤ 50 reps per movement" chipper ceiling meeting a
  long cap: the model can't fill the time without breaking the ceiling, so it
  underfills. v1 also used token stations to tick off equipment (8-movement
  grab bags).
- **v2 at low effort** got the shape right (more couplets and triplets,
  sensible notes) but still underfilled long pieces in 6 cases: chippers 33,
  34, 35, 37 and 3, plus For Time 40 min (case 23), where it also set a 52 min
  cap. It also
  slipped twice on the avoid list or variants: Hand-Release Push-up when
  Push-up was avoided, and Bar-Facing Burpee in a barbell-only case. The judge
  called that bodyweight work; it's arguably fine, because the app counts it as
  a barbell movement.
- **v2 at medium effort** is the only condition the judges never capped. The
  extra thinking goes into the time math: it fills long chippers with bigger
  sets instead of underfilling. It wins the long-format styles (chipper, For
  Time) clearly, while low · v2 is as good or better on short EMOMs and AMRAPs.
- **The freedom to go off-list wasn't used.** With the movement list made
  optional, Sonnet still used only list movements in all 100 v2 workouts. The
  creativity showed up as structure (fewer, better-chosen movements),
  stimulus-driven notes and time-filling. Closing the list again would cost
  nothing measurable.
- **Notes are often good, but not always accurate.** For example, case 4,
  medium: "aim for about 4 minutes per round" for a round that takes ~2:15.

## Caveats

- **Notes bias.** The rubric rewards helpful notes, v1 rarely writes them, and
  several judges docked v1 explicitly for "no notes". That inflates v1's gap.
  But nearly every v1 score ≤ 4 also cites a time-budget miss, and v2 also beats
  v1 on the product-relevant checks at medium effort (2 vs 3).
- **Self-preference.** Claude judges were judging Claude output, but all three
  conditions here are the same model, so this mostly cancels out.
- **One draw per case** at pinned nonces.
- **Latency cost of medium effort.** The median is unchanged (~4.7 s vs 4.5 s),
  but the tail grows: long chippers take 20–34 s, versus ~15 s max at low.
  Medium also spends more thinking tokens, so costs more per workout. Not
  measured; check the AI Gateway dashboard.
- **gpt-oss-120b was not re-run here.** Its round-3 numbers (71% clean, 12.4 s
  median) are the production reference.

## Recommendation

1. **If Claude ships, ship it with v2.** It beats the v1 prompt on Sonnet in
   41–43 of 50 cases, and v1 stays as gpt-oss's prompt for the fallback path.
2. **Effort:** medium gives the best and most reliable workouts (zero capped
   scores). Low is ~as good on short formats and has a much tighter latency
   tail. A sensible split is **medium for Chipper and For Time, low for
   AMRAP, EMOM and Intervals**. That's a one-line rule, and it puts each style
   on the effort that won it. Untested as a combination.
3. **Small v2 follow-ups:**
   - Re-close the movement list. It wasn't used, and closing it keeps
     `_canonicalize_names` and the equipment index fully effective.
   - Tell the model notes must match the prescription.
   - Add the Hand-Release-Push-up-counts-as-Push-up rule for the avoid list.
4. **Still required before production:** the cost guard
   (`claude-cost-guard-plan.md`) and a real per-workout cost from the AI
   Gateway dashboard.
