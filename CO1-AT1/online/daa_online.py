import random
import statistics
import time
from datetime import datetime

SIZE = 1000
MODE = "bench"

REG_NO = 192465067
NAME = "N D YOGESHWAR"
SEED = 5067
KEY_LOW, KEY_HIGH = 192000000, 194999999


def generate(n):
    rng = random.Random(SEED)
    keys = set(rng.sample(range(KEY_LOW, KEY_HIGH + 1), n))
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


def make_queries(data, count=100):
    rng = random.Random(SEED + 1)
    present = set(data)
    hits = rng.sample(data, count)
    misses = []
    while len(misses) < count:
        k = rng.randint(KEY_LOW, KEY_HIGH)
        if k not in present:
            misses.append(k)
    qs = hits + misses + [REG_NO, REG_NO + 1]
    rng.shuffle(qs)
    return qs


def linear_search(data, key):
    comparisons = 0
    for i in range(len(data)):
        comparisons += 1
        if data[i] == key:
            return i, comparisons
    return -1, comparisons


def binary_search(arr, key, low=0, high=None, c=None):
    if high is None:
        high = len(arr) - 1
    if c is None:
        c = [0]
    if low > high:
        return -1, c[0]
    mid = (low + high) // 2
    c[0] += 1
    if arr[mid] == key:
        return mid, c[0]
    if key < arr[mid]:
        return binary_search(arr, key, low, mid - 1, c)
    return binary_search(arr, key, mid + 1, high, c)


def binary_search_iterative(arr, key):
    low, high, comparisons = 0, len(arr) - 1, 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == key:
            return mid, comparisons
        if key < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, comparisons


class Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def bst_insert(root, key):
    cur = root
    while True:
        if key < cur.key:
            if cur.left is None:
                cur.left = Node(key)
                return
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = Node(key)
                return
            cur = cur.right


def build_bst(data):
    root = None
    for key in data:
        if root is None:
            root = Node(key)
        else:
            bst_insert(root, key)
    return root


def bst_search(root, key):
    comparisons = 0
    cur = root
    while cur is not None:
        comparisons += 1
        if key == cur.key:
            return True, comparisons
        cur = cur.left if key < cur.key else cur.right
    return False, comparisons


def height(root):
    if root is None:
        return 0
    level, h = [root], 0
    while level:
        h += 1
        level = [c for n in level for c in (n.left, n.right) if c is not None]
    return h


def header(title):
    print("=" * 70)
    print("Reg No: %d | Name: %s" % (REG_NO, NAME))
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 70)


def run_tests():
    header("TASK 8 - CORRECTNESS TESTS")
    small = [42, 7, 19, 88, 3, 56, 61]
    srt = sorted(small)
    root = build_bst(small)
    cases = [("first element", 42), ("last element", 61), ("middle value", 19), ("smallest value", 3),
             ("largest value", 88), ("absent (low)", 1), ("absent (high)", 99), ("absent (between)", 20)]
    ok_all = True
    for name, key in cases:
        expect = key in small
        l = linear_search(small, key)[0] != -1
        b = binary_search(srt, key)[0] != -1
        t = bst_search(root, key)[0]
        ok = l == b == t == expect
        ok_all = ok_all and ok
        print("%-20s key=%-4d linear=%-5s binary=%-5s bst=%-5s expected=%-5s %s" %
              (name, key, l, b, t, expect, "PASS" if ok else "FAIL"))
    for n in (1000, 10000, 100000):
        data = generate(n)
        srt, root = sorted(data), build_bst(data)
        present = set(data)
        wrong = 0
        for q in make_queries(data):
            e = q in present
            if not ((linear_search(data, q)[0] != -1) == e and (binary_search(srt, q)[0] != -1) == e
                    and bst_search(root, q)[0] == e):
                wrong += 1
        own = (linear_search(data, REG_NO)[0] != -1, binary_search(srt, REG_NO)[0] != -1, bst_search(root, REG_NO)[0])
        own1 = (linear_search(data, REG_NO + 1)[0] != -1, binary_search(srt, REG_NO + 1)[0] != -1,
                bst_search(root, REG_NO + 1)[0])
        good = wrong == 0 and all(own) and not any(own1)
        ok_all = ok_all and good
        print("n=%-7d mismatches=%d own key found=%s own+1 found=%s %s" %
              (n, wrong, own, own1, "PASS" if good else "FAIL"))
    print("ALL TESTS PASSED" if ok_all else "SOME TESTS FAILED")


def time_algo(fn, structure, queries, present):
    cf, cn, res = [], [], []
    t0 = time.perf_counter()
    for q in queries:
        r, c = fn(structure, q)
        res.append(r)
        (cf if q in present else cn).append(c)
    total = time.perf_counter() - t0
    allc = cf + cn
    return [total, total / len(queries) * 1e6, statistics.mean(allc), statistics.mean(cf),
            statistics.mean(cn), max(allc), len(queries)], res


def run_bench(n):
    header("TASK 9 - BENCHMARK  n = %s records" % format(n, ","))
    data = generate(n)
    present = set(data)
    queries = make_queries(data)
    print("dataset: %d unique records (seed %d), %d queries" % (len(set(data)), SEED, len(queries)))
    rows = []
    s, r1 = time_algo(linear_search, data, queries, present)
    rows.append(("Linear search", 0.0, s, ""))
    t0 = time.perf_counter()
    srt = sorted(data)
    prep = time.perf_counter() - t0
    s, r2 = time_algo(binary_search, srt, queries, present)
    rows.append(("Binary search (recursive)", prep, s, ""))
    t0 = time.perf_counter()
    root = build_bst(data)
    prep = time.perf_counter() - t0
    s, r3 = time_algo(bst_search, root, queries, present)
    rows.append(("BST search", prep, s, height(root)))
    agree = all((a != -1) == (b != -1) == c for a, b, c in zip(r1, r2, r3))
    print("all three algorithms agree on every query:", agree)
    print("%-27s%14s%14s%13s%11s%10s" % ("algorithm", "preprocess(s)", "search tot(s)", "avg us/query",
                                         "avg comps", "max comps"))
    for name, prep, s, h in rows:
        print("%-27s%14.4f%14.4f%13.2f%11.1f%10d" % (name, prep, s[0], s[1], s[2], s[5]))
    print("BST height =", rows[2][3])
    print()
    for name, prep, s, h in rows:
        print("CSV,%d,%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d,%d,%s" %
              (n, name, prep, s[0], s[1], s[2], s[3], s[4], s[5], s[6], h))


def run_cases(n):
    header("TASK 4 - BEST / AVERAGE / WORST CASE COUNTERS (n = %s)" % format(n, ","))
    data = generate(n)
    srt = sorted(data)
    root = build_bst(data)
    sample = random.Random(SEED).sample(data, 2000)
    print("Linear: best", linear_search(data, data[0])[1], "| average",
          round(statistics.mean(linear_search(data, k)[1] for k in sample), 1),
          "| worst (last key)", linear_search(data, data[-1])[1],
          "| worst (absent)", linear_search(data, REG_NO + 1)[1])
    print("Binary: best", binary_search(srt, srt[(len(srt) - 1) // 2])[1], "| average",
          round(statistics.mean(binary_search(srt, k)[1] for k in sample), 2),
          "| worst (absent)", binary_search(srt, REG_NO + 1)[1])
    print("BST   : best", bst_search(root, data[0])[1], "| average",
          round(statistics.mean(bst_search(root, k)[1] for k in sample), 2), "| height", height(root))
    chain = build_bst(sorted(data[:2000]))
    print("BST on 2000 sorted records: height", height(chain),
          "| comparisons for last key", bst_search(chain, max(data[:2000]))[1])


def run_task12():
    n, searches, new_count, sample_n = 1000000, 50000, 1000, 50
    header("TASK 12 - 50,000 searches on 1,000,000 records")
    data = generate(n)
    present = set(data)
    rng = random.Random(SEED + 12)
    pool = list(present)
    half = searches // 2
    qs = [rng.choice(pool) for _ in range(half - 1)] + [REG_NO]
    misses = []
    while len(misses) < searches - half - 1:
        k = rng.randint(KEY_LOW, KEY_HIGH)
        if k not in present:
            misses.append(k)
    qs += misses + [REG_NO + 1]
    rng.shuffle(qs)

    def run(fn, st, q):
        t0 = time.perf_counter()
        for x in q:
            fn(st, x)
        return time.perf_counter() - t0

    out = []
    t = run(linear_search, data, qs[:sample_n])
    out.append(("Linear search (estimated from %d queries)" % sample_n, 0.0, t / sample_n * searches,
                t / sample_n * 1e6))
    t0 = time.perf_counter()
    srt = sorted(data)
    prep = time.perf_counter() - t0
    t = run(binary_search, srt, qs)
    out.append(("Binary search - original (recursive)", prep, t, t / searches * 1e6))
    t = run(binary_search_iterative, srt, qs)
    out.append(("Binary search - iterative", prep, t, t / searches * 1e6))
    t0 = time.perf_counter()
    root = build_bst(data)
    prep_b = time.perf_counter() - t0
    t = run(bst_search, root, qs)
    out.append(("BST search", prep_b, t, t / searches * 1e6))
    t0 = time.perf_counter()
    table = set(data)
    prep_h = time.perf_counter() - t0
    t = run(lambda s, k: (k in s, 1), table, qs)
    out.append(("Hash table (set) - revised index", prep_h, t, t / searches * 1e6))
    print("%-44s%10s%18s%11s" % ("design", "prep (s)", "50k searches (s)", "us/search"))
    for name, p, tot, us in out:
        print("%-44s%10.4f%18.4f%11.2f" % (name, p, tot, us))
    new = set()
    while len(new) < new_count:
        k = rng.randint(KEY_LOW, KEY_HIGH)
        if k not in present and k != REG_NO + 1:
            new.add(k)
    new = list(new)
    t0 = time.perf_counter()
    sorted(data + new)
    t_resort = time.perf_counter() - t0
    ns = sorted(new)
    t0 = time.perf_counter()
    sorted(srt + ns)
    t_merge = time.perf_counter() - t0
    t0 = time.perf_counter()
    for k in new:
        bst_insert(root, k)
    t_bst = time.perf_counter() - t0
    t0 = time.perf_counter()
    for k in new:
        table.add(k)
    t_hash = time.perf_counter() - t0
    print("daily update of %d records: full re-sort %.4f s | merge %.4f s | BST insert %.4f s | hash insert %.4f s" %
          (new_count, t_resort, t_merge, t_bst, t_hash))
    print()
    for name, p, tot, us in out:
        print("CSV12,%s,%.6f,%.6f,%.4f,%.6f,%.6f,%.6f,%.6f" % (name, p, tot, us, t_resort, t_merge, t_bst, t_hash))


if MODE == "test":
    run_tests()
elif MODE == "cases":
    run_cases(SIZE)
elif MODE == "task12":
    run_task12()
else:
    run_bench(SIZE)
