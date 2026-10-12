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


def render(lines, title, name):
    cw = FONT.getlength("M")
    width = max(int(max(len(l) for l in lines) * cw) + 50, 760)
    height = 40 + len(lines) * LINE_H + 70
    img = Image.new("RGB", (width, height), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width - 1, height - 1], outline="black")
    d.line([(0, 32), (width, 32)], fill="black")
    d.text((12, 8), title, font=BOLD, fill="black")
    y = 44
    for line in lines:
        d.text((20, y), line, font=FONT, fill="black")
        y += LINE_H
    d.line([(0, height - 38), (width, height - 38)], fill="black")
    w = d.textlength(STAMP, font=BOLD)
    d.text((width - w - 16, height - 28), STAMP, font=BOLD, fill="black")
    img.save(os.path.join(SHOTS, name))
    print("wrote", name)


def shot(log, title, name, start=None, stop=None):
    with open(os.path.join(LOGS, log + ".txt"), encoding="ascii") as f:
        lines = [l.rstrip("\n") for l in f if not l.startswith("CSV,")]
    while lines and not lines[-1].strip():
        lines.pop()
    lines = lines[start:stop]
    render(lines, "C:\DAA-A2\src>  python " + title, name)


if __name__ == "__main__":
    shot("q1_sorting", "q1_sorting.py", "q1_sorting_output.png")
    shot("q2_sequential", "q2_sequential.py", "q2_sequential_output.png")
    shot("q3_string_matching", "q3_string_matching.py", "q3_string_matching_output.png")
    shot("q4_closest_pair", "q4_closest_pair.py", "q4_closest_pair_output.png")
    shot("q5_convex_hull", "q5_convex_hull.py", "q5_convex_hull_output.png")
    shot("q6_exhaustive", "q6_exhaustive.py", "q6_exhaustive_output.png")
    shot("q7_redesign", "q7_redesign.py", "q7_redesign_output.png")
