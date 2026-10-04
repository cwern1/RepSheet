"""Render every generated workout from a round into one Markdown file for a
human (coach) review: per case, the inputs and each condition's workout in
whiteboard form, with latency, deterministic violations and — once judged —
the blind judge's score and note.

Usage (from a round directory): python ../render_review.py OUT.md COND1 COND2 ...
Reads results.jsonl, analysis.json (optional), judge_scores*.json (optional).
"""
import glob
import json
import sys
from collections import defaultdict

out, conditions = sys.argv[1], sys.argv[2:]
runs = defaultdict(dict)
for line in open("results.jsonl"):
    r = json.loads(line)
    prev = runs[r["case"]].get(r["model"])
    if prev and prev["status"] == 200:
        continue
    runs[r["case"]][r["model"]] = r

violations = defaultdict(dict)
try:
    for model, a in json.load(open("analysis.json")).items():
        for d in a["details"]:
            violations[d["case"]][model] = d["violations"]
except FileNotFoundError:
    pass

judge = {}
for path in glob.glob("judge_scores*.json"):
    judge = json.load(open(path))


def whiteboard(w):
    lines = [f"**{w['format_line']}**" + (f" · {w['scheme']}" if w.get("scheme") else "")]
    for m in w["movements"]:
        load = f" @ {m['load_kg']}" if m.get("load_kg") else ""
        lines.append(f"- {m['reps']} {m['name']}{load}")
    if w.get("notes"):
        lines.append(f"\n_{w['notes']}_")
    return "\n".join(lines)


doc = [f"# Generated workouts — {', '.join(conditions)}", "",
       "Each case shows the request, then every condition's workout. "
       "⏱ = end-to-end latency; ⚠ = deterministic check findings (strict v1 "
       "rules — off-list names are *allowed* under v2); ⚖ = blind judge "
       "score /10 and note.", ""]
for case in sorted(runs):
    first = next(iter(runs[case].values()))
    inp = first["inputs"]
    doc.append(f"## Case {case} — {inp['style']} {inp['duration']} min")
    doc.append(f"Equipment: {', '.join(inp['equipment']) or '(none)'}")
    if inp.get("custom"):
        doc.append(f"  \nAthlete request: “{inp['custom']}”")
    if inp.get("avoid"):
        doc.append(f"  \nAvoid: {', '.join(inp['avoid'])}")
    doc.append("")
    for cond in conditions:
        r = runs[case].get(cond)
        doc.append(f"### {cond}")
        if r is None:
            doc.append("_not run_\n")
            continue
        if r["status"] != 200:
            doc.append(f"❌ failed after {r['seconds']} s: {r['result'].get('detail')}\n")
        else:
            doc.append(whiteboard(r["result"]))
            meta = [f"⏱ {r['seconds']} s"]
            if v := violations.get(case, {}).get(cond):
                meta.append("⚠ " + "; ".join(v))
            if j := judge.get(str(case), {}).get(cond):
                meta.append(f"⚖ {j['score']}/10 — {j['note']}")
            doc.append("\n" + "  \n".join(meta) + "\n")
    doc.append("---\n")
open(out, "w").write("\n".join(doc))
print(f"wrote {out}")
