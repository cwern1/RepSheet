# Prompt-robustness ideas — from 69 low-effort generations

Basis: the 49 low-effort runs from [`effort-comparison.md`](effort-comparison.md)
plus 20 fresh production runs (2026-08-24, after the switch to `effort: "low"`)
over the 20 historically hardest cases — raw data in
[`prod_low_results.jsonl`](prod_low_results.jsonl). The prod sample: 20/20
succeeded, median 19.1 s, 11/20 fully clean. Every idea below is anchored to a
failure that actually happened; per CLAUDE.md the bias is **narrow added rules,
not section rewrites**, and every change should be judged by re-running
`harness/` (one 50-case pass ≈ $0.25).

## Failure taxonomy, ranked by frequency × severity

### 1. Implement-prefixed and implement-swapped names (top off-vocab source)
Observed: "Barbell Deadlift", "Barbell Front Rack Lunge" (case 7), "Kettlebell
Overhead Lunge" (33), "Kettlebell Lunge" (49), bare "Swing" (36). The model
composes implement+lift freely; the vocabulary's no-invented-variants rule bans
new *movements* but doesn't clearly ban renaming its *own* movement.

- **Prompt idea:** one line in MOVEMENT VOCABULARY: *"Never prepend an implement
  to a name — the list is already implement-specific: write `Deadlift`, never
  `Barbell Deadlift`; the kettlebell lunge IS `Goblet Lunge`."*
- **Code idea (bigger win):** canonicalize before validating — strip a leading
  listed-implement word when the remainder is a vocab name, and alias-map the
  obvious cases ("Swing"→"Kettlebell Swing"). Turns a whole failure class into
  a non-event without touching model behavior.

### 2. Chipper volume and ceilings (worst style, both efforts)
Observed: 300 Double-Unders, 1800 m row, 10 movements, 120-rep sets, broken
descent (36); ascending tail (37); 240 reps under a 15-min cap (33). The
ceilings exist in prose but get skipped exactly when the model juggles many
items.

- **Prompt idea:** give Chipper what fixed For Time — a **worked example**:
  *"35 min, 8 items → e.g. 50-40-35-30-25-20-15-12 across 8 movements ≈ 227
  reps ≈ 15/min — no set above 50, row ≤ 1000 m, jump rope ≤ 100."*
- **Prompt idea:** an explicit pre-flight check: *"Before answering, check
  EVERY chipper line against the ceilings; if a count exceeds its ceiling, add
  a movement instead of a bigger set."*
- **Code idea:** the validator already catches these; chippers often burn the
  single corrective retry on 4–5 stacked problems. Cap the feedback to the 3
  worst problems so the retry is focused.

### 3. Machine calories overflow interval windows
Observed: 20 cal Ski Erg + lifts in a 3-min window (41), 20 cal Assault Bike +
50 reps (43); interval-window overflow was the #1 low-effort validator hit
(5 of 21 violations). The 2/3-rate rule exists but is arithmetic the model
skips; the EMOM blueprint's hard numeric caps ("Row ≤ 10 cal, Assault Bike
≤ 8") worked — EMOMs were mostly legal.

- **Prompt idea:** replicate the EMOM pattern inside Intervals: *"In an
  interval window shared with other movements, a machine gets at most 10 cal
  (Assault Bike 8) — and alone at most half the window."*

### 4. Balance rule beats equipment rule on machines-only lists
Observed: EMOM 30 with 4 machines grew `Overhead Squat`/`Front Squat` @ 40 kg —
no barbell listed (case 2, survived to the user because `_impossible_movements`
has no marker for those names). The monostructural exemption exists but reads
as optional.

- **Prompt idea:** make it imperative: *"A machines-only list IS a
  monostructural workout: machines are the only movements. Never add lifts to
  'balance' it."*
- **Code idea (highest-leverage validator fix):** the vocabulary is closed, so
  replace the heuristic `_IMPLEMENT_MARKERS` with a complete reverse index —
  every vocab name → its implement(s). `Front Squat` with no barbell then
  triggers the corrective retry / 502 instead of shipping.

### 5. AMRAP round-length drift
Observed: rounds of ~4.5–6 min with big equipment lists (6, 10, 49), ~1.6 min
with tiny ones (8, 12). The validator only flags rounds > 6 min, so 5-minute
rounds pass silently.

- **Code idea:** tighten `_quality_problems` AMRAP bounds to flag > ~4.5 min
  (270 s) and < ~1.8 min, so the retry actually fires on these.
- **Prompt idea:** *"5+ movements almost always exceeds a 4-minute round —
  3–5 movements is the AMRAP sweet spot."*

### 6. Small format slop (each cheap to close)
- Intervals `scheme` junk ("4 stations × 6 rounds", case 41) — the AMRAP
  blueprint says `scheme` must be null; the Intervals blueprint never does.
  Add: *"Intervals: `scheme` must be null."*
- `notes` restating the rest scheme already in `format_line` (case 9) —
  validator could flag notes containing "rest" when format_line has it.
- Sub-5-rep tokens (3 Burpee, case 39) — the ≥5-rep floor exists in prose;
  add a generic validator check (reps < 5 and not heavy-barbell → problem).
- Both seasoning movements at once (Broad Jump AND Bear Crawl, case 1) —
  trivial validator check.
- Two-handed dumbbell moves with a single-bell load ("22.5 kg" on a Front-Rack
  Lunge, case 4) — could be normalized in code to "2×22.5 kg".

### 7. "Easy day" shrinks the workout instead of the load
Observed once (case 45: ~7 min of work for a 12-min target at otherwise-honest
loads). The rule exists ("easy means lighter, never shorter"); low frequency —
watch, don't fix yet.

## Suggested order of attack

| step | change | risk | expected effect |
|---|---|---|---|
| 1 | Complete reverse-index `_impossible_movements` + name canonicalization (code only) | none to prompt behavior | kills taxonomy #1 and #4 leaks entirely |
| 2 | Intervals machine-cal cap + `scheme: null` (2 prompt lines) | low | biggest validator-hit class |
| 3 | Chipper worked example + pre-flight ceilings line | medium (touches the worst style) | chipper clean-rate up |
| 4 | Tighten AMRAP validator bounds (code) | low | retry fires on 5-min rounds |
| 5 | No-implement-prefix line (prompt) | low | halves off-vocab hits |

Each step: run `harness/run_experiment.py` (or the 20-case prod subset in
`prod_low_results.jsonl`'s PICK list), `analyze.py`, and blind-judge before/after
per `harness/judge_prep.py` — one sample proves nothing.
