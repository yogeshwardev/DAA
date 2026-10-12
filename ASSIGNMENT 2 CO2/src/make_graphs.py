import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from q5_convex_hull import brute_force_hull, set_a, set_b

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
OUT = os.path.join(RES, "graphs")
os.makedirs(OUT, exist_ok=True)
SIGN = "N D YOGESHWAR | 192465067"
HATCH = ["//", "\\\\", "xx", "..", "++"]
MARK = ["o", "s", "^", "D", "v"]
LINES = ["-", "--", "-.", ":", (0, (5, 1))]


def rows(name):
    with open(os.path.join(RES, name + ".csv")) as f:
        return list(csv.reader(f))


def save(fig, ax, name, title, xl, yl, legend=True):
    ax.set_title(title)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.grid(True, which="major", linestyle=":", linewidth=0.5, color="black")
    if legend:
        ax.legend(fontsize=8)
    fig.text(0.99, 0.005, SIGN, ha="right", va="bottom", fontsize=8, color="black")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, name), dpi=140)
    plt.close(fig)


def q1():
    data = [r for r in rows("q1") if r[1] == "2000"]
    kinds = []
    for r in data:
        if r[0] not in kinds:
            kinds.append(r[0])
    algos = ["Selection sort", "Bubble sort", "Insertion sort"]
    for idx, (col, name, yl) in enumerate(((3, "q1_comparisons.png", "comparisons (log scale)"),
                                           (4, "q1_swaps_moves.png", "swaps / moves (log scale)"))):
        fig, ax = plt.subplots(figsize=(9, 4.6))
        w = 0.26
        for a_i, a in enumerate(algos):
            vals = []
            for k in kinds:
                v = [int(r[col]) for r in data if r[0] == k and r[2] == a][0]
                vals.append(max(v, 0.8))
            ax.bar([i + a_i * w for i in range(len(kinds))], vals, w, color="white", edgecolor="black",
                   hatch=HATCH[a_i], label=a)
        ax.set_yscale("log")
        ax.set_xticks([i + w for i in range(len(kinds))])
        ax.set_xticklabels([k.replace(" ", "\n", 1) for k in kinds], fontsize=8)
        save(fig, ax, name, "Q1: " + yl.split(" (")[0] + " for n = 2000", "dataset", yl)
    fig, ax = plt.subplots(figsize=(7, 4.6))
    sizes = [500, 1000, 2000, 4000]
    i = 0
    for k in ("nearly sorted 95%", "random"):
        for a in ("Insertion sort", "Bubble sort"):
            ys = [int(r[4]) for s in sizes for r in rows("q1") if r[0] == k and r[1] == str(s) and r[2] == a][:len(sizes)]
            ax.loglog(sizes, ys, marker=MARK[i], linestyle=LINES[i], color="black", label="%s, %s" % (a, k))
            i += 1
    save(fig, ax, "q1_growth.png", "Q1: swaps / moves as n grows", "n", "swaps / moves")


def q2():
    r = rows("q2")
    fig, ax = plt.subplots(figsize=(7, 4.6))
    for i, case in enumerate(["first", "middle", "last", "absent", "mean of 1000 successful"]):
        pts = [(int(x[0]), float(x[2])) for x in r if x[1] == case]
        ax.loglog([p[0] for p in pts], [p[1] for p in pts], marker=MARK[i], linestyle=LINES[i], color="black",
                  label=case)
    save(fig, ax, "q2_comparisons.png", "Q2: comparisons of sequential search", "list size n", "comparisons")


def q3():
    r = rows("q3m")
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot([int(x[1]) for x in r], [int(x[3]) for x in r], marker="o", color="black", linestyle="-",
            label="observed")
    ax.plot([int(x[1]) for x in r], [int(x[2]) for x in r], marker="s", color="black", linestyle="--",
            markerfacecolor="white", label="predicted m(n - m + 1)")
    save(fig, ax, "q3_pattern_length.png", "Q3: engineered worst case, n = 10,000", "pattern length m",
         "character comparisons")


def q4():
    r = rows("q4")
    n = [int(x[0]) for x in r]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.loglog(n, [int(x[2]) for x in r], marker="o", color="black", label="pairs examined (observed)")
    ax.loglog(n, [int(x[1]) for x in r], linestyle="--", color="black", label="n(n-1)/2")
    save(fig, ax, "q4_pairs.png", "Q4: candidate pairs", "n (drones)", "pairs")
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.plot(n, [float(x[4]) for x in r], marker="o", color="black", label="measured time")
    ax.axhline(1.0, color="black", linestyle=":", label="acceptable limit (1 s)")
    save(fig, ax, "q4_time.png", "Q4: execution time", "n (drones)", "seconds")


def q5():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
    for ax, (title, pts) in zip(axes, (("Set A: boundary and interior", set_a()), ("Set B: designed set", set_b()))):
        hull, edges, tests, n = brute_force_hull(pts)
        inside = [p for p in set(pts) if p not in hull]
        for (a, b) in edges:
            ax.plot([a[0], b[0]], [a[1], b[1]], color="black", linewidth=1.6)
        ax.scatter([p[0] for p in inside], [p[1] for p in inside], facecolors="white", edgecolors="black", s=30,
                   label="interior or edge-interior point")
        ax.scatter([p[0] for p in hull], [p[1] for p in hull], color="black", s=45, label="hull vertex")
        ax.set_title(title)
        ax.set_aspect("equal")
        ax.legend(fontsize=7, loc="upper center", bbox_to_anchor=(0.5, -0.07))
        ax.grid(True, linestyle=":", linewidth=0.5, color="black")
    fig.text(0.99, 0.005, SIGN, ha="right", va="bottom", fontsize=8)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(OUT, "q5_hull.png"), dpi=140)
    plt.close(fig)
    r = rows("q5")
    n = [int(x[0]) for x in r]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.loglog(n, [int(x[2]) for x in r], marker="o", color="black", label="orientation tests, random points")
    ax.loglog(n, [int(x[3]) for x in r], marker="s", linestyle="--", color="black",
              markerfacecolor="white", label="orientation tests, points on a circle")
    ax.loglog(n, [x * (x - 1) * (x - 2) / 2 for x in n], linestyle=":", color="black", label="n(n-1)(n-2)/2 bound")
    save(fig, ax, "q5_growth.png", "Q5: work of the brute-force hull", "n (points)", "orientation tests")


def q6():
    r = rows("q6")
    n = [int(x[0]) for x in r]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.semilogy(n, [int(x[2]) for x in r], marker="o", color="black", label="candidates examined")
    ax.semilogy(n, [int(x[3]) for x in r], marker="s", linestyle="--", color="black", markerfacecolor="white",
                label="feasible candidates")
    save(fig, ax, "q6_candidates.png", "Q6: solution space", "n (packages)", "subsets (log scale)")
    fig, ax = plt.subplots(figsize=(7, 4.6))
    ax.semilogy(n, [float(x[5]) for x in r], marker="o", color="black", label="measured time")
    ax.axhline(5.0, color="black", linestyle=":", label="response time chosen (5 s)")
    save(fig, ax, "q6_time.png", "Q6: execution time", "n (packages)", "seconds (log scale)")


def q7():
    r = rows("q7")
    kinds = []
    for x in r:
        if x[0] not in kinds:
            kinds.append(x[0])
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    first = [x for x in r if x[0] == kinds[0]]
    ax.semilogy([int(x[1]) for x in first], [int(x[2]) for x in first], color="black", linestyle=":", marker="x",
                label="exhaustive search: 2^n candidates")
    for i, k in enumerate(kinds):
        pts = [x for x in r if x[0] == k]
        ax.semilogy([int(x[1]) for x in pts], [int(x[4]) for x in pts], marker=MARK[i], linestyle=LINES[i],
                    color="black", markerfacecolor="white", label="pruned search, " + k)
    save(fig, ax, "q7_nodes.png", "Q7: nodes visited, original and redesigned", "n (packages)",
         "candidates / nodes (log scale)")


if __name__ == "__main__":
    q1()
    q2()
    q3()
    q4()
    q5()
    q6()
    q7()
    print("graphs written to results/graphs")
