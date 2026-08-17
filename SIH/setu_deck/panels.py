"""Content panels for the SETU SIH 2026 idea presentation.

Deliberately plain and hand-typed looking: typed headings with a thin
rule instead of filled banner bands, three colours instead of seven,
ordinary bullets instead of pill clouds, and big text with very few
words on each slide.
"""

import os
from layout import *   # noqa: F401,F403

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(ASSETS, exist_ok=True)

PW, PH = 12.73, 5.62          # content panel for slides 2-6
DPI = 200


def out(name):
    return os.path.join(ASSETS, name)


# ======================================================================
#  SLIDE 2 - The problem, our solution, why we are different
# ======================================================================
def slide2():
    """Three horizontal bands, read top to bottom: the problem, the
    solution as a left-to-right flow, then the uniqueness grid. The
    uniqueness band is the biggest thing on the slide because that is the
    question a jury actually asks - each card names the number or the
    mechanism that nobody else in the field has."""
    p = Panel(PW, PH, DPI, bg=WHITE)

    # =============== BAND 1 - the problem ============================
    p.head(0.04, 0.00, PW - 0.08, "The problem we are solving", size=21,
           rule_frac=0.99)

    py = p.text(0.07, 0.48,
                "Indian cities have no automated, real-time way to find and "
                "verify road defects. They rely on slow citizen complaints, "
                "unverified contractor repairs and costly survey vehicles "
                "that reach under 2% of the network.",
                size=13.6, color=INK, maxw=PW - 0.30, lh=1.24)

    # the numbers, kept but squeezed into one plain strip
    py += 0.06
    strip_h = 0.72
    p.rrect(0.02, py, PW - 0.04, strip_h, fc=RED_T, ec=RED, lw=1.4, r=0.05)

    facts = [("9,438", "pothole deaths, 2020-24"),
             ("+53%", "more than five years ago"),
             ("Rs 17,693", "to audit one pothole"),
             ("1-2", "checks a road gets a year")]
    fw = (PW - 0.60) / 4
    for i, (val, lab) in enumerate(facts):
        cx = 0.30 + i * fw + fw / 2
        vs = p.fit_size(val, 25, fw - 0.30, minsize=16, weight="bold")
        p.ax.text(cx, py + 0.28, val, size=vs, weight="bold", color=RED,
                  ha="center", va="center_baseline", zorder=6)
        p.text(cx, py + 0.42, lab, size=11.4, weight="bold", color=INK,
               ha="center", maxw=fw - 0.20, lh=1.20)
        if i:
            p.rect(0.30 + i * fw - 0.06, py + 0.10, 0.012, strip_h - 0.20,
                   LINE, z=3)

    # =============== BAND 2 - the solution, left to right ============
    ry = py + strip_h + 0.14
    hs2 = 20
    hb = p.head(0.04, ry, PW - 0.08, "Our solution", size=hs2,
                rule_frac=0.99)
    # the one-line "what it is" sits beside the heading, not under it
    p.raw_text(0.10 + p.text_w("Our solution", hs2, "bold") + 0.28, ry + 0.06,
               "gig-delivery phones (Zomato, Swiggy, Rapido) become a free, "
               "real-time road inspection network",
               size=12.6, weight="bold", color=INK_SOFT, va="top", z=6)

    steps = [(BLUE, "1", "Phones feel the bump",
              "100 Hz sensors, nothing for the rider to do"),
             (BLUE, "2", "Four phones must agree",
              "same 20 m stretch, four different devices"),
             (RED, "3", "Camera only when unsure",
              "one short blurred clip settles the doubt")]
    sgap, sh = 0.42, 0.74
    sw = (PW - 0.08 - sgap * (len(steps) - 1)) / len(steps)
    sy = hb + 0.08
    for i, (c, num, ttl, sub) in enumerate(steps):
        x = 0.04 + i * (sw + sgap)
        p.rrect(x, sy, sw, sh, fc=WHITE, ec=LINE, lw=1.1, r=0.05)
        p.circle(x + 0.36, sy + sh / 2, 0.195, c, z=4)
        p.ax.text(x + 0.36, sy + sh / 2 + 0.005, num, size=13.5,
                  weight="bold", color=WHITE, ha="center",
                  va="center_baseline", zorder=6)
        ts = p.fit_size(ttl, 14.4, sw - 0.78, minsize=11.5, weight="bold")
        p.raw_text(x + 0.66, sy + 0.14, ttl, size=ts, weight="bold",
                   color=INK, ha="left", va="top", z=6)
        ss = p.fit_size(sub, 10.8, sw - 0.78, minsize=8.8)
        p.raw_text(x + 0.66, sy + 0.14 + ts * 1.30 / 72.0, sub, size=ss,
                   color=MUTED, ha="left", va="top", z=6)
        if i < len(steps) - 1:
            p.arrow_right(x + sw + 0.09, sy + sh / 2, x + sw + sgap - 0.09,
                          color=MUTED, w=0.05, head=0.11)

    # =============== BAND 3 - the uniqueness grid ====================
    uy = sy + sh + 0.14
    ub = p.head(0.04, uy, PW - 0.08,
                "What makes it different - and what nobody else does",
                size=hs2, rule_frac=0.99)

    diffs = [
        (BLUE, "Zero new hardware: Rs 3, not Rs 17,693",
         "Rivals buy survey vans or bolt-on IoT kits. We ride phones "
         "already on the road."),
        (BLUE, "A cost-gated ladder, not one model",
         "Free sensors screen every metre, agreement kills false alarms, "
         "video confirms the last 5%."),
        (GREEN, "1 wrong flag in 9 becomes 1 in 250",
         "Four phones agreeing on one 20 m segment - maths, not costlier "
         "hardware, buys the accuracy."),
        (RED, "We train on the look-alikes",
         "A quarter of our dataset is speed breakers, manholes and tar "
         "patches - where models fail."),
        (GREEN, "A repair proves itself",
         "Fixed roads go quiet, and before/after evidence makes contractor "
         "payment auditable."),
        (RED, "Tuned for Indian two-wheelers",
         "Per-phone and per-vehicle calibration; severity weighted by who "
         "actually dies."),
    ]

    # pack the grid into whatever height is left, shrinking only the body
    # type until every card fits - the headline size never moves
    cols, gapx, gapy = 3, 0.16, 0.10
    cw = (PW - 0.08 - gapx * (cols - 1)) / cols
    top = ub + 0.08
    avail = PH - 0.04 - top
    dhs = 13.0
    head_h = dhs * 1.28 / 72.0
    for bs in (11.4, 11.0, 10.6, 10.2, 9.8, 9.4):
        line_h = bs * 1.24 / 72.0
        nl = [len(p.wrap(b, bs, cw - 0.46)) for _, _, b in diffs]
        rows_h = [0.075 + head_h + 0.03
                  + max(nl[r:r + cols]) * line_h + 0.085
                  for r in range(0, len(diffs), cols)]
        if sum(rows_h) + gapy * (len(rows_h) - 1) <= avail:
            break

    for i, (c, head_, body) in enumerate(diffs):
        r, col = divmod(i, cols)
        x = 0.04 + col * (cw + gapx)
        y = top + sum(rows_h[:r]) + gapy * r
        dh = rows_h[r]
        p.rrect(x, y, cw, dh, fc=CANVAS, ec=LINE, lw=1.0, r=0.05)
        p.rect(x, y, 0.055, dh, c, z=3)
        hsz = p.fit_size(head_, dhs, cw - 0.46, minsize=10.5, weight="bold")
        p.raw_text(x + 0.23, y + 0.075, head_, size=hsz, weight="bold",
                   color=INK, ha="left", va="top", z=6)
        p.text(x + 0.23, y + 0.075 + head_h + 0.03, body, size=bs,
               color=INK_SOFT, maxw=cw - 0.46, lh=1.24)

    return p.save(out("s2_solution.png"))


# ======================================================================
#  SLIDE 3 - Technical approach
# ======================================================================
def slide3():
    p = Panel(PW, PH, DPI, bg=WHITE)

    # ---------------- left: the flow, stacked in a narrow column -----
    ax0, aw = 0.02, 3.62
    p.head(ax0 + 0.02, 0.00, aw, "How the data moves", size=20,
           rule_frac=0.94)

    stages = [("1", "Phone feels a jolt", BLUE),
              ("2", "It reaches our server", BLUE),
              ("3", "Nearby readings grouped", BLUE),
              ("4", "Gig worker is asked to vote", RED),
              ("5", "A short clip is asked for", RED),
              ("6", "Confirmed or dropped", GREEN),
              ("7", "Dashboard and work order", GREEN)]
    y, ch, gap = 0.52, 0.56, 0.16
    for i, (num, title, c) in enumerate(stages):
        p.rrect(ax0, y, aw, ch, fc=WHITE, ec=c, lw=1.5, r=0.05)
        p.circle(ax0 + 0.32, y + ch / 2, 0.185, c, z=4)
        p.ax.text(ax0 + 0.32, y + ch / 2 + 0.005, num, size=13.0,
                  weight="bold", color=WHITE, ha="center",
                  va="center_baseline", zorder=6)
        ts = p.fit_size(title, 13.4, aw - 0.68, minsize=10.5, weight="bold")
        p.ax.text(ax0 + 0.58, y + ch / 2 + 0.005, title, size=ts,
                  weight="bold", color=INK, ha="left", va="center_baseline",
                  zorder=6)
        if i < len(stages) - 1:
            p.arrow_down(ax0 + aw / 2, y + ch + 0.015, y + ch + gap - 0.01,
                         color=MUTED, w=0.05, head=0.09)
        y += ch + gap

    # ---------------- right: the stack, named tool by tool -----------
    bx0 = 3.92
    bw = PW - bx0 - 0.02
    p.head(bx0, 0.00, bw, "What we are building it with", size=20,
           rule_frac=0.97)

    rows = [
        ("On the phone", BLUE,
         "React Native (Android and iOS), 100 Hz accelerometer and GPS, "
         "on-device 1D-CNN bump classifier (Keras), SQLite queue for "
         "offline trips"),
        ("Our server", BLUE,
         "Python (FastAPI), Celery workers on Redis, REST/JSON "
         "APIs, JWT auth, Pydantic validation"),
        ("Map and database", BLUE,
         "PostgreSQL 16 with PostGIS, OSRM for map-matching each reading "
         "to a real road, DBSCAN to group nearby hits, GeoJSON output"),
        ("The AI models", RED,
         "YOLOv11s (Ultralytics, PyTorch) on the clips, OpenCV frame "
         "handling, trained on RDD2022"),
        ("The dashboard", GREEN,
         "HTML, CSS, JavaScript, React, deck.gl and MapLibre GL for the "
         "live map, Chart.js for ward-level trends"),
        ("Running it", MUTED,
         "Docker + docker-compose, GitHub Actions, Nginx"),
    ]
    y = 0.56
    for i, (label, c, body) in enumerate(rows):
        nlines = len(p.wrap(body, 12.6, bw - 0.30))
        blk = 0.26 + nlines * 12.6 * 1.26 / 72.0
        p.rect(bx0, y - 0.03, 0.05, blk, c, z=3)
        p.raw_text(bx0 + 0.20, y, label, size=14.0, weight="bold", color=c,
                   ha="left", va="top", z=6)
        yy = p.text(bx0 + 0.20, y + 0.26, body, size=12.6, color=INK,
                    maxw=bw - 0.30, lh=1.26)
        y = yy + 0.15

    return p.save(out("s3_technical.png"))


# ======================================================================
#  SLIDE 4 - Why the math works, feasibility, risks
# ======================================================================
def slide4():
    p = Panel(PW, PH, DPI, bg=WHITE)

    # ---------------- why the math works ----------------------------
    ax0, aw = 0.02, 6.72
    p.head(ax0 + 0.02, 0.00, aw, "Why the math works", size=20,
           rule_frac=0.95)

    p.rrect(ax0, 0.50, aw, 1.05, fc=BLUE_T, ec=BLUE, lw=1.3, r=0.05)
    p.raw_text(ax0 + 0.22, 0.60, "Wu, Wang, Hu et al. - Sensors 20:5564 (2020)",
               size=13.6, weight="bold", color=INK, z=6)
    p.text(ax0 + 0.22, 0.92,
           "88.5% of one phone's flags are real. Their published counts also "
           "give 1.5% false flags per clean pass.",
           size=13.0, color=INK, maxw=aw - 0.44, lh=1.26)

    lines = [
        ("One phone on its own:", "1 flag in 9 is wrong."),
        ("We wait for 4 phones", "to flag the same 20 m."),
    ]
    y = 1.80
    for a, b in lines:
        p.rich(ax0 + 0.06, y, [(a + " ", "bold", INK), (b, "normal", INK)],
               size=14.0)
        y += 0.40

    p.rrect(ax0 + 0.06, y + 0.02, aw - 0.12, 0.66, fc=CANVAS, ec=LINE,
            lw=1.0, r=0.04)
    eq = "1 in 9      ->      1 in 250 once 4 phones agree"
    es = p.fit_size(eq, 15.5, aw - 0.40, minsize=11, weight="bold")
    p.ax.text(ax0 + aw / 2, y + 0.37, eq, size=es, weight="bold", color=RED,
              ha="center", va="center_baseline", zorder=6)
    y += 0.84

    p.rich(ax0 + 0.06, y,
           [("We credit each extra phone with 3x, ", "bold", INK),
            ("not the 50x the paper implies.", "normal", INK)], size=13.4)
    y += 0.44

    p.rrect(ax0, y, aw, 0.90, fc=GREEN_T, ec=GREEN, lw=1.3, r=0.05)
    p.text(ax0 + 0.22, y + 0.15,
           "So about 1 confirmed spot in 250 is wrong, and the camera check "
           "settles those.",
           size=13.6, weight="bold", color="#0F5C34", maxw=aw - 0.44,
           lh=1.28)

    # ---------------- is it doable ----------------------------------
    bx0 = 6.94
    bw = PW - bx0 - 0.02
    p.head(bx0, 0.00, bw, "Is it actually doable?", size=20, rule_frac=0.92)

    p.rrect(bx0, 0.46, bw, 0.58, fc=GREEN_T, ec=GREEN, lw=1.4, r=0.05)
    p.ax.text(bx0 + 0.28, 0.77, "YES", size=25, weight="bold", color=GREEN,
              ha="left", va="center_baseline", zorder=6)
    p.ax.text(bx0 + 1.24, 0.77,
              "- every piece already exists and is free",
              size=13.0, weight="bold", color=INK, ha="left",
              va="center_baseline", zorder=6)

    doable = [
        "Every piece is free and open source",
        "Runs on an ordinary Rs 8,000 Android phone",
        "One bus route or municipal fleet is enough to start",
        "Six of us: one app, one server, one dashboard",
    ]
    y = 1.14
    for d in doable:
        p.rect(bx0, y, bw, 0.42, CANVAS, z=2)
        p.circle(bx0 + 0.18, y + 0.21, 0.055, GREEN, z=4)
        ds = p.fit_size(d, 13.0, bw - 0.48, minsize=10.5, weight="normal")
        p.ax.text(bx0 + 0.34, y + 0.215, d, size=ds, color=INK,
                  ha="left", va="center_baseline", zorder=6)
        y += 0.47

    # ---------------- risks -----------------------------------------
    y += 0.10
    p.head(bx0, y, bw, "What could go wrong", size=20, rule_frac=0.88)
    y += 0.48

    risks = ["Phones kill background apps",
             "GPS drifts by 20-30 m",
             "Speed breakers look like potholes",
             "Video can catch faces"]
    for name in risks:
        p.rrect(bx0, y, bw, 0.44, fc=WHITE, ec=LINE, lw=1.0, r=0.04)
        p.rect(bx0, y, 0.05, 0.44, RED, z=3)
        p.ax.text(bx0 + 0.22, y + 0.23, name, size=13.4, weight="bold",
                  color=INK, ha="left", va="center_baseline", zorder=6)
        y += 0.49

    return p.save(out("s4_feasibility.png"))


# ======================================================================
#  SLIDE 5 - Impact and benefits
# ======================================================================
def slide5():
    p = Panel(PW, PH, DPI, bg=WHITE)

    ax0, aw = 0.02, 6.44
    p.head(ax0 + 0.02, 0.00, aw, "What changes on the ground", size=20,
           rule_frac=0.96)

    stats = [("6+", "DEATHS A DAY", "pothole crashes, MoRTH", RED, RED_T),
             ("Daily", "ROAD CHECK", "instead of once a year", BLUE, BLUE_T),
             ("100%", "REPAIRS CHECKED", "evidence before and after",
              GREEN, GREEN_T)]
    sw = (aw - 2 * 0.18) / 3
    sh = 1.30
    for i, (v, l, s, c, t) in enumerate(stats):
        p.stat(ax0 + i * (sw + 0.18), 0.50, sw, sh, v, l, s, c, t,
               vsize=30, lsize=12.2, ssize=10.6)

    y = 0.50 + sh + 0.28
    p.table(ax0, y, aw,
            ["Who", "Today", "With SETU"],
            [["Citizens", "no warning, nobody answerable",
              "safer roads, repairs on a clock"],
             ["Municipality", "costly audits, guesswork",
              "a ranked repair list, daily"],
             ["NHAI / PWD", "one survey pass a year",
              "every lane that gets driven"],
             ["Gig workers", "vehicle damage, back pain",
              "warnings ahead, no extra work"]],
            col_w=[0.21, 0.40, 0.39], hl_col=2, size=12.6, row_h=0.62)

    # ---------------- the money -------------------------------------
    bx0 = 6.70
    bw = PW - bx0 - 0.02
    p.head(bx0, 0.00, bw, "What it costs to confirm one pothole", size=20,
           rule_frac=0.94)

    bars = [("Survey vehicle or manual audit", 1.00, "Rs 17,693", RED),
            ("Citizen complaint app", 0.42, "cannot be verified", MUTED),
            ("SETU", 0.02, "Rs 3", GREEN)]
    bar_x = bx0 + 0.04
    bar_max = bw - 2.10
    yy = 0.58
    for label, frac, val, c in bars:
        p.ax.text(bar_x, yy, label, size=12.6, color=INK, ha="left",
                  va="top", zorder=6)
        p.rrect(bar_x, yy + 0.28, bar_max, 0.30, fc=CANVAS, r=0.03, z=2)
        p.rrect(bar_x, yy + 0.28, max(bar_max * frac, 0.06), 0.30, fc=c,
                r=0.03, z=3)
        p.ax.text(bar_x + bar_max + 0.14, yy + 0.44, val, size=13.0,
                  weight="bold", color=c, ha="left", va="center_baseline",
                  zorder=6)
        yy += 0.76

    p.rrect(bx0, yy + 0.06, bw, 0.92, fc=GREEN_T, ec=GREEN, lw=1.4, r=0.05)
    p.ax.text(bx0 + 0.26, yy + 0.56, "5,900x", size=32, weight="bold",
              color=GREEN, ha="left", va="center_baseline", zorder=6)
    p.text(bx0 + 2.06, yy + 0.20,
           "cheaper for the same kind of proof, because the camera only "
           "runs when the sensors are unsure.",
           size=12.4, weight="bold", color=INK, maxw=bw - 2.30, lh=1.26)

    yy += 1.14
    p.head(bx0, yy, bw, "Side benefits we did not plan for", size=17,
           rule_frac=0.86)
    p.bullets(bx0 + 0.04, yy + 0.46, bw - 0.10, [
        "Monsoon damage shows up in days",
        "Less fuel, fewer suspension repairs",
        "Proof of which contractor delivered",
    ], size=14.2, dot=BLUE, gap=0.10, color=INK)

    return p.save(out("s5_impact.png"))


if __name__ == "__main__":
    print(slide2())
    print(slide3())
    print(slide4())
    print(slide5())
