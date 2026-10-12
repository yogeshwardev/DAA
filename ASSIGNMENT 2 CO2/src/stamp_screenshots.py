import glob
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "screenshots", "raw")
OUT = os.path.join(HERE, "..", "screenshots")
TEXT = "N D YOGESHWAR  |  Reg No 192465067"


def main():
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 16)
    files = sorted(glob.glob(os.path.join(RAW, "*.png")) + glob.glob(os.path.join(RAW, "*.jpg")))
    for path in files:
        img = Image.open(path).convert("RGB")
        w, h = img.size
        canvas = Image.new("RGB", (w, h + 34), "white")
        canvas.paste(img, (0, 0))
        d = ImageDraw.Draw(canvas)
        tw = d.textlength(TEXT, font=font)
        d.text((w - tw - 12, h + 8), TEXT, font=font, fill="black")
        name = os.path.splitext(os.path.basename(path))[0] + ".png"
        canvas.save(os.path.join(OUT, name))
        print("stamped", name)
    if not files:
        print("no images found in", RAW)


if __name__ == "__main__":
    main()
