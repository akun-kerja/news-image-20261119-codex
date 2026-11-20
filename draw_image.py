from PIL import Image, ImageDraw, ImageFont
import os
import textwrap


W = H = 1024
PAPER = (244, 240, 229)
INK = (22, 30, 37)
MUTED = (92, 98, 98)
RULE = (193, 186, 168)
RED = (167, 48, 37)
BLUE = (35, 72, 91)
GOLD = (194, 146, 61)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)


def f(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def fit(text, max_width, start, bold=True, minimum=12):
    for size in range(start, minimum - 1, -1):
        face = f(size, bold)
        if d.textbbox((0, 0), text, font=face)[2] <= max_width:
            return face
    return f(minimum, bold)


def wrap_draw(text, x, y, width, face, fill=INK, leading=4, max_lines=3):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = (line + " " + word).strip()
        if d.textbbox((0, 0), test, font=face)[2] <= width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    for i, s in enumerate(lines[:max_lines]):
        d.text((x, y), s, font=face, fill=fill)
        y += face.size + leading
    return y


def rule(y, x1=42, x2=982, fill=RULE, thick=1):
    d.line((x1, y, x2, y), fill=fill, width=thick)


# Newspaper masthead and issue line
d.rectangle((0, 0, W, 9), fill=RED)
d.text((42, 25), "THE WORLD LEDGER", font=f(35, True), fill=INK)
d.text((691, 36), "GLOBAL EDITION  /  NO. 324", font=f(13, True), fill=BLUE)
rule(77, 42, 982, INK, 2)
d.text((43, 89), "WORLD NEWS", font=f(13, True), fill=RED)
d.text((43, 108), "THURSDAY, 19 NOVEMBER 2026", font=f(18, True), fill=INK)
d.text((798, 111), "SIX STORIES. ONE DAY.", font=f(12, True), fill=MUTED)
rule(143, 42, 982, INK, 2)

# Lead story: a restrained courtroom illustration anchors the page.
lead_x, lead_y, lead_w, lead_h = 42, 158, 940, 353
d.rounded_rectangle((lead_x, lead_y, lead_x + lead_w, lead_y + lead_h), radius=5, fill=(232, 226, 211))
d.rectangle((lead_x, lead_y, lead_x + 10, lead_y + lead_h), fill=RED)
d.text((70, 178), "THE HAGUE  /  INTERNATIONAL JUSTICE", font=f(13, True), fill=RED)
d.text((70, 204), "WORLD COURT RULES MYANMAR", font=fit("WORLD COURT RULES MYANMAR", 635, 36), fill=INK)
d.text((70, 247), "COMMITTED GENOCIDE", font=fit("COMMITTED GENOCIDE", 635, 43), fill=RED)
wrap_draw("In a first ruling of its kind against a State, the ICJ finds Myanmar responsible for genocide against the Rohingya.", 70, 304, 615, f(18), fill=INK, leading=7, max_lines=3)
d.text((70, 398), "GAMBIA BROUGHT THE CASE IN 2019", font=f(13, True), fill=BLUE)

# Court icon, drawn only from geometric forms.
cx, cy = 802, 273
d.ellipse((cx - 66, cy - 54, cx + 66, cy + 78), fill=(222, 212, 190), outline=(177, 161, 132), width=2)
d.polygon([(cx - 48, cy - 18), (cx, cy - 49), (cx + 48, cy - 18)], fill=BLUE)
d.rectangle((cx - 48, cy - 17, cx + 48, cy - 8), fill=BLUE)
for dx in (-34, -12, 12, 34):
    d.rectangle((cx + dx - 4, cy - 7, cx + dx + 4, cy + 35), fill=(250, 246, 235))
d.rectangle((cx - 55, cy + 35, cx + 55, cy + 45), fill=BLUE)
d.rectangle((cx - 65, cy + 46, cx + 65, cy + 56), fill=BLUE)
d.text((744, 348), "A LANDMARK", font=f(12, True), fill=BLUE)
d.text((732, 365), "ACCOUNTABILITY", font=f(12, True), fill=BLUE)
d.text((713, 459), "ROHINGYA  •  MYANMAR  •  GAMBIA", font=fit("ROHINGYA  •  MYANMAR  •  GAMBIA", 235, 12), fill=MUTED)
d.text((70, 463), "THE WORLD COURT  •  19 NOVEMBER", font=f(12, True), fill=MUTED)

# Two columns of compact dispatches, with clear numerals and restrained accents.
rule(531, 42, 982, INK, 2)
d.text((43, 543), "DIPLOMACY & CONFLICT", font=f(12, True), fill=RED)
d.text((524, 543), "SOCIETY & THE ECONOMY", font=f(12, True), fill=RED)
d.line((505, 566, 505, 920), fill=RULE, width=1)


def story(x, y, width, number, kicker, headline, body, accent=BLUE):
    d.text((x, y), number, font=f(24, True), fill=accent)
    d.text((x + 42, y + 2), kicker.upper(), font=f(10, True), fill=MUTED)
    head_face = fit(headline, width - 42, 20, True, 15)
    hy = y + 20
    hy = wrap_draw(headline, x + 42, hy, width - 42, head_face, fill=INK, leading=2, max_lines=2)
    by = hy + 4
    wrap_draw(body, x + 42, by, width - 49, f(12), fill=(56, 62, 63), leading=3, max_lines=3)


story(47, 573, 442, "01", "Shenzhen · APEC", "Three leaders meet in historic summit", "Trump, Putin and Xi issue a four-point Declaration toward Peace. Ukraine dominates the talks.", BLUE)
rule(681, 58, 486)
story(47, 694, 442, "02", "Central Gaza · Nuseirat", "Israeli forces cross ceasefire line", "Ground operation unfolds despite the truce; aid groups rate peace-plan progress 4 of 26.", RED)
rule(802, 58, 486)
story(47, 814, 442, "03", "COP31 · Antalya / Energy", "Climate talks race against the clock", "Ministers seek a final text; IEA calls the Hormuz crisis the greatest energy-security threat observed.", GOLD)

story(526, 573, 456, "04", "Bangladesh · 28 districts", "Unrest kills four; Yunus home burned", "The ancestral home of Nobel laureate Muhammad Yunus is set on fire as political unrest spreads.", RED)
rule(681, 538, 982)
story(526, 694, 456, "05", "Art market · Record sale", "Van Gogh sells for $190.4 million", "A new auction record for a painting, as money and culture make headlines worldwide.", GOLD)
rule(802, 538, 982)
story(526, 814, 456, "06", "Technology · Markets", "Anthropic raises about $81 billion", "A record-setting IPO puts the AI company among the day’s biggest financial stories.", BLUE)

# Footer gives the eye a firm endpoint and keeps all type inside the page.
rule(925, 42, 982, INK, 2)
d.text((43, 940), "A DAY OF JUSTICE, DIPLOMACY, CONFLICT, CLIMATE AND RECORDS", font=fit("A DAY OF JUSTICE, DIPLOMACY, CONFLICT, CLIMATE AND RECORDS", 780, 14), fill=INK)
d.text((884, 940), "01 / 01", font=f(12, True), fill=RED)
d.line((42, 964, 982, 964), fill=RULE, width=1)
d.text((43, 973), "Sources: UN News, Horizon, 10 Things, eGazette, BBC, Foreign Exchanges — 19 November 2026", font=fit("Sources: UN News, Horizon, 10 Things, eGazette, BBC, Foreign Exchanges — 19 November 2026", 930, 12, False, 10), fill=MUTED)
d.rectangle((0, 1013, W, 1024), fill=RED)

im.save("entry.png", format="PNG", optimize=True)
