"""Task 5 - Minimum spanning tree: Kruskal, Prim and Boruvka.

Undirected graph given as (u, v, weight) edges. Each algorithm returns
its MST edges in the order they were added, plus a construction log.
"""
import heapq


# ------------------------------------------------------------ helpers
class DisjointSet:
    """Union-find with path compression and union by size."""

    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.size = {x: 1 for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


# ------------------------------------------------------------ algorithms
def kruskal(vertices, edges):
    """Next safe edge: globally lightest edge joining two components."""
    ds, mst, log = DisjointSet(vertices), [], []
    ordered = sorted(range(len(edges)), key=lambda k: (edges[k][2], k))
    for k in ordered:
        u, v, w = edges[k]
        if ds.union(u, v):
            mst.append((u, v, w))
            log.append("add %s-%s %d" % (u, v, w))
        else:
            log.append("reject %s-%s %d (cycle)" % (u, v, w))
        if len(mst) == len(vertices) - 1:
            break
    return mst, log


def prim(vertices, edges, start):
    """Next safe edge: lightest edge leaving the current tree."""
    adj = {v: [] for v in vertices}
    for u, v, w in edges:
        adj[u].append((w, v, u))
        adj[v].append((w, u, v))
    in_tree, mst, log = {start}, [], ["start at %s" % start]
    heap = list(adj[start])
    heapq.heapify(heap)                    # ties: lower weight, then vertex
    while heap and len(in_tree) < len(vertices):
        w, v, u = heapq.heappop(heap)
        if v in in_tree:
            continue                       # both ends already in the tree
        in_tree.add(v)
        mst.append((u, v, w))
        log.append("add %s-%s %d  tree={%s}" % (u, v, w, "".join(sorted(in_tree))))
        for item in adj[v]:
            if item[1] not in in_tree:
                heapq.heappush(heap, item)
    return mst, log


def boruvka(vertices, edges, prefer_later=False):
    """Each round every component picks its cheapest outgoing edge.
    Ties are broken by a fixed total order on edges (index), so no
    cycle can be created; prefer_later flips that order."""
    ds, mst, log, rounds = DisjointSet(vertices), [], [], 0
    def rank(k):
        return (edges[k][2], -k if prefer_later else k)
    while len(mst) < len(vertices) - 1:
        rounds += 1
        cheapest = {}
        for k, (u, v, w) in enumerate(edges):
            ru, rv = ds.find(u), ds.find(v)
            if ru == rv:
                continue
            for r in (ru, rv):
                if r not in cheapest or rank(k) < rank(cheapest[r]):
                    cheapest[r] = k
        if not cheapest:
            raise ValueError("graph is not connected")
        added = []
        for k in sorted(set(cheapest.values())):
            u, v, w = edges[k]
            if ds.union(u, v):
                mst.append((u, v, w))
                added.append("%s-%s %d" % (u, v, w))
        comps = len({ds.find(x) for x in vertices})
        log.append("round %d: %s -> %d component(s)" % (rounds, ", ".join(added), comps))
    return mst, log


# ------------------------------------------------------------ reporting
def edge_set(mst):
    return sorted("".join(sorted((u, v))) for u, v, _ in mst)


def report(name, mst, log):
    print("  %s:" % name)
    for line in log:
        print("    " + line)
    print("    MST %s cost=%d" % (edge_set(mst), sum(w for *_, w in mst)))


V = list("ABCDEFGH")
E = [("A", "B", 4), ("A", "C", 7), ("B", "C", 10), ("B", "D", 3),
     ("C", "D", 13), ("C", "E", 5), ("D", "E", 9), ("D", "F", 6),
     ("E", "F", 12), ("E", "G", 2), ("F", "G", 8), ("F", "H", 11),
     ("G", "H", 1)]
# Stress test: equal weights so that several MSTs share the same cost
E_TIES = [("A", "B", 4), ("A", "C", 4), ("B", "C", 4), ("B", "D", 3),
          ("C", "D", 13), ("C", "E", 5), ("D", "E", 9), ("D", "F", 6),
          ("E", "F", 12), ("E", "G", 2), ("F", "G", 8), ("F", "H", 11),
          ("G", "H", 1)]


def main(part="ALL"):
    if part in ("A", "ALL"):
        print("Graph: %d vertices, %d edges (distinct weights)" % (len(V), len(E)))
        report("Kruskal", *kruskal(V, E))
        report("Prim", *prim(V, E, "A"))
    if part in ("B", "ALL"):
        report("Boruvka", *boruvka(V, E))
    if part in ("C", "ALL"):
        print("Stress: A-C 7 -> 4 and B-C 10 -> 4, so A-B=A-C=B-C=4")
        results = {"Kruskal": kruskal(V, E_TIES),
                   "Prim(A)": prim(V, E_TIES, "A"),
                   "Prim(H)": prim(V, E_TIES, "H"),
                   "Boruvka": boruvka(V, E_TIES, prefer_later=True)}
        for name, (mst, _) in results.items():
            print("  %-8s %s cost=%d" % (name, " ".join(edge_set(mst)),
                                         sum(w for *_, w in mst)))
        sets = {tuple(edge_set(m)) for m, _ in results.values()}
        print("  different edge sets returned: %d" % len(sets))


if __name__ == "__main__":
    main("ALL")
