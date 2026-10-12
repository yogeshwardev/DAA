import math
import random
import time
from datetime import datetime

SEED = 5067


def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def between(a, b, c):
    return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])


def brute_force_hull(points):
    pts = sorted(set(points))
    n = len(pts)
    edges = []
    tests = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            pos = neg = False
            ok = True
            for k in range(n):
                if k == i or k == j:
                    continue
                tests += 1
                c = cross(pts[i], pts[j], pts[k])
                if c > 0:
                    pos = True
                elif c < 0:
                    neg = True
                elif not between(pts[i], pts[j], pts[k]):
                    ok = False
                    break
                if pos and neg:
                    ok = False
                    break
            if ok:
                edges.append((i, j))
    verts = sorted({v for e in edges for v in e})
    hull = [pts[v] for v in verts]
    cx = sum(p[0] for p in hull) / len(hull)
    cy = sum(p[1] for p in hull) / len(hull)
    hull.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))
    return hull, [(pts[i], pts[j]) for i, j in edges], tests, n


def set_a():
    rng = random.Random(SEED)
    pts = []
    for k in range(6):
        ang = math.radians(60 * k + 15)
        pts.append((round(50 + 48 * math.cos(ang)), round(50 + 48 * math.sin(ang))))
    while len(pts) < 36:
        x, y = rng.randint(20, 80), rng.randint(20, 80)
        if (x - 50) ** 2 + (y - 50) ** 2 <= 30 ** 2:
            pts.append((x, y))
    return pts


def set_b():
    corners = [(0, 0), (20, 0), (20, 20), (0, 20)]
    mids = [(10, 0), (20, 10), (10, 20), (0, 10), (5, 0), (20, 15)]
    inner = [(x, y) for x in (5, 10, 15) for y in (5, 10, 15)]
    return corners + mids + inner + [(0, 0), (20, 20), (10, 1), (19, 19)]


def header(title):
    print("=" * 74)
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 74)


def main():
    header("Q5 - BRUTE-FORCE CONVEX HULL")
    csv_lines = []
    for name, pts in (("A: boundary and interior points", set_a()), ("B: designed (collinear, duplicates)", set_b())):
        hull, edges, tests, n = brute_force_hull(pts)
        print("Set %s" % name)
        print("  points given: %d, distinct: %d, orientation tests: %d, accepted edges: %d" %
              (len(pts), n, tests, len(edges)))
        print("  hull vertices (counter-clockwise):", hull)
        csv_lines.append("CSV,q5set,%s,%d,%d,%d,%d" % (name[0], len(pts), n, tests, len(hull)))
    line_pts = [(i, 2 * i) for i in range(8)]
    hull, edges, tests, n = brute_force_hull(line_pts)
    print("Set C: all points collinear -> hull vertices:", hull, "(tests %d)" % tests)
    print()
    rng = random.Random(SEED)
    print("%8s%12s%18s%18s%12s%12s" % ("n", "pairs", "tests (random)", "tests (circle)", "hull (rand)", "time (s)"))
    for n in (10, 20, 40, 80, 160, 320):
        pts = set()
        while len(pts) < n:
            pts.add((rng.randint(0, 1000), rng.randint(0, 1000)))
        t0 = time.perf_counter()
        hull, e, tests, m = brute_force_hull(list(pts))
        t = time.perf_counter() - t0
        circ = [(round(5000 + 4000 * math.cos(2 * math.pi * k / n)), round(5000 + 4000 * math.sin(2 * math.pi * k / n)))
                for k in range(n)]
        h2, e2, tests2, m2 = brute_force_hull(circ)
        print("%8d%12d%18d%18d%12d%12.4f" % (n, n * (n - 1) // 2, tests, tests2, len(hull), t))
        csv_lines.append("CSV,q5,%d,%d,%d,%d,%d,%.5f" % (n, n * (n - 1) // 2, tests, tests2, len(hull), t))
    print()
    for line in csv_lines:
        print(line)


if __name__ == "__main__":
    main()
