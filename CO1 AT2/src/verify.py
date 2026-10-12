import math
from datetime import datetime


def m1_comparisons(n):
    count = 0
    for i in range(0, n - 1):
        for j in range(i + 1, n):
            count += 1
    return count


def m2_audits(n):
    count = 0
    i = 1
    while i < n:
        for j in range(i):
            count += 1
        i *= 2
    return count


def s2(n):
    return 1 if n == 1 else s2(n // 2) + 1


def m4_current(n):
    return 1 if n == 1 else 4 * m4_current(n // 2) + n


def m4_redesign(n):
    return 1 if n == 1 else 2 * m4_redesign(n // 2) + n


def m5(n):
    return 1 if n == 1 else 2 * m5(n // 2) + n * math.log2(n)


def main():
    print("=" * 70)
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("CSA06 CO1 - verification of the derived formulae")
    print("=" * 70)
    print("M1 comparisons vs n(n-1)/2")
    for n in (10, 100, 1000):
        print("  n = %5d  counted %8d  formula %8d" % (n, m1_comparisons(n), n * (n - 1) // 2))
    print("M2 audits vs 2^ceil(log2 n) - 1")
    for n in (8, 100, 1000, 1024, 1025):
        print("  n = %5d  counted %6d  formula %6d  n-1 = %5d  n log2 n = %8.0f" %
              (n, m2_audits(n), 2 ** math.ceil(math.log2(n)) - 1, n - 1, n * math.log2(n)))
    print("S2 recurrence vs floor(log2 n) + 1")
    for n in (1, 2, 16, 1024, 2 ** 20):
        print("  n = %8d  T(n) = %2d  formula %2d" % (n, s2(n), int(math.log2(n)) + 1))
    print("M4 recurrences (n a power of two)")
    for n in (2, 16, 1024):
        print("  n = %5d  current %9d (2n^2 - n = %9d)  redesign %7d (n log2 n + n = %7d)" %
              (n, m4_current(n), 2 * n * n - n, m4_redesign(n), n * int(math.log2(n)) + n))
    print("M5 recurrence vs n log2 n (log2 n + 1)/2 + n")
    for n in (2, 16, 1024):
        l = math.log2(n)
        print("  n = %5d  T(n) = %10.1f  formula %10.1f" % (n, m5(n), n * l * (l + 1) / 2 + n))
    print("f(n) = 3n^2 + 10 n log2 n + 50 against 3n^2 and 4n^2")
    for n in (1, 16, 59, 60, 64, 1000, 10 ** 6):
        f = 3 * n * n + 10 * n * math.log2(n) + 50
        print("  n = %8d  f = %16.1f  3n^2 = %16d  4n^2 = %16d  f <= 4n^2: %s" % (n, f, 3 * n * n, 4 * n * n, f <= 4 * n * n))
    print("Estimates for n = 1,000,000 at 10^8 operations per second")
    n = 10 ** 6
    L = math.log2(n)
    est = [("M1", n * (n - 1) / 2), ("M2", 2 ** math.ceil(L) - 1), ("S2 (one search)", math.floor(L) + 1),
           ("S1 (one search, worst)", n), ("M4 current", 2 * n * n - n), ("M4 redesign", n * L + n),
           ("M5", n * L * (L + 1) / 2 + n), ("report generator f(n)", 3 * n * n + 10 * n * L + 50)]
    for name, ops in est:
        print("  %-24s %18.4e ops  %14.4f s  %s" % (name, ops, ops / 1e8, "FAILS 600 s window" if ops / 1e8 > 600 else "ok"))


if __name__ == "__main__":
    main()
