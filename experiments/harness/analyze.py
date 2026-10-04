"""Deterministic quality analysis of model-comparison results.

Replicates the pure checks from src/generator.py (which cannot be imported on
the host) plus a strict movement-vocabulary check, and prints per-model stats.
Writes analysis.json with per-run violation details for the report.
"""
import json
import re
import statistics
import sys
from collections import defaultdict

IN = sys.argv[1] if len(sys.argv) > 1 else "results.jsonl"

VOCAB = {
    "Bodyweight": ["Burpee", "Push-up", "Hand-Release Push-up", "Air Squat",
                   "Walking Lunge", "Reverse Lunge", "Jumping Lunge", "Sit-up",
                   "Broad Jump", "Bear Crawl"],
    "Barbell": ["Deadlift", "Sumo Deadlift High Pull", "Power Clean",
                "Hang Power Clean", "Squat Clean", "Clean & Jerk",
                "Power Snatch", "Overhead Squat", "Front Squat", "Push Press",
                "Push Jerk", "Thruster", "Front-Rack Lunge", "Overhead Lunge",
                "Bar-Facing Burpee"],
    "Dumbbells": ["Dumbbell Snatch", "Dumbbell Clean",
                  "Dumbbell Hang Clean & Jerk", "Dumbbell Push Press",
                  "Dumbbell Thruster", "Dumbbell Front-Rack Lunge",
                  "Dumbbell Overhead Lunge", "Devil Press", "Dumbbell Deadlift",
                  "Dumbbell Box Step-Up", "Farmers Carry"],
    "Kettlebell": ["Kettlebell Swing", "Goblet Squat", "Kettlebell Clean",
                   "Kettlebell Snatch", "Kettlebell Push Press", "Goblet Lunge",
                   "Kettlebell Deadlift", "Turkish Get-Up"],
    "Pull-up Bar": ["Pull-up", "Chest-to-Bar Pull-up", "Chin-up",
                    "Toes-to-Bar", "Hanging Knee Raise", "Burpee Pull-up"],
    "Rings": ["Ring Row", "Ring Dip", "Ring Push-up"],
    "Rower": ["Row"], "Bike Erg": ["Bike Erg"], "Ski Erg": ["Ski Erg"],
    "Assault Bike": ["Assault Bike"],
    "Jump Rope": ["Single-Under", "Double-Under"],
    "Plyo Box": ["Box Jump", "Box Jump-Over", "Box Step-Up",
                 "Burpee Box Jump-Over"],
    "Wall Ball": ["Wall Ball", "Wall-Ball Sit-up"],
    "Sandbag": ["Sandbag Clean", "Bearhug Squat", "Sandbag Lunge",
                "Shoulder-to-Shoulder Press", "Sandbag Carry"],
    "Running": ["Run"], "GHD": ["GHD Sit-up", "Hip Extension"],
}
ALLOWED = {n.lower() for names in VOCAB.values() for n in names} | {"rest"}

# ---- pure checks copied from src/generator.py ----

_IMPLEMENT_MARKERS = (
    ("Pull-up Bar", ("pull-up", "pullup", "chin-up", "chinup", "toes-to-bar",
                     "hanging", "muscle-up")),
    ("Rings", ("ring dip", "ring row", "ring push", "ring muscle")),
    ("Kettlebell", ("kettlebell", "goblet", "swing")),
    ("Jump Rope", ("double-under", "single-under", "jump rope")),
    ("Plyo Box", ("box jump", "box step", "step-up")),
    ("Wall Ball", ("wall ball", "wall-ball")),
    ("GHD", ("ghd", "hip extension")),
    ("Barbell", ("barbell", "bar-facing")),
    ("Dumbbells", ("dumbbell", "devil press")),
    ("Sandbag", ("sandbag", "bearhug")),
    ("Assault Bike", ("assault bike",)),
    ("Ski Erg", ("ski erg",)),
    ("Bike Erg", ("bike erg",)),
)
_EXACT_NAMES = {"row": "Rower", "rower": "Rower", "calorie row": "Rower",
                "run": "Running", "running": "Running"}
_GRUNT_MARKERS = (
    "burpee", "snatch", "clean", "deadlift", "get-up", "ghd", "pull-up",
    "chin-up", "muscle", "dip", "toes-to-bar", "knee raise", "wall ball",
    "thruster", "box jump", "broad jump", "devil",
)
_LOADED_GRUNT_MARKERS = ("lunge", "step-up")
_BASE_LIFT_SUFFIXES = (
    "clean", "snatch", "deadlift", "squat", "press", "lunge", "swing",
    "carry", "push-up", "sit-up", "pull-up", "burpee",
)


def _parse_reps(reps):
    r = reps.strip().lower()
    if re.fullmatch(r"\d+(?:-\d+)+", r):
        return float(sum(int(x) for x in r.split("-"))), "rep"
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*(cal|m|min)?\s*(/\s*(?:leg|arm|side))?", r)
    if not m:
        return None
    n = float(m.group(1)) * (2 if m.group(3) else 1)
    return n, (m.group(2) or "rep")


def _movement_seconds(m):
    parsed = _parse_reps(m["reps"])
    if parsed is None:
        return None
    n, unit = parsed
    name = m["name"].lower()
    if unit == "min":
        return n * 60
    if unit == "cal":
        return n * (7.0 if "assault" in name else 4.5)
    if unit == "m":
        if "run" in name:
            return n * 0.3
        if "row" in name or "erg" in name:
            return n * 0.25
        return n * 1.2
    if "under" in name or "jump rope" in name:
        return n * 0.8
    if any(k in name for k in _GRUNT_MARKERS) or (
        m.get("load_kg") and any(k in name for k in _LOADED_GRUNT_MARKERS)
    ):
        return n * 5.0
    return n * 3.0


def _scheme_rounds(scheme):
    if scheme and (m := re.search(r"(\d+)\s*round", scheme.lower())):
        return int(m.group(1))
    return 1


def _missing_equipment(w, equipment):
    used = {e.lower() for m in w["movements"] for e in m["equipment"]}
    used |= {e.lower() for e in w.get("equipment_used") or []}
    return [e for e in equipment if e.lower() not in used]


def _coverage_gap(w, equipment):
    missing = _missing_equipment(w, equipment)
    if len(equipment) > 7 and len(missing) <= len(equipment) - 7:
        return []
    return missing


def _impossible_movements(w, equipment):
    have = {e.lower() for e in equipment}
    bad = []
    for m in w["movements"]:
        name = m["name"].lower().strip()
        needed = _EXACT_NAMES.get(name)
        if needed is None:
            for item, markers in _IMPLEMENT_MARKERS:
                if any(marker in name for marker in markers):
                    needed = item
                    break
        if needed and needed.lower() not in have:
            bad.append(m["name"])
    return bad


def _quality_problems(w, style, duration_min, avoid):
    problems = []
    movements = w["movements"]
    names = [m["name"] for m in movements]
    lower = [n.lower().strip() for n in names]
    rounds = _scheme_rounds(w.get("scheme"))

    seen = {}
    for name, low in zip(names, lower):
        if low in seen:
            problems.append(f"duplicate movement: {name}")
        seen[low] = name
    suffix_seen = {}
    for name, low in zip(names, lower):
        tail = low.split()[-1] if low.split() else ""
        if tail in _BASE_LIFT_SUFFIXES:
            if tail in suffix_seen and suffix_seen[tail] != low:
                problems.append(f"repeated base lift ({tail}): {suffix_seen[tail]} + {name}")
            suffix_seen.setdefault(tail, name)

    if len(movements) > 8:
        problems.append(f"{len(movements)} movements (max 8)")

    by_implement = {}
    for m in movements:
        if not m.get("load_kg"):
            continue
        nums = re.findall(r"\d+(?:\.\d+)?", m["load_kg"])
        if not nums:
            continue
        for item in m["equipment"]:
            by_implement.setdefault(item.lower(), set()).add(float(nums[-1]))
    for item, loads in by_implement.items():
        if len(loads) > 1:
            problems.append(f"two {item} loads: {sorted(loads)}")

    hits = []
    for a in avoid:
        al = a.lower().strip()
        if al and any(al in low or low in al for low in lower):
            hits.append(a)
    if len(hits) >= 2:
        problems.append(f"avoid-list ignored: {hits}")

    ghd_total = sum(
        (_parse_reps(m["reps"]) or (0, ""))[0] * rounds
        for m in movements
        if "ghd" in m["name"].lower() and (_parse_reps(m["reps"]) or (0, "x"))[1] == "rep"
    )
    if ghd_total > 50:
        problems.append(f"{ghd_total:.0f} GHD sit-ups (cap 50)")

    secs = [_movement_seconds(m) for m in movements]
    known = [x for x in secs if x is not None]
    total = sum(known)

    if style == "EMOM":
        for m, sec in zip(movements, secs):
            name = m["name"].lower()
            if name == "rest":
                continue
            parsed = _parse_reps(m["reps"])
            if "run" in name and (not parsed or parsed[1] != "m" or parsed[0] > 100):
                problems.append(f"EMOM run minute too big: {m['reps']} {m['name']}")
            elif parsed and parsed[1] == "m" and ("row" in name or "erg" in name) and parsed[0] > 200:
                problems.append(f"EMOM row minute too big: {m['reps']}")
            elif parsed and parsed[1] == "cal" and parsed[0] > (8 if "assault" in name else 10):
                problems.append(f"EMOM cal minute too big: {m['reps']} {m['name']}")
            elif sec is not None and sec > 60:
                problems.append(f"EMOM minute overflows: {m['reps']} {m['name']}")
            elif sec is not None and sec < 20:
                problems.append(f"EMOM token minute: {m['reps']} {m['name']}")
        n_st = len(movements)
        if n_st and duration_min % n_st != 0:
            m2 = re.search(r"emom\s+(\d+)", w.get("format_line", "").lower())
            eff = int(m2.group(1)) if m2 else duration_min
            if eff % n_st != 0:
                problems.append(f"{n_st} stations do not divide EMOM {eff}")
    elif style == "Chipper":
        for m in movements:
            parsed = _parse_reps(m["reps"])
            if not parsed:
                continue
            n, unit = parsed
            name = m["name"].lower()
            if unit == "rep":
                cap = 100 if ("under" in name or "jump rope" in name) else 50
                if n > cap:
                    problems.append(f"chipper reps over ceiling: {m['reps']} {m['name']}")
            elif unit == "m" and ("row" in name or "erg" in name) and n > 1000:
                problems.append(f"chipper row over 1000 m: {m['reps']}")
            elif unit == "m" and "run" in name and n > 800:
                problems.append(f"chipper run over 800 m: {m['reps']}")
        if known and total > duration_min * 60 * 1.3:
            problems.append(f"chipper ~{total/60:.0f} min vs {duration_min} cap")
        elif known and total < duration_min * 60 * 0.5:
            problems.append(f"chipper ~{total/60:.0f} min vs {duration_min} target (too little)")
        if len(movements) < 6:
            problems.append(f"chipper with {len(movements)} movements (want 6-8)")
    elif style == "For Time":
        if known:
            est = total * rounds
            if est > (duration_min + 3) * 60 * 1.25:
                problems.append(f"for-time ~{est/60:.0f} min vs cap {duration_min+3}")
            elif est < duration_min * 60 * 0.5:
                problems.append(f"for-time ~{est/60:.0f} min vs target {duration_min} (too little)")
    elif style == "AMRAP":
        if known:
            if total > 360:
                problems.append(f"AMRAP round ~{total/60:.0f} min (want 2-4)")
            elif total < 60:
                problems.append(f"AMRAP round ~{total:.0f}s (want 2-4 min)")
    elif style == "Intervals":
        m = re.search(r"(\d+)\s*[×x]\s*(\d+)\s*min on(?:\s*/\s*(\d+)\s*min rest)?",
                      w.get("format_line", "").lower())
        if not m:
            problems.append(f"interval format_line unparseable: {w.get('format_line')}")
        else:
            reps_, on, rest = int(m.group(1)), int(m.group(2)), m.group(3)
            if rest is None:
                problems.append("intervals without rest")
            else:
                span = reps_ * (on + int(rest))
                if abs(span - duration_min) > 2:
                    problems.append(f"intervals span {span} min vs target {duration_min}")
            if known and total > on * 60:
                problems.append(f"interval work ~{total/60:.1f} min overflows {on} min window")
            elif known and total < on * 60 * 0.6:
                problems.append(f"interval work ~{total/60:.1f} min underfills {on} min window")
    return problems


def check(run):
    """All deterministic violations for one successful generation."""
    w = run["result"]
    inp = run["inputs"]
    v = []
    for m in w["movements"]:
        if m["name"].lower().strip() not in ALLOWED:
            v.append(f"OFF-VOCABULARY: {m['name']}")
    for item in _coverage_gap(w, inp["equipment"]):
        v.append(f"equipment unused: {item}")
    for name in _impossible_movements(w, inp["equipment"]):
        v.append(f"impossible movement (equipment not listed): {name}")
    # movements tagged with equipment outside the athlete's list
    have = {e.lower() for e in inp["equipment"]}
    for m in w["movements"]:
        for e in m["equipment"]:
            if e.lower() not in have and m["name"].lower() != "rest":
                v.append(f"tagged with unlisted equipment: {m['name']} -> {e}")
    v += _quality_problems(w, inp["style"], inp["duration"], inp.get("avoid") or [])
    return v


raw = [json.loads(l) for l in open(IN)]
best = {}
for r in raw:
    k = (r["model"], r["case"])
    if k in best and best[k]["status"] == 200:
        continue
    best[k] = r
runs = list(best.values())
by_model = defaultdict(list)
for r in runs:
    by_model[r["model"]].append(r)

analysis = {}
for model, rs in by_model.items():
    ok = [r for r in rs if r["status"] == 200]
    times_ok = [r["seconds"] for r in ok]
    details = []
    clean = 0
    total_viol = 0
    for r in ok:
        v = check(r)
        details.append({"case": r["case"], "seconds": r["seconds"], "violations": v})
        total_viol += len(v)
        if not v:
            clean += 1
    failed = [{"case": r["case"], "seconds": r["seconds"],
               "detail": r["result"].get("detail", "?")} for r in rs
              if r["status"] != 200 and "4006" not in str(r["result"].get("detail", ""))]
    quota_blocked = sum(1 for r in rs if r["status"] != 200
                        and "4006" in str(r["result"].get("detail", "")))
    analysis[model] = {
        "n": len(rs), "ok": len(ok), "failed": failed, "quota_blocked": quota_blocked,
        "time_median": round(statistics.median(times_ok), 1) if times_ok else None,
        "time_mean": round(statistics.mean(times_ok), 1) if times_ok else None,
        "time_p90": round(sorted(times_ok)[int(len(times_ok) * 0.9)], 1) if times_ok else None,
        "time_min": min(times_ok) if times_ok else None,
        "time_max": max(times_ok) if times_ok else None,
        "clean": clean, "total_violations": total_viol,
        "details": details,
    }
    print(f"\n=== {model}")
    print(f"  ok {len(ok)}/{len(rs)}  time med {analysis[model]['time_median']}s "
          f"mean {analysis[model]['time_mean']}s p90 {analysis[model]['time_p90']}s")
    print(f"  clean workouts {clean}/{len(ok)}  total violations {total_viol}")
    counts = defaultdict(int)
    for d in details:
        for v in d["violations"]:
            counts[v.split(":")[0]] += 1
    for k, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"    {n:>3}  {k}")
    for f in failed:
        print(f"    FAILED case {f['case']}: {f['detail'][:80]}")

with open("analysis.json", "w") as f:
    json.dump(analysis, f, indent=1)
print("\n-> analysis.json")
