import random
from datetime import datetime

SEED = 5067


def brute_force_match(text, pattern):
    n, m = len(text), len(pattern)
    comps = 0
    for i in range(n - m + 1):
        j = 0
        while j < m:
            comps += 1
            if text[i + j] != pattern[j]:
                break
            j += 1
        if j == m:
            return i, comps
    return -1, comps


def header(title):
    print("=" * 74)
    print("Date/Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print(title)
    print("=" * 74)


def log_text(n, rng):
    words = ["accepted", "session", "opened", "user", "admin", "connection", "closed", "from", "port",
             "kernel", "service", "started", "timeout", "request", "denied", "login", "file", "read"]
    out, size = [], 0
    while size < n:
        line = "%02d:%02d:%02d %s %s %d\n" % (rng.randint(0, 23), rng.randint(0, 59), rng.randint(0, 59),
                                              rng.choice(words), rng.choice(words), rng.randint(1000, 9999))
        out.append(line)
        size += len(line)
    return "".join(out)[:n]


def main():
    header("Q3 - BRUTE-FORCE STRING MATCHING")
    rng = random.Random(SEED)
    n, m = 10000, 10
    csv_lines = []
    freq_alpha = "ACGT"
    tests = []
    t1 = ("b" * n, "a" * m)
    t2 = ("a" * n, "a" * (m - 1) + "b")
    lt = log_text(n, rng)
    pat3 = "request timeout 10000"
    t3 = (lt, pat3)
    t4 = ("".join(rng.choice(freq_alpha) for _ in range(n)), "ACGTACGTAC" + "T")
    tests = [("1 low work: no pattern letter in text", *t1), ("2 engineered worst case", *t2),
             ("3 log-style text and absent signature", *t3), ("4 DNA-like alphabet (4 letters)", *t4)]

    print("PREDICTIONS (made before running)")
    print("  test 1: first character mismatches at every alignment -> n - m + 1 comparisons")
    print("  test 2: m - 1 characters match at every alignment, last one fails -> m (n - m + 1) comparisons")
    def per_alignment(text, pat):
        total, prod = 0.0, 1.0
        for ch in pat:
            total += prod
            prod *= text.count(ch) / len(text)
        return total

    est3 = (n - len(pat3) + 1) * per_alignment(lt, pat3)
    print("  test 3: character frequencies of the text give %.3f comparisons per alignment -> about %.0f"
          % (per_alignment(lt, pat3), est3))
    est4 = (n - len(t4[1]) + 1) * per_alignment(t4[0], t4[1])
    print("  test 4: each letter has probability 1/4 -> %.3f per alignment -> about %.0f" %
          (per_alignment(t4[0], t4[1]), est4))
    print()
    preds = [n - m + 1, m * (n - m + 1), est3, est4]
    print("%-40s%8s%6s%12s%12s%10s" % ("test", "n", "m", "predicted", "observed", "found at"))
    for (name, text, pat), pr in zip(tests, preds):
        pos, c = brute_force_match(text, pat)
        print("%-40s%8d%6d%12.0f%12d%10d" % (name, len(text), len(pat), pr, c, pos))
        csv_lines.append("CSV,q3,%s,%d,%d,%.0f,%d" % (name, len(text), len(pat), pr, c))
    print()
    print("EFFECT OF TEXT LENGTH (engineered worst case, m = 10)")
    for size in (1000, 10000, 100000):
        c = brute_force_match("a" * size, "a" * 9 + "b")[1]
        print("  n = %6d  observed %8d   predicted m(n-m+1) = %8d" % (size, c, 10 * (size - 9)))
        csv_lines.append("CSV,q3n,%d,10,%d,%d" % (size, 10 * (size - 9), c))
    print("EFFECT OF PATTERN LENGTH (engineered worst case, n = 10000)")
    for mm in (2, 5, 10, 50, 200):
        c = brute_force_match("a" * 10000, "a" * (mm - 1) + "b")[1]
        print("  m = %4d  observed %8d   predicted m(n-m+1) = %8d" % (mm, c, mm * (10000 - mm + 1)))
        csv_lines.append("CSV,q3m,10000,%d,%d,%d" % (mm, mm * (10000 - mm + 1), c))
    print()
    for line in csv_lines:
        print(line)


if __name__ == "__main__":
    main()
