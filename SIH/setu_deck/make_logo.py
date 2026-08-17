"""Patch the SIH logo bitmap so the year reads 2026 instead of 2025.

The template ships a small 181x92 logo (ppt/media/image2.png). We upscale it,
paint over the year and re-draw "2026" in a bold face that matches the
original digits, then save it as a normal PNG the deck can place.
"""

import os
import zipfile

from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ASSETS = os.path.join(HERE, "assets")
TEMPLATE = os.path.join(ROOT, "Sih-ppt-template-2025-pdf-download.pptx")
OUT = os.path.join(ASSETS, "sih_logo_2026.png")

SCALE = 8
SLATE = (65, 83, 93, 255)
FONT = r"C:\Windows\Fonts\verdanab.ttf"

# year box in the original 181x92 logo (measured from the bitmap)
YEAR = (105, 56, 153, 75)


def build():
    os.makedirs(ASSETS, exist_ok=True)
    with zipfile.ZipFile(TEMPLATE) as z:
        raw = z.read("ppt/media/image2.png")
    tmp = os.path.join(ASSETS, "_sih_src.png")
    with open(tmp, "wb") as fh:
        fh.write(raw)

    src = Image.open(tmp).convert("RGBA")
    w, h = src.size
    big = src.resize((w * SCALE, h * SCALE), Image.LANCZOS)

    x0, y0, x1, y1 = [v * SCALE for v in YEAR]
    # wipe the old year
    ImageDraw.Draw(big).rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4],
                                  fill=(255, 255, 255, 0))

    target_h = (75 - 59) * SCALE          # cap height of the original digits
    size = 10
    while True:
        f = ImageFont.truetype(FONT, size + 2)
        bb = ImageDraw.Draw(big).textbbox((0, 0), "2026", font=f)
        if bb[3] - bb[1] > target_h:
            break
        size += 2
    font = ImageFont.truetype(FONT, size)

    # draw the year on its own layer so we can soften it to match the
    # resolution of the rest of the (upscaled) logo
    layer = Image.new("RGBA", big.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    bb = d.textbbox((0, 0), "2026", font=font)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    cx = (105 + 153) / 2 * SCALE
    d.text((cx - tw / 2 - bb[0], 59 * SCALE - bb[1]), "2026",
           font=font, fill=SLATE)
    layer = layer.filter(ImageFilter.GaussianBlur(SCALE * 0.16))
    big = Image.alpha_composite(big, layer)

    big.save(OUT)
    os.remove(tmp)
    print("logo ->", OUT, big.size)
    return OUT


if __name__ == "__main__":
    build()
