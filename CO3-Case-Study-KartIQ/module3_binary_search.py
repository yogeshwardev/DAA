# KartIQ - Module 3 : Order Lookup using Binary Search (first occurrence)
import math
import random


def first_order(arr, key, trace=False):
    """Return the index of the FIRST element whose timestamp == key, else -1.
    On a match we remember it and keep searching the left half."""
    lo, hi, ans, steps = 0, len(arr) - 1, -1, 0
    while lo <= hi:
        mid = (lo + hi) // 2
        steps += 1
        t = arr[mid][0] if isinstance(arr[mid], tuple) else arr[mid]
        old_lo, old_hi = lo, hi
        if t == key:
            ans, hi, act = mid, mid - 1, "match, record and go left"
        elif t < key:
            lo, act = mid + 1, "go right"
        else:
            hi, act = mid - 1, "go left"
        if trace:
            print("   lo=%d hi=%d mid=%d A[mid]=%d -> %s" % (old_lo, old_hi, mid, t, act))
    return ans, steps


consolidated = [(101, "O4"), (102, "O2"), (102, "O5"), (103, "O6"), (105, "O1"), (105, "O3")]
print("Sorted list from Module 1:", consolidated)
for key in (102, 105, 104):
    print("Search timestamp", key)
    idx, steps = first_order(consolidated, key, trace=True)
    print("   result:", consolidated[idx] if idx >= 0 else "not found", " (comparisons = %d)" % steps)

print("\nWhy sorting is essential - same search on the UNSORTED input:")
unsorted = [(105, "O1"), (102, "O2"), (105, "O3"), (101, "O4"), (102, "O5"), (103, "O6")]
idx, _ = first_order(unsorted, 101)
print("   search 101 ->", unsorted[idx] if idx >= 0 else "not found (but O4 has 101!)")

n = 10_000_000
timestamps = range(n)                   # a sorted list of 10,000,000 keys (no memory used)
worst = 0
for key in [0, n - 1, -5, n + 5] + [random.randrange(n) for _ in range(2000)]:
    _, steps = first_order(timestamps, key)
    worst = max(worst, steps)
print("\n10,000,000 orders: floor(log2 n) + 1 = %d" % (math.floor(math.log2(n)) + 1))
print("Largest number of comparisons measured over 2,004 searches = %d" % worst)
