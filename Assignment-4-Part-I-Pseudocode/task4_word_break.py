# Task 4 - WordBreak: faulty version vs repaired version

def word_break(text, dictionary, repaired):
    n = len(text)
    dp = [True] + [False] * n
    for i in range(1, n + 1):
        for j in range(i):
            word_ok = text[j:i] in dictionary          # substring(Text, j, i)
            if (dp[j] and word_ok) if repaired else word_ok:
                dp[i] = True
                break
    return dp


dictionary = {"my", "lue", "car"}
for text in ("mybluecar", "mycar"):
    print("Text =", repr(text), " Dictionary =", sorted(dictionary))
    faulty = word_break(text, dictionary, repaired=False)
    fixed = word_break(text, dictionary, repaired=True)
    print("  i  prefix       faulty  repaired")
    for i in range(len(text) + 1):
        mark = "   <-- differs" if faulty[i] != fixed[i] else ""
        print("  %d  %-11s  %-6s  %-6s%s" % (i, text[:i] or "(empty)", faulty[i], fixed[i], mark))
    print("  Result: faulty =", faulty[-1], " repaired =", fixed[-1])
