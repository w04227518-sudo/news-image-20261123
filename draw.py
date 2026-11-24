#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261123 (v4).

Back to the v2 newspaper front-page approach (text-led, simple abstract
icons), with one change: the COP31 lead story gets a large generated
hero illustration (assets/cop31-hero.png, domed conference hall in
Antalya) taking about half the page, and the ALSO strip is compressed
from four items to two short ones. 1024x1024, PIL + DejaVu only.
Eight stories from Monday 23 November 2026. No network, deterministic
output: the hero image is a committed asset, cropped and resized the
same way on every run.
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
text_center(128, "Eight stories that defined the day", F_SANS(20), GREY)

# Hero panel: COP31, about half the page
rounded(28, 156, 996, 540, 12, WHITE, outline=INK, width=2)
d.text((48, 170), "CLIMATE  \u2022  ANTALYA, TURKEY", font=F_SANS_B(21), fill=RED)
d.text((48, 198), "COP31 COLLAPSES", font=F_SANS_B(48), fill=INK)
d.text((48, 252), "WITH NO DEAL", font=F_SANS_B(48), fill=INK)
body = ("Climate talks end after two days of overtime. The EU and "
        "about 130 countries rejected a text with no fossil-fuel "
        "phase-out.")
y = 322
for line in textwrap.wrap(body, width=46):
    d.text((48, y), line, font=F_SANS(19), fill=INK)
    y += 25
d.rectangle([48, 412, 218, 438], fill=RED)
d.text((78, 417), "TOP STORY", font=F_SANS_B(20), fill=WHITE)
# Hero illustration: generated domed conference hall, centre-cropped
# to the box and resized, deterministically.
hero = Image.open("assets/cop31-hero.png").convert("RGB")
hx0, hy0, hx1, hy1 = 560, 170, 976, 512
tw, th = hx1 - hx0, hy1 - hy0
sw, sh = hero.size
target = tw / th
if sw / sh > target:
    nw = int(sh * target)
    x0 = (sw - nw) // 2
    hero = hero.crop((x0, 0, x0 + nw, sh))
else:
    nh = int(sw / target)
    y0 = (sh - nh) // 2
    hero = hero.crop((0, y0, sw, y0 + nh))
hero = hero.resize((tw, th), Image.LANCZOS)
img.paste(hero, (hx0, hy0))
d.rectangle([hx0, hy0, hx1, hy1], outline=NAVY, width=2)
cap = "ANTALYA, TURKEY"
cw = d.textlength(cap, font=F_SANS_B(17))
d.text(((hx0 + hx1 - cw) / 2, 518), cap, font=F_SANS_B(17), fill=GREY)

# Story strips (v2 simple abstract icons)
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
y0 = 548
sh, gap = 64, 6
for i, (cat, head, body, icon) in enumerate(stories):
    y = y0 + i * (sh + gap)
    rounded(28, y, 996, y + sh, 10, WHITE, outline=(203, 213, 225), width=1)
    d.rounded_rectangle([44, y + 8, 106, y + sh - 8], radius=8, fill=NAVY)
    ix, iy = 75, y + sh // 2
    if icon == "star":
        pts = [(ix, iy - 22), (ix + 7, iy - 7), (ix + 23, iy - 7), (ix + 11, iy + 4),
               (ix + 16, iy + 20), (ix, iy + 10), (ix - 16, iy + 20), (ix - 11, iy + 4),
               (ix - 23, iy - 7), (ix - 7, iy - 7)]
        d.polygon(pts, fill=(245, 158, 11))
    elif icon == "chart":
        d.line([(ix - 20, iy + 12), (ix - 8, iy + 2), (ix + 2, iy + 8), (ix + 20, iy - 14)],
               fill=WHITE, width=4)
        d.polygon([(ix + 20, iy - 14), (ix + 12, iy - 14), (ix + 20, iy - 6)], fill=WHITE)
    elif icon == "capitol":
        d.rectangle([ix - 18, iy - 4, ix + 18, iy + 14], fill=WHITE)
        d.polygon([(ix - 12, iy - 4), (ix + 12, iy - 4), (ix, iy - 18)], fill=WHITE)
        d.rectangle([ix - 2, iy - 12, ix + 2, iy - 4], fill=WHITE)
    elif icon == "ship":
        d.polygon([(ix - 20, iy - 12), (ix + 20, iy - 12), (ix + 12, iy + 8),
                   (ix - 12, iy + 8)], fill=WHITE)
        d.rectangle([ix - 2, iy - 22, ix + 2, iy - 12], fill=WHITE)
        d.line([(ix - 22, iy + 14), (ix + 22, iy + 14)], fill=(56, 189, 248), width=4)
    else:
        d.ellipse([ix - 18, iy - 18, ix + 18, iy + 18], fill=(245, 158, 11))
        d.ellipse([ix - 12, iy - 12, ix + 12, iy + 12], outline=WHITE, width=3)
        d.text((ix - 5, iy - 8), "*", font=F_SANS_B(20), fill=NAVY)
    d.text((122, y + 5), cat, font=F_SANS_B(15), fill=RED)
    d.text((122, y + 22), head, font=F_SANS_B(24), fill=INK)
    d.text((122, y + 47), body, font=F_SANS(17), fill=GREY)

# ALSO strip: two short items only
ay0 = 900
rounded(28, ay0, 996, 976, 10, WHITE, outline=(203, 213, 225), width=1)
d.text((48, ay0 + 8), "ALSO ON 23 NOVEMBER", font=F_SANS_B(18), fill=RED)
d.text((48, ay0 + 34), "SUDAN \u2014 Drone attacks kill children in Khartoum",
       font=F_SANS(18), fill=INK)
d.text((48, ay0 + 56), "INDONESIA \u2014 Candy factory fire, 34 workers missing",
       font=F_SANS(18), fill=INK)

# Footer
d.line([28, 986, 996, 986], fill=INK, width=2)
text_center(994, "23 NOVEMBER 2026  \u2022  COP31  \u2022  KYIV  \u2022  MARKETS  \u2022  U.S. HOUSE  \u2022  BLACK SEA  \u2022  MEXICO",
            F_SANS_B(15), INK)

img.save("entry.png", format="PNG", optimize=True)
print("saved entry.png", img.size)
