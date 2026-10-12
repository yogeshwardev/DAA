import random
import time
from datetime import datetime

SEED = 5067


def selection_sort(a):
    a = a[:]
    n = len(a)
    comps = swaps = 0
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            comps += 1
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
            swaps += 1
    return a, comps, swaps


def bubble_sort(a):
    a = a[:]
    n = len(a)
    comps = swaps = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comps += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return a, comps, swaps


def insertion_sort(a):
    a = a[:]
    n = len(a)
    comps = moves = 0
    for i in range(1, n):
        v = a[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if a[j] > v:
                a[j + 1] = a[j]
                moves += 1
                j -= 1
            else:
                break
        a[j + 1] = v
    return a, comps, moves


ALGOS = [("Selection sort", selection_sort), ("Bubble sort", bubble_sort), ("Insertion sort", insertion_sort)]


def make(kind, n, rng):
    if kind == "random":
        return rng.sample(range(1, 10 * n), n)
    if kind == "sorted":
        return sorted(rng.sample(range(1, 10 * n), n))
    if kind == "reversed":
        return sorted(rng.sample(range(1, 10 * n), n), reverse=True)
    if kind == "nearly sorted 95%":
        base = sorted(rng.sample(range(1, 10 * n), n))
        k = n // 20
        keep, new = base[:n - k], [rng.randint(1, 10 * n) for _ in range(k)]
        return keep + new
    if kind == "sorted + batch of 20":
        base = sorted(rng.sample(range(1, 10 * n), n - 20))
        return base + [rng.randint(1, 10 * n) for _ in range(20)]
    if kind == "few distinct scores":
        return [rng.randint(1, 5) for _ in range(n)]


def predict(kind, n):
    full = n * (n - 1) // 2
    if kind == "sorted":
        return {"Selection sort": (full, 0), "Bubble sort": (n - 1, 0), "Insertion sort": (n - 1, 0)}
    if kind == "reversed":
        return {"Selection sort": (full, n // 2), "Bubble sort": (full, full), "Insertion sort": (full, full)}
    if kind == "random":
        return {"Selection sort": (full, n - 1), "Bubble sort": (full, full // 2), "Insertion sort": (full // 2, full // 2)}
    return None


def header(title):
    print("=" * 74)
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 74)


def main():
    header("Q1 - SELECTION, BUBBLE AND INSERTION SORT")
    rng = random.Random(SEED)
    n = 2000
    print("n = %d, seed = %d\n" % (n, SEED))
    print("PREDICTIONS (made before running), comparisons / swaps-or-moves:")
    for kind in ("sorted", "reversed", "random"):
        p = predict(kind, n)
        print("  %-20s" % kind, "; ".join("%s %s" % (a.split()[0], p[a]) for a in p))
    print("  nearly sorted 95%    selection unchanged; bubble needs passes until the last displaced item is placed;")
    print("                       insertion should do far fewer moves than on random data")
    print()
    kinds = ["random", "sorted", "reversed", "nearly sorted 95%", "sorted + batch of 20", "few distinct scores"]
    print("%-22s%-16s%14s%14s%11s%9s" % ("dataset", "algorithm", "comparisons", "swaps/moves", "time(ms)", "sorted"))
    csv_lines = []
    for kind in kinds:
        data = make(kind, n, rng)
        for name, fn in ALGOS:
            t0 = time.perf_counter()
            out, c, s = fn(data)
            ms = (time.perf_counter() - t0) * 1000
            ok = out == sorted(data)
            print("%-22s%-16s%14d%14d%11.2f%9s" % (kind, name, c, s, ms, ok))
            csv_lines.append("CSV,q1,%s,%d,%s,%d,%d,%.3f" % (kind, n, name, c, s, ms))
    print()
    print("GROWTH WITH n (nearly sorted 95% and random):")
    print("%-22s%8s%-16s%14s%14s" % ("dataset", "n", "  algorithm", "comparisons", "swaps/moves"))
    for kind in ("nearly sorted 95%", "random"):
        for m in (500, 1000, 2000, 4000):
            data = make(kind, m, rng)
            for name, fn in ALGOS:
                out, c, s = fn(data)
                print("%-22s%8d  %-14s%14d%14d" % (kind, m, name, c, s))
                csv_lines.append("CSV,q1,%s,%d,%s,%d,%d,0" % (kind, m, name, c, s))
    print()
    for line in csv_lines:
        print(line)


if __name__ == "__main__":
    main()
