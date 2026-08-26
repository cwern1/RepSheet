"""Model-comparison driver: 50 fixed cases x N models against local dev server.

Writes one JSONL line per generation: model, case, inputs, seconds, status, body.
Concurrency 3; per-request wall time measured individually.
"""
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8787/api/generate"
OUT = sys.argv[1] if len(sys.argv) > 1 else "results.jsonl"

MODELS = [
    "@cf/openai/gpt-oss-120b",            # baseline (production)
    "@cf/openai/gpt-oss-20b",
    "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
    "@cf/meta/llama-4-scout-17b-16e-instruct",
]

BW = "Bodyweight"
KB = "Kettlebell"
DB = "Dumbbells"
BB = "Barbell"
PU = "Pull-up Bar"
MACHINES = ["Rower", "Bike Erg", "Ski Erg", "Assault Bike"]
FULL_GYM = [BW, BB, DB, KB, PU, "Rings", "Rower", "Jump Rope", "Plyo Box",
            "Wall Ball", "Running"]  # 11 items

def C(style, dur, eq, custom="", avoid=None, nonce=None):
    return {"style": style, "duration": dur, "equipment": eq, "custom": custom,
            "avoid": avoid or [], "nonce": nonce}

CASES = [
    # --- known hard cases from the eval matrix (pinned nonces) ---
    C("EMOM", 7, [BW], nonce=111),                                   # 1
    C("EMOM", 30, MACHINES, nonce=112),                              # 2
    C("Chipper", 30, [BW, BB, KB, PU, "Rower"], nonce=114),          # 3
    C("AMRAP", 20, [BW, DB, KB], nonce=115),                         # 4  unilateral angle
    C("For Time", 25, [BW, BB, PU], nonce=119),                      # 5  grindy+heavy angle
    C("AMRAP", 45, FULL_GYM, nonce=120),                             # 6  11 items
    C("For Time", 15, [BW, BB, DB], "no overhead today", nonce=105), # 7
    C("AMRAP", 12, [BW, KB, PU], "no overhead", nonce=117),          # 8
    C("Intervals", 15, ["Running", BW], nonce=368),                  # 9  midline angle
    C("AMRAP", 16, [KB, DB, BW], nonce=113),                         # 10 cross-implement dup trap
    # --- AMRAP spread ---
    C("AMRAP", 5, [BW], nonce=1011),                                 # 11
    C("AMRAP", 10, [BW, "Jump Rope"], nonce=1012),                   # 12
    C("AMRAP", 15, [BB, BW], nonce=1013),                            # 13
    C("AMRAP", 20, [KB, PU, BW], nonce=1014),                        # 14
    C("AMRAP", 25, [DB, "Plyo Box", BW], nonce=1015),                # 15
    C("AMRAP", 30, [BW, BB, "Wall Ball", "Rower"], nonce=1016),      # 16
    C("AMRAP", 12, [KB], nonce=1017),                                # 17 single implement, no BW
    C("AMRAP", 18, [DB, "Sandbag", BW], nonce=1018),                 # 18
    # --- For Time spread ---
    C("For Time", 8, [BW, KB], nonce=1021),                          # 19
    C("For Time", 12, [BB], nonce=1022),                             # 20 barbell only
    C("For Time", 20, [BW, DB, PU, "Rower"], nonce=1023),            # 21
    C("For Time", 30, [BW, BB, KB, "Running"], nonce=1024),          # 22 runs eat budget
    C("For Time", 40, FULL_GYM[:8], nonce=1025),                     # 23 8 items
    C("For Time", 10, [BW, "Jump Rope"], nonce=1026),                # 24
    C("For Time", 15, ["Wall Ball", "Rower", BW], nonce=1027),       # 25
    # --- EMOM spread (divisibility traps) ---
    C("EMOM", 10, [KB, BW], nonce=1031),                             # 26
    C("EMOM", 12, [BB, DB, BW], nonce=1032),                         # 27
    C("EMOM", 16, [DB, "Plyo Box", "Rower", BW], nonce=1033),        # 28
    C("EMOM", 20, [KB, BB, PU, BW, "Rower"], nonce=1034),            # 29 5 items / 20 min
    C("EMOM", 9, [BW, "Running"], nonce=1035),                       # 30 run minutes
    C("EMOM", 14, [KB, DB], nonce=1036),                             # 31 14 prime-ish
    C("EMOM", 24, [BW, BB, "Assault Bike"], nonce=1037),             # 32
    # --- Chipper spread ---
    C("Chipper", 15, [BW, KB], nonce=1041),                          # 33 short chipper
    C("Chipper", 20, [BW, DB, PU, "Jump Rope"], nonce=1042),         # 34
    C("Chipper", 25, [BB, BW, "Rower", "Wall Ball"], nonce=1043),    # 35
    C("Chipper", 35, FULL_GYM[:9], nonce=1044),                      # 36 9 items
    C("Chipper", 45, [BW, BB, KB, DB, PU, "Running"], nonce=1045),   # 37 long chipper
    C("Chipper", 20, ["Sandbag", BW, "GHD"], nonce=1046),            # 38 GHD cap
    # --- Intervals spread ---
    C("Intervals", 12, [BW, KB], nonce=1051),                        # 39
    C("Intervals", 20, [BB, BW, "Rower"], nonce=1052),               # 40
    C("Intervals", 24, [DB, "Ski Erg", BW], nonce=1053),             # 41
    C("Intervals", 30, [BW, "Running", PU], nonce=1054),             # 42
    C("Intervals", 16, ["Assault Bike", "Wall Ball", BW], nonce=1055),  # 43
    # --- custom-text cases ---
    C("AMRAP", 15, [BW, BB, DB], "bad knee - nothing that loads a deep bend",
      nonce=1061),                                                   # 44
    C("For Time", 12, [BW, KB], "easy recovery day please", nonce=1062),  # 45
    C("EMOM", 12, [BW, DB], "I want devil press in there", nonce=1063),   # 46
    C("Chipper", 25, [BW, KB, PU], "use the rower a lot", nonce=1064),    # 47 contradicts equipment
    C("Intervals", 18, [BW], "no jumping, downstairs neighbours", nonce=1065),  # 48
    # --- avoid-list cases ---
    C("AMRAP", 12, [KB, BW],
      avoid=["Kettlebell Swing", "Goblet Squat", "Burpee", "Push-up", "Sit-up"],
      nonce=1071),                                                   # 49
    C("For Time", 15, [BW, BB, PU],
      avoid=["Deadlift", "Pull-up", "Thruster", "Push-up", "Air Squat", "Run"],
      nonce=1072),                                                   # 50
]
assert len(CASES) == 50, len(CASES)


def run_one(job):  # pragma: no cover - driver
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
    line = {"model": model, "case": idx, "inputs": case, "seconds": secs,
            "status": status, "result": parsed}
    print(f"{model.split('/')[-1]:<32} case {idx:>2} {status} {secs:>6}s", flush=True)
    return line


if __name__ == "__main__":
    jobs = [(m, i + 1, c) for m in MODELS for i, c in enumerate(CASES)]
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        for line in pool.map(run_one, jobs):
            results.append(line)
            with open(OUT, "a") as f:
                f.write(json.dumps(line) + "\n")

    ok = sum(1 for r in results if r["status"] == 200)
    print(f"\ndone: {ok}/{len(results)} ok -> {OUT}")
