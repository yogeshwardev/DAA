import csv
import math
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
OUT = os.path.join(ROOT, "report", "DAA_A1_192465067.pdf")

REPO = "https://github.com/yogeshwardev/DAA-A1-192465067-N-D-YOGESHWAR"
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
h1 = ParagraphStyle("h1", parent=body, fontName="Serif-B", fontSize=15, leading=19, spaceBefore=10,
                    spaceAfter=7, alignment=0)
h2 = ParagraphStyle("h2", parent=body, fontName="Serif-B", fontSize=12, leading=16, spaceBefore=6,
                    spaceAfter=3, alignment=0)
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
    story.append(KeepTogether([Image(path, width=width * mm, height=width * mm * h / w), Paragraph(caption, cap)]))


def table(rows, widths=None, head=True):
    hs = ParagraphStyle("th", parent=small, fontName="Serif-B")
    rows = [[Paragraph(c, hs if (head and i == 0) else small) if isinstance(c, str) else c for c in r]
            for i, r in enumerate(rows)]
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, BLACK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story.append(t)
    story.append(Spacer(1, 8))


R = {}
with open(os.path.join(RES, "results.csv")) as f:
    for row in csv.DictReader(f):
        R[(int(row["n"]), row["algorithm"])] = row
T12 = {}
with open(os.path.join(RES, "task12_results.csv")) as f:
    for row in csv.DictReader(f):
        T12[row["design"]] = row

LIN, BIN, BST = "Linear search", "Binary search (recursive)", "BST search"
SIZES = [1000, 10000, 100000, 1000000]


def g(n, a, k):
    return float(R[(n, a)][k])


def nice(n):
    return f"{n:,}"


def cover():
    story.append(Spacer(1, 30 * mm))
    P("DESIGN AND ANALYSIS OF ALGORITHMS", ParagraphStyle("t1", parent=center, fontName="Serif-B", fontSize=18,
                                                          leading=24))
    P("Assignment 1 (CO1)", ParagraphStyle("t2", parent=center, fontName="Serif-B", fontSize=14, leading=20))
    story.append(Spacer(1, 10 * mm))
    P("Design, Analysis and Validation of an Efficient Search Strategy for a Large-Scale Student Record System",
      ParagraphStyle("t3", parent=center, fontName="Serif-I", fontSize=14, leading=20))
    story.append(Spacer(1, 18 * mm))
    table([["Submitted by", "N D YOGESHWAR"], ["Registration number", "192465067"],
           ["Dataset seed", "5067 (last four digits of the registration number)"],
           ["Third algorithm", "Binary Search Tree (group D)"],
           ["Programming language", "Python 3.11"],
           ["GitHub repository", f'<link href="{REPO}">{REPO}</link>']],
          widths=[50 * mm, 110 * mm], head=False)
    story.append(PageBreak())
    H1("Abstract")
    P("This report studies the problem of finding a student record from its registration number when the database "
      "grows from one thousand to one million records. Three different strategies were designed: linear "
      "search, recursive binary search on a sorted array, and search in a binary search tree. For each of them the "
      "basic operation was identified, the running time was derived mathematically for the best, average and "
      "worst cases, and the recurrence of the recursive algorithm was formed and solved. The algorithms were then "
      "implemented, run on datasets of 1,000, 10,000, 100,000 and 1,000,000 records and the measured comparison "
      "counts and times were compared with the theory. Finally the design was re-examined for a workload of "
      "50,000 searches per hour on one million records with one batch of new records per day.")
    P("The measured comparison counts followed the derived formulae closely. Binary search on a sorted array "
      "was found to be the most suitable design, and for the changed workload of Task 12 it is kept with a "
      "daily merge of new records in place of a full sort.")
    H2("Contents")
    for line in ["Task 1. Design of the algorithms", "Task 2. Basic operation", "Task 3. Time-complexity derivation",
                 "Task 4. Best, average and worst case", "Task 5. Asymptotic analysis",
                 "Task 6. Formulation of the recurrence", "Task 7. Solution of the recurrence",
                 "Task 8. Implementation and testing", "Task 9. Experimental performance",
                 "Task 10. Theory compared with experiment", "Task 11. Final design recommendation",
                 "Task 12. Day-4 design challenge", "Conclusion and references"]:
        P(line, ParagraphStyle("toc", parent=body, alignment=0, spaceAfter=2))
    story.append(PageBreak())


def task1():
    H1("Task 1. Design of the Algorithms")
    P("The registration numbers are unique integers that arrive in no particular order. Three strategies were "
      "chosen so that each of them treats the data in a different way: examining every record, reducing the problem "
      "by half after sorting, and restructuring the records into a tree. Linear and binary search are compulsory, "
      "and the binary search tree was selected as the third algorithm for roll-number group D.")
    H2("1.1 Algorithm 1: linear search (brute force, iterative)")
    P("The records are scanned from the first position, and each registration number is compared with the key "
      "until a match is found or the list ends. No preprocessing is needed, because the records can stay in the "
      "order of arrival. This method was selected because it is the simplest possible solution and gives the "
      "baseline against which the other two are judged.")
    pseudo("""
LinearSearch(data[0..n-1], key)
    for i = 0 to n-1
        if data[i] == key
            return i
    return -1
""")
    fig(os.path.join(GR, "flowchart1_linear_search.png"), "Figure 1.1: Flowchart of linear search", 85)
    H2("1.2 Algorithm 2: binary search (decrease and conquer, recursive)")
    P("When the array is sorted, the key is compared with the middle element. If they are equal the search ends; "
      "otherwise the key can lie only in one half, so the other half is discarded and the same step is applied "
      "to the remaining half. The records must be sorted once before the first search, and this preprocessing "
      "has a cost that must be counted. The method was selected to find out whether this one-time cost is "
      "worth paying, and it is the recursive approach required by the assignment.")
    pseudo("""
Sort(data)                              // preprocessing
BinarySearch(arr, key, low, high)
    if low > high
        return -1                       // base case
    mid = (low + high) / 2
    if arr[mid] == key
        return mid
    if key < arr[mid]
        return BinarySearch(arr, key, low, mid - 1)
    return BinarySearch(arr, key, mid + 1, high)
""")
    fig(os.path.join(GR, "flowchart2_binary_search.png"), "Figure 1.2: Flowchart of recursive binary search", 95)
    H2("1.3 Algorithm 3: binary search tree (transform and conquer, iterative)")
    P("In this approach the representation of the data is changed. Every record becomes a node of a tree; keys "
      "smaller than the key of a node are placed in its left subtree and larger keys in its right subtree. A search "
      "begins at the root and moves to the left or the right child at every node, so only one path from the root is "
      "followed. The preprocessing consists of inserting all records into the tree in the order of arrival. "
      "This strategy differs from binary search, because the structure is grown from the data and not obtained "
      "by sorting, and it also allows a single record to be added without sorting again. Both the build and the "
      "search were written with loops, so that a very deep tree cannot exceed the recursion limit of Python.")
    pseudo("""
Build(data)                             // preprocessing
    root = empty
    for each key in data
        cur = root
        while true
            if key < cur.key
                if cur.left is empty: cur.left = Node(key); break
                cur = cur.left
            else
                if cur.right is empty: cur.right = Node(key); break
                cur = cur.right

BSTSearch(root, key)
    cur = root
    while cur is not empty
        if key == cur.key
            return found
        if key < cur.key: cur = cur.left
        else:             cur = cur.right
    return not found
""")
    fig(os.path.join(GR, "flowchart3_bst_search.png"), "Figure 1.3: Flowchart of BST construction and search", 95)
    table([["", "Linear search", "Binary search", "BST search"],
           ["Design strategy", "Brute force", "Decrease and conquer", "Transform and conquer"],
           ["Implementation", "Iterative", "Recursive", "Iterative"],
           ["Preprocessing", "None", "Sorting the records", "Inserting all records into a tree"],
           ["Extra memory", "None", "A sorted copy", "One node (two pointers) per record"]],
          widths=[32 * mm, 38 * mm, 45 * mm, 52 * mm])
    P("Table 1.1: Summary of the three approaches", cap)


def task2():
    H1("Task 2. Basic Operation")
    P("In all three algorithms the time taken is governed by the number of comparisons between a stored "
      "registration number and the key. The other statements, such as changing an index or finding the middle "
      "position, are executed at most once for each comparison, so they change only the constant factor and not "
      "the way the running time grows with n. For this reason the comparison was taken as the basic operation.")
    P("In linear search the basic operation is the test <font name='Mono'>data[i] == key</font> in the body of the "
      "loop. It is executed once for every position that is visited, so its count equals the position of the key "
      "or n when the key is absent. If n becomes ten times larger, a search that has to travel through the list "
      "takes ten times as many comparisons.")
    fig(os.path.join(SH, "task02_basic_operation_linear.png"), "Figure 2.1: Basic operation of linear search "
        "(highlighted line)", 110)
    P("In recursive binary search the basic operation is the comparison of the key with "
      "<font name='Mono'>arr[mid]</font>, which is made once in every recursive call. Each call removes half of "
      "the remaining records, so the number of calls is the number of times n can be halved, a quantity that "
      "grows very slowly. The counter in the program is increased at exactly the place where this comparison is "
      "made.")
    fig(os.path.join(SH, "task02_basic_operation_binary.png"), "Figure 2.2: Basic operation of binary search "
        "(highlighted lines)", 110)
    P("In the tree search the basic operation is the comparison of the key with <font name='Mono'>cur.key</font> "
      "at every node that is visited. The number of comparisons equals the depth of the node where the search "
      "stops, so it depends on the height of the tree, and that in turn depends on the order in which the records "
      "were inserted. During construction the comparison <font name='Mono'>key &lt; cur.key</font> plays the "
      "same role.")
    fig(os.path.join(SH, "task02_basic_operation_bst.png"), "Figure 2.3: Basic operation of BST search "
        "(highlighted lines)", 110)


def task3():
    H1("Task 3. Derivation of the Time-Complexity Function")
    P("The input size n is the number of student records. C(n) denotes the number of key comparisons made by one "
      "search. The cost of preprocessing is added separately, because the assignment requires it to be part of "
      "the analysis.")
    H2("3.1 Linear search")
    P("If the key is at position i, the loop makes exactly i comparisons, and if the key is absent it makes n. "
      "Assuming that the key is equally likely to be at any of the n positions, "
      "C<sub>avg</sub>(n) = (1 + 2 + ... + n)/n = [n(n + 1)/2]/n = (n + 1)/2. "
      "Therefore C<sub>best</sub> = 1, C<sub>avg</sub> = (n + 1)/2 and C<sub>worst</sub> = n. There is no "
      "preprocessing, so the total cost of q searches is between q&middot;n/2 and q&middot;n, and the cost of "
      "one search is &Theta;(n).")
    H2("3.2 Binary search")
    P("After one comparison at most n/2 records remain, after two at most n/4, and after k comparisons at most "
      "n/2<super>k</super>. The search has to stop when the range becomes empty, that is when "
      "n/2<super>k</super> &lt; 1, which gives k &gt; log<sub>2</sub> n. Hence "
      "C<sub>worst</sub>(n) = floor(log<sub>2</sub> n) + 1. For n = 1,000,000 this equals 19 + 1 = 20, and the "
      "largest value recorded by the program in Task 9 is also 20.")
    P("For the average successful search the comparison tree can be used. One element is found with 1 "
      "comparison, two elements with 2, four with 3, and in general 2<super>j-1</super> elements with j comparisons. "
      "For n = 2<super>m</super> - 1 the total is S = &Sigma; j&middot;2<super>j-1</super> (j = 1 to m) "
      "= (m - 1)2<super>m</super> + 1, so C<sub>avg</sub> = S/n &asymp; m - 1 &asymp; log<sub>2</sub> n - 1.")
    P("The preprocessing is the sorting of n records, which costs &Theta;(n log n) for a comparison sort. The "
      "overall cost of q searches is therefore n log<sub>2</sub> n + q log<sub>2</sub> n = (n + q) log<sub>2</sub> n. "
      "Linear search needs about q&middot;n/2 comparisons for the same searches, so binary search becomes cheaper "
      "after only a few searches when n is large; Task 11 gives the number obtained from the measurements.")
    H2("3.3 Binary search tree")
    P("A search that ends at a node of depth d makes d comparisons, with the root at depth 1, so the cost depends "
      "on the shape of the tree. When the keys are inserted in random order, the expected depth of a node is "
      "D(n) = 2(1 + 1/n)H<sub>n</sub> - 4, where H<sub>n</sub> is the n-th harmonic number and "
      "H<sub>n</sub> &asymp; ln n + 0.577. This gives D(n) &asymp; 2 ln n - 2.85 = 1.39 log<sub>2</sub> n - 2.85, "
      "about 39 percent more than the best possible value. For n = 1,000,000 the formula gives "
      f"1.39 &times; 19.93 - 2.85 &asymp; 24.9, and the average measured for stored keys was "
      f"{g(1000000, BST, 'avg_comp_found'):.1f}. When the keys arrive in sorted order the tree degenerates into a "
      "chain and C<sub>worst</sub> = n.")
    P("The insertion of the i-th key costs about as many comparisons as the depth of its position, so building the "
      "tree costs &Sigma; 2 ln i &asymp; 2n ln n = &Theta;(n log n) on the average, and "
      "&Sigma; i = n(n + 1)/2 = &Theta;(n<super>2</super>) for sorted input. The overall cost of q searches on "
      "random input is about 2n ln n + q&middot;1.39 log<sub>2</sub> n.")
    table([["", "Preprocessing", "Search, average", "Search, worst", "n records and q searches"],
           ["Linear", "0", "(n + 1)/2", "n", "q&middot;n/2 on average"],
           ["Binary", "n log n", "log n - 1", "floor(log n) + 1", "n log n + q log n"],
           ["BST", "2n ln n on average, n&sup2;/2 worst", "1.39 log n - 2.85", "n", "2n ln n + q&middot;1.39 log n"]],
          widths=[20 * mm, 40 * mm, 34 * mm, 32 * mm, 44 * mm])
    P("Table 3.1: Derived cost functions", cap)


def task4():
    H1("Task 4. Best, Average and Worst Case")
    P("The cases arise from the position of the key in the data and, for the tree, from the order in which the "
      "records were inserted. Each case was also measured with the comparison counter on 100,000 records "
      "(Figure 4.1).")
    P("For linear search the best case occurs when the key is the first record, and a single comparison is enough. "
      "The worst case occurs when the key is the last record or is not present at all, and then all n records "
      "are examined, which is 100,000 comparisons for this dataset. If every position is equally likely, the "
      "search stops on average near the middle, (n + 1)/2, and a random sample of 2,000 stored keys gave "
      "about 50,576 against the theoretical 50,000. A search for a registration number that does not exist is always "
      "the worst case, which is important because such searches are common in a real system.")
    P("For binary search the best case is a key lying exactly at the first midpoint, one comparison. The worst case "
      "is a missing key or a key on the last level of the comparison tree, floor(log<sub>2</sub> n) + 1 = 17 comparisons "
      "for n = 100,000. Half of all the records are on the last level of that tree, and this is why the average "
      "successful search, about log<sub>2</sub> n - 1 &asymp; 15.7 comparisons, is only one or two comparisons "
      "below the worst case.")
    P("For the tree the best case is a key at the root. In the average case the tree is built from records in random "
      "order, so it is reasonably balanced and a typical node is about 1.39 log<sub>2</sub> n levels deep (about 21.5 "
      "was measured). The deepest node of this tree, which is the worst case for it, has depth 44. The real worst "
      "case occurs when the records arrive in sorted order, because then every new key goes to the right of the "
      "previous one and the tree becomes a linked list. This was demonstrated with 2,000 sorted records: the "
      "height was 2,000 and the last key needed 2,000 comparisons. A tree built in this way is therefore fast only "
      "when the insertion order is random.")
    fig(os.path.join(SH, "task04_case_counters.png"), "Figure 4.1: Counter output for the best, average and "
        "worst cases (n = 100,000)", 160)


def task5():
    H1("Task 5. Asymptotic Analysis")
    table([["Algorithm", "Best case", "Average case", "Worst case", "Remark"],
           ["Linear search", "&Omega;(1)", "&Theta;(n)", "&Theta;(n)", "O(n) overall"],
           ["Binary search", "&Omega;(1)", "&Theta;(log n)", "&Theta;(log n)", "after an O(n log n) sort"],
           ["BST search", "&Omega;(1)", "&Theta;(log n)", "&Theta;(n)", "&Theta;(log n) only for random order"]],
          widths=[32 * mm, 24 * mm, 30 * mm, 28 * mm, 52 * mm])
    P("Table 5.1: Asymptotic behaviour", cap)
    P("The lower bound &Omega;(1) is the same for all three, since the key may always be at the first place that is "
      "examined. The worst case is the one the system must be designed for. Preprocessing is &Theta;(n log n) "
      "for binary search (sorting) and for the tree built from random input, and it is absent for linear search.")
    rows = [["n", "log<sub>2</sub> n", "n log<sub>2</sub> n", "Linear: n", "Binary: log<sub>2</sub> n",
             "BST: 1.39 log<sub>2</sub> n"]]
    for n in SIZES:
        lg = math.log2(n)
        rows.append([nice(n), f"{lg:.2f}", nice(round(n * lg)), nice(n), f"{lg:.1f}", f"{1.39 * lg:.1f}"])
    table(rows, widths=[24 * mm, 22 * mm, 30 * mm, 28 * mm, 32 * mm, 32 * mm])
    P("Table 5.2: Growth of the functions from 10<super>3</super> to 10<super>6</super> records", cap)
    P("When the database grows from 1,000 to 1,000,000 records, which is a thousand times more data, the work of "
      "linear search also grows a thousand times, so a search that is unnoticeable at one thousand records "
      "becomes a delay of a few hundred milliseconds in this program at one million. For binary search "
      "log<sub>2</sub> n rises only from about 10 to about 20, so a thousand times more data costs just twice "
      "as many comparisons, and the tree behaves in the same way with a constant factor of about 1.39. A growth "
      "like n cannot be accepted for a large database, whereas a growth like log n can, and the price paid for "
      "it is the one-time preprocessing of order n log n.")


def task6():
    H1("Task 6. Formulation of the Recurrence Relation")
    P("The recurrence is formed for the recursive algorithm, which is the recursive binary search.")
    P("The size of the original problem is n = high - low + 1, the number of records still in the range. After the "
      "key has been compared with <font name='Mono'>arr[mid]</font> the function continues either on the left part "
      "(low to mid - 1) or on the right part (mid + 1 to high), and each of these contains at most floor(n/2) "
      "records. Hence the subproblem has size n/2. Only one of the two recursive calls in the code is executed "
      "for a given call, so the number of recursive calls is one. The work done outside the call consists of "
      "computing mid and making one comparison, which is a constant amount, taken as 1 basic operation. "
      "The recursion stops when low &gt; high; the range is then empty and no comparison is made, so T(0) = 0. "
      "A range of a single record makes one comparison and then calls itself on two empty ranges, so T(1) = 1.")
    P("Combining these facts, the worst case is described by")
    pseudo("""
T(n) = T(n/2) + 1     for n > 1
T(1) = 1
""")
    P("In the program the term '+ 1' is the statement <font name='Mono'>c[0] += 1</font>, and the term T(n/2) is the "
      "single <font name='Mono'>return binary_search(...)</font> on one half of the range.")


def task7():
    H1("Task 7. Solution of the Recurrence Relation")
    P("The iteration (backward substitution) method is applicable because the recurrence refers to only one "
      "smaller instance, T(n/2), which can be replaced repeatedly. Let n = 2<super>k</super>.")
    pseudo("""
T(n) = T(n/2) + 1
     = [T(n/4) + 1] + 1         = T(n/4) + 2
     = [T(n/8) + 1] + 2         = T(n/8) + 3
     ...
     = T(n / 2^i) + i
The recursion ends when n / 2^i = 1, i.e. i = log2 n, so
T(n) = T(1) + log2 n = 1 + log2 n
""")
    P("The result can be checked with the Master Theorem. The recurrence has the form T(n) = aT(n/b) + f(n) with "
      "a = 1, b = 2 and f(n) = 1. Since n<super>log<sub>b</sub> a</super> = n<super>0</super> = 1 and "
      "f(n) = &Theta;(1), the second case of the theorem applies and T(n) = &Theta;(log n).")
    P("The result can also be proved by substitution. Suppose T(n) &le; c log<sub>2</sub> n + 1 for n &ge; 2. Then "
      "T(n) = T(n/2) + 1 &le; c log<sub>2</sub>(n/2) + 1 + 1 = c log<sub>2</sub> n - c + 2, which is at most "
      "c log<sub>2</sub> n + 1 when c &ge; 1. The base case T(1) = 1 satisfies the assumption.")
    P("Thus T(n) = 1 + log<sub>2</sub> n = &Theta;(log n), in agreement with the count floor(log<sub>2</sub> n) + 1 "
      "of Task 3, which is the exact value when n is not a power of two. The result shows that every doubling "
      "of the database adds only one more comparison: one million records need about 20 comparisons and two "
      "million need about 21. The depth of the recursion is the same number, so there is no danger of exhausting "
      "the stack.")


def task8():
    H1("Task 8. Implementation and Testing")
    P("The three algorithms were implemented in Python in the files <font name='Mono'>algo1_linear_search.py</font>, "
      "<font name='Mono'>algo2_binary_search.py</font> and <font name='Mono'>algo3_bst_search.py</font>. The "
      "dataset generator uses the random seed 5067, which are the last four digits of the registration number "
      "192465067, and draws unique nine-digit numbers between 192,000,000 and 194,999,999. Every dataset "
      "contains 192465067 and never contains 192465068, and these two numbers are included in the test queries. "
      "All algorithms receive the same data and the same list of 202 queries, which consists of 101 stored keys "
      "and 101 absent keys.")
    P("The test cases are the first, last, middle, smallest and largest keys, three kinds of absent key, a list "
      "with a single element and an empty list. For 1,000, 10,000 and 100,000 records every query is also "
      "checked against a Python set to confirm that the three algorithms return the correct answer. For "
      "1,000,000 records the benchmark itself checks that the three algorithms agree on every query.")
    fig(os.path.join(SH, "task08_correctness_test.png"), "Figure 8.1: Output of the correctness tests", 165)
    P("The program was run with the commands <font name='Mono'>python benchmark.py --test</font> and "
      "<font name='Mono'>python benchmark.py --size n</font> for the four sizes. The complete instructions are in "
      "the README file of the repository.")


def task9():
    H1("Task 9. Experimental Performance")
    P("For every dataset the program recorded the time for preprocessing, the total time for the 202 searches, the "
      "average time for one search, and the average and maximum number of comparisons. The time was measured with "
      "<font name='Mono'>time.perf_counter()</font>. The comparison counter is inside the search functions, so "
      "the times include the small cost of counting, which is the same for all algorithms.")
    rows = [["n", "Algorithm", "Preprocessing (s)", "202 searches (s)", "Average time per search (&micro;s)",
             "Average comparisons", "Maximum comparisons"]]
    for n in SIZES:
        for a in (LIN, BIN, BST):
            rows.append([nice(n), a, f"{g(n, a, 'preprocess_s'):.4f}", f"{g(n, a, 'search_total_s'):.4f}",
                         f"{g(n, a, 'avg_search_us'):.2f}", f"{g(n, a, 'avg_comparisons'):.1f}",
                         nice(int(R[(n, a)]['max_comparisons']))])
    table(rows, widths=[20 * mm, 34 * mm, 24 * mm, 24 * mm, 28 * mm, 22 * mm, 22 * mm])
    P("Table 9.1: Measured results (taken from results.csv)", cap)
    for i, n in enumerate(SIZES, 1):
        fig(os.path.join(SH, f"task09_runtime_{n}.png"), f"Figure 9.{i}: Program output for n = {nice(n)} records", 150)
    fig(os.path.join(GR, "graph1_avg_search_time.png"), "Figure 9.5: Average time per search (logarithmic axes)", 125)
    fig(os.path.join(GR, "graph2_avg_comparisons.png"), "Figure 9.6: Average comparisons per search (logarithmic axes)", 125)
    fig(os.path.join(GR, "graph3_preprocessing_time.png"), "Figure 9.7: Preprocessing time (logarithmic axes)", 125)


def task10():
    H1("Task 10. Theory Compared with Experiment")
    fig(os.path.join(GR, "graph4_theory_vs_experiment.png"), "Figure 10.1: Measured comparisons (markers) and "
        "theoretical curves (lines)", 125)
    l1, l6 = g(1000, LIN, "avg_comparisons"), g(1000000, LIN, "avg_comparisons")
    b1, b6 = g(1000, BIN, "avg_comparisons"), g(1000000, BIN, "avg_comparisons")
    t1, t6 = g(1000, BST, "avg_comparisons"), g(1000000, BST, "avg_comparisons")
    heights = ", ".join(str(R[(n, BST)]["tree_height"]) for n in SIZES)
    P("The numbers of comparisons agree with the theory. Half of the queries are present keys and half are absent, so "
      f"the average for linear search should be (n/2 + n)/2 = 0.75n, and the measured values are {l1:.0f} for "
      f"n = 1,000 and {nice(round(l6))} for n = 1,000,000, a growth of {l6 / l1:.0f} times for a database that "
      f"is 1,000 times larger. Binary search went from {b1:.1f} to {b6:.1f} comparisons while log<sub>2</sub> n goes "
      f"from 9.97 to 19.93, and the tree went from {t1:.1f} to {t6:.1f}, always close to 1.3 times the binary "
      f"search value. The measured heights of the tree were {heights} for the four sizes, which is more than "
      "log<sub>2</sub> n, as is expected for a tree built from random input.")
    s1, s6 = g(1000, LIN, "avg_search_us"), g(1000000, LIN, "avg_search_us")
    q6, r6 = g(1000000, BIN, "avg_search_us"), g(1000000, BST, "avg_search_us")
    P(f"The running times do not follow the theory as exactly as the counts. The time of linear search grew "
      f"{s6 / s1:.0f} times, not 1,000 times. One possible reason is that a list of a million integers no longer "
      "fits in the processor cache, so each step becomes slower, and another is background activity on the "
      f"machine. The tree was faster per search than the recursive binary search at one million records "
      f"({r6:.1f} &micro;s against {q6:.1f} &micro;s) although it makes more comparisons ({t6:.1f} against "
      f"{b6:.1f}). The probable cause is the cost of function calls in Python, since every step of the recursive "
      "binary search is a function call whereas a step in the tree search is only one iteration of a loop. "
      "The iterative binary search used in Task 12 removes a large part of this difference. Small irregularities "
      "in the table, such as the binary search time at 100,000 records, are caused by timing noise, because "
      "202 searches take only a few milliseconds. The comparison counts are free of this noise, and therefore "
      "they were used to confirm the growth rates.")
    P("Binary search and the tree both scale much better than linear search because their work grows with log n. "
      "Between these two, binary search needs fewer comparisons and a much cheaper preprocessing "
      f"({g(1000000, BIN, 'preprocess_s'):.2f} s against {g(1000000, BST, 'preprocess_s'):.2f} s at one million "
      "records), whereas the tree gave slightly faster searches in Python. The preprocessing times agree with "
      f"n log n: from 100,000 to 1,000,000 records the sorting time grew "
      f"{g(1000000, BIN, 'preprocess_s') / g(100000, BIN, 'preprocess_s'):.1f} times and the tree building time "
      f"{g(1000000, BST, 'preprocess_s') / g(100000, BST, 'preprocess_s'):.1f} times, while n log n predicts 12.0. "
      "The tree grows more slowly than predicted because its nodes are scattered in memory.")


def task11():
    H1("Task 11. Final Design Recommendation")
    pre = g(1000000, BIN, "preprocess_s")
    lin_one = g(1000000, LIN, "avg_search_us") / 1e6
    P("Binary search on a sorted array is recommended for the student record system.")
    P("From the theory, the worst-case cost of a search is exactly floor(log<sub>2</sub> n) + 1 comparisons, so "
      "an unfavourable arrangement of the data cannot make a search slower, and the only extra cost is the "
      f"O(n log n) sort. In the experiment at 1,000,000 records the sort took {pre:.2f} s, after which a search took "
      f"about {g(1000000, BIN, 'avg_search_us'):.1f} &micro;s with at most 20 comparisons, whereas a linear search "
      f"took about {lin_one * 1000:.0f} ms and up to 1,000,000 comparisons. The sort costs as much as roughly "
      f"{pre / lin_one:.0f} linear searches, so the sorted array is ahead from the fourth search onward, and a "
      "university database is certainly searched more often than that.")
    P("The tree was not chosen for the following reasons. Its searches were slightly faster in the Python tests, but "
      f"building it took {g(1000000, BST, 'preprocess_s'):.1f} s, which is about "
      f"{g(1000000, BST, 'preprocess_s') / pre:.0f} times the sorting time. It needs a node object with two "
      "pointers for every record and therefore much more memory than a list of numbers. Its worst case is n if "
      "the records arrive in sorted order, which is quite possible when registration numbers are issued in sequence, "
      "so it offers no guarantee comparable to that of binary search. Linear search is acceptable for 1,000 records, "
      f"where a search takes about {g(1000, LIN, 'avg_search_us') / 1000:.1f} ms and no preprocessing is needed, "
      f"but it needs about {g(100000, LIN, 'avg_search_us') / 1000:.0f} ms at 100,000 records and about "
      f"{g(1000000, LIN, 'avg_search_us') / 1000:.0f} ms at 1,000,000 records.")
    P("The main limitation of the sorted array is that it has to stay sorted. Inserting a record into the middle "
      "moves about half of the array, so many small insertions are expensive, and this is handled by batching the "
      "updates in Task 12. If records were added continuously in random order, a balanced tree such as an AVL tree or "
      "a B-tree would be better than the plain tree used here. The solution remains practical as the database grows, "
      "because a thousand times more data adds only about ten comparisons, and even ten million records would "
      "need about 23.")


def task12():
    H1("Task 12. Day-4 Design Challenge")
    lin = [v for k, v in T12.items() if k.startswith("Linear")][0]
    brec = T12["Binary search - original (recursive)"]
    bit = T12["Binary search - iterative"]
    bst = T12["BST search"]
    hs = T12["Hash table (set) - revised index"]
    f = lambda d, k: float(d[k])
    H2("12.A Impact analysis")
    P("The workload is now defined: 50,000 searches per hour, about 14 per second or 1.2 million per day, on "
      "1,000,000 records, and new records are added only once a day. In the original problem the number of "
      "searches was not known, so only the cost of one search was compared with the cost of preprocessing. "
      "Now the number of searches q is known and very large, and this changes the assumption on which "
      "preprocessing is judged. A one-time cost is shared by 1.2 million searches a day and becomes small, "
      "whereas a cost paid on every search, such as the 300 ms of linear search, is multiplied by 50,000. Because "
      "updates are rare, the weak point of the sorted array, which is slow insertion, hardly matters, since it "
      "has to be repaired only once a day and in a single batch.")
    H2("12.B Evaluation of the original design")
    P("The original recommendation was binary search on a sorted array. It was measured with 50,000 searches "
      f"(25,000 stored and 25,000 absent keys) on 1,000,000 records. The recursive version took "
      f"{f(brec, 'search_50000_s'):.2f} s and the iterative version {f(bit, 'search_50000_s'):.2f} s. As the hour "
      f"has 3,600 s, this is {f(bit, 'search_50000_s') / 3600 * 100:.3f} percent of the available time, which is "
      f"easily acceptable, and the sort of {f(brec, 'preprocess_s'):.2f} s is needed only once a day. Linear search "
      f"would need about {f(lin, 'search_50000_s'):,.0f} s for the same searches (estimated from a smaller number of "
      f"measured searches), which is about {f(lin, 'search_50000_s') / 3600:.1f} hours of work for every hour of "
      f"load, so it can never keep up. The tree needed {f(bst, 'search_50000_s'):.2f} s for the searches but "
      f"{f(bst, 'preprocess_s'):.1f} s to be built. A hash table needed only {f(hs, 'search_50000_s'):.3f} s, about "
      f"{f(bit, 'search_50000_s') / f(hs, 'search_50000_s'):.0f} times less than iterative binary search, with a "
      f"build time of {f(hs, 'preprocess_s'):.2f} s. Another approach can therefore be faster, but binary search "
      "is already far faster than the requirement.")
    H2("12.C Adaptation: the design is modified")
    P("The sorted array with binary search is retained, with two changes. First, the daily update no longer sorts "
      "the whole array again. The new records of the day (1,000 were simulated) are sorted separately and merged "
      "with the existing sorted array in one pass, which costs O(n + m) in place of O(n log n). The measured times "
      f"were {f(bst, 'daily_update_resort_s'):.3f} s for a complete sort and {f(bst, 'daily_update_merge_s'):.3f} s "
      "for the merge. Second, the iterative form of the search is used, because it avoids a function call at each "
      f"step ({f(brec, 'us_per_search'):.1f} &micro;s against {f(bit, 'us_per_search'):.1f} &micro;s per search). "
      "The search remains O(log n), and the daily update changes from O(n log n) to O(n + m log m). If only exact "
      "lookups of registration numbers were ever needed, a hash index could be added later, with expected O(1) "
      "lookup.")
    fig(os.path.join(SH, "task12_challenge_benchmark.png"), "Figure 12.1: Benchmark of 50,000 searches on "
        "1,000,000 records with the daily update costs", 150)
    fig(os.path.join(GR, "graph5_task12_50000_searches.png"), "Figure 12.2: Time for 50,000 searches", 120)
    H2("12.D Defence of the decision")
    rows = [["Design", "Preprocessing (s)", "50,000 searches (s)", "Search time for one day (s)"]]
    for d in (lin, brec, bit, bst, hs):
        rows.append([d["design"], f"{f(d, 'preprocess_s'):.3f}", f"{f(d, 'search_50000_s'):,.3f}",
                     f"{f(d, 'search_50000_s') * 24:,.1f}"])
    table(rows, widths=[75 * mm, 25 * mm, 34 * mm, 36 * mm])
    P("Table 12.1: Results of the Task 12 benchmark. The linear search row is estimated from a smaller number of "
      "measured searches, since 50,000 linear searches would take several hours.", cap)
    P("The decision follows from four quantities. As regards the frequency of searches, 14 searches per second can be "
      "served by any design that answers in microseconds, and only linear search fails, being about "
      f"{f(lin, 'search_50000_s') / f(bit, 'search_50000_s'):,.0f} times slower than iterative binary search. "
      f"As regards preprocessing, the sort needs about {f(brec, 'preprocess_s'):.1f} s a day against about "
      f"{f(bit, 'search_50000_s') * 24:.0f} s of searching, and with merging only "
      f"{f(bst, 'daily_update_merge_s'):.2f} s. As regards the size of the data, binary search needs at most 20 "
      f"comparisons for 1,000,000 records, while the tree needs {f(bst, 'preprocess_s'):.0f} s to be built, "
      "which makes it the worst choice when the structure has to be rebuilt. As regards trade-offs, the hash "
      "table is fastest for single lookups but cannot answer ordered or range questions, for example all the "
      "students of one batch, and it uses more memory, whereas the sorted array supports these questions and "
      "is the smaller structure. Since the system needs far less speed than binary search provides, the simplest "
      "design with a guaranteed worst case is kept. The original solution is therefore modified and not replaced.")


def conclusion():
    H1("Conclusion")
    P("Three search strategies were designed, analysed mathematically and tested on datasets from 1,000 to "
      "1,000,000 records. The derived costs, n/2 for linear search, log<sub>2</sub> n for binary search and about "
      "1.39 log<sub>2</sub> n for a tree built from random input, were confirmed by the measured comparison counts. "
      "Binary search on a sorted array gave the best balance of preprocessing cost, guaranteed worst case and "
      "memory, and it was kept for the changed workload of Task 12 with a daily merge of new records.")
    H2("References")
    for r in ["T. H. Cormen, C. E. Leiserson, R. L. Rivest and C. Stein, Introduction to Algorithms, 3rd edition, "
              "MIT Press, 2009.",
              "A. Levitin, Introduction to the Design and Analysis of Algorithms, 3rd edition, Pearson, 2012.",
              "D. E. Knuth, The Art of Computer Programming, Volume 3: Sorting and Searching, 2nd edition, "
              "Addison-Wesley, 1998."]:
        P(r, ParagraphStyle("ref", parent=body, leftIndent=12, firstLineIndent=-12, spaceAfter=3))


def build():
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title="DAA Assignment 1 - 192465067", author="N D YOGESHWAR")

    def footer(c, d):
        c.saveState()
        c.setFont("Serif", 9)
        c.setFillColor(BLACK)
        c.drawString(22 * mm, 11 * mm, "DAA Assignment 1  |  N D YOGESHWAR  |  192465067")
        c.drawRightString(188 * mm, 11 * mm, f"Page {d.page}")
        c.restoreState()

    cover()
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()
    task11()
    task12()
    conclusion()
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    build()
