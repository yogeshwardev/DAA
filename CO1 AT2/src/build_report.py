import math
import os
import subprocess
import sys

from PIL import Image as PILImage, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, Preformatted, SimpleDocTemplate,
                                Spacer, Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "report", "CSA06_CO1_192465067.pdf")
SHOT = os.path.join(ROOT, "report", "verify_output.png")
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
h1 = ParagraphStyle("h1", parent=body, fontName="Serif-B", fontSize=14, leading=18, spaceBefore=10, spaceAfter=6,
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


def table(rows, widths=None, head=True):
    hs = ParagraphStyle("th", parent=small, fontName="Serif-B")
    rows = [[Paragraph(str(c), hs if (head and i == 0) else small) for c in r] for i, r in enumerate(rows)]
    t = Table(rows, colWidths=widths, repeatRows=1 if head else 0)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.6, BLACK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story.append(t)
    story.append(Spacer(1, 8))


def render_output():
    out = subprocess.run([sys.executable, os.path.join(HERE, "verify.py")], capture_output=True, text=True,
                         check=True).stdout
    lines = out.rstrip("\n").split("\n")
    font = ImageFont.truetype(F + "consola.ttf", 15)
    bold = ImageFont.truetype(F + "arialbd.ttf", 15)
    cw = font.getlength("M")
    width = int(max(len(l) for l in lines) * cw) + 50
    height = 40 + len(lines) * 21 + 70
    img = PILImage.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width - 1, height - 1], outline="black")
    d.line([(0, 32), (width, 32)], fill="black")
    d.text((12, 8), "C:\\CSA06\\src>  python verify.py", font=bold, fill="black")
    for i, l in enumerate(lines):
        d.text((20, 44 + i * 21), l, font=font, fill="black")
    d.line([(0, height - 38), (width, height - 38)], fill="black")
    stamp = "N D YOGESHWAR  |  Reg No 192465067"
    d.text((width - d.textlength(stamp, font=bold) - 16, height - 28), stamp, font=bold, fill="black")
    img.save(SHOT)
    return width, height


def cover():
    story.append(Spacer(1, 12 * mm))
    P("Department of Computer Science and Engineering", ParagraphStyle("t0", parent=center, fontName="Serif-B",
                                                                       fontSize=13, leading=18))
    P("CSA06 - Design and Analysis of Algorithms", ParagraphStyle("t1", parent=center, fontName="Serif-B",
                                                                  fontSize=16, leading=22))
    P("CO1 - Assessment Tool 1: IT Application-Based Problem Solving", center)
    P("Scalability Audit of an E-Commerce Platform (ShopSphere)", ParagraphStyle("t2", parent=center,
                                                                                  fontName="Serif-I", fontSize=13))
    story.append(Spacer(1, 10 * mm))
    table([["Student Reg. No.", "192465067"], ["Student Name", "N D YOGESHWAR"],
           ["Course outcome assessed", "Determine algorithm efficiency using asymptotic notations and mathematical "
            "techniques including the Master Theorem and the substitution method"],
           ["Mode", "Individual"],
           ["Assumption", "Servers execute 10<super>8</super> basic operations per second; nightly window of "
            "10 minutes = 6 x 10<super>10</super> operations"]], widths=[50 * mm, 110 * mm], head=False)
    P("Notation. log means log<sub>2</sub>. n is the number of products in the catalogue. The two sizes studied are "
      "the present n = 100,000 and the expected n = 1,000,000.")


def part_a():
    H1("(a) Understanding the problem")
    table([["Module", "Input size", "Basic operation and where it occurs", "Expected growth of the count"],
           ["M1 duplicate detector", "n products",
            "Comparison Product[i].title = Product[j].title, the first test of the IF in the inner loop. It is "
            "executed for every pair (i, j) with i &lt; j. The seller comparison is made only when the titles "
            "are equal, so it is executed no more often.",
            "Quadratic. n x 10 gives 100 times more comparisons."],
           ["M2 rate limiter", "n, the largest window that is audited",
            "The call Audit(Request[j]) in the inner FOR loop, executed once for every request in every window.",
            "The windows have sizes 1, 2, 4, ..., so the total is a geometric sum, linear in n."],
           ["M3 search, S1", "n products in the unsorted catalogue",
            "Comparison of the key with the product in the scan, once per examined entry.",
            "Linear in n for a failed search; n/2 on average for a hit."],
           ["M3 search, S2", "n entries in the sorted index",
            "Comparison of the key with the middle entry, once per recursion or loop step.",
            "Logarithmic: one more comparison each time n is doubled."],
           ["M4 recommendation engine", "n, size of the customer-product data",
            "The linear-time merging of partial results, f(n) = n operations at each node of the recursion tree.",
            "Current design: quadratic, because 4 subproblems of half size are created. Redesign: n log n."],
           ["M5 sales analytics", "n sales records",
            "The comparisons of the sort that is done at every level, f(n) = n log n at the top node.",
            "Slightly more than n log n: all levels together cost about n log<super>2</super> n."]],
          widths=[28 * mm, 26 * mm, 70 * mm, 40 * mm])
    P("The report generator is not a recursive module; the profile gives its operation count directly as "
      "f(n) = 3n<super>2</super> + 10n log n + 50, in which the term 3n<super>2</super> will dominate.")


def part_b():
    H1("(b) Analysis of the iterative modules")
    H2("Module M1")
    P("The outer loop variable i runs from 0 to n - 2. For a fixed i the inner loop variable j runs from i + 1 to "
      "n - 1, which is n - 1 - i values. The comparison is executed at every iteration, because there is no "
      "early exit (a duplicate is only marked).")
    pseudo("""
C(n) = sum for i = 0 to n-2 of (n - 1 - i)
     = (n-1) + (n-2) + ... + 2 + 1
     = (n - 1) n / 2
     = n^2/2 - n/2
""")
    P("Time complexity: C(n) = n(n - 1)/2 is of the form n<super>2</super>/2 - n/2, therefore T(n) = &Theta;(n<super>2</super>), "
      "and the same count is obtained in the best, average and worst case, since the loops do not depend on the data. "
      "Space complexity: only the loop counters i and j are needed, so the extra space is &Theta;(1) (the "
      "catalogue itself, of size n, is the input). For n = 100,000 the count is 4,999,950,000 and for "
      "n = 1,000,000 it is 499,999,500,000.")
    H2("Module M2")
    P("Let the values taken by i be 1, 2, 4, ... The loop runs while i &lt; n. If k is the smallest integer with "
      "2<super>k</super> &ge; n, that is k = ceil(log n), then the values are i = 2<super>0</super>, 2<super>1</super>, ..., "
      "2<super>k-1</super>, and the outer loop therefore runs k times. In the iteration with the value i the "
      "inner loop makes exactly i calls to Audit, not n calls. The total is a geometric series:")
    pseudo("""
A(n) = 2^0 + 2^1 + ... + 2^(k-1) = 2^k - 1,   k = ceil(log2 n)
""")
    P("Since 2<super>k</super> &ge; n and 2<super>k</super> &lt; 2n, we get n - 1 &le; A(n) &lt; 2n - 1. For n a power of "
      "two, A(n) = n - 1 exactly. Hence A(n) = &Theta;(n).")
    P("The claim of the team member is not correct as a tight bound. It is true that the outer loop runs about log n "
      "times and that the inner loop never runs more than n times, so the cost is O(n log n), and an O(n log n) "
      "bound is a valid upper bound, but it is not tight. The error is to multiply the number of iterations of the "
      "outer loop by the largest value of the inner loop: the inner loop runs n/2<super>j</super> times fewer in "
      "the earlier iterations, and only the last iteration costs about n/2. The tight bound is &Theta;(n).")
    P("Verification for n = 1,024. The values of i are 1, 2, 4, 8, 16, 32, 64, 128, 256, 512 (the value 1,024 is "
      "not less than n and the loop stops), which is k = 10 iterations. The count is 2<super>10</super> - 1 = 1,023 = n - 1. "
      "The claim of n log n would give 1,024 x 10 = 10,240 operations, about ten times more than the real count. "
      "The program output in Figure 1 shows the counted value 1,023 for n = 1,024.")


def part_c():
    H1("(c) Recurrence of search version S2 by backward substitution")
    P("The recurrence is T(n) = T(n/2) + 1 with T(1) = 1. Assume n = 2<super>k</super> at first.")
    pseudo("""
T(n) = T(n/2) + 1
     = [ T(n/4) + 1 ] + 1              = T(n/2^2) + 2
     = [ T(n/8) + 1 ] + 2              = T(n/2^3) + 3
     ...
     = T(n/2^i) + i                    (after i substitutions)
Stop when n/2^i = 1, i.e. i = log2 n:
T(n) = T(1) + log2 n = 1 + log2 n
""")
    P("Check: T(2) = T(1) + 1 = 2 = 1 + log 2; T(16) = 5 = 1 + 4. For an n that is not a power of two the "
      "halving takes the floor, and the exact closed form is T(n) = floor(log<sub>2</sub> n) + 1; for "
      "n = 1,000,000 it is 19 + 1 = 20. Time complexity: &Theta;(log n).")
    table([["Implementation", "Time", "Space", "Reason"],
           ["Iterative (low, high loop)", "&Theta;(log n)", "&Theta;(1)",
            "One comparison per halving; only low, high and mid are stored."],
           ["Recursive", "&Theta;(log n)", "&Theta;(log n)",
            "The same number of comparisons, but every halving adds a stack frame, so the depth of the "
            "recursion is floor(log n) + 1."]], widths=[40 * mm, 28 * mm, 28 * mm, 68 * mm])
    P("Interpretation: with n = 1,000,000 the index needs at most 20 comparisons, and a doubling of the "
      "catalogue costs only one more. For the platform the memory of the recursive version (about 20 frames) is "
      "negligible, so both versions are acceptable; the iterative one is preferable on a busy server because it "
      "avoids the call overhead.")


def part_d():
    H1("(d) The Master Theorem for M4 and M5")
    P("Form: T(n) = aT(n/b) + f(n), compared with n<super>log<sub>b</sub> a</super>.")
    table([["", "Current design of M4", "Proposed redesign of M4"],
           ["Recurrence", "T(n) = 4T(n/2) + n", "T(n) = 2T(n/2) + n"],
           ["a, b, f(n)", "a = 4, b = 2, f(n) = n", "a = 2, b = 2, f(n) = n"],
           ["n^(log_b a)", "n<super>log<sub>2</sub> 4</super> = n<super>2</super>", "n<super>log<sub>2</sub> 2</super> = n"],
           ["Comparison", "f(n) = n = O(n<super>2-&epsilon;</super>) with &epsilon; = 1: f grows polynomially slower",
            "f(n) = n = &Theta;(n): the same growth"],
           ["Case", "Case 1", "Case 2"],
           ["Result", "T(n) = &Theta;(n<super>2</super>)", "T(n) = &Theta;(n log n)"]],
          widths=[30 * mm, 70 * mm, 64 * mm])
    P("Exact solutions with T(1) = 1 are T(n) = 2n<super>2</super> - n for the current design and "
      "T(n) = n log n + n for the redesign (both were confirmed by a program for n = 2, 16 and 1,024).")
    P("When the data doubles, the quadratic design takes T(2n)/T(n) = (2(2n)<super>2</super> - 2n)/(2n<super>2</super> - n) "
      "&asymp; 4 times as long: a catalogue twice as large means four times the work. The redesign needs "
      "T(2n)/T(n) = 2n(log n + 2)/(n(log n + 1)) = 2(1 + 1/(log n + 1)), about 2.1 times for n = 10<super>6</super>, "
      "which is almost linear. The redesign is therefore not only faster but also scales proportionally.")
    H2("Module M5: T(n) = 2T(n/2) + n log n")
    P("Here a = 2, b = 2, n<super>log<sub>2</sub> 2</super> = n and f(n) = n log n. Case 2 needs f(n) = &Theta;(n) and "
      "is not satisfied, since n log n is larger. Case 3 needs f(n) = &Omega;(n<super>1+&epsilon;</super>) for some "
      "&epsilon; &gt; 0, but n log n / n = log n grows more slowly than any n<super>&epsilon;</super>, so Case 3 does "
      "not apply. Case 1 fails since f is larger than n. Therefore none of the three standard cases applies; "
      "the gap between f(n) and n is only a logarithmic factor.")
    P("The extended Master Theorem covers f(n) = &Theta;(n<super>log<sub>b</sub> a</super> log<super>k</super> n) with "
      "k &ge; 0, and gives T(n) = &Theta;(n<super>log<sub>b</sub> a</super> log<super>k+1</super> n). Here k = 1, so "
      "T(n) = &Theta;(n log<super>2</super> n). The same follows from the recursion tree:")
    pseudo("""
level i has 2^i nodes, each of size n/2^i, each costing (n/2^i) log(n/2^i)
cost of level i = 2^i * (n/2^i) * log(n/2^i) = n (log n - i)
levels i = 0 .. log n - 1:
sum = n [ log n + (log n - 1) + ... + 1 ] = n log n (log n + 1) / 2
plus the n leaves of cost T(1) = 1  ->  T(n) = n log n (log n + 1)/2 + n = Theta(n log^2 n)
""")
    P("Interpretation: sorting at every level of the recursion costs a factor of log n more than sorting "
      "once. For n = 1,000,000, log n &asymp; 20, so M5 does about 2.1 x 10<super>8</super> operations instead of "
      "about 2 x 10<super>7</super>.")


def part_e():
    H1("(e) Best, average and worst cases of S1 and S2")
    table([["", "Best case", "Average case", "Worst case"],
           ["S1 sequential search", "Key is the first product: 1 comparison",
            "Key present, equally likely at any position: (n + 1)/2",
            "Key is last or absent: n comparisons"],
           ["S2 binary search", "Key is the middle entry of the index: 1 comparison",
            "Key present: about log n - 1 comparisons",
            "Key absent or on the last level: floor(log n) + 1 comparisons"]],
          widths=[34 * mm, 42 * mm, 46 * mm, 42 * mm])
    P("For n = 1,000,000: S1 needs 1, about 500,000.5 and 1,000,000 comparisons; S2 needs 1, about 18.9 and 20 "
      "comparisons. In S2 half of all the entries are on the last level of the comparison tree, which is why "
      "the average is only one or two comparisons below the worst case.")
    H2("Average number of comparisons of S1 with probability p")
    P("If the product exists (probability p) and every position is equally likely, the expected number of "
      "comparisons is (1 + 2 + ... + n)/n = (n + 1)/2. If it does not exist (probability 1 - p) all n entries are "
      "examined. By the law of total expectation:")
    pseudo("""
C_avg(n, p) = p (n + 1)/2 + (1 - p) n
            = n (1 - p/2) + p/2
n = 1,000,000 and p = 0.5:
C_avg = 0.5 x 500,000.5 + 0.5 x 1,000,000 = 250,000.25 + 500,000 = 750,000.25 comparisons
""")
    P("Interpretation: when half of the searches are for products that are not in the catalogue, the average "
      "cost rises from n/2 to 0.75n, and the failed searches contribute two thirds of the work. For S2 with "
      "p = 0.5 the average is about 0.5 x 18.9 + 0.5 x 20 &asymp; 19.5 comparisons, so the presence of missing "
      "products makes almost no difference to it.")


def part_f():
    H1("(f) Proof that f(n) = 3n<super>2</super> + 10n log<sub>2</sub> n + 50 is &Theta;(n<super>2</super>)")
    P("Definition: f(n) = &Theta;(g(n)) if there are positive constants c<sub>1</sub>, c<sub>2</sub> and n<sub>0</sub> such "
      "that c<sub>1</sub> g(n) &le; f(n) &le; c<sub>2</sub> g(n) for all n &ge; n<sub>0</sub>. Here g(n) = n<super>2</super>.")
    P("<b>Lower bound.</b> For n &ge; 1 every term of f(n) is non-negative, so f(n) &ge; 3n<super>2</super>. "
      "Hence c<sub>1</sub> = 3 works for n &ge; 1.")
    P("<b>Upper bound.</b> We need 10n log n + 50 &le; (c<sub>2</sub> - 3) n<super>2</super>. Choose c<sub>2</sub> = 4, so "
      "that we need 10n log n + 50 &le; n<super>2</super> for n &ge; n<sub>0</sub>. At n = 64 the left side is "
      "10 x 64 x 6 + 50 = 3,890 and the right side is 4,096, so the inequality holds. For n &ge; 64: "
      "10 n log n = n<super>2</super> (10 log n / n), and the factor 10 log n / n is decreasing for n &ge; 3 (the "
      "derivative of log n / n is negative beyond e), so it is at most 60/64 = 0.9375. Therefore "
      "10n log n &le; 0.9375 n<super>2</super>, and the remaining 50 &le; 0.0625 n<super>2</super> since "
      "0.0625 x 64<super>2</super> = 256. So f(n) &le; 4n<super>2</super> for n &ge; 64.")
    P("Thus 3n<super>2</super> &le; f(n) &le; 4n<super>2</super> for all n &ge; 64, with c<sub>1</sub> = 3, c<sub>2</sub> = 4 and "
      "n<sub>0</sub> = 64, and f(n) = &Theta;(n<super>2</super>). (A cruder but simpler choice is c<sub>2</sub> = 63 and "
      "n<sub>0</sub> = 1, since log n &le; n and 1 &le; n<super>2</super> for n &ge; 1. The values near the boundary were "
      "checked by a program: f(59) &gt; 4 x 59<super>2</super> and f(60) &le; 4 x 60<super>2</super>, so the constant "
      "n<sub>0</sub> = 64 is safe.)")
    P("<b>f(n) is not O(n).</b> Suppose that f(n) &le; cn for some constant c and all n &ge; n<sub>1</sub>. Since "
      "f(n) &ge; 3n<super>2</super>, this would give 3n<super>2</super> &le; cn, that is n &le; c/3, for every "
      "n &ge; n<sub>1</sub>. This is false for n = max(n<sub>1</sub>, ceil(c/3) + 1). The assumption is therefore wrong "
      "and f(n) is not O(n). In the same way f(n) is not o(n<super>2</super>). "
      "Interpretation: only the term 3n<super>2</super> matters for the scalability of the report generator, and "
      "reducing the n log n or constant terms will not change its growth.")


def part_g():
    H1("(g) Scalability decision")
    n = 10 ** 6
    L = math.log2(n)
    data = [("M1", "n(n-1)/2", n * (n - 1) / 2), ("M2", "2<super>20</super> - 1", 2 ** 20 - 1),
            ("S2 (one search)", "floor(log n) + 1", math.floor(L) + 1),
            ("M4 current", "2n<super>2</super> - n", 2 * n * n - n), ("M4 redesign", "n log n + n", n * L + n),
            ("M5", "n log n (log n + 1)/2 + n", n * L * (L + 1) / 2 + n),
            ("Report generator", "3n<super>2</super> + 10n log n + 50", 3 * n * n + 10 * n * L + 50)]
    t = [["Module", "Operation count", "Operations for n = 10<super>6</super>", "Time at 10<super>8</super> op/s",
          "Fits 10-minute window (6 x 10<super>10</super> op)?"]]
    for name, formula, ops in data:
        secs = ops / 1e8
        shown = f"{secs:.2e} s" if secs < 0.01 else (f"{secs:.2f} s" if secs < 3600 else f"{secs:,.0f} s ({secs / 3600:.1f} h)")
        t.append([name, formula, f"{ops:.3e}", shown, "Yes" if secs <= 600 else "<b>No</b>"])
    table(t, widths=[28 * mm, 40 * mm, 34 * mm, 34 * mm, 28 * mm])
    P("For comparison, at the present n = 100,000: M1 needs 5.0 x 10<super>9</super> operations (50 s), M4 current "
      "2.0 x 10<super>10</super> (200 s) and the report generator 3.0 x 10<super>10</super> (300 s); all fit in 600 s today, "
      "and all three fail after the expansion because they are quadratic, so a tenfold growth costs a hundredfold "
      "time.")
    P("<b>Modules that fail the 10-minute window at n = 1,000,000:</b> M1 (about 5,000 s, 83 minutes), the current "
      "M4 (about 20,000 s, 5.6 hours) and the report generator (about 30,000 s, 8.3 hours). M2, S2, the redesigned "
      "M4 and M5 are comfortably within the window (0.01 s, 0.2 microseconds, 0.21 s and 2.1 s).")
    H2("Recommendations")
    P("<b>M1 must be redesigned.</b> The duplicate test depends only on equality of the pair (title, seller), so "
      "comparing every pair is unnecessary. Build a hash table keyed on (title, seller) and mark a product as a "
      "duplicate when its key is already in the table: expected &Theta;(n) time and &Theta;(n) space, about "
      "10<super>6</super> operations (0.01 s). If memory is a concern, sort the products by (title, seller) in "
      "&Theta;(n log n) (about 2 x 10<super>7</super> operations, 0.2 s) and compare only neighbouring "
      "records. Both bring the module far below the window; the price is the extra memory of the hash table "
      "or the sort.")
    P("<b>M4 must adopt the proposed redesign.</b> Removing the replication changes a = 4 to a = 2, which moves "
      "the recurrence from Case 1 (&Theta;(n<super>2</super>)) to Case 2 (&Theta;(n log n)): about 2.1 x 10<super>7</super> "
      "operations instead of 2 x 10<super>12</super>, an improvement of about 100,000 times. The replicated "
      "partitions presumably give availability, so that requirement has to be met by another means (copying "
      "data without recomputing on it).")
    P("<b>The report generator must also be redesigned.</b> Its dominant term is 3n<super>2</super>, which suggests a nested "
      "loop over the catalogue; as for M1 the inner pass should be replaced by a sort followed by one scan, or by "
      "a hash-based aggregation, to reach &Theta;(n log n) or &Theta;(n).")
    P("<b>M5 is acceptable</b> at about 2 seconds, but it re-sorts at every level. If the sort were done "
      "once at the top, or if a merge were used to combine already sorted halves, the recurrence would become "
      "T(n) = 2T(n/2) + n, that is &Theta;(n log n), saving a further factor of about 10. This is optional.")
    P("<b>M2 and S2</b> need no change. M2 is linear (about one million audits), and S2 needs 20 comparisons, so "
      "it should replace the sequential search S1 for every interactive lookup, whose worst case of 10<super>6</super> "
      "comparisons (0.01 s) would cost thousands of seconds of processor time if many users search at once. "
      "The sorted index only has to be maintained when products are added.")
    P("Figure 1 shows the output of the program that checks the formulae of this report.")
    w, h = PILImage.open(SHOT).size
    width = min(165, w * 0.2)
    story.append(KeepTogether([Image(SHOT, width=width * mm, height=width * mm * h / w),
                               Paragraph("Figure 1: Verification of the derived formulae by counting", cap)]))


def certification():
    H1("Code of Conduct")
    P("I N D YOGESHWAR / 192465067 certify that this submission is my original work and that I have adhered to "
      "the guidelines specified for this assessment. I understand that any violation of academic integrity rules "
      "will result in disciplinary action.")
    P("Signature of the Student: ____________________          Date: ______________")


def build():
    render_output()
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title="CSA06 CO1 - 192465067", author="N D YOGESHWAR")

    def footer(c, d):
        c.saveState()
        c.setFont("Serif", 9)
        c.drawString(22 * mm, 11 * mm, "CSA06 CO1  |  N D YOGESHWAR  |  192465067")
        c.drawRightString(188 * mm, 11 * mm, f"Page {d.page}")
        c.restoreState()

    cover()
    part_a()
    part_b()
    part_c()
    part_d()
    part_e()
    part_f()
    part_g()
    certification()
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print("wrote", os.path.abspath(OUT))


if __name__ == "__main__":
    build()
