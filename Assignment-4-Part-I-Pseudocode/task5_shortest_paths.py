# Task 5 - Dijkstra, Bellman-Ford and Floyd on the same graph
import math

V = ["A", "B", "C", "D", "E"]
E = [("A", "B", 4), ("A", "C", 7), ("B", "C", 2), ("B", "D", 6), ("C", "D", 1), ("D", "E", 3), ("C", "E", 8)]
INF = math.inf

print("Dijkstra from A")
dist = {v: INF for v in V}; pred = {v: None for v in V}; done = set()
dist["A"] = 0
while len(done) < len(V):
    u = min((v for v in V if v not in done), key=lambda v: dist[v])   # EXTRACT_MIN
    if dist[u] == INF:
        break
    done.add(u)
    for a, b, w in E:
        if a == u and b not in done and dist[u] + w < dist[b]:       # relaxation
            dist[b], pred[b] = dist[u] + w, u
    print("  select %s -> dist %s" % (u, [dist[v] for v in V]))
path, v = [], "E"
while v:
    path.append(v); v = pred[v]
print("  path to E:", " -> ".join(path[::-1]), "=", dist["E"])

print("Bellman-Ford from A")
bf = {v: INF for v in V}; bf["A"] = 0
for _ in range(len(V) - 1):
    for a, b, w in E:
        if bf[a] != INF and bf[a] + w < bf[b]:
            bf[b] = bf[a] + w
neg = any(bf[a] != INF and bf[a] + w < bf[b] for a, b, w in E)
print("  dist", [bf[v] for v in V], " negative cycle:", neg)

neg_graph = [("A", "B", 2), ("A", "C", 5), ("C", "B", -4)]
d = {"A": 0, "B": INF, "C": INF}; fixed = []
for _ in range(2):                                         # greedy order fixes B first
    u = min((x for x in d if x not in fixed), key=lambda x: d[x]); fixed.append(u)
    for a, b, w in neg_graph:
        if a == u and b not in fixed and d[u] + w < d[b]:
            d[b] = d[u] + w
print("  negative edge example: greedy B =", d["B"], " true B = 5 + (-4) =", 1)

print("Floyd all pairs")
D = {(i, j): 0 if i == j else INF for i in V for j in V}
for a, b, w in E:
    D[(a, b)] = w
for k in V:
    for i in V:
        for j in V:
            if D[(i, k)] + D[(k, j)] < D[(i, j)]:
                D[(i, j)] = D[(i, k)] + D[(k, j)]
for i in V:
    print("  from %s:" % i, [D[(i, j)] for j in V])
