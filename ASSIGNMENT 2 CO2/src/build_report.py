import csv
import itertools
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, Preformatted,
                                SimpleDocTemplate, Spacer, Table, TableStyle)
from PIL import Image as PILImage

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
RES = os.path.join(ROOT, "results")
GR = os.path.join(RES, "graphs")
SH = os.path.join(ROOT, "screenshots")
OUT = os.path.join(ROOT, "report", "DAA_A2_192465067.pdf")
REPO = "https://github.com/yogeshwardev/DAA-A2-192465067-N-D-YOGESHWAR"
BLACK = colors.black

F = "C:/Windows/Fonts/"
pdfmetrics.registerFont(TTFont("Serif", F + "times.ttf"))
pdfmetrics.registerFont(TTFont("Serif-B", F + "timesbd.ttf"))
pdfmetrics.registerFont(TTFont("Serif-I", F + "timesi.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BI", F + "timesbi.ttf"))
pdfmetrics.registerFont(TTFont("Mono", F + "cour.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")

ss = getSampleStyleSheet()
body = ParagraphStyle("b", parent=ss["Normal"], fontName="Serif", fontSize=11.5, leading=16, spaceAfter=7,
                      alignment=TA_JUSTIFY, textColor=BLACK)
small = ParagraphStyle("s", parent=body, fontSize=9.5, leading=12, spaceAfter=0, alignment=0)
cap = ParagraphStyle("cap", parent=body, fontName="Serif-I", fontSize=10, alignment=TA_CENTER, spaceAfter=12)
h1 = ParagraphStyle("h1", parent=body, fontName="Serif-B", fontSize=15, leading=19, spaceBefore=10, spaceAfter=7,
                    alignment=0)
h2 = ParagraphStyle("h2", parent=body, fontName="Serif-B", fontSize=12, leading=16, spaceBefore=6, spaceAfter=3,
                    alignment=0)
center = ParagraphStyle("c", parent=body, alignment=TA_CENTER)
code = ParagraphStyle("code", fontName="Mono", fontSize=9, leading=11.5, borderColor=BLACK, borderWidth=0.6,
                      borderPadding=6, spaceBefore=4, spaceAfter=12, leftIndent=6, rightIndent=6)

story = []


def P(t, st=body):
    story.append(Paragraph(t, st))


def H1(t):
    story.append(Paragraph(t, h1))


def H2(t):
    story.append(Paragraph(t, h2))


def pseudo(text):
    story.append(Preformatted(text.strip("\n"), code))


def fig(path, caption, width=160):
    w, h = PILImage.open(path).size
    width = min(width, w * 0.2)
    if width * h / w > 215:
        width = 215 * w / h
    story.append(KeepTogether([Image(path, width=width * mm, height=width * mm * h / w), Paragraph(caption, cap)]))


def table(rows, widths=None, head=True):
    hs = ParagraphStyle("th", parent=small, fontName="Serif-B")
    rows = [[Paragraph(str(c), hs if (head and i == 0) else small) for c in r] for i, r in enumerate(rows)]
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, BLACK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story.append(t)
    story.append(Spacer(1, 8))


def rows(name):
    with open(os.path.join(RES, name + ".csv")) as f:
        return list(csv.reader(f))


def n_(x):
    return f"{int(round(float(x))):,}"


Q1 = rows("q1")
Q2 = rows("q2")
Q2S = rows("q2s")
Q2T = rows("q2t")[0]
Q3 = rows("q3")
Q3N = rows("q3n")
Q3M = rows("q3m")
Q4 = rows("q4")
Q4L = rows("q4lim")[0]
Q5 = rows("q5")
Q5S = rows("q5set")
Q6 = rows("q6")
Q6L = rows("q6lim")[0]
Q7 = rows("q7")


def q1val(kind, n, algo):
    for r in Q1:
        if r[0] == kind and r[1] == str(n) and r[2] == algo:
            return int(r[3]), int(r[4]), float(r[5])


def cover():
    story.append(Spacer(1, 28 * mm))
    P("DESIGN AND ANALYSIS OF ALGORITHMS", ParagraphStyle("t1", parent=center, fontName="Serif-B", fontSize=18,
                                                          leading=24))
    P("Assignment 2 (CO2)", ParagraphStyle("t2", parent=center, fontName="Serif-B", fontSize=14, leading=20))
    story.append(Spacer(1, 8 * mm))
    P("Brute-Force and Exhaustive-Search Techniques: Prediction, Measurement and Redesign",
      ParagraphStyle("t3", parent=center, fontName="Serif-I", fontSize=14, leading=20))
    story.append(Spacer(1, 16 * mm))
    table([["Submitted by", "N D YOGESHWAR"], ["Registration number", "192465067"],
           ["Random seed for all test data", "5067 (last four digits of the registration number)"],
           ["Programming language", "Python 3.11"],
           ["GitHub repository", f'<link href="{REPO}">{REPO}</link>']], widths=[55 * mm, 105 * mm], head=False)
    story.append(PageBreak())
    H1("Abstract")
    P("This report investigates six brute-force and exhaustive-search problems and then redesigns the one that "
      "scales worst. Selection, bubble and insertion sort are compared on six input arrangements; sequential "
      "search is studied for different positions, list sizes and loads; brute-force string matching is tested on "
      "inputs designed to cause little and much work; closest pair and convex hull are derived from geometric "
      "properties; and an exhaustive search for the best airlift load is analysed up to the point where it stops "
      "being usable. For every question a prediction was written first, operation counts were recorded as the main "
      "evidence, and the observed behaviour was compared with the prediction.")
    P("The exhaustive search of Q6 was chosen for the design challenge. Its bottleneck is that it enumerates "
      "all 2<super>n</super> subsets and recomputes every sum from scratch. A depth-first search that prunes "
      "overweight branches and uses a value-density bound was designed, predicted, implemented and measured, "
      "and it examined a small fraction of the original candidates while giving the same optimum. The report also "
      "records the instances on which this redesign loses most of its advantage.")
    H2("Contents")
    for t in ["Q1. Sorting under different data conditions", "Q2. Sequential search as an engineering choice",
              "Q3. Behaviour of brute-force string matching", "Q4. Closest pair", "Q5. Convex hull",
              "Q6. Exhaustive search and combinatorial growth", "Q7. Day-4 design challenge: diagnose, redesign "
              "and validate", "Conclusion and references"]:
        P(t, ParagraphStyle("toc", parent=body, alignment=0, spaceAfter=2))
    P("Note on measurements. Operation counts are the primary evidence in this report. Execution times were "
      "measured on one laptop with Python and vary from run to run, so they are used only as supporting evidence.",
      small)
    story.append(PageBreak())


def q1():
    H1("Q1. Sorting under Different Data Conditions")
    H2("1.1 Predictions made before implementation")
    P("The three algorithms differ in how much of their work depends on the order of the input. Selection sort "
      "always scans the whole unsorted part to find the minimum, so its number of comparisons is n(n - 1)/2 for "
      "every input, and it makes at most n - 1 swaps. Bubble sort with an early-exit flag stops after a pass "
      "without swaps, so it needs n - 1 comparisons on sorted data, but on other data it needs as many passes "
      "as the farthest displacement, and it performs one swap for every inversion. Insertion sort moves an element "
      "left past larger elements only, so the number of element moves equals the number of inversions and the "
      "comparisons are about n - 1 plus the number of inversions.")
    P("From this the expected results for n = 2000 are: sorted input, 1,999 comparisons and no moves for bubble "
      "and insertion sort and 1,999,000 comparisons for selection sort; reversed input, 1,999,000 comparisons "
      "for all three and about 2 million swaps or moves for bubble and insertion sort; random input, about half "
      "as many moves (n<super>2</super>/4, since a random permutation has about n(n - 1)/4 inversions).")
    H2("1.2 Test data")
    P("Six datasets of 2,000 priority scores were generated with seed 5067. Two contrasting datasets are the "
      "random order (many inversions) and the already sorted order (none). The reversed order is the most "
      "disordered case. Because the fulfilment centre reports that 95 percent of orders are already in order, "
      "two datasets resemble that situation: 1,900 sorted scores followed by 100 new random ones, and "
      "1,980 sorted scores followed by a small batch of 20 new ones. The edge case is a list that contains only "
      "five distinct scores, which produces many equal keys.")
    H2("1.3 Results")
    kinds = ["random", "sorted", "reversed", "nearly sorted 95%", "sorted + batch of 20", "few distinct scores"]
    t = [["Dataset (n = 2000)", "Selection sort<br/>comp / swaps", "Bubble sort<br/>comp / swaps",
          "Insertion sort<br/>comp / moves"]]
    for k in kinds:
        row = [k]
        for a in ("Selection sort", "Bubble sort", "Insertion sort"):
            c, s, _ = q1val(k, 2000, a)
            row.append(f"{c:,} / {s:,}")
        t.append(row)
    table(t, widths=[44 * mm, 40 * mm, 40 * mm, 40 * mm])
    P("Table 1.1: Comparisons and swaps or moves (from results/q1.csv)", cap)
    fig(os.path.join(GR, "q1_comparisons.png"), "Figure 1.1: Comparisons for the six datasets (logarithmic axis)", 140)
    fig(os.path.join(GR, "q1_swaps_moves.png"), "Figure 1.2: Swaps or moves for the six datasets (logarithmic axis)", 140)
    fig(os.path.join(SH, "q1_sorting_output.png"), "Figure 1.3: Program output for Q1", 160)
    H2("1.4 Prediction compared with observation")
    c_r = q1val("random", 2000, "Insertion sort")
    c_n = q1val("nearly sorted 95%", 2000, "Insertion sort")
    c_b = q1val("sorted + batch of 20", 2000, "Insertion sort")
    b_n = q1val("nearly sorted 95%", 2000, "Bubble sort")
    P("The predictions for sorted and reversed input were confirmed exactly: selection sort made 1,999,000 "
      "comparisons on every dataset, and bubble and insertion sort made 1,999 comparisons and no swaps on sorted "
      f"input. On random input the moves of insertion sort were {c_r[1]:,}, close to the predicted n(n - 1)/4 = "
      "999,500, which confirms the inversion argument.")
    P("One prediction was only partly right. I expected bubble sort to profit from its early exit on the 95 "
      f"percent sorted data, but it still made {b_n[0]:,} comparisons, almost the same as on random data. The "
      "reason is that in a pass a large element can travel all the way to the right, whereas a small element "
      "moves only one place to the left. New orders with small priority scores appended at the end therefore need "
      "a pass for every position they must travel, so the number of passes is close to n and the early exit "
      "never helps. Insertion sort does not have this problem, because it places each element directly. On "
      f"the same data it made only {c_n[0]:,} comparisons, and for the batch of 20 new orders only {c_b[0]:,}.")
    P("Selection sort is unaffected by the order of the data in its comparisons, which is both its weakness (it "
      "cannot benefit from existing order) and its strength (its swaps stay below n - 1, which would matter if "
      "writing an element were very expensive). With few distinct scores, bubble and insertion sort both "
      "needed fewer moves than on random data, because equal elements are not swapped.")
    H2("1.5 Design decision")
    P("Insertion sort is recommended for the fulfilment centre. When about 95 percent of the orders are already "
      f"in order, it needed {c_n[0]:,} comparisons against about two million for selection and bubble sort, "
      f"roughly {1999000 / c_n[0]:.0f} times fewer, and {c_b[0]:,} comparisons when only a small batch of new "
      "orders is added, which is about 78 times fewer. Its cost is proportional to the number of inversions, which "
      "is exactly the quantity that is small for nearly sorted data. The growth experiment in Table 1.2 shows "
      "that the benefit is not an accident of one size.")
    t = [["n", "Insertion, nearly sorted 95%<br/>comparisons", "Insertion, random<br/>comparisons",
          "Bubble, nearly sorted 95%<br/>comparisons"]]
    for n in (500, 1000, 2000, 4000):
        t.append([n, f"{q1val('nearly sorted 95%', n, 'Insertion sort')[0]:,}",
                  f"{q1val('random', n, 'Insertion sort')[0]:,}", f"{q1val('nearly sorted 95%', n, 'Bubble sort')[0]:,}"])
    table(t, widths=[20 * mm, 50 * mm, 45 * mm, 50 * mm])
    P("Table 1.2: Growth with n", cap)
    P("A limitation should be stated. If the 5 percent of new orders is large and scattered, insertion sort "
      "still has quadratic cost (it was about ten times cheaper than on random data, not linear). A better "
      "practical design for periodic batches would be to sort the small batch alone and merge it with the "
      "existing sorted list, but this is outside the three algorithms compared in this question.")


def q2():
    H1("Q2. Sequential Search as an Engineering Choice")
    H2("2.1 Experiment design")
    P("Each record has a tool identifier, a technician identifier, an issue time and a work bay, and the list is "
      "searched by tool identifier. Lists of 100, 1,000, 10,000 and 100,000 records were generated with seed "
      "5067. For each size the number of comparisons was recorded for a search for the first record, the middle "
      "record, the last record, an identifier that is not on the list, and the mean of 1,000 random successful "
      "searches. The cost of one comparison was also timed in this environment, so that comparison counts could be "
      "turned into a response time.")
    t = [["n", "First", "Middle", "Last", "Not present", "Mean of 1,000 successful", "(n + 1)/2"]]
    for n in (100, 1000, 10000, 100000):
        g = {r[1]: r[2] for r in Q2 if r[0] == str(n)}
        t.append([f"{n:,}", n_(g["first"]), n_(g["middle"]), n_(g["last"]), n_(g["absent"]),
                  f"{float(g['mean of 1000 successful']):,.1f}", f"{(n + 1) / 2:,.1f}"])
    table(t, widths=[20 * mm, 18 * mm, 22 * mm, 22 * mm, 24 * mm, 36 * mm, 24 * mm])
    P("Table 2.1: Comparisons of sequential search (from results/q2.csv)", cap)
    fig(os.path.join(GR, "q2_comparisons.png"), "Figure 2.1: Comparisons against list size (logarithmic axes)", 120)
    fig(os.path.join(SH, "q2_sequential_output.png"), "Figure 2.2: Program output for Q2", 160)
    H2("2.2 Observations")
    P("A successful search needs a number of comparisons equal to the position of the record, so the first record "
      "always costs one comparison and the last costs n. The mean over random successful searches is very "
      "close to (n + 1)/2, as expected for a uniform choice of record. An unsuccessful search always costs n "
      "comparisons, because the whole list has to be examined before the system can say that the tool is not "
      "issued. This is the important asymmetry: a failed search is twice as expensive as the average successful one.")
    H2("2.3 Operating boundary")
    per = float(Q2T[0])
    lim = int(Q2T[1])
    P(f"One comparison cost about {per:.0f} ns in the run recorded here (the value varied between 87 and 124 ns in "
      f"repeated runs on the same machine, and it includes the tuple access and string comparison of Python). "
      "I define an acceptable response time for a technician at the counter as 1 ms. An unsuccessful search stays "
      f"inside that limit up to about {lim:,} records in this run, and from the other runs the boundary lies "
      "between roughly 8,000 and 11,000 records. Below this size sequential search is a reasonable engineering "
      "choice, and it has real advantages for this application: the list changes all the time, a new record is "
      "added or removed in constant time, no sorted order or index has to be maintained, and the code is trivial "
      "to verify. Because tool identifiers are unique, a search can stop at the first match.")
    P("The second dimension is the frequency of requests. The comparisons per hour equal requests per hour "
      "multiplied by the average comparisons per request, so a list that is acceptable for one request may "
      "become a continuous load when requests arrive many times a second. I would stop recommending sequential "
      "search when either the list passes about 10,000 records or the request rate is high enough that the "
      "comparisons consume a noticeable share of the processor.")
    H2("2.4 Changed condition: 20 maintenance facilities")
    one, many = Q2S[0], Q2S[1]
    P("The numbers of records and requests for a single hangar are not given in the assignment, so I assumed "
      f"{one[1]} active records and {one[2]} requests per hour for one hangar, with half of the requests "
      f"unsuccessful, and scaled both by 20 for the combined system. This gives {many[1]} records and {many[2]} "
      f"requests per hour, an average of {many[3]} comparisons per request and {int(many[4]):,} comparisons per "
      f"hour, against {int(one[4]):,} for one hangar.")
    t = [["Scenario", "Records", "Requests per hour", "Average comparisons per request", "Comparisons per hour"]]
    for r in Q2S:
        t.append([r[0], r[1], r[2], r[3], f"{int(r[4]):,}"])
    table(t, widths=[45 * mm, 22 * mm, 30 * mm, 38 * mm, 32 * mm])
    P("Table 2.2: Effect of expanding from one hangar to 20 facilities (assumed workload)", cap)
    P(f"One unsuccessful search in the combined list needs {many[1]} comparisons, which is about "
      f"{float(Q2T[2]):.2f} ms in this run, so the system sits right at my 1 ms limit. The total of 36 million "
      "comparisons per hour is still small for a processor, so sequential search would not fail technically. "
      "My revised recommendation is nevertheless to stop using it for the combined system: the list is at the "
      "edge of the response-time limit, any further growth crosses it, and 20 facilities would probably send "
      "requests concurrently. A hash table keyed by tool identifier gives expected constant-time lookup and "
      "also supports the continuous issue and return of tools in constant time, whereas a sorted array "
      "would make every update expensive. If the combined list were kept per facility (about 400 records each), "
      "sequential search would remain acceptable for each of the 20 lists.")


def q3():
    H1("Q3. Behaviour of Brute-Force String Matching")
    H2("3.1 Test conditions and predictions")
    P("The matcher aligns the pattern at each of the n - m + 1 positions of the text and compares characters from "
      "left to right until a mismatch occurs or the whole pattern has matched. The work therefore depends on how "
      "many characters of the pattern match at each alignment before the first mismatch. Four test conditions "
      "were designed, each with n = 10,000 characters, and a prediction was written before running.")
    t = [["Test", "Text and pattern", "Prediction and reason"],
         ["1 Little work", "Text of the letter b only; pattern of ten letters a",
          "The first character mismatches at every alignment, so one comparison per alignment: n - m + 1 = 9,991."],
         ["2 Engineered worst case", "Text of the letter a only; pattern of nine a followed by b",
          "Nine characters match and the tenth fails at every alignment: m(n - m + 1) = 99,910."],
         ["3 Own condition: log text", "Random log lines (time, two words, number); pattern 'request timeout 10000', "
          "which cannot occur",
          "Expected comparisons per alignment from the character frequencies (1 + p1 + p1p2 + ...); "
          "close to one, so about 10,300."],
         ["4 Own condition: four-letter alphabet", "Random text over A, C, G, T; pattern of eleven letters that does "
          "not occur", "Each letter matches with probability 1/4, so 1 + 1/4 + 1/16 + ... = 1.33 comparisons per "
          "alignment: about 13,300."]]
    table(t, widths=[34 * mm, 58 * mm, 72 * mm])
    P("Table 3.1: Designed test conditions", cap)
    H2("3.2 Results")
    t = [["Test", "n", "m", "Predicted comparisons", "Observed comparisons"]]
    for r in Q3:
        t.append([r[0], r[1], r[2], n_(r[3]), n_(r[4])])
    table(t, widths=[70 * mm, 18 * mm, 14 * mm, 30 * mm, 30 * mm])
    P("Table 3.2: Predicted and observed character comparisons (from results/q3.csv)", cap)
    t = [["Text length n (m = 10)", "Predicted m(n - m + 1)", "Observed"]]
    for r in Q3N:
        t.append([f"{int(r[0]):,}", n_(r[2]), n_(r[3])])
    table(t, widths=[55 * mm, 55 * mm, 40 * mm])
    P("Table 3.3: Worst case for increasing text length", cap)
    fig(os.path.join(GR, "q3_pattern_length.png"), "Figure 3.1: Engineered worst case against pattern length", 115)
    fig(os.path.join(SH, "q3_string_matching_output.png"), "Figure 3.2: Program output for Q3", 160)
    H2("3.3 Inquiry")
    P("Test 1 and test 2 have exactly the same text length and pattern length, yet the second needed ten times "
      "as many comparisons. The difference comes from the content: in test 2 almost the entire pattern matches "
      "at every alignment before the mismatch at the last character, so each alignment repeats nine successful "
      "comparisons, and the text offers many overlapping partial matches. In test 1 the mismatch at the first "
      "character discards the alignment immediately. Repeated comparisons are produced by a pattern whose "
      "prefix also occurs repeatedly in the text, by a small alphabet, and by a mismatch that occurs late in "
      "the pattern. The algorithm never uses what it learned at one alignment to skip the next one, and for "
      "this reason it re-reads the same text characters up to m times.")
    P("Predictions 1, 2 and 4 were confirmed almost exactly. Test 3 was observed about three percent above the "
      "prediction (10,622 against 10,318), because the prediction multiplies single-letter frequencies as if "
      "neighbouring letters were independent, whereas letters in the log lines are correlated; the "
      "prediction method is therefore good but not exact for natural text.")
    P("The result shows that the input size n (and m) is not sufficient to describe the running time of this "
      "algorithm. The cost of the three experiments with the same n lies between 9,991 and 99,910 comparisons, "
      "a factor of ten, and the worst case of m(n - m + 1) grows linearly in both parameters. An analysis in terms "
      "of input size alone must therefore be accompanied by the structure of the input, and it should state "
      "which case (best, average or worst) it describes.")


def q4():
    H1("Q4. Closest Pair and the Cost of Examining Every Possibility")
    H2("4.1 Design and pair count")
    P("A brute-force solution has to look at the distance between every two different drones, because the "
      "closest pair could be any of them. A pair (i, j) is the same as the pair (j, i), and a drone is not "
      "paired with itself, so the loops run with i from 1 to n - 1 and j from i + 1 to n. The number of candidate "
      "pairs is therefore")
    pseudo("""
sum over i = 1..n-1 of (n - i) = (n-1) + (n-2) + ... + 1 = n(n - 1) / 2
""")
    P("For 100 drones this is 4,950 pairs, and doubling n multiplies the number of pairs by about four. "
      "Squared distances (dx<super>2</super> + dy<super>2</super>) are compared instead of distances, because the "
      "square root is monotonic, so the closest pair is the same, and one square root per pair is avoided. "
      "Each examined pair requires exactly one distance calculation, so the number of distance calculations equals "
      "the number of pairs.")
    pseudo("""
best = infinity
for i = 0 to n-2
    for j = i+1 to n-1
        d = (xi - xj)^2 + (yi - yj)^2
        if d < best: best = d; pair = (i, j)
return pair
""")
    H2("4.2 Results")
    t = [["n", "n(n - 1)/2", "Pairs examined", "Distance calculations", "Time (s)"]]
    for r in Q4:
        t.append([f"{int(r[0]):,}", n_(r[1]), n_(r[2]), n_(r[3]), f"{float(r[4]):.4f}"])
    table(t, widths=[22 * mm, 36 * mm, 36 * mm, 40 * mm, 24 * mm])
    P("Table 4.1: Closest-pair experiments (from results/q4.csv)", cap)
    fig(os.path.join(GR, "q4_pairs.png"), "Figure 4.1: Pairs examined and the theoretical n(n - 1)/2", 110)
    fig(os.path.join(GR, "q4_time.png"), "Figure 4.2: Execution time against n", 110)
    fig(os.path.join(SH, "q4_closest_pair_output.png"), "Figure 4.3: Program output for Q4", 160)
    P("The observed number of pairs is identical to n(n - 1)/2 for all seven sizes, so the theoretical derivation "
      "matches the implementation exactly. When n doubled from 1,600 to 3,200 the pair count grew by a factor of "
      "4.0 and the time by about 4, which is consistent with quadratic growth.")
    H2("4.3 Scalability")
    per, lim = float(Q4L[0]), int(Q4L[1])
    P("For this experimental environment I take an acceptable response time to be one second, which is a "
      f"reasonable limit for a monitoring display that is refreshed every few seconds. One pair cost about "
      f"{per:.0f} ns in the largest run, so the time t(n) = {per:.0f} ns x n(n - 1)/2 reaches one second at "
      f"about n = {lim:,} drones. This agrees with the table, where 1,600 drones took {float(Q4[4][4]):.2f} s "
      f"and 3,200 drones took {float(Q4[5][4]):.2f} s. Extrapolating, 10,000 drones would need roughly "
      f"{per * 1e-9 * 10000 * 9999 / 2:.0f} s and 100,000 drones roughly "
      f"{per * 1e-9 * 100000 * 99999 / 2 / 60:.0f} minutes. Brute force becomes impractical for this "
      f"environment at a few thousand drones.")
    P("The inefficiency comes from the fact that every pair is treated as a separate, independent question: the "
      "algorithm does not use the positions of the points to rule out pairs that are obviously far apart. Most of "
      "the n(n - 1)/2 distances can never be the minimum, but they are still calculated. A redesigned strategy "
      "would have to avoid comparing points that are too far from each other to beat the best distance found so "
      "far, for example by ordering or partitioning the points in space so that each point is compared only with "
      "its neighbourhood, and by reusing the current best distance as a pruning limit.")


def q5():
    H1("Q5. A Convex Hull Algorithm from a Geometric Principle")
    H2("5.1 Derivation of the decision rule")
    P("Two different points p<sub>i</sub> = (x<sub>i</sub>, y<sub>i</sub>) and p<sub>j</sub> define a line. "
      "The position of a third point p<sub>k</sub> relative to the directed line from p<sub>i</sub> to p<sub>j</sub> "
      "is given by the sign of the cross product of the vectors p<sub>i</sub>p<sub>j</sub> and p<sub>i</sub>p<sub>k</sub>:")
    pseudo("""
s = (xj - xi)(yk - yi) - (yj - yi)(xk - xi)
s > 0 : pk lies to the left of the line
s < 0 : pk lies to the right of the line
s = 0 : pk lies on the line
""")
    P("The principle given in the assignment says that the segment p<sub>i</sub>p<sub>j</sub> can be part of the "
      "boundary only if all the other points lie on one side of the line. In terms of the sign, the segment is a "
      "hull edge if no pair of points k and l exists with s<sub>k</sub> &gt; 0 and s<sub>l</sub> &lt; 0. A point "
      "with s = 0 needs separate treatment: if it lies between p<sub>i</sub> and p<sub>j</sub> it does no harm, "
      "but if it lies outside the segment, then p<sub>i</sub>p<sub>j</sub> is only part of a longer boundary "
      "edge and must be rejected, because the longer segment between the two extreme points will be accepted "
      "instead. Duplicate points are removed first.")
    pseudo("""
remove duplicate points
for every pair (i, j), i < j
    seenLeft = seenRight = false ; ok = true
    for every other point k
        s = cross(pi, pj, pk)
        if s > 0: seenLeft = true
        else if s < 0: seenRight = true
        else if pk is not between pi and pj: ok = false ; stop
        if seenLeft and seenRight: ok = false ; stop
    if ok: accept edge (i, j)
hull vertices = end points of accepted edges
order the vertices by angle around their centroid (only for drawing)
""")
    H2("5.2 Test configurations")
    P("Set A has six points on a hexagon-like outer ring and thirty interior points, so it contains clear "
      "boundary and interior points. Set B was designed to challenge the rule: the four corners of a square, "
      "points in the middle of the sides and other points on the sides (collinear with the corners), a duplicated "
      "corner, interior grid points, and points very close to the boundary such as (19, 19) and (10, 1). Set C "
      "has eight collinear points, for which the hull degenerates into a segment.")
    t = [["Set", "Points given", "Distinct points", "Orientation tests", "Hull vertices"]]
    for r in Q5S:
        t.append([r[0], r[1], r[2], n_(r[3]), r[4]])
    table(t, widths=[20 * mm, 32 * mm, 36 * mm, 40 * mm, 32 * mm])
    P("Table 5.1: Results for the two designed sets (from results/q5set.csv)", cap)
    fig(os.path.join(GR, "q5_hull.png"), "Figure 5.1: Boundary found for set A (left) and set B (right)", 150)
    fig(os.path.join(SH, "q5_convex_hull_output.png"), "Figure 5.2: Program output for Q5", 160)
    P("For set B the algorithm returned exactly the four corners; the points at (10, 0), (20, 10), (5, 0) and "
      "(20, 15), which lie on the boundary but between corners, were correctly not reported as vertices, and the "
      "duplicate corner was reported once. For set C the result was the two end points of the line.")
    H2("5.3 Growth of the work")
    t = [["n", "Pairs", "Tests, random points", "Tests, points on a circle", "Hull vertices (random)", "Time (s)"]]
    for r in Q5:
        t.append([r[0], n_(r[1]), n_(r[2]), n_(r[3]), r[4], f"{float(r[5]):.4f}"])
    table(t, widths=[16 * mm, 24 * mm, 34 * mm, 38 * mm, 32 * mm, 20 * mm])
    P("Table 5.2: Orientation tests as the number of points grows (from results/q5.csv)", cap)
    fig(os.path.join(GR, "q5_growth.png"), "Figure 5.3: Orientation tests against n (logarithmic axes)", 115)
    P("There are n(n - 1)/2 pairs, and each pair is tested against at most n - 2 other points, so the worst case is "
      "n(n - 1)(n - 2)/2 orientation tests, which is O(n<super>3</super>). The measured counts grow by a factor "
      "of about 6.4 to 8 when n doubles, close to the factor of 8 of a cubic function. The counts are below the "
      "bound because a pair that is not a hull edge is usually rejected as soon as one point is found on each "
      "side. For 320 points the bound is about 16.2 million tests, and 3.2 million (random points) and 5.6 million "
      "(points on a circle) were needed. Points that are all on the hull give more tests, because the rejection "
      "of a pair takes longer to occur.")
    H2("5.4 Why an accepted edge belongs to the boundary")
    P("The convex hull of a set of points is the intersection of all half-planes that contain the whole set. If "
      "a line through p<sub>i</sub> and p<sub>j</sub> has every other point on one closed side of it, then that "
      "closed half-plane contains the whole set, and so it is one of the half-planes whose intersection forms "
      "the hull. The line therefore touches the hull, because it passes through p<sub>i</sub> and p<sub>j</sub>, "
      "which are points of the hull. The segment lies on the line, and it also lies inside the hull, as both of "
      "its end points are in the hull and the hull is convex. A segment that lies in the hull and on a supporting "
      "line must lie on the boundary, since an interior point of the hull has a small disc around it inside the "
      "hull, which would cross the supporting line. This is why one-sidedness is sufficient. It is also "
      "necessary: if points were on both sides, the line would pass through the interior of the hull. Collinear "
      "points need the extra rule because a supporting line may contain several points, and only the two "
      "extreme ones are vertices.")


def q6():
    H1("Q6. Exhaustive Search and Combinatorial Growth")
    H2("6.1 Design of the enumeration")
    P("A candidate solution is a subset of the n packages. A subset is represented as an n-bit number, in which "
      "bit i is 1 when package i is loaded. All candidates are generated by counting the integers from 0 to "
      "2<super>n</super> - 1. For each candidate the weights and values of the chosen packages are added; the "
      "candidate is feasible if the total weight does not exceed the payload limit, a feasible candidate is "
      "evaluated by its total value, and the best value and its bit pattern are retained whenever a feasible "
      "candidate improves them.")
    pseudo("""
best = -1
for mask = 0 to 2^n - 1
    w = 0 ; v = 0
    for i = 0 to n-1
        if bit i of mask is 1: w = w + weight[i] ; v = v + value[i]
    if w <= capacity and v > best: best = v ; bestMask = mask
return best, bestMask
""")
    H2("6.2 Correctness check on a small instance")
    items = [("P1", 7, 42), ("P2", 3, 12), ("P3", 4, 40), ("P4", 5, 25), ("P5", 2, 10)]
    limit = 10
    P("A small instance with five packages and a payload limit of 10 kg was created, so that all "
      "2<super>5</super> = 32 subsets can be written down and checked by hand. The packages are "
      "P1 (7 kg, value 42), P2 (3 kg, 12), P3 (4 kg, 40), P4 (5 kg, 25) and P5 (2 kg, 10). The feasible subsets "
      "are listed below; the other 16 exceed 10 kg.")
    t = [["Subset", "Weight", "Value"]]
    feas = []
    for r in range(6):
        for combo in itertools.combinations(items, r):
            w = sum(c[1] for c in combo)
            v = sum(c[2] for c in combo)
            if w <= limit:
                feas.append(("{" + ",".join(c[0] for c in combo) + "}", w, v))
    for name, w, v in feas:
        t.append([name, w, v])
    table(t, widths=[60 * mm, 25 * mm, 25 * mm])
    P("Table 6.1: Feasible subsets of the verification instance", cap)
    best = max(feas, key=lambda x: x[2])
    P(f"By inspection the best feasible subset is {best[0]} with weight {best[1]} kg and value {best[2]}. The "
      "exhaustive search returned exactly this subset and the same value, and an independent check that uses "
      "<font name='Mono'>itertools.combinations</font> gave the same result (output in Figure 6.1).")
    fig(os.path.join(SH, "q6_exhaustive_output.png"), "Figure 6.1: Program output for Q6", 140)
    H2("6.3 Growth: prediction and experiment")
    P("The number of subsets of n packages is 2<super>n</super>, because each package is independently either "
      "in or out. The prediction made before the experiment was therefore that the number of candidates "
      "doubles for every additional package, and that the execution time, which is proportional to the number "
      "of candidates (each needs an inner loop of n steps), roughly doubles as well.")
    t = [["n", "2^n", "Candidates examined", "Feasible", "Best value", "Time (s)", "Time ratio to previous n"]]
    prev = None
    for r in Q6:
        t.append([r[0], n_(r[1]), n_(r[2]), n_(r[3]), r[4], f"{float(r[5]):.4f}",
                  "-" if prev is None else f"{float(r[5]) / prev:.2f}"])
        prev = float(r[5])
    table(t, widths=[12 * mm, 28 * mm, 34 * mm, 26 * mm, 22 * mm, 20 * mm, 30 * mm])
    P("Table 6.2: Exhaustive search for increasing n, capacity 40 percent of the total weight (from "
      "results/q6.csv)", cap)
    fig(os.path.join(GR, "q6_candidates.png"), "Figure 6.2: Candidate subsets against n (logarithmic axis)", 110)
    fig(os.path.join(GR, "q6_time.png"), "Figure 6.3: Execution time against n (logarithmic axis)", 110)
    P("The number of candidates examined was exactly 2<super>n</super> for every size, so the prediction for "
      "the solution space was confirmed. The ratio of the times for n = 20 and n = 21 is about two, as "
      "predicted. The time ratios for two additional packages (n = 14 to 16, 16 to 18, 18 to 20) are about "
      "4 to 5, again consistent with 2<super>2</super> = 4 plus the extra inner-loop work.")
    H2("6.4 Why a few more packages are expensive")
    P("Every new package doubles the number of candidate subsets, because each of the existing subsets can be "
      "taken with or without it. Adding k packages therefore multiplies the work by 2<super>k</super>: ten more "
      "packages mean 1,024 times more candidates, and twenty more mean more than a million times. The "
      "increase in the size of the input is additive, but the solution space is multiplicative, and the "
      "algorithm examines the entire solution space.")
    H2("6.5 Deployment decision")
    per, nlim = float(Q6L[0]), int(Q6L[1])
    P(f"For the airlift planner I select a response time of 5 seconds, since a loading decision that is requested "
      f"interactively should appear while the operator is still looking at the screen. A candidate cost about "
      f"{per:.1f} microseconds in this environment, so n = {Q6[-1][0]} packages needed {float(Q6[-1][5]):.1f} s. "
      f"I would therefore deploy this exhaustive search only up to about {nlim} packages in this environment. "
      f"At 25 packages the same program would need about {per * 1e-6 * 2 ** 25:.0f} seconds, at 30 packages "
      f"about {per * 1e-6 * 2 ** 30 / 60:.0f} minutes and at 40 packages about "
      f"{per * 1e-6 * 2 ** 40 / 86400:.0f} days. A compiled language would shift this limit by only a few "
      "packages, since a speed-up of one hundred times is worth only about seven additional packages.")


def q7():
    H1("Q7. Day-4 Design Challenge: Diagnose, Redesign and Validate")
    P("The solution selected is the exhaustive search of Q6, because it is the only one of my solutions for which "
      "the experiments show a limit that cannot be removed by waiting for a faster machine: its effort doubles "
      "with every package.")
    H2("A. Diagnosis of the bottleneck")
    P("Almost all of the effort is spent in the double loop of the enumeration: 2<super>n</super> candidates are "
      "generated, and for each of them the inner loop makes n steps, so about n 2<super>n</super> additions are "
      "made. The operation that grows is therefore the generation and evaluation of a candidate, and in Table 6.2 "
      "the feasible candidates are only a quarter or less of the total, which means that most of the work is "
      "spent on subsets that are too heavy. For n = 20 only 223,607 of 1,048,576 candidates were feasible.")
    P("Work is also repeated. The weight and value of a subset are recalculated from zero although two "
      "subsets that differ only in the last package share all the other additions. More importantly, once a set "
      "of packages is already over the payload limit, every superset of it is also over the limit, but the "
      "enumeration still builds and tests all of them separately (a heavy set of k packages has "
      "2<super>n - k</super> supersets). The cause of the limitation is therefore a property of the original "
      "algorithm: it treats the candidates as unrelated and independent numbers, instead of as the leaves of a "
      "decision tree in which a decision on one package restricts all of the later ones.")
    H2("B. Design objective")
    P("The redesign must (1) avoid generating subsets that cannot be feasible or cannot beat the best load "
      "found so far, (2) reuse the partial weight and value instead of recomputing them, and (3) still return "
      "the exact optimum. The measurable objective is that, for random instances with n = 20, the number of "
      "search nodes visited should be at most 1 percent of the 2<super>n</super> candidates of the original, with "
      "the same best value on every instance that both programs can solve.")
    H2("C. The revised strategy")
    P("The candidates are organised as a decision tree. At depth i the algorithm decides whether to take package "
      "i, and it carries the weight and value of the decisions made so far, so that each node costs O(1) instead "
      "of O(n). Three changes are made. First, a branch that takes a package which would exceed the limit is not "
      "generated, so the whole subtree of overweight supersets disappears. Second, the packages are sorted "
      "in decreasing order of value per kg before the search, so the first complete loads found are good ones and "
      "the best value rises quickly. Third, a bound is calculated at every node: the value already collected "
      "plus the most that the remaining packages could add. The remaining packages can add at most their total "
      "value, and also at most the free capacity multiplied by the best density still available (the density "
      "of the next package, since they are sorted), so the smaller of the two is used. If this bound is not "
      "greater than the best value already found, the subtree cannot improve the solution and it is skipped.")
    pseudo("""
sort packages by value/weight, largest first
suffix[i] = total value of packages i..n-1
best = 0
search(i, w, v):
    if v > best: best = v
    if i == n: return
    bound = v + min(suffix[i], (capacity - w) * value[i] / weight[i])
    if bound <= best: return                      // prune: cannot improve
    search(i + 1, w, v)                           // leave package i
    if w + weight[i] <= capacity:                 // take package i only if feasible
        search(i + 1, w + weight[i], v + value[i])
""")
    P("The redesign introduces preprocessing of O(n log n) for the sort and O(n) memory for the suffix sums and "
      "the stack (the implementation uses an explicit stack). The new trade-off is that the running time is no "
      "longer fixed by n: it depends on the instance, and the worst case remains exponential.")
    H2("D. Prediction before implementation")
    P("I predicted that, on random instances, the number of nodes visited would be a very small fraction of "
      "2<super>n</super> and would not double with every package; that the saving would be smaller on strongly "
      "correlated instances (value equal to weight plus 10), because the density of all packages is then almost "
      "the same and the bound is weak; and that on instances where all packages have exactly the same density and "
      "the capacity cannot be filled exactly, the bound could never cut anything, so the advantage would almost "
      "vanish. The performance measure expected to improve is the number of candidates (nodes) examined.")
    H2("E. Implementation and comparison")
    for kind in ("random", "correlated", "equal density and odd capacity"):
        t = [["n", "Original: 2^n candidates", "Feasibility pruning only (nodes)", "Feasibility and bound (nodes)",
              "Best value", "Time of original (s)", "Time of redesign (s)"]]
        for r in Q7:
            if r[0] == kind:
                t.append([r[1], n_(r[2]), n_(r[3]) if r[3] else "-", n_(r[4]), r[5], r[6] if r[6] else "-", r[7]])
        P("Instance type: %s" % kind, ParagraphStyle("it", parent=body, fontName="Serif-B", alignment=0))
        table(t, widths=[10 * mm, 28 * mm, 28 * mm, 28 * mm, 18 * mm, 24 * mm, 24 * mm])
    P("Table 7.1: Original and redesigned search (from results/q7.csv). The original was run only up to n = 22; "
      "for larger n the number 2^n is shown. The best values of both programs were identical on every instance "
      "that both could solve.", cap)
    fig(os.path.join(GR, "q7_nodes.png"), "Figure 7.1: Candidates of the original and nodes of the redesign", 125)
    fig(os.path.join(SH, "q7_redesign_output.png"), "Figure 7.2: Program output for Q7", 160)
    H2("F. Evaluation")
    r20 = [r for r in Q7 if r[0] == "random" and r[1] == "20"][0]
    c20 = [r for r in Q7 if r[0] == "correlated" and r[1] == "20"][0]
    e24 = [r for r in Q7 if r[0] == "equal density and odd capacity" and r[1] == "24"][0]
    r40 = [r for r in Q7 if r[0] == "random" and r[1] == "40"][0]
    P(f"The first prediction was supported. For random instances with n = 20 the redesign visited "
      f"{int(r20[4]):,} nodes against {int(r20[2]):,} candidates, which is {int(r20[4]) / int(r20[2]) * 100:.3f} "
      f"percent, so the objective of 1 percent was met by a large margin, and with n = 40 it visited only "
      f"{int(r40[4]):,} nodes, where the original would have needed {int(r40[2]):,} candidates (about 10 "
      f"<super>12</super>), which is out of reach for it. Feasibility pruning alone reduced the work only to "
      f"about 60 percent of 2<super>n</super> (644,449 nodes at n = 20), so almost all of the improvement comes "
      f"from the bound and from the density order.")
    P(f"The second prediction was supported in direction but not in size. The correlated instance with n = 20 "
      f"needed {int(c20[4]):,} nodes, about ten times more than the random one, yet still only "
      f"{int(c20[4]) / int(c20[2]) * 100:.2f} percent of 2<super>n</super>; I had expected a weaker saving. "
      f"The third prediction was clearly supported: on the equal-density instance with an odd capacity, "
      f"n = 24 needed {int(e24[4]):,} nodes against {int(e24[2]):,} candidates, a saving of only about "
      f"{(1 - int(e24[4]) / int(e24[2])) * 100:.0f} percent, which is just the effect of the feasibility rule. "
      "The node count does not increase smoothly with n in the tables, because every row is a new random "
      "instance, so the counts depend on the instance, not only on n. This is the main new cost of the redesign: "
      "its running time cannot be predicted from n alone.")
    P("The redesign therefore addresses the limitation for typical instances: the planner could handle 40 "
      f"packages in a fraction of a second where the original is unusable beyond about {int(Q6L[1])}. It does not remove the "
      "exponential worst case, and no guarantee can be given for adversarial instances. The original "
      "exhaustive search is still preferable in three situations: when n is small (about 12 or less, where it "
      "takes milliseconds and is trivially correct), when a fixed and predictable response time is more "
      "important than speed on average, and as an independent reference used to verify the optimiser, which is "
      "how it was used here. The extra costs of the redesign are the sorting step, the memory for the stack and "
      "the more complicated code, whose correctness depends on the bound being valid; this was checked by "
      "comparing the best values with the original for every size up to 22.")


def conclusion():
    H1("Conclusion")
    P("The experiments in this assignment support four general conclusions. First, the best algorithm among "
      "several simple ones depends on the input: insertion sort is the right choice for nearly sorted orders and "
      "selection sort is never preferable unless swaps are expensive. Second, input size alone does not decide "
      "running time, as the string matching tests with identical n and m differed by a factor of ten. Third, the "
      "brute-force solutions of closest pair, convex hull and exhaustive search have polynomial or exponential "
      "growth that is predicted exactly by counting, and their practical limits were estimated from the "
      "measurements: a few thousand points for closest pair, a few hundred for the cubic hull, and "
      f"about {int(Q6L[1])} packages for the exhaustive search at a five-second response time. Fourth, a redesign that exploits "
      "the structure of the problem, such as pruning by feasibility and bound, can bring an exponential "
      "problem within reach for typical instances, but only an analysis of instances where it fails shows what "
      "the improvement really guarantees.")
    H2("References")
    for r in ["T. H. Cormen, C. E. Leiserson, R. L. Rivest and C. Stein, Introduction to Algorithms, 3rd edition, "
              "MIT Press, 2009.",
              "A. Levitin, Introduction to the Design and Analysis of Algorithms, 3rd edition, Pearson, 2012.",
              "D. E. Knuth, The Art of Computer Programming, Volume 3: Sorting and Searching, 2nd edition, "
              "Addison-Wesley, 1998."]:
        P(r, ParagraphStyle("ref", parent=body, leftIndent=12, firstLineIndent=-12, spaceAfter=3))


def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title="DAA Assignment 2 - 192465067", author="N D YOGESHWAR")

    def footer(c, d):
        c.saveState()
        c.setFont("Serif", 9)
        c.setFillColor(BLACK)
        c.drawString(22 * mm, 11 * mm, "DAA Assignment 2  |  N D YOGESHWAR  |  192465067")
        c.drawRightString(188 * mm, 11 * mm, f"Page {d.page}")
        c.restoreState()

    cover()
    q1()
    q2()
    q3()
    q4()
    q5()
    q6()
    q7()
    conclusion()
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    build()
