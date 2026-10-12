import argparse
import csv
import os
import random
import statistics
import sys
import time
from datetime import datetime

from dataset_generator import (REG_NO, SIZES, banner, generate, make_queries)
from algo1_linear_search import linear_search
from algo2_binary_search import binary_search, preprocess as sort_records
from algo3_bst_search import build_bst, bst_search, height

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "..", "results")
CSV_PATH = os.path.join(RESULTS, "results.csv")
FIELDS = ["n", "algorithm", "preprocess_s", "search_total_s", "avg_search_us",
          "avg_comparisons", "avg_comp_found", "avg_comp_notfound",
          "max_comparisons", "queries", "tree_height"]


def header(title):
    print("=" * 70)
    print(banner())
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 70)


def run_tests():
    header("TASK 8 - CORRECTNESS TESTS")
    small = [42, 7, 19, 88, 3, 56, 61]
    cases = [("first element", 42, True), ("last element", 61, True),
             ("middle value", 19, True), ("smallest value", 3, True),
             ("largest value", 88, True), ("absent (low)", 1, False),
             ("absent (high)", 99, False), ("absent (between)", 20, False)]
    srt = sort_records(small)
    root = build_bst(small)
    ok_all = True
    print(f"{'test case':<22}{'key':>5}  {'linear':>8}{'binary':>8}{'BST':>8}  expected  result")
    for name, key, expect in cases:
        l = linear_search(small, key)[0] != -1
        b = binary_search(srt, key)[0] != -1
        t = bst_search(root, key)[0]
        ok = (l == b == t == expect)
        ok_all &= ok
        print(f"{name:<22}{key:>5}  {str(l):>8}{str(b):>8}{str(t):>8}  {str(expect):<8}  {'PASS' if ok else 'FAIL'}")

    for label, arr in (("single element", [5]), ("empty list", [])):
        for key, expect in ((5, len(arr) == 1), (6, False)):
            l = linear_search(arr, key)[0] != -1
            b = binary_search(sort_records(arr), key)[0] != -1
            t = bst_search(build_bst(arr), key)[0]
            ok = (l == b == t == expect)
            ok_all &= ok
            print(f"{label:<22}{key:>5}  {str(l):>8}{str(b):>8}{str(t):>8}  {str(expect):<8}  {'PASS' if ok else 'FAIL'}")

    print("-" * 70)
    for n in SIZES[:3]:
        data = generate(n)
        srt, root = sort_records(data), build_bst(data)
        queries = make_queries(data)
        present = set(data)
        wrong = 0
        for q in queries:
            exp = q in present
            if not (((linear_search(data, q)[0] != -1) == exp) and
                    ((binary_search(srt, q)[0] != -1) == exp) and
                    (bst_search(root, q)[0] == exp)):
                wrong += 1
        own = (linear_search(data, REG_NO)[0] != -1, binary_search(srt, REG_NO)[0] != -1,
               bst_search(root, REG_NO)[0])
        own1 = (linear_search(data, REG_NO + 1)[0] != -1, binary_search(srt, REG_NO + 1)[0] != -1,
                bst_search(root, REG_NO + 1)[0])
        good = wrong == 0 and all(own) and not any(own1)
        ok_all &= good
        print(f"n={n:>7,}: {len(queries)} queries, mismatches={wrong}; "
              f"own reg {REG_NO} found by (lin,bin,bst)={own}; "
              f"reg+1 {REG_NO + 1} found={own1}  -> {'PASS' if good else 'FAIL'}")
    print("-" * 70)
    print("ALL TESTS PASSED" if ok_all else "SOME TESTS FAILED")
    return ok_all


def time_algo(name, search_fn, structure, queries, present):
    comps_f, comps_n, total = [], [], 0.0
    t0 = time.perf_counter()
    results = []
    for q in queries:
        r, c = search_fn(structure, q)
        results.append(r)
        (comps_f if q in present else comps_n).append(c)
    total = time.perf_counter() - t0
    allc = comps_f + comps_n
    return dict(search_total_s=total, avg_search_us=total / len(queries) * 1e6,
                avg_comparisons=statistics.mean(allc),
                avg_comp_found=statistics.mean(comps_f) if comps_f else 0,
                avg_comp_notfound=statistics.mean(comps_n) if comps_n else 0,
                max_comparisons=max(allc), queries=len(queries)), results


def benchmark_size(n):
    header(f"TASK 9 - BENCHMARK  n = {n:,} records")
    t0 = time.perf_counter()
    data = generate(n)
    print(f"dataset generated (seed 5067): {len(data):,} unique records "
          f"in {time.perf_counter() - t0:.3f}s")
    present = set(data)
    queries = make_queries(data)
    print(f"queries: {len(queries)} (100 found + 100 not found + own reg {REG_NO} + {REG_NO + 1})")
    rows, outputs = [], {}


    stats, outputs["linear"] = time_algo("linear", linear_search, data, queries, present)
    rows.append(dict(n=n, algorithm="Linear search", preprocess_s=0.0, tree_height="", **stats))


    t0 = time.perf_counter()
    srt = sort_records(data)
    prep = time.perf_counter() - t0
    stats, outputs["binary"] = time_algo("binary", binary_search, srt, queries, present)
    rows.append(dict(n=n, algorithm="Binary search (recursive)", preprocess_s=prep, tree_height="", **stats))


    t0 = time.perf_counter()
    root = build_bst(data)
    prep = time.perf_counter() - t0
    stats, outputs["bst"] = time_algo("bst", bst_search, root, queries, present)
    rows.append(dict(n=n, algorithm="BST search", preprocess_s=prep, tree_height=height(root), **stats))

    agree = all((a != -1) == (b != -1) == c for a, b, c in
                zip(outputs["linear"], outputs["binary"], outputs["bst"]))
    print(f"\nall three algorithms agree on every query: {agree}")
    print(f"\n{'algorithm':<27}{'preprocess(s)':>14}{'search tot(s)':>14}{'avg us/query':>13}"
          f"{'avg comps':>11}{'max comps':>10}")
    for r in rows:
        print(f"{r['algorithm']:<27}{r['preprocess_s']:>14.4f}{r['search_total_s']:>14.4f}"
              f"{r['avg_search_us']:>13.2f}{r['avg_comparisons']:>11.1f}{r['max_comparisons']:>10}")
    print(f"\nBST height = {rows[2]['tree_height']}  (log2 n = {n.bit_length() - 1}+)")
    return rows


def save_rows(rows):
    os.makedirs(RESULTS, exist_ok=True)
    existing = []
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="") as f:
            existing = list(csv.DictReader(f))
    sizes_new = {str(r["n"]) for r in rows}
    existing = [r for r in existing if r["n"] not in sizes_new]
    existing += rows
    existing.sort(key=lambda r: (int(r["n"]), r["algorithm"]))
    with open(CSV_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in existing:
            w.writerow({k: (f"{float(r[k]):.6f}" if k in ("preprocess_s", "search_total_s", "avg_search_us",
                                                         "avg_comparisons", "avg_comp_found",
                                                         "avg_comp_notfound") else r[k])
                        for k in FIELDS})
    print(f"\nresults saved to results/results.csv")


def run_cases(n=100_000):
    header(f"TASK 4 - BEST / AVERAGE / WORST CASE COUNTERS  (n = {n:,})")
    data = generate(n)
    srt = sort_records(data)
    root = build_bst(data)
    found_keys = random.Random(5067).sample(data, 2000)
    print("\nLinear search (basic op = comparison data[i] == key)")
    print(f"  best    : key is first element             -> {linear_search(data, data[0])[1]:>9,} comparison")
    avg = statistics.mean(linear_search(data, k)[1] for k in found_keys)
    print(f"  average : successful, random key (mean of {len(found_keys)}) -> {avg:>9,.1f}  (theory (n+1)/2 = {(n + 1) / 2:,.1f})")
    print(f"  worst   : key is last element              -> {linear_search(data, data[-1])[1]:>9,} comparisons")
    print(f"  worst   : key not present                  -> {linear_search(data, REG_NO + 1)[1]:>9,} comparisons")

    print("\nBinary search (basic op = comparison with arr[mid])")
    mid_key = srt[(len(srt) - 1) // 2]
    print(f"  best    : key sits at the first midpoint   -> {binary_search(srt, mid_key)[1]:>9,} comparison")
    avg = statistics.mean(binary_search(srt, k)[1] for k in found_keys)
    print(f"  average : successful, random key           -> {avg:>9,.2f}  (theory ~ log2 n - 1 = {n.bit_length() - 2:,})")
    worst = max(binary_search(srt, k)[1] for k in srt[::50])
    print(f"  worst   : deepest hit / key not present    -> {max(worst, binary_search(srt, REG_NO + 1)[1]):>9,} comparisons  (theory floor(log2 n)+1 = {n.bit_length():,})")

    print("\nBST search on randomly ordered input (basic op = comparison with node.key)")
    print(f"  best    : key is the root                  -> {bst_search(root, data[0])[1]:>9,} comparison")
    avg = statistics.mean(bst_search(root, k)[1] for k in found_keys)
    print(f"  average : successful, random key           -> {avg:>9,.2f}  (theory ~ 1.39 log2 n = {1.39 * (n.bit_length() - 1):,.1f})")
    print(f"  worst   : deepest node (tree height)       -> {height(root):>9,} comparisons")

    m = 2000
    chain = build_bst(sorted(data[:m]))
    print(f"\nBST worst-case demonstration: {m:,} records inserted in SORTED order")
    print(f"  height = {height(chain):,}; searching the last key costs {bst_search(chain, max(data[:m]))[1]:,} comparisons (= n)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--size", type=int)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--cases", action="store_true")
    a = ap.parse_args()
    if a.test:
        sys.exit(0 if run_tests() else 1)
    if a.cases:
        run_cases()
    if a.size:
        save_rows(benchmark_size(a.size))
    if a.all:
        rows = []
        for n in SIZES:
            rows += benchmark_size(n)
            print()
        save_rows(rows)
    if not (a.test or a.cases or a.size or a.all):
        ap.print_help()


if __name__ == "__main__":
    main()
