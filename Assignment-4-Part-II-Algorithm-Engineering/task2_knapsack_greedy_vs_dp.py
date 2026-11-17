"""Task 2 - Greedy (fractional) vs Dynamic Programming (0/1) knapsack.

Items are (item_id, weight, value) with integer weights.
Every solver returns the items/fractions chosen, not only the value,
and fills a counter dict so the work done can be compared.
"""
import random
from functools import cmp_to_key


# ------------------------------------------------------------ algorithms
def sort_by_ratio(items, counter):
    """Sort by value/weight, highest first, counting comparisons."""
    def compare(a, b):
        counter["comparisons"] += 1
        return (b[2] * a[1]) - (a[2] * b[1])     # cross-multiplied ratios
    return sorted(items, key=cmp_to_key(compare))


def fractional_knapsack(items, capacity, counter, log=None):
    """Solution A: greedy by ratio, the last item may be split."""
    remaining, total, chosen = capacity, 0.0, []
    for item_id, weight, value in sort_by_ratio(items, counter):
        if remaining == 0:
            break
        counter["steps"] += 1
        take = min(1.0, remaining / weight)
        remaining -= take * weight
        total += take * value
        chosen.append((item_id, take))
        if log is not None:
            log.append("take %s x%.2f -> value %.1f, left %g"
                       % (item_id, take, total, remaining))
    counter["memory_cells"] = len(items)
    return total, chosen


def greedy_01(items, capacity, counter, log=None):
    """Same ratio intuition applied to 0/1 items: take whole items only."""
    remaining, total, chosen = capacity, 0, []
    for item_id, weight, value in sort_by_ratio(items, counter):
        counter["steps"] += 1
        if weight <= remaining:
            remaining -= weight
            total += value
            chosen.append(item_id)
            verdict = "take"
        else:
            verdict = "skip (needs %d, left %d)" % (weight, remaining)
        if log is not None:
            log.append("%s w=%d v=%d: %s" % (item_id, weight, value, verdict))
    counter["memory_cells"] = len(items)
    return total, chosen


def knapsack_01_dp(items, capacity, counter):
    """Solution B: V[i][c] = best value from the first i items, capacity c."""
    n = len(items)
    V = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        _, weight, value = items[i - 1]
        for c in range(capacity + 1):
            counter["steps"] += 1
            V[i][c] = V[i - 1][c]
            if weight <= c and value + V[i - 1][c - weight] > V[i][c]:
                V[i][c] = value + V[i - 1][c - weight]
    chosen, c = [], capacity
    for i in range(n, 0, -1):                    # reconstruction
        if V[i][c] != V[i - 1][c]:
            chosen.append(items[i - 1][0])
            c -= items[i - 1][1]
    counter["memory_cells"] = (n + 1) * (capacity + 1)
    return V[n][capacity], chosen[::-1]


def new_counter():
    return {"comparisons": 0, "steps": 0, "memory_cells": 0}


# ------------------------------------------------------------ reporting
def run_case(title, items, capacity):
    print(title + "  capacity = %d" % capacity)
    print("  items:", ", ".join("%s(w%d,v%d,r%.2f)" % (i, w, v, v / w)
                                for i, w, v in items))
    log = []
    total, chosen = fractional_knapsack(items, capacity, new_counter(), log)
    print("  A fractional greedy:")
    for line in log:
        print("    " + line)
    print("    value = %.1f" % total)
    log = []
    g_total, g_chosen = greedy_01(items, capacity, new_counter(), log)
    print("  greedy ratio rule on 0/1 items:")
    for line in log:
        print("    " + line)
    print("    value = %d  items = %s" % (g_total, g_chosen))
    d_total, d_chosen = knapsack_01_dp(items, capacity, new_counter())
    print("  B 0/1 DP: value = %d  items = %s" % (d_total, d_chosen))
    return g_total, d_total


def comparison():
    print("2.3  Work and memory (random items, weights 1..60)")
    print("  %4s %5s | %8s %6s | %9s %9s" % ("n", "W", "greedy", "cells",
                                              "DP steps", "DP cells"))
    rng = random.Random(11)
    for n, cap in ((20, 200), (50, 500), (100, 1000), (200, 2000)):
        items = [("I%d" % k, rng.randint(1, 60), rng.randint(1, 100))
                 for k in range(n)]
        cg, cd = new_counter(), new_counter()
        greedy_01(items, cap, cg)
        knapsack_01_dp(items, cap, cd)
        print("  %4d %5d | %8d %6d | %9d %9d" % (n, cap, cg["comparisons"] +
              cg["steps"], cg["memory_cells"], cd["steps"], cd["memory_cells"]))
    print("  Quality over 300 random 0/1 instances (n=30, W=300):")
    worst, total_ratio, optimal = 1.0, 0.0, 0
    for _ in range(300):
        items = [("I%d" % k, rng.randint(1, 60), rng.randint(1, 100))
                 for k in range(30)]
        g, _ = greedy_01(items, 300, new_counter())
        d, _ = knapsack_01_dp(items, 300, new_counter())
        worst = min(worst, g / d)
        total_ratio += g / d
        optimal += (g == d)
    print("    greedy/optimum: average %.4f, worst %.4f, optimal in %d/300"
          % (total_ratio / 300, worst, optimal))
    trap = [("A", 1, 2), ("B", 100, 100)]
    g, gi = greedy_01(trap, 100, new_counter())
    d, di = knapsack_01_dp(trap, 100, new_counter())
    print("  No guarantee: A(w1,v2) B(w100,v100), W=100")
    print("    greedy %s = %d, DP %s = %d  (%.0f%% of optimum)"
          % (gi, g, di, d, 100 * g / d))
    best_single = max(v for _, w, v in trap if w <= 100)
    print("    max(greedy, best single item) = %d  (>= 1/2 optimum)"
          % max(g, best_single))


NORMAL = [("P1", 4, 40), ("P2", 3, 24), ("P3", 5, 30), ("P4", 2, 8)]
BREAK = [("X", 6, 30), ("Y", 5, 24), ("Z", 5, 24)]


def main(part="ALL"):
    if part in ("A", "ALL"):
        run_case("2.1  Normal case", NORMAL, 12)
    if part in ("B", "ALL"):
        g, d = run_case("2.2  Breaking the greedy intuition", BREAK, 10)
        print("  greedy reaches %d of %d (%.1f%%)" % (g, d, 100 * g / d))
    if part in ("C", "ALL"):
        comparison()


if __name__ == "__main__":
    main("ALL")
