"""Round 3 (2026-10-04): Claude Sonnet 5.5 (effort low, via AI Gateway unified
billing) vs the production baseline, same 50 cases as round 2.

Usage: python run_sonnet.py round3_results.jsonl
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor

import run_experiment
from run_experiment import CASES, run_one

MODELS = [
    "@cf/openai/gpt-oss-120b",      # baseline (production, effort low)
    "anthropic/claude-sonnet-5.5",  # candidate, effort low
]

if __name__ == "__main__":
    out = sys.argv[1]
    jobs = [(m, i + 1, c) for i, c in enumerate(CASES) for m in MODELS]  # interleaved
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for line in pool.map(run_one, jobs):
            results.append(line)
            with open(out, "a") as f:
                f.write(json.dumps(line) + "\n")
    ok = sum(1 for r in results if r["status"] == 200)
    print(f"\ndone: {ok}/{len(results)} ok -> {out}")
