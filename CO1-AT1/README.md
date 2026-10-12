# DAA Assignment 1 - Efficient Search in a Student Record System

- **Name:** N D YOGESHWAR
- **Registration No:** 192465067
- **Dataset seed:** 5067 (last four digits of the registration number)
- **Language:** Python 3.11

## Algorithms chosen

| # | Algorithm | Strategy | Preprocessing |
|---|-----------|----------|---------------|
| 1 | Linear search | Brute force (iterative) | none |
| 2 | Binary search | Decrease-and-conquer (recursive) | sort the records |
| 3 | Binary search tree (group D) | Transform-and-conquer (iterative) | build the tree |

Task 12 (50,000 searches on 1,000,000 records) also benchmarks an iterative binary search and a hash set.

## How to run

Only the standard library is needed to run the algorithms. The graph, screenshot and report scripts need
`matplotlib`, `pillow` and `reportlab` (`pip install matplotlib pillow reportlab`).

```
cd src
python dataset_generator.py          # writes data/sample_1000.csv, checks all four sizes
python benchmark.py --test           # Task 8: correctness tests
python benchmark.py --cases          # Task 4: best / average / worst counters
python benchmark.py --size 1000      # Task 9: one size (10000, 100000, 1000000 the same way)
python benchmark.py --all            # Task 9: all four sizes in one go
python task12_challenge.py           # Task 12: 50,000 searches on 1,000,000 records
python make_graphs.py                # graphs from results/results.csv
python make_flowcharts.py            # flowcharts for Task 1
python make_screenshots.py           # screenshots from results/logs
python build_report.py               # builds report/DAA_A1_192465067.pdf
```

The 1,000,000-record linear search takes about a minute. Large datasets are not stored; the generator
recreates them from the seed. Timings differ a little from machine to machine; comparison counts do not.

## Running on an online compiler

`online/daa_online.py` is a single-file copy of everything. Set `SIZE` (1000, 10000, 100000 or 1000000) and
`MODE` (`"bench"`, `"test"`, `"cases"` or `"task12"`) at the top, run it, and take a full screenshot of the output.
Save the screenshots in `screenshots/raw/` and the copied console text in `results/online/`, then run:

```
cd src
python import_online.py              # rebuilds results.csv and task12_results.csv from the online output
python stamp_screenshots.py          # adds name and reg no at the bottom right of every raw screenshot
python make_graphs.py
python build_report.py
```

## Layout

```
README.md
report/DAA_A1_192465067.pdf
src/        algo1_linear_search.py, algo2_binary_search.py, algo3_bst_search.py,
            dataset_generator.py, benchmark.py, task12_challenge.py, make_*.py, build_report.py
data/       sample_1000.csv
results/    results.csv, task12_results.csv, graphs/, logs/
screenshots/
```
