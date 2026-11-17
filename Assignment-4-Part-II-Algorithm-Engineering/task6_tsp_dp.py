"""Task 6 - Last-mile delivery route: TSP by Dynamic Programming (Held-Karp).

Location 0 is the distribution hub; 1..n are delivery locations.
DP[S][j] = minimum cost of a route that starts at the hub, visits exactly
the set S of delivery locations (bitmask) and ends at location j (j in S).
"""
import itertools
import random
import time
import tracemalloc

INF = float("inf")


# ------------------------------------------------------------ algorithms
def held_karp(cost):
    """Return (min_cost, route, states_evaluated). cost is a square matrix."""
    n = len(cost) - 1                         # delivery locations
    if n == 0:
        return 0, [0, 0], 0
    if any(len(row) != n + 1 for row in cost):
        raise ValueError("cost matrix must be square")
    full = (1 << n) - 1
    dp = {}
    parent = {}
    states = 0
    for j in range(1, n + 1):                 # base: hub -> j
        dp[(1 << (j - 1), j)] = cost[0][j]
        parent[(1 << (j - 1), j)] = 0
        states += 1
    for size in range(2, n + 1):
        for subset in itertools.combinations(range(1, n + 1), size):
            S = 0
            for loc in subset:
                S |= 1 << (loc - 1)
            for j in subset:                  # route over S ending at j
                prev_set = S & ~(1 << (j - 1))
                best, best_k = INF, None
                for k in subset:
                    if k == j:
                        continue
                    cand = dp[(prev_set, k)] + cost[k][j]
                    if cand < best:
                        best, best_k = cand, k
                dp[(S, j)], parent[(S, j)] = best, best_k
                states += 1
    best, last = INF, None
    for j in range(1, n + 1):                 # close the tour at the hub
        cand = dp[(full, j)] + cost[j][0]
        if cand < best:
            best, last = cand, j
    route, S, j = [0], full, last
    while j != 0:                             # follow parents backwards
        route.append(j)
        S, j = S & ~(1 << (j - 1)), parent[(S, j)]
    route.append(0)
    route = [0] + route[1:-1][::-1] + [0]
    return best, route, states


def brute_force(cost):
    """Exhaustive enumeration of every visiting order (reference)."""
    n = len(cost) - 1
    results = []
    for perm in itertools.permutations(range(1, n + 1)):
        tour = (0,) + perm + (0,)
        results.append((sum(cost[a][b] for a, b in zip(tour, tour[1:])), tour))
    return results


def route_cost(cost, route):
    return sum(cost[a][b] for a, b in zip(route, route[1:]))


def random_matrix(n, seed):
    rng = random.Random(seed)
    pts = [(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(n + 1)]
    return [[round(((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5) for x2, y2 in pts]
            for x1, y1 in pts]


# ------------------------------------------------------------ reporting
NAMES = ["Hub", "A", "B", "C", "D", "E", "F"]
COST = [  # Hub  A   B   C   D   E   F
    [0, 12, 10, 19, 8, 14, 22],    # Hub
    [12, 0, 7, 11, 15, 9, 13],     # A
    [10, 7, 0, 6, 13, 16, 18],     # B
    [19, 11, 6, 0, 17, 12, 7],     # C
    [8, 15, 13, 17, 0, 6, 16],     # D
    [14, 9, 16, 12, 6, 0, 10],     # E
    [22, 13, 18, 7, 16, 10, 0]]    # F


def show_route(route, names):
    return " -> ".join(names[k] for k in route)


def main(part="ALL"):
    if part in ("A", "ALL"):
        print("6.3  Cost matrix (symmetric)")
        print("       " + "".join("%5s" % x for x in NAMES))
        for name, row in zip(NAMES, COST):
            print("  %-4s " % name + "".join("%5d" % c for c in row))
        best, route, states = held_karp(COST)
        print("  Optimal route : " + show_route(route, NAMES))
        print("  Visit order   :", ", ".join(NAMES[k] for k in route[1:-1]))
        legs = ["%s-%s %d" % (NAMES[a], NAMES[b], COST[a][b])
                for a, b in zip(route, route[1:])]
        print("  Legs          : " + ", ".join(legs[:4]))
        print("                  " + ", ".join(legs[4:]))
        print("  Minimum Travel Cost = %d   (DP states: %d)" % (best, states))
    if part in ("B", "ALL"):
        small = [row[:5] for row in COST[:5]]          # Hub + A, B, C, D
        print("6.4  Validation: Hub + A, B, C, D")
        tours = sorted(brute_force(small))
        seen = set()
        for c, tour in tours:
            key = min(tour, tour[::-1])                # tour and its reverse
            if key in seen:
                continue
            seen.add(key)
            print("  %3d  %s" % (c, show_route(tour, NAMES)))
        best, route, states = held_karp(small)
        print("  enumeration optimum = %d" % tours[0][0])
        print("  DP optimum          = %d  %s" % (best, show_route(route, NAMES)))
        print("  match:", best == tours[0][0] == route_cost(small, route))
    if part in ("C", "ALL"):
        print("6.5  State-space growth (random symmetric matrices)")
        print("  %2s %8s %9s %9s %10s" % ("n", "states", "n*2^(n-1)",
                                         "time(s)", "peak mem"))
        for n in range(4, 14):
            matrix = random_matrix(n, seed=n)
            tracemalloc.start()
            t0 = time.perf_counter()
            _, _, states = held_karp(matrix)
            elapsed = time.perf_counter() - t0
            peak = tracemalloc.get_traced_memory()[1]
            tracemalloc.stop()
            print("  %2d %8d %9d %9.3f %8.0fKB" % (n, states, n * 2 ** (n - 1),
                                                   elapsed, peak / 1024))


if __name__ == "__main__":
    main("ALL")
