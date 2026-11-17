# KartIQ - Module 4 : Recommendation scores C = A x B using Strassen's method
import random
import time

mults = 0


def strassen_2x2(A, B):
    (a00, a01), (a10, a11) = A
    (b00, b01), (b10, b11) = B
    m1 = (a00 + a11) * (b00 + b11)
    m2 = (a10 + a11) * b00
    m3 = a00 * (b01 - b11)
    m4 = a11 * (b10 - b00)
    m5 = (a00 + a01) * b11
    m6 = (a10 - a00) * (b00 + b01)
    m7 = (a01 - a11) * (b10 + b11)
    print("m1..m7 =", [m1, m2, m3, m4, m5, m6, m7])
    return [[m1 + m4 - m5 + m7, m3 + m5],
            [m2 + m4, m1 + m3 - m2 + m6]]


def conventional(A, B):
    global mults
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik, Bk, Ci = A[i][k], B[k], C[i]
            for j in range(n):
                Ci[j] += aik * Bk[j]
        mults += n * n
    return C


def add(X, Y, s=1):
    return [[x + s * y for x, y in zip(rx, ry)] for rx, ry in zip(X, Y)]


def split(M):
    h = len(M) // 2
    return ([r[:h] for r in M[:h]], [r[h:] for r in M[:h]],
            [r[:h] for r in M[h:]], [r[h:] for r in M[h:]])


def strassen(A, B, cutoff):
    """Hybrid Strassen: recurse while n > cutoff, then use the conventional method."""
    global mults
    n = len(A)
    if n <= cutoff:
        return conventional(A, B)
    a00, a01, a10, a11 = split(A)
    b00, b01, b10, b11 = split(B)
    m1 = strassen(add(a00, a11), add(b00, b11), cutoff)
    m2 = strassen(add(a10, a11), b00, cutoff)
    m3 = strassen(a00, add(b01, b11, -1), cutoff)
    m4 = strassen(a11, add(b10, b00, -1), cutoff)
    m5 = strassen(add(a00, a01), b11, cutoff)
    m6 = strassen(add(a10, a00, -1), add(b00, b01), cutoff)
    m7 = strassen(add(a01, a11, -1), add(b10, b11), cutoff)
    c00 = add(add(m1, m4), add(m7, m5, -1))
    c01 = add(m3, m5)
    c10 = add(m2, m4)
    c11 = add(add(m1, m3), add(m6, m2, -1))
    return [l + r for l, r in zip(c00, c01)] + [l + r for l, r in zip(c10, c11)]


A = [[1, 7], [3, 5]]
B = [[1, 3], [7, 5]]
print("Strassen    C =", strassen_2x2(A, B))
print("Conventional C =", conventional(A, B))


def counts(n, cutoff):
    """Scalar multiplications and additions for an n x n product (n power of 2)."""
    if n <= cutoff:
        return n ** 3, n ** 3 - n ** 2
    m, a = counts(n // 2, cutoff)
    return 7 * m, 7 * a + 18 * (n // 2) ** 2


print("\nn = 1024      multiplications      additions          total")
for name, c in (("conventional", 1024), ("Strassen n0=1", 1), ("hybrid n0=32", 32),
                ("hybrid n0=64", 64), ("hybrid n0=128", 128)):
    m, a = counts(1024, c)
    print("%-14s %14d %14d %14d" % (name, m, a, m + a))

n = 128
random.seed(1)
X = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
Y = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
mults = 0; t = time.perf_counter(); C1 = conventional(X, Y)
print("\nn=128 conventional : %9d mults %6.2f s" % (mults, time.perf_counter() - t))
for cut in (8, 32):
    mults = 0; t = time.perf_counter(); C2 = strassen(X, Y, cut)
    print("n=128 Strassen n0=%-2d: %9d mults %6.2f s  same result: %s"
          % (cut, mults, time.perf_counter() - t, C1 == C2))
