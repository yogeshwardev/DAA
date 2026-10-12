import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "..", "results", "logs")
SHOTS = os.path.join(HERE, "..", "screenshots")
os.makedirs(SHOTS, exist_ok=True)
FONT = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
BOLD = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
STAMP = "N D YOGESHWAR  |  Reg No 192465067"
LINE_H = 22


def render(lines, title, name, highlight=None, numbered=False, start_line=1):
    cw = FONT.getlength("M")
    width = int(max(len(l) for l in lines) * cw) + 60 + (50 if numbered else 0)
    width = max(width, 760)
    height = 40 + len(lines) * LINE_H + 70
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width - 1, height - 1], outline="black")
    d.line([(0, 32), (width, 32)], fill="black")
    d.text((12, 8), title, font=BOLD, fill="black")
    y = 44
    for i, line in enumerate(lines):
        no = start_line + i
        x = 20
        hl = bool(highlight and no in highlight)
        if hl:
            d.rectangle([8, y - 2, width - 8, y + LINE_H - 3], fill="black")
        if numbered:
            d.text((x, y), f"{no:>3}", font=FONT, fill="white" if hl else "black")
            x += 50
        d.text((x, y), line, font=FONT, fill="white" if hl else "black")
        y += LINE_H
    d.line([(0, height - 38), (width, height - 38)], fill="black")
    stamp_w = d.textlength(STAMP, font=BOLD)
    d.text((width - stamp_w - 16, height - 28), STAMP, font=BOLD, fill="black")
    img.save(os.path.join(SHOTS, name))
    print("wrote", name)


def from_log(logname, title, shotname):
    with open(os.path.join(LOGS, logname), encoding="ascii") as f:
        lines = f.read().rstrip("\n").split("\n")
    render(lines, "C:\\DAA-A1\\src>  " + title, shotname)


def code_shot(srcfile, needle, title, shotname):
    with open(os.path.join(HERE, srcfile), encoding="utf-8") as f:
        lines = f.read().rstrip("\n").split("\n")
    needles = needle if isinstance(needle, tuple) else (needle,)
    hits = [i + 1 for i, l in enumerate(lines) if any(n in l for n in needles)]
    render(lines, title, shotname, highlight=hits, numbered=True)


if __name__ == "__main__":
    from_log("dataset_generator.txt", "python dataset_generator.py", "task08_dataset_generator.png")
    from_log("task08_correctness_test.txt", "python benchmark.py --test", "task08_correctness_test.png")
    from_log("task04_case_counters.txt", "python benchmark.py --cases", "task04_case_counters.png")
    for n, label in ((1000, "1000"), (10000, "10000"), (100000, "100000"), (1000000, "1000000")):
        from_log(f"task09_n{n}.txt", f"python benchmark.py --size {n}", f"task09_runtime_{label}.png")
    from_log("task12_challenge.txt", "python task12_challenge.py", "task12_challenge_benchmark.png")
    code_shot("algo1_linear_search.py", "data[i] == key", "algo1_linear_search.py  (basic operation highlighted)",
              "task02_basic_operation_linear.png")
    code_shot("algo2_binary_search.py", ("_c[0] += 1", "if arr[mid] == key:"), "algo2_binary_search.py  (basic operation highlighted)",
              "task02_basic_operation_binary.png")
    code_shot("algo3_bst_search.py", ("comparisons += 1", "if key == cur.key:"), "algo3_bst_search.py  (basic operation highlighted)",
              "task02_basic_operation_bst.png")
