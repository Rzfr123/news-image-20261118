#!/usr/bin/env python3
"""Render the news-image-20261118 entry: a newspaper front page summing up
Wednesday 18 November 2026. Output: entry.png (1024x1024, deterministic)."""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (176, 42, 32)
BLUE = (31, 58, 95)
GREY = (96, 96, 96)
SAND = (214, 196, 150)
SEA = (140, 180, 205)
LIGHT_BLUE = (170, 200, 220)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, xy, s, f, fill=INK):
    draw.text(xy, s, font=f, fill=fill)


def text_c(draw, cx, y, s, f, fill=INK):
    w = draw.textlength(s, font=f)
    draw.text((cx - w / 2, y), s, font=f, fill=fill)


def wrap(draw, s, f, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, s, f, max_w, fill=INK, leading=6):
    lh = f.size + leading
    for i, line in enumerate(wrap(draw, s, f, max_w)):
        draw.text((x, y + i * lh), line, font=f, fill=fill)
    return y + len(wrap(draw, s, f, max_w)) * lh


def starburst(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def flag_us(d, x, y, w, h):
    stripe = h / 13
    for i in range(13):
        d.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x, y, x + w * 0.4, y + stripe * 7], fill=(30, 50, 110))
    for r in range(4):
        for c in range(5):
            d.ellipse([x + 4 + c * 7, y + 3 + r * 6, x + 7 + c * 7, y + 6 + r * 6],
                      fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    starburst(d, x + w * 0.28, y + h * 0.3, 9, (255, 222, 0))


def flag_ru(d, x, y, w, h):
    for i, col in enumerate([(255, 255, 255), (0, 60, 160), (210, 30, 30)]):
        d.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3], fill=col)


def draw_lead_art(d):
    # Shenzhen skyline + three flags, area x 620..990, y 235..455
    base = 445
    skyline = [(630, 330), (665, 300), (700, 360), (735, 280), (770, 340),
               (805, 310), (840, 370), (875, 320), (910, 355), (945, 330)]
    for i, (bx, top) in enumerate(skyline):
        d.rectangle([bx, top, bx + 32, base], fill=BLUE)
    # tallest tower with spire
    d.rectangle([735, 262, 767, base], fill=BLUE)
    d.polygon([(743, 262), (759, 262), (751, 228)], fill=BLUE)
    d.ellipse([747, 218, 755, 226], fill=RED)
    # ground line
    d.line([(620, base), (990, base)], fill=INK, width=3)
    # three flag poles with flags
    flags = [(flag_us, 660), (flag_cn, 800), (flag_ru, 910)]
    for fn, fx in flags:
        d.line([(fx, 235), (fx, 330)], fill=INK, width=3)
        fn(d, fx + 3, 238, 72, 44)


def draw_gulf_map(d, x, y, w, h):
    # stylised Gulf: sand land, blue sea, red strikes at Kuwait/Bahrain
    d.rectangle([x, y, x + w, y + h], fill=SAND)
    d.polygon([(x + 15, y + 30), (x + 95, y + 10), (x + 150, y + 45),
               (x + 130, y + 120), (x + 60, y + 150), (x + 10, y + 100)],
              fill=SEA)
    d.polygon([(x + 15, y + 30), (x + 95, y + 10), (x + 150, y + 45),
               (x + 130, y + 120), (x + 60, y + 150), (x + 10, y + 100)],
              outline=BLUE, width=2)
    starburst(d, x + 55, y + 45, 14, RED)
    starburst(d, x + 115, y + 85, 14, RED)
    f = font(SANS_B, 17)
    text_w(d, (x + 8, y + 2), "KUWAIT", f, fill=INK)
    text_w(d, (x + 78, y + 118), "BAHRAIN", f, fill=INK)
    f2 = font(SANS, 15)
    text_w(d, (x + 5, y + h - 20), "STRAIT OF HORMUZ", f2, fill=BLUE)


def draw_bridge(d, x, y, w, h):
    water_y = y + 115
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
    d.rectangle([x, water_y, x + w, y + h], fill=SEA)
    # pylons
    d.rectangle([x + 25, y + 30, x + 33, water_y], fill=INK)
    d.rectangle([x + 120, y + 30, x + 128, water_y], fill=INK)
    # deck with a broken gap in the middle
    d.line([(x, y + 55), (x + 62, y + 55)], fill=INK, width=7)
    d.line([(x + 92, y + 55), (x + w, y + 55)], fill=INK, width=7)
    # fallen span piece tilted into the water
    d.line([(x + 64, y + 62), (x + 90, y + 105)], fill=INK, width=6)
    # cables
    d.line([(x + 29, y + 32), (x + 62, y + 55)], fill=GREY, width=2)
    d.line([(x + 29, y + 32), (x + 5, y + 55)], fill=GREY, width=2)
    d.line([(x + 124, y + 32), (x + 92, y + 55)], fill=GREY, width=2)
    d.line([(x + 124, y + 32), (x + 150, y + 55)], fill=GREY, width=2)
    # explosion at the gap + smoke
    starburst(d, x + 77, y + 55, 22, (230, 120, 20))
    starburst(d, x + 77, y + 55, 12, RED)
    d.ellipse([x + 55, y + 5, x + 85, y + 30], fill=(150, 150, 150))
    d.ellipse([x + 75, y - 2, x + 105, y + 22], fill=(180, 180, 180))


def draw_capitol(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
    base_y = y + h - 18
    # base + columns
    d.rectangle([x + 10, base_y - 22, x + w - 10, base_y], fill=BLUE)
    for cx in range(x + 22, x + w - 20, 22):
        d.rectangle([cx, base_y - 62, cx + 9, base_y - 22], fill=BLUE)
    d.rectangle([x + 14, base_y - 70, x + w - 14, base_y - 62], fill=BLUE)
    # dome
    d.pieslice([x + w / 2 - 42, base_y - 130, x + w / 2 + 42, base_y - 46],
               180, 360, fill=BLUE)
    d.rectangle([x + w / 2 - 42, base_y - 92, x + w / 2 + 42, base_y - 70],
                fill=BLUE)
    d.rectangle([x + w / 2 - 4, base_y - 150, x + w / 2 + 4, base_y - 128],
                fill=BLUE)
    d.line([(x + w / 2, base_y - 168), (x + w / 2, base_y - 150)], fill=INK,
           width=3)
    flag_us(d, x + w / 2 + 3, base_y - 168, 30, 18)


def draw_dove(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 236, 240))
    # olive branch
    d.line([(x + 15, y + h - 25), (x + w - 15, y + h - 55)], fill=(60, 110, 50),
           width=4)
    for lx, ly in [(x + 40, y + h - 38), (x + 70, y + h - 46),
                   (x + 100, y + h - 54)]:
        d.ellipse([lx, ly, lx + 22, ly + 10], fill=(60, 110, 50))
    # dove body, wing, head
    d.ellipse([x + 35, y + 45, x + 115, y + 105], fill=(255, 255, 255),
              outline=INK, width=2)
    d.polygon([(x + 45, y + 55), (x + 95, y + 50), (x + 70, y + 95)],
              fill=(225, 225, 225), outline=INK)
    d.ellipse([x + 100, y + 30, x + 130, y + 60], fill=(255, 255, 255),
              outline=INK, width=2)
    d.polygon([(x + 128, y + 42), (x + 148, y + 48), (x + 128, y + 52)],
              fill=(230, 150, 30))
    d.ellipse([x + 112, y + 40, x + 117, y + 45], fill=INK)
    # crack through the branch
    d.line([(x + 78, y + h - 30), (x + 88, y + h - 18)], fill=RED, width=4)
    d.line([(x + 88, y + h - 18), (x + 80, y + h - 8)], fill=RED, width=4)


def panel(d, x, y, w, h, kicker, headline, caption, art):
    art(d, x + 8, y + 8, 158, h - 16)
    tx = x + 178
    f_k = font(SANS_B, 20)
    f_h = font(SANS_B, 27)
    f_c = font(SANS, 22)
    text_w(d, (tx, y + 10), kicker, f_k, fill=RED)
    hl = wrap(d, headline, f_h, w - 186)
    hy = y + 36
    for i, line in enumerate(hl):
        d.text((tx, hy + i * 32), line, font=f_h, fill=INK)
    cy = hy + len(hl) * 32 + 4
    para(d, tx, cy, caption, f_c, w - 186, leading=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # frames
    d.rectangle([10, 10, 1014, 1014], outline=INK, width=5)
    d.rectangle([20, 20, 1004, 1004], outline=INK, width=2)

    # ---- masthead ----
    f_small = font(SANS_B, 24)
    text_w(d, (38, 36), "WEDNESDAY", f_small)
    wr = d.textlength("WORLD NEWS", font=f_small)
    text_w(d, (986 - wr, 36), "WORLD NEWS", f_small)
    f_mast = font(SERIF_B, 92)
    text_c(d, 512, 66, "18 NOVEMBER 2026", f_mast)
    f_sub = font(SANS_B, 25)
    text_c(d, 512, 168, "THE WORLD'S NEWS IN ONE IMAGE", f_sub, fill=GREY)
    d.line([(36, 208), (988, 208)], fill=INK, width=4)
    d.line([(36, 216), (988, 216)], fill=INK, width=2)

    # ---- lead story: Shenzhen summit ----
    f_k = font(SANS_B, 22)
    f_h = font(SANS_B, 34)
    f_c = font(SANS, 27)
    text_w(d, (36, 236), "SHENZHEN  ·  DIPLOMACY", f_k, fill=RED)
    text_w(d, (36, 264), "THREE LEADERS, ONE SUMMIT", f_h)
    para(d, 36, 322, "Trump lands in China as Xi and Putin meet a day "
       "ahead of the first US–China–Russia three-way talks.",
       f_c, 570, leading=8)
    draw_lead_art(d)
    d.line([(36, 470), (988, 470)], fill=INK, width=3)

    # ---- 2x2 grid ----
    gx, gy = 36, 490
    cw, ch = 466, 204
    panel(d, gx, gy, cw, ch, "THE GULF", "IRAN HITS KUWAIT, BAHRAIN",
          "Tehran hits a US base and Gulf sites after US strikes on "
          "Qeshm Island.", draw_gulf_map)
    panel(d, gx + cw + 20, gy, cw, ch, "UKRAINE", "KERCH BRIDGE HIT AGAIN",
          "Ukraine strikes the Crimea link; part of the road span "
          "collapses.", draw_bridge)
    d.line([(36, gy + ch + 6), (988, gy + ch + 6)], fill=GREY, width=1)
    panel(d, gx, gy + ch + 12, cw, ch, "WASHINGTON",
          "DEMOCRATS TAKE SENATE",
          "Peltola unseats Sullivan in Alaska; Democrats lead 56–44.",
          draw_capitol)
    panel(d, gx + cw + 20, gy + ch + 12, cw, ch, "GAZA", "TRUCE AT RISK",
          "The Board of Peace warns the ceasefire is at risk of "
          "collapse.", draw_dove)
    d.line([(36, 920), (988, 920)], fill=INK, width=3)

    # ---- footer briefs ----
    f_b = font(SANS_B, 19)
    f_bt = font(SANS, 19)
    briefs = [
        ("EBOLA", "Outbreak in DR Congo passes 11,000 cases."),
        ("ANTHROPIC", "Raises a record $81.3bn in a stock offering."),
        ("MEASLES", "US loses measles-free status after 26 years."),
    ]
    bx = 36
    bw = 304
    for kicker, txt in briefs:
        text_w(d, (bx, 928), kicker, f_b, fill=RED)
        para(d, bx, 954, txt, f_bt, bw, leading=3)
        bx += bw + 20

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
