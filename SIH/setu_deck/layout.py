"""
Layout toolkit for the SETU SIH deck panels.

Everything is drawn in INCHES on a top-down coordinate system
(y = 0 at the top of the panel), so panel geometry maps 1:1 onto
PowerPoint inches. Text is measured with the real font renderer
before it is drawn, so nothing can ever overlap or overflow.

Two renderers share this one layout engine:

  * ``Panel``      - draws with matplotlib into a bitmap (legacy preview).
  * ``PptxPanel``  - see ``native.py``; emits real PowerPoint shapes and
                     real text so the exported PDF is fully selectable.

Every composite (band / stat / bullets / chips / group / table / ...)
only ever calls the primitives ``rrect``, ``rect``, ``circle``, ``poly``,
the arrow helpers and ``raw_text``. Subclasses override those primitives
and inherit all of the geometry unchanged.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle, FancyArrow

# ---------------------------------------------------------------- fonts
FONT_STACK = ["Segoe UI", "Calibri", "Tahoma", "DejaVu Sans"]
FONT_NAME = "Segoe UI"          # font the PPTX renderer asks for

matplotlib.rcParams["font.family"] = "sans-serif"
matplotlib.rcParams["font.sans-serif"] = list(FONT_STACK)
matplotlib.rcParams["axes.unicode_minus"] = False

# ---------------------------------------------------------------- palette
INK        = "#0B1B33"   # headline navy
INK_SOFT   = "#3C4C63"   # body grey-blue
MUTED      = "#6B7A90"
WHITE      = "#FFFFFF"
CANVAS     = "#F5F8FC"
LINE       = "#D4DEEA"

BLUE       = "#1565D8"
BLUE_T     = "#E8F1FE"
TEAL       = "#0E9594"
TEAL_T     = "#E3F6F5"
GREEN      = "#178A4C"
GREEN_T    = "#E6F6EC"
AMBER      = "#D98A00"
AMBER_T    = "#FFF5E1"
RED        = "#D93025"
RED_T      = "#FDECEA"
PURPLE     = "#6C3BD1"
PURPLE_T   = "#F0EAFE"
SAFFRON    = "#FF7A18"
SAFFRON_T  = "#FFF0E4"
NAVY       = "#12294B"

HILITE     = "#FFF3B0"   # highlighter yellow for key phrases


class Panel:
    """A drawing surface measured in inches, origin top-left."""

    def __init__(self, w, h, dpi=200, bg=WHITE):
        self.w, self.h, self.dpi = w, h, dpi
        self.fig = plt.figure(figsize=(w, h), dpi=dpi)
        self.fig.patch.set_facecolor(bg)
        self._ax = self.fig.add_axes([0, 0, 1, 1])
        self._ax.set_xlim(0, w)
        self._ax.set_ylim(h, 0)         # top-down
        self._ax.axis("off")
        self.ax = self._ax              # panels may draw text directly
        self.fig.canvas.draw()
        self._r = self.fig.canvas.get_renderer()

    # ------------------------------------------------------------ measure
    def text_w(self, s, size, weight="normal", style="normal"):
        t = self._ax.text(0, 0, s, size=size, weight=weight, style=style)
        bb = t.get_window_extent(renderer=self._r)
        t.remove()
        return bb.width / self.dpi

    def wrap(self, s, size, maxw, weight="normal", style="normal"):
        out, line = [], ""
        for word in s.split():
            trial = word if not line else line + " " + word
            if self.text_w(trial, size, weight, style) <= maxw or not line:
                line = trial
            else:
                out.append(line)
                line = word
        if line:
            out.append(line)
        return out

    def fit_size(self, s, size, maxw, minsize=5.5, weight="normal"):
        """Shrink a single-line string until it fits maxw."""
        while size > minsize and self.text_w(s, size, weight) > maxw:
            size -= 0.25
        return size

    # ------------------------------------------------------------ shapes
    def rrect(self, x, y, w, h, fc=WHITE, ec=None, lw=1.1, r=0.07,
              z=2, alpha=1.0, shadow=False):
        if shadow:
            self._ax.add_patch(FancyBboxPatch(
                (x + 0.035, y + 0.045), w, h,
                boxstyle=f"round,pad=0,rounding_size={r}",
                fc="#C9D4E2", ec="none", alpha=0.55, zorder=z - 1))
        p = FancyBboxPatch((x, y), w, h,
                           boxstyle=f"round,pad=0,rounding_size={r}",
                           fc=fc, ec=ec if ec else "none",
                           lw=lw if ec else 0, alpha=alpha, zorder=z)
        self._ax.add_patch(p)
        return p

    def rect(self, x, y, w, h, fc, alpha=1.0, z=2):
        self._ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="none",
                                     alpha=alpha, zorder=z))

    def circle(self, cx, cy, r, fc, ec=None, lw=1.2, z=3):
        self._ax.add_patch(Circle((cx, cy), r, fc=fc,
                                  ec=ec if ec else "none",
                                  lw=lw, zorder=z))

    def poly(self, pts, fc, ec=None, lw=1.0, z=2, alpha=1.0):
        self._ax.add_patch(Polygon(pts, closed=True, fc=fc,
                                   ec=ec if ec else "none", lw=lw,
                                   zorder=z, alpha=alpha))

    def arrow_down(self, cx, y0, y1, color=MUTED, w=0.055, head=0.13):
        self._ax.add_patch(FancyArrow(
            cx, y0, 0, (y1 - y0) - head, width=w, head_width=w * 3.6,
            head_length=head, length_includes_head=False,
            fc=color, ec="none", zorder=4))

    def arrow_right(self, x0, cy, x1, color=MUTED, w=0.05, head=0.12):
        self._ax.add_patch(FancyArrow(
            x0, cy, (x1 - x0) - head, 0, width=w, head_width=w * 3.6,
            head_length=head, length_includes_head=False,
            fc=color, ec="none", zorder=4))

    def curved_arrow(self, x0, y0, x1, y1, rad=0.25, color=MUTED, lw=1.5,
                     dashed=True, z=4, scale=11):
        """Feedback / return arrow drawn as an arc between two points."""
        from matplotlib.patches import FancyArrowPatch
        ap = FancyArrowPatch(
            (x0, y0), (x1, y1),
            connectionstyle=f"arc3,rad={rad}",
            arrowstyle="-|>", mutation_scale=scale, lw=lw,
            linestyle=(0, (4, 3)) if dashed else "solid",
            color=color, zorder=z, shrinkA=0, shrinkB=0,
            joinstyle="miter")
        self._ax.add_patch(ap)
        return ap

    # ------------------------------------------------------------ text
    def raw_text(self, x, y, s, size=9, weight="normal", color=INK_SOFT,
                 ha="left", va="top", style="normal", z=6):
        """Draw ONE unwrapped line. The single text primitive; every
        composite below goes through here so other renderers only have
        to override this method."""
        self._ax.text(x, y, s, size=size, weight=weight, color=color,
                      ha=ha, va=va, style=style, zorder=z)

    def text(self, x, y, s, size=9, weight="normal", color=INK_SOFT,
             ha="left", va="top", maxw=None, lh=1.28, style="normal", z=6):
        """Draw (wrapped) text. Returns y of the bottom of the block."""
        lines = self.wrap(s, size, maxw, weight, style) if maxw else [s]
        line_h = size * lh / 72.0
        yy = y
        for ln in lines:
            self.raw_text(x, yy, ln, size=size, weight=weight, color=color,
                          ha=ha, va=va, style=style, z=z)
            yy += line_h
        return yy

    def rich(self, x, y, parts, size=9, color=INK_SOFT, va="top", z=6):
        """Single line made of (text, weight, color) parts. Returns end x."""
        xx = x
        for txt, weight, col in parts:
            self.raw_text(xx, y, txt, size=size, weight=weight,
                          color=col if col else color, ha="left", va=va, z=z)
            xx += self.text_w(txt, size, weight)
        return xx

    def mark(self, x, y, s, size=9, weight="bold", color=INK,
             fc=HILITE, pad=0.045, z=5):
        """Highlighter-pen effect behind a short phrase."""
        w = self.text_w(s, size, weight)
        h = size * 1.32 / 72.0
        self.rrect(x - pad, y - 0.02, w + 2 * pad, h + 0.02,
                   fc=fc, r=0.03, z=z)
        self.raw_text(x, y, s, size=size, weight=weight, color=color,
                      ha="left", va="top", z=z + 1)
        return x + w + 2 * pad

    # ------------------------------------------------------------ combos
    def card(self, x, y, w, h, fc=WHITE, ec=LINE, accent=None,
             shadow=True, r=0.09):
        self.rrect(x, y, w, h, fc=fc, ec=ec, r=r, shadow=shadow)
        if accent:
            self.rrect(x, y, 0.085, h, fc=accent, r=0.04, z=3)
        return (x, y, w, h)

    def band(self, x, y, w, label, fc=NAVY, tc=WHITE, size=10.5,
             h=0.33, r=0.07, ha="center"):
        self.rrect(x, y, w, h, fc=fc, r=r, z=3)
        size = self.fit_size(label, size, w - 0.22, weight="bold")
        cx = x + w / 2 if ha == "center" else x + 0.12
        self.raw_text(cx, y + h / 2, label, size=size, weight="bold",
                      color=tc, ha=ha, va="center_baseline", z=5)
        return y + h

    def head(self, x, y, w, label, color=INK, size=15.5, rule=True,
             rule_frac=0.97, rule_color=None):
        """A plain typed heading with a thin rule under it.

        Deliberately unglamorous - this is what a person types into
        PowerPoint, as opposed to a filled navy band. ``rule_frac`` lets
        each section end its rule at a slightly different place so the
        page does not look machine-aligned.
        """
        size = self.fit_size(label, size, w - 0.06, minsize=9, weight="bold")
        self.raw_text(x, y, label, size=size, weight="bold", color=color,
                      ha="left", va="top", z=6)
        bottom = y + size * 1.30 / 72.0
        if rule:
            self.rect(x, bottom + 0.02, w * rule_frac, 0.018,
                      rule_color or LINE, z=3)
            bottom += 0.06
        return bottom

    def kv(self, x, y, w, head, body, hsize=12.0, bsize=10.8,
           hcolor=INK, bcolor=INK_SOFT, gap=0.03, lh=1.26):
        """Bold lead-in line, then one wrapped body block under it."""
        self.raw_text(x, y, head, size=hsize, weight="bold", color=hcolor,
                      ha="left", va="top", z=6)
        yy = y + hsize * 1.28 / 72.0 + gap
        return self.text(x, yy, body, size=bsize, color=bcolor, maxw=w,
                         lh=lh)

    def stat(self, x, y, w, h, value, label, sub, accent, tint,
             vsize=25, lsize=9, ssize=7.6):
        self.rrect(x, y, w, h, fc=tint, ec=accent, lw=1.2)
        vs = self.fit_size(value, vsize, w - 0.22, minsize=12, weight="bold")
        self.raw_text(x + w / 2, y + h * 0.40, value, size=vs, weight="bold",
                      color=accent, ha="center", va="center_baseline", z=6)
        ls = self.fit_size(label, lsize, w - 0.18, minsize=6, weight="bold")
        self.raw_text(x + w / 2, y + h * 0.62, label, size=ls, weight="bold",
                      color=INK, ha="center", va="center_baseline", z=6)
        if sub:
            self.text(x + w / 2, y + h * 0.70, sub, size=ssize, color=MUTED,
                      ha="center", maxw=w - 0.22, lh=1.22)

    def bullets(self, x, y, w, items, size=8.4, gap=0.055, dot=GREEN,
                color=INK_SOFT, lh=1.26, bold_head=True):
        """items: str  or  (head, rest)."""
        yy = y
        for it in items:
            self.circle(x + 0.055, yy + size * 0.55 / 72.0, 0.032, dot, z=5)
            tx = x + 0.16
            if isinstance(it, tuple):
                head, rest = it
                hw = self.text_w(head, size, "bold")
                if hw + 0.05 < w - 0.16:
                    self.raw_text(tx, yy, head, size=size, weight="bold",
                                  color=INK, ha="left", va="top", z=6)
                    first = self.wrap(rest, size, w - 0.16 - hw - 0.03, )
                    if first:
                        self.raw_text(tx + hw + 0.03, yy, first[0], size=size,
                                      color=color, ha="left", va="top", z=6)
                    rest_lines = " ".join(first[1:]) if len(first) > 1 else ""
                    yy += size * lh / 72.0
                    if rest_lines:
                        yy = self.text(tx, yy, rest_lines, size=size,
                                       color=color, maxw=w - 0.16, lh=lh)
                else:
                    yy = self.text(tx, yy, head + " " + rest, size=size,
                                   color=color, maxw=w - 0.16, lh=lh)
            else:
                yy = self.text(tx, yy, it, size=size, color=color,
                               maxw=w - 0.16, lh=lh)
            yy += gap
        return yy

    def chips(self, x, y, w, labels, size=7.8, fc=WHITE, ec=LINE,
              tc=INK_SOFT, h=0.235, gap=0.07, pad=0.10, lw=1.0):
        """Wrap a list of short labels into rounded pills. Returns bottom y."""
        cx, cy = x, y
        for lab in labels:
            tw = self.text_w(lab, size, "normal")
            cw = tw + 2 * pad
            if cx > x and cx + cw > x + w:
                cx = x
                cy += h + gap
            self.rrect(cx, cy, cw, h, fc=fc, ec=ec, lw=lw, r=h / 2, z=3)
            self.raw_text(cx + cw / 2, cy + h / 2 + 0.004, lab, size=size,
                          color=tc, ha="center", va="center_baseline", z=6)
            cx += cw + gap
        return cy + h

    def group(self, x, y, w, label, labels, accent, size=7.8, lsize=8.4,
              h=0.235, gap=0.07):
        """A labelled row of pills with a coloured rule on the left."""
        top = y
        self.raw_text(x + 0.14, y + 0.09, label, size=lsize, weight="bold",
                      color=accent, ha="left", va="top", z=6)
        lw_ = self.text_w(label, lsize, "bold")
        bottom = self.chips(x + 0.20 + lw_ + 0.10, y + 0.03,
                            w - 0.30 - lw_ - 0.10, labels, size=size,
                            ec=accent, h=h, gap=gap)
        bottom = max(bottom, y + 0.30)
        self.rrect(x, top + 0.02, 0.045, bottom - top - 0.04, fc=accent,
                   r=0.02, z=3)
        return bottom

    def table(self, x, y, w, headers, rows, col_w, hl_col=None,
              size=8.0, row_h=0.34, head_fc=NAVY, hl=TEAL):
        """Compact comparison table. col_w: fractions summing to 1."""
        widths = [w * c for c in col_w]
        self.rrect(x, y, w, row_h, fc=head_fc, r=0.06, z=3)
        cx = x
        for i, hd in enumerate(headers):
            s = self.fit_size(hd, size, widths[i] - 0.14, minsize=6,
                              weight="bold")
            self.raw_text(cx + widths[i] / 2, y + row_h / 2, hd, size=s,
                          weight="bold", color=WHITE, ha="center",
                          va="center_baseline", z=5)
            cx += widths[i]
        yy = y + row_h
        for ri, row in enumerate(rows):
            if ri % 2 == 0:
                self.rect(x, yy, w, row_h, CANVAS, z=2)
            cx = x
            for ci, cell in enumerate(row):
                is_hl = (hl_col is not None and ci == hl_col)
                col = hl if is_hl else INK_SOFT
                wt = "bold" if is_hl or ci == 0 else "normal"
                s = self.fit_size(str(cell), size, widths[ci] - 0.12,
                                  minsize=5.8, weight=wt)
                self.raw_text(cx + widths[ci] / 2, yy + row_h / 2, str(cell),
                              size=s, weight=wt, color=col, ha="center",
                              va="center_baseline", z=5)
                cx += widths[ci]
            self.rect(x, yy + row_h - 0.008, w, 0.008, LINE, z=3)
            yy += row_h
        if hl_col is not None:
            xh = x + sum(widths[:hl_col])
            self.rrect(xh, y, widths[hl_col], yy - y, fc="none", ec=hl,
                       lw=1.6, r=0.05, z=6, shadow=False)
        return yy

    # ------------------------------------------------------------ output
    def save(self, path):
        self.fig.savefig(path, dpi=self.dpi, facecolor=self.fig.get_facecolor())
        plt.close(self.fig)
        return path
