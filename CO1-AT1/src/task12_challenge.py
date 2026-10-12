import csv
import os
import random
import time
from datetime import datetime

from dataset_generator import REG_NO, KEY_LOW, KEY_HIGH, banner, generate
from algo1_linear_search import linear_search
from algo2_binary_search import binary_search, binary_search_iterative
from algo3_bst_search import build_bst, bst_search

N = 1_000_000
SEARCHES = 50_000
NEW_PER_DAY = 1_000
LINEAR_SAMPLE = 200
HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "..", "results", "task12_results.csv")


def build_queries(present, count):
    rng = random.Random(5067 + 12)
    pool = list(present)
    half = count // 2
    hits = [rng.choice(pool) for _ in range(half - 1)] + [REG_NO]
    misses = []
    while len(misses) < count - half - 1:
        k = rng.randint(KEY_LOW, KEY_HIGH)
        if k not in present:
            misses.append(k)
    misses.append(REG_NO + 1)
    qs = hits + misses
    rng.shuffle(qs)
    return qs


def timed(fn):
    t0 = time.perf_counter()
    out = fn()
    return out, time.perf_counter() - t0


def run_searches(fn, structure, queries):
    t0 = time.perf_counter()
    found = 0
    for q in queries:
        r = fn(structure, q)[0]
        if r is True or (r is not False and r != -1):
            found += 1
    return time.perf_counter() - t0, found


def hash_lookup(table, key):
    return (key in table), 1


def main():
    print("=" * 70)
    print(banner())
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(f"TASK 12 - CHALLENGE: {SEARCHES:,} searches on {N:,} records")
    print("=" * 70)
    data = generate(N)
    present = set(data)
    queries = build_queries(present, SEARCHES)
    expected = sum(1 for q in queries if q in present)
    print(f"{SEARCHES:,} queries built ({expected:,} found, {SEARCHES - expected:,} not found)")
    print(f"load: 50,000 per hour = {SEARCHES / 3600:.1f} searches/second\n")

    rows = []

    t_lin, found = run_searches(linear_search, data, queries[:LINEAR_SAMPLE])
    t_lin_total = t_lin / LINEAR_SAMPLE * SEARCHES
    rows.append(["Linear search (estimated from %d queries)" % LINEAR_SAMPLE, 0.0, t_lin_total,
                 t_lin / LINEAR_SAMPLE * 1e6])

    srt, prep = timed(lambda: sorted(data))
    t, f_bin = run_searches(binary_search, srt, queries)
    rows.append(["Binary search - original (recursive)", prep, t, t / SEARCHES * 1e6])
    t, f_it = run_searches(binary_search_iterative, srt, queries)
    rows.append(["Binary search - iterative", prep, t, t / SEARCHES * 1e6])

    root, prep_bst = timed(lambda: build_bst(data))
    t, f_bst = run_searches(bst_search, root, queries)
    rows.append(["BST search", prep_bst, t, t / SEARCHES * 1e6])

    table, prep_h = timed(lambda: set(data))
    t, f_h = run_searches(hash_lookup, table, queries)
    rows.append(["Hash table (set) - revised index", prep_h, t, t / SEARCHES * 1e6])

    print(f"results agree (found counts): binary={f_bin:,} iterative={f_it:,} bst={f_bst:,} "
          f"hash={f_h:,} expected={expected:,}\n")
    print(f"{'design':<44}{'prep (s)':>10}{'50k searches (s)':>18}{'us/search':>11}")
    for name, prep, total, us in rows:
        print(f"{name:<44}{prep:>10.4f}{total:>18.4f}{us:>11.2f}")

    print("\nDaily update: %d new records arrive once per day" % NEW_PER_DAY)
    rng = random.Random(99)
    new = set()
    while len(new) < NEW_PER_DAY:
        k = rng.randint(KEY_LOW, KEY_HIGH)
        if k not in present and k != REG_NO + 1:
            new.add(k)
    new = list(new)
    _, t_resort = timed(lambda: sorted(data + new))
    new_sorted = sorted(new)
    _, t_merge = timed(lambda: sorted(srt + new_sorted))
    def bst_add():
        for key in new:
            build_bst_insert(root, key)
    _, t_bst_add = timed(bst_add)
    def hash_add():
        for key in new:
            table.add(key)
    _, t_hash_add = timed(hash_add)
    print(f"  sorted array: full re-sort            {t_resort:.4f} s")
    print(f"  sorted array: merge sorted batch      {t_merge:.4f} s")
    print(f"  BST: insert {NEW_PER_DAY:,} records           {t_bst_add:.4f} s")
    print(f"  hash table: insert {NEW_PER_DAY:,} records    {t_hash_add:.4f} s")

    per_day = SEARCHES * 24
    print(f"\nSearches per day at this rate: {per_day:,}")
    for name, prep, total, us in rows:
        print(f"  {name:<44} total search time for a day = {total * 24:.2f} s")

    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["design", "preprocess_s", "search_50000_s", "us_per_search",
                    "daily_update_resort_s", "daily_update_merge_s", "daily_update_bst_s",
                    "daily_update_hash_s"])
        for name, prep, total, us in rows:
            w.writerow([name, f"{prep:.6f}", f"{total:.6f}", f"{us:.4f}", f"{t_resort:.6f}",
                        f"{t_merge:.6f}", f"{t_bst_add:.6f}", f"{t_hash_add:.6f}"])
    print("\nresults saved to results/task12_results.csv")


def build_bst_insert(root, key):
    cur = root
    while True:
        if key < cur.key:
            if cur.left is None:
                cur.left = type(root)(key)
                return
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = type(root)(key)
                return
            cur = cur.right


if __name__ == "__main__":
    main()
