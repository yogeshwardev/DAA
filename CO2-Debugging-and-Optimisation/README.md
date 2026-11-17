# CSA06 – CO2 Debugging and Optimisation Task (SentinelOps SOC Alert-Triage Module)

**N D YOGESHWAR – 192465067**

| File | Purpose |
|---|---|
| `CSA06_CO2_SentinelOps_Answer.pdf` | Full answer document, parts (a)–(e), with program output screenshots |
| `buggy_module.py` | Original code, unchanged, run on the test data (Part a) |
| `corrected_module.py` | Minimal fixes tagged FIX-1 … FIX-9, plus boundary tests (Part b) |
| `stepwise_debug.py` | Applies the fixes one at a time and re-tests after each one (Part b) |
| `sentinel_triage.py` | Final optimised module with docstrings, test harness and `measure()` (Parts c–e) |
| `measurements.txt` | Output of `measure()` used in Part d |
| `screenshots/` | Program output screenshots |

## Run

```
python sentinel_triage.py                                   # test harness: 32 passed, 0 failed
python -c "import sentinel_triage as s; s.measure()"        # Part (d) measurements
```

## Defects found (9)

1. `sort_alerts`: `while j > 0` → `j >= 0`
2. `sort_alerts`: `alerts[j] = key` → `alerts[j + 1] = key`
3. `is_blocked`: a match returned `False` → `True`
4. `is_blocked`: `else: return False` inside the loop → `return False` after the loop
5. `find_signature`: `range(n - m)` → `range(n - m + 1)`
6. `find_signature`: `if j == m - 1` false match → `for … else`
7. `closest_logins`: `min_dist = 0` → `math.inf`
8. `closest_logins`: `d > min_dist` → `d < min_dist`
9. `closest_logins`: self-pairs `i == j` compared → skipped

## Optimisations

- `sort_alerts`: Timsort (stable, O(n) on nearly sorted input, O(n log n) worst case)
- `is_blocked`: blocklist stored as a hash set, O(1) average lookup
- `find_signature`: Knuth–Morris–Pratt, O(n + m)
- `closest_logins`: only pairs with j > i, squared distances, sorted by x with pruning. For 8,000 events it needs 15,124 distance computations instead of 63,992,000.
