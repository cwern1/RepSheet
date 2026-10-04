"""Round 4 (2026-10-04, branch sonnet-prompt-v2): does a principles-first,
less rigid prompt (SYSTEM_PROMPT_CLAUDE, "v2") get more out of Sonnet 5.5, and
does a higher reasoning effort help? Same 50 cases as rounds 1-3.

Conditions (labels go in the JSONL "model" field so analyze.py / judge_prep.py
group by condition):
  sonnet-low-v1     production prompt + strict checks (control; re-run with
                    the double-JSON parse fix so it compares cleanly)
  sonnet-low-v2     v2 prompt + relaxed checks, effort low
  sonnet-medium-v2  v2 prompt + relaxed checks, effort medium

Usage: python run_round4.py round4/results.jsonl
"""
import json
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from run_experiment import CASES, URL

SONNET = "anthropic/claude-sonnet-5.5"
CONDITIONS = {
    "sonnet-low-v1": {"model": SONNET, "effort": "low", "prompt": "v1"},
    "sonnet-low-v2": {"model": SONNET, "effort": "low", "prompt": "v2"},
    "sonnet-medium-v2": {"model": SONNET, "effort": "medium", "prompt": "v2"},
}


def run_one(job):
    # Gateway auth blips are infrastructure, not model failures: wait and retry.
    for _ in range(4):
        line = _run_once(job)
        if "2018" not in json.dumps(line["result"]):
            return line
        time.sleep(15)
    return line


def _run_once(job):
    label, idx, case = job
    payload = dict(case, **CONDITIONS[label])
    req = urllib.request.Request(
        URL, json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            status, body = resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        status, body = e.code, e.read().decode()
    except Exception as e:
        status, body = 0, json.dumps({"detail": f"client error: {e}"})
    secs = round(time.time() - t0, 1)
    try:
        parsed = json.loads(body)
    except Exception:
        parsed = {"detail": body[:500]}
    print(f"{label:<18} case {idx:>2} {status} {secs:>6}s", flush=True)
    return {"model": label, "params": CONDITIONS[label], "case": idx,
            "inputs": case, "seconds": secs, "status": status, "result": parsed}


if __name__ == "__main__":
    out = sys.argv[1]
    # Resumable: keep successful lines, re-run everything else. (A transient
    # "AiGatewayError 2018: Invalid User Credentials" burst killed 138/150 of
    # the first attempt; the wrangler dev remote session recovered by itself.)
    done = set()
    try:
        kept = [l for l in open(out) if json.loads(l)["status"] == 200]
        done = {(json.loads(l)["model"], json.loads(l)["case"]) for l in kept}
        open(out, "w").writelines(kept)
    except FileNotFoundError:
        pass
    # Interleaved per case so every condition sees the same time window.
    jobs = [(c, i + 1, case) for i, case in enumerate(CASES) for c in CONDITIONS
            if (c, i + 1) not in done]
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for line in pool.map(run_one, jobs):
            results.append(line)
            with open(out, "a") as f:
                f.write(json.dumps(line) + "\n")
    ok = sum(1 for r in results if r["status"] == 200)
    print(f"\ndone: {ok}/{len(results)} ok -> {out}")
