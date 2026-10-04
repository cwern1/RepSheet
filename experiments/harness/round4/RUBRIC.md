# Round 4 judging rubric

You are judging workouts for Repsheet, an app that generates one CrossFit-style
workout for a **fit amateur** from the athlete's picked equipment, style and
duration. Judge each candidate as an experienced CrossFit coach would.

Candidates may have been generated under different prompts. Judge every one
against **this rubric only**: not the wording of any prompt in the repo, and
not whether a movement name appears in some fixed list.

## Hard requirements: a breach caps the score at 4

1. **Equipment.** Only equipment from the athlete's list. With up to 7 items,
   every item is used. With more than 7, at least 7 are used. "Bodyweight" and
   "Running" count as items: listed means used; not listed means absent.
2. **Physically possible.** There is no rack and no bench. Bodyweight-only means
   nothing to hang from.
3. **Fit for a fit amateur.** No muscle-ups, handstand work, pistols or max lifts.
   Loads are realistic in kg, and each implement uses one load for the whole
   workout.
4. **The requested style:**
   - AMRAP: one repeated round.
   - For Time: fixed work with a cap.
   - EMOM: a rotation that divides the minutes.
   - Chipper: one descending list done once.
   - Intervals: explicit work/rest that spans the target duration.
5. **The duration is honest.** The prescribed work actually takes about the target time.
6. **The athlete request and avoid list are honoured.** Restrictions extend to
   close variants. A request that contradicts the equipment is ignored silently.

## Coaching quality: this decides the score above the cap

- **Clear stimulus.** It's obvious what the workout is meant to feel like, and
  there's one main limiter.
- **Smart movement choice.** Classic couplets and triplets where possible,
  pairings that create pacing decisions, no pointless or token stations.
- **Balance.** No redundant movements (the same lift twice), and no all-arms or
  all-legs workouts unless the workout is deliberately monostructural.
- **Sensible reps and loads.** Sets an amateur can manage, a time cap that fits.
- **Notes.** If there's a note, it helps the athlete (pacing, what will bite)
  rather than restating the format.
- **Interesting but correct.** Reward variety and creativity only when it's
  also good programming. A standard, well-known movement is fine even if it's
  less common.

## Output

Score each candidate 0–10 (a failed generation scores 0). Rank the candidates
1..N with no ties, where 1 is best. Each note is 15 words or fewer.
