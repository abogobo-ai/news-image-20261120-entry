#!/usr/bin/env python3
"""Build entry.png — THE WORLD TODAY, Friday 20 November 2026.
Procedural PIL drawing only; no downloaded assets, no photos.
Deterministic: same input -> same sha256 every run.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (253, 246, 227)
INK = (26, 26, 26)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (13, 116, 128)
GOLD = (180, 130, 20)
OCEAN = (207, 227, 238)
LAND = (232, 220, 192)
LAND_EDGE = (190, 170, 130)
GREY = (90, 90, 90)
LIGHT = (240, 232, 210)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, font, fill=INK, leading=None):
    if leading is None:
        leading = font.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def scene_capitol(d, x, y, w, h):
    """Lead 1: Capitol dome + flags + 2027 clock."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 244))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(120, 160, 110))
    cx = x + w // 2
    # dome
    d.pieslice([cx - 52, y + 18, cx + 52, y + 122], 180, 360, fill=(245, 245, 240))
    d.rectangle([cx - 52, y + 70, cx + 52, y + h - 26], fill=(245, 245, 240))
    for i in range(5):
        px = cx - 40 + i * 20
        d.rectangle([px, y + 78, px + 8, y + h - 26], fill=(200, 200, 190))
    d.rectangle([cx - 3, y + 6, cx + 3, y + 20], fill=INK)
    d.ellipse([cx - 5, y + 2, cx + 5, y + 10], fill=GOLD)
    # flags
    for fx, col in ((x + 16, RED), (x + w - 34, BLUE)):
        d.rectangle([fx + 8, y + 26, fx + 10, y + 66], fill=INK)
        d.rectangle([fx + 10, y + 26, fx + 34, y + 42], fill=col)
        d.rectangle([fx + 10, y + 34, fx + 34, y + 38], fill=(255, 255, 255))
    # 2027 badge
    d.rounded_rectangle([x + w - 122, y + h - 52, x + w - 8, y + h - 30],
                        radius=6, fill=RED)
    d.text((x + w - 114, y + h - 50), "DECISION: 2027", font=F(SANS_B, 10),
           fill=(255, 255, 255))


def scene_ipo(d, x, y, w, h):
    """Lead 2: rising chart + skyscraper + big $."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 240, 226))
    # bars rising
    bars = [34, 52, 46, 70, 66, 92, 118]
    bw = (w - 40) // len(bars)
    for i, bh in enumerate(bars):
        bx = x + 20 + i * bw
        col = TEAL if i < len(bars) - 1 else RED
        d.rectangle([bx, y + h - 30 - bh, bx + bw - 6, y + h - 30], fill=col)
    d.line([(x + 16, y + h - 30), (x + w - 16, y + h - 30)], fill=INK, width=2)
    # arrow
    d.line([(x + 24, y + 62), (x + w - 60, y + 18)], fill=RED, width=4)
    d.polygon([(x + w - 60, y + 18), (x + w - 84, y + 16), (x + w - 62, y + 38)],
              fill=RED)
    d.text((x + 18, y + 8), "$107.3bn  +17%", font=F(SANS_B, 15), fill=INK)
    d.text((x + w - 118, y + h - 26), "ANT  $97.17", font=F(SANS_B, 12),
           fill=RED)


def scene_cyclone(d, x, y, w, h):
    """Lead 3: cyclone spiral over coast + rain + houses."""
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 235))
    cx, cy = x + w // 2 - 30, y + h // 2 - 8
    # spiral arms
    for r in (14, 26, 38, 50, 62):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20 + r, end=200 + r,
              fill=(255, 255, 255), width=7)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)
    # coast + houses
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(150, 190, 140))
    for i in range(4):
        hx = x + 18 + i * 62
        d.polygon([(hx, y + h - 52), (hx + 16, y + h - 66),
                   (hx + 32, y + h - 52)], fill=RED)
        d.rectangle([hx + 3, y + h - 52, hx + 29, y + h - 34], fill=(250, 240, 210))
    # rain streaks
    for i in range(8):
        rx = x + 30 + i * 34
        d.line([(rx, y + 12), (rx - 6, y + 30)], fill=BLUE, width=2)
    d.text((x + 12, y + h - 26), "300,000 EVACUATED", font=F(SANS_B, 12),
           fill=(255, 255, 255))


def icon_voyager(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(20, 30, 60))
    d.ellipse([x + s - 16, y + 6, x + s - 8, y + 14], fill=GOLD)
    d.ellipse([x + 8, y + s - 14, x + 14, y + s - 8], fill=(255, 255, 255))
    d.polygon([(x + 14, y + 40), (x + 34, y + 22), (x + 40, y + 34),
               (x + 22, y + 48)], fill=(200, 200, 200))
    d.rectangle([x + 30, y + 26, x + 46, y + 40], fill=(240, 240, 240))
    d.line([(x + 34, y + 30), (x + 50, y + 14)], fill=(255, 255, 255), width=2)
    d.text((x + 4, y + s - 12), "1 LIGHT-DAY", font=F(SANS_B, 8),
           fill=(255, 255, 255))


def icon_hayabusa(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(40, 40, 48))
    d.ellipse([x + 34, y + 8, x + 56, y + 30], fill=(150, 120, 90))
    d.ellipse([x + 40, y + 13, x + 48, y + 21], fill=(110, 85, 60))
    d.rectangle([x + 8, y + 34, x + 24, y + 42], fill=BLUE)
    d.rectangle([x + 24, y + 30, x + 38, y + 46], fill=(220, 220, 220))
    d.rectangle([x + 38, y + 34, x + 54, y + 42], fill=BLUE)
    d.line([(x + 31, y + 46), (x + 31, y + 54)], fill=(255, 255, 255), width=2)
    d.text((x + 4, y + s - 12), "NO LANDING", font=F(SANS_B, 8),
           fill=(255, 255, 255))


def icon_gta(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(90, 20, 90))
    d.rounded_rectangle([x + 10, y + 20, x + s - 10, y + 46], radius=10,
                        fill=(30, 30, 30))
    d.rectangle([x + 18, y + 28, x + 26, y + 38], fill=(255, 255, 255))
    d.ellipse([x + s - 26, y + 28, x + s - 18, y + 36], fill=RED)
    d.ellipse([x + s - 36, y + 32, x + s - 28, y + 40], fill=GOLD)
    d.text((x + 6, y + 4), "GTA 6", font=F(SANS_B, 12), fill=(255, 255, 255))
    d.text((x + 6, y + s - 12), "$1.8bn", font=F(SANS_B, 9), fill=GOLD)


def icon_talks(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(226, 236, 250))
    d.ellipse([x + 6, y + 10, x + 34, y + 34], fill=(255, 255, 255),
              outline=BLUE, width=2)
    d.ellipse([x + 28, y + 26, x + 56, y + 50], fill=(255, 255, 255),
              outline=RED, width=2)
    for i in range(6):
        ang = i * 60
        import math
        px = x + 31 + int(9 * math.cos(math.radians(ang)))
        py = y + 52 + int(9 * math.sin(math.radians(ang)))
        d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=GOLD)
    d.text((x + 8, y + 4), "TALKS", font=F(SANS_B, 9), fill=BLUE)


def icon_shield(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(232, 240, 232))
    d.polygon([(x + 31, y + 8), (x + 52, y + 16), (x + 52, y + 34),
               (x + 31, y + 54), (x + 10, y + 34), (x + 10, y + 16)],
              fill=TEAL)
    d.line([(x + 20, y + 30), (x + 28, y + 38), (x + 44, y + 22)], fill=(255, 255, 255),
           width=3)
    d.text((x + 6, y + s - 12), "GUARANTEE", font=F(SANS_B, 8), fill=INK)


def icon_ship(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(200, 228, 240))
    d.polygon([(x + 8, y + 40), (x + 54, y + 40), (x + 46, y + 52),
               (x + 16, y + 52)], fill=(120, 60, 40))
    d.rectangle([x + 14, y + 26, x + 26, y + 40], fill=RED)
    d.rectangle([x + 28, y + 26, x + 40, y + 40], fill=GOLD)
    d.rectangle([x + 42, y + 26, x + 50, y + 40], fill=TEAL)
    d.text((x + 8, y + 6), "$1tn", font=F(SANS_B, 13), fill=INK)
    d.text((x + 6, y + s - 12), "EXPORTS", font=F(SANS_B, 8), fill=INK)


def icon_taiwan(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(255, 244, 214))
    d.line([(x + 8, y + 44), (x + 20, y + 30), (x + 30, y + 36),
            (x + 44, y + 18), (x + 54, y + 12)], fill=TEAL, width=3)
    d.polygon([(x + 54, y + 12), (x + 44, y + 10), (x + 52, y + 22)], fill=TEAL)
    d.rectangle([x + 8, y + 6, x + 26, y + 16], fill=RED)
    d.text((x + 9, y + 7), "5", font=F(SANS_B, 8), fill=(255, 255, 255))
    d.text((x + 30, y + 6), "MEASURES", font=F(SANS_B, 8), fill=INK)


def icon_baseball(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(240, 240, 235))
    d.ellipse([x + 14, y + 12, x + 48, y + 46], fill=(255, 255, 255),
              outline=RED, width=2)
    d.arc([x + 20, y + 14, x + 40, y + 44], 300, 60, fill=RED, width=2)
    d.arc([x + 22, y + 14, x + 42, y + 44], 120, 240, fill=RED, width=2)
    d.text((x + 6, y + s - 12), "PARDON", font=F(SANS_B, 8), fill=INK)


def icon_cricket(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(220, 240, 210))
    d.rectangle([x + 14, y + 10, x + 22, y + 44], fill=(180, 140, 80))
    d.rectangle([x + 14, y + 10, x + 22, y + 18], fill=(120, 80, 40))
    d.ellipse([x + 38, y + 30, x + 52, y + 44], fill=RED)
    d.text((x + 6, y + 46), "118  NZ 317-6", font=F(SANS_B, 8), fill=INK)


def icon_cop(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 240, 230))
    d.ellipse([x + 12, y + 10, x + 50, y + 48], fill=(120, 190, 160))
    d.arc([x + 16, y + 14, x + 46, y + 44], 200, 340, fill=(255, 255, 255),
          width=2)
    d.polygon([(x + 31, y + 26), (x + 36, y + 36), (x + 26, y + 36)], fill=TEAL)
    d.text((x + 10, y + 50), "35% BY 2035", font=F(SANS_B, 8), fill=INK)


LEADS = [
    ("LEAD 1 — WASHINGTON", "Trump pushes Iran war decision to 2027",
     "“No rush,” Trump says — he will “see what happens” after Jan 1, pushing any call on Iran into next year. (Reuters)",
     scene_capitol),
    ("LEAD 2 — NEW YORK", "Anthropic IPO closes first day up 17%",
     "Shares end at $97.17 after the record $107.3bn raise; they opened at $111.50, briefly topping a $2tn value. (Hindu BusinessLine)",
     scene_ipo),
    ("LEAD 3 — ODISHA, INDIA", "Cyclone Akvan: 300,000 evacuated",
     "The severe storm bears down on the Odisha coast as 423 rescue teams deploy and schools shut. (The Hindu)",
     scene_cyclone),
]

MIDS = [
    ("Voyager 1 hits a light-day", "NASA confirms the probe has passed one light-day from Earth — a first.", icon_voyager),
    ("Hayabusa2 landing scrapped", "Engine trouble forces Japan's probe to drop its asteroid landing plan.", icon_hayabusa),
    ("GTA 6 tops $1.8bn", "Rockstar's sequel has already outgrossed The Odyssey's global run.", icon_gta),
    ("Europe open to Russia talks", "Leaders say they are ready to negotiate an end to the Ukraine war.", icon_talks),
    ("NATO-style shield on table", "US envoy: Moscow is not ruling out NATO-like guarantees for Kyiv.", icon_shield),
    ("Korea exports pass $1tn", "South Korea's annual exports top one trillion dollars for the first time.", icon_ship),
    ("Taiwan steadies its stocks", "Regulator unveils five measures; short-selling limits start today.", icon_taiwan),
    ("Pardon for Pete Rose", "Trump announces a posthumous pardon for the late baseball star.", icon_baseball),
    ("Phillips ton lifts NZ", "Glenn Phillips hits 118 as NZ reach 317-6 vs India, Day 2.", icon_cricket),
    ("COP31 draft: 35% by 2035", "New text proposes a 35% electricity share and adaptation finance.", icon_cop),
]

BRIEFS = [
    "Trump returns from China; White House press conference scheduled today",
    "Trump warns APEC nations strict AI rules would stifle development",
    "Saudi Arabia confirms a Houthi attack damaged a Riyadh landmark tower",
    "Projectile lands near the Dutch embassy in Kyiv; minor damage reported",
    "US and Venezuela sign a deal to restore military cooperation",
    "Meta reviews its net-zero 2030 timetable as AI infrastructure grows",
    "US military drones tap 150,000 radios to defeat battlefield jamming",
    "Modi meets the Prince and Princess of Wales in New Delhi",
    "ICMR completes 100 health-technology transfer agreements",
    "India stresses climate resilience at COP31 in Turkiye",
    "UK-EU summit: nature groups urge a pesticide crackdown",
    "Pakistan v Sri Lanka: Sri Lanka 309/9, lead by 82 on Day 3",
    "57th International Film Festival of India opens in Goa",
    "Women's Asian Hockey Champions Trophy begins",
    "India beat Malaysia at the Hong Kong Open badminton",
    "UFC Fight Night 294: Prochazka v Stirling in Doha",
    "Oil flat as Hormuz tanker disruption offsets glut fears",
    "Migrant boat sinks off Senegal; dozens missing",
    "Taiwan approves Civil Code reform; spouse's share rises to two-thirds",
]

# (number, name, lon, lat, dx, dy) — dx/dy spread crowded pins apart
PINS = [
    (1, "Washington", -77, 39, -4, -6),
    (2, "New York", -74, 41, 10, -8),
    (3, "Odisha", 85, 20, 0, 0),
    (4, "Tokyo", 139, 36, 0, 0),
    (5, "Los Angeles", -118, 34, 0, 0),
    (6, "Brussels", 4, 51, -8, -6),
    (7, "Kyiv", 30, 50, 2, -10),
    (8, "Seoul", 127, 37, 8, -6),
    (9, "Taipei", 121, 25, 6, 6),
    (10, "Cincinnati", -84, 39, -14, 8),
    (11, "Wellington", 175, -41, 0, 0),
    (12, "Ankara", 33, 40, 10, 10),
]

CONTINENTS = [
    # North America (lon, lat)
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-80, 73),
     (-76, 62), (-65, 60), (-55, 47), (-70, 42), (-75, 35), (-80, 26),
     (-85, 30), (-97, 26), (-105, 20), (-95, 16), (-83, 9), (-90, 14),
     (-105, 23), (-117, 33), (-125, 40), (-125, 49), (-135, 58),
     (-155, 58), (-165, 60)],
    # South America
    [(-79, 9), (-72, 12), (-62, 9), (-52, 5), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-58, -38), (-65, -45), (-68, -52),
     (-70, -40), (-72, -30), (-77, -12), (-81, -5), (-80, 1)],
    # Africa
    [(-17, 15), (-15, 27), (-10, 31), (0, 36), (10, 37), (20, 32),
     (30, 31), (35, 28), (40, 15), (51, 11), (48, -2), (40, -12),
     (36, -20), (32, -29), (20, -35), (15, -27), (12, -18), (9, -1),
     (9, 4), (-8, 4), (-13, 8)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (4, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 70),
     (40, 68), (44, 66), (40, 60), (48, 46), (40, 44), (30, 46), (28, 44),
     (23, 40), (19, 42), (12, 44), (8, 44), (3, 42), (-1, 38)],
    # Asia
    [(44, 66), (60, 69), (70, 72), (90, 75), (110, 74), (130, 72),
     (150, 70), (170, 66), (162, 60), (158, 52), (142, 50), (140, 40),
     (130, 34), (127, 35), (122, 30), (120, 22), (110, 20), (105, 10),
     (100, 8), (97, 16), (92, 21), (88, 22), (80, 15), (76, 8),
     (72, 20), (66, 25), (60, 25), (52, 26), (48, 30), (44, 29),
     (40, 36), (36, 36), (44, 40), (48, 42), (42, 46), (40, 52), (44, 60)],
    # Australia
    [(114, -22), (114, -32), (124, -33), (130, -32), (136, -35),
     (140, -38), (146, -39), (150, -37), (153, -27), (150, -22),
     (146, -19), (142, -11), (136, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=OCEAN)
    # graticule
    for gx in range(1, 6):
        d.line([(x + w * gx // 6, y), (x + w * gx // 6, y + h)], fill=(255, 255, 255),
               width=1)
    for gy in range(1, 4):
        d.line([(x, y + h * gy // 4), (x + w, y + h * gy // 4)],
               fill=(255, 255, 255), width=1)

    def proj(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h)

    for cont in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in cont]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # Voyager callout (deep space, off-map star)
    d.text((x + w - 268, y + 4), "★ VOYAGER 1 — 1 LIGHT-DAY FROM EARTH",
           font=F(SANS_B, 9), fill=BLUE)
    for num, name, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        # leader line back to true spot
        tx, ty = proj(lon, lat)
        if dx or dy:
            d.line([(tx, ty), (px, py)], fill=RED, width=1)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px - 3, py - 7), str(num), font=F(SANS_B, 9),
               fill=(255, 255, 255))
    # key as two rows of six, bottom strip
    key = ["1 Washington", "2 New York", "3 Odisha", "4 Tokyo",
           "5 Los Angeles", "6 Brussels", "7 Kyiv", "8 Seoul",
           "9 Taipei", "10 Cincinnati", "11 Wellington", "12 Ankara"]
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(255, 255, 255))
    for i, k in enumerate(key):
        kx = x + 6 + (i % 6) * 106
        ky = y + h - 28 + (i // 6) * 13
        d.text((kx, ky), k, font=F(SANS, 8), fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14
    # ---- masthead ----
    d.rectangle([M, M, W - M, 102], outline=INK, width=2)
    d.text((W // 2, 20), "THE WORLD TODAY", font=F(SERIF_B, 54),
           fill=INK, anchor="ma")
    d.line([(M + 8, 78), (W - M - 8, 78)], fill=INK, width=1)
    d.text((W // 2, 82), "FRIDAY, 20 NOVEMBER 2026  •  32 STORIES  •  13 DRAWN ILLUSTRATIONS",
           font=F(SANS_B, 13), fill=RED, anchor="ma")
    # ---- stat strip ----
    stats = [("32", "STORIES"), ("13", "ILLUSTRATIONS"), ("12", "MAP PINS"),
             ("6", "REGIONS + SPACE")]
    sw = (W - 2 * M) // 4
    for i, (n, lab) in enumerate(stats):
        x0 = M + i * sw
        d.rectangle([x0, 106, x0 + sw - 4, 130], fill=LIGHT, outline=INK)
        d.text((x0 + 8, 108), n, font=F(SANS_B, 14), fill=RED)
        d.text((x0 + 40, 111), lab, font=F(SANS_B, 10), fill=INK)
    # ---- leads ----
    cw = 324
    for i, (kick, head, body, scene) in enumerate(LEADS):
        x0 = M + i * (cw + 12)
        y0 = 134
        d.rectangle([x0, y0, x0 + cw, 396], outline=INK, width=1)
        d.text((x0 + 8, y0 + 5), kick, font=F(SANS_B, 9), fill=RED)
        y = text_block(d, x0 + 8, y0 + 20,
                       wrap(d, head, F(SERIF_B, 17), cw - 16),
                       F(SERIF_B, 17), leading=20)
        scene(d, x0 + 8, y + 4, cw - 16, 138)
        d.text((x0 + 8, y + 144), "(Illustration — drawn, not a photo)",
               font=F(SANS, 8), fill=GREY)
        text_block(d, x0 + 8, y + 158,
                   wrap(d, body, F(SANS, 10), cw - 16), F(SANS, 10),
                   leading=13)
    # ---- mid header ----
    d.text((M, 402), "THE WORLD IN BRIEF — TEN MORE, EACH WITH A DRAWN ICON",
           font=F(SANS_B, 11), fill=INK)
    d.line([(M, 418), (W - M, 418)], fill=INK, width=1)
    # ---- mid grid ----
    mcw, mch = 195, 118
    for i, (head, body, icon) in enumerate(MIDS):
        col, row = i % 5, i // 5
        x0 = M + col * (mcw + 5)
        y0 = 422 + row * (mch + 4)
        d.rectangle([x0, y0, x0 + mcw, y0 + mch], outline=INK, width=1)
        icon(d, x0 + (mcw - 62) // 2, y0 + 5, 62)
        y = text_block(d, x0 + 6, y0 + 70,
                       wrap(d, head, F(SANS_B, 10), mcw - 12),
                       F(SANS_B, 10), leading=12)
        text_block(d, x0 + 6, y + 1,
                   wrap(d, body, F(SANS, 9), mcw - 12), F(SANS, 9),
                   leading=11)
    # ---- map section ----
    d.text((M, 668), "WHERE IT HAPPENED — THE WORLD MAP",
           font=F(SANS_B, 11), fill=INK)
    draw_map(d, M, 684, 640, 162)
    rx = 662
    d.rectangle([rx, 684, W - M, 846], outline=INK, width=1)
    y = 690
    d.text((rx + 8, y), "REGIONS", font=F(SANS_B, 10), fill=RED)
    y += 15
    for ln in ["AMERICAS 8  •  EUROPE 4  •  ASIA 17",
               "AFRICA 1  •  OCEANIA 1  •  DEEP SPACE 1"]:
        d.text((rx + 8, y), ln, font=F(SANS, 10), fill=INK)
        y += 13
    y += 3
    d.text((rx + 8, y), "TIMELINE — UTC, 20 NOV 2026", font=F(SANS_B, 10),
           fill=RED)
    y += 14
    for t in ["00:22  Phillips 118 — NZ 317-6 v India",
              "01:34  Voyager 1 — one light-day",
              "01:43  Akvan: 300,000 evacuated",
              "02:30  Pardon for Pete Rose",
              "03:06  Trump pushes Iran call to 2027"]:
        d.text((rx + 8, y), t, font=F(SANS, 9), fill=INK)
        y += 11
    y += 3
    d.rectangle([rx + 8, y, W - M - 8, 842], fill=(255, 244, 214),
                outline=RED, width=1)
    d.text((rx + 14, y + 4), "DATE CHECK", font=F(SANS_B, 9), fill=RED)
    text_block(d, rx + 14, y + 17,
               wrap(d, "All 32 stories happened or were first reported on Friday, 20 November 2026.",
                    F(SANS, 8), 320), F(SANS, 8), leading=10)
    # ---- briefs ----
    d.text((M, 852), "IN BRIEF — 19 MORE STORIES FROM 20 NOVEMBER 2026",
           font=F(SANS_B, 11), fill=INK)
    d.line([(M, 868), (W - M, 868)], fill=INK, width=1)
    bf = F(SANS, 9)
    for i, b in enumerate(BRIEFS):
        col, row = i % 2, i // 2
        x0 = M + col * 498
        y0 = 872 + row * 11
        d.text((x0, y0), "• " + b, font=bf, fill=INK)
    # ---- footer ----
    d.line([(M, 978), (W - M, 978)], fill=INK, width=1)
    d.text((M, 982),
           "Sources: Reuters, BBC, The Hindu, The Hindu BusinessLine, Space.com, "
           "NASA, LiveScore, SimpleLife wires, AppiSToS, Interesting Engineering.",
           font=F(SANS, 8), fill=GREY)
    d.text((M, 994),
           "All 32 stories happened or were first reported on Friday, 20 November 2026. "
           "Scenes and icons are original drawings; no photographs.",
           font=F(SANS_B, 8), fill=INK)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
