# Model comparison — Workers AI alternatives to gpt-oss-120b

Experiment run 2026-08-24/25 on branch `model-comparison`. Question: is there a
Workers AI model that generates **equal-or-better workouts faster** than the
production model `@cf/openai/gpt-oss-120b`?

## Method

- **Same 50 fixed cases for every model** — all 5 styles × durations 5–60 min ×
  equipment lists from 1 to 11 items, plus custom-text cases (restrictions,
  contradictions, requested movements) and avoid-list cases. Nonces are pinned per
  case, so every model sees the identical prompt including the same programming angle.
  Cases 1–10 are the known-hard cases from the prompt eval matrix.
- Generation goes through the **full production path** (FastAPI → prompt → parse →
  Pydantic → equipment/quality validators → up to 1 corrective retry), via
  `pywrangler dev` with the real Workers AI binding. Only the model id (and the
  transport shape it requires) differs.
- **Time** = client wall-clock per request, concurrency 3, so it includes any
  server-side shape/corrective retries — the honest number a user would feel.
- **Deterministic violations** = host-side re-run of the validator checks plus a
  strict movement-vocabulary check (`analyze.py`).
- **Blind judging**: per case, the four models' workouts were shuffled into
  candidates A–D and ranked by Claude (Fable 5) as a CrossFit coach, without
  knowing which model wrote which. Rank 1 = best of the four.
- Caveats: single day, 50 samples/model; Workers AI was generally slow during the
  first window (the 120b baseline normally runs ~14 s but measured far slower here,
  and the free-tier quota exhaustion split the runs across two windows).
  Relative comparisons are the point, absolute times less so.

## Models

| model | role | transport | price (in/out) |
|---|---|---|---|
| `@cf/openai/gpt-oss-120b` | baseline (current prod) | Responses API, reasoning medium | $0.35 / $0.75 per M tok |
| `@cf/openai/gpt-oss-20b` | candidate | Responses API, reasoning medium | $0.20 / $0.30 per M tok |
| `@cf/meta/llama-3.3-70b-instruct-fp8-fast` | candidate | chat completions, no reasoning | $0.29 / $2.25 per M tok |
| `@cf/meta/llama-4-scout-17b-16e-instruct` | candidate | chat completions + JSON-schema mode | $0.27 / $0.85 per M tok |

## Results summary

| model | ok | med time | mean | p90 | min–max | clean workouts | violations | hard failures |
|---|---|---|---|---|---|---|---|---|
| gpt-oss-120b | 50/50 | 47.3s | 55.2s | 103.5s | 13.1–186.1s | 37/50 (74%) | 20 | 0 |
| gpt-oss-20b | 50/50 | 43.3s | 48.5s | 86.0s | 15.2–215.3s | 32/50 (64%) | 36 | 0 |
| llama-3.3-70b-instruct-fp8-fast | 49/50 | 6.6s | 6.8s | 10.1s | 2.5–16.1s | 33/49 (67%) | 35 | 1 |
| llama-4-scout-17b-16e-instruct | 47/50 | 10.3s | 10.0s | 13.6s | 3.3–22.5s | 18/47 (38%) | 52 | 3 |

## Blind judge results (Fable 5, per-case ranking)

| model | mean rank (1=best) | mean score /10 | case wins |
|---|---|---|---|
| gpt-oss-120b | 1.90 | 5.8 | 23 |
| gpt-oss-20b | 2.36 | 5.1 | 13 |
| llama-3.3-70b-instruct-fp8-fast | 2.48 | 5.1 | 12 |
| llama-4-scout-17b-16e-instruct | 3.26 | 3.8 | 2 |

## Conclusions

**Answer to the experiment's question: no.** No Workers AI model produced
equal-or-better workouts faster. What the data shows instead:

1. **gpt-oss-120b (current prod) is clearly the best programmer.** Best blind-judge
   rank (1.90, winning 23 of 50 cases), best clean rate (74%), the only model with
   zero unrecoverable failures. Its weaknesses are chipper volume ceilings and the
   occasional off-vocabulary name — the same known weaknesses the prompt already
   fights, just less often than everyone else.
2. **llama-3.3-70b-fast is a different latency class: ~7× faster** (median 6.6 s vs
   47.3 s, p90 10.1 s vs 103.5 s), and the speed gap is model-inherent, not a
   measurement artifact — the gpt-oss models spend their time on reasoning tokens
   (their retried cases in the fast second window still took 58–96 s, while the
   llamas smoke-tested at 8–10 s even in the slow first window). Its quality is a
   real step down from baseline though (judge rank 2.48 vs 1.90): blueprint
   arithmetic slips (EMOM divisibility, interval window fit, chipper ceilings and
   descent), occasional invented or prefixed movement names, and one case it never
   solved in 3 tries (the 4-machines EMOM 30). Deterministic clean rate (67%) looks
   close to baseline, but the judge saw the craft gap the validator can't measure —
   round sizing, balance, restriction handling.
3. **gpt-oss-20b is pointless for this workload**: only ~10% faster than 120b
   (reasoning dominates its latency too) with quality at llama-3.3's level — the
   worst of both axes.
4. **llama-4-scout is disqualified**: 38% clean, worst judge scores (3.8/10, two
   case wins), three cases failed permanently by hallucinating equipment. Also
   tested and rejected before the main run: glm-4.7-flash (echoed the schema
   instead of a workout; 2.5–3+ min per generation even with thinking disabled) and
   gemma-4-26b (valid output but ~50 s warm — slower than baseline).
5. Cost is a non-factor: every model lands under ~half a cent per workout.

## Plan

1. **Keep `@cf/openai/gpt-oss-120b` in production.** Quality is the product; nothing
   matched it. This branch's model-override plumbing stays experimental — do not
   deploy it (an open per-request `model` field on the public endpoint is not
   something prod should have).
2. **If latency is the pain, attack reasoning effort before switching models**: the
   cheapest promising experiment is `reasoning: {effort: "low"}` on 120b — one line,
   re-runnable through this exact harness (50 cases, validator, blind judge) to see
   what quality it costs. Reasoning tokens are where the 40+ seconds go.
3. **If a truly fast mode is wanted** (e.g. instant regenerate), llama-3.3-70b-fast
   is the only viable base — but adopt it only after a prompt-tuning pass aimed at
   its specific failure modes (EMOM divisibility wording, chipper ceilings,
   JSON-schema mode to kill name slop), judged with this same harness. The current
   SYSTEM_PROMPT was tuned for years against 120b's failure modes; llama-3.3 never
   got that treatment and still came within half a rank at 7× the speed.
4. **A UX route sidesteps the tradeoff entirely**: prefetch a second workout in the
   background after each generation so "regenerate" — the latency-sensitive path —
   is instant, keeping 120b quality. Worth considering before any model change.

## Violation breakdown

**gpt-oss-120b**
- 8 × OFF-VOCABULARY
- 5 × chipper reps over ceiling
- 2 × EMOM token minute
- 1 × repeated base lift (lunge)
- 1 × chipper with 5 movements (want 6-8)
- 1 × two barbell loads
- 1 × chipper row over 1000 m
- 1 × interval work ~4.1 min overflows 3 min window

**gpt-oss-20b**
- 20 × OFF-VOCABULARY
- 7 × chipper reps over ceiling
- 2 × interval work ~3.2 min overflows 3 min window
- 1 × repeated base lift (deadlift)
- 1 × chipper ~13 min vs 35 target (too little)
- 1 × chipper ~22 min vs 45 target (too little)
- 1 × repeated base lift (lunge)
- 1 × interval work ~3.5 min overflows 3 min window
- 1 × interval work ~5.3 min overflows 4 min window
- 1 × interval work ~6.5 min overflows 5 min window

**llama-3.3-70b-instruct-fp8-fast**
- 11 × OFF-VOCABULARY
- 9 × chipper reps over ceiling
- 2 × 9 movements (max 8)
- 2 × repeated base lift (lunge)
- 2 × repeated base lift (squat)
- 1 × 4 stations do not divide EMOM 7
- 1 × 10 movements (max 8)
- 1 × AMRAP round ~6 min (want 2-4)
- 1 × repeated base lift (sit-up)
- 1 × duplicate movement
- 1 × chipper run over 800 m
- 1 × interval work ~5.4 min overflows 4 min window
- 1 × interval format_line unparseable
- 1 × interval work ~6.2 min overflows 4 min window
- FAILED case 2: The model kept using equipment the athlete does not have: Wall Ball, Dumbbell Thruster

**llama-4-scout-17b-16e-instruct**
- 10 × OFF-VOCABULARY
- 5 × duplicate movement
- 3 × AMRAP round ~8 min (want 2-4)
- 2 × chipper reps over ceiling
- 1 × EMOM minute overflows
- 1 × 4 stations do not divide EMOM 7
- 1 × tagged with unlisted equipment
- 1 × chipper ~10 min vs 30 target (too little)
- 1 × chipper with 5 movements (want 6-8)
- 1 × repeated base lift (clean)
- 1 × for-time ~26 min vs cap 18
- 1 × intervals span 20 min vs target 15
- 1 × interval work ~3.1 min overflows 3 min window
- 1 × repeated base lift (lunge)
- 1 × AMRAP round ~7 min (want 2-4)
- 1 × 6 stations do not divide EMOM 16
- 1 × 4 stations do not divide EMOM 9
- 1 × 4 stations do not divide EMOM 14
- 1 × EMOM cal minute too big
- 1 × EMOM token minute
- 1 × repeated base lift (squat)
- 1 × chipper ~7 min vs 15 target (too little)
- 1 × chipper ~6 min vs 20 target (too little)
- 1 × chipper ~10 min vs 25 target (too little)
- 1 × 9 movements (max 8)
- 1 × repeated base lift (deadlift)
- 1 × repeated base lift (swing)
- 1 × repeated base lift (snatch)
- 1 × 10 movements (max 8)
- 1 × intervals span 25 min vs target 20
- 1 × interval work ~2.1 min underfills 4 min window
- 1 × interval work ~3.5 min overflows 3 min window
- 1 × interval work ~4.7 min overflows 3 min window
- 1 × repeated base lift (press)
- 1 × interval work ~4.8 min overflows 4 min window
- 1 × AMRAP round ~6 min (want 2-4)
- FAILED case 5: The model kept using equipment the athlete does not have: Goblet Lunge
- FAILED case 46: The model kept using equipment the athlete does not have: Ring Row
- FAILED case 47: The model kept using equipment the athlete does not have: Row, Row, Row

---

## Appendix — all generations

Raw data: [`results.jsonl`](results.jsonl) (one line per generation, includes
resumed retries), [`analysis.json`](analysis.json) (per-run violations).

### Case 1 — EMOM 7 min · Bodyweight

**gpt-oss-120b** — 74.6s · judge rank 1, score 6/10 · violations: repeated base lift (lunge): Walking Lunge + Reverse Lunge
  `EMOM 7` · scheme: 7 stations × 1 round
  - 15 Push-up
  - 6/leg Walking Lunge
  - 20 Air Squat
  - 8 Burpee
  - 20 Sit-up
  - 6/leg Reverse Lunge
  - 1 min Rest

**gpt-oss-20b** — 31.3s · judge rank 2, score 5/10
  `EMOM 7` · scheme: 7 rounds
  - 12 Push-up

**llama-3.3-70b-instruct-fp8-fast** — 6.8s · judge rank 4, score 3/10 · violations: 4 stations do not divide EMOM 7
  `EMOM 7` · scheme: 4 stations × 7 rounds
  - 12 Burpee
  - 15 Sit-up
  - 20 Jumping Lunge
  - 10 Broad Jump

**llama-4-scout-17b-16e-instruct** — 10.7s · judge rank 3, score 4/10 · violations: EMOM minute overflows: 12/leg Jumping Lunge; 4 stations do not divide EMOM 7
  `EMOM 7` · scheme: 4 stations × 2 rounds
  - 8 Burpee
  - 15 Sit-up
  - 12/leg Jumping Lunge
  - 10 Push-up


### Case 2 — EMOM 30 min · Rower, Bike Erg, Ski Erg, Assault Bike

**gpt-oss-120b** — 54.2s · judge rank 1, score 7/10
  `EMOM 30` · scheme: 5 stations × 6 rounds
  - 100 m Row
  - 10 cal Bike Erg
  - 10 cal Ski Erg
  - 8 cal Assault Bike
  - 1 min Rest

**gpt-oss-20b** — 29.1s · judge rank 2, score 5/10
  `EMOM 32` · scheme: 4 stations × 8 rounds
  - 200 m Row
  - 10 cal Bike Erg
  - 10 cal Ski Erg
  - 8 cal Assault Bike

**llama-3.3-70b-instruct-fp8-fast** — 15.9s · judge rank 4, score 0/10
  - GENERATION FAILED: The model kept using equipment the athlete does not have: Wall Ball, Dumbbell Thruster

**llama-4-scout-17b-16e-instruct** — 14.3s · judge rank 3, score 3/10 · violations: tagged with unlisted equipment: Burpee -> Bodyweight
  `EMOM 30` · scheme: 5 stations × 6 rounds
  - 8 Burpee
  - 10 cal Row
  - 10 cal Bike Erg
  - 10 cal Ski Erg
  - 8 cal Assault Bike


### Case 3 — Chipper 30 min · Bodyweight, Barbell, Kettlebell, Pull-up Bar, Rower

**gpt-oss-120b** — 70.5s · judge rank 4, score 2/10 · violations: chipper with 5 movements (want 6-8)
  `Chipper · cap 30 min`
  - 300 cal Row
  - 50 Kettlebell Swing @ 24 kg
  - 30 Pull-up
  - 20 Deadlift @ 60 kg
  - 10 Air Squat

**gpt-oss-20b** — 58.0s · judge rank 2, score 3/10 · violations: OFF-VOCABULARY: Barbell Deadlift; OFF-VOCABULARY: Push Up; chipper reps over ceiling: 120 Kettlebell Swing; chipper reps over ceiling: 80 Pull-up; chipper reps over ceiling: 80 Air Squat; chipper reps over ceiling: 70 Barbell Deadlift; chipper reps over ceiling: 80 Push Up
  `Chipper · cap 30 min`
  - 1000 m Row
  - 120 Kettlebell Swing @ 24 kg
  - 80 Pull-up
  - 80 Air Squat
  - 70 Barbell Deadlift @ 60 kg
  - 80 Push Up

**llama-3.3-70b-instruct-fp8-fast** — 12.6s · judge rank 1, score 5/10 · violations: OFF-VOCABULARY: Barbell Deadlift; OFF-VOCABULARY: Kettlebell Goblet Squat; OFF-VOCABULARY: Barbell Hang Power Clean; chipper reps over ceiling: 80 Pull-up; chipper reps over ceiling: 60 Barbell Deadlift
  `Chipper · cap 33 min`
  - 80 Pull-up
  - 60 Barbell Deadlift @ 60 kg
  - 50 Kettlebell Swing @ 24 kg
  - 40 Burpee
  - 500 m Row
  - 30 Toes-to-Bar
  - 20 Kettlebell Goblet Squat @ 24 kg
  - 15 Barbell Hang Power Clean @ 60 kg

**llama-4-scout-17b-16e-instruct** — 10.0s · judge rank 3, score 3/10 · violations: chipper ~10 min vs 30 target (too little); chipper with 5 movements (want 6-8)
  `Chipper · cap 33 min`
  - 500 m Row
  - 24 Pull-up
  - 30 Deadlift @ 40 kg
  - 40 Kettlebell Swing @ 16 kg
  - 18 Burpee


### Case 4 — AMRAP 20 min · Bodyweight, Dumbbells, Kettlebell

**gpt-oss-120b** — 25.9s · judge rank 1, score 8/10
  `AMRAP 20 min`
  - 8 Dumbbell Snatch @ 22.5 kg
  - 8 Kettlebell Clean @ 24 kg
  - 8 Dumbbell Front-Rack Lunge @ 22.5 kg
  - 10 Push-up
  - 12 Goblet Squat @ 24 kg
  - 6 Burpee

**gpt-oss-20b** — 54.2s · judge rank 3, score 5/10
  `AMRAP 20 min`
  - 8 Dumbbell Deadlift @ 40 kg
  - 10 Kettlebell Swing @ 20 kg
  - 15 Push-up
  - 12/leg Dumbbell Front-Rack Lunge @ 40 kg
  - 10 Kettlebell Push Press @ 20 kg

**llama-3.3-70b-instruct-fp8-fast** — 8.6s · judge rank 4, score 4/10 · violations: OFF-VOCABULARY: Kettlebell Goblet Squat
  `AMRAP 20 min`
  - 6/leg Dumbbell Front-Rack Lunge @ 20 kg
  - 9 Kettlebell Goblet Squat @ 20 kg
  - 6/arm Dumbbell Snatch @ 20 kg
  - 12 Bear Crawl
  - 9 Kettlebell Swing @ 20 kg

**llama-4-scout-17b-16e-instruct** — 13.6s · judge rank 2, score 7/10
  `AMRAP 20 min`
  - 8 Dumbbell Deadlift @ 2×22.5 kg
  - 8/arm Kettlebell Clean @ 24 kg
  - 10/leg Reverse Lunge
  - 12 Kettlebell Swing @ 24 kg
  - 6 Dumbbell Push Press @ 2×22.5 kg
  - 10 Hand-Release Push-up


### Case 5 — For Time 25 min · Bodyweight, Barbell, Pull-up Bar

**gpt-oss-120b** — 34.2s · judge rank 3, score 4/10 · violations: OFF-VOCABULARY: Front Rack Lunge
  `For Time · cap 28 min` · scheme: 8 Rounds
  - 8 Deadlift @ 60 kg
  - 8/leg Front Rack Lunge @ 60 kg
  - 8 Pull-up
  - 15 Push-up
  - 8 Bar-Facing Burpee

**gpt-oss-20b** — 52.3s · judge rank 2, score 5/10
  `For Time · cap 28 min` · scheme: 5 Rounds
  - 15 Burpee
  - 15 Pull-up
  - 30 Front-Rack Lunge @ 50 kg

**llama-3.3-70b-instruct-fp8-fast** — 9.5s · judge rank 1, score 8/10
  `For Time · cap 28 min` · scheme: 5 Rounds
  - 9 Front-Rack Lunge @ 40 kg
  - 12 Pull-up
  - 9 Burpee
  - 12 Air Squat
  - 6 Power Clean @ 40 kg

**llama-4-scout-17b-16e-instruct** — 11.9s · judge rank 4, score 0/10
  - GENERATION FAILED: The model kept using equipment the athlete does not have: Goblet Lunge


### Case 6 — AMRAP 45 min · Bodyweight, Barbell, Dumbbells, Kettlebell, Pull-up Bar, Rings, Rower, Jump Rope, Plyo Box, Wall Ball, Running

**gpt-oss-120b** — 103.5s · judge rank 3, score 5/10
  `AMRAP 45 min`
  - 250 m Row
  - 400 m Run
  - 30 Double-Under
  - 5 Pull-up
  - 5 Ring Dip
  - 3 Deadlift @ 80 kg
  - 3/arm Dumbbell Snatch @ 22.5 kg
  - 8 Kettlebell Swing @ 24 kg

**gpt-oss-20b** — 82.2s · judge rank 1, score 8/10
  `AMRAP 45 min`
  - 3 Deadlift @ 80 kg
  - 6 Dumbbell Thruster @ 2×22.5 kg
  - 12 Kettlebell Swing @ 24 kg
  - 10 Double-Under
  - 8 Push-up
  - 5 Pull-up
  - 250 m Row
  - 10 Wall Ball @ 9 kg

**llama-3.3-70b-instruct-fp8-fast** — 15.0s · judge rank 4, score 4/10 · violations: 10 movements (max 8); AMRAP round ~6 min (want 2-4)
  `AMRAP 45 min`
  - 6 Power Clean @ 50 kg
  - 9 Dumbbell Thruster @ 2×20 kg
  - 15 Kettlebell Swing @ 20 kg
  - 10 cal Row
  - 10 Pull-up
  - 20 Double-Under
  - 10 Wall Ball @ 9 kg
  - 3 Box Jump
  - 12 Ring Row
  - 100 m Run

**llama-4-scout-17b-16e-instruct** — 11.5s · judge rank 2, score 5/10 · violations: OFF-VOCABULARY: 250 m; AMRAP round ~8 min (want 2-4)
  `AMRAP 45 min`
  - 3 Deadlift @ 60 kg
  - 250 m 250 m
  - 5 Pull-up
  - 6/leg Dumbbell Snatch @ 22.5 kg
  - 8 Ring Dip
  - 12 Kettlebell Swing @ 24 kg
  - 5 Burpee


### Case 7 — For Time 15 min · Bodyweight, Barbell, Dumbbells
*Athlete request:* `no overhead today`

**gpt-oss-120b** — 68.2s · judge rank 1, score 7/10
  `For Time · cap 18 min`
  - 21-15-9 Deadlift @ 50 kg
  - 21-15-9 Front-Rack Lunge @ 2×22.5 kg
  - 21-15-9 Push-up
  - 21-15-9 Sumo Deadlift High Pull @ 50 kg
  - 21-15-9 Sit-up

**gpt-oss-20b** — 86.9s · judge rank 3, score 5/10 · violations: OFF-VOCABULARY: Dumbbell Front Rack Lunge; repeated base lift (deadlift): Deadlift + Dumbbell Deadlift
  `For Time · cap 18 min` · scheme: 5 Rounds
  - 6 Deadlift @ 50 kg
  - 12 Burpee
  - 10 Front Squat @ 50 kg
  - 6 Dumbbell Deadlift @ 2×22.5 kg
  - 6 Dumbbell Front Rack Lunge @ 2×22.5 kg
  - *notes: null*

**llama-3.3-70b-instruct-fp8-fast** — 4.3s · judge rank 2, score 6/10 · violations: OFF-VOCABULARY: Barbell Deadlift
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 18 Air Squat
  - 12/leg Dumbbell Front-Rack Lunge @ 22.5 kg
  - 15 Barbell Deadlift @ 50 kg
  - 12 Burpee

**llama-4-scout-17b-16e-instruct** — 13.2s · judge rank 4, score 3/10 · violations: repeated base lift (clean): Squat Clean + Dumbbell Clean; for-time ~26 min vs cap 18
  `For Time · cap 18 min` · scheme: 4 Rounds
  - 9 Deadlift @ 50 kg
  - 12/leg Dumbbell Front-Rack Lunge @ 22.5 kg
  - 12 Burpee
  - 6 Squat Clean @ 50 kg
  - 15 Dumbbell Clean @ 22.5 kg
  - 18 Air Squat


### Case 8 — AMRAP 12 min · Bodyweight, Kettlebell, Pull-up Bar
*Athlete request:* `no overhead`

**gpt-oss-120b** — 68.3s · judge rank 3, score 4/10
  `AMRAP 12 min`
  - 4 Toes-to-Bar
  - 5 Kettlebell Deadlift @ 24 kg
  - 5 Goblet Squat @ 24 kg
  - 8 Kettlebell Swing @ 24 kg
  - 5 Burpee

**gpt-oss-20b** — 21.3s · judge rank 1, score 8/10
  `AMRAP 12 min`
  - 15 Kettlebell Swing @ 24 kg
  - 12 Pull-up
  - 5 Burpee

**llama-3.3-70b-instruct-fp8-fast** — 10.1s · judge rank 4, score 2/10 · violations: OFF-VOCABULARY: Kettlebell GHD Sit-up; repeated base lift (sit-up): Sit-up + Kettlebell GHD Sit-up; 9 movements (max 8)
  `AMRAP 12 min`
  - 6 Kettlebell Deadlift @ 24 kg
  - 6 Pull-up
  - 12 Air Squat
  - 9 Sit-up
  - 6 Kettlebell Swing @ 24 kg
  - 9 Burpee
  - 6 Hanging Knee Raise
  - 9 Bear Crawl
  - 6 Kettlebell GHD Sit-up @ 24 kg

**llama-4-scout-17b-16e-instruct** — 11.1s · judge rank 2, score 6/10
  `AMRAP 12 min`
  - 8 Kettlebell Deadlift @ 24 kg
  - 6 Pull-up
  - 12 Sit-up
  - 12/leg Goblet Lunge @ 24 kg
  - 8 Toes-to-Bar
  - 10 Hand-Release Push-up


### Case 9 — Intervals 15 min · Running, Bodyweight

**gpt-oss-120b** — 56.2s · judge rank 3, score 5/10
  `5 × 2 min on / 1 min rest` · scheme: 4 stations × 5 rounds
  - 200 m Run
  - 4 Air Squat
  - 4 Push-up
  - 8 Sit-up
  - *notes: ≈15 sec remainder each 2‑min on interval*

**gpt-oss-20b** — 93.0s · judge rank 2, score 7/10
  `3 × 4 min on / 1 min rest`
  - 100 m Run
  - 20 Sit-up
  - 20 Burpee
  - 8 Push-up
  - 8 Air Squat

**llama-3.3-70b-instruct-fp8-fast** — 8.2s · judge rank 1, score 8/10
  `3 × 4 min on / 1 min rest`
  - 200 m Run
  - 12 Burpee
  - 12 Air Squat
  - 20 Sit-up

**llama-4-scout-17b-16e-instruct** — 7.0s · judge rank 4, score 4/10 · violations: intervals span 20 min vs target 15; interval work ~3.1 min overflows 3 min window
  `5 × 3 min on / 1 min rest`
  - 10 Burpee
  - 15 Air Squat
  - 200 m Run
  - 10 Sit-up


### Case 10 — AMRAP 16 min · Kettlebell, Dumbbells, Bodyweight

**gpt-oss-120b** — 33.1s · judge rank 1, score 7/10
  `AMRAP 16 min`
  - 12 Kettlebell Swing @ 24 kg
  - 6 Push-up
  - 5 Dumbbell Deadlift @ 2×22.5 kg
  - 5/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 8 Sit-up

**gpt-oss-20b** — 29.0s · judge rank 3, score 5/10 · violations: OFF-VOCABULARY: Push Up
  `AMRAP 16 min`
  - 15 Kettlebell Swing @ 24 kg
  - 10 Dumbbell Deadlift @ 2×22.5 kg
  - 12 Push Up
  - 12 Sit-up

**llama-3.3-70b-instruct-fp8-fast** — 4.8s · judge rank 2, score 6/10
  `AMRAP 16 min`
  - 12 Kettlebell Swing @ 20 kg
  - 12/leg Walking Lunge
  - 12 Dumbbell Deadlift @ 22.5 kg
  - 12 Burpee

**llama-4-scout-17b-16e-instruct** — 12.1s · judge rank 4, score 2/10 · violations: OFF-VOCABULARY: Dumbbell Lunge; repeated base lift (lunge): Dumbbell Lunge + Goblet Lunge; AMRAP round ~8 min (want 2-4)
  `AMRAP 16 min`
  - 40 Kettlebell Swing @ 24 kg
  - 15 Dumbbell Deadlift @ 2×22.5 kg
  - 10 Burpee
  - 10/leg Dumbbell Lunge @ 2×22.5 kg
  - 10/leg Goblet Lunge @ 24 kg
  - 20 Sit-up


### Case 11 — AMRAP 5 min · Bodyweight

**gpt-oss-120b** — 20.6s · judge rank 1, score 8/10
  `AMRAP 5 min`
  - 12/leg Reverse Lunge
  - 15 Push-up
  - 25 m Bear Crawl
  - 20 Sit-up

**gpt-oss-20b** — 45.6s · judge rank 2, score 6/10
  `AMRAP 5 min`
  - 12 Air Squat
  - 10 Push-up
  - 10 Sit-up
  - 5 Broad Jump

**llama-3.3-70b-instruct-fp8-fast** — 3.1s · judge rank 4, score 4/10
  `AMRAP 5 min`
  - 12 Jumping Lunge
  - 12 Broad Jump
  - 15 Sit-up

**llama-4-scout-17b-16e-instruct** — 4.1s · judge rank 3, score 5/10
  `AMRAP 5 min`
  - 10 Burpee
  - 15 Air Squat
  - 12/leg Walking Lunge


### Case 12 — AMRAP 10 min · Bodyweight, Jump Rope

**gpt-oss-120b** — 15.1s · judge rank 1, score 7/10
  `AMRAP 10 min`
  - 10/leg Reverse Lunge
  - 5 Burpee
  - 15 Double-Under
  - 25 m Bear Crawl

**gpt-oss-20b** — 22.3s · judge rank 3, score 5/10
  `AMRAP 10 min`
  - 5/leg Reverse Lunge
  - 5 Push-up
  - 20 Double-Under

**llama-3.3-70b-instruct-fp8-fast** — 5.1s · judge rank 2, score 5/10
  `AMRAP 10 min`
  - 12 Air Squat
  - 9 Sit-up
  - 6 Broad Jump
  - 50 Single-Under

**llama-4-scout-17b-16e-instruct** — 8.9s · judge rank 4, score 2/10
  `AMRAP 10 min`
  - 5 Burpee
  - 8 Sit-up
  - 6 Deadlift @ 60 kg
  - 30 Double-Under


### Case 13 — AMRAP 15 min · Barbell, Bodyweight

**gpt-oss-120b** — 15.5s · judge rank 2, score 7/10
  `AMRAP 15 min`
  - 20 Sit-up
  - 15 Jumping Lunge
  - 5 Deadlift @ 40 kg
  - 5 Front Squat @ 40 kg
  - 5 Push Press @ 40 kg

**gpt-oss-20b** — 45.3s · judge rank 3, score 6/10
  `AMRAP 15 min`
  - 30 Sit-up
  - 8 Front Squat @ 50 kg
  - 7 Hang Power Clean @ 50 kg

**llama-3.3-70b-instruct-fp8-fast** — 2.9s · judge rank 1, score 8/10
  `AMRAP 15 min`
  - 12 Front Squat @ 40 kg
  - 12 Push Press @ 40 kg
  - 25 Sit-up
  - 12 Bar-Facing Burpee

**llama-4-scout-17b-16e-instruct** — 5.4s · judge rank 4, score 4/10
  `AMRAP 15 min`
  - 12 Thruster @ 40 kg
  - 15 Burpee
  - 10 Front Squat @ 40 kg
  - 20 Sit-up
  - 12 Push Press @ 40 kg


### Case 14 — AMRAP 20 min · Kettlebell, Pull-up Bar, Bodyweight

**gpt-oss-120b** — 42.5s · judge rank 1, score 8/10
  `AMRAP 20 min`
  - 15 Kettlebell Swing @ 24 kg
  - 8 Pull-up
  - 12 Goblet Squat @ 24 kg
  - 8 Burpee
  - 6/arm Kettlebell Snatch @ 24 kg

**gpt-oss-20b** — 25.1s · judge rank 2, score 7/10
  `AMRAP 20 min`
  - 30 Kettlebell Swing @ 20 kg
  - 8 Pull-up
  - 10 Goblet Squat @ 20 kg
  - 10 Burpee

**llama-3.3-70b-instruct-fp8-fast** — 4.4s · judge rank 4, score 6/10
  `AMRAP 20 min`
  - 12 Kettlebell Swing @ 20 kg
  - 12 Pull-up
  - 20 Air Squat

**llama-4-scout-17b-16e-instruct** — 4.5s · judge rank 3, score 7/10
  `AMRAP 20 min`
  - 10 Burpee
  - 12 Pull-up
  - 20 Kettlebell Swing @ 24 kg
  - 15 Air Squat


### Case 15 — AMRAP 25 min · Dumbbells, Plyo Box, Bodyweight

**gpt-oss-120b** — 44.3s · judge rank 1, score 7/10
  `AMRAP 25 min`
  - 15 Air Squat
  - 12 Dumbbell Push Press @ 2×15 kg
  - 12/leg Dumbbell Front-Rack Lunge @ 2×15 kg
  - 12 Dumbbell Deadlift @ 2×15 kg
  - 8 Burpee Box Jump-Over

**gpt-oss-20b** — 21.9s · judge rank 3, score 5/10
  `AMRAP 25 min`
  - 12 Dumbbell Thruster @ 2×22.5 kg
  - 12/leg Dumbbell Box Step-Up @ 2×22.5 kg
  - 30 Air Squat

**llama-3.3-70b-instruct-fp8-fast** — 3.9s · judge rank 2, score 6/10
  `AMRAP 25 min`
  - 12 Dumbbell Front-Rack Lunge @ 22.5 kg
  - 12 Box Jump
  - 20 Air Squat
  - 12 Dumbbell Thruster @ 22.5 kg

**llama-4-scout-17b-16e-instruct** — 12.1s · judge rank 4, score 3/10 · violations: OFF-VOCABULARY: Dumbbell Squat Clean
  `AMRAP 25 min`
  - 10 Air Squat
  - 6/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 5 Box Jump
  - 5 Burpee
  - 4 Dumbbell Squat Clean @ 2×22.5 kg
  - 4 Burpee Box Jump-Over


### Case 16 — AMRAP 30 min · Bodyweight, Barbell, Wall Ball, Rower

**gpt-oss-120b** — 13.1s · judge rank 2, score 7/10
  `AMRAP 30 min`
  - 10 Deadlift @ 60 kg
  - 15 Wall Ball @ 6 kg
  - 12/leg Walking Lunge
  - 250 m Row

**gpt-oss-20b** — 20.2s · judge rank 1, score 8/10
  `AMRAP 30 min`
  - 8 Deadlift @ 70 kg
  - 12 Wall Ball @ 9 kg
  - 12/leg Walking Lunge
  - 250 m Row

**llama-3.3-70b-instruct-fp8-fast** — 3.1s · judge rank 3, score 7/10
  `AMRAP 30 min`
  - 18 Air Squat
  - 15 Deadlift @ 50 kg
  - 12 Wall Ball @ 9 kg
  - 250 m Row

**llama-4-scout-17b-16e-instruct** — 10.0s · judge rank 4, score 4/10 · violations: OFF-VOCABULARY: Rower
  `AMRAP 30 min`
  - 10 Deadlift @ 50 kg
  - 15 Hang Power Clean @ 50 kg
  - 12 Wall Ball @ 9 kg
  - 250 m Rower
  - 12 Burpee


### Case 17 — AMRAP 12 min · Kettlebell

**gpt-oss-120b** — 23.9s · judge rank 2, score 4/10 · violations: OFF-VOCABULARY: Kettlebell Goblet Squat; OFF-VOCABULARY: Kettlebell Overhead Lunge
  `AMRAP 12 min`
  - 25 Kettlebell Swing @ 16 kg
  - 12 Kettlebell Goblet Squat @ 16 kg
  - 8 Kettlebell Push Press @ 16 kg
  - 8/leg Kettlebell Overhead Lunge @ 16 kg

**gpt-oss-20b** — 41.3s · judge rank 3, score 2/10
  `AMRAP 12 min`
  - 6/arm Turkish Get-Up @ 20 kg
  - 15 Kettlebell Swing @ 20 kg
  - 6 Kettlebell Push Press @ 20 kg
  - 6 Goblet Squat @ 20 kg
  - 8 Kettlebell Clean @ 20 kg

**llama-3.3-70b-instruct-fp8-fast** — 3.4s · judge rank 1, score 7/10 · violations: OFF-VOCABULARY: Kettlebell Goblet Squat
  `AMRAP 12 min`
  - 12 Kettlebell Goblet Squat @ 20 kg
  - 12 Kettlebell Push Press @ 20 kg
  - 12 Goblet Lunge @ 20 kg
  - 24 Kettlebell Swing @ 20 kg

**llama-4-scout-17b-16e-instruct** — 9.3s · judge rank 4, score 1/10 · violations: AMRAP round ~7 min (want 2-4)
  `AMRAP 12 min`
  - 30 Kettlebell Swing @ 24 kg
  - 12 Goblet Squat @ 24 kg
  - 18/leg Kettlebell Clean @ 24 kg
  - 6/arm Turkish Get-Up @ 24 kg
  - 15 Kettlebell Push Press @ 24 kg


### Case 18 — AMRAP 18 min · Dumbbells, Sandbag, Bodyweight

**gpt-oss-120b** — 31.4s · judge rank 1, score 8/10
  `AMRAP 18 min`
  - 6 Dumbbell Snatch @ 22.5 kg
  - 6 Sandbag Clean @ 30 kg
  - 6/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 10 Push-up
  - 50 m Sandbag Carry @ 30 kg
  - 10 Air Squat

**gpt-oss-20b** — 36.9s · judge rank 3, score 4/10
  `AMRAP 18 min`
  - 8 Dumbbell Clean @ 40 kg
  - 15 Burpee
  - 12/leg Sandbag Lunge @ 20 kg
  - 8 Dumbbell Push Press @ 40 kg
  - 50 m Sandbag Carry @ 20 kg

**llama-3.3-70b-instruct-fp8-fast** — 2.5s · judge rank 2, score 5/10
  `AMRAP 18 min`
  - 12 Dumbbell Hang Clean & Jerk @ 22.5 kg
  - 12 Sandbag Clean @ 40 kg
  - 20 Bear Crawl
  - 20 Walking Lunge

**llama-4-scout-17b-16e-instruct** — 11.2s · judge rank 4, score 3/10 · violations: AMRAP round ~8 min (want 2-4)
  `AMRAP 18 min`
  - 12/arm Dumbbell Snatch @ 2×22.5 kg
  - 10/leg Sandbag Lunge @ 40 kg
  - 10 Burpee
  - 15/arm Dumbbell Clean @ 2×22.5 kg
  - 8 Shoulder-to-Shoulder Press @ 40 kg
  - 15 Hand-Release Push-up


### Case 19 — For Time 8 min · Bodyweight, Kettlebell

**gpt-oss-120b** — 24.9s · judge rank 3, score 5/10
  `For Time · cap 11 min` · scheme: 4 Rounds
  - 12 Kettlebell Swing @ 16 kg
  - 10 Goblet Squat @ 16 kg
  - 8 Walking Lunge
  - 6 Burpee
  - 10 Sit-up

**gpt-oss-20b** — 50.9s · judge rank 1, score 7/10
  `For Time · cap 11 min` · scheme: 5 Rounds
  - 25 Kettlebell Swing @ 20 kg
  - 15 Push-up

**llama-3.3-70b-instruct-fp8-fast** — 8.0s · judge rank 2, score 6/10
  `For Time · cap 11 min` · scheme: 3 Rounds
  - 20 Air Squat
  - 20 Kettlebell Swing @ 20 kg
  - 15 Sit-up
  - 12 Kettlebell Clean @ 20 kg

**llama-4-scout-17b-16e-instruct** — 10.3s · judge rank 4, score 4/10
  `For Time · cap 11 min`
  - 50 Kettlebell Swing @ 24 kg
  - 20 Burpee
  - 15 Goblet Squat @ 24 kg
  - 30 Sit-up
  - 20/arm Kettlebell Clean @ 24 kg
  - 25 Hand-Release Push-up


### Case 20 — For Time 12 min · Barbell

**gpt-oss-120b** — 37.9s · judge rank 3, score 4/10
  `For Time · cap 15 min` · scheme: 4 Rounds
  - 12 Front Squat @ 40 kg
  - 12 Push Press @ 40 kg
  - 12 Sumo Deadlift High Pull @ 40 kg
  - 12 Push Jerk @ 40 kg

**gpt-oss-20b** — 51.7s · judge rank 2, score 6/10
  `For Time · cap 15 min` · scheme: 5 Rounds
  - 12 Push Press @ 40 kg
  - 12 Sumo Deadlift High Pull @ 40 kg
  - 12 Front Squat @ 40 kg

**llama-3.3-70b-instruct-fp8-fast** — 3.4s · judge rank 4, score 3/10
  `For Time · cap 15 min` · scheme: 3 Rounds
  - 12 Push Press @ 40 kg
  - 18 Front Squat @ 40 kg
  - 24 Thruster @ 40 kg

**llama-4-scout-17b-16e-instruct** — 3.3s · judge rank 1, score 7/10
  `For Time · cap 15 min` · scheme: 3 Rounds
  - 12 Squat Clean @ 40 kg
  - 12 Push Jerk @ 40 kg
  - 12 Overhead Squat @ 40 kg


### Case 21 — For Time 20 min · Bodyweight, Dumbbells, Pull-up Bar, Rower

**gpt-oss-120b** — 31.5s · judge rank 3, score 5/10
  `For Time · cap 23 min` · scheme: 5 Rounds
  - 250 m Row
  - 4 Pull-up
  - 10 Push-up
  - 8/leg Dumbbell Front-Rack Lunge @ 2×15 kg
  - 6 Dumbbell Push Press @ 2×15 kg
  - 50 m Farmers Carry @ 2×15 kg
  - 15 Sit-up

**gpt-oss-20b** — 40.4s · judge rank 1, score 7/10
  `For Time · cap 23 min` · scheme: 5 Rounds
  - 400 m Row
  - 10 Pull-up
  - 10 Dumbbell Thruster @ 2×20 kg
  - 20 Sit-up

**llama-3.3-70b-instruct-fp8-fast** — 4.3s · judge rank 4, score 5/10
  `For Time · cap 23 min` · scheme: 3 Rounds
  - 18 Dumbbell Front-Rack Lunge @ 22.5 kg
  - 250 m Row
  - 12 Pull-up
  - 30 Burpee

**llama-4-scout-17b-16e-instruct** — 13.1s · judge rank 2, score 6/10 · violations: OFF-VOCABULARY: Rower
  `For Time · cap 23 min` · scheme: 3 Rounds
  - 10/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 200 m Rower
  - 10 Chest-to-Bar Pull-up
  - 12 Dumbbell Push Press @ 2×22.5 kg
  - 15 Sit-up
  - 15 Dumbbell Deadlift @ 2×22.5 kg


### Case 22 — For Time 30 min · Bodyweight, Barbell, Kettlebell, Running

**gpt-oss-120b** — 186.1s · judge rank 1, score 7/10 · violations: OFF-VOCABULARY: Barbell Deadlift; OFF-VOCABULARY: Barbell Push Press
  `For Time · cap 33 min` · scheme: 7 Rounds
  - 10 Barbell Deadlift @ 40 kg
  - 10 Barbell Push Press @ 40 kg
  - 10 Kettlebell Swing @ 24 kg
  - 10 Air Squat
  - 10 Push-up
  - 10 Sit-up
  - 200 m Run

**gpt-oss-20b** — 54.6s · judge rank 2, score 5/10
  `For Time · cap 33 min` · scheme: 5 Rounds
  - 18 Deadlift @ 60 kg
  - 28 Kettlebell Swing @ 20 kg
  - 12 Burpee
  - 8 Push Press @ 60 kg
  - 200 m Run

**llama-3.3-70b-instruct-fp8-fast** — 4.7s · judge rank 3, score 5/10
  `For Time · cap 33 min` · scheme: 5 Rounds
  - 18 Deadlift @ 60 kg
  - 24 Kettlebell Swing @ 20 kg
  - 30 Air Squat
  - 400 m Run

**llama-4-scout-17b-16e-instruct** — 3.5s · judge rank 4, score 4/10
  `For Time · cap 33 min` · scheme: 4 Rounds
  - 15 Deadlift @ 60 kg
  - 30 Kettlebell Swing @ 24 kg
  - 12 Burpee
  - 400 m Run


### Case 23 — For Time 40 min · Bodyweight, Barbell, Dumbbells, Kettlebell, Pull-up Bar, Rings, Rower, Jump Rope

**gpt-oss-120b** — 38.2s · judge rank 3, score 4/10
  `For Time · cap 43 min` · scheme: 5 Rounds
  - 12 Pull-up
  - 15 Front Squat @ 40 kg
  - 12/arm Dumbbell Snatch @ 12.5 kg
  - 15 Kettlebell Swing @ 20 kg
  - 250 m Row
  - 30 Double-Under

**gpt-oss-20b** — 40.3s · judge rank 4, score 3/10 · violations: OFF-VOCABULARY: Dumbbell Hang Clean
  `For Time · cap 43 min` · scheme: 5 Rounds
  - 80 Double-Under
  - 30 Pull-up
  - 40 Kettlebell Swing @ 20 kg
  - 30 Ring Row
  - 18 Deadlift @ 80 kg
  - 12/arm Dumbbell Hang Clean @ 22.5 kg

**llama-3.3-70b-instruct-fp8-fast** — 14.4s · judge rank 1, score 6/10 · violations: OFF-VOCABULARY: Barbell Front-Rack Lunge
  `For Time · cap 43 min` · scheme: 4 Rounds
  - 12 Pull-up
  - 18 Ring Row
  - 250 m Row
  - 21 Dumbbell Hang Clean & Jerk @ 20 kg
  - 12/leg Barbell Front-Rack Lunge @ 40 kg
  - 50 Double-Under
  - 15 Kettlebell Swing @ 20 kg
  - 18 Burpee

**llama-4-scout-17b-16e-instruct** — 7.4s · judge rank 2, score 5/10
  `For Time · cap 43 min` · scheme: 5 Rounds
  - 250 m Row
  - 12 Chest-to-Bar Pull-up
  - 15 Deadlift @ 40 kg
  - 12/arm Dumbbell Snatch @ 2×22.5 kg
  - 21 Kettlebell Swing @ 16 kg
  - 12 Ring Dip
  - 9 Burpee
  - 90 Double-Under


### Case 24 — For Time 10 min · Bodyweight, Jump Rope

**gpt-oss-120b** — 56.3s · judge rank 1, score 7/10
  `For Time · cap 13 min` · scheme: 5 Rounds
  - 20 Double-Under
  - 6 Broad Jump
  - 12 Reverse Lunge
  - 12 Push-up

**gpt-oss-20b** — 25.7s · judge rank 3, score 5/10
  `For Time · cap 13 min` · scheme: 5 Rounds
  - 15 Walking Lunge
  - 20 Push-Up
  - 30 Single-Under

**llama-3.3-70b-instruct-fp8-fast** — 6.5s · judge rank 2, score 6/10
  `For Time · cap 13 min` · scheme: 3 Rounds
  - 20 Air Squat
  - 15 Sit-up
  - 10 Burpee
  - 50 Single-Under

**llama-4-scout-17b-16e-instruct** — 4.3s · judge rank 4, score 3/10
  `For Time · cap 13 min`
  - 10 Burpee
  - 90 Double-Under
  - 30 Air Squat
  - 120 Single-Under
  - 20 Sit-up


### Case 25 — For Time 15 min · Wall Ball, Rower, Bodyweight

**gpt-oss-120b** — 31.0s · judge rank 4, score 5/10
  `For Time · cap 18 min` · scheme: 5 Rounds
  - 250 m Row
  - 12 Wall Ball @ 6 kg
  - 12 Air Squat
  - 8 Push-up
  - 6 Burpee

**gpt-oss-20b** — 33.9s · judge rank 1, score 8/10
  `For Time · cap 18 min` · scheme: 5 Rounds
  - 250 m Row
  - 18 Wall Ball @ 9 kg
  - 12 Burpee
  - 12 Air Squat

**llama-3.3-70b-instruct-fp8-fast** — 6.6s · judge rank 2, score 7/10
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 18 Wall Ball @ 9 kg
  - 250 m Row
  - 24 Air Squat
  - 18 Burpee

**llama-4-scout-17b-16e-instruct** — 3.7s · judge rank 3, score 5/10 · violations: OFF-VOCABULARY: Rower
  `For Time · cap 18 min` · scheme: 4 Rounds
  - 15 Burpee
  - 250 m Rower
  - 21 Wall Ball @ 6 kg
  - 30 Air Squat


### Case 26 — EMOM 10 min · Kettlebell, Bodyweight

**gpt-oss-120b** — 24.4s · judge rank 2, score 7/10
  `EMOM 10` · scheme: 5 stations × 2 rounds
  - 20 Kettlebell Swing @ 16 kg
  - 12 Goblet Squat @ 16 kg
  - 8 Kettlebell Push Press @ 16 kg
  - 10 Walking Lunge
  - 20 Sit-up

**gpt-oss-20b** — 22.1s · judge rank 1, score 8/10
  `EMOM 10` · scheme: 5 stations × 2 rounds
  - 20 Kettlebell Swing @ 20 kg
  - 15 Goblet Squat @ 20 kg
  - 15 Push-up
  - 10 Burpee
  - 20 Sit-up

**llama-3.3-70b-instruct-fp8-fast** — 2.9s · judge rank 3, score 6/10
  `EMOM 10` · scheme: 5 stations × 2 rounds
  - 12 Kettlebell Swing @ 20 kg
  - 12 Burpee
  - 12 Goblet Squat @ 20 kg
  - 12 Push-up
  - 12 Kettlebell Clean @ 20 kg

**llama-4-scout-17b-16e-instruct** — 8.8s · judge rank 4, score 5/10
  `EMOM 10` · scheme: 5 rounds
  - 10 Burpee
  - 15 Kettlebell Swing @ 16 kg
  - 12 Sit-up
  - 8 Kettlebell Clean @ 16 kg
  - 10 Push-up


### Case 27 — EMOM 12 min · Barbell, Dumbbells, Bodyweight

**gpt-oss-120b** — 62.8s · judge rank 1, score 8/10
  `EMOM 12` · scheme: 3 stations × 4 rounds
  - 6 Deadlift @ 60 kg
  - 50 m Farmers Carry @ 2×22.5 kg
  - 10 Push-up

**gpt-oss-20b** — 23.1s · judge rank 4, score 5/10 · violations: OFF-VOCABULARY: Dumbbell Clean & Jerk
  `EMOM 12` · scheme: 3 stations × 4 rounds
  - 5 Deadlift @ 80 kg
  - 8 Dumbbell Clean & Jerk @ 2×22.5 kg
  - 12 Push-up

**llama-3.3-70b-instruct-fp8-fast** — 9.9s · judge rank 2, score 7/10
  `EMOM 12` · scheme: 3 stations × 4 rounds
  - 9 Deadlift @ 50 kg
  - 12 Dumbbell Snatch @ 22.5 kg
  - 15 Jumping Lunge

**llama-4-scout-17b-16e-instruct** — 8.6s · judge rank 3, score 6/10
  `EMOM 12` · scheme: 3 stations × 4 rounds
  - 8 Deadlift @ 40 kg
  - 12 Dumbbell Clean @ 22.5 kg
  - 10 Burpee


### Case 28 — EMOM 16 min · Dumbbells, Plyo Box, Rower, Bodyweight

**gpt-oss-120b** — 74.6s · judge rank 3, score 4/10 · violations: EMOM token minute: 4 cal Row; EMOM token minute: 5 Push-up
  `EMOM 16` · scheme: 4 stations × 4 rounds
  - 4 cal Row
  - 5/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 5 Box Jump
  - 5 Push-up

**gpt-oss-20b** — 53.0s · judge rank 2, score 5/10 · violations: OFF-VOCABULARY: Rower
  `EMOM 16 min` · scheme: 4 stations × 4 rounds
  - 200 m Rower
  - 12 Dumbbell Deadlift @ 2×20 kg
  - 12 Dumbbell Box Step-Up @ 2×20 kg
  - 15 Air Squat

**llama-3.3-70b-instruct-fp8-fast** — 6.1s · judge rank 1, score 6/10
  `EMOM 16` · scheme: 4 stations × 4 rounds
  - 10 Dumbbell Hang Clean & Jerk @ 20 kg
  - 5/leg Dumbbell Front-Rack Lunge @ 20 kg
  - 10 Box Jump
  - 10 cal Row

**llama-4-scout-17b-16e-instruct** — 13.0s · judge rank 4, score 4/10 · violations: OFF-VOCABULARY: Rower; 6 stations do not divide EMOM 16
  `EMOM 16` · scheme: 6 stations × 4 rounds (with a 2-minute rotation remainder, the last 2 minutes are work only without additional rotation)
  - 8 Burpee
  - 6/arm Dumbbell Snatch @ 2×22.5 kg
  - 10 cal Rower
  - 10 Box Jump
  - 20 Air Squat
  - 6/arm Dumbbell Clean @ 2×22.5 kg


### Case 29 — EMOM 20 min · Kettlebell, Barbell, Pull-up Bar, Bodyweight, Rower

**gpt-oss-120b** — 56.6s · judge rank 1, score 7/10 · violations: OFF-VOCABULARY: Barbell Deadlift
  `EMOM 20` · scheme: 5 stations × 4 rounds
  - 20 Kettlebell Swing @ 24 kg
  - 8 Pull-up
  - 8 Barbell Deadlift @ 80 kg
  - 15 Air Squat
  - 10 cal Row

**gpt-oss-20b** — 22.0s · judge rank 2, score 6/10
  `EMOM 20` · scheme: 5 stations × 4 rounds
  - 15 Kettlebell Swing @ 24 kg
  - 8 Deadlift @ 60 kg
  - 6 Pull-up
  - 10 Burpee
  - 200 m Row

**llama-3.3-70b-instruct-fp8-fast** — 7.5s · judge rank 4, score 5/10
  `EMOM 20` · scheme: 4 stations × 5 rounds
  - 12 Kettlebell Swing @ 20 kg
  - 8 Deadlift @ 50 kg
  - 6 Pull-up
  - 10 Air Squat
  - 10 cal Row

**llama-4-scout-17b-16e-instruct** — 7.2s · judge rank 3, score 5/10 · violations: OFF-VOCABULARY: Rower
  `EMOM 20` · scheme: 5 rounds × 4 stations
  - 15 Kettlebell Swing @ 24 kg
  - 8 Deadlift @ 40 kg
  - 8 Pull-up
  - 10 cal Rower
  - 10 Burpee


### Case 30 — EMOM 9 min · Bodyweight, Running

**gpt-oss-120b** — 63.6s · judge rank 3, score 5/10
  `EMOM 9` · scheme: 3 stations × 3 rounds
  - 20 Sit-up
  - 50 m Bear Crawl
  - 100 m Run

**gpt-oss-20b** — 54.6s · judge rank 1, score 7/10
  `EMOM 9` · scheme: 3 stations × 3 rounds
  - 15 Sit-up
  - 12 Burpee
  - 100 m Run

**llama-3.3-70b-instruct-fp8-fast** — 6.9s · judge rank 2, score 5/10
  `EMOM 9` · scheme: 3 stations × 3 rounds
  - 12 Air Squat
  - 12 Sit-up
  - 100 m Run

**llama-4-scout-17b-16e-instruct** — 7.1s · judge rank 4, score 4/10 · violations: 4 stations do not divide EMOM 9
  `EMOM 9` · scheme: 4 stations × 2 rounds + 1
  - 8 Burpee
  - 100 m Run
  - 12 Sit-up
  - 10 Air Squat


### Case 31 — EMOM 14 min · Kettlebell, Dumbbells

**gpt-oss-120b** — 53.2s · judge rank 3, score 4/10 · violations: OFF-VOCABULARY: Kettlebell Goblet Squat
  `EMOM 14` · scheme: 7 stations × 2 rounds
  - 12 Kettlebell Swing @ 24 kg
  - 12 Kettlebell Goblet Squat @ 24 kg
  - 8 Kettlebell Clean @ 24 kg
  - 6/arm Dumbbell Snatch @ 22.5 kg
  - 10 Dumbbell Push Press @ 22.5 kg
  - 8 Dumbbell Thruster @ 22.5 kg
  - 6/leg Dumbbell Overhead Lunge @ 22.5 kg

**gpt-oss-20b** — 20.8s · judge rank 1, score 7/10
  `EMOM 14` · scheme: 2 stations × 7 rounds
  - 15 Kettlebell Swing @ 20 kg
  - 10 Dumbbell Hang Clean & Jerk @ 2×22.5 kg

**llama-3.3-70b-instruct-fp8-fast** — 7.1s · judge rank 2, score 6/10
  `EMOM 14` · scheme: 7 stations × 2 rounds
  - 12 Kettlebell Swing @ 20 kg
  - 9 Dumbbell Snatch @ 22.5 kg
  - 12 Goblet Squat @ 20 kg
  - 9 Dumbbell Hang Clean & Jerk @ 22.5 kg
  - 12 Kettlebell Clean @ 20 kg
  - 9 Dumbbell Thruster @ 22.5 kg
  - 12 Kettlebell Push Press @ 20 kg

**llama-4-scout-17b-16e-instruct** — 10.3s · judge rank 4, score 3/10 · violations: 4 stations do not divide EMOM 14
  `EMOM 14` · scheme: 4 stations × 3.5 rounds
  - 15 Kettlebell Swing @ 24 kg
  - 10/10 Dumbbell Snatch @ 2×22.5 kg
  - 8/8 Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 6/6 Kettlebell Push Press @ 24 kg


### Case 32 — EMOM 24 min · Bodyweight, Barbell, Assault Bike

**gpt-oss-120b** — 33.9s · judge rank 2, score 5/10
  `EMOM 24` · scheme: 3 stations × 8 rounds
  - 12 Front Squat @ 40 kg
  - 8 cal Assault Bike
  - 20 Push-up

**gpt-oss-20b** — 18.7s · judge rank 4, score 2/10 · violations: OFF-VOCABULARY: Back Squat
  `EMOM 24` · scheme: 3 stations × 8 rounds
  - 12 Back Squat @ 50 kg
  - 20 Push-up
  - 8 cal Assault Bike

**llama-3.3-70b-instruct-fp8-fast** — 7.6s · judge rank 1, score 7/10
  `EMOM 24` · scheme: 4 stations × 6 rounds
  - 15 Air Squat
  - 8 Push Press @ 30 kg
  - 12 Push-up
  - 8 cal Assault Bike

**llama-4-scout-17b-16e-instruct** — 10.8s · judge rank 3, score 3/10 · violations: EMOM cal minute too big: 10 cal Assault Bike; EMOM token minute: 6 Overhead Squat
  `EMOM 24` · scheme: 4 stations × 6 rounds
  - 6 Squat Clean @ 60 kg
  - 12 Push-up
  - 10 cal Assault Bike
  - 6 Overhead Squat @ 60 kg


### Case 33 — Chipper 15 min · Bodyweight, Kettlebell

**gpt-oss-120b** — 64.2s · judge rank 1, score 7/10
  `Chipper · cap 15 min`
  - 50 Sit-up
  - 45 Kettlebell Swing @ 24 kg
  - 35 Goblet Squat @ 24 kg
  - 30 Kettlebell Push Press @ 24 kg
  - 25 Burpee
  - 20 Kettlebell Clean @ 24 kg
  - 15 Kettlebell Snatch @ 24 kg

**gpt-oss-20b** — 82.0s · judge rank 4, score 3/10
  `Chipper · cap 15 min`
  - 50 Sit-up
  - 35 Kettlebell Push Press @ 40 kg
  - 30 Goblet Squat @ 40 kg
  - 25 Kettlebell Swing @ 40 kg
  - 20 Burpee
  - 15 Push-up
  - 10 Walking Lunge

**llama-3.3-70b-instruct-fp8-fast** — 7.0s · judge rank 2, score 4/10 · violations: OFF-VOCABULARY: Kettlebell Goblet Squat
  `Chipper · cap 18 min`
  - 30 Kettlebell Goblet Squat @ 24 kg
  - 20 Kettlebell Push Press @ 24 kg
  - 50 Sit-up
  - 15 Kettlebell Clean @ 24 kg
  - 12/leg Goblet Lunge @ 24 kg
  - 40 Burpee

**llama-4-scout-17b-16e-instruct** — 11.0s · judge rank 3, score 3/10 · violations: repeated base lift (squat): Goblet Squat + Air Squat; chipper ~7 min vs 15 target (too little)
  `Chipper · cap 18 min`
  - 12 Kettlebell Deadlift @ 24 kg
  - 15 Burpee
  - 10 Kettlebell Clean @ 24 kg
  - 12 Goblet Squat @ 24 kg
  - 20 Sit-up
  - 25 Kettlebell Swing @ 24 kg
  - 30 Air Squat


### Case 34 — Chipper 20 min · Bodyweight, Dumbbells, Pull-up Bar, Jump Rope

**gpt-oss-120b** — 86.6s · judge rank 2, score 5/10 · violations: chipper reps over ceiling: 120 Double-Under
  `Chipper · cap 20 min`
  - 120 Double-Under
  - 50 Air Squat
  - 25 Burpee
  - 20 Pull-up
  - 15 Toes-to-Bar
  - 12 Dumbbell Snatch @ 22.5 kg
  - 10 Dumbbell Deadlift @ 2×22.5 kg
  - 8 Dumbbell Clean @ 2×22.5 kg

**gpt-oss-20b** — 65.7s · judge rank 1, score 7/10
  `Chipper · cap 20 min`
  - 90 Double-Under
  - 48 Pull-up
  - 40 Dumbbell Hang Clean & Jerk @ 2×22.5 kg
  - 30 Air Squat
  - 25 Push-up
  - 20 Sit-up

**llama-3.3-70b-instruct-fp8-fast** — 9.4s · judge rank 4, score 2/10 · violations: repeated base lift (lunge): Dumbbell Front-Rack Lunge + Jumping Lunge; chipper reps over ceiling: 30/leg Dumbbell Front-Rack Lunge
  `Chipper · cap 23 min`
  - 30 Pull-up
  - 21 Dumbbell Clean @ 22.5 kg
  - 30/leg Dumbbell Front-Rack Lunge @ 22.5 kg
  - 50 Sit-up
  - 100 Single-Under
  - 30 Dumbbell Push Press @ 22.5 kg
  - 21 Burpee
  - 50 Jumping Lunge

**llama-4-scout-17b-16e-instruct** — 13.6s · judge rank 3, score 3/10 · violations: chipper ~6 min vs 20 target (too little)
  `Chipper · cap 23 min`
  - 10 Dumbbell Deadlift @ 2×22.5 kg
  - 8 Chest-to-Bar Pull-up
  - 12 Burpee
  - 40 Double-Under
  - 8 Dumbbell Clean @ 2×22.5 kg
  - 20 Air Squat
  - 12 Toes-to-Bar
  - 15 Sit-up


### Case 35 — Chipper 25 min · Barbell, Bodyweight, Rower, Wall Ball

**gpt-oss-120b** — 110.6s · judge rank 1, score 6/10 · violations: two barbell loads: [40.0, 70.0]
  `Chipper · cap 25 min`
  - 1000 m Row
  - 25/leg Walking Lunge
  - 50 Sit-up
  - 50 Air Squat
  - 50 Wall Ball @ 9 kg
  - 40 Deadlift @ 70 kg
  - 40 Push Press @ 40 kg
  - 30 Bar-Facing Burpee

**gpt-oss-20b** — 215.3s · judge rank 3, score 3/10 · violations: OFF-VOCABULARY: Barbell Thruster; OFF-VOCABULARY: Barbell Push Press; OFF-VOCABULARY: Barbell Deadlift; chipper reps over ceiling: 120 Burpee; chipper reps over ceiling: 80 Jumping Lunge
  `Chipper · cap 25 min`
  - 250m Row
  - 50 Wall Ball
  - 120 Burpee
  - 80 Jumping Lunge
  - 50 Barbell Thruster @ 30 kg
  - 50 Barbell Push Press @ 30 kg
  - 20 Barbell Deadlift @ 30 kg

**llama-3.3-70b-instruct-fp8-fast** — 8.0s · judge rank 2, score 5/10
  `Chipper · cap 28 min`
  - 50 Air Squat
  - 40 Push Press @ 40 kg
  - 30 Wall Ball @ 9 kg
  - 30 Deadlift @ 40 kg
  - 500 m Row
  - 30 Burpee
  - 20 Sit-up
  - 20 Thruster @ 40 kg

**llama-4-scout-17b-16e-instruct** — 14.4s · judge rank 4, score 2/10 · violations: duplicate movement: Row; duplicate movement: Wall Ball; chipper ~10 min vs 25 target (too little)
  `Chipper · cap 28 min`
  - 18 Deadlift @ 40 kg
  - 21 Burpee
  - 400 m Row
  - 12 Wall Ball @ 6 kg
  - 12 Overhead Squat @ 40 kg
  - 24 Push-up
  - 250 m Row
  - 9 Wall Ball @ 6 kg


### Case 36 — Chipper 35 min · Bodyweight, Barbell, Dumbbells, Kettlebell, Pull-up Bar, Rings, Rower, Jump Rope, Plyo Box

**gpt-oss-120b** — 161.7s · judge rank 2, score 4/10 · violations: chipper row over 1000 m: 2500 m; chipper reps over ceiling: 210 Air Squat
  `Chipper · cap 35 min`
  - 2500 m Row
  - 210 Air Squat
  - 100 Double-Under
  - 50 Kettlebell Swing @ 24 kg
  - 45 Pull-up
  - 40 Box Jump
  - 18/leg Front-Rack Lunge @ 30 kg
  - 30 Ring Row

**gpt-oss-20b** — 63.8s · judge rank 4, score 3/10 · violations: OFF-VOCABULARY: Plyo Box Jump; OFF-VOCABULARY: Rings Row; chipper ~13 min vs 35 target (too little)
  `Chipper · cap 35 min`
  - 250 m Row
  - 45 Pull-up
  - 40 Kettlebell Swing @ 20 kg
  - 35 Dumbbell Thruster @ 2×22.5 kg
  - 30 Double-Under
  - 25 Plyo Box Jump
  - 20 Rings Row

**llama-3.3-70b-instruct-fp8-fast** — 9.0s · judge rank 1, score 5/10
  `Chipper · cap 38 min`
  - 50 Jumping Lunge
  - 40 Pull-up
  - 30 Dumbbell Hang Clean & Jerk @ 20 kg
  - 30 Kettlebell Swing @ 20 kg
  - 25 Bar-Facing Burpee
  - 20 Ring Row
  - 1000 m Row
  - 100 Double-Under

**llama-4-scout-17b-16e-instruct** — 22.5s · judge rank 3, score 3/10 · violations: OFF-VOCABULARY: Rower; 9 movements (max 8); chipper reps over ceiling: 36/arm Dumbbell Snatch
  `Chipper · cap 38 min`
  - 18 Deadlift @ 60 kg
  - 18 Pull-up
  - 24 Ring Dip
  - 36/arm Dumbbell Snatch @ 22.5 kg
  - 50 Kettlebell Swing @ 16 kg
  - 12 Burpee
  - 500 m Rower
  - 90 Double-Under
  - 24 Box Jump


### Case 37 — Chipper 45 min · Bodyweight, Barbell, Kettlebell, Dumbbells, Pull-up Bar, Running

**gpt-oss-120b** — 117.0s · judge rank 1, score 6/10
  `Chipper · cap 45 min`
  - 800 m Run
  - 50 Kettlebell Swing @ 24 kg
  - 50 Deadlift @ 60 kg
  - 50 Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 50 Pull-up
  - 50 Hand-Release Push-up
  - 50 Front Squat @ 60 kg
  - 50 Burpee

**gpt-oss-20b** — 96.5s · judge rank 2, score 4/10 · violations: chipper ~22 min vs 45 target (too little)
  `Chipper · cap 45 min`
  - 800 m Run
  - 50 Air Squat
  - 50 Kettlebell Swing @ 20 kg
  - 50 Deadlift @ 50 kg
  - 50 Dumbbell Snatch @ 22.5 kg
  - 50 Pull-up

**llama-3.3-70b-instruct-fp8-fast** — 16.1s · judge rank 3, score 4/10 · violations: OFF-VOCABULARY: Kettlebell Goblet Squat; duplicate movement: Run; repeated base lift (squat): Air Squat + Kettlebell Goblet Squat; 9 movements (max 8); chipper reps over ceiling: 100 Air Squat; chipper reps over ceiling: 80 Deadlift; chipper reps over ceiling: 60 Kettlebell Swing; chipper run over 800 m: 1600 m
  `Chipper · cap 48 min`
  - 100 Air Squat
  - 80 Deadlift @ 60 kg
  - 60 Kettlebell Swing @ 24 kg
  - 50 Dumbbell Thruster @ 2×15 kg
  - 40 Pull-up
  - 800 m Run
  - 30 Burpee
  - 20 Kettlebell Goblet Squat @ 24 kg
  - 1600 m Run

**llama-4-scout-17b-16e-instruct** — 15.4s · judge rank 4, score 2/10 · violations: duplicate movement: Deadlift; duplicate movement: Kettlebell Swing; duplicate movement: Dumbbell Snatch; repeated base lift (deadlift): Deadlift + Deadlift; repeated base lift (swing): Kettlebell Swing + Kettlebell Swing; repeated base lift (snatch): Dumbbell Snatch + Dumbbell Snatch; 10 movements (max 8); chipper reps over ceiling: 40/leg Dumbbell Snatch
  `Chipper · cap 48 min`
  - 30 Deadlift @ 60 kg
  - 50 Kettlebell Swing @ 24 kg
  - 40/leg Dumbbell Snatch @ 22.5 kg
  - 20 Pull-up
  - 20 Burpee
  - 800 m Run
  - 20 Deadlift @ 60 kg
  - 30 Kettlebell Swing @ 24 kg
  - 20/leg Dumbbell Snatch @ 22.5 kg
  - 30 Air Squat


### Case 38 — Chipper 20 min · Sandbag, Bodyweight, GHD

**gpt-oss-120b** — 93.3s · judge rank 2, score 5/10
  `Chipper · cap 20 min`
  - 50 m Sandbag Carry @ 40 kg
  - 48 GHD Sit-up
  - 47 Bearhug Squat @ 40 kg
  - 42 Shoulder-to-Shoulder Press @ 40 kg
  - 38 Sandbag Clean @ 40 kg
  - 33 Sandbag Lunge @ 40 kg
  - 28 Burpee
  - 20 Broad Jump

**gpt-oss-20b** — 86.0s · judge rank 1, score 6/10 · violations: repeated base lift (lunge): Sandbag Lunge + Jumping Lunge
  `Chipper · cap 20 min`
  - 50 GHD Sit-up
  - 50 m Sandbag Carry @ 40 kg
  - 50 Sandbag Clean @ 40 kg
  - 50 Shoulder-to-Shoulder Press @ 40 kg
  - 50 Sandbag Lunge @ 40 kg
  - 40 Jumping Lunge

**llama-3.3-70b-instruct-fp8-fast** — 4.3s · judge rank 4, score 3/10
  `Chipper · cap 23 min`
  - 50 GHD Sit-up
  - 30 Sandbag Carry @ 40 kg
  - 20 Bear Crawl
  - 20 Burpee
  - 15 Sandbag Clean @ 40 kg
  - 10 Jumping Lunge

**llama-4-scout-17b-16e-instruct** — 11.9s · judge rank 3, score 4/10
  `Chipper · cap 20 min`
  - 18 Burpee
  - 24/leg Walking Lunge
  - 15 Sandbag Clean @ 40 kg
  - 50 GHD Sit-up
  - 21 Hand-Release Push-up
  - 50 m Sandbag Carry @ 40 kg


### Case 39 — Intervals 12 min · Bodyweight, Kettlebell

**gpt-oss-120b** — 50.4s · judge rank 2, score 7/10
  `3 × 3 min on / 1 min rest`
  - 20 Kettlebell Swing @ 24 kg
  - 10 Push-up
  - 8 Kettlebell Deadlift @ 24 kg
  - 15 Sit-up

**gpt-oss-20b** — 46.3s · judge rank 3, score 5/10 · violations: interval work ~3.5 min overflows 3 min window
  `3 × 3 min on / 1 min rest`
  - 25 Kettlebell Swing @ 24 kg
  - 15 Burpee
  - 10 Push-up
  - 10 Sit-up

**llama-3.3-70b-instruct-fp8-fast** — 7.5s · judge rank 4, score 4/10
  `3 × 3 min on / 1 min rest`
  - 18 Kettlebell Swing @ 24 kg
  - 9 Air Squat
  - 9 Sit-up
  - *notes: Maintain a sprint pace throughout the 3-minute windows*

**llama-4-scout-17b-16e-instruct** — 8.2s · judge rank 1, score 8/10
  `4 × 2 min on / 1 min rest`
  - 20 Kettlebell Swing @ 24 kg
  - 8 Burpee


### Case 40 — Intervals 20 min · Barbell, Bodyweight, Rower

**gpt-oss-120b** — 19.8s · judge rank 1, score 6/10
  `5 × 3 min on / 1 min rest`
  - 250 m Row
  - 12 Push Press @ 30 kg
  - 12 Push-up

**gpt-oss-20b** — 47.1s · judge rank 3, score 3/10 · violations: OFF-VOCABULARY: Barbell Push Press; OFF-VOCABULARY: Bodyweight Push-up; OFF-VOCABULARY: Rower; OFF-VOCABULARY: Bodyweight Sit-up; interval work ~5.3 min overflows 4 min window
  `4 × 4 min on / 1 min rest`
  - 30 Barbell Push Press @ 35 kg
  - 40 Bodyweight Push-up
  - 200 m Rower
  - 20 Bodyweight Sit-up

**llama-3.3-70b-instruct-fp8-fast** — 5.9s · judge rank 2, score 4/10 · violations: interval work ~5.4 min overflows 4 min window
  `4 × 4 min on / 1 min rest` · scheme: same work every interval
  - 21 Push Press @ 40 kg
  - 40 Push-up
  - 150 m Row
  - 21 Burpee
  - *notes: sprint pace, aim for fastest row of the day*

**llama-4-scout-17b-16e-instruct** — 10.1s · judge rank 4, score 3/10 · violations: OFF-VOCABULARY: Rower; intervals span 25 min vs target 20; interval work ~2.1 min underfills 4 min window
  `5 × 4 min on / 1 min rest`
  - 8 Push Press @ 40 kg
  - 10 Burpee
  - 200 m Rower


### Case 41 — Intervals 24 min · Dumbbells, Ski Erg, Bodyweight

**gpt-oss-120b** — 74.2s · judge rank 1, score 7/10
  `6 × 3 min on / 1 min rest`
  - 6 Dumbbell Deadlift @ 2×22.5 kg
  - 10 cal Ski Erg
  - 6/leg Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 6 Burpee

**gpt-oss-20b** — 64.4s · judge rank 4, score 2/10 · violations: OFF-VOCABULARY: Dumbbell Alternating Lunge; interval work ~6.5 min overflows 5 min window
  `4 × 5 min on / 1 min rest`
  - 8 Burpee
  - 20/leg Dumbbell Alternating Lunge @ 2×22.5 kg
  - 600 m Ski Erg

**llama-3.3-70b-instruct-fp8-fast** — 6.8s · judge rank 2, score 4/10
  `6 × 3 min on / 1 min rest`
  - 9/leg Dumbbell Front-Rack Lunge @ 22.5 kg
  - 15 Air Squat
  - 50 m Ski Erg

**llama-4-scout-17b-16e-instruct** — 11.8s · judge rank 3, score 3/10
  `5 × 4 min on / 1 min rest`
  - 10 Burpee
  - 15 Dumbbell Deadlift @ 2×22.5 kg
  - 20 cal Ski Erg


### Case 42 — Intervals 30 min · Bodyweight, Running, Pull-up Bar

**gpt-oss-120b** — 26.6s · judge rank 1, score 8/10
  `6 × 4 min on / 1 min rest`
  - 200 m Run
  - 40 Air Squat
  - 12 Pull-up

**gpt-oss-20b** — 35.4s · judge rank 2, score 5/10
  `10 × 2 min on / 1 min rest`
  - 200 m Run
  - 10 Air Squat
  - 3 Pull-up

**llama-3.3-70b-instruct-fp8-fast** — 6.7s · judge rank 3, score 5/10
  `7 × 3 min on / 1 min rest`
  - 15 Air Squat
  - 10 Pull-up
  - 200 m Run

**llama-4-scout-17b-16e-instruct** — 11.3s · judge rank 4, score 3/10 · violations: interval work ~3.5 min overflows 3 min window
  `8 × 3 min on / 1 min rest`
  - 20 Air Squat
  - 150 m Run
  - 6 Pull-up
  - 12/leg Jumping Lunge


### Case 43 — Intervals 16 min · Assault Bike, Wall Ball, Bodyweight

**gpt-oss-120b** — 58.6s · judge rank 2, score 4/10 · violations: interval work ~4.1 min overflows 3 min window
  `4 × 3 min on / 1 min rest`
  - 8 cal Assault Bike
  - 20 Wall Ball @ 9 kg
  - 30 Air Squat

**gpt-oss-20b** — 60.7s · judge rank 1, score 6/10 · violations: interval work ~3.2 min overflows 3 min window
  `4 × 3 min on / 1 min rest`
  - 15 Air Squat
  - 10 Push-up
  - 10 Wall Ball @ 6 kg
  - 10 cal Assault Bike

**llama-3.3-70b-instruct-fp8-fast** — 5.7s · judge rank 4, score 2/10 · violations: interval format_line unparseable: 8 × 1.5 min on / 0.5 min rest
  `8 × 1.5 min on / 0.5 min rest`
  - 20 Air Squat
  - 15 Wall Ball @ 9 kg
  - 10 cal Assault Bike

**llama-4-scout-17b-16e-instruct** — 8.1s · judge rank 3, score 3/10 · violations: interval work ~4.7 min overflows 3 min window
  `4 × 3 min on / 1 min rest`
  - 20 Air Squat
  - 15 cal Assault Bike
  - 15 Wall Ball @ 6 kg
  - 8 Burpee


### Case 44 — AMRAP 15 min · Bodyweight, Barbell, Dumbbells
*Athlete request:* `bad knee - nothing that loads a deep bend`

**gpt-oss-120b** — 60.4s · judge rank 1, score 8/10
  `AMRAP 15 min`
  - 12 Push-up
  - 8 Deadlift @ 40 kg
  - 6/arm Dumbbell Snatch @ 22.5 kg
  - 8 Push Press @ 40 kg
  - 8 Burpee

**gpt-oss-20b** — 15.2s · judge rank 2, score 6/10
  `AMRAP 15 min`
  - 20 Push-up
  - 10 Deadlift @ 60 kg
  - 20 Dumbbell Snatch @ 22.5 kg

**llama-3.3-70b-instruct-fp8-fast** — 4.3s · judge rank 3, score 5/10 · violations: OFF-VOCABULARY: Barbell Hang Power Clean
  `AMRAP 15 min`
  - 12 Push-up
  - 9 Dumbbell Push Press @ 15 kg
  - 12 Barbell Hang Power Clean @ 30 kg
  - 15 Burpee

**llama-4-scout-17b-16e-instruct** — 12.9s · judge rank 4, score 2/10 · violations: repeated base lift (press): Push Press + Dumbbell Push Press
  `AMRAP 15 min`
  - 10 Burpee
  - 8 Power Clean @ 40 kg
  - 12 Dumbbell Hang Clean & Jerk @ 2×22.5 kg
  - 20 Air Squat
  - 10 Push Press @ 40 kg
  - 12 Dumbbell Push Press @ 2×22.5 kg


### Case 45 — For Time 12 min · Bodyweight, Kettlebell
*Athlete request:* `easy recovery day please`

**gpt-oss-120b** — 35.1s · judge rank 1, score 7/10
  `For Time · cap 15 min` · scheme: 8 Rounds
  - 6 Goblet Squat @ 16 kg
  - 6 Kettlebell Swing @ 16 kg
  - 8 Walking Lunge
  - 8 Sit-up

**gpt-oss-20b** — 18.1s · judge rank 4, score 2/10 · violations: OFF-VOCABULARY: Kettlebell Goblet Squat
  `For Time · cap 15 min` · scheme: 5 Rounds
  - 14 Kettlebell Goblet Squat @ 32 kg
  - 14 Kettlebell Swing @ 32 kg
  - 8 Burpee

**llama-3.3-70b-instruct-fp8-fast** — 7.0s · judge rank 2, score 6/10
  `For Time · cap 15 min` · scheme: 3 Rounds
  - 9 Goblet Squat @ 20 kg
  - 12 Push-up
  - 9 Kettlebell Swing @ 20 kg
  - 12 Sit-up

**llama-4-scout-17b-16e-instruct** — 9.4s · judge rank 3, score 5/10
  `For Time · cap 15 min` · scheme: 4 Rounds
  - 8 Kettlebell Deadlift @ 24 kg
  - 12/leg Reverse Lunge
  - 6 Goblet Squat @ 24 kg
  - 15 Sit-up
  - 12 Kettlebell Swing @ 24 kg


### Case 46 — EMOM 12 min · Bodyweight, Dumbbells
*Athlete request:* `I want devil press in there`

**gpt-oss-120b** — 39.4s · judge rank 2, score 5/10
  `EMOM 12` · scheme: 3 stations × 4 rounds
  - 6 Devil Press @ 22.5 kg
  - 4 Dumbbell Hang Clean & Jerk @ 22.5 kg
  - 5 Dumbbell Snatch @ 22.5 kg

**gpt-oss-20b** — 58.1s · judge rank 3, score 4/10
  `EMOM 12` · scheme: 3 stations × 4 rounds
  - 5 Dumbbell Deadlift @ 2×22.5 kg
  - 5 Dumbbell Clean @ 22.5 kg
  - 10 Devil Press

**llama-3.3-70b-instruct-fp8-fast** — 4.8s · judge rank 1, score 7/10
  `EMOM 12` · scheme: 4 stations × 3 rounds
  - 6 Devil Press @ 2×22.5 kg
  - 9 Dumbbell Front-Rack Lunge @ 2×22.5 kg
  - 12 Sit-up
  - 9 Dumbbell Hang Clean & Jerk @ 2×22.5 kg

**llama-4-scout-17b-16e-instruct** — 10.0s · judge rank 4, score 0/10
  - GENERATION FAILED: The model kept using equipment the athlete does not have: Ring Row


### Case 47 — Chipper 25 min · Bodyweight, Kettlebell, Pull-up Bar
*Athlete request:* `use the rower a lot`

**gpt-oss-120b** — 87.9s · judge rank 3, score 2/10 · violations: OFF-VOCABULARY: Kettlebell Sumo Deadlift High Pull; chipper reps over ceiling: 120 Kettlebell Swing; chipper reps over ceiling: 100 Kettlebell Deadlift; chipper reps over ceiling: 80 Hand-Release Push-up
  `Chipper · cap 25 min`
  - 120 Kettlebell Swing @ 24 kg
  - 45 Pull-up
  - 100 Kettlebell Deadlift @ 24 kg
  - 45 Kettlebell Sumo Deadlift High Pull @ 24 kg
  - 80 Hand-Release Push-up
  - 45 Hanging Knee Raise
  - 6 Turkish Get-Up @ 24 kg
  - *notes: steady pace, no rest*

**gpt-oss-20b** — 77.9s · judge rank 1, score 4/10 · violations: OFF-VOCABULARY: Kettlebell Front-Rack Lunge
  `Chipper · cap 25 min`
  - 50 Pull-up
  - 50 Kettlebell Swing @ 20 kg
  - 50 Kettlebell Clean @ 20 kg
  - 35 Kettlebell Snatch @ 20 kg
  - 35 Air Squat
  - 12/leg Kettlebell Front-Rack Lunge @ 20 kg
  - 35 Hand-Release Push-up
  - 30 Kettlebell Deadlift @ 20 kg

**llama-3.3-70b-instruct-fp8-fast** — 9.9s · judge rank 2, score 3/10 · violations: repeated base lift (squat): Air Squat + Goblet Squat; chipper reps over ceiling: 100 Pull-up; chipper reps over ceiling: 80 Kettlebell Swing; chipper reps over ceiling: 60 Sit-up
  `Chipper · cap 28 min`
  - 100 Pull-up
  - 80 Kettlebell Swing @ 20 kg
  - 60 Sit-up
  - 40 Kettlebell Clean @ 20 kg
  - 30 Air Squat
  - 20 Goblet Squat @ 20 kg

**llama-4-scout-17b-16e-instruct** — 16.9s · judge rank 4, score 0/10
  - GENERATION FAILED: The model kept using equipment the athlete does not have: Row, Row, Row


### Case 48 — Intervals 18 min · Bodyweight
*Athlete request:* `no jumping, downstairs neighbours`

**gpt-oss-120b** — 39.2s · judge rank 1, score 7/10
  `6 × 2 min on / 1 min rest`
  - 10 Air Squat
  - 4/leg Reverse Lunge
  - 6 Push-up
  - 25 m Bear Crawl

**gpt-oss-20b** — 30.7s · judge rank 3, score 4/10 · violations: interval work ~3.2 min overflows 3 min window
  `4 × 3 min on / 2 min rest`
  - 25 Air Squat
  - 12/leg Walking Lunge
  - 15 Hand-Release Push-up

**llama-3.3-70b-instruct-fp8-fast** — 5.5s · judge rank 4, score 3/10 · violations: repeated base lift (lunge): Walking Lunge + Reverse Lunge; interval work ~6.2 min overflows 4 min window
  `3 × 4 min on / 2 min rest`
  - 40 Air Squat
  - 30 Sit-up
  - 20 Push-up
  - 20 Walking Lunge
  - 15 Reverse Lunge
  - *notes: Pace for lung burn, not muscle failure*

**llama-4-scout-17b-16e-instruct** — 6.4s · judge rank 2, score 5/10 · violations: interval work ~4.8 min overflows 4 min window
  `3 × 4 min on / 2 min rest`
  - 25 Air Squat
  - 15/leg Walking Lunge
  - 20 Sit-up
  - 20 Push-up


### Case 49 — AMRAP 12 min · Kettlebell, Bodyweight
*Avoid:* Kettlebell Swing, Goblet Squat, Burpee, Push-up, Sit-up

**gpt-oss-120b** — 28.6s · judge rank 2, score 5/10
  `AMRAP 12 min`
  - 30 Air Squat
  - 12 Kettlebell Clean @ 20 kg
  - 20 Kettlebell Deadlift @ 20 kg

**gpt-oss-20b** — 21.7s · judge rank 4, score 3/10
  `AMRAP 12 min`
  - 18 Air Squat
  - 10 Hand-Release Push-up
  - 6 Kettlebell Clean @ 50 kg

**llama-3.3-70b-instruct-fp8-fast** — 6.6s · judge rank 1, score 6/10
  `AMRAP 12 min`
  - 18 Air Squat
  - 12 Kettlebell Clean @ 20 kg
  - 12 Kettlebell Snatch @ 20 kg
  - 12/leg Reverse Lunge

**llama-4-scout-17b-16e-instruct** — 12.6s · judge rank 3, score 4/10 · violations: AMRAP round ~6 min (want 2-4)
  `AMRAP 12 min`
  - 40 Air Squat
  - 25 Kettlebell Clean @ 24 kg
  - 20/leg Reverse Lunge


### Case 50 — For Time 15 min · Bodyweight, Barbell, Pull-up Bar
*Avoid:* Deadlift, Pull-up, Thruster, Push-up, Air Squat, Run

**gpt-oss-120b** — 35.5s · judge rank 4, score 4/10
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 40 Sit-up
  - 12 Front Squat @ 40 kg
  - 9 Power Clean @ 40 kg
  - 10 Bar-Facing Burpee

**gpt-oss-20b** — 34.6s · judge rank 3, score 6/10
  `For Time · cap 18 min` · scheme: 5 Rounds
  - 8 Front Squat @ 60 kg
  - 6 Chin-up
  - 12 Hand-Release Push-up
  - 18 Hanging Knee Raise

**llama-3.3-70b-instruct-fp8-fast** — 4.0s · judge rank 1, score 8/10
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 12 Front Squat @ 40 kg
  - 12 Bar-Facing Burpee
  - 30 Sit-up
  - 9 Clean & Jerk @ 40 kg
  - 9 Toes-to-Bar

**llama-4-scout-17b-16e-instruct** — 12.3s · judge rank 2, score 7/10
  `For Time · cap 18 min` · scheme: 3 Rounds
  - 9 Hang Power Clean @ 40 kg
  - 8/leg Front-Rack Lunge @ 40 kg
  - 6 Chest-to-Bar Pull-up
  - 12 Sit-up
  - 6 Overhead Squat @ 40 kg
  - 9 Bar-Facing Burpee

