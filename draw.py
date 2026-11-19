#!/usr/bin/env python3
"""Draw entry.png: one-image summary of the world news of Thursday 19 November 2026.

Layout: newspaper front page, 1024x1024. Header band names the day; six story
panels (3 x 2), each with a flat drawn illustration, a short headline and one
factual sub-line. Every story was verified against at least two news sources.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
RED = (192, 57, 43)
SUB = (74, 74, 68)
CARD = (255, 255, 255)
BORDER = (217, 210, 194)
GOLD = (183, 149, 11)

BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def star_points(cx, cy, r_out, r_in, rot=-90):
    pts = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 36)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_flag_us(d, x, y, w, h):
    stripe = h / 7.0
    for i in range(7):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=c)
    cw, ch = w * 0.4, stripe * 4
    d.rectangle([x, y, x + cw, y + ch], fill=(30, 60, 114))
    for r in range(3):
        for c in range(3):
            px = x + 6 + c * (cw - 10) / 2
            py = y + 5 + r * (ch - 8) / 2
            d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6], fill=(255, 255, 255))
    d.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)


def draw_flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    d.polygon(star_points(x + w * 0.22, y + h * 0.28, 9, 3.6), fill=(255, 222, 0))
    for sx, sy in [(0.55, 0.18), (0.68, 0.32), (0.66, 0.52), (0.5, 0.62)]:
        d.polygon(star_points(x + w * sx, y + h * sy, 4, 1.6), fill=(255, 222, 0))
    d.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)


def draw_flag_ru(d, x, y, w, h):
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=c)
    d.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)


def draw_skyline(d, x, y, w, h, color):
    import random
    rnd = random.Random(7)
    bx = x
    while bx < x + w - 18:
        bw = rnd.randint(16, 30)
        bh = rnd.randint(int(h * 0.35), int(h * 0.95))
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=color)
        for wy in range(int(y + h - bh + 6), int(y + h - 4), 10):
            for wx in range(int(bx + 4), int(bx + bw - 4), 9):
                if rnd.random() < 0.5:
                    d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
        bx += bw + 4


def draw_burst(d, cx, cy, r, color):
    d.polygon(star_points(cx, cy, r, r * 0.35), fill=color)
    d.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3], fill=(255, 255, 255))


def ill_summit(d, x, y, w, h):
    # three flags on poles over a skyline
    draw_skyline(d, x + 10, y + h - 52, w - 20, 52, (31, 52, 86))
    fw, fh = 74, 48
    gap = (w - 3 * fw) / 4
    flags = [draw_flag_us, draw_flag_cn, draw_flag_ru]
    for i, fn in enumerate(flags):
        fx = x + gap + i * (fw + gap)
        d.line([fx + fw / 2, y + 8, fx + fw / 2, y + 8 + fh + 26], fill=(90, 90, 90), width=3)
        d.ellipse([fx + fw / 2 - 3, y + 4, fx + fw / 2 + 3, y + 10], fill=GOLD)
        fn(d, fx, y + 10, fw, fh)


def ill_scales(d, x, y, w, h):
    cx, cy = x + w / 2, y + 18
    d.line([cx, cy, cx, cy + 108], fill=(40, 40, 40), width=5)
    d.line([cx - 78, cy + 14, cx + 78, cy + 14], fill=(40, 40, 40), width=5)
    for sx in (cx - 78, cx + 78):
        d.line([sx, cy + 14, sx - 26, cy + 62], fill=(40, 40, 40), width=3)
        d.line([sx, cy + 14, sx + 26, cy + 62], fill=(40, 40, 40), width=3)
        d.arc([sx - 26, cy + 52, sx + 26, cy + 78], 0, 180, fill=(183, 149, 11), width=5)
    d.rectangle([cx - 52, cy + 108, cx + 52, cy + 118], fill=(40, 40, 40))
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=GOLD)


def ill_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54))
    for i in range(40):
        px = x + (i * 67) % w
        py = y + (i * 41) % 60
        d.ellipse([px, py, px + 2, py + 2], fill=(255, 255, 255))
    # tower
    tx, tw = x + w * 0.55, 46
    d.polygon([(tx, y + h), (tx + 10, y + 42), (tx + tw - 10, y + 42),
               (tx + tw, y + h)], fill=(120, 130, 150))
    for wy in range(int(y + 52), int(y + h - 6), 12):
        d.line([tx + 6, wy, tx + tw - 6, wy], fill=(70, 80, 100), width=2)
    # missile arc
    d.arc([x + 10, y + 30, x + w - 90, y + 150], 200, 340, fill=(255, 214, 90), width=4)
    draw_burst(d, x + w - 70, y + 52, 26, (255, 180, 40))
    d.polygon([(x + w - 96, y + 88), (x + w - 82, y + 96), (x + w - 70, y + 92)],
              fill=(255, 214, 90))


def ill_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 234, 245))
    deck_y = y + 78
    d.rectangle([x + 8, deck_y, x + w - 8, deck_y + 12], fill=(70, 80, 90))
    for px in (x + w * 0.3, x + w * 0.72):
        d.rectangle([px - 5, y + 18, px + 5, deck_y], fill=(50, 60, 70))
        d.line([px, y + 18, x + 14, deck_y], fill=(90, 100, 110), width=2)
        d.line([px, y + 18, x + w - 14, deck_y], fill=(90, 100, 110), width=2)
    draw_burst(d, x + w / 2, deck_y - 6, 22, (255, 120, 30))
    for wy in range(int(y + 108), int(y + h - 6), 14):
        for wx in range(int(x + 10), int(x + w - 10), 26):
            d.arc([wx, wy, wx + 22, wy + 10], 180, 360, fill=(31, 97, 141), width=2)


def ill_tank(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 205))
    # dashed ceasefire line
    for dx in range(int(x + 6), int(x + w - 6), 18):
        d.line([dx, y + h - 34, dx + 11, y + h - 34], fill=(192, 57, 43), width=3)
    cx, cy = x + w / 2, y + 66
    d.rounded_rectangle([cx - 78, cy - 6, cx + 78, cy + 26], 8, fill=(74, 86, 60))
    d.rounded_rectangle([cx - 34, cy - 30, cx + 30, cy - 4], 6, fill=(90, 102, 74))
    d.line([cx + 28, cy - 18, cx + 88, cy - 30], fill=(60, 70, 48), width=7)
    for i in range(5):
        wx = cx - 58 + i * 29
        d.ellipse([wx - 11, cy + 26, wx + 11, cy + 48], fill=(40, 44, 34))
        d.ellipse([wx - 4, cy + 33, wx + 4, cy + 41], fill=(150, 150, 140))
    d.rectangle([x + 14, y + h - 22, x + 44, y + h - 8], fill=(160, 140, 110))
    d.rectangle([x + 52, y + h - 16, x + 74, y + h - 8], fill=(150, 128, 96))


def ill_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 245, 233))
    ox, oy = x + 26, y + h - 30
    d.line([ox, oy, x + w - 16, oy], fill=(60, 60, 60), width=3)
    d.line([ox, oy, ox, y + 14], fill=(60, 60, 60), width=3)
    bars = [34, 52, 44, 74, 66, 96]
    bw = (w - 70) / len(bars)
    pts = []
    for i, v in enumerate(bars):
        bx = ox + 8 + i * bw
        d.rectangle([bx, oy - v, bx + bw - 10, oy], fill=(39, 174, 96))
        pts.append((bx + (bw - 10) / 2, oy - v - 8))
    d.line(pts, fill=(30, 132, 73), width=4, joint="curve")
    ax, ay = pts[-1]
    d.polygon([(ax, ay - 14), (ax + 16, ay + 2), (ax - 2, ay + 6)], fill=(30, 132, 73))


PANELS = [
    dict(accent=(31, 97, 141), tag="DIPLOMACY  ·  SHENZHEN",
         head="TRUMP, XI, PUTIN MEET IN SHENZHEN",
         sub="First three-way summit ends with a joint peace declaration.",
         ill=ill_summit),
    dict(accent=(17, 122, 101), tag="JUSTICE  ·  THE HAGUE",
         head="MYANMAR COMMITTED GENOCIDE",
         sub="UN court rules on the Rohingya case — a first.",
         ill=ill_scales),
    dict(accent=(146, 43, 33), tag="CONFLICT  ·  THE GULF",
         head="IRAN WAR WIDENS TO GULF STATES",
         sub="Iran fires on Gulf states; Riyadh tower damaged.",
         ill=ill_missile),
    dict(accent=(26, 82, 118), tag="WAR  ·  UKRAINE",
         head="UKRAINE HITS CRIMEAN BRIDGE",
         sub="Third attack on the bridge in a week, Russia says.",
         ill=ill_bridge),
    dict(accent=(147, 81, 22), tag="CONFLICT  ·  GAZA",
         head="ISRAEL PUSHES INTO GAZA",
         sub="Tanks cross the ceasefire line; hospital strike kills six.",
         ill=ill_tank),
    dict(accent=(30, 132, 73), tag="MARKETS  ·  NEW YORK",
         head="ANTHROPIC'S $83 NASDAQ DEBUT",
         sub="AI firm lists at $83 a share in a record debut.",
         ill=ill_chart),
]


def fit_lines(d, text, path, sizes, width, max_lines=2):
    """Largest size from `sizes` whose wrap fits in max_lines lines."""
    for size in sizes:
        fnt = font(path, size)
        if len(wrap(d, text, fnt, width)) <= max_lines:
            return fnt, wrap(d, text, fnt, width)
    fnt = font(path, sizes[-1])
    return fnt, wrap(d, text, fnt, width)[:max_lines]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # header band
    d.rectangle([0, 0, W, 140], fill=NAVY)
    d.text((32, 20), "THE WORLD IN ONE IMAGE", font=font(BOLD, 25), fill=(255, 214, 90))
    d.text((32, 52), "THURSDAY 19 NOVEMBER 2026", font=font(BOLD, 56), fill=(255, 255, 255))
    # globe icon, top right
    gx, gy, gr = 940, 70, 42
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=(255, 214, 90), width=4)
    d.ellipse([gx - gr * 0.45, gy - gr, gx + gr * 0.45, gy + gr], outline=(255, 214, 90), width=3)
    d.line([gx - gr, gy, gx + gr, gy], fill=(255, 214, 90), width=3)
    d.arc([gx - gr, gy - gr * 0.5, gx + gr, gy + gr * 0.5], 0, 180, fill=(255, 214, 90), width=3)
    # red rule
    d.rectangle([0, 140, W, 146], fill=RED)

    # panels 3 x 2
    margin, gutter = 16, 12
    pw = (W - 2 * margin - 2 * gutter) // 3
    ph = (990 - 158 - gutter) // 2
    for i, p in enumerate(PANELS):
        col, row = i % 3, i // 3
        x = margin + col * (pw + gutter)
        yy = 158 + row * (ph + gutter)
        d.rectangle([x, yy, x + pw, yy + ph], fill=CARD, outline=BORDER, width=2)
        d.rectangle([x, yy, x + pw, yy + 6], fill=p["accent"])
        d.text((x + 14, yy + 16), p["tag"], font=font(BOLD, 17), fill=p["accent"])
        p["ill"](d, x + 14, yy + 44, pw - 28, 168)
        hfnt, hlines = fit_lines(d, p["head"], BOLD, [29, 27, 25], pw - 28)
        hy = yy + 222
        for ln in hlines:
            d.text((x + 14, hy), ln, font=hfnt, fill=INK)
            hy += 35 if hfnt.size >= 29 else 32
        sfnt, slines = fit_lines(d, p["sub"], REG, [20, 19, 18], pw - 28)
        sy = yy + 296
        for ln in slines:
            d.text((x + 14, sy), ln, font=sfnt, fill=SUB)
            sy += 26 if sfnt.size >= 20 else 24

    d.text((W // 2, 1002), "Sources: AP, Reuters, BBC, NYT — 19 Nov 2026",
           font=font(REG, 15), fill=(120, 112, 96), anchor="ma")
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
