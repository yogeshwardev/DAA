import random
import time
from datetime import datetime

SEED = 5067


def closest_pair(points):
    n = len(points)
    best = None
    best_pair = None
    pairs = 0
    for i in range(n - 1):
        xi, yi = points[i]
        for j in range(i + 1, n):
            pairs += 1
            dx = xi - points[j][0]
            dy = yi - points[j][1]
            d = dx * dx + dy * dy
            if best is None or d < best:
                best = d
                best_pair = (i, j)
    return best_pair, best, pairs


def header(title):
    print("=" * 74)
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 74)


def main():
    header("Q4 - BRUTE-FORCE CLOSEST PAIR")
    rng = random.Random(SEED)
    print("%8s%18s%18s%18s%12s" % ("n", "n(n-1)/2", "pairs examined", "distance calcs", "time (s)"))
    rows = []
    csv_lines = []
    for n in (100, 200, 400, 800, 1600, 3200, 5000):
        pts = [(rng.randint(0, 100000), rng.randint(0, 100000)) for _ in range(n)]
        t0 = time.perf_counter()
        pair, d, pairs = closest_pair(pts)
        t = time.perf_counter() - t0
        rows.append((n, pairs, t))
        print("%8d%18d%18d%18d%12.4f" % (n, n * (n - 1) // 2, pairs, pairs, t))
        csv_lines.append("CSV,q4,%d,%d,%d,%d,%.5f" % (n, n * (n - 1) // 2, pairs, pairs, t))
    n, pairs, t = rows[-1]
    per_pair = t / pairs
    limit = 1.0
    n_lim = int((1 + (1 + 8 * limit / per_pair) ** 0.5) / 2)
    print()
    print("measured cost of one pair: %.0f ns" % (per_pair * 1e9))
    print("acceptable response time chosen: %.1f s -> brute force stays acceptable up to about n = %d drones"
          % (limit, n_lim))
    for target in (10000, 50000, 100000):
        print("  estimated time for n = %6d : %9.1f s" % (target, per_pair * target * (target - 1) / 2))
    csv_lines.append("CSV,q4lim,%.1f,%d" % (per_pair * 1e9, n_lim))
    print()
    for line in csv_lines:
        print(line)


if __name__ == "__main__":
    main()
