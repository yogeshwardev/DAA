# KartIQ - Module 2 : Live Seller Leaderboard - Quick Sort pivot study
import random


def partition(a, lo, hi, cnt, trace=False):
    """Hoare-style partition with a[lo] as pivot (Levitin's version)."""
    p = a[lo]
    i, j = lo + 1, hi
    while True:
        while i <= hi:                      # scan right for element >= pivot
            cnt[0] += 1
            if a[i] >= p:
                break
            i += 1
        while True:                         # scan left for element <= pivot
            cnt[0] += 1
            if a[j] <= p:
                break
            j -= 1
        if i >= j:
            break
        if trace:
            print("   i=%d (%d) j=%d (%d) -> swap   %s" % (i, a[i], j, a[j], a))
        a[i], a[j] = a[j], a[i]
        if trace:
            print("                         after %s" % a)
        i += 1
        j -= 1
    if trace:
        print("   i=%d j=%d crossed -> swap pivot with a[%d]=%d" % (i, j, j, a[j]))
    a[lo], a[j] = a[j], a[lo]
    return j


def median_of_three(a, lo, hi, cnt):
    """Move the median of a[lo], a[mid], a[hi] to a[lo] so it becomes the pivot."""
    mid = (lo + hi) // 2
    cnt[0] += 3
    trio = sorted([(a[lo], lo), (a[mid], mid), (a[hi], hi)])
    m = trio[1][1]
    a[lo], a[m] = a[m], a[lo]


def quick_sort(a, strategy, cnt):
    """Iterative quick sort (explicit stack) so deep worst cases do not crash.
    Returns the maximum recursion depth the recursive version would reach."""
    stack, max_depth = [(0, len(a) - 1, 1)], 0
    while stack:
        lo, hi, d = stack.pop()
        if lo >= hi:
            continue
        max_depth = max(max_depth, d)
        if strategy == "median3":
            median_of_three(a, lo, hi, cnt)
        elif strategy == "middle":
            m = (lo + hi) // 2
            a[lo], a[m] = a[m], a[lo]
        elif strategy == "random":
            r = random.randint(lo, hi)
            a[lo], a[r] = a[r], a[lo]
        s = partition(a, lo, hi, cnt)
        stack.append((lo, s - 1, d + 1))
        stack.append((s + 1, hi, d + 1))
    return max_depth


scores = [42, 17, 63, 8, 55, 29]
print("One partition step, pivot = first element = 42")
a, c = list(scores), [0]
s = partition(a, 0, len(a) - 1, c, trace=True)
print("Result %s  pivot index=%d  comparisons=%d" % (a, s, c[0]))
print("Left part %s  pivot [42]  right part %s\n" % (a[:s], a[s + 1:]))

def nearly_sorted(n, changed=10):
    """Sorted leaderboard in which only a few scores changed since last refresh."""
    a = sorted(random.sample(range(10 * n), n))
    for _ in range(changed):
        a[random.randrange(n)] = random.randrange(10 * n)
    return a


STRATS = ("first", "median3", "middle", "random")
print("Comparisons (max depth) on NEARLY SORTED scores, 10 scores changed")
print("%6s %10s %16s %16s %16s %16s" % ("n", "n(n-1)/2", *STRATS))
random.seed(5)
for n in (1000, 2000, 4000):
    base = nearly_sorted(n)
    row = []
    for strat in STRATS:
        arr, cnt = list(base), [0]
        depth = quick_sort(arr, strat, cnt)
        assert arr == sorted(base)
        row.append("%9d (%4d)" % (cnt[0], depth))
    print("%6d %10d %s" % (n, n * (n - 1) // 2, " ".join(row)))

n = 100_000
print("\n100,000 sellers, first pivot (estimate) : n(n-1)/2 = %d" % (n * (n - 1) // 2))
for strat in ("middle", "random"):
    arr, cnt = nearly_sorted(n), [0]
    depth = quick_sort(arr, strat, cnt)
    print("100,000 sellers, %-6s pivot (measured): %d  (max depth %d)" % (strat, cnt[0], depth))
