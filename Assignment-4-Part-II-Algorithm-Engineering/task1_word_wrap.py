"""Task 1 - Word wrap as a document-layout engine (Dynamic Programming).

Penalty of a non-final line = (unused spaces at the end of the line) ** 3.
The final line carries no penalty. A line holding words i..j has length
(sum of word lengths) + (number of words - 1) single spaces.
"""

INF = float("inf")


# ------------------------------------------------------------ algorithm
def line_penalty(unused, is_last_line):
    """Penalty of one line; the last line is free."""
    return 0 if is_last_line else unused ** 3


def word_wrap(words, width):
    """Minimum-penalty line breaking.

    best[j]  = minimum total penalty for laying out the first j words
    start[j] = index (1-based) of the first word on the last line of that
               optimal layout
    Returns (min_penalty, lines, states) where each line is
    (text, unused, penalty) and states is a list of (j, best[j], start[j]).
    Raises ValueError for a word that can never fit in a line.
    """
    if width <= 0:
        raise ValueError("line width must be positive")
    for w in words:
        if len(w) > width:
            raise ValueError("word '%s' (%d chars) is longer than width %d"
                             % (w, len(w), width))
    n = len(words)
    best = [INF] * (n + 1)
    start = [0] * (n + 1)
    best[0] = 0
    states = []
    for j in range(1, n + 1):
        length = -1                       # no leading space before word i
        for i in range(j, 0, -1):         # last line = words i..j
            length += len(words[i - 1]) + 1
            if length > width:            # longer lines cannot fit either
                break
            cost = best[i - 1] + line_penalty(width - length, j == n)
            if cost < best[j]:
                best[j], start[j] = cost, i
        states.append((j, best[j], start[j]))
    lines, j = [], n
    while j > 0:                          # follow start[] back to word 1
        i = start[j]
        text = " ".join(words[i - 1:j])
        unused = width - len(text)
        lines.append((text, unused, line_penalty(unused, j == n)))
        j = i - 1
    lines.reverse()
    return best[n], lines, states


def greedy_wrap_penalty(words, width):
    """Fill each line as far as possible (for comparison only)."""
    lines, current = [], ""
    for w in words:
        if current and len(current) + 1 + len(w) <= width:
            current += " " + w
        else:
            if current:
                lines.append(current)
            current = w
    lines.append(current)
    return sum((width - len(t)) ** 3 for t in lines[:-1]), len(lines)


# ------------------------------------------------------------ reporting
def print_layout(words, width):
    total, lines, _ = word_wrap(words, width)
    print("Width M = %d" % width)
    print("  %-2s %-*s %6s %7s" % ("#", width, "line text", "unused", "penalty"))
    for k, (text, unused, pen) in enumerate(lines, 1):
        print("  %-2d %-*s %6d %7d" % (k, width, text, unused, pen))
    print("  Minimum total penalty = %d  (%d lines)" % (total, len(lines)))
    return total, lines


def print_states(words, width):
    _, _, states = word_wrap(words, width)
    print("DP states  best[j] = min penalty for words 1..j")
    print("  %-3s %-12s %8s  %s" % ("j", "word j", "best[j]", "last line starts at"))
    for j, b, s in states:
        print("  %-3d %-12s %8d  word %d (%s)" % (j, words[j - 1], b, s, words[s - 1]))


TEXT = ("Greedy line filling can leave large gaps that a dynamic "
        "programming layout engine avoids by looking ahead").split()


def main(part="ALL"):
    if part in ("A", "ALL"):
        print("1.1/1.2  Text of %d words, width 20" % len(TEXT))
        total, _ = print_layout(TEXT, 20)
        g, gl = greedy_wrap_penalty(TEXT, 20)
        print("  (greedy line filling: penalty %d, %d lines)" % (g, gl))
        print_states(TEXT, 20)
    if part in ("B", "ALL"):
        print("1.3  Same text, different widths")
        for width in (20, 16, 24, 30):
            print_layout(TEXT, width)
    if part in ("C", "ALL"):
        print("1.4  Boundary tests")
        tests = [("word exactly as long as width", ["abcdefgh", "ab", "cd"], 8),
                 ("two words fill line exactly", ["abc", "defg", "h"], 8),
                 ("single word", ["solo"], 8),
                 ("empty text", [], 8)]
        for name, words, width in tests:
            total, lines, _ = word_wrap(words, width)
            print("  %s: %s W=%d" % (name, words, width))
            print("    lines=%s penalty=%d" % ([t for t, _, _ in lines], total))
        try:
            word_wrap(["tiny", "internationalisation"], 12)
        except ValueError as err:
            print("  word longer than width -> ValueError:")
            print("    %s" % err)


if __name__ == "__main__":
    main("ALL")
