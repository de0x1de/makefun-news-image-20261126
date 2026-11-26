#!/usr/bin/env python3
"""Draw the news-image-20261126 entry from scratch with PIL.

One image that sums up the world news of Thursday 26 November 2026,
laid out as a broadsheet front page: a masthead with the date in full,
one lead story with a drawn illustration, six secondary stories in a
grid, and a footer strip with three more.  Every letter is rendered
by PIL from system fonts, so no text can come out garbled, and the
output is byte-identical on every run.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (24, 24, 28)
RED = (178, 34, 40)
NAVY = (23, 42, 74)
GREY = (92, 92, 96)
CARD = (255, 253, 247)
RULE = (24, 24, 28)

SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap against pixel widths."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y


# ---------------------------------------------------------------- icons

def icon_containers(d, x, y, s):
    """Stacked shipping containers with a percent mark: the tariff lead."""
    cols = [(178, 34, 40), (23, 42, 74), (214, 144, 32)]
    cw, ch, step = 138, 50, 56
    rows = [(0, 2), (14, 2), (7, 1)]  # (x offset, boxes) bottom to top
    for r, (off, n) in enumerate(rows):
        for c in range(n):
            cx = x + off + c * (cw + 8)
            cy = y + (2 - r) * step
            d.rectangle([cx, cy, cx + cw, cy + ch], fill=cols[(r + c) % 3])
            d.rectangle([cx + 8, cy + 6, cx + cw - 8, cy + ch - 6],
                        outline=(255, 253, 247), width=2)
    d.text((x + 218, y - 58), "%", font=font(SANS_B, 84), fill=INK)


def icon_drone(d, x, y, s):
    d.ellipse([x, y, x + s * 0.28, y + s * 0.28], outline=INK, width=5)
    d.ellipse([x + s * 0.72, y, x + s, y + s * 0.28], outline=INK, width=5)
    d.ellipse([x, y + s * 0.72, x + s * 0.28, y + s], outline=INK, width=5)
    d.ellipse([x + s * 0.72, y + s * 0.72, x + s, y + s], outline=INK, width=5)
    d.line([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8], fill=INK, width=6)
    d.line([x + s * 0.8, y + s * 0.2, x + s * 0.2, y + s * 0.8], fill=INK, width=6)
    d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], fill=RED)


def icon_virus(d, x, y, s):
    cx, cy, r = x + s / 2, y + s / 2, s * 0.26
    for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]:
        ex, ey = cx + dx * r * 1.55, cy + dy * r * 1.55
        d.line([cx, cy, ex, ey], fill=INK, width=5)
        d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=RED)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    d.ellipse([cx - r * 0.35, cy - r * 0.3, cx - r * 0.1, cy - r * 0.05], fill=PAPER)
    d.ellipse([cx + r * 0.15, cy + r * 0.2, cx + r * 0.4, cy + r * 0.45], fill=PAPER)


def icon_euro(d, x, y, s):
    d.text((x + s * 0.18, y - 10), "€", font=font(SERIF_B, int(s * 1.05)), fill=NAVY)


def icon_skyline(d, x, y, s):
    base = y + s
    for bx, bw, bh in [(0.0, 0.24, 0.55), (0.28, 0.2, 0.8), (0.52, 0.22, 0.45), (0.78, 0.2, 0.65)]:
        d.rectangle([x + s * bx, base - s * bh, x + s * (bx + bw), base], fill=INK)
    pts = []
    import math
    for i in range(13):
        ang = 2 * math.pi * i / 12
        rr = s * 0.30 if i % 2 == 0 else s * 0.13
        pts.append((x + s * 0.78 + rr * math.cos(ang), y + s * 0.22 + rr * math.sin(ang)))
    d.polygon(pts, fill=(232, 148, 28))


def icon_radiation(d, x, y, s):
    import math
    cx, cy = x + s / 2, y + s / 2
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=INK)
    for a0 in (-90, 30, 150):
        pts = [(cx, cy)]
        for a in range(a0 - 28, a0 + 29, 4):
            pts.append((cx + s * 0.48 * math.cos(math.radians(a)),
                        cy + s * 0.48 * math.sin(math.radians(a))))
        d.polygon(pts, fill=(222, 178, 26), outline=INK)


def icon_flame(d, x, y, s):
    d.polygon([(x + s * 0.5, y), (x + s * 0.86, y + s * 0.62), (x + s * 0.72, y + s),
               (x + s * 0.28, y + s), (x + s * 0.14, y + s * 0.62)], fill=RED)
    d.polygon([(x + s * 0.5, y + s * 0.34), (x + s * 0.7, y + s * 0.68),
               (x + s * 0.6, y + s), (x + s * 0.4, y + s), (x + s * 0.3, y + s * 0.68)],
              fill=(240, 166, 40))


ICONS = {
    "drone": icon_drone,
    "virus": icon_virus,
    "euro": icon_euro,
    "skyline": icon_skyline,
    "radiation": icon_radiation,
    "flame": icon_flame,
}

# ---------------------------------------------------------------- stories

CARDS = [
    ("KUWAIT · MIDDLE EAST", "drone", RED,
     "Iranian drone kills two Italians",
     "A drone strike on an air-defence site killed two Italian technicians "
     "of Rheinmetall Italia."),
    ("CONGO · HEALTH", "virus", RED,
     "Ebola cases pass 12,000",
     "Congo's deadliest outbreak yet: 12,021 cases, nearly half fatal. "
     "No approved vaccine."),
    ("BRUSSELS · EUROPE", "euro", NAVY,
     "EU leaders open budget summit",
     "Two days on the 2028-34 budget: a €1.78tn compromise, up to €100bn "
     "for Ukraine. Merz: still too high."),
    ("GAZA · MIDDLE EAST", "skyline", RED,
     "Israeli strikes kill eight",
     "Eight died, among them Gaza's Hamas-appointed deputy education "
     "minister and his wife."),
    ("NORTH KOREA · ASIA", "radiation", NAVY,
     "Kim widens nuclear push",
     "Kim Jong Un called for tactical nuclear weapons across more "
     "missions and domains."),
    ("EGYPT · AFRICA", "flame", RED,
     "Tanker fire kills 31 in Cairo",
     "A fuel tanker overturned and burned on the Ring Road: 31 dead, 21 "
     "hurt. A driver is detained."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead ------------------------------------------------------------
    d.rectangle([0, 0, W, 148], fill=INK)
    centred(d, W / 2, 12, "T H E   D A I L Y   P I C T U R E", font(SANS_B, 25), (240, 220, 160))
    centred(d, W / 2, 48, "THURSDAY 26 NOVEMBER 2026", font(SERIF_B, 47), PAPER)
    centred(d, W / 2, 114, "The world's news of one day, in one image", font(SANS, 22), (196, 196, 200))

    # Lead story ----------------------------------------------------------
    d.rectangle([28, 166, W - 28, 548], fill=CARD, outline=RULE, width=3)
    d.rectangle([28, 166, W - 28, 204], fill=RED)
    d.text((48, 174), "LEAD STORY · GLOBAL ECONOMY", font=font(SANS_B, 24), fill=PAPER)
    icon_containers(d, 58, 268, 300)
    centred(d, 200, 452, "TARIFF WALL RISES", font(SANS_B, 25), INK)
    d.text((58, 492), "Crates, duties, a deadline",
           font=font(SANS, 19), fill=GREY)
    lx = 400
    y = block(d, (lx, 220), "US unveils new tariffs on 14 trading partners",
              font(SERIF_B, 40), INK, W - 28 - lx - 24, 47)
    y += 4
    y = block(d, (lx, y),
              "Washington says the duties answer “excess factory capacity” "
              "that undercuts American firms.",
              font(SANS, 24), INK, W - 28 - lx - 24, 31)
    y += 10
    facts = [
        "CHINA 20% — 40% if truce lapses 10 Jan",
        "EU · JAPAN · KOREA · TAIWAN capped at 15%",
        "INDIA 17% with a deal, 25% without",
        "Beijing & Brasília push back at the list",
    ]
    for f in facts:
        d.rectangle([lx, y + 7, lx + 10, y + 17], fill=RED)
        y = block(d, (lx + 22, y), f, font(SANS_B, 21), INK, W - 28 - lx - 46, 27)
        y += 5

    # Secondary grid ------------------------------------------------------
    gx, gy, gw, gh, gap = 28, 564, 312, 162, 14
    for i, (kicker, icon, accent, head, body) in enumerate(CARDS):
        cx = gx + (i % 3) * (gw + gap)
        cy = gy + (i // 3) * (gh + gap)
        d.rectangle([cx, cy, cx + gw, cy + gh], fill=CARD, outline=RULE, width=2)
        d.rectangle([cx, cy, cx + gw, cy + 30], fill=accent)
        d.text((cx + 12, cy + 5), kicker, font=font(SANS_B, 17), fill=PAPER)
        ICONS[icon](d, cx + 12, cy + 42, 50)
        block(d, (cx + 74, cy + 38), head, font(SERIF_B, 21), INK, gw - 86, 25)
        block(d, (cx + 12, cy + 100), body, font(SANS, 16), INK, gw - 24, 20)

    # Footer ticker -------------------------------------------------------
    fy = 916
    d.rectangle([0, fy, W, H], fill=NAVY)
    d.text((28, fy + 10), "ALSO ON THURSDAY", font=font(SANS_B, 20), fill=(240, 220, 160))
    ticker = [
        "NEW YORK — Macy's 100th Thanksgiving parade postponed for the "
        "first time ever; it moves to Saturday.",
        "SPACE — US clears SpaceX orbital data centres, up to 1M satellites.",
        "RUSSIA — Krasnodar oil refinery ablaze after a drone attack.",
    ]
    ty = fy + 38
    for t in ticker:
        ty = block(d, (28, ty), "▸ " + t, font(SANS, 17), PAPER, W - 56, 21)
        ty += 1

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
