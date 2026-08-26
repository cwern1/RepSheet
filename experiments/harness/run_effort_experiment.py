"""Reasoning-effort benchmark: gpt-oss-120b at low/medium/high over the same
50 cases as the model comparison, all in one time window for fair timing.

JSONL lines use model label "gpt-oss-120b@<effort>" so analyze.py/judge_prep.py
group by effort; the actual request always targets @cf/openai/gpt-oss-120b.
"""
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/private/tmp/claude-501/-Users-chris-Workspace-wodgen-web/"
                   "a625b396-2e27-46dd-85bd-82f72f21f6da/scratchpad")
from run_experiment import CASES, URL

OUT = sys.argv[1] if len(sys.argv) > 1 else "effort_results.jsonl"
# "high" dropped on Chris's call: prod runs medium, and high is too slow to
# be a time-optimization candidate anyway.
EFFORTS = ["low", "medium"]
MODEL = "@cf/openai/gpt-oss-120b"

done = set()
try:
    for line in open(OUT):
        r = json.loads(line)
        if r["status"] == 200:
            done.add((r["model"], r["case"]))
except FileNotFoundError:
    pass


def run_one(job):
    effort, idx, case = job
    label = f"gpt-oss-120b@{effort}"
    if (label, idx) in done:
        return None
    payload = dict(case, model=MODEL, effort=effort)
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
    line = {"model": label, "case": idx, "inputs": case, "seconds": secs,
            "status": status, "result": parsed}
    print(f"{label:<22} case {idx:>2} {status} {secs:>6}s", flush=True)
    return line


if __name__ == "__main__":
    jobs = [(e, i + 1, c) for e in EFFORTS for i, c in enumerate(CASES)]
    ok = 0
    n = 0
    with ThreadPoolExecutor(max_workers=3) as pool:
        for line in pool.map(run_one, jobs):
            if line is None:
                continue
            n += 1
            ok += line["status"] == 200
            with open(OUT, "a") as f:
                f.write(json.dumps(line) + "\n")
    print(f"\ndone: {ok}/{n} ok -> {OUT}")
