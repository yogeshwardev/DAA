# Part (b) evidence: apply the fixes one at a time and re-test after each one.
import math

alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
log, pattern = "FAILFAIXFAIL", "FAIL"
events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

def sort_v(alerts, fix1, fix2):
    for i in range(1, len(alerts)):
        key = alerts[i]; j = i - 1
        while (j >= 0 if fix1 else j > 0) and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]; j -= 1
        alerts[j + 1 if fix2 else j] = key
    return alerts

def blocked_v(bl, ip, fix3, fix4):
    for i in range(len(bl)):
        if bl[i] == ip:
            return True if fix3 else False
        elif not fix4:
            return False
    return False if fix4 else None

def sig_v(log, pattern, fix5, fix6):
    n, m = len(log), len(pattern); hits = []
    for i in range(n - m + 1 if fix5 else n - m):
        matched = True
        for j in range(m):
            if log[i + j] != pattern[j]:
                matched = False; break
        if (matched if fix6 else j == m - 1):
            hits.append(i)
    return hits

def cp_v(ev, fix7, fix8, fix9):
    md = math.inf if fix7 else 0; pair = None
    for i in range(len(ev)):
        for j in range(len(ev)):
            if fix9 and i == j: continue
            d = math.sqrt((ev[i][0]-ev[j][0])**2 + (ev[i][1]-ev[j][1])**2)
            if (d < md) if fix8 else (d > md):
                md, pair = d, (i, j)
    return pair, round(md, 4) if md != math.inf else md

print("sort_alerts")
for label, f1, f2 in (("original", 0, 0), ("+FIX-2 only", 0, 1), ("+FIX-1 only", 1, 0), ("FIX-1 + FIX-2", 1, 1)):
    print("  %-14s" % label, sort_v(list(alerts), f1, f2))
print("  equal severities, original:", sort_v([("B1", 4), ("B2", 4), ("B3", 4)], 0, 0))
print("  [('B1',2),('B2',7)] original:", sort_v([("B1", 2), ("B2", 7)], 0, 0))
print("is_blocked")
for label, f3, f4 in (("original", 0, 0), ("+FIX-3", 1, 0), ("+FIX-3 +FIX-4", 1, 1)):
    print("  %-14s" % label, [blocked_v(blocklist, q, f3, f4) for q in queries], "empty:", blocked_v([], "x", f3, f4))
print("find_signature")
for label, f5, f6 in (("original", 0, 0), ("+FIX-5", 1, 0), ("+FIX-5 +FIX-6", 1, 1)):
    print("  %-14s" % label, sig_v(log, pattern, f5, f6), "end:", sig_v("XXXXFAIL", "FAIL", f5, f6),
          "longer:", sig_v("FAIL", "FAILURE", f5, f6))
print("closest_logins")
for label, f7, f8, f9 in (("original", 0, 0, 0), ("+FIX-7", 1, 0, 0), ("+FIX-7 +FIX-8", 1, 1, 0), ("+FIX-9", 1, 1, 1)):
    print("  %-14s" % label, cp_v(events, f7, f8, f9), "one:", cp_v([(1, 1)], f7, f8, f9), "none:", cp_v([], f7, f8, f9))
print("pair distances (i<j)")
for i in range(6):
    print("  ", " ".join("%d-%d:%.2f" % (i, j, math.dist(events[i], events[j])) for j in range(i + 1, 6)))
