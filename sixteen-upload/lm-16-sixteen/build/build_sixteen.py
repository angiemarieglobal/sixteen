#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIXTEEN -> print-ready, fillable A4 PDF
Angie Marie Global | lead magnet 16

RECOGNISE ASSET LAW (locked 27 July 2026, amg-brand-boards):
  - No gradients. Any fade is baked into a raster before it reaches the document.
  - No transparency. Every alpha value pre-mixed into a solid colour.
  - Plain DeviceRGB only. No soft masks, no transparency groups.
Reason: Chromium writes a CSS fade into a PDF as a shading with a transparency mask,
and some viewers render that mask as magenta. This script draws solid fills only,
so the file renders identically on Mac, PC, a print RIP and inside GHL.

FONTS: Forum (title) and Montserrat (subtitle, body) are the locked AMG type system.
Neither is reachable in this build environment, so Lora and Poppins stand in, matching
the Recognise Loop Map build of 27 July 2026. To swap in the real fonts, drop
Forum-Regular.ttf and Montserrat-{Light,Regular,Medium,SemiBold}.ttf into ./fonts and
set USE_REAL_FONTS = True.

Usage:  python3 build_sixteen.py
Output: ../dist/AMG-Sixteen.pdf
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import content as C

# --------------------------------------------------------------------------- #
# PALETTE - Recognise, de-pinked, locked 27 July 2026
# Retired and never reused: #945D36 #AF8B6C #E8CDAD #F7E3CB #FBF4E8
# --------------------------------------------------------------------------- #

def hx(h):
    h = h.lstrip("#")
    return Color(int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)

GOLDEN_SAND = hx("D09E69")   # signature accent
DEEP_UMBER  = hx("5D3520")   # anchor
WARM_CLAY   = hx("8A6238")   # sub-headers, descriptor copy
AMBER_EMBER = hx("C6792F")   # the small metallic signal
SAND_STONE  = hx("B7A184")   # dividers, ruled lines, neutral midtone
IVORY_GLOW  = hx("E6DAC2")   # soft rules, light borders
OAT_CREAM   = hx("F2E9D5")   # soft cards, callout blocks
PALE_OAT    = hx("FBF7EE")   # page background
ESPRESSO    = hx("2A1711")   # body text on light

# --------------------------------------------------------------------------- #
# FONTS
# --------------------------------------------------------------------------- #

USE_REAL_FONTS = False
HERE = os.path.dirname(os.path.abspath(__file__))
GF = "/usr/share/fonts/truetype/google-fonts"

if USE_REAL_FONTS:
    F_DIR = os.path.join(HERE, "fonts")
    pdfmetrics.registerFont(TTFont("Title", os.path.join(F_DIR, "Forum-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("TitleI", os.path.join(F_DIR, "Forum-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Body", os.path.join(F_DIR, "Montserrat-Light.ttf")))
    pdfmetrics.registerFont(TTFont("BodyR", os.path.join(F_DIR, "Montserrat-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("BodyM", os.path.join(F_DIR, "Montserrat-Medium.ttf")))
    pdfmetrics.registerFont(TTFont("BodySB", os.path.join(F_DIR, "Montserrat-SemiBold.ttf")))
    pdfmetrics.registerFont(TTFont("BodyI", os.path.join(F_DIR, "Montserrat-Light.ttf")))
else:
    pdfmetrics.registerFont(TTFont("Title", f"{GF}/Lora-Variable.ttf"))
    pdfmetrics.registerFont(TTFont("TitleI", f"{GF}/Lora-Italic-Variable.ttf"))
    pdfmetrics.registerFont(TTFont("Body", f"{GF}/Poppins-Light.ttf"))
    pdfmetrics.registerFont(TTFont("BodyR", f"{GF}/Poppins-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("BodyM", f"{GF}/Poppins-Medium.ttf"))
    pdfmetrics.registerFont(TTFont("BodySB", f"{GF}/Poppins-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("BodyI", f"{GF}/Poppins-LightItalic.ttf"))

# --------------------------------------------------------------------------- #
# GEOMETRY
# --------------------------------------------------------------------------- #

W, H = A4
M = 52.0                 # side margin
CW = W - 2 * M           # content width
OUT = os.path.join(HERE, "..", "dist", "AMG-Sixteen.pdf")
BANNER = os.path.join(HERE, "..", "assets", "sixteen-cover.jpg")

# --------------------------------------------------------------------------- #
# PRIMITIVES - solid fills only, never a gradient, never an alpha
# --------------------------------------------------------------------------- #

def page_bg(c):
    c.setFillColor(PALE_OAT)
    c.rect(0, 0, W, H, stroke=0, fill=1)


def tracked(c, text, x, y, font, size, colour, track=1.6, centre=False):
    """Letter-spaced text. reportlab has no tracking, so glyphs are placed by hand."""
    c.setFont(font, size)
    c.setFillColor(colour)
    total = sum(pdfmetrics.stringWidth(ch, font, size) + track for ch in text) - track
    cx = x - total / 2.0 if centre else x
    for ch in text:
        c.drawString(cx, y, ch)
        cx += pdfmetrics.stringWidth(ch, font, size) + track
    return total


def para(c, text, x, y, width, font, size, leading, colour, italic=False):
    """Draw a wrapped paragraph. Returns the y below the last line."""
    c.setFont(font, size)
    c.setFillColor(colour)
    for line in simpleSplit(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def para_h(text, width, font, size, leading):
    """Height a paragraph will occupy, without drawing it."""
    return len(simpleSplit(text, font, size, width)) * leading


def rule(c, x, y, width, colour=SAND_STONE, w=0.6):
    c.setStrokeColor(colour)
    c.setLineWidth(w)
    c.line(x, y, x + width, y)


def label(c, text, x, y, colour=SAND_STONE, size=7.0):
    tracked(c, text, x, y, "BodyM", size, colour, track=2.0)


def card(c, x, y, width, height, fill=OAT_CREAM, border=GOLDEN_SAND, bw=2.4):
    """Solid card with a solid left border. No shadow, no alpha, no fade."""
    c.setFillColor(fill)
    c.rect(x, y, width, height, stroke=0, fill=1)
    if border is not None:
        c.setFillColor(border)
        c.rect(x, y, bw, height, stroke=0, fill=1)


def ruled_lines(c, x, y, width, count, gap=10 * 2.8346, colour=SAND_STONE):
    """Fill-in lines at 10mm spacing. Returns the y below the last line."""
    for _ in range(count):
        rule(c, x, y, width, colour, 0.5)
        y -= gap
    return y + gap


def running_head(c, left, right):
    tracked(c, left, M, H - 34, "BodyM", 6.6, SAND_STONE, track=2.2)
    tw = sum(pdfmetrics.stringWidth(ch, "BodyM", 6.6) + 2.2 for ch in right) - 2.2
    tracked(c, right, W - M - tw, H - 34, "BodyM", 6.6, SAND_STONE, track=2.2)
    rule(c, M, H - 44, CW, IVORY_GLOW, 0.5)


def footer(c, text=None):
    rule(c, M, 50, CW, IVORY_GLOW, 0.5)
    tracked(c, text or C.FOOTER_BRAND, W / 2, 36, "BodyM", 6.4, SAND_STONE,
            track=2.4, centre=True)


# --------------------------------------------------------------------------- #
# PAGES
# --------------------------------------------------------------------------- #

def cover(c):
    page_bg(c)

    # THE BANNER IS THE SOURCE (amg-brand-boards). The wordmark already lives on
    # the banner, so no title text is overlaid on top of it. The cream fade at the
    # bottom of the image is baked into the raster by prepare_assets.py, which is
    # why there is no PDF shading and no soft mask anywhere in this file.
    band_h = W * 720.0 / 1280.0        # the banner's own 16:9, full bleed
    if os.path.exists(BANNER):
        c.drawImage(BANNER, 0, H - band_h, width=W, height=band_h,
                    preserveAspectRatio=False, mask=None)
    else:                              # fallback if the banner is missing
        c.setFillColor(DEEP_UMBER)
        c.rect(0, H - band_h, W, band_h, stroke=0, fill=1)
        c.setFont("Title", 68)
        c.setFillColor(PALE_OAT)
        c.drawCentredString(W / 2, H - band_h / 2, C.TITLE.upper())

    # Stepped solid bars under the banner. Four flat colours, never a gradient.
    bar_y = H - band_h - 3
    seg = W / 4.0
    for i, col in enumerate([WARM_CLAY, AMBER_EMBER, GOLDEN_SAND, IVORY_GLOW]):
        c.setFillColor(col)
        c.rect(i * seg, bar_y, seg, 6, stroke=0, fill=1)

    y = H - band_h - 58
    tracked(c, C.EYEBROW, W / 2, y, "BodyM", 8.4, WARM_CLAY, track=3.6, centre=True)
    y -= 44

    c.setFont("TitleI", 19)
    c.setFillColor(DEEP_UMBER)
    for line in simpleSplit(C.SUBTITLE, "TitleI", 19, CW - 60):
        c.drawCentredString(W / 2, y, line)
        y -= 27

    y -= 12
    rule(c, W / 2 - 46, y, 92, GOLDEN_SAND, 1.2)
    y -= 30

    c.setFont("Body", 11.8)
    c.setFillColor(ESPRESSO)
    for line in simpleSplit(C.COVER_STANDFIRST, "Body", 11.8, CW - 110):
        c.drawCentredString(W / 2, y, line)
        y -= 19

    # the numbered strip. the whole guide, at a glance. anchored low.
    y = 214.0
    rule(c, M + 30, y + 22, CW - 60, IVORY_GLOW, 0.6)
    cols, colw = 8, (CW - 60) / 8.0
    for i in range(16):
        r, k = divmod(i, cols)
        cx = M + 30 + k * colw + colw / 2.0
        cy = y - r * 26
        tracked(c, f"{i + 1:02d}", cx, cy, "BodyM", 8.2,
                GOLDEN_SAND if r == 0 else WARM_CLAY, track=1.4, centre=True)
    y -= 26 + 22
    rule(c, M + 30, y, CW - 60, IVORY_GLOW, 0.6)

    tracked(c, C.CLOSING_LINE, W / 2, 92, "BodyM", 7.8, WARM_CLAY,
            track=3.6, centre=True)
    tracked(c, C.FOOTER_BRAND, W / 2, 70, "BodyM", 6.4, SAND_STONE,
            track=2.4, centre=True)
    c.showPage()


def intro(c):
    page_bg(c)
    running_head(c, C.TITLE.upper(), "RECOGNISE")

    y = H - 100
    c.setFont("Title", 32)
    c.setFillColor(DEEP_UMBER)
    c.drawString(M, y, C.INTRO_TITLE)
    y -= 22
    rule(c, M, y, 70, GOLDEN_SAND, 1.2)
    y -= 34

    for i, p in enumerate(C.INTRO):
        font, size, lead, col = "Body", 11.0, 17.5, ESPRESSO
        if i == 0:
            font, size, lead, col = "TitleI", 14.0, 21.0, DEEP_UMBER
        y = para(c, p, M, y, CW, font, size, lead, col)
        y -= 9

    footer(c)
    c.showPage()


def code_page(c, d):
    page_bg(c)
    running_head(c, C.TITLE.upper(), f"{d['n']} OF 16")

    TOP = H - 82
    BOTTOM = 216.0          # the name block owns everything below this

    LPAD = 18.0
    LW = CW - 2 * LPAD - 8

    # --- pass one: measure -------------------------------------------------
    h_num = 34.0
    h_moment = para_h(d["moment"], CW - 10, "TitleI", 18.0, 27.0)
    h_rule = 1.0
    h_disg = 18.0 + para_h(d["disguise"], CW, "BodyR", 11.8, 19.0)
    h_truth = 18.0 + para_h(d["truth"], CW, "Body", 11.6, 19.0)
    h_loop = para_h(d["loop"], LW, "Body", 10.6, 17.0) + LPAD * 2 + 18
    h_note = para_h(d["note"], CW, "TitleI", 11.4, 17.5) if d.get("note") else 0.0

    MIN = [16.0, 22.0, 26.0, 20.0, 24.0]        # gaps after num, moment, rule, disg, truth
    if h_note:
        MIN.append(20.0)                         # gap after loop, before note
    natural = h_num + h_moment + h_rule + h_disg + h_truth + h_loop + h_note + sum(MIN)
    slack = max(0.0, (TOP - BOTTOM) - natural)
    share = slack / len(MIN)
    G = [g + share for g in MIN]

    # --- pass two: draw ----------------------------------------------------
    y = TOP

    c.setFont("Title", 46)
    c.setFillColor(GOLDEN_SAND)
    c.drawString(M, y - 34, d["n"])
    y -= h_num + G[0]

    # the moment. the entry. never the label.
    y = para(c, d["moment"], M, y, CW - 10, "TitleI", 18.0, 27.0, DEEP_UMBER)
    y -= G[1]

    rule(c, M, y, CW, IVORY_GLOW, 0.6)
    y -= G[2]

    label(c, "YOU HAVE BEEN CALLING IT", M, y, SAND_STONE, 7.2)
    y -= 18
    y = para(c, d["disguise"], M, y, CW, "BodyR", 11.8, 19.0, WARM_CLAY)
    y -= G[3]

    label(c, "WHAT IT ACTUALLY IS", M, y, SAND_STONE, 7.2)
    y -= 18
    y = para(c, d["truth"], M, y, CW, "Body", 11.6, 19.0, ESPRESSO)
    y -= G[4]

    # the loop, in a solid card
    card(c, M, y - h_loop, CW, h_loop)
    label(c, "THE LOOP", M + LPAD + 8, y - LPAD - 2, AMBER_EMBER, 7.0)
    para(c, d["loop"], M + LPAD + 8, y - LPAD - 22, LW, "Body", 10.6, 17.0, ESPRESSO)
    y -= h_loop

    # optional lived-proof note
    if h_note:
        y -= G[5]
        y = para(c, d["note"], M, y, CW, "TitleI", 11.4, 17.5, WARM_CLAY)

    # the name. the arrival. bottom of the page, always.
    name_y = 152
    rule(c, M, name_y + 30, CW, IVORY_GLOW, 0.6)
    tracked(c, "AND THIS IS WHAT IT IS CALLED", W / 2, name_y + 14, "BodyM", 6.6,
            SAND_STONE, track=2.4, centre=True)
    tracked(c, d["name"], W / 2, name_y - 12, "BodySB", 15.0, DEEP_UMBER,
            track=3.4, centre=True)

    # one question
    qpad = 14.0
    qh = para_h(d["question"], CW - 2 * qpad - 8, "TitleI", 11.2, 17.0)
    qbox = qh + qpad * 2
    card(c, M, 66, CW, qbox, fill=OAT_CREAM, border=AMBER_EMBER, bw=2.0)
    para(c, d["question"], M + qpad + 8, 66 + qbox - qpad - 3,
         CW - 2 * qpad - 8, "TitleI", 11.2, 17.0, DEEP_UMBER)

    footer(c)
    c.showPage()


def scan(c):
    """
    The scan, fillable.

    Sixteen checkboxes, three text lines, a live counter and six cluster rows that
    light up on their own. The interactivity is a real AcroForm, so the boxes tick
    and the lines type in every reader. The automatic cluster highlighting runs on
    a calculate action, which Adobe Acrobat honours and lighter viewers ignore, so
    the page also carries a link to the live web version where it always moves.
    """
    page_bg(c)
    running_head(c, C.TITLE.upper(), "THE SCAN")

    af = c.acroForm
    y = H - 92

    c.setFont("Title", 30)
    c.setFillColor(DEEP_UMBER)
    c.drawString(M, y, C.SCAN_TITLE)
    y -= 21
    rule(c, M, y, 70, GOLDEN_SAND, 1.2)
    y -= 28

    for p in C.SCAN_INTRO:
        y = para(c, p, M, y, CW, "Body", 10.8, 17.0, ESPRESSO)
    y -= 14

    # --- the sixteen ticks. real checkboxes. -------------------------------
    box = 23.0
    gap = (CW - 8 * box) / 7.0
    for row in range(2):
        by = y - row * 44
        for col in range(8):
            n = row * 8 + col + 1
            bx = M + col * (box + gap)
            af.checkbox(
                name=f"tick{n:02d}", x=bx, y=by - box, size=box,
                checked=False, buttonStyle="check", shape="square",
                fillColor=OAT_CREAM, borderColor=SAND_STONE, textColor=DEEP_UMBER,
                borderWidth=0.8, forceBorder=True,
                tooltip=f"{n:02d} {C.CODES[n - 1]['name'].title()}",
                annotationFlags="print",
            )
            tracked(c, f"{n:02d}", bx + box / 2, by - box - 11, "BodyM", 6.6,
                    WARM_CLAY, track=1.2, centre=True)
    y -= 44 + box + 54

    # --- the counter -------------------------------------------------------
    label(c, "TICKED", M, y + 6, SAND_STONE, 7.2)
    af.textfield(
        name="count", value="0", x=M + 58, y=y - 3, width=40, height=24,
        fontName="Helvetica", fontSize=12,
        fillColor=OAT_CREAM, borderColor=GOLDEN_SAND, textColor=DEEP_UMBER,
        borderWidth=1.0, fieldFlags="readOnly", annotationFlags="print",
        tooltip="Your count, updated as you tick",
    )
    para(c, C.SCAN_COUNT, M + 116, y + 15, CW - 116, "TitleI", 10.6, 16.0, WARM_CLAY)
    y -= 50

    # --- three names, typeable --------------------------------------------
    for p in C.SCAN_MID:
        y = para(c, p, M, y, CW, "Body", 10.8, 17.0, ESPRESSO)
    y -= 10

    for i in range(3):
        ly = y - i * 30
        af.textfield(
            name=f"name{i + 1}", value="", x=M, y=ly - 5, width=CW, height=23,
            fontName="Helvetica", fontSize=11.5,
            fillColor=PALE_OAT, borderColor=PALE_OAT, textColor=DEEP_UMBER,
            borderWidth=0, maxlen=60, annotationFlags="print",
            tooltip=f"Name {i + 1}",
        )
        rule(c, M, ly - 7, CW, SAND_STONE, 0.6)
    y -= 3 * 30 + 22

    # --- the clusters. these light up on their own. ------------------------
    label(c, "THE CLUSTERS", M, y, SAND_STONE, 7.2)
    tracked(c, "FULL CLUSTER LIGHTS UP", M + CW - 118, y, "BodyM", 6.4,
            AMBER_EMBER, track=1.8)
    y -= 24
    colw = CW / 2.0
    rowh = 31.0
    for i, (nm, nums) in enumerate(C.CLUSTERS):
        cx = M + (i % 2) * colw
        cy = y - (i // 2) * rowh
        # the marker. an empty read-only field whose fill the script flips.
        af.textfield(
            name=f"mark{i}", value="", x=cx, y=cy - 2, width=9, height=9,
            fontName="Helvetica", fontSize=6,
            fillColor=IVORY_GLOW, borderColor=IVORY_GLOW, textColor=IVORY_GLOW,
            borderWidth=0, fieldFlags="readOnly", annotationFlags="print",
        )
        tracked(c, nm, cx + 18, cy, "BodySB", 8.8, DEEP_UMBER, track=2.0)
        c.setFont("Body", 9.6)
        c.setFillColor(AMBER_EMBER)
        c.drawString(cx + 140, cy, nums)
        # the underline. same trick, wider and thinner.
        af.textfield(
            name=f"bar{i}", value="", x=cx, y=cy - 12, width=colw - 26, height=2.5,
            fontName="Helvetica", fontSize=4,
            fillColor=IVORY_GLOW, borderColor=IVORY_GLOW, textColor=IVORY_GLOW,
            borderWidth=0, fieldFlags="readOnly", annotationFlags="print",
        )
    y -= 3 * rowh + 16

    pad = 16.0
    ch_ = para_h(C.SCAN_CLOSE, CW - 2 * pad - 8, "TitleI", 12.0, 18.5)
    bh = ch_ + pad * 2
    card(c, M, y - bh, CW, bh)
    para(c, C.SCAN_CLOSE, M + pad + 8, y - pad - 4, CW - 2 * pad - 8,
         "TitleI", 12.0, 18.5, DEEP_UMBER)
    y -= bh + 20

    # --- the fillable note and the live link ------------------------------
    y = para(c, C.SCAN_FILLABLE_NOTE, M, y, CW - 150, "Body", 8.4, 12.8, SAND_STONE)
    lx, ly = M + CW - 142, y + 30
    c.setFillColor(DEEP_UMBER)
    c.rect(lx, ly, 142, 26, stroke=0, fill=1)
    c.setFillColor(GOLDEN_SAND)
    c.rect(lx, ly, 142, 2, stroke=0, fill=1)
    tracked(c, C.SCAN_LIVE_LINK, lx + 71, ly + 10, "BodySB", 7.4, PALE_OAT,
            track=2.0, centre=True)
    c.linkURL(C.SCAN_URL, (lx, ly, lx + 142, ly + 26), relative=0, thickness=0)

    footer(c)
    c.showPage()


def cta(c):
    page_bg(c)
    running_head(c, C.TITLE.upper(), "WHAT NOW")

    y = H - 100
    c.setFont("Title", 32)
    c.setFillColor(DEEP_UMBER)
    c.drawString(M, y, C.CTA_TITLE)
    y -= 22
    rule(c, M, y, 70, GOLDEN_SAND, 1.2)
    y -= 34

    for i, p in enumerate(C.CTA_BODY):
        if i == 0:
            y = para(c, p, M, y, CW, "TitleI", 16.5, 25.0, DEEP_UMBER)
        else:
            y = para(c, p, M, y, CW, "Body", 11.6, 19.0, ESPRESSO)
        y -= 16

    y -= 26
    # solid button. no gradient, no shadow.
    btn_h = 52.0
    c.setFillColor(DEEP_UMBER)
    c.rect(M, y - btn_h, CW, btn_h, stroke=0, fill=1)
    c.setFillColor(GOLDEN_SAND)
    c.rect(M, y - btn_h, CW, 3, stroke=0, fill=1)
    tracked(c, C.CTA_BUTTON, W / 2, y - 31, "BodySB", 11.0, PALE_OAT,
            track=3.2, centre=True)
    # the whole button is the link, and so is the url beneath it
    c.linkURL(C.CTA_URL, (M, y - btn_h, M + CW, y), relative=0, thickness=0)
    y -= btn_h + 22
    lw = tracked(c, C.CTA_URL_LABEL, W / 2, y, "BodyM", 8.2, WARM_CLAY,
                 track=2.2, centre=True)
    c.linkURL(C.CTA_URL, (W / 2 - lw / 2, y - 5, W / 2 + lw / 2, y + 11),
              relative=0, thickness=0)
    y -= 54

    for i, p in enumerate(C.CTA_CLOSE):
        if i == len(C.CTA_CLOSE) - 1:
            y -= 12
            pad = 20.0
            hh = para_h(p, CW - 2 * pad - 8, "TitleI", 17.0, 26.0)
            bh = hh + pad * 2
            card(c, M, y - bh, CW, bh)
            para(c, p, M + pad + 8, y - pad - 5, CW - 2 * pad - 8,
                 "TitleI", 17.0, 26.0, DEEP_UMBER)
        else:
            y = para(c, p, M, y, CW, "Body", 11.6, 19.0, ESPRESSO)
            y -= 12

    # sign-off, anchored low so the page always closes the same way
    c.setFont("TitleI", 14.0)
    c.setFillColor(DEEP_UMBER)
    c.drawString(M, 150, C.SIGN_OFF)
    c.setFont("Body", 10.6)
    c.setFillColor(WARM_CLAY)
    c.drawString(M, 126, C.SIGN_OFF_PS)

    rule(c, M, 84, CW, IVORY_GLOW, 0.5)
    tracked(c, C.CLOSING_LINE, W / 2, 64, "BodyM", 8.0, GOLDEN_SAND,
            track=3.6, centre=True)
    tracked(c, C.FOOTER_BRAND, W / 2, 44, "BodyM", 6.4, SAND_STONE,
            track=2.4, centre=True)
    c.showPage()


# --------------------------------------------------------------------------- #

def build():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    c = canvas.Canvas(OUT, pagesize=A4)
    c.setTitle("Sixteen | Angie Marie Global")
    c.setAuthor("Angie Marie, Angie Marie Global")
    c.setSubject("Sixteen patterns nobody ever named for you")
    c.setKeywords("recognise, baseline, high performer, patterns, angie marie global")

    cover(c)
    intro(c)
    for d in C.CODES:
        code_page(c, d)
    scan(c)
    cta(c)

    c.save()
    print(f"built {OUT}")
    print(f"pages: {2 + len(C.CODES) + 2}")

    # attach the interactive layer to the scan page
    import add_scan_script
    add_scan_script.main()


if __name__ == "__main__":
    build()
