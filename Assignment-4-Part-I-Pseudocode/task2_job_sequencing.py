# Task 2 - Job sequencing with deadlines (greedy: highest profit, latest free slot)

def job_sequencing(jobs):
    jobs = sorted(jobs, key=lambda j: j[2], reverse=True)
    m = min(len(jobs), max(d for _, d, _ in jobs))
    slot = [None] * (m + 1)
    total = 0
    for jid, d, p in jobs:
        t = min(d, m)
        while t >= 1 and slot[t] is not None:      # feasibility check
            t -= 1
        if t >= 1:
            slot[t] = jid
            total += p
            print("  %s (d=%d, p=%d): placed in slot %d   slots=%s  profit=%d" % (jid, d, p, t, slot[1:], total))
        else:
            print("  %s (d=%d, p=%d): rejected, no free slot   slots=%s  profit=%d" % (jid, d, p, slot[1:], total))
    return slot[1:], total


jobs = [("A", 2, 80), ("B", 1, 35), ("C", 2, 60), ("D", 3, 40), ("E", 1, 25)]
print("Task 2.4 - given instance")
print("Schedule and profit:", job_sequencing(jobs))

print("\nTask 2.5 - profit of B changed from 35 to 90")
jobs[1] = ("B", 1, 90)
print("Schedule and profit:", job_sequencing(jobs))
