#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261123 (v2).

Programmatic newspaper front page, 1024x1024, PIL + DejaVu only.
Six main stories plus an ALSO strip with four more verified stories
from Monday 23 November 2026. No network, deterministic output.
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap

W, H = 1024, 1024
BG = (247, 243, 232)
INK = (17, 24, 39)
RED = (185, 28, 28)
NAVY = (30, 58, 95)
GREY = (75, 85, 99)
WHITE = (255, 255, 255)
LIGHT = (214, 234, 248)

FD = "/usr/share/fonts/truetype/dejavu/"
def font(name, size):
    return ImageFont.truetype(FD + name, size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

def text_center(y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill)

def rounded(x0, y0, x1, y1, r, fill, outline=None, width=1):
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill,
                        outline=outline, width=width)

# Top bar
d.rectangle([0, 0, W, 10], fill=RED)
# Masthead
text_center(24, "MONDAY  23 NOVEMBER 2026", F_SERIF_B(44), INK)
text_center(82, "WORLD NEWS IN ONE IMAGE", F_SANS_B(26), RED)
d.line([28, 120, 996, 120], fill=INK, width=2)
text_center(128, "Ten stories that defined the day", F_SANS(20), GREY)

# Lead panel: COP31
rounded(28, 156, 996, 426, 12, WHITE, outline=INK, width=2)
d.text((48, 170), "CLIMATE  \u2022  ANTALYA, TURKEY", font=F_SANS_B(21), fill=RED)
d.text((48, 198), "COP31 COLLAPSES", font=F_SANS_B(54), fill=INK)
d.text((48, 254), "WITH NO DEAL", font=F_SANS_B(54), fill=INK)
body = ("Climate talks end after two days of overtime. The EU and "
        "about 130 countries rejected a text with no fossil-fuel "
        "phase-out.")
y = 318
for line in textwrap.wrap(body, width=64):
    d.text((48, y), line, font=F_SANS(20), fill=INK)
    y += 26
d.rectangle([48, 388, 218, 414], fill=RED)
d.text((78, 393), "TOP STORY", font=F_SANS_B(20), fill=WHITE)
# COP31 scene: Antalya coast, conference hall, fossil-fuel chimney crossed out
import math
sx0, sy0, sx1, sy1 = 736, 168, 976, 384
d.rectangle([sx0, sy0, sx1, sy1], fill=(186, 226, 243))          # sky
d.ellipse([934, 178, 964, 208], fill=(245, 158, 11))            # sun
# large conference hall: dome, columns, flags
d.rectangle([752, 300, 960, 384], fill=WHITE, outline=NAVY, width=3)
d.rectangle([752, 300, 960, 312], fill=NAVY)
d.ellipse([816, 224, 892, 302], fill=(180, 200, 220), outline=NAVY, width=3)
d.line([(854, 224), (854, 204)], fill=NAVY, width=3)
d.polygon([(854, 204), (874, 210), (854, 216)], fill=RED)
for col in (776, 812, 896, 932):
    d.rectangle([col, 322, col + 10, 384], fill=(200, 210, 225), outline=NAVY, width=1)
for fx, fc in [(768, (0, 90, 160)), (938, (0, 130, 80))]:
    d.line([(fx, 300), (fx, 278)], fill=NAVY, width=2)
    d.polygon([(fx, 278), (fx + 14, 283), (fx, 288)], fill=fc)
# small crossed-out chimney at the hall's right (fossil fuel dispute)
d.rectangle([962, 340, 972, 384], fill=(120, 120, 120))
d.line([(958, 336), (976, 356)], fill=RED, width=4)
d.line([(976, 336), (958, 356)], fill=RED, width=4)
d.text((788, 396), "ANTALYA, TURKEY", font=F_SANS_B(17), fill=GREY)

# Story strips
stories = [
    ("UKRAINE WAR", "AT LEAST 15 KILLED IN KYIV REGION",
     "Russian strikes hit Dymer; Kyiv region declares a day of mourning.", "star"),
    ("MARKETS", "AI SELL-OFF HITS MARKETS",
     "Japan's Nikkei falls 5.06%; the S&P 500 drops 3.7%.", "chart"),
    ("UNITED STATES", "DEMOCRATS WIN HOUSE, 258 SEATS",
     "Largest House majority since 1992.", "capitol"),
    ("BLACK SEA", "UKRAINE DRONE HITS RUSSIAN WARSHIP",
     "Corvette Merkury severely damaged off Libya.", "ship"),
    ("MEXICO", "'EL CHAPO ISIDRO' CAPTURED",
     "FBI most-wanted drug kingpin seized in Sinaloa.", "badge"),
]
y0 = 438
sh, gap = 76, 8
for i, (cat, head, body, icon) in enumerate(stories):
    y = y0 + i * (sh + gap)
    rounded(28, y, 996, y + sh, 10, WHITE, outline=(203, 213, 225), width=1)
    d.rounded_rectangle([44, y + 8, 106, y + sh - 8], radius=8, fill=NAVY)
    ix, iy = 75, y + sh // 2
    if icon == "star":
        # Kyiv skyline at night, explosion burst over a building
        d.rectangle([ix - 22, iy - 6, ix - 8, iy + 20], fill=(180, 200, 230))
        d.rectangle([ix - 4, iy - 14, ix + 10, iy + 20], fill=(200, 215, 240))
        d.rectangle([ix + 14, iy - 2, ix + 22, iy + 20], fill=(180, 200, 230))
        pts = [(ix + 3, iy - 26), (ix + 8, iy - 16), (ix + 18, iy - 16), (ix + 10, iy - 10),
               (ix + 13, iy - 1), (ix + 3, iy - 6), (ix - 7, iy - 1), (ix - 4, iy - 10),
               (ix - 12, iy - 16), (ix - 2, iy - 16)]
        d.polygon(pts, fill=(245, 158, 11))
        d.ellipse([ix - 14, iy - 26, ix - 4, iy - 16], fill=(120, 120, 120))
    elif icon == "chart":
        # falling market: red candlesticks and a down arrow
        for cx, ch, cw in [(ix - 16, 14, 5), (ix - 5, 20, 5), (ix + 6, 26, 5), (ix + 17, 32, 5)]:
            d.rectangle([cx - 2, iy - 4, cx + 2, iy - 4 + ch], fill=(239, 68, 68))
        d.line([(ix - 22, iy - 18), (ix - 8, iy - 6), (ix + 4, iy + 2), (ix + 20, iy + 14)],
               fill=WHITE, width=4)
        d.polygon([(ix + 20, iy + 14), (ix + 20, iy + 4), (ix + 12, iy + 14)], fill=WHITE)
    elif icon == "capitol":
        # US Capitol dome with columns and a flag
        d.rectangle([ix - 18, iy + 2, ix + 18, iy + 16], fill=WHITE)
        for col in (-12, -4, 4, 12):
            d.rectangle([ix + col - 1, iy + 4, ix + col + 1, iy + 14], fill=NAVY)
        d.ellipse([ix - 9, iy - 14, ix + 9, iy + 2], fill=WHITE)
        d.line([(ix, iy - 14), (ix, iy - 24)], fill=WHITE, width=2)
        d.polygon([(ix, iy - 24), (ix + 9, iy - 21), (ix, iy - 18)], fill=(239, 68, 68))
    elif icon == "ship":
        # warship at sea, drone above, hit burst on deck
        d.line([(ix - 22, iy + 16), (ix + 22, iy + 16)], fill=(56, 189, 248), width=4)
        d.line([(ix - 20, iy + 20), (ix + 20, iy + 20)], fill=(56, 189, 248), width=3)
        d.polygon([(ix - 20, iy - 4), (ix + 20, iy - 4), (ix + 12, iy + 12),
                   (ix - 12, iy + 12)], fill=WHITE)
        d.rectangle([ix - 2, iy - 14, ix + 2, iy - 4], fill=WHITE)
        d.ellipse([ix - 4, iy - 24, ix + 4, iy - 18], fill=(200, 200, 200))
        d.line([(ix - 8, iy - 21), (ix + 8, iy - 21)], fill=(200, 200, 200), width=2)
        pts = [(ix + 8, iy - 12), (ix + 11, iy - 6), (ix + 17, iy - 6), (ix + 12, iy - 2),
               (ix + 14, iy + 3), (ix + 8, iy + 0), (ix + 2, iy + 3), (ix + 4, iy - 2),
               (ix - 1, iy - 6), (ix + 5, iy - 6)]
        d.polygon(pts, fill=(245, 158, 11))
    else:
        # handcuffs over a police star
        d.ellipse([ix - 18, iy - 12, ix - 2, iy + 4], outline=WHITE, width=3)
        d.ellipse([ix + 2, iy + 2, ix + 18, iy + 18], outline=WHITE, width=3)
        d.line([(ix - 2, iy - 4), (ix + 2, iy + 10)], fill=WHITE, width=3)
        d.ellipse([ix - 6, iy - 22, ix + 6, iy - 10], fill=(245, 158, 11))
    d.text((122, y + 8), cat, font=F_SANS_B(17), fill=RED)
    d.text((122, y + 28), head, font=F_SANS_B(27), fill=INK)
    d.text((122, y + 56), body, font=F_SANS(19), fill=GREY)

# ALSO strip
ay0 = y0 + 5 * (sh + gap) + 2
rounded(28, ay0, 996, ay0 + 84, 10, WHITE, outline=(203, 213, 225), width=1)
d.text((48, ay0 + 8), "ALSO ON 23 NOVEMBER", font=F_SANS_B(18), fill=RED)
also = [
    ("SUDAN", "Drone attacks kill children in Khartoum"),
    ("SOUTH SUDAN", "Attack kills at least 24 civilians"),
    ("INDONESIA", "Candy factory fire, 34 workers missing"),
    ("SPORT", "M\u00e1rquez wins eighth MotoGP title"),
]
for j, (k, v) in enumerate(also):
    x = 48 + (j % 2) * 484
    yy = ay0 + 36 + (j // 2) * 24
    d.text((x, yy), k + " \u2014 " + v, font=F_SANS(18), fill=INK)

# Footer
fy = ay0 + 94
d.line([28, fy, 996, fy], fill=INK, width=2)
text_center(fy + 8, "23 NOVEMBER 2026  \u2022  COP31  \u2022  KYIV  \u2022  MARKETS  \u2022  U.S. HOUSE  \u2022  BLACK SEA  \u2022  MEXICO",
            F_SANS_B(16), INK)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
