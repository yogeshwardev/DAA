import csv
import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
LOGS = os.path.join(RES, "logs")
ONLINE = os.path.join(RES, "online")
SCRIPTS = ["q1_sorting", "q2_sequential", "q3_string_matching", "q4_closest_pair", "q5_convex_hull",
           "q6_exhaustive", "q7_redesign"]


def run_local():
    os.makedirs(LOGS, exist_ok=True)
    for name in SCRIPTS:
        print("running", name, flush=True)
        out = subprocess.run([sys.executable, os.path.join(HERE, name + ".py")], capture_output=True,
                             text=True, check=True).stdout
        with open(os.path.join(LOGS, name + ".txt"), "w", encoding="ascii", errors="replace") as f:
            f.write(out)


def parse(paths):
    groups = {}
    for path in paths:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("CSV,"):
                    parts = line.split(",")
                    groups.setdefault(parts[1], []).append(parts[2:])
    os.makedirs(RES, exist_ok=True)
    for key, rows in groups.items():
        with open(os.path.join(RES, key + ".csv"), "w", newline="") as f:
            csv.writer(f).writerows(rows)
        print("wrote results/%s.csv (%d rows)" % (key, len(rows)))


def main():
    if "--online" in sys.argv:
        parse(sorted(glob.glob(os.path.join(ONLINE, "*.txt"))))
    else:
        run_local()
        parse(sorted(glob.glob(os.path.join(LOGS, "*.txt"))))


if __name__ == "__main__":
    main()
