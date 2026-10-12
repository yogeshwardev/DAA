import random
import time
from datetime import datetime

SEED = 5067


def sequential_search(records, tool_id):
    comps = 0
    for i in range(len(records)):
        comps += 1
        if records[i][0] == tool_id:
            return i, comps
    return -1, comps


def make_records(n, rng):
    ids = rng.sample(range(1, 10 * n + 1), n)
    return [("T-%d" % t, "E%04d" % rng.randint(1, 900), rng.randint(0, 1439), rng.randint(1, 12)) for t in ids]


def header(title):
    print("=" * 74)
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 74)


def main():
    header("Q2 - SEQUENTIAL SEARCH EXPERIMENTS")
    rng = random.Random(SEED)
    csv_lines = []
    print("%8s%12s%12s%12s%12s%20s" % ("n", "first", "middle", "last", "absent", "mean (1000 hits)"))
    for n in (100, 1000, 10000, 100000):
        rec = make_records(n, rng)
        c_first = sequential_search(rec, rec[0][0])[1]
        c_mid = sequential_search(rec, rec[n // 2][0])[1]
        c_last = sequential_search(rec, rec[-1][0])[1]
        c_abs = sequential_search(rec, "T-0")[1]
        hits = [rec[rng.randrange(n)][0] for _ in range(1000)]
        mean = sum(sequential_search(rec, h)[1] for h in hits) / 1000
        print("%8d%12d%12d%12d%12d%20.1f" % (n, c_first, c_mid, c_last, c_abs, mean))
        for case, v in (("first", c_first), ("middle", c_mid), ("last", c_last), ("absent", c_abs),
                        ("mean of 1000 successful", mean)):
            csv_lines.append("CSV,q2,%d,%s,%.1f" % (n, case, v))
    print()
    rec = make_records(100000, rng)
    reps = 20
    t0 = time.perf_counter()
    for _ in range(reps):
        sequential_search(rec, "T-0")
    per_cmp_ns = (time.perf_counter() - t0) / (reps * 100000) * 1e9
    print("measured cost of one comparison in this environment: %.1f ns" % per_cmp_ns)
    limit_ms = 1.0
    n_limit = int(limit_ms * 1e6 / per_cmp_ns)
    print("acceptable response time chosen: %.1f ms -> unsuccessful search stays acceptable up to n = %d records"
          % (limit_ms, n_limit))
    print()
    print("CHANGED CONDITION (assumed figures): one hangar vs 20 facilities")
    one_n, one_req = 400, 300
    print("%-26s%10s%14s%16s%22s" % ("scenario", "records", "requests/h", "avg comps/req", "comparisons per hour"))
    for label, mult in (("one hangar", 1), ("20 facilities (one list)", 20)):
        n = one_n * mult
        req = one_req * mult
        avg = 0.5 * (n / 2) + 0.5 * n
        print("%-26s%10d%14d%16.0f%22.0f" % (label, n, req, avg, req * avg))
        csv_lines.append("CSV,q2s,%s,%d,%d,%.0f,%.0f" % (label, n, req, avg, req * avg))
    n20 = one_n * 20
    t_one = n20 * per_cmp_ns / 1e6
    print("one unsuccessful search in the 20-facility list: %d comparisons = %.2f ms" % (n20, t_one))
    csv_lines.append("CSV,q2t,%.1f,%d,%.3f" % (per_cmp_ns, n_limit, t_one))
    print()
    for line in csv_lines:
        print(line)


if __name__ == "__main__":
    main()
