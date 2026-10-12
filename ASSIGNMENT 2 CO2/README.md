# DAA Assignment 2 (CO2) - Brute-Force and Exhaustive Search

- **Name:** N D YOGESHWAR
- **Registration No:** 192465067
- **Seed:** 5067 (last four digits of the registration number)
- **Language:** Python 3.11

## Contents

| Question | Script | What it does |
|----------|--------|--------------|
| Q1 | `src/q1_sorting.py` | Selection, bubble and insertion sort on six input arrangements, with comparison and swap/move counters |
| Q2 | `src/q2_sequential.py` | Sequential search: positions, absent keys, list sizes, 20-facility scenario |
| Q3 | `src/q3_string_matching.py` | Brute-force string matching, four designed test conditions with predictions |
| Q4 | `src/q4_closest_pair.py` | Brute-force closest pair, pair counts, time limit estimate |
| Q5 | `src/q5_convex_hull.py` | Brute-force convex hull from the cross-product rule |
| Q6 | `src/q6_exhaustive.py` | Exhaustive search for the best airlift load, correctness check and growth |
| Q7 | `src/q7_redesign.py` | Redesign of Q6 with pruning, compared with the original |

Every `qN_*.py` file is self-contained (standard library only), so it can be pasted into an online compiler as it is.

## How to run

```
cd src
python q1_sorting.py                 # and q2 ... q7 in the same way
python collect.py                    # runs all seven, writes results/logs/*.txt and results/*.csv
python make_graphs.py                # graphs in results/graphs (needs matplotlib)
python make_screenshots.py           # screenshots of the logs (needs pillow)
python build_report.py                # builds report/DAA_A2_192465067.pdf (needs reportlab)
```

`q6_exhaustive.py` and `q7_redesign.py` together take a few minutes.

## Using an online compiler for the screenshots

1. Run each `qN_*.py` file in an online Python compiler and take a full screenshot of the output.
2. Save the screenshots in `screenshots/raw/` as `q1_sorting_output.png` ... `q7_redesign_output.png`.
3. Copy the console text of each run into `results/online/qN.txt`.
4. From `src` run `python collect.py --online`, `python stamp_screenshots.py`, `python make_graphs.py` and
   `python build_report.py`. The tables and graphs are then built from the online numbers, so they match the screenshots.

## Layout

```
README.md
report/DAA_A2_192465067.pdf
src/          q1_sorting.py ... q7_redesign.py, collect.py, make_graphs.py, make_screenshots.py,
              stamp_screenshots.py, build_report.py
data/         (test data is generated from the seed)
results/      q1.csv ... q7.csv, logs/, graphs/, online/
screenshots/  raw/
```
