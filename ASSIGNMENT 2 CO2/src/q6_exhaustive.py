import itertools
import random
import time
from datetime import datetime

SEED = 5067


def exhaustive(items, cap):
    n = len(items)
    best_value, best_mask = -1, 0
    feasible = 0
    for mask in range(1 << n):
        w = v = 0
        for i in range(n):
            if mask >> i & 1:
                w += items[i][1]
                v += items[i][2]
        if w <= cap:
            feasible += 1
            if v > best_value:
                best_value, best_mask = v, mask
    return best_value, best_mask, feasible


def independent_check(items, cap):
    best = 0
    for r in range(len(items) + 1):
        for combo in itertools.combinations(items, r):
            if sum(c[1] for c in combo) <= cap:
                best = max(best, sum(c[2] for c in combo))
    return best


def make_items(n, rng):
    return [("P%d" % (i + 1), rng.randint(5, 50), rng.randint(10, 100)) for i in range(n)]


def header(title):
    print("=" * 74)
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 74)


def main():
    header("Q6 - EXHAUSTIVE SEARCH (HELICOPTER PAYLOAD)")
    small = [("P1", 7, 42), ("P2", 3, 12), ("P3", 4, 40), ("P4", 5, 25), ("P5", 2, 10)]
    cap = 10
    print("Verification instance, capacity %d kg" % cap)
    for it in small:
        print("  %s weight %d value %d" % it)
    print("all 32 subsets:")
    print("  %-22s%8s%8s%10s" % ("subset", "weight", "value", "feasible"))
    for mask in range(32):
        names = [small[i][0] for i in range(5) if mask >> i & 1]
        w = sum(small[i][1] for i in range(5) if mask >> i & 1)
        v = sum(small[i][2] for i in range(5) if mask >> i & 1)
        print("  %-22s%8d%8d%10s" % ("{" + ",".join(names) + "}", w, v, "yes" if w <= cap else "no"))
    bv, bm, feas = exhaustive(small, cap)
    chosen = [small[i][0] for i in range(5) if bm >> i & 1]
    print("exhaustive search: best value %d with %s, feasible subsets %d" % (bv, chosen, feas))
    check = independent_check(small, cap)
    print("independent check (itertools.combinations): best value %d -> %s" %
          (check, "MATCH" if check == bv else "MISMATCH"))
    print()
    rng = random.Random(SEED)
    print("GROWTH (capacity = 40 percent of total weight)")
    print("%5s%14s%14s%14s%12s%12s" % ("n", "2^n", "candidates", "feasible", "best value", "time (s)"))
    csv_lines = []
    last = None
    for n in (10, 12, 14, 16, 18, 20, 21):
        items = make_items(n, rng)
        cap = int(0.4 * sum(i[1] for i in items))
        t0 = time.perf_counter()
        bv, bm, feas = exhaustive(items, cap)
        t = time.perf_counter() - t0
        print("%5d%14d%14d%14d%12d%12.4f" % (n, 2 ** n, 2 ** n, feas, bv, t))
        csv_lines.append("CSV,q6,%d,%d,%d,%d,%d,%.4f" % (n, 2 ** n, 2 ** n, feas, bv, t))
        last = (n, t)
    n, t = last
    per_cand = t / 2 ** n
    limit = 5.0
    n_lim = 1
    while per_cand * 2 ** (n_lim + 1) <= limit:
        n_lim += 1
    print()
    print("time per candidate: %.2f microseconds" % (per_cand * 1e6))
    print("response time chosen for the planner: %.0f s -> largest deployable n about %d packages" % (limit, n_lim))
    for target in (25, 30, 40, 50):
        secs = per_cand * 2 ** target
        text = "%.1f s" % secs if secs < 86400 * 365 else "%.1f years" % (secs / 31536000)
        print("  predicted time for n = %2d : %s" % (target, text))
    csv_lines.append("CSV,q6lim,%.3f,%d" % (per_cand * 1e6, n_lim))
    print()
    for line in csv_lines:
        print(line)


if __name__ == "__main__":
    main()
