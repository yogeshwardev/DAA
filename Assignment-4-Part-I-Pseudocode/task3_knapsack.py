# Task 3 - 0/1 Knapsack by dynamic programming with item reconstruction

def knapsack01(items, W):
    n = len(items)
    V = [[0] * (W + 1) for _ in range(n + 1)]
    take = [[False] * (W + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        name, w, v = items[i - 1]
        for c in range(1, W + 1):
            exclude = V[i - 1][c]
            if w <= c and v + V[i - 1][c - w] > exclude:      # include / exclude decision
                V[i][c] = v + V[i - 1][c - w]
                take[i][c] = True
            else:
                V[i][c] = exclude
    selected, c = [], W
    for i in range(n, 0, -1):                                 # reconstruction
        if c >= 1 and take[i][c]:
            selected.append(items[i - 1][0])
            c -= items[i - 1][1]
    return V, V[n][W], selected[::-1]


items = [("P", 2, 12), ("Q", 3, 20), ("R", 4, 25), ("S", 5, 30)]
V, best, chosen = knapsack01(items, 7)
print("DP table V[i][c], c = 0..7")
print("  none     ", V[0])
for i, (name, w, v) in enumerate(items, 1):
    print("  %s(%d,%2d)  " % (name, w, v), V[i])
print("Maximum value  :", best)
print("Items selected :", chosen)
print("Total weight   :", sum(w for n, w, v in items if n in chosen))
