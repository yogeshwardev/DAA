# Task 6 - Energy-aware job scheduling (weighted interval scheduling by DP)

def schedule(jobs):
    jobs = sorted(jobs, key=lambda j: (j[2], j[1]))          # by finish, then start
    n = len(jobs)
    p = [0] * (n + 1)
    for j in range(1, n + 1):                                # binary search for p(j)
        lo, hi = 1, j - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if jobs[mid - 1][2] <= jobs[j - 1][1]:
                p[j], lo = mid, mid + 1
            else:
                hi = mid - 1
    opt, take = [0] * (n + 1), [False] * (n + 1)
    for j in range(1, n + 1):
        skip = opt[j - 1]
        take_val = jobs[j - 1][3] + opt[p[j]]
        if take_val > skip:
            opt[j], take[j] = take_val, True
        else:
            opt[j] = skip
        print("  j=%d %s p=%d skip=%3d take=%3d -> %s  OPT=%d"
              % (j, jobs[j - 1][0], p[j], skip, take_val, "take" if take[j] else "skip", opt[j]))
    selected, j = [], n
    while j > 0:                                             # reconstruction
        if take[j]:
            selected.append(jobs[j - 1][0]); j = p[j]
        else:
            j -= 1
    return selected[::-1], opt[n]


jobs = [("J1", 1, 3, 20), ("J2", 2, 5, 50), ("J3", 4, 6, 30), ("J4", 6, 8, 40),
        ("J5", 5, 9, 60), ("J6", 8, 10, 30), ("J7", 9, 11, 50), ("J8", 11, 13, 40)]
print("Stage 5 - eight given jobs")
sel, best = schedule(jobs)
print("Selected:", sel, " Total energy saving:", best)

adversarial = [("K1", 0, 10, 100), ("K2", 0, 3, 40), ("K3", 3, 6, 40),
               ("K4", 6, 10, 40), ("K5", 9, 12, 70), ("K6", 10, 12, 10)]
print("\nStage 6 - adversarial jobs")
sel, best = schedule(adversarial)
print("Selected:", sel, " Total energy saving:", best)
