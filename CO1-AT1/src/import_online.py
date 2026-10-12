import csv
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "results")
ONLINE = os.path.join(RES, "online")
FIELDS = ["n", "algorithm", "preprocess_s", "search_total_s", "avg_search_us", "avg_comparisons",
          "avg_comp_found", "avg_comp_notfound", "max_comparisons", "queries", "tree_height"]
FIELDS12 = ["design", "preprocess_s", "search_50000_s", "us_per_search", "daily_update_resort_s",
            "daily_update_merge_s", "daily_update_bst_s", "daily_update_hash_s"]


def main():
    rows, rows12 = {}, []
    for path in sorted(glob.glob(os.path.join(ONLINE, "*.txt"))):
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("CSV,"):
                    p = line.split(",")
                    rows[(int(p[1]), p[2])] = dict(zip(FIELDS, p[1:]))
                elif line.startswith("CSV12,"):
                    rows12.append(dict(zip(FIELDS12, line.split(",")[1:])))
    if rows:
        with open(os.path.join(RES, "results.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            w.writeheader()
            for k in sorted(rows):
                w.writerow(rows[k])
        print("results.csv updated with", len(rows), "rows")
    if rows12:
        with open(os.path.join(RES, "task12_results.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS12)
            w.writeheader()
            w.writerows(rows12)
        print("task12_results.csv updated with", len(rows12), "rows")
    if not rows and not rows12:
        print("no CSV lines found in", ONLINE)


if __name__ == "__main__":
    main()
