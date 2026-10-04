"""Build blind judging batches from results.jsonl.

Per case, the 4 models' workouts are shuffled into letters A-D (seeded by case
number so the mapping is reproducible) and grouped 10 cases per batch file.
Writes judge_batch_{1..5}.md and mapping.json {case: {letter: model}}.
"""
import json
import random
from collections import defaultdict

runs = [json.loads(l) for l in open("results.jsonl")]
by_case = defaultdict(dict)
for r in runs:
    prev = by_case[r["case"]].get(r["model"])
    if prev and prev["status"] == 200:
        continue
    by_case[r["case"]][r["model"]] = r

mapping = {}
batches = defaultdict(list)
for case in sorted(by_case):
    models = sorted(by_case[case])
    rng = random.Random(case * 7919)
    rng.shuffle(models)
    letters = "ABCD"[: len(models)]
    mapping[case] = dict(zip(letters, models))
    inp = next(iter(by_case[case].values()))["inputs"]
    lines = [f"## Case {case}",
             f"Inputs: style={inp['style']}, duration={inp['duration']} min, "
             f"equipment={inp['equipment']}"]
    if inp.get("custom"):
        lines.append(f"Athlete request: {inp['custom']!r}")
    if inp.get("avoid"):
        lines.append(f"Avoid (recently used): {inp['avoid']}")
    for letter, model in zip(letters, models):
        r = by_case[case][model]
        if r["status"] == 200:
            lines.append(f"### Candidate {letter}\n```json\n"
                         + json.dumps(r["result"], indent=1) + "\n```")
        else:
            lines.append(f"### Candidate {letter}\nGENERATION FAILED: "
                         + r["result"].get("detail", "?"))
    batches[(case - 1) // 10].append("\n".join(lines))

for i in sorted(batches):
    with open(f"judge_batch_{i + 1}.md", "w") as f:
        f.write("\n\n".join(batches[i]))
with open("mapping.json", "w") as f:
    json.dump(mapping, f, indent=1)
print(f"wrote {len(batches)} batches, mapping.json")
