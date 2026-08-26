"""Re-run every (model, case) pair that has no successful line in results.jsonl.

Priority: cheapest model first, so a second quota exhaustion costs the least
data. Successes and real failures are appended to results.jsonl; quota errors
(AiError 4006) are not recorded — after 3 consecutive ones the script exits 2.
Exit 0 = experiment complete, exit 1 = some pairs still failing (non-quota).
"""
import json
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, "/private/tmp/claude-501/-Users-chris-Workspace-wodgen-web/"
                   "a625b396-2e27-46dd-85bd-82f72f21f6da/scratchpad")
from run_experiment import CASES, URL

OUT = sys.argv[1] if len(sys.argv) > 1 else "results.jsonl"

PRIORITY = [
    "@cf/meta/llama-4-scout-17b-16e-instruct",   # cheapest
    "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    "@cf/openai/gpt-oss-20b",
    "@cf/openai/gpt-oss-120b",
]

done = set()
for line in open(OUT):
    r = json.loads(line)
    if r["status"] == 200:
        done.add((r["model"], r["case"]))

missing = [(m, i + 1, c) for m in PRIORITY for i, c in enumerate(CASES)
           if (m, i + 1) not in done]
print(f"missing pairs: {len(missing)}", flush=True)
if not missing:
    sys.exit(0)

quota_strikes = 0
lock = threading.Lock()
stop = False


def run_one(job):
    global quota_strikes, stop
    if stop:
        return None
    model, idx, case = job
    payload = dict(case, model=model)
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
    detail = parsed.get("detail", "") if isinstance(parsed, dict) else ""
    print(f"{model.split('/')[-1]:<32} case {idx:>2} {status} {secs:>6}s "
          f"{detail[:60]}", flush=True)
    with lock:
        if "4006" in str(detail):
            quota_strikes += 1
            if quota_strikes >= 3:
                stop = True
            return None
        quota_strikes = 0
    line = {"model": model, "case": idx, "inputs": case, "seconds": secs,
            "status": status, "result": parsed, "resumed": True}
    with lock:
        with open(OUT, "a") as f:
            f.write(json.dumps(line) + "\n")
    return status


with ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(run_one, missing))

if stop:
    print("quota exhausted again — stopping", flush=True)
    sys.exit(2)
sys.exit(0 if all(s == 200 for s in results if s is not None) and None not in results else 1)
