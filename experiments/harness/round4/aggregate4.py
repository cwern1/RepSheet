"""Merge the five round-4 blind-judge result files, de-anonymize via
mapping.json, write judge_scores4.json {case: {model: {rank, score, note}}}
and print a summary. Run from experiments/harness/round4/."""
import json
import statistics
from collections import defaultdict

merged = {}
for i in range(1, 6):
    merged.update(json.load(open(f"judge_result_{i}.json")))

mapping = json.load(open("mapping.json"))
scores = {}
for case, per_letter in merged.items():
    m = mapping[case]
    scores[case] = {m[letter]: v for letter, v in per_letter.items()
                    if letter in ("A", "B", "C")}
json.dump(scores, open("judge_scores4.json", "w"), indent=1)

ranks = defaultdict(list)
pts = defaultdict(list)
wins = defaultdict(int)
for case, per_model in scores.items():
    top = min(per_model.items(), key=lambda kv: kv[1]["rank"])
    wins[top[0]] += 1
    for model, v in per_model.items():
        ranks[model].append(v["rank"])
        pts[model].append(v["score"])
print(f"{'model':<45} {'mean rank':>9} {'mean score':>10} {'wins':>5}")
for model in sorted(ranks, key=lambda m: statistics.mean(ranks[m])):
    print(f"{model:<45} {statistics.mean(ranks[model]):>9.2f} "
          f"{statistics.mean(pts[model]):>10.2f} {wins[model]:>5}")
