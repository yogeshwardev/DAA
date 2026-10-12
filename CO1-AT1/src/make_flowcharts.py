import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results", "graphs")
os.makedirs(OUT, exist_ok=True)


def box(ax, x, y, text, w=3.4, h=0.9, kind="proc"):
    if kind == "term":
        p = FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.4",
                           fc="#dfe9f7", ec="#1f3a5f")
        ax.add_patch(p)
    elif kind == "dec":
        ax.add_patch(Polygon([(x, y + h * 0.75), (x + w / 2 + 0.2, y), (x, y - h * 0.75),
                              (x - w / 2 - 0.2, y)], fc="#fdf3d8", ec="#7a5c00"))
    else:
        ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, fc="#eef6ee", ec="#2e5e2e"))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.5)


def arrow(ax, x1, y1, x2, y2, label=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color="#333"))
    if label:
        ax.text((x1 + x2) / 2 + 0.15, (y1 + y2) / 2 + 0.1, label, fontsize=8, color="#900")


def canvas(title, h):
    fig, ax = plt.subplots(figsize=(6.5, h))
    ax.set_xlim(-4.2, 6.2)
    ax.set_ylim(0, h * 1.6)
    ax.axis("off")
    ax.set_title(title, fontsize=11)
    return fig, ax


def save(fig, name):
    fig.text(0.99, 0.01, "N D YOGESHWAR | 192465067", ha="right", fontsize=7, color="gray")
    fig.savefig(os.path.join(OUT, name), dpi=140, bbox_inches="tight")
    plt.close(fig)


def linear():
    fig, ax = canvas("Flowchart 1: Linear search", 7)
    top = 10.4
    box(ax, 0, top, "Start: data[0..n-1], key", kind="term")
    box(ax, 0, top - 1.6, "i = 0")
    box(ax, 0, top - 3.3, "i < n ?", kind="dec", w=2.6)
    box(ax, 0, top - 5.0, "data[i] == key ?", kind="dec", w=2.8)
    box(ax, 0, top - 6.7, "i = i + 1")
    box(ax, 4.6, top - 3.3, "return -1\n(not found)", w=2.2, kind="term")
    box(ax, 4.6, top - 5.0, "return i\n(found)", w=2.2, kind="term")
    arrow(ax, 0, top - 0.45, 0, top - 1.15)
    arrow(ax, 0, top - 2.05, 0, top - 2.6)
    arrow(ax, 0, top - 4.0, 0, top - 4.3, "yes")
    arrow(ax, 1.5, top - 3.3, 3.5, top - 3.3, "no")
    arrow(ax, 1.6, top - 5.0, 3.5, top - 5.0, "yes")
    arrow(ax, 0, top - 5.75, 0, top - 6.25, "no")
    ax.plot([-1.75, -3.2, -3.2, -1.5], [top - 6.7, top - 6.7, top - 3.3, top - 3.3], color="#333")
    ax.annotate("", xy=(-1.5, top - 3.3), xytext=(-1.6, top - 3.3), arrowprops=dict(arrowstyle="->"))
    save(fig, "flowchart1_linear_search.png")


def binary():
    fig, ax = canvas("Flowchart 2: Recursive binary search (sorted array)", 7.6)
    top = 11.2
    box(ax, 0, top, "BS(arr, key, low, high)", kind="term")
    box(ax, 0, top - 1.8, "low > high ?", kind="dec", w=2.6)
    box(ax, 4.6, top - 1.8, "return -1\n(base case)", w=2.2, kind="term")
    box(ax, 0, top - 3.8, "mid = (low + high) / 2")
    box(ax, 0, top - 5.5, "arr[mid] == key ?", kind="dec", w=2.8)
    box(ax, 4.6, top - 5.5, "return mid", w=2.2, kind="term")
    box(ax, 0, top - 7.4, "key < arr[mid] ?", kind="dec", w=2.8)
    box(ax, -2.3, top - 9.2, "BS(arr, key,\nlow, mid-1)", w=2.6, h=1.0)
    box(ax, 2.7, top - 9.2, "BS(arr, key,\nmid+1, high)", w=2.6, h=1.0)
    arrow(ax, 0, top - 0.45, 0, top - 1.05)
    arrow(ax, 1.6, top - 1.8, 3.5, top - 1.8, "yes")
    arrow(ax, 0, top - 2.55, 0, top - 3.35, "no")
    arrow(ax, 0, top - 4.25, 0, top - 4.75)
    arrow(ax, 1.6, top - 5.5, 3.5, top - 5.5, "yes")
    arrow(ax, 0, top - 6.25, 0, top - 6.65, "no")
    arrow(ax, -1.3, top - 7.4, -2.3, top - 8.7, "yes")
    arrow(ax, 1.3, top - 7.4, 2.7, top - 8.7, "no")
    save(fig, "flowchart2_binary_search.png")


def bst():
    fig, ax = canvas("Flowchart 3: BST build (preprocessing) and search", 8.6)
    top = 12.6
    box(ax, 0, top, "BUILD: for each key in data", kind="term", w=3.8)
    box(ax, 0, top - 1.5, "cur = root; walk down:\nkey < cur.key -> left, else right", w=4.2, h=1.0)
    box(ax, 0, top - 3.0, "empty child slot found:\nattach new Node(key)", w=4.2, h=1.0)
    arrow(ax, 0, top - 0.45, 0, top - 1.0)
    arrow(ax, 0, top - 2.0, 0, top - 2.5)
    box(ax, 0, top - 4.9, "SEARCH(root, key): cur = root", kind="term", w=4.0)
    box(ax, 0, top - 6.5, "cur is empty ?", kind="dec", w=2.4)
    box(ax, 4.6, top - 6.5, "return not found", w=2.4, kind="term")
    box(ax, 0, top - 8.3, "key == cur.key ?", kind="dec", w=2.6)
    box(ax, 4.6, top - 8.3, "return found", w=2.4, kind="term")
    box(ax, 0, top - 10.1, "cur = left if key < cur.key\nelse right", w=3.8, h=1.0)
    arrow(ax, 0, top - 5.35, 0, top - 5.75)
    arrow(ax, 1.4, top - 6.5, 3.4, top - 6.5, "yes")
    arrow(ax, 0, top - 7.25, 0, top - 7.55, "no")
    arrow(ax, 1.5, top - 8.3, 3.4, top - 8.3, "yes")
    arrow(ax, 0, top - 9.05, 0, top - 9.6, "no")
    ax.plot([-1.95, -3.2, -3.2, -1.4], [top - 10.1, top - 10.1, top - 6.5, top - 6.5], color="#333")
    ax.annotate("", xy=(-1.4, top - 6.5), xytext=(-1.5, top - 6.5), arrowprops=dict(arrowstyle="->"))
    save(fig, "flowchart3_bst_search.png")


if __name__ == "__main__":
    linear()
    binary()
    bst()
    print("flowcharts written to results/graphs")
