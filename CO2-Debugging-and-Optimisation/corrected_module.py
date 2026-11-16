# SentinelOps SOC alert-triage module -- CORRECTED (Part b).
# Minimal fixes only: every changed line is tagged FIX-n (n = defect number).
# No optimisation yet, so the algorithms are exactly the original brute-force ones.
import math

def sort_alerts(alerts): # insertion sort by severity, highest first (stable)
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j >= 0 and alerts[j][1] < key[1]:      # FIX-1: j > 0  ->  j >= 0
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j + 1] = key                            # FIX-2: alerts[j] -> alerts[j + 1]
    return alerts

def is_blocked(blocklist, ip): # sequential search
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return True                                # FIX-3: False -> True
    return False                                       # FIX-4: else-branch moved out of loop

def find_signature(log, pattern): # brute-force string matching, all occurrences
    n, m = len(log), len(pattern)
    hits = []
    if m == 0:                                         # guard: empty pattern has no signature
        return hits
    for i in range(n - m + 1):                         # FIX-5: n - m -> n - m + 1
        for j in range(m):
            if log[i + j] != pattern[j]:
                break
        else:                                          # FIX-6: hit only if loop never broke
            hits.append(i)
    return hits

def closest_logins(events): # brute-force closest pair of login locations
    min_dist = math.inf                                # FIX-7: 0 -> infinity
    pair = None
    for i in range(len(events)):
        for j in range(len(events)):
            if i == j:                                 # FIX-9: skip self-pair (distance 0)
                continue
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            if d < min_dist:                           # FIX-8: > -> <
                min_dist = d
                pair = (i, j)
    return pair, min_dist

if __name__ == "__main__":
    alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    log, pattern = "FAILFAIXFAIL", "FAIL"
    events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

    print("=== CORRECTED MODULE: OUTPUT ON TEST DATA ===")
    print("sort_alerts    :", sort_alerts(list(alerts)))
    for q in queries:
        print("is_blocked(%-10s):" % q, is_blocked(blocklist, q))
    print("find_signature :", find_signature(log, pattern))
    pair, d = closest_logins(events)
    print("closest_logins :", pair, "distance = %.4f km" % d)

    print("\n=== BOUNDARY TESTS ===")
    print("empty blocklist         :", is_blocked([], "10.0.0.5"))
    print("pattern at very end     :", find_signature("XXXXFAIL", "FAIL"))
    print("pattern longer than log :", find_signature("FAIL", "FAILURE"))
    print("pattern == log          :", find_signature("FAIL", "FAIL"))
    print("overlapping matches     :", find_signature("AAAA", "AA"))
    print("empty pattern           :", find_signature("FAIL", ""))
    print("equal severities        :", sort_alerts([("B1", 4), ("B2", 4), ("B3", 4)]))
    print("empty alert list        :", sort_alerts([]))
    print("one login event         :", closest_logins([(1, 1)]))
    print("no login events         :", closest_logins([]))
    print("two login events        :", closest_logins([(0, 0), (3, 4)]))
