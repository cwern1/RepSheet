"""Assemble experiments/model-comparison.md from results + analysis + judging.

Inputs (scratchpad): results.jsonl, analysis.json, mapping.json,
judge_scores.json (optional until judging ran).
Output: repo experiments/model-comparison.md + raw data copies.
"""
import json
import shutil
import statistics
import sys
from collections import defaultdict
from pathlib import Path

S = Path(__file__).parent
REPO = Path("/Users/chris/Workspace/wodgen-web")
OUTDIR = REPO / "experiments"
OUTDIR.mkdir(exist_ok=True)

raw = [json.loads(l) for l in open(S / "results.jsonl")]
best = {}
for r in raw:
    k = (r["model"], r["case"])
    if k in best and best[k]["status"] == 200:
        continue
    best[k] = r
runs = list(best.values())
analysis = json.load(open(S / "analysis.json"))
judge = {}
if (S / "judge_scores.json").exists():
    judge = json.load(open(S / "judge_scores.json"))

MODELS = [
    ("@cf/openai/gpt-oss-120b", "baseline (current prod)", "Responses API, reasoning medium",
     "$0.35 / $0.75 per M tok"),
    ("@cf/openai/gpt-oss-20b", "candidate", "Responses API, reasoning medium",
     "$0.20 / $0.30 per M tok"),
    ("@cf/meta/llama-3.3-70b-instruct-fp8-fast", "candidate", "chat completions, no reasoning",
     "$0.29 / $2.25 per M tok"),
    ("@cf/meta/llama-4-scout-17b-16e-instruct", "candidate", "chat completions + JSON-schema mode",
     "$0.27 / $0.85 per M tok"),
]
SHORT = {m: m.split("/")[-1] for m, *_ in MODELS}

by_case = defaultdict(dict)
for r in runs:
    by_case[r["case"]][r["model"]] = r

lines = []
w = lines.append
w("# Model comparison — Workers AI alternatives to gpt-oss-120b")
w("")
w("Experiment run 2026-08-24/25 on branch `model-comparison`. Question: is there a")
w("Workers AI model that generates **equal-or-better workouts faster** than the")
w("production model `@cf/openai/gpt-oss-120b`?")
w("")
w("## Method")
w("")
w("- **Same 50 fixed cases for every model** — all 5 styles × durations 5–60 min ×")
w("  equipment lists from 1 to 11 items, plus custom-text cases (restrictions,")
w("  contradictions, requested movements) and avoid-list cases. Nonces are pinned per")
w("  case, so every model sees the identical prompt including the same programming angle.")
w("  Cases 1–10 are the known-hard cases from the prompt eval matrix.")
w("- Generation goes through the **full production path** (FastAPI → prompt → parse →")
w("  Pydantic → equipment/quality validators → up to 1 corrective retry), via")
w("  `pywrangler dev` with the real Workers AI binding. Only the model id (and the")
w("  transport shape it requires) differs.")
w("- **Time** = client wall-clock per request, concurrency 3, so it includes any")
w("  server-side shape/corrective retries — the honest number a user would feel.")
w("- **Deterministic violations** = host-side re-run of the validator checks plus a")
w("  strict movement-vocabulary check (`analyze.py`).")
w("- **Blind judging**: per case, the four models' workouts were shuffled into")
w("  candidates A–D and ranked by Claude (Fable 5) as a CrossFit coach, without")
w("  knowing which model wrote which. Rank 1 = best of the four.")
w("- Caveats: single day, 50 samples/model; Workers AI was generally slow during the")
w("  first window (the 120b baseline normally runs ~14 s but measured far slower here,")
w("  and the free-tier quota exhaustion split the runs across two windows).")
w("  Relative comparisons are the point, absolute times less so.")
w("")
w("## Models")
w("")
w("| model | role | transport | price (in/out) |")
w("|---|---|---|---|")
for m, role, transport, price in MODELS:
    w(f"| `{m}` | {role} | {transport} | {price} |")
w("")
w("## Results summary")
w("")
w("| model | ok | med time | mean | p90 | min–max | clean workouts | violations | hard failures |")
w("|---|---|---|---|---|---|---|---|---|")
for m, *_ in MODELS:
    a = analysis.get(m)
    if not a:
        continue
    n_fail = len(a["failed"])
    rng = f"{a['time_min']}–{a['time_max']}s" if a["time_min"] is not None else "—"
    w(f"| {SHORT[m]} | {a['ok']}/50 | {a['time_median']}s | {a['time_mean']}s "
      f"| {a['time_p90']}s | {rng} | {a['clean']}/{a['ok']} "
      f"({100*a['clean']//max(a['ok'],1)}%) | {a['total_violations']} | {n_fail} |")
w("")
if judge:
    w("## Blind judge results (Fable 5, per-case ranking)")
    w("")
    ranks = defaultdict(list)
    scores = defaultdict(list)
    wins = defaultdict(int)
    for case, per_model in judge.items():
        ranked = sorted(per_model.items(), key=lambda kv: kv[1]["rank"])
        if ranked:
            wins[ranked[0][0]] += 1
        for m, sc in per_model.items():
            ranks[m].append(sc["rank"])
            scores[m].append(sc["score"])
    w("| model | mean rank (1=best) | mean score /10 | case wins |")
    w("|---|---|---|---|")
    for m, *_ in MODELS:
        if m in ranks:
            w(f"| {SHORT[m]} | {statistics.mean(ranks[m]):.2f} "
              f"| {statistics.mean(scores[m]):.1f} | {wins.get(m, 0)} |")
    w("")
w("## Violation breakdown")
w("")
for m, *_ in MODELS:
    a = analysis.get(m)
    if not a:
        continue
    counts = defaultdict(int)
    for d in a["details"]:
        for v in d["violations"]:
            counts[v.split(":")[0]] += 1
    w(f"**{SHORT[m]}**")
    if not counts and not a["failed"]:
        w("- none")
    for k, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        w(f"- {n} × {k}")
    for f in a["failed"]:
        w(f"- FAILED case {f['case']}: {f['detail'][:90]}")
    w("")
w("---")
w("")
w("## Appendix — all generations")
w("")
w("Raw data: [`results.jsonl`](results.jsonl) (one line per generation, includes")
w("resumed retries), [`analysis.json`](analysis.json) (per-run violations).")
w("")
for case in sorted(by_case):
    inp = next(iter(by_case[case].values()))["inputs"]
    hdr = (f"### Case {case} — {inp['style']} {inp['duration']} min · "
           f"{', '.join(inp['equipment']) or 'no equipment'}")
    w(hdr)
    if inp.get("custom"):
        w(f"*Athlete request:* `{inp['custom']}`")
    if inp.get("avoid"):
        w(f"*Avoid:* {', '.join(inp['avoid'])}")
    w("")
    for m, *_ in MODELS:
        r = by_case[case].get(m)
        if r is None:
            continue
        jr = judge.get(str(case), {}).get(m)
        jtxt = (f" · judge rank {jr['rank']}, score {jr['score']}/10" if jr else "")
        viol = ""
        a = analysis.get(m)
        if a:
            for d in a["details"]:
                if d["case"] == case and d["violations"]:
                    viol = " · violations: " + "; ".join(d["violations"])
        w(f"**{SHORT[m]}** — {r['seconds']}s{jtxt}{viol}")
        if r["status"] == 200:
            wk = r["result"]
            parts = [f"`{wk.get('format_line', '?')}`"]
            if wk.get("scheme"):
                parts.append(f"scheme: {wk['scheme']}")
            w("  " + " · ".join(parts))
            for mv in wk["movements"]:
                load = f" @ {mv['load_kg']}" if mv.get("load_kg") else ""
                w(f"  - {mv['reps']} {mv['name']}{load}")
            if wk.get("notes"):
                w(f"  - *notes: {wk['notes']}*")
        else:
            w(f"  - GENERATION FAILED: {r['result'].get('detail', '?')[:120]}")
        w("")
    w("")

out = OUTDIR / "model-comparison.md"
out.write_text("\n".join(lines))
shutil.copy(S / "results.jsonl", OUTDIR / "results.jsonl")
shutil.copy(S / "analysis.json", OUTDIR / "analysis.json")
print(f"wrote {out} ({out.stat().st_size} bytes)")
