import csv
import math
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
OUT = os.path.join(RES, "graphs")
os.makedirs(OUT, exist_ok=True)
SIGN = "N D YOGESHWAR | 192465067"
STYLE = {"Linear search": ("o", "-"), "Binary search (recursive)": ("s", "--"), "BST search": ("^", "-.")}


def load():
    data = {}
    with open(os.path.join(RES, "results.csv")) as f:
        for r in csv.DictReader(f):
            data.setdefault(r["algorithm"], []).append(r)
    return data


def finish(fig, ax, name, title, xlabel, ylabel):
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, which="major", linestyle=":", linewidth=0.5, color="black")
    ax.legend()
    fig.text(0.99, 0.01, SIGN, ha="right", va="bottom", fontsize=8, color="black")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, name), dpi=140)
    plt.close(fig)


def series(data, key):
    return {a: ([int(r["n"]) for r in rows], [float(r[key]) for r in rows]) for a, rows in data.items()}


def main():
    data = load()

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for a, (x, y) in series(data, "avg_search_us").items():
        ax.loglog(x, y, marker=STYLE[a][0], linestyle=STYLE[a][1], label=a, color="black")
    finish(fig, ax, "graph1_avg_search_time.png", "Average time per search",
           "n (records)", "microseconds per search")

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for a, (x, y) in series(data, "avg_comparisons").items():
        ax.loglog(x, y, marker=STYLE[a][0], linestyle=STYLE[a][1], label=a, color="black")
    finish(fig, ax, "graph2_avg_comparisons.png", "Average key comparisons per search",
           "n (records)", "comparisons")

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for a in ("Binary search (recursive)", "BST search"):
        x, y = series(data, "preprocess_s")[a]
        ax.loglog(x, y, marker=STYLE[a][0], linestyle=STYLE[a][1], label=a, color="black")
    finish(fig, ax, "graph3_preprocessing_time.png", "Preprocessing time (sort / tree build)",
           "n (records)", "seconds")

    ns = [1000, 10000, 100000, 1000000]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for a, (x, y) in series(data, "avg_comparisons").items():
        ax.loglog(x, y, marker=STYLE[a][0], linestyle="none", label=a + " (measured)", color="black",
                  markerfacecolor="white", markersize=8)
    ax.loglog(ns, [0.75 * n for n in ns], linestyle="-", color="black", linewidth=0.9, label="linear theory 0.75n")
    ax.loglog(ns, [math.log2(n) for n in ns], linestyle="--", color="black", linewidth=0.9, label="binary theory log2 n")
    ax.loglog(ns, [1.39 * math.log2(n) for n in ns], linestyle="-.", color="black", linewidth=0.9,
              label="BST theory 1.39 log2 n")
    finish(fig, ax, "graph4_theory_vs_experiment.png", "Theory vs experiment: comparisons per search",
           "n (records)", "comparisons")

    fig, ax = plt.subplots(figsize=(7, 4.5))
    rows = list(csv.DictReader(open(os.path.join(RES, "task12_results.csv"))))
    rows = [r for r in rows if not r["design"].startswith("Linear")]
    names = [r["design"].replace(" - ", "\n") for r in rows]
    vals = [float(r["search_50000_s"]) for r in rows]
    bars = ax.bar(range(len(rows)), vals, color="white", edgecolor="black", hatch="//")
    for b, h in zip(bars, ["//", "\\\\", "xx", ".."]):
        b.set_hatch(h)
    ax.set_xticks(range(len(rows)))
    ax.set_xticklabels(names, fontsize=8)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{v:.3f}s", ha="center", va="bottom", fontsize=8)
    ax.set_title("Task 12: time for 50,000 searches on 1,000,000 records")
    ax.set_ylabel("seconds")
    ax.grid(True, axis="y", linestyle=":", linewidth=0.5, color="black")
    fig.text(0.99, 0.01, SIGN, ha="right", va="bottom", fontsize=8, color="black")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "graph5_task12_50000_searches.png"), dpi=140)
    plt.close(fig)
    print("graphs written to results/graphs")


if __name__ == "__main__":
    main()
