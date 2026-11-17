# KartIQ - Module 1 : Nightly Order Consolidation using (stable) Merge Sort
# Orders are (timestamp, order_id). Equal timestamps must keep arrival order.
import math
import random

comparisons = 0


def show(lst):
    return "[" + ", ".join("%d:%s" % (t, o) for t, o in lst) + "]"


def merge(left, right):
    """Combine step: merge two sorted lists. '<=' takes the LEFT element on a
    tie, so the order that arrived first stays first (stable)."""
    global comparisons
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        comparisons += 1
        if left[i][0] <= right[j][0]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def merge_sort(orders, depth=0, trace=False):
    if len(orders) <= 1:                      # base case
        return orders
    mid = (len(orders) + 1) // 2              # divide
    if trace:
        print("  " * depth + "split " + show(orders[:mid]) + " | " + show(orders[mid:]))
    left = merge_sort(orders[:mid], depth + 1, trace)    # conquer
    right = merge_sort(orders[mid:], depth + 1, trace)
    merged = merge(left, right)                           # combine
    if trace:
        print("  " * depth + "merge " + show(left) + " + " + show(right) + " -> " + show(merged))
    return merged


orders = [(105, "O1"), (102, "O2"), (105, "O3"), (101, "O4"), (102, "O5"), (103, "O6")]
print("Input :", show(orders))
result = merge_sort(orders, trace=True)
print("Output:", show(result))
print("Comparisons on sample:", comparisons)
print("O2 before O5 (both 102):", result.index((102, "O2")) < result.index((102, "O5")))
print("O1 before O3 (both 105):", result.index((105, "O1")) < result.index((105, "O3")))

# check the worst-case formula n*ceil(log2 n) - 2^ceil(log2 n) + 1 on random data
for n in (1000, 10000, 100000):
    comparisons = 0
    data = [(random.randint(0, 86399), "X%d" % k) for k in range(n)]
    out = merge_sort(data)
    assert out == sorted(data, key=lambda x: x[0])          # Python sort is stable too
    k = math.ceil(math.log2(n))
    print("n=%6d comparisons=%8d  worst bound=%8d  n*log2(n)=%9.0f"
          % (n, comparisons, n * k - 2 ** k + 1, n * math.log2(n)))

n = 10_000_000
k = math.ceil(math.log2(n))
print("10,000,000 orders: worst-case comparisons = %d (about %.2e)" % (n * k - 2 ** k + 1, n * k - 2 ** k + 1))
print("levels of recursion = %d" % k)
