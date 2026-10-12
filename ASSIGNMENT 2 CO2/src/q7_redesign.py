import random
import time
from datetime import datetime

SEED = 5067


def exhaustive_count(items, cap):
    n = len(items)
    best = 0
    for mask in range(1 << n):
        w = v = 0
        for i in range(n):
            if mask >> i & 1:
                w += items[i][1]
                v += items[i][2]
        if w <= cap and v > best:
            best = v
    return best, 1 << n


def pruned_search(items, cap, use_bound=True):
    order = sorted(items, key=lambda it: it[2] / it[1], reverse=True)
    n = len(order)
    suffix = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] + order[i][2]
    best = 0
    nodes = 0
    stack = [(0, 0, 0)]
    while stack:
        i, w, v = stack.pop()
        nodes += 1
        if v > best:
            best = v
        if i == n:
            continue
        if use_bound:
            room = cap - w
            ub = v + min(suffix[i], room * order[i][2] / order[i][1])
            if ub <= best:
                continue
        stack.append((i + 1, w, v))
        if w + order[i][1] <= cap:
            stack.append((i + 1, w + order[i][1], v + order[i][2]))
    return best, nodes


def make_items(n, rng, kind="random"):
    items = []
    for i in range(n):
        w = rng.randint(5, 50)
        if kind == "random":
            v = rng.randint(10, 100)
        elif kind == "correlated":
            v = w + 10
        else:
            w = 2 * rng.randint(3, 25)
            v = w
        items.append(("P%d" % (i + 1), w, v))
    return items


def header(title):
    print("=" * 74)
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 74)


def main():
    header("Q7 - REDESIGN OF THE EXHAUSTIVE SEARCH (PRUNED SEARCH)")
    print("PREDICTION (made before running): the number of nodes visited will be a very small fraction of 2^n")
    print("on random instances, and the saving will shrink on strongly correlated instances where value is")
    print("almost proportional to weight. If every item has the same value density and the capacity cannot be")
    print("filled exactly, the bound should never be able to cut anything, and the search should lose its advantage.")
    print()
    csv_lines = []
    for kind in ("random", "correlated", "equal density and odd capacity"):
        rng = random.Random(SEED)
        print("Instance type: %s (capacity = 40 percent of total weight)" % kind)
        print("%5s%14s%14s%14s%12s%11s%11s%7s" % ("n", "exhaustive", "feasibility", "feas+bound", "best value",
                                                 "t exh (s)", "t pruned", "same"))
        sizes = (12, 16, 20, 22, 24) if kind.startswith("equal") else (12, 16, 20, 22, 24, 28, 32, 36, 40)
        for n in sizes:
            items = make_items(n, rng, kind)
            cap = int(0.4 * sum(i[1] for i in items))
            if kind.startswith("equal") and cap % 2 == 0:
                cap -= 1
            if n <= 22:
                t0 = time.perf_counter()
                bv, cand = exhaustive_count(items, cap)
                t_ex = time.perf_counter() - t0
            else:
                bv, cand, t_ex = None, 1 << n, None
            v1, n1 = pruned_search(items, cap, False) if n <= 24 else (None, None)
            t0 = time.perf_counter()
            v2, n2 = pruned_search(items, cap, True)
            t_p = time.perf_counter() - t0
            same = "-" if bv is None else str(bv == v2 and (v1 is None or v1 == v2))
            print("%5d%14d%14s%14d%12d%11s%11.4f%7s" % (n, cand, n1 if n1 is not None else "-", n2, v2,
                                                       "%.3f" % t_ex if t_ex is not None else "-", t_p, same))
            csv_lines.append("CSV,q7,%s,%d,%d,%s,%d,%d,%s,%.5f" % (kind, n, cand, n1 if n1 is not None else "", n2, v2,
                                                              "%.4f" % t_ex if t_ex is not None else "", t_p))
        print()
    for line in csv_lines:
        print(line)


if __name__ == "__main__":
    main()
