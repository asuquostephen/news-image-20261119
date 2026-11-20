#!/usr/bin/env python3
"""Draws this entry's news image: one picture summing up the world's news of
Thursday 19 November 2026. Run with Pillow available:

    python3 draw.py            # writes ./entry.png beside this file

The submitted program is main.py, which copies the finished entry.png to
/output/entry.png exactly as the starter entry does; draw.py is kept in the
repository so anyone can see (and re-run) how the image itself was made.
All story text below is factual copy written from the day's reporting
(see BUILD-STATUS.md in the build folder for the sources).

Layout is measured, not guessed: every text block is word-wrapped at its
real pixel width, block heights are computed from the wrapped line counts,
and the font profile is stepped down until the whole page fits 1024x1024.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 36

BG = (13, 20, 38)          # deep navy
PANEL = (22, 34, 58)       # lead panel
CARD = (19, 29, 50)        # story card
INK = (242, 245, 250)      # near-white
SOFT = (185, 198, 220)     # caption grey-blue
GOLD = (232, 179, 60)
RED = (226, 75, 63)
RULE = (74, 92, 128)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

DATE_LINE = "THURSDAY  \u00b7  19 NOVEMBER 2026"

LEAD_TAG = "TOP STORY \u2014 THE HAGUE"
LEAD_HEADLINE = "World Court Rules Myanmar Committed Genocide Against the Rohingya"
LEAD_CAPTION = (
    "The Hague court found Myanmar responsible for genocide in its 2017 crackdown "
    "in Rakhine State \u2014 a first such ruling against a state."
)

# (category, colour, headline, caption)
STORIES = [
    (
        "DIPLOMACY \u00b7 SHENZHEN", (108, 178, 245),
        "Trump, Xi and Putin Hold First Three-Way Summit",
        "The US, Chinese and Russian presidents met in Shenzhen, signing a joint "
        "declaration on nuclear-risk talks \u2014 no peace deal.",
    ),
    (
        "BUSINESS \u00b7 NEW YORK", (127, 208, 140),
        "Anthropic Debuts in the Largest IPO in History",
        "The Claude AI maker raised $81.3bn at $83 a share; shares opened 30% "
        "higher, valuing the firm near $1.5 trillion.",
    ),
    (
        "CULTURE \u00b7 WORLDWIDE", (229, 142, 199),
        "GTA VI Launches to Rave Reviews After 13-Year Wait",
        "Rockstar's first GTA since 2013 scored 99/100 on Metacritic; IGN called "
        "it a masterpiece. Out now on PS5 and Xbox.",
    ),
    (
        "EUROPE \u00b7 COPENHAGEN", (154, 142, 245),
        "Denmark Approves Greenland\u2013US Security Pact",
        "Lawmakers voted 109\u20130 for an expanded Arctic defence arrangement "
        "with the United States centred on Greenland.",
    ),
    (
        "POLITICS \u00b7 WASHINGTON", (245, 142, 108),
        "Senate Rejects Bid to Rein In Iran Strikes, 51\u201348",
        "The war-powers resolution failed despite three Republican votes in "
        "favour, leaving strike authority with the president.",
    ),
    (
        "BUSINESS \u00b7 BENTONVILLE", (127, 208, 140),
        "Walmart Sales Reach $188.8bn as Shoppers Hunt Value",
        "Revenue rose 5.2% and US online sales jumped 23% as value-hunting "
        "shoppers drove growth; the outlook was raised.",
    ),
]

FOOTER_LEFT = "ONE DAY \u00b7 ONE PICTURE"
FOOTER_RIGHT = "Compiled from the day's reporting: wires, broadsheets and broadcasters worldwide"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def measure(draw, profile):
    """Wrap everything at this profile's sizes; return the layout plan."""
    inner_w = W - 2 * MARGIN
    lead_pw = inner_w - 62
    col_w = (inner_w - 14) // 2
    card_tw = col_w - 44

    lead_head = wrap(draw, LEAD_HEADLINE, font(SERIF_B, profile["lead_head"]), lead_pw)
    lead_cap = wrap(draw, LEAD_CAPTION, font(SANS, profile["lead_cap"]), lead_pw)
    lead_h = (18 + 34 + 10 + len(lead_head) * profile["lead_head"] * 1.08
              + 7 + len(lead_cap) * profile["lead_cap"] * 1.18 + 16)

    cards = []
    for cat, colour, head, cap in STORIES:
        hl = wrap(draw, head, font(SANS_B, profile["card_head"]), card_tw)
        cl = wrap(draw, cap, font(SANS, profile["cap"]), card_tw)
        h = (15 + 28 + len(hl) * profile["card_head"] * 1.1
             + 5 + len(cl) * profile["cap"] * 1.16 + 12)
        cards.append((cat, colour, hl, cl, h))
    row_h = [max(cards[r * 2][4], cards[r * 2 + 1][4]) for r in range(3)]

    masthead_h = 24 + 32 + profile["title"] + 46
    total = (masthead_h + lead_h + 12 + sum(row_h) + 2 * 12 + 54)
    return {
        "lead_head": lead_head, "lead_cap": lead_cap, "lead_h": lead_h,
        "cards": cards, "row_h": row_h, "masthead_h": masthead_h,
        "col_w": col_w, "total": total,
    }


PROFILES = [
    {"title": 80, "lead_head": 46, "lead_cap": 25, "card_head": 27, "cap": 21},
    {"title": 76, "lead_head": 44, "lead_cap": 24, "card_head": 26, "cap": 20},
    {"title": 72, "lead_head": 42, "lead_cap": 23, "card_head": 25, "cap": 19},
    {"title": 68, "lead_head": 40, "lead_cap": 22, "card_head": 24, "cap": 18},
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    plan, profile = None, PROFILES[-1]
    for p in PROFILES:
        plan = measure(d, p)
        profile = p
        if plan["total"] <= H:
            break
    assert plan["total"] <= H, f"layout does not fit: {plan['total']}"

    inner_w = W - 2 * MARGIN

    # ---------- masthead ----------
    y = 24
    kicker = "T H E   W O R L D   I N   O N E   P I C T U R E"
    kf = font(SANS_B, 23)
    kw = d.textlength(kicker, font=kf)
    d.text(((W - kw) / 2, y), kicker, font=kf, fill=GOLD)
    y += 32
    title = "WORLD NEWS"
    tf = font(SERIF_B, profile["title"])
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, y), title, font=tf, fill=INK)
    y += profile["title"]
    df = font(SANS_B, 30)
    dw = d.textlength(DATE_LINE, font=df)
    d.text(((W - dw) / 2, y), DATE_LINE, font=df, fill=GOLD)
    ry = y + 19
    d.line([(MARGIN, ry), ((W - dw) / 2 - 22, ry)], fill=RULE, width=2)
    d.line([((W + dw) / 2 + 22, ry), (W - MARGIN, ry)], fill=RULE, width=2)
    y += 46

    # ---------- lead story ----------
    lead_x, lead_y, lead_w = MARGIN, y, inner_w
    lead_h = plan["lead_h"]
    d.rounded_rectangle([lead_x, lead_y, lead_x + lead_w, lead_y + lead_h],
                        radius=14, fill=PANEL)
    d.rectangle([lead_x, lead_y + 14, lead_x + 10, lead_y + lead_h - 14], fill=RED)
    px = lead_x + 34
    py = lead_y + 18
    tag_f = font(SANS_B, 20)
    tag_w = d.textlength(LEAD_TAG, font=tag_f) + 28
    d.rounded_rectangle([px, py, px + tag_w, py + 34], radius=8, fill=RED)
    d.text((px + 14, py + 6), LEAD_TAG, font=tag_f, fill=(255, 255, 255))
    py += 44
    hf = font(SERIF_B, profile["lead_head"])
    for ln in plan["lead_head"]:
        d.text((px, py), ln, font=hf, fill=INK)
        py += profile["lead_head"] * 1.08
    py += 7
    cf = font(SANS, profile["lead_cap"])
    for ln in plan["lead_cap"]:
        d.text((px, py), ln, font=cf, fill=SOFT)
        py += profile["lead_cap"] * 1.18
    y = lead_y + lead_h + 12

    # ---------- story grid: 2 columns x 3 rows ----------
    gap = 14
    col_w = plan["col_w"]
    for i, (cat, colour, hl, cl, _h) in enumerate(plan["cards"]):
        cx = MARGIN + (i % 2) * (col_w + gap)
        cy = y + sum(plan["row_h"][: i // 2]) + (i // 2) * gap
        rh = plan["row_h"][i // 2]
        d.rounded_rectangle([cx, cy, cx + col_w, cy + rh], radius=12, fill=CARD)
        tx = cx + 22
        ty = cy + 15
        d.rectangle([tx, ty + 2, tx + 12, ty + 15], fill=colour)
        d.text((tx + 20, ty), cat, font=font(SANS_B, 18), fill=colour)
        ty += 28
        hf = font(SANS_B, profile["card_head"])
        for ln in hl:
            d.text((tx, ty), ln, font=hf, fill=INK)
            ty += profile["card_head"] * 1.1
        ty += 5
        cf = font(SANS, profile["cap"])
        for ln in cl:
            d.text((tx, ty), ln, font=cf, fill=SOFT)
            ty += profile["cap"] * 1.16

    # ---------- footer ----------
    fy = H - 40
    d.line([(MARGIN, fy - 13), (W - MARGIN, fy - 13)], fill=RULE, width=2)
    d.text((MARGIN, fy), FOOTER_LEFT, font=font(SANS_B, 19), fill=GOLD)
    rf = font(SANS, 17)
    rw = d.textlength(FOOTER_RIGHT, font=rf)
    d.text((W - MARGIN - rw, fy + 1), FOOTER_RIGHT, font=rf, fill=SOFT)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size, "layout total:", round(plan["total"]))


if __name__ == "__main__":
    main()
