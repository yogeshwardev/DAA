"""Task 3 - Routing engine: Dijkstra, Bellman-Ford, Floyd and Warshall.

The network is directed. Vertices are depots A..H, edge weights are
travel costs. Graphs are stored as edge lists; algorithms never print.
"""
import heapq

INF = float("inf")
VERTICES = list("ABCDEFGH")
BASE_EDGES = [("A", "B", 2), ("A", "C", 6), ("B", "D", 3), ("B", "E", 8),
              ("C", "E", 9), ("C", "F", 5), ("D", "E", 4), ("D", "F", 7),
              ("E", "G", 3), ("E", "H", 6), ("F", "G", 2), ("F", "H", 9),
              ("G", "H", 2)]
NEGATIVE_EDGE = ("C", "D", -3)          # Stage B: rebate on road C -> D
CYCLE_EDGE = ("D", "C", 1)              # Stage C: makes C->D->C = -2


# ------------------------------------------------------------ algorithms
def dijkstra(vertices, edges, source):
    """Greedy shortest paths. Returns dist, pred, finalisation order."""
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((v, w))
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    done, order, heap = set(), [], [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue                      # stale heap entry
        done.add(u)
        order.append((u, d))              # dist[u] is now final
        for v, w in adj[u]:
            if v not in done and d + w < dist[v]:
                dist[v], pred[v] = d + w, u
                heapq.heappush(heap, (dist[v], v))
    return dist, pred, order


def bellman_ford(vertices, edges, source):
    """Returns (dist, pred, passes_used, cycle) - cycle is None if absent."""
    dist = {v: INF for v in vertices}
    pred = {v: None for v in vertices}
    dist[source] = 0
    passes = 0
    for _ in range(len(vertices) - 1):
        passes += 1
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v], pred[v], changed = dist[u] + w, u, True
        if not changed:
            break                         # early exit: already stable
    for u, v, w in edges:                 # |V|-th check pass
        if dist[u] != INF and dist[u] + w < dist[v]:
            pred[v] = u
            x = v
            for _ in range(len(vertices)):    # walk back into the cycle
                x = pred[x]
            cycle, y = [x], pred[x]
            while y != x:
                cycle.append(y)
                y = pred[y]
            cycle.append(x)
            return dist, pred, passes, cycle[::-1]
    return dist, pred, passes, None


def floyd(vertices, edges):
    D = {(i, j): (0 if i == j else INF) for i in vertices for j in vertices}
    for u, v, w in edges:
        D[(u, v)] = min(D[(u, v)], w)
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if D[(i, k)] + D[(k, j)] < D[(i, j)]:
                    D[(i, j)] = D[(i, k)] + D[(k, j)]
    negative = [v for v in vertices if D[(v, v)] < 0]
    return D, negative


def warshall(vertices, edges):
    R = {(i, j): (i == j) for i in vertices for j in vertices}
    for u, v, _ in edges:
        R[(u, v)] = True
    for k in vertices:
        for i in vertices:
            for j in vertices:
                R[(i, j)] = R[(i, j)] or (R[(i, k)] and R[(k, j)])
    return R


def path_to(pred, target):
    path = []
    while target is not None:
        path.append(target)
        target = pred[target]
    return path[::-1]


# ------------------------------------------------------------ reporting
def fmt(x):
    return "inf" if x == INF else str(x)


def show_routes(dist, pred, title):
    print(title)
    for v in VERTICES:
        print("  %s dist=%-4s pred=%-4s path=%s" % (v, fmt(dist[v]), pred[v],
              "-".join(path_to(pred, v)) if dist[v] != INF else "-"))


def show_matrix(vertices, M, cell):
    print("     " + "".join("%5s" % v for v in vertices))
    for i in vertices:
        print("  %s  " % i + "".join("%5s" % cell(M[(i, j)]) for j in vertices))


def main(part="ALL"):
    if part in ("A", "ALL"):
        print("Stage A - %d vertices, %d edges, source A"
              % (len(VERTICES), len(BASE_EDGES)))
        dist, pred, order = dijkstra(VERTICES, BASE_EDGES, "A")
        print("  finalised:", ", ".join("%s(%d)" % o for o in order))
        show_routes(dist, pred, "  Dijkstra results:")
    if part in ("B", "ALL"):
        edges = BASE_EDGES + [NEGATIVE_EDGE]
        print("Stage B - add %s->%s %d" % NEGATIVE_EDGE)
        dist, pred, order = dijkstra(VERTICES, edges, "A")
        print("  Dijkstra finalised:", ", ".join("%s(%d)" % o for o in order))
        show_routes(dist, pred, "  Dijkstra (unsafe with negative edge):")
        bdist, bpred, passes, cycle = bellman_ford(VERTICES, edges, "A")
        show_routes(bdist, bpred, "  Bellman-Ford (%d passes):" % passes)
        wrong = [v for v in VERTICES if dist[v] != bdist[v]]
        print("  vertices where Dijkstra is wrong:", wrong)
    if part in ("C", "ALL"):
        edges = BASE_EDGES + [NEGATIVE_EDGE, CYCLE_EDGE]
        print("Stage C - also add %s->%s %d" % CYCLE_EDGE)
        _, _, passes, cycle = bellman_ford(VERTICES, edges, "A")
        if cycle:
            cost = sum(w for u, v, w in edges
                       for a, b in zip(cycle, cycle[1:]) if (u, v) == (a, b))
            print("  ERROR: negative-weight cycle reachable from A")
            print("  cycle %s, total weight %d" % ("->".join(cycle), cost))
            print("  shortest paths are undefined; no distances returned")
        D, negative = floyd(VERTICES, edges)
        print("  Floyd check: D[v][v] < 0 for", negative)
    if part in ("D", "ALL"):
        edges = BASE_EDGES + [NEGATIVE_EDGE]
        print("Stage D - all pairs on the Stage B network")
        D, negative = floyd(VERTICES, edges)
        print("  Floyd distance matrix (row = from):")
        show_matrix(VERTICES, D, fmt)
        print("  negative cycle:", negative or "none")
        R = warshall(VERTICES, edges)
        print("  Warshall reachability (1 = reachable):")
        show_matrix(VERTICES, R, lambda b: "1" if b else "0")


if __name__ == "__main__":
    main("ALL")
