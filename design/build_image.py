#!/usr/bin/env python3
"""Draw the entry image: one day of world news as a broadsheet front page.

Renders "THE WORLD IN ONE DAY" for Tuesday 24 November 2026 at 1024x1024
with Pillow, using only precise typesetting (no generated imagery), and
writes the result to ../assets/entry.png relative to this file.

Run locally with:  python3 design/build_image.py
This script is a build tool only; the submitted program (main.py) ships
the rendered PNG as an asset and copies it, because the grading sandbox
has no Pillow.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 234)      # off-white newsprint
INK = (20, 16, 12)           # near-black ink
INK_SOFT = (43, 37, 30)      # body text
RED = (164, 18, 24)          # deep red accent
NAVY = (31, 58, 95)          # muted navy secondary
RULE_SOFT = (120, 110, 96)   # hairline grey-brown

W = H = 1024
MARGIN = 28
CW = W - 2 * MARGIN          # content width: 968

FONT_DIR = Path("/usr/share/fonts/truetype")
SERIF_BOLD = FONT_DIR / "noto/NotoSerif-Bold.ttf"
SANS_BOLD = FONT_DIR / "liberation/LiberationSans-Bold.ttf"
SANS = FONT_DIR / "liberation/LiberationSans-Regular.ttf"
COND_BOLD = FONT_DIR / "noto/NotoSans-ExtraCondensedBold.ttf"
COND = FONT_DIR / "noto/NotoSans-Condensed.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def text_w(draw: ImageDraw.ImageDraw, s: str, f: ImageFont.FreeTypeFont) -> float:
    return draw.textlength(s, font=f)


def wrap(draw, s, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in s.split():
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_size(draw, s, path, start, max_w, minimum=10):
    """Largest font size <= start whose single line fits max_w."""
    size = start
    while size > minimum:
        if text_w(draw, s, font(path, size)) <= max_w:
            return size
        size -= 1
    return minimum


def draw_centered(draw, y, s, f, fill):
    draw.text(((W - text_w(draw, s, f)) / 2, y), s, font=f, fill=fill)


def draw_pill(draw, x, y, s, f, fill, fg=(255, 255, 255), pad_x=10, pad_y=4):
    w = text_w(draw, s, f)
    bbox = draw.textbbox((0, 0), s, font=f)
    h = bbox[3] - bbox[1]
    draw.rounded_rectangle(
        [x, y, x + w + 2 * pad_x, y + h + 2 * pad_y], radius=(h + 2 * pad_y) // 2,
        fill=fill,
    )
    draw.text((x + pad_x, y + pad_y - bbox[1]), s, font=f, fill=fg)
    return w + 2 * pad_x, h + 2 * pad_y


def draw_globe(draw, cx, cy, r, colour, width=2):
    """Simple geometric globe: outline, meridians and parallels."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=width)
    for frac in (0.45, 0.8):
        rx = r * frac
        draw.ellipse([cx - rx, cy - r, cx + rx, cy + r], outline=colour, width=1)
    draw.line([cx - r, cy, cx + r, cy], fill=colour, width=1)
    for frac in (-0.5, 0.5):
        yy = cy + r * frac
        half = (r * r - (r * frac) ** 2) ** 0.5
        draw.line([cx - half, yy, cx + half, yy], fill=colour, width=1)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)


# ---------------------------------------------------------------- content
TITLE = "THE WORLD IN ONE DAY"
DATE_LINE = "TUESDAY 24 NOVEMBER 2026"
STRIP_LEFT = "GLOBAL EDITION"
STRIP_RIGHT = "ONE DAY · ONE PAGE"

HERO_TAG = "TOP STORY · MARKETS & TECH"
HERO_HEADLINE = "NVIDIA COMEBACK IGNITES A GLOBAL RALLY"
HERO_TAKEAWAY = (
    "Two weeks after resigning, Jensen Huang is reinstated as Nvidia CEO; "
    "the stock closes up 31% in New York. On Tuesday, Asia surges: "
    "Tokyo +4%, Seoul +7%, Taipei +9%."
)

STORIES = [
    ("MIDDLE EAST", "HOUTHI STRIKE HITS RIYADH'S TALLEST TOWER",
     "A second strike on the tower in five days injures 11 people."),
    ("MIDDLE EAST", "ISRAELI STRIKE KILLS HAMAS SECURITY CHIEF",
     "Naeem Abu Nahel and six others are killed in Gaza City."),
    ("EUROPE", "RUSSIAN ATTACK ON ZAPORIZHZHIA KILLS TWO",
     "An overnight strike on an apartment block kills two and wounds 40, including four children."),
    ("EUROPE", "NATO VOWS SPACE DEFENCE OVER SATELLITE REPORTS",
     "Rutte says the alliance will defend space after reports Russia plans a nuclear-armed satellite."),
    ("AFRICA", "UKRAINE SINKS RUSSIAN CORVETTE OFF LIBYA",
     "Kyiv says its naval drones sank the corvette Merkury in Benghazi port."),
    ("AFRICA", "FIGHTING TRAPS EBOLA TEAMS IN DR CONGO",
     "Battles near an Ituri hospital force responders to take cover for over a day."),
    ("SPORT", "SENEGAL RESTORED AS AFRICA CUP CHAMPIONS",
     "Sport's top court rules in Senegal's favour over the 2025 title."),
    ("ASIA-PACIFIC", "RUSSIAN JETS ENTER KOREA AIR DEFENCE ZONE",
     "The jets cross the air defence identification zone; Ulleungdo islanders are told to shelter."),
    ("SCIENCE & TECH", "SEOUL PAYS BOUNTIES TO CATCH AI EXAM CHEATERS",
     "Up to $375,000 is offered for tips on AI cheating in the national college entrance exam."),
]

TICKER_LABEL = "ALSO ON TUESDAY"
TICKER = (
    "Landmine deaths hit a five-year high of 7,000 · Iraq's PM orders takeover "
    "of Kurdish-region oilfields · Car bomb destroys buildings in "
    "Villavicencio, Colombia · Spain's top court grants amnesty to Puigdemont "
    "· Nepal hit by 5.6-magnitude quake near China border"
)


# ---------------------------------------------------------------- drawing
def build() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    y = 12
    f_title = font(SERIF_BOLD, 48)
    draw_centered(d, y, TITLE, f_title, INK)
    title_w = text_w(d, TITLE, f_title)
    globe_cx = (W - title_w) / 2 - 44
    draw_globe(d, globe_cx, y + 27, 21, NAVY)
    draw_globe(d, W - globe_cx, y + 27, 21, NAVY)
    y += 60

    # Date line, flanked by the edition strips in classic newspaper style.
    date_size = fit_size(d, DATE_LINE, SANS_BOLD, 56, CW - 390)
    f_date = font(SANS_BOLD, date_size)
    draw_centered(d, y, DATE_LINE, f_date, RED)
    f_strip = font(SANS_BOLD, 15)
    mid = y + date_size // 2 - 8
    d.text((MARGIN, mid), STRIP_LEFT, font=f_strip, fill=INK)
    rw = text_w(d, STRIP_RIGHT, f_strip)
    d.text((W - MARGIN - rw, mid), STRIP_RIGHT, font=f_strip, fill=INK)
    y += date_size + 12
    d.rectangle([MARGIN, y, W - MARGIN, y + 6], fill=INK)
    d.line([MARGIN, y + 10, W - MARGIN, y + 10], fill=INK, width=2)
    y += 14

    # ---- hero ----------------------------------------------------------
    f_tag = font(SANS_BOLD, 18)
    draw_pill(d, MARGIN, y, HERO_TAG, f_tag, RED)
    y += 30

    hero_size = fit_size(d, "NVIDIA COMEBACK IGNITES", SANS_BOLD, 50, CW)
    f_hero = font(SANS_BOLD, hero_size)
    hero_lh = hero_size + 6
    # Slightly narrower measure so the two lines balance instead of
    # leaving one short word alone on the second line.
    for line in wrap(d, HERO_HEADLINE, f_hero, int(CW * 0.93)):
        d.text((MARGIN, y), line, font=f_hero, fill=INK)
        y += hero_lh
    y += 2

    f_take = font(SANS, 22)
    for line in wrap(d, HERO_TAKEAWAY, f_take, CW):
        d.text((MARGIN, y), line, font=f_take, fill=INK_SOFT)
        y += 27
    y += 4
    d.line([MARGIN, y, W - MARGIN, y], fill=RULE_SOFT, width=2)
    y += 8

    # ---- story cards ---------------------------------------------------
    cards_top = y
    ticker_h = 84
    cards_bottom = H - MARGIN - ticker_h
    gap = 12
    col_w = (CW - 2 * gap) // 3
    inner_w = col_w - 20

    # Pick the largest type sizes whose wrapped cards fit the space.
    chosen = None
    for hs in range(32, 25, -1):
        for ts in range(20, 16, -1):
            f_h, f_t = font(COND_BOLD, hs), font(COND, ts)
            rows = []
            for r in range(3):
                need = 0
                for c in range(3):
                    _, head, take = STORIES[r * 3 + c]
                    hl = len(wrap(d, head, f_h, inner_w))
                    tl = len(wrap(d, take, f_t, inner_w))
                    need = max(need, 6 + 24 + hl * (hs + 3) + tl * (ts + 4) + 4)
                rows.append(need)
            if sum(rows) + 2 * gap <= cards_bottom - cards_top:
                chosen = (hs, ts, rows)
                break
        if chosen:
            break
    if chosen is None:
        raise SystemExit("card content does not fit at any tried size")
    hs, ts, row_h = chosen
    print(f"card type: headline {hs}px, takeaway {ts}px, rows {row_h}")
    f_head, f_take_c = font(COND_BOLD, hs), font(COND, ts)
    f_pill = font(SANS_BOLD, 13)

    # Spread any leftover height evenly between the rows so the grid
    # fills its area instead of leaving a gap above the ticker.
    leftover = (cards_bottom - cards_top) - (sum(row_h) + 2 * gap)
    row_gap = gap + max(0, leftover) // 2

    cy = cards_top
    for r in range(3):
        cx = MARGIN
        for c in range(3):
            tag, head, take = STORIES[r * 3 + c]
            d.rectangle([cx, cy, cx + col_w, cy + 3], fill=INK)
            ty = cy + 6
            draw_pill(d, cx + 10, ty, tag, f_pill, NAVY, pad_x=8, pad_y=3)
            ty += 24
            for line in wrap(d, head, f_head, inner_w):
                d.text((cx + 10, ty), line, font=f_head, fill=INK)
                ty += hs + 3
            ty += 0
            for line in wrap(d, take, f_take_c, inner_w):
                d.text((cx + 10, ty), line, font=f_take_c, fill=INK_SOFT)
                ty += ts + 4
            cx += col_w + gap
        cy += row_h[r] + row_gap

    # ---- ticker ----------------------------------------------------------
    ty = H - MARGIN - ticker_h + 4
    d.line([MARGIN, ty, W - MARGIN, ty], fill=INK, width=3)
    d.line([MARGIN, ty + 5, W - MARGIN, ty + 5], fill=INK, width=1)
    ty += 12
    f_tick_label = font(SANS_BOLD, 16)
    d.text((MARGIN, ty), TICKER_LABEL, font=f_tick_label, fill=RED)
    ty += 22
    f_tick = font(SANS, 18)
    for line in wrap(d, TICKER, f_tick, CW):
        d.text((MARGIN, ty), line, font=f_tick, fill=INK_SOFT)
        ty += 23

    return img


def main() -> None:
    out = Path(__file__).resolve().parent.parent / "assets" / "entry.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    img = build()
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
