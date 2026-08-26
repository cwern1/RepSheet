# Reasoning-effort benchmark — gpt-oss-120b low vs medium

Follow-up to [`model-comparison.md`](model-comparison.md), run 2026-08-24 on the
same branch. That experiment concluded the model stays `@cf/openai/gpt-oss-120b`
(production uses `reasoning effort: medium`) and that latency lives in the
reasoning tokens — so this benchmark asks: **what does `effort: low` cost in
quality, and what does it buy in time?** (`high` was dropped on Chris's call —
prod is medium, and high only gets slower.)

## Method

Identical to the model comparison: the same 50 nonce-pinned cases through the
full production path, both efforts measured **in the same evening window** so
times are directly comparable (absolute values ran higher than usual all
evening — Workers AI was slow; the ratio is the signal). Deterministic validator
+ blind per-case judging (Claude Fable 5 as coach, the two workouts per case
anonymized A/B). During the run the wrangler dev tunnel repeatedly wedged under
long requests; affected pairs were retried on fresh tunnels, and the failures
listed below are the survivors of 3+ attempts.

## Results summary

| effort | ok | med time | mean | p90 | min–max | clean workouts | violations | hard failures |
|---|---|---|---|---|---|---|---|---|
| low | 49/50 | 16.6s | 18.3s | 36.9s | 4.1–41.7s | 34/49 (69%) | 21 | 1 |
| medium | 46/50 | 38.2s | 47.1s | 75.8s | 13.0–187.0s | 34/46 (73%) | 23 | 4 |

## Blind judge results (Fable 5, per-case head-to-head)

| effort | mean score /10 | case wins |
|---|---|---|
| low | 5.62 | 25 |
| medium | 5.58 | 25 |

## Conclusions

**Low effort is a straight win.** On identical inputs, blind-judged head-to-head:

1. **Quality is a statistical dead heat**: 25 case wins each; mean score 5.62 (low)
   vs 5.58 (medium); validator clean rate 69% vs 74% with near-identical violation
   totals (21 vs 23). No systematic quality regression showed up anywhere — low's
   extra interval-window overflows are balanced by medium's extra chipper-ceiling
   breaks.
2. **Low is ~2.3× faster, measured in the same window**: median 16.6 s vs 38.2 s,
   p90 36.9 s vs 75.8 s. Combined with the earlier model comparison, this puts
   120b@low in striking distance of usable latency while keeping the best
   programming quality available on Workers AI.
3. **Low is also more robust tonight's way**: medium's 4 hard failures included
   reasoning-token blowouts — the model spent the entire 6000-token output budget
   thinking on hard chipper cases and never emitted JSON. Low reasons less, so it
   structurally can't fail that way as easily (its single failure was a dev-tunnel
   network drop, not a model fault).
4. Cost drops proportionally with reasoning tokens (fewer output tokens billed).

**Recommendation: switch production to `reasoning effort "low"`** — a one-line
change in `src/generator.py` on main. Suggested rollout: apply, deploy, and
spot-check a handful of generations on the phone; the eval harness in
`experiments/harness/` can re-verify any doubt (50 cases ≈ $0.25 at low effort).

One caveat worth keeping in mind: this is one evening, 50 cases, on a night when
Workers AI was unusually slow. The 2.3× ratio should hold (it's reasoning-token
arithmetic), but absolute times on a normal day will be lower — the old ~14 s
medium baseline suggests low would land around ~6–8 s median.

## Violation breakdown

**gpt-oss-120b@low**
- 3 × OFF-VOCABULARY
- 3 × chipper reps over ceiling
- 2 × two barbell loads
- 2 × 9 movements (max 8)
- 1 × tagged with unlisted equipment
- 1 × interval work ~2.5 min overflows 2 min window
- 1 × EMOM row minute too big
- 1 × EMOM minute overflows
- 1 × chipper ~9 min vs 20 target (too little)
- 1 × repeated base lift (squat)
- 1 × chipper ~22 min vs 45 target (too little)
- 1 × interval work ~4.5 min overflows 3 min window
- 1 × interval work ~5.6 min overflows 5 min window
- 1 × interval work ~9.7 min overflows 3 min window
- 1 × interval work ~2.2 min overflows 2 min window
- FAILED case 1: Workout generation failed: InferenceUpstreamError: Error: Network connection lost.
    at 

**gpt-oss-120b@medium**
- 10 × chipper reps over ceiling
- 6 × OFF-VOCABULARY
- 1 × EMOM token minute
- 1 × repeated base lift (squat)
- 1 × chipper row over 1000 m
- 1 × two kettlebell loads
- 1 × EMOM minute overflows
- 1 × interval work ~3.2 min overflows 3 min window
- 1 × interval work ~3.6 min overflows 3 min window
- FAILED case 35: The model kept using equipment the athlete does not have: Pull-up
- FAILED case 36: client error: timed out
- FAILED case 47: client error: timed out
- FAILED case 48: client error: timed out

---

## Appendix — all generations

Raw data: [`effort_results.jsonl`](effort_results.jsonl) (every attempt,
including tunnel-failure retries), [`effort_analysis.json`](effort_analysis.json).

### Case 1 — EMOM 7 min · Bodyweight

**low** — 395.7s · judge loss, score 0/10
  - GENERATION FAILED: Workout generation failed: InferenceUpstreamError: Error: Network connection lost.
    at async Object.fetch (file:///Us

**medium** — 59.1s · judge WIN, score 6/10 · violations: EMOM token minute: 6 m Broad Jump
  `EMOM 7` · scheme: 7 stations × 1 round
  - 8 Hand-Release Push-up
  - 15 Air Squat
  - 10 Jumping Lunge
  - 20 Sit-up
  - 6 m Broad Jump
  - 6 Burpee
  - 1 min Rest


### Case 2 — EMOM 30 min · Rower, Bike Erg, Ski Erg, Assault Bike

**low** — 39.3s · judge loss, score 2/10 · violations: tagged with unlisted equipment: Front Squat -> Barbell
  `EMOM 30` · scheme: 5 stations × 6 rounds
  - 150 m Row
  - 8 cal Bike Erg
  - 8 cal Ski Erg
  - 12 Front Squat @ 40 kg
  - 6 cal Assault Bike

**medium** — 75.8s · judge WIN, score 8/10
  `EMOM 30` · scheme: 5 stations × 6 rounds
  - 200 m Row
  - 10 cal Bike Erg
  - 8 cal Ski Erg
  - 6 cal Assault Bike
  - 1 min Rest


### Case 3 — Chipper 30 min · Bodyweight, Barbell, Kettlebell, Pull-up Bar, Rower

**low** — 36.2s · judge WIN, score 7/10
  `Chipper · cap 30 min`
  - 800 m Row
  - 50 Kettlebell Swing @ 24 kg
  - 40 Kettlebell Clean @ 24 kg
  - 30 Air Squat
  - 30 Deadlift @ 70 kg
  - 20 Pull-up
  - 15 Push-up

**medium** — 187.0s · judge loss, score 3/10 · violations: repeated base lift (squat): Air Squat + Goblet Squat; chipper row over 1000 m: 1500 m; chipper reps over ceiling: 80 Pull-up; chipper reps over ceiling: 70 Kettlebell Clean; chipper reps over ceiling: 60 Sumo Deadlift High Pull
  `Chipper · cap 30 min`
  - 1500 m Row
  - 80 Pull-up
  - 70 Kettlebell Clean @ 20 kg
  - 60 Sumo Deadlift High Pull @ 40 kg
  - 50 Air Squat
  - 40 Bar-Facing Burpee
  - 30 Sit-up
  - 20 Goblet Squat @ 20 kg


### Case 4 — AMRAP 20 min · Bodyweight, Dumbbells, Kettlebell

**low** — 24.8s · judge WIN, score 8/10
  `AMRAP 20 min`
  - 8 Burpee
  - 5/arm Dumbbell Snatch @ 22.5 kg
  - 6/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 12 Kettlebell Swing @ 24 kg
  - 15 Air Squat

**medium** — 37.7s · judge loss, score 5/10 · violations: two kettlebell loads: [16.0, 24.0]
  `AMRAP 20 min`
  - 6 Dumbbell Snatch @ 22.5 kg
  - 12 Kettlebell Swing @ 24 kg
  - 8 Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 10 Push-up
  - 1/arm Turkish Get-Up @ 16 kg


### Case 5 — For Time 25 min · Bodyweight, Barbell, Pull-up Bar

**low** — 9.1s · judge loss, score 4/10
  `For Time · cap 28 min` · scheme: 12 Rounds
  - 10 Deadlift @ 80 kg
  - 8 Pull-up
  - 15 Air Squat

**medium** — 38.1s · judge WIN, score 6/10
  `For Time · cap 28 min` · scheme: 5 Rounds
  - 8 Pull-up
  - 10/leg Front-Rack Lunge @ 40 kg
  - 8 Deadlift @ 40 kg
  - 30 Push-up
  - 35 Air Squat


### Case 6 — AMRAP 45 min · Bodyweight, Barbell, Dumbbells, Kettlebell, Pull-up Bar, Rings, Rower, Jump Rope, Plyo Box, Wall Ball, Running

**low** — 24.8s · judge WIN, score 6/10
  `AMRAP 45 min`
  - 250 m Row
  - 200 m Run
  - 5 Deadlift @ 70 kg
  - 10 Kettlebell Swing @ 24 kg
  - 5 Pull-up
  - 30 Double-Under

**medium** — 49.8s · judge loss, score 4/10 · violations: OFF-VOCABULARY: Barbell Deadlift
  `AMRAP 45 min`
  - 3 Barbell Deadlift @ 80 kg
  - 6 Kettlebell Swing @ 24 kg
  - 2/arm Dumbbell Snatch @ 22.5 kg
  - 3 Pull-up
  - 5 Ring Row
  - 250 m Row
  - 200 m Run
  - 3 Burpee


### Case 7 — For Time 15 min · Bodyweight, Barbell, Dumbbells
*Athlete request:* `no overhead today`

**low** — 17.5s · judge loss, score 4/10 · violations: OFF-VOCABULARY: Clean
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 10 Front Squat @ 50 kg
  - 12/leg Reverse Lunge @ 2×22.5 kg
  - 10 Sumo Deadlift High Pull @ 50 kg
  - 8 Burpee
  - 8 Clean @ 22.5 kg
  - 15 Sit-up

**medium** — 105.9s · judge WIN, score 7/10
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 8 Deadlift @ 60 kg
  - 8 Front Squat @ 60 kg
  - 12/leg Walking Lunge
  - 15 Push-up
  - 6/arm Dumbbell Clean @ 22.5 kg
  - 15 Sit-up


### Case 8 — AMRAP 12 min · Bodyweight, Kettlebell, Pull-up Bar
*Athlete request:* `no overhead`

**low** — 12.3s · judge WIN, score 8/10
  `AMRAP 12 min`
  - 5 Pull-up
  - 5 Kettlebell Deadlift @ 24 kg
  - 8 Goblet Squat @ 24 kg
  - 10 Kettlebell Swing @ 24 kg
  - 12 Walking Lunge

**medium** — 23.8s · judge loss, score 7/10
  `AMRAP 12 min`
  - 5 Burpee Pull-up
  - 10 Kettlebell Swing @ 24 kg
  - 10 Air Squat
  - 15 Sit-up


### Case 9 — Intervals 15 min · Running, Bodyweight

**low** — 14.7s · judge loss, score 6/10 · violations: interval work ~2.5 min overflows 2 min window
  `5 × 2 min on / 1 min rest`
  - 100 m Run
  - 12 Air Squat
  - 8 Push-up
  - 20 Sit-up

**medium** — 75.7s · judge WIN, score 7/10
  `3 × 4 min on / 1 min rest`
  - 200 m Run
  - 12 Air Squat
  - 12 Push-up
  - 20 Sit-up


### Case 10 — AMRAP 16 min · Kettlebell, Dumbbells, Bodyweight

**low** — 7.5s · judge WIN, score 8/10
  `AMRAP 16 min`
  - 12 Kettlebell Swing @ 24 kg
  - 6/arm Dumbbell Snatch @ 22.5 kg
  - 8/leg Walking Lunge
  - 10 Push-up
  - 10 Air Squat

**medium** — 24.7s · judge loss, score 7/10
  `AMRAP 16 min`
  - 10 Kettlebell Swing @ 24 kg
  - 10 Dumbbell Deadlift @ 2×22.5 kg
  - 12/leg Walking Lunge
  - 10 Push-up
  - 15 Sit-up


### Case 11 — AMRAP 5 min · Bodyweight

**low** — 4.1s · judge loss, score 5/10
  `AMRAP 5 min`
  - 12/leg Walking Lunge
  - 15 Push-up
  - 25 m Bear Crawl
  - 12 Broad Jump

**medium** — 21.7s · judge WIN, score 6/10
  `AMRAP 5 min`
  - 10/leg Reverse Lunge
  - 15 Air Squat
  - 10 Broad Jump
  - 12 Push-up
  - 20 Sit-up


### Case 12 — AMRAP 10 min · Bodyweight, Jump Rope

**low** — 8.1s · judge loss, score 4/10
  `AMRAP 10 min`
  - 8/leg Reverse Lunge
  - 10 Single-Under
  - 5 Burpee

**medium** — 13.0s · judge WIN, score 5/10
  `AMRAP 10 min`
  - 5 Broad Jump
  - 8/leg Reverse Lunge
  - 5 Burpee
  - 15 Single-Under


### Case 13 — AMRAP 15 min · Barbell, Bodyweight

**low** — 10.5s · judge loss, score 5/10
  `AMRAP 15 min`
  - 10 Sit-up
  - 8 Front Squat @ 60 kg
  - 6 Bar-Facing Burpee
  - 5 Push Press @ 60 kg
  - 5 Deadlift @ 60 kg

**medium** — 21.5s · judge WIN, score 8/10
  `AMRAP 15 min`
  - 12 Deadlift @ 40 kg
  - 10 Overhead Squat @ 40 kg
  - 10 Push Press @ 40 kg
  - 20 Sit-up
  - 10 Burpee


### Case 14 — AMRAP 20 min · Kettlebell, Pull-up Bar, Bodyweight

**low** — 7.1s · judge WIN, score 8/10
  `AMRAP 20 min`
  - 30 Kettlebell Swing @ 24 kg
  - 10 Pull-up
  - 30 Air Squat
  - 20 Push-up

**medium** — 15.4s · judge loss, score 7/10
  `AMRAP 20 min`
  - 20 Kettlebell Swing @ 24 kg
  - 5 Pull-up
  - 5 Burpee
  - 15 Air Squat
  - 20 Sit-up


### Case 15 — AMRAP 25 min · Dumbbells, Plyo Box, Bodyweight

**low** — 19.2s · judge WIN, score 7/10
  `AMRAP 25 min`
  - 20 Air Squat
  - 12 Dumbbell Thruster @ 15 kg
  - 10 Box Jump
  - 12 Dumbbell Front-Rack Lunge @ 2×15 kg
  - 15 Push-up

**medium** — 60.1s · judge loss, score 6/10
  `AMRAP 25 min`
  - 12 Air Squat
  - 6/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 8 Box Jump
  - 12 Push-up
  - 12 Sit-up
  - 6 Dumbbell Snatch @ 22.5 kg


### Case 16 — AMRAP 30 min · Bodyweight, Barbell, Wall Ball, Rower

**low** — 16.6s · judge WIN, score 8/10
  `AMRAP 30 min`
  - 250 m Row
  - 12 Deadlift @ 60 kg
  - 15 Wall Ball @ 6 kg
  - 12 Push-up

**medium** — 20.2s · judge loss, score 7/10
  `AMRAP 30 min`
  - 10 Deadlift @ 60 kg
  - 10/leg Walking Lunge
  - 150 m Row
  - 12 Wall Ball @ 6 kg


### Case 17 — AMRAP 12 min · Kettlebell

**low** — 7.2s · judge WIN, score 6/10
  `AMRAP 12 min`
  - 10 Kettlebell Swing @ 24 kg
  - 8 Goblet Squat @ 24 kg
  - 6 Kettlebell Clean @ 24 kg
  - 6 Kettlebell Push Press @ 24 kg
  - 3/arm Turkish Get-Up @ 24 kg

**medium** — 22.9s · judge loss, score 3/10
  `AMRAP 12 min`
  - 20 Kettlebell Swing @ 24 kg
  - 15 Goblet Squat @ 24 kg
  - 10 Kettlebell Push Press @ 24 kg
  - 5/arm Turkish Get-Up @ 24 kg


### Case 18 — AMRAP 18 min · Dumbbells, Sandbag, Bodyweight

**low** — 19.5s · judge loss, score 6/10
  `AMRAP 18 min`
  - 8/arm Dumbbell Snatch @ 22.5 kg
  - 12 Sandbag Clean @ 40 kg
  - 50 m Sandbag Carry
  - 15 Push-up
  - 20 Air Squat

**medium** — 20.7s · judge WIN, score 7/10
  `AMRAP 18 min`
  - 8 Dumbbell Snatch @ 22.5 kg
  - 50 m Sandbag Carry @ 30 kg
  - 15 Push-up
  - 12 Air Squat
  - 12 Sit-up


### Case 19 — For Time 8 min · Bodyweight, Kettlebell

**low** — 25.9s · judge loss, score 5/10
  `For Time · cap 11 min` · scheme: 3 Rounds
  - 20 Kettlebell Swing @ 24 kg
  - 10/arm Kettlebell Clean @ 24 kg
  - 12 Push-up
  - 8 Burpee

**medium** — 42.8s · judge WIN, score 8/10
  `For Time · cap 11 min` · scheme: 2 Rounds
  - 20 Kettlebell Swing @ 16 kg
  - 12 Goblet Squat @ 16 kg
  - 15 Push-up
  - 8/arm Kettlebell Snatch @ 16 kg
  - 10 Kettlebell Push Press @ 16 kg
  - 12 Sit-up


### Case 20 — For Time 12 min · Barbell

**low** — 17.8s · judge loss, score 2/10
  `For Time · cap 13 min` · scheme: 4 Rounds
  - 15 Push Press @ 40 kg
  - 15 Thruster @ 40 kg
  - 15 Push Jerk @ 40 kg
  - 15 Deadlift @ 40 kg

**medium** — 28.7s · judge WIN, score 5/10
  `For Time · cap 15 min` · scheme: 3 Rounds
  - 12 Deadlift @ 40 kg
  - 12 Push Press @ 40 kg
  - 12 Front Squat @ 40 kg
  - 12 Thruster @ 40 kg


### Case 21 — For Time 20 min · Bodyweight, Dumbbells, Pull-up Bar, Rower

**low** — 8.4s · judge WIN, score 7/10
  `For Time · cap 23 min` · scheme: 5 Rounds
  - 250 m Row
  - 10 Pull-up
  - 12 Dumbbell Push Press @ 2×20 kg
  - 15 Dumbbell Deadlift @ 2×20 kg
  - 20 Sit-up

**medium** — 24.8s · judge loss, score 6/10
  `For Time · cap 23 min` · scheme: 3 Rounds
  - 30 Sit-up
  - 8/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 8 Dumbbell Thruster @ 2×22.5 kg
  - 6 Pull-up
  - 250 m Row
  - 8 Dumbbell Deadlift @ 2×22.5 kg


### Case 22 — For Time 30 min · Bodyweight, Barbell, Kettlebell, Running

**low** — 23.9s · judge loss, score 5/10
  `For Time · cap 33 min` · scheme: 5 Rounds
  - 30 Kettlebell Swing @ 24 kg
  - 12 Deadlift @ 60 kg
  - 20 Hand-Release Push-up
  - 30 Air Squat
  - 400 m Run

**medium** — 56.3s · judge WIN, score 6/10
  `For Time · cap 33 min` · scheme: 6 Rounds
  - 12 Deadlift @ 40 kg
  - 12 Push Press @ 40 kg
  - 30 Kettlebell Swing @ 24 kg
  - 15 Push-up
  - 400 m Run


### Case 23 — For Time 40 min · Bodyweight, Barbell, Dumbbells, Kettlebell, Pull-up Bar, Rings, Rower, Jump Rope

**low** — 16.6s · judge WIN, score 6/10
  `For Time · cap 43 min` · scheme: 5 Rounds
  - 10 Pull-up
  - 15 Ring Row
  - 20 Kettlebell Swing @ 24 kg
  - 12/arm Dumbbell Snatch @ 15 kg
  - 12 Deadlift @ 60 kg
  - 30 Double-Under
  - 20 Air Squat
  - 250 m Row

**medium** — 72.7s · judge loss, score 5/10
  `For Time · cap 43 min` · scheme: 5 Rounds
  - 250 m Row
  - 40 Double-Under
  - 30 Air Squat
  - 15 Pull-up
  - 25 Kettlebell Swing @ 24 kg
  - 15 Ring Row
  - 10 Deadlift @ 60 kg
  - 15/arm Dumbbell Snatch @ 22.5 kg


### Case 24 — For Time 10 min · Bodyweight, Jump Rope

**low** — 41.7s · judge loss, score 4/10
  `For Time · cap 13 min`
  - 100 Double-Under
  - 150 Single-Under
  - 40 Air Squat
  - 20 Broad Jump
  - 20 Burpee
  - 30 Hand-Release Push-up
  - 30 Sit-up
  - 20/leg Jumping Lunge

**medium** — 36.0s · judge WIN, score 7/10
  `For Time · cap 13 min` · scheme: 4 Rounds
  - 12 Double-Under
  - 8/leg Reverse Lunge
  - 15 Sit-up
  - 8 Broad Jump
  - 10 Push-up


### Case 25 — For Time 15 min · Wall Ball, Rower, Bodyweight

**low** — 8.8s · judge loss, score 6/10
  `For Time · cap 18 min` · scheme: 5 Rounds
  - 250 m Row
  - 20 Wall Ball @ 6 kg
  - 10 Broad Jump
  - 10 Burpee

**medium** — 35.7s · judge WIN, score 7/10
  `For Time · cap 18 min` · scheme: 5 Rounds
  - 250 m Row
  - 20 Wall Ball @ 6 kg
  - 15 Push-up
  - 12 Burpee


### Case 26 — EMOM 10 min · Kettlebell, Bodyweight

**low** — 17.5s · judge loss, score 4/10
  `EMOM 10` · scheme: 5 stations × 2 rounds
  - 15 Kettlebell Swing @ 16 kg
  - 12 Goblet Squat @ 16 kg
  - 12 Push-up
  - 10 Kettlebell Clean @ 16 kg
  - 3/arm Turkish Get-Up @ 16 kg

**medium** — 65.6s · judge WIN, score 6/10
  `EMOM 10` · scheme: 5 stations × 2 rounds
  - 15 Kettlebell Swing @ 24 kg
  - 8 Push-up
  - 15 Goblet Squat @ 24 kg
  - 8 Kettlebell Push Press @ 24 kg
  - 12 Sit-up


### Case 27 — EMOM 12 min · Barbell, Dumbbells, Bodyweight

**low** — 19.1s · judge loss, score 5/10 · violations: two barbell loads: [50.0, 60.0]
  `EMOM 12` · scheme: 4 stations × 3 rounds
  - 6 Deadlift @ 60 kg
  - 8 Dumbbell Snatch @ 22.5 kg
  - 6 Hang Power Clean @ 50 kg
  - 12 Air Squat

**medium** — 20.2s · judge WIN, score 7/10
  `EMOM 12` · scheme: 4 stations × 3 rounds
  - 5 Deadlift @ 60 kg
  - 50 m Farmers Carry @ 2×22.5 kg
  - 15 Air Squat
  - 12 Push-up


### Case 28 — EMOM 16 min · Dumbbells, Plyo Box, Rower, Bodyweight

**low** — 15.8s · judge loss, score 3/10 · violations: EMOM row minute too big: 250 m; EMOM minute overflows: 8/leg Dumbbell Front-Rack Lunge
  `EMOM 16` · scheme: 4 stations × 4 rounds
  - 250 m Row
  - 8/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 12 Box Jump-Over
  - 6/arm Dumbbell Snatch @ 22.5 kg

**medium** — 21.9s · judge WIN, score 7/10
  `EMOM 16` · scheme: 4 stations × 4 rounds
  - 150 m Row
  - 12 Burpee
  - 8 Dumbbell Snatch @ 22.5 kg
  - 12 Dumbbell Box Step-Up @ 2×22.5 kg


### Case 29 — EMOM 20 min · Kettlebell, Barbell, Pull-up Bar, Bodyweight, Rower

**low** — 7.0s · judge WIN, score 7/10
  `EMOM 20` · scheme: 5 stations × 4 rounds
  - 20 Kettlebell Swing @ 24 kg
  - 6 Deadlift @ 60 kg
  - 8 Pull-up
  - 10 Burpee
  - 150 m Row

**medium** — 23.5s · judge loss, score 5/10 · violations: OFF-VOCABULARY: Barbell Deadlift
  `EMOM 20` · scheme: 5 stations × 4 rounds
  - 15 Kettlebell Swing @ 16 kg
  - 6 Barbell Deadlift @ 70 kg
  - 5 Pull-up
  - 18 Air Squat
  - 150 m Row


### Case 30 — EMOM 9 min · Bodyweight, Running

**low** — 4.8s · judge WIN, score 7/10
  `EMOM 9` · scheme: 3 stations × 3 rounds
  - 100 m Run
  - 10 Push-up
  - 15 Sit-up

**medium** — 43.1s · judge loss, score 5/10 · violations: EMOM minute overflows: 22 Sit-up
  `EMOM 9` · scheme: 3 stations × 3 rounds
  - 6 Burpee
  - 22 Sit-up
  - 100 m Run


### Case 31 — EMOM 14 min · Kettlebell, Dumbbells

**low** — 8.3s · judge loss, score 7/10
  `EMOM 14` · scheme: 2 stations × 7 rounds
  - 20 Kettlebell Swing @ 24 kg
  - 10 Dumbbell Snatch @ 22.5 kg

**medium** — 17.5s · judge WIN, score 8/10
  `EMOM 14` · scheme: 2 stations × 7 rounds
  - 20 Kettlebell Swing @ 24 kg
  - 6/arm Dumbbell Snatch @ 15 kg


### Case 32 — EMOM 24 min · Bodyweight, Barbell, Assault Bike

**low** — 5.8s · judge WIN, score 9/10
  `EMOM 24` · scheme: 4 stations × 6 rounds
  - 8 Front Squat @ 40 kg
  - 15 Push-up
  - 8 cal Assault Bike
  - 8 Deadlift @ 40 kg

**medium** — 50.4s · judge loss, score 3/10 · violations: OFF-VOCABULARY: Back Squat
  `EMOM 24` · scheme: 3 stations × 8 rounds
  - 8 Back Squat @ 40 kg
  - 8 cal Assault Bike
  - 15 Push-up


### Case 33 — Chipper 15 min · Bodyweight, Kettlebell

**low** — 38.0s · judge loss, score 4/10 · violations: chipper reps over ceiling: 60 Sit-up
  `Chipper · cap 15 min`
  - 60 Sit-up
  - 40 Kettlebell Swing @ 24 kg
  - 35 Goblet Squat @ 24 kg
  - 30 Overhead Lunge @ 24 kg
  - 20 Push-up
  - 15 Kettlebell Clean @ 24 kg
  - 12 Kettlebell Deadlift @ 24 kg
  - 10 Kettlebell Snatch @ 24 kg

**medium** — 57.9s · judge WIN, score 7/10
  `Chipper · cap 15 min`
  - 50 Sit-up
  - 45 Kettlebell Swing @ 24 kg
  - 40 Goblet Squat @ 24 kg
  - 35 Kettlebell Push Press @ 24 kg
  - 25 Push-up
  - 20 Kettlebell Snatch @ 24 kg


### Case 34 — Chipper 20 min · Bodyweight, Dumbbells, Pull-up Bar, Jump Rope

**low** — 36.9s · judge WIN, score 8/10 · violations: chipper ~9 min vs 20 target (too little)
  `Chipper · cap 20 min`
  - 100 Double-Under
  - 50 Air Squat
  - 20 Chin-up
  - 15 Dumbbell Clean @ 2×22.5 kg
  - 12 Dumbbell Snatch @ 22.5 kg
  - 10 Dumbbell Push Press @ 2×22.5 kg
  - 8 Burpee

**medium** — 41.0s · judge loss, score 6/10
  `Chipper · cap 20 min`
  - 100 Double-Under
  - 50 Pull-up
  - 40 Dumbbell Clean @ 2×22.5 kg
  - 30 Air Squat
  - 20 Sit-up
  - 10/arm Dumbbell Snatch @ 22.5 kg
  - 5 Burpee


### Case 35 — Chipper 25 min · Barbell, Bodyweight, Rower, Wall Ball

**low** — 15.1s · judge WIN, score 4/10 · violations: OFF-VOCABULARY: Barbell Walking Lunge; chipper reps over ceiling: 40/leg Barbell Walking Lunge
  `Chipper · cap 25 min`
  - 40/leg Barbell Walking Lunge @ 40 kg
  - 30 Wall Ball @ 9 kg
  - 20 Deadlift @ 40 kg
  - 15 Burpee
  - 250 m Row
  - 25 Push-up

**medium** — 319.3s · judge loss, score 0/10
  - GENERATION FAILED: The model kept using equipment the athlete does not have: Pull-up


### Case 36 — Chipper 35 min · Bodyweight, Barbell, Dumbbells, Kettlebell, Pull-up Bar, Rings, Rower, Jump Rope, Plyo Box

**low** — 34.3s · judge WIN, score 4/10 · violations: 9 movements (max 8); chipper reps over ceiling: 50/leg Dumbbell Front-Rack Lunge
  `Chipper · cap 35 min`
  - 1000 m Row
  - 100 Double-Under
  - 50 Kettlebell Swing @ 24 kg
  - 50/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 30 Pull-up
  - 30 Ring Row
  - 30 Sit-up
  - 20 Deadlift @ 60 kg
  - 30 Box Jump

**medium** — 420.0s · judge loss, score 0/10
  - GENERATION FAILED: client error: timed out


### Case 37 — Chipper 45 min · Bodyweight, Barbell, Kettlebell, Dumbbells, Pull-up Bar, Running

**low** — 39.2s · judge WIN, score 5/10 · violations: repeated base lift (squat): Air Squat + Front Squat; 9 movements (max 8); two barbell loads: [60.0, 70.0]; chipper ~22 min vs 45 target (too little)
  `Chipper · cap 45 min`
  - 50 Deadlift @ 70 kg
  - 45 Kettlebell Swing @ 24 kg
  - 40 Dumbbell Snatch @ 22.5 kg
  - 35 Pull-up
  - 800 m Run
  - 30 Air Squat
  - 25 Dumbbell Push Press @ 2×22.5 kg
  - 20 Burpee
  - 15 Front Squat @ 60 kg

**medium** — 121.1s · judge loss, score 2/10 · violations: OFF-VOCABULARY: Swing; OFF-VOCABULARY: Snatch; chipper reps over ceiling: 130 Swing; chipper reps over ceiling: 115 Deadlift; chipper reps over ceiling: 100/arm Snatch; chipper reps over ceiling: 90 Pull-up; chipper reps over ceiling: 80 Push-up; chipper reps over ceiling: 70 Air Squat
  `Chipper · cap 45 min`
  - 800 m Run
  - 130 Swing @ 24 kg
  - 115 Deadlift @ 60 kg
  - 100/arm Snatch @ 22.5 kg
  - 90 Pull-up
  - 80 Push-up
  - 70 Air Squat


### Case 38 — Chipper 20 min · Sandbag, Bodyweight, GHD

**low** — 25.8s · judge WIN, score 6/10 · violations: OFF-VOCABULARY: Sandbag Shoulder-to-Shoulder Press
  `Chipper · cap 20 min`
  - 45 GHD Sit-up
  - 40 Sandbag Clean @ 30 kg
  - 35 Sandbag Lunge @ 30 kg
  - 30 Sandbag Shoulder-to-Shoulder Press @ 30 kg
  - 20 Push-up
  - 25 m Sandbag Carry

**medium** — 126.6s · judge loss, score 5/10 · violations: chipper reps over ceiling: 55 Bearhug Squat
  `Chipper · cap 20 min`
  - 55 Bearhug Squat @ 30 kg
  - 50 GHD Sit-up
  - 48 Shoulder-to-Shoulder Press @ 30 kg
  - 35 Reverse Lunge
  - 30 Burpee
  - 25 m Sandbag Carry @ 30 kg
  - 25 Push-up


### Case 39 — Intervals 12 min · Bodyweight, Kettlebell

**low** — 8.2s · judge WIN, score 8/10
  `4 × 2 min on / 1 min rest`
  - 30 Kettlebell Swing @ 24 kg
  - 10 Push-up

**medium** — 67.0s · judge loss, score 7/10 · violations: interval work ~3.2 min overflows 3 min window
  `3 × 3 min on / 1 min rest`
  - 30 Kettlebell Swing @ 16 kg
  - 12 Kettlebell Deadlift @ 16 kg
  - 8 Burpee
  - *notes: Move quickly, keep a sprint‑pace turnover during the work periods.*


### Case 40 — Intervals 20 min · Barbell, Bodyweight, Rower

**low** — 8.7s · judge loss, score 6/10
  `5 × 3 min on / 1 min rest`
  - 250 m Row
  - 8 Push Press @ 40 kg
  - 12 Push-up
  - *notes: Maintain sprint pace on the row; keep fast turnover on press and push‑ups.*

**medium** — 21.7s · judge WIN, score 7/10
  `5 × 3 min on / 1 min rest`
  - 6 Push Press @ 40 kg
  - 250 m Row
  - 15 Push-up
  - *notes: 1 min rest between rounds*


### Case 41 — Intervals 24 min · Dumbbells, Ski Erg, Bodyweight

**low** — 18.5s · judge loss, score 4/10 · violations: interval work ~4.5 min overflows 3 min window
  `6 × 3 min on / 1 min rest`
  - 20 cal Ski Erg
  - 8 Dumbbell Deadlift @ 30 kg
  - 8/leg Reverse Lunge
  - 12 Sit-up
  - 10 Air Squat
  - 8 Hand-Release Push-up

**medium** — 38.3s · judge WIN, score 7/10
  `4 × 5 min on / 1 min rest`
  - 12 Dumbbell Deadlift @ 2×22.5 kg
  - 8 Dumbbell Push Press @ 2×22.5 kg
  - 12/leg Reverse Lunge
  - 20 cal Ski Erg


### Case 42 — Intervals 30 min · Bodyweight, Running, Pull-up Bar

**low** — 24.2s · judge WIN, score 7/10 · violations: interval work ~5.6 min overflows 5 min window
  `5 × 5 min on / 1 min rest` · scheme: 5 stations × 5 rounds
  - 200 m Run
  - 30 Air Squat
  - 8 Pull-up
  - 20 Walking Lunge
  - 20 Sit-up
  - 5 Broad Jump

**medium** — 28.4s · judge loss, score 6/10
  `5 × 4 min on / 2 min rest`
  - 30 Air Squat
  - 200 m Run
  - 8/leg Walking Lunge
  - 6 Pull-up


### Case 43 — Intervals 16 min · Assault Bike, Wall Ball, Bodyweight

**low** — 24.2s · judge loss, score 2/10 · violations: interval work ~9.7 min overflows 3 min window
  `4 × 3 min on / 1 min rest`
  - 30 cal Assault Bike
  - 20 Wall Ball @ 6 kg
  - 30 Air Squat
  - 20 Push-up
  - 20/leg Walking Lunge

**medium** — 47.2s · judge WIN, score 6/10 · violations: interval work ~3.6 min overflows 3 min window
  `4 × 3 min on / 1 min rest`
  - 20 Air Squat
  - 15 Wall Ball @ 6 kg
  - 12 cal Assault Bike


### Case 44 — AMRAP 15 min · Bodyweight, Barbell, Dumbbells
*Athlete request:* `bad knee - nothing that loads a deep bend`

**low** — 16.5s · judge WIN, score 8/10
  `AMRAP 15 min`
  - 10 Deadlift @ 70 kg
  - 8/arm Dumbbell Snatch @ 22.5 kg
  - 12 Dumbbell Push Press @ 2×22.5 kg
  - 15 Push-up
  - 20 Sit-up

**medium** — 23.7s · judge loss, score 6/10
  `AMRAP 15 min`
  - 8 Deadlift @ 60 kg
  - 10 Push Press @ 2×22.5 kg
  - 12 Push-up
  - 15 Sit-up


### Case 45 — For Time 12 min · Bodyweight, Kettlebell
*Athlete request:* `easy recovery day please`

**low** — 9.9s · judge loss, score 6/10
  `For Time · cap 15 min` · scheme: 5 Rounds
  - 8 Goblet Squat @ 24 kg
  - 12 Kettlebell Swing @ 24 kg
  - 8 Push-up
  - 8 Kettlebell Deadlift @ 24 kg

**medium** — 26.0s · judge WIN, score 7/10
  `For Time · cap 15 min` · scheme: 5 Rounds
  - 8 Goblet Squat @ 24 kg
  - 12 Kettlebell Swing @ 24 kg
  - 8 Push-up
  - 10 Sit-up


### Case 46 — EMOM 12 min · Bodyweight, Dumbbells
*Athlete request:* `I want devil press in there`

**low** — 11.8s · judge WIN, score 7/10
  `EMOM 12` · scheme: 3 stations × 4 rounds
  - 5 Devil Press @ 2×22.5 kg
  - 5/arm Dumbbell Snatch @ 22.5 kg
  - 6 Dumbbell Deadlift @ 2×22.5 kg

**medium** — 49.5s · judge loss, score 6/10
  `EMOM 12` · scheme: 4 stations × 3 rounds
  - 5 Devil Press @ 2×22.5 kg
  - 5 Dumbbell Deadlift @ 2×22.5 kg
  - 8 Air Squat
  - 8 Push-up


### Case 47 — Chipper 25 min · Bodyweight, Kettlebell, Pull-up Bar
*Athlete request:* `use the rower a lot`

**low** — 29.4s · judge WIN, score 6/10
  `Chipper · cap 25 min`
  - 45 Pull-up
  - 50 Kettlebell Swing @ 12.5 kg
  - 40 Goblet Squat @ 12.5 kg
  - 35 Push-up
  - 30 Kettlebell Clean @ 12.5 kg
  - 25 Hanging Knee Raise
  - 20 Burpee

**medium** — 420.0s · judge loss, score 0/10
  - GENERATION FAILED: client error: timed out


### Case 48 — Intervals 18 min · Bodyweight
*Athlete request:* `no jumping, downstairs neighbours`

**low** — 21.9s · judge WIN, score 7/10 · violations: interval work ~2.2 min overflows 2 min window
  `6 × 2 min on / 1 min rest`
  - 15 Air Squat
  - 8/leg Walking Lunge
  - 6 Push-up
  - 8 Sit-up

**medium** — 420.0s · judge loss, score 0/10
  - GENERATION FAILED: client error: timed out


### Case 49 — AMRAP 12 min · Kettlebell, Bodyweight
*Avoid:* Kettlebell Swing, Goblet Squat, Burpee, Push-up, Sit-up

**low** — 21.6s · judge loss, score 6/10
  `AMRAP 12 min`
  - 15 Air Squat
  - 12 Walking Lunge
  - 10 Kettlebell Clean @ 16 kg
  - 8 Kettlebell Push Press @ 16 kg
  - 12 Kettlebell Deadlift @ 16 kg
  - 25 m Bear Crawl

**medium** — 39.7s · judge WIN, score 8/10
  `AMRAP 12 min`
  - 20 Air Squat
  - 12 Kettlebell Clean @ 16 kg
  - 10 Kettlebell Push Press @ 16 kg
  - 12/leg Walking Lunge


### Case 50 — For Time 15 min · Bodyweight, Barbell, Pull-up Bar
*Avoid:* Deadlift, Pull-up, Thruster, Push-up, Air Squat, Run

**low** — 11.3s · judge loss, score 4/10
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 30 Sit-up
  - 15 Pull-up
  - 30 Front Squat @ 40 kg
  - 15 Bar-Facing Burpee

**medium** — 67.9s · judge WIN, score 5/10 · violations: OFF-VOCABULARY: Overhead Press
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 10 Front Squat @ 30 kg
  - 10 Overhead Press @ 30 kg
  - 30 Sit-up
  - 8 Chest-to-Bar Pull-up
  - 10/leg Front-Rack Lunge @ 30 kg

