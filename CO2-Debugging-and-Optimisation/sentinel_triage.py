"""
sentinel_triage.py -- SentinelOps SOC alert-triage module (corrected + optimised).

CSA06 Design and Analysis of Algorithms, CO2 Debugging and Optimisation Task.

Functions (production versions)
    sort_alerts(alerts)            stable sort by severity, highest first
    build_blocklist(entries)       one-time hash index of blocked IPs
    is_blocked(blocklist, ip)      O(1) average membership test
    find_signature(log, pattern)   every start index of pattern in log (KMP)
    closest_logins(events)         closest pair of login locations (sorted sweep
                                   with pruning, squared distances)

Reference (corrected brute-force) versions are kept with a `_bf` suffix.  They
are used by the test harness to prove that every optimisation preserves the
corrected output, and by the measurement code in Part (d).

Run `python sentinel_triage.py` to execute the test harness, and
`python -c "import sentinel_triage as s; s.measure()"` for the Part (d) counts.
"""

import math
import random
import time
from functools import cmp_to_key

# ---------------------------------------------------------------------------
# 1. Sorting alerts by severity (highest first, ties keep arrival order)
# ---------------------------------------------------------------------------

def sort_alerts_bf(alerts, counter=None):
    """Corrected insertion sort (descending severity, stable), in place.

    Args:
        alerts: list of (alert_id, severity) tuples. Sorted in place.
        counter: optional dict; counter["cmp"] is increased by one for every
            severity comparison (used for the Part (d) measurements).
    Returns:
        The same list, sorted.
    """
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0:
            if counter is not None:
                counter["cmp"] += 1
            # strict '<' : an equal severity is never moved past -> stable
            if alerts[j][1] < key[1]:
                alerts[j + 1] = alerts[j]
                j -= 1
            else:
                break
        alerts[j + 1] = key
    return alerts


def sort_alerts(alerts):
    """Production sort: Python's Timsort, in place, stable.

    Timsort detects already-ordered runs, so a nearly sorted feed costs about
    n comparisons (like insertion sort), but a random feed costs O(n log n)
    instead of insertion sort's O(n^2).  `reverse=True` keeps equal keys in
    their original (arrival) order, so the output is identical to sort_alerts_bf.
    """
    alerts.sort(key=lambda alert: alert[1], reverse=True)
    return alerts


# ---------------------------------------------------------------------------
# 2. Blocklist lookup
# ---------------------------------------------------------------------------

def is_blocked_bf(blocklist, ip, counter=None):
    """Corrected sequential search: True if ip occurs in the blocklist list."""
    for entry in blocklist:
        if counter is not None:
            counter["cmp"] += 1
        if entry == ip:
            return True
    return False          # reached only after every entry was checked


def build_blocklist(entries):
    """Build the lookup index once per blocklist update: O(m) time and space."""
    return frozenset(entries)


def is_blocked(blocklist, ip):
    """O(1) average membership test on an index from build_blocklist().

    A plain list is also accepted (then `in` falls back to a linear scan),
    so the function never returns a wrong answer, only a slower one.
    """
    return ip in blocklist


# ---------------------------------------------------------------------------
# 3. Attack-signature search (all, possibly overlapping, occurrences)
# ---------------------------------------------------------------------------

def find_signature_bf(log, pattern, counter=None):
    """Corrected brute-force matcher with early exit on the first mismatch."""
    n, m = len(log), len(pattern)
    hits = []
    if m == 0 or m > n:          # empty pattern / pattern longer than log
        return hits
    for i in range(n - m + 1):   # last alignment is i = n - m
        j = 0
        while j < m:
            if counter is not None:
                counter["cmp"] += 1
            if log[i + j] != pattern[j]:
                break
            j += 1
        if j == m:               # all m characters matched
            hits.append(i)
    return hits


def _failure_table(pattern):
    """KMP failure function: fail[q] = length of the longest proper prefix of
    pattern[:q+1] that is also a suffix of it."""
    fail = [0] * len(pattern)
    k = 0
    for q in range(1, len(pattern)):
        while k > 0 and pattern[q] != pattern[k]:
            k = fail[k - 1]
        if pattern[q] == pattern[k]:
            k += 1
        fail[q] = k
    return fail


def find_signature(log, pattern, counter=None):
    """Production matcher (Knuth-Morris-Pratt), same output as find_signature_bf.

    The log pointer never moves backwards, so no log character is re-compared
    after a partial match: at most 2n comparisons for the scan plus O(m) for the
    failure table, i.e. O(n + m) instead of O(n * m).
    """
    n, m = len(log), len(pattern)
    hits = []
    if m == 0 or m > n:
        return hits
    fail = _failure_table(pattern)
    k = 0                                   # characters of pattern matched so far
    for i, ch in enumerate(log):
        while True:
            if counter is not None:
                counter["cmp"] += 1
            if ch == pattern[k]:
                k += 1
                break
            if k == 0:
                break
            k = fail[k - 1]                 # fall back without moving i
        if k == m:
            hits.append(i - m + 1)
            k = fail[m - 1]                 # allow overlapping matches
    return hits


# ---------------------------------------------------------------------------
# 4. Closest pair of login locations
# ---------------------------------------------------------------------------

def closest_logins_bf(events, counter=None):
    """Corrected brute force (Part b form): every ordered pair i != j, with sqrt.

    Returns ((i, j), distance) with i < j, or (None, math.inf) if fewer than
    two events.  Ties resolve to the lexicographically smallest (i, j).
    """
    min_dist = math.inf
    pair = None
    for i in range(len(events)):
        for j in range(len(events)):
            if i == j:
                continue
            if counter is not None:
                counter["dist"] += 1
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            if d < min_dist:
                min_dist = d
                pair = (i, j)
    return pair, min_dist


def closest_logins_pairs(events, counter=None):
    """Intermediate step: unordered pairs only (j > i) and squared distances."""
    n = len(events)
    best_d2 = math.inf
    pair = None
    for i in range(n - 1):
        xi, yi = events[i]
        for j in range(i + 1, n):
            if counter is not None:
                counter["dist"] += 1
            dx = xi - events[j][0]
            dy = yi - events[j][1]
            d2 = dx * dx + dy * dy
            if d2 < best_d2:
                best_d2 = d2
                pair = (i, j)
    return pair, (math.sqrt(best_d2) if pair else math.inf)


def closest_logins(events, counter=None):
    """Production closest pair: sort by x, sweep, prune, compare squared distances.

    1. Self-pairs and repeated pairs are never generated (b > a).
    2. Squared distances are compared; one sqrt is taken at the end.
    3. Events are visited in x order; once dx^2 exceeds the best squared
       distance so far, no later event can be closer, so the inner loop stops.
    Output is identical to closest_logins_bf (same tie-break: smallest (i, j)).
    """
    n = len(events)
    if n < 2:
        return None, math.inf
    order = sorted(range(n), key=lambda k: events[k][0])   # O(n log n)
    best_d2 = math.inf
    best_pair = None
    for a in range(n - 1):
        i = order[a]
        xi, yi = events[i]
        for b in range(a + 1, n):
            j = order[b]
            xj, yj = events[j]
            dx = xj - xi
            dx2 = dx * dx
            if dx2 > best_d2:            # prune: every later point is farther in x
                break
            if counter is not None:
                counter["dist"] += 1
            dy = yj - yi
            d2 = dx2 + dy * dy
            pair = (i, j) if i < j else (j, i)
            if d2 < best_d2 or (d2 == best_d2 and pair < best_pair):
                best_d2 = d2
                best_pair = pair
    return best_pair, math.sqrt(best_d2)


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------

_results = {"pass": 0, "fail": 0}


def check(name, actual, expected):
    """Print one test line and record the result."""
    ok = actual == expected
    _results["pass" if ok else "fail"] += 1
    print("  [%s] %-38s -> %s" % ("PASS" if ok else "FAIL", name, actual))
    if not ok:
        print("         expected %s" % (expected,))


def close_pair(result):
    """Round the distance so float results can be compared in tests."""
    pair, dist = result
    return pair, (round(dist, 4) if dist != math.inf else dist)


def run_tests():
    """Check every function on the task data, boundary cases and random data."""
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    log, pattern = "FAILFAIXFAIL", "FAIL"
    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    sorted_alerts = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]

    print("1. sort_alerts")
    check("task data (insertion)", sort_alerts_bf(list(alerts)), sorted_alerts)
    check("task data (Timsort)", sort_alerts(list(alerts)), sorted_alerts)
    check("equal severities keep order", sort_alerts([("B1", 4), ("B2", 4), ("B3", 4)]),
          [("B1", 4), ("B2", 4), ("B3", 4)])
    check("empty list", sort_alerts([]), [])
    check("single alert", sort_alerts([("Z", 7)]), [("Z", 7)])
    check("already sorted", sort_alerts(list(sorted_alerts)), sorted_alerts)
    check("reverse order", sort_alerts([("C1", 1), ("C2", 2), ("C3", 3)]),
          [("C3", 3), ("C2", 2), ("C1", 1)])

    print("2. is_blocked")
    index = build_blocklist(blocklist)
    check("task queries (linear)", [is_blocked_bf(blocklist, q) for q in queries],
          [True, True, False])
    check("task queries (hash set)", [is_blocked(index, q) for q in queries],
          [True, True, False])
    check("empty blocklist", is_blocked(build_blocklist([]), "10.0.0.5"), False)
    check("empty blocklist (linear)", is_blocked_bf([], "10.0.0.5"), False)
    check("last entry", is_blocked(index, "172.16.4.2"), True)
    check("prefix is not a match", is_blocked(index, "10.0.0.50"), False)

    print("3. find_signature")
    check("task data", find_signature(log, pattern), [0, 8])
    check("task data (brute force)", find_signature_bf(log, pattern), [0, 8])
    check("pattern at very end", find_signature("XXXXFAIL", "FAIL"), [4])
    check("pattern longer than log", find_signature("FAIL", "FAILURE"), [])
    check("pattern equals log", find_signature("FAIL", "FAIL"), [0])
    check("overlapping matches", find_signature("AAAA", "AA"), [0, 1, 2])
    check("last char mismatch only", find_signature("FAIX", "FAIL"), [])
    check("empty pattern", find_signature("FAIL", ""), [])
    check("empty log", find_signature("", "FAIL"), [])

    print("4. closest_logins")
    check("task data", close_pair(closest_logins(events)), ((0, 5), 1.4142))
    check("task data (brute force)", close_pair(closest_logins_bf(events)), ((0, 5), 1.4142))
    check("no events", closest_logins([]), (None, math.inf))
    check("one event", closest_logins([(1, 1)]), (None, math.inf))
    check("two events", close_pair(closest_logins([(0, 0), (3, 4)])), ((0, 1), 5.0))
    check("duplicate location", close_pair(closest_logins([(9, 9), (1, 1), (9, 9)])),
          ((0, 2), 0.0))

    print("5. optimised == corrected brute force (random data, 200 trials each)")
    rng = random.Random(2026)
    same_sort = same_sig = same_cp = same_blk = True
    for _ in range(200):
        a = [("X%d" % k, rng.randint(1, 10)) for k in range(rng.randint(0, 60))]
        same_sort &= sort_alerts(list(a)) == sort_alerts_bf(list(a))
        s = "".join(rng.choice("AB") for _ in range(rng.randint(0, 80)))
        p = "".join(rng.choice("AB") for _ in range(rng.randint(1, 5)))
        same_sig &= find_signature(s, p) == find_signature_bf(s, p)
        pts = [(rng.randint(0, 30), rng.randint(0, 30)) for _ in range(rng.randint(0, 40))]
        same_cp &= closest_logins(pts) == closest_logins_bf(pts)
        bl = ["10.0.%d.%d" % (rng.randint(0, 3), rng.randint(0, 9)) for _ in range(rng.randint(0, 15))]
        q = "10.0.%d.%d" % (rng.randint(0, 3), rng.randint(0, 9))
        same_blk &= is_blocked(build_blocklist(bl), q) == is_blocked_bf(bl, q)
    check("sort_alerts", same_sort, True)
    check("is_blocked", same_blk, True)
    check("find_signature", same_sig, True)
    check("closest_logins (ties included)", same_cp, True)

    print("\nRESULT: %d passed, %d failed" % (_results["pass"], _results["fail"]))
    return _results["fail"] == 0


# ---------------------------------------------------------------------------
# Measurements for Part (d)
# ---------------------------------------------------------------------------

def measure(sizes=(1000, 2000, 4000, 8000), seed=7):
    """Print distance computations and comparison counts (Part d)."""
    rng = random.Random(seed)
    print("\nclosest_logins: distance computations (points uniform in 1000 x 1000 km)")
    print("%6s %12s %12s %10s %8s %9s %9s" % ("n", "bf n(n-1)", "pairs j>i",
                                              "optimised", "ratio", "bf sec", "opt sec"))
    for n in sizes:
        pts = [(rng.uniform(0, 1000), rng.uniform(0, 1000)) for _ in range(n)]
        c1, c2, c3 = {"dist": 0}, {"dist": 0}, {"dist": 0}
        t = time.perf_counter(); r1 = closest_logins_bf(pts, c1); t1 = time.perf_counter() - t
        closest_logins_pairs(pts, c2)
        t = time.perf_counter(); r3 = closest_logins(pts, c3); t3 = time.perf_counter() - t
        assert r1 == r3
        print("%6d %12d %12d %10d %7.0fx %9.2f %9.3f" % (n, c1["dist"], c2["dist"], c3["dist"],
                                                      c1["dist"] / c3["dist"], t1, t3))

    print("\nsort_alerts: severity comparisons (severity 1..10)")
    print("%6s %16s %16s %14s %14s" % ("n", "ins. nearly", "ins. random",
                                       "Timsort nearly", "Timsort random"))
    for n in (1000, 2000, 5000):
        rand = [("R%d" % k, rng.randint(1, 10)) for k in range(n)]
        nearly = sorted(rand, key=lambda a: -a[1])
        for _ in range(n // 50):             # 2% of alerts arrive out of place
            p = rng.randrange(n)
            nearly[p] = (nearly[p][0], rng.randint(1, 10))
        row = []
        for data in (nearly, rand):
            c = {"cmp": 0}
            sort_alerts_bf(list(data), c)
            row.append(c["cmp"])
        for data in (nearly, rand):
            c = [0]

            def cmp(x, y):
                c[0] += 1
                return y[1] - x[1]
            sorted(data, key=cmp_to_key(cmp))
            row.append(c[0])
        print("%6d %16d %16d %14d %14d" % (n, *row))

    print("\nfind_signature: character comparisons")
    for name, text, pat in (("worst case A..AB / A^9B", "A" * 100000, "A" * 9 + "B"),
                            ("random log ACGT / 10 chars",
                             "".join(rng.choice("ACGT") for _ in range(100000)), "ACGTACGTAC")):
        c1, c2 = {"cmp": 0}, {"cmp": 0}
        assert find_signature_bf(text, pat, c1) == find_signature(text, pat, c2)
        print("  %-28s n=%d m=%d  brute force=%d  KMP=%d" % (name, len(text), len(pat),
                                                            c1["cmp"], c2["cmp"]))

    print("\nis_blocked: blocklist of 2,000 IPs, 5,000 queries (half blocked)")
    bl = ["10.%d.%d.%d" % (k // 65536, (k // 256) % 256, k % 256) for k in range(2000)]
    qs = [rng.choice(bl) if k % 2 else "192.168.%d.%d" % (k % 256, k // 256) for k in range(5000)]
    c = {"cmp": 0}
    for q in qs:
        is_blocked_bf(bl, q, c)
    print("  linear search comparisons = %d   hash-set probes = %d (+%d to build)"
          % (c["cmp"], len(qs), len(bl)))


if __name__ == "__main__":
    if not run_tests():
        raise SystemExit(1)          # non-zero exit status if any test fails
