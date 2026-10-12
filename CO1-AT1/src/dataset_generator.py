import csv
import os
import random

REG_NO = 192465067
NAME = "N D YOGESHWAR"
SEED = int(str(REG_NO)[-4:])
KEY_LOW, KEY_HIGH = 192_000_000, 194_999_999
SIZES = [1_000, 10_000, 100_000, 1_000_000]


def banner():
    return f"Reg No: {REG_NO} | Name: {NAME}"


def generate(n, seed=SEED):
    rng = random.Random(seed)
    pool = range(KEY_LOW, KEY_HIGH + 1)
    keys = set(rng.sample(pool, n))
    keys.discard(REG_NO + 1)
    if REG_NO not in keys:
        keys.discard(next(iter(keys)))
        keys.add(REG_NO)
    while len(keys) < n:
        k = rng.randint(KEY_LOW, KEY_HIGH)
        if k != REG_NO + 1:
            keys.add(k)
    data = list(keys)
    rng.shuffle(data)
    return data


def make_queries(data, count=100, seed=SEED):
    rng = random.Random(seed + 1)
    present = set(data)
    hits = rng.sample(data, min(count, len(data)))
    misses = []
    while len(misses) < count:
        k = rng.randint(KEY_LOW, KEY_HIGH)
        if k not in present:
            misses.append(k)
    queries = hits + misses + [REG_NO, REG_NO + 1]
    rng.shuffle(queries)
    return queries


def save_csv(path, data):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["registration_number"])
        w.writerows([k] for k in data)


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "data")
    os.makedirs(out, exist_ok=True)
    print(banner())
    print(f"seed = {SEED}")

    d = generate(1000)
    save_csv(os.path.join(out, "sample_1000.csv"), d)
    print(f"wrote data/sample_1000.csv ({len(d)} records)")
    for n in SIZES:
        d = generate(n)
        print(f"n={n:>9,}  unique={len(set(d)):>9,}  own key present={REG_NO in set(d)}  "
              f"own+1 present={(REG_NO + 1) in set(d)}")
