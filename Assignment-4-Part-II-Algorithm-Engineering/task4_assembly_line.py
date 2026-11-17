"""Task 4 - Assembly-line scheduling with two lines (Dynamic Programming).

f[l][j] = fastest time to finish station j on line l (l = 0 or 1).
Reaching station j on line l: either stay on line l from station j-1, or
come from the other line and pay the transfer time after station j-1.
"""
import copy


# ------------------------------------------------------------ algorithm
def schedule(plant):
    """plant: dict with entry[2], exit[2], a[2][n], t[2][n-1].
    t[l][j] = time to move away from line l after station j (0-based).
    Returns (best_time, route, trace)."""
    a, t, e, x = plant["a"], plant["t"], plant["entry"], plant["exit"]
    n = len(a[0])
    if n == 0 or len(a[1]) != n or len(t[0]) != n - 1 or len(t[1]) != n - 1:
        raise ValueError("inconsistent plant description")
    f = [[0] * n for _ in range(2)]
    came_from = [[0] * n for _ in range(2)]
    f[0][0], f[1][0] = e[0] + a[0][0], e[1] + a[1][0]
    trace = []
    for j in range(1, n):
        row = [j + 1]
        for line in (0, 1):
            other = 1 - line
            stay = f[line][j - 1] + a[line][j]
            move = f[other][j - 1] + t[other][j - 1] + a[line][j]
            if stay <= move:
                f[line][j], came_from[line][j] = stay, line
            else:
                f[line][j], came_from[line][j] = move, other
            row += [stay, move, "stay" if stay <= move else "transfer"]
        trace.append(row)
    finish = [f[0][n - 1] + x[0], f[1][n - 1] + x[1]]
    line = 0 if finish[0] <= finish[1] else 1
    route = [line]
    for j in range(n - 1, 0, -1):          # walk the decisions backwards
        line = came_from[line][j]
        route.append(line)
    route.reverse()
    return min(finish), route, trace, f, finish


# ------------------------------------------------------------ reporting
def print_trace(trace):
    print("  %3s | %5s %5s %-8s | %5s %5s %-8s" % ("St", "L1stay", "L1tr",
          "chosen", "L2stay", "L2tr", "chosen"))
    for st, s1, m1, c1, s2, m2, c2 in trace:
        print("  %3d | %5d %5d %-8s | %5d %5d %-8s" % (st, s1, m1, c1, s2, m2, c2))


def print_route(route, best):
    print("  Entry")
    for j, line in enumerate(route):
        arrow = "  |  Transfer" if j and route[j - 1] != line else "  |"
        if j:
            print(arrow)
        print("  Line %d - Station %d" % (line + 1, j + 1))
    print("  |")
    print("  Exit")
    moves = ["after station %d (L%d->L%d)" % (j, route[j - 1] + 1, route[j] + 1)
             for j in range(1, len(route)) if route[j] != route[j - 1]]
    print("  Transfers:", "; ".join(moves) if moves else "none")
    print("  Minimum Production Time = %d" % best)


def solve_and_show(title, plant, show_trace=True):
    best, route, trace, f, finish = schedule(plant)
    print(title)
    if show_trace:
        print("  f1 =", f[0], "+ exit", plant["exit"][0], "=", finish[0])
        print("  f2 =", f[1], "+ exit", plant["exit"][1], "=", finish[1])
        print_trace(trace)
    print_route(route, best)
    return best, route


PLANT = {"entry": [3, 2], "exit": [2, 3],
         "a": [[6, 9, 4, 7, 5, 8],          # line 1 stations 1..6
               [8, 4, 7, 3, 9, 4]],         # line 2 stations 1..6
         "t": [[2, 3, 1, 2, 3],             # leave line 1 after station j
               [3, 1, 2, 2, 1]]}            # leave line 2 after station j


def main(part="ALL"):
    if part in ("A", "ALL"):
        solve_and_show("4.1/4.2  Base plant", PLANT)
    if part in ("B", "ALL"):
        slow_transfer = copy.deepcopy(PLANT)
        slow_transfer["t"][1][1] = 10      # L2 -> L1 after station 2: 1 -> 10
        solve_and_show("4.3  Transfer L2->L1 after station 2: 1 -> 10",
                       slow_transfer)
    if part in ("C", "ALL"):
        slow_machine = copy.deepcopy(PLANT)
        slow_machine["a"][1][3] = 12       # line 2 station 4: 3 -> 12
        solve_and_show("4.4  Line 2 station 4 slows down: 3 -> 12",
                       slow_machine)


if __name__ == "__main__":
    main("ALL")
