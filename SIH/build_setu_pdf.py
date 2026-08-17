"""
build_setu_pdf.py
Converts PROJECT.md (SETU project report) into a colour-coded, well-organised A4 PDF.

Design:
  - one accent colour per major section (band, table headers, code accents, thumb tab)
  - semantic colours: green = fix/verified, red = problem/risk, amber = caution
  - auto-generated table of contents with real page numbers (two-pass build)
  - PDF bookmarks/outline for every section and sub-section
  - ASCII diagrams rendered in Consolas at a size that fits the page
"""

import os
import re
import sys
import datetime

from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Flowable, CondPageBreak, KeepTogether,
)

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'PROJECT.md')
OUT = os.path.join(HERE, 'SETU_Project_Report.pdf')
SCRATCH = os.path.join(HERE, '_setu_pass1.pdf')

PAGE_W, PAGE_H = A4
M_L, M_R, M_T, M_B = 40, 38, 56, 46
AVAIL_W = PAGE_W - M_L - M_R

# --------------------------------------------------------------------------
# fonts
# --------------------------------------------------------------------------
WINF = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts')


def _reg(name, filename):
    path = os.path.join(WINF, filename)
    if not os.path.exists(path):
        return False
    pdfmetrics.registerFont(TTFont(name, path))
    return True


FONTS_OK = all([
    _reg('Body', 'arial.ttf'), _reg('Body-B', 'arialbd.ttf'),
    _reg('Body-I', 'ariali.ttf'), _reg('Body-BI', 'arialbi.ttf'),
    _reg('Mono', 'consola.ttf'), _reg('Mono-B', 'consolab.ttf'),
])
if not FONTS_OK:
    sys.exit('Required Windows fonts (Arial / Consolas) not found.')
pdfmetrics.registerFontFamily('Body', normal='Body', bold='Body-B',
                              italic='Body-I', boldItalic='Body-BI')
pdfmetrics.registerFontFamily('Mono', normal='Mono', bold='Mono-B',
                              italic='Mono', boldItalic='Mono-B')

# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------
INK = HexColor('#111827')
INK_SOFT = HexColor('#374151')
MUTED = HexColor('#6B7280')
LINE = HexColor('#D6DCE5')
ZEBRA = HexColor('#F5F8FB')
NAVY = HexColor('#0B1B33')

GREEN = HexColor('#15803D')
RED = HexColor('#B91C1C')
AMBER = HexColor('#B45309')
BLUE = HexColor('#1D4ED8')
GOLD = HexColor('#A16207')
SILVER = HexColor('#64748B')
BRONZE = HexColor('#92400E')
GREY = HexColor('#6B7280')

SECTION_COLORS = {
    'TOC': HexColor('#0F172A'),
    1: HexColor('#1E5AA8'), 2: HexColor('#C1121F'), 3: HexColor('#D97706'),
    4: HexColor('#0F766E'), 5: HexColor('#5B21B6'), 6: HexColor('#BE185D'),
    7: HexColor('#15803D'), 8: HexColor('#B91C1C'), 9: HexColor('#A16207'),
    10: HexColor('#0E7490'), 11: HexColor('#1D4ED8'), 12: HexColor('#6D28D9'),
    13: HexColor('#7C3AED'), 14: HexColor('#047857'), 15: HexColor('#334155'),
    16: HexColor('#0369A1'), 17: HexColor('#065F46'), 18: HexColor('#C2410C'),
    19: HexColor('#4338CA'), 20: HexColor('#0D9488'), 21: HexColor('#166534'),
    22: HexColor('#92400E'), 23: HexColor('#9F1239'), 24: HexColor('#6B21A8'),
    25: HexColor('#475569'),
    'APPENDIX': HexColor('#1E3A8A'),
}


def tint(color, factor):
    """Blend a colour towards white. factor 0 = white, 1 = colour."""
    r = 1 - (1 - color.red) * factor
    g = 1 - (1 - color.green) * factor
    b = 1 - (1 - color.blue) * factor
    return colors.Color(r, g, b)


# --------------------------------------------------------------------------
# character sanitising
# --------------------------------------------------------------------------
# Marks that carry meaning -> coloured text badges (prose / tables).
BADGES = {
    '\u2705': (GREEN, 'OK'),        # white heavy check
    '\u274c': (RED, 'NO'),          # cross mark
    '\u26a0': (AMBER, '!'),         # warning sign
    '\U0001f6a8': (RED, '!!'),      # police light
    '\U0001f534': (HexColor('#DC2626'), 'MUST'),   # red circle
    '\U0001f7e1': (HexColor('#B45309'), 'REC'),    # yellow circle
    '\U0001f7e2': (HexColor('#15803D'), 'OPT'),    # green circle
    '\u26ab': (HexColor('#334155'), 'v2'),         # black circle
    '\U0001f947': (GOLD, '#1'), '\U0001f948': (SILVER, '#2'),
    '\U0001f949': (BRONZE, '#3'),
    '\U0001f3c6': (GOLD, 'BEST'),
    '\U0001f3af': (BLUE, 'ADOPT'),
    '\U0001f914': (GREY, '?'),
    '\u2b50': (GOLD, '*'),
}
# Characters Arial/Consolas lack -> visually close substitutes.
CHAR_FIX = {
    '\ufe0f': '', '\u200b': '', '\u2028': ' ',
    '\u279c': '\u2192', '\u2715': '\u00d7', '\u2717': '\u00d7',
    '\u221d': '~', '\u25d0': '\u25cf', '\u2b21': '\u25cb',
    '\u1d62': 'i', '\u017d': 'Z', '\u25be': '\u25bc',
}
# Inside ASCII diagrams every replacement must be exactly ONE character
# so that column alignment survives.
CODE_FIX = dict(CHAR_FIX)
CODE_FIX.update({
    '\u2705': '+', '\u274c': 'x', '\u26a0': '!', '\U0001f6a8': '!',
    '\u2b50': '*', '\U0001f534': 'o', '\U0001f7e1': 'o', '\U0001f7e2': 'o',
    '\u26ab': 'o', '\U0001f3af': '>', '\U0001f914': '?',
    '\U0001f947': '1', '\U0001f948': '2', '\U0001f949': '3',
    '\U0001f3c6': '*',
})


def fix_code(text):
    return ''.join(CODE_FIX.get(ch, ch) for ch in text)


def strip_marks(text):
    """Plain-text version used for width estimation and TOC titles."""
    out = []
    for ch in text:
        if ch in BADGES:
            out.append(BADGES[ch][1])
        elif ch in CHAR_FIX:
            out.append(CHAR_FIX[ch])
        else:
            out.append(ch)
    return ''.join(out)


def plain(text):
    """Markdown/markup -> clean text for canvas drawing and PDF bookmarks."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = text.replace('`', '').replace('**', '').replace('*', '')
    text = (text.replace('&amp;', '&').replace('&lt;', '<')
                .replace('&gt;', '>').replace('&mdash;', '\u2014')
                .replace('&nbsp;', ' '))
    text = strip_marks(text)
    return re.sub(r'\s+', ' ', text).strip()


# --------------------------------------------------------------------------
# inline markdown -> reportlab markup
# --------------------------------------------------------------------------
CODE_COLOR = '#9D174D'
LINK_COLOR = '#1D4ED8'


def _esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def inline(text, mono_size=None):
    """Convert inline markdown to reportlab paragraph markup."""
    text = text.replace('\\|', '\u2502')
    codes, links = [], []

    def stash_code(m):
        codes.append(m.group(1))
        return '\x01%d\x01' % (len(codes) - 1)

    text = re.sub(r'`([^`]+)`', stash_code, text)

    def stash_link(m):
        links.append((m.group(1), m.group(2)))
        return '\x02%d\x02' % (len(links) - 1)

    text = re.sub(r'\[([^\]]*)\]\((https?://[^)\s]+|#[^)\s]*)\)', stash_link, text)

    def stash_bare(m):
        url = m.group(0)
        trail = ''
        while url and url[-1] in '.,;:)':
            trail = url[-1] + trail
            url = url[:-1]
        links.append((url, url))
        return '\x02%d\x02%s' % (len(links) - 1, trail)

    text = re.sub(r'https?://[^\s<>\[\]"\x01\x02]+', stash_bare, text)
    text = _esc(text)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<i>\1</i>', text)

    def put_code(m):
        body = _esc(codes[int(m.group(1))])
        size = ' size="%.1f"' % mono_size if mono_size else ''
        return '<font face="Mono" color="%s"%s>%s</font>' % (CODE_COLOR, size, body)

    text = re.sub('\x01(\\d+)\x01', put_code, text)

    def put_link(m):
        label, href = links[int(m.group(1))]
        label = _esc(label)
        if href.startswith('#'):
            return '<b>%s</b>' % label
        return '<a href="%s" color="%s">%s</a>' % (_esc(href), LINK_COLOR, label)

    text = re.sub('\x02(\\d+)\x02', put_link, text)

    for ch, (col, label) in BADGES.items():
        if ch in text:
            text = text.replace(
                ch, '<font color="%s"><b>%s</b></font>' % (col.hexval().replace('0x', '#'), label))
    for ch, rep in CHAR_FIX.items():
        if ch in text:
            text = text.replace(ch, rep)
    text = text.replace('\u2502', '|')
    return text


# --------------------------------------------------------------------------
# styles
# --------------------------------------------------------------------------
S_BODY = ParagraphStyle('body', fontName='Body', fontSize=9, leading=12.6,
                        textColor=INK_SOFT, spaceAfter=5, alignment=TA_LEFT,
                        splitLongWords=1)
S_LEAD = ParagraphStyle('lead', parent=S_BODY, fontSize=9.6, leading=13.4,
                        textColor=INK)
S_BULLET = ParagraphStyle('bullet', parent=S_BODY, leftIndent=14,
                          bulletIndent=3, spaceAfter=2.6)
S_BULLET2 = ParagraphStyle('bullet2', parent=S_BULLET, leftIndent=28,
                           bulletIndent=17, fontSize=8.6, leading=11.8)
S_NUM = ParagraphStyle('num', parent=S_BODY, leftIndent=19, firstLineIndent=-19,
                       spaceAfter=3.2)
S_TH = ParagraphStyle('th', fontName='Body-B', fontSize=7.6, leading=9.6,
                      textColor=colors.white, splitLongWords=1)
S_TD = ParagraphStyle('td', fontName='Body', fontSize=7.6, leading=9.8,
                      textColor=INK_SOFT, splitLongWords=1)
S_QUOTE = ParagraphStyle('quote', fontName='Body-I', fontSize=9.4, leading=13.4,
                         textColor=INK, splitLongWords=1)
S_CALL = ParagraphStyle('call', parent=S_BODY, fontSize=9, leading=12.6,
                        textColor=INK)
S_H3 = ParagraphStyle('h3', fontName='Body-B', fontSize=11, leading=14,
                      textColor=INK, spaceAfter=0)
S_H4 = ParagraphStyle('h4', fontName='Body-B', fontSize=9.4, leading=12.4,
                      textColor=INK, spaceBefore=4, spaceAfter=2)
S_TOC = ParagraphStyle('toc', fontName='Body', fontSize=8.4, leading=10.8,
                       textColor=INK_SOFT)
S_TOCB = ParagraphStyle('tocb', parent=S_TOC, fontName='Body-B', textColor=INK)

_BULLET_CACHE = {}


def bullet_styles(color):
    """Bullet styles whose marker takes the current section colour."""
    key = color.hexval()
    if key not in _BULLET_CACHE:
        _BULLET_CACHE[key] = (
            ParagraphStyle('bl1_' + key, parent=S_BULLET, bulletColor=color,
                           bulletFontSize=8.5),
            ParagraphStyle('bl2_' + key, parent=S_BULLET2, bulletColor=color,
                           bulletFontSize=7.5),
        )
    return _BULLET_CACHE[key]


# --------------------------------------------------------------------------
# custom flowables
# --------------------------------------------------------------------------
PAGE_SECTION = {}     # page number -> section key
ANCHOR_PAGES = {}     # anchor key   -> page number
OUTLINE_ITEMS = []    # (page, key, title, level) in document order
OUTLINE_SEEN = set()


def note_outline(page, key, title, level):
    if key in OUTLINE_SEEN:
        return
    OUTLINE_SEEN.add(key)
    OUTLINE_ITEMS.append((page, key, title, level))


class SectionBand(Flowable):
    """Full-width coloured banner that opens a major section."""

    def __init__(self, key, number, title, color, kicker=None):
        Flowable.__init__(self)
        self.key, self.number, self.title, self.color = key, number, title, color
        self.kicker = kicker
        self.pad = 9
        self._title_lines = None

    def _lines(self, width):
        avail = width - self.pad * 2 - (44 if self.number else 0)
        words, lines, cur = self.title.split(), [], ''
        for w in words:
            probe = (cur + ' ' + w).strip()
            if pdfmetrics.stringWidth(probe, 'Body-B', 15) <= avail or not cur:
                cur = probe
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
        return lines

    def wrap(self, aw, ah):
        self.width = aw
        self._title_lines = self._lines(aw)
        self.height = self.pad * 2 + 19 * len(self._title_lines) + \
            (11 if self.kicker else 0)
        return aw, self.height + 10

    def draw(self):
        c = self.canv
        h = self.height
        page = c.getPageNumber()
        PAGE_SECTION.setdefault(page, self.key)
        ANCHOR_PAGES[self.key] = page
        label = ('%s. %s' % (self.number, self.title)) if self.number else self.title
        note_outline(page, 'bm_%s' % self.key, plain(label)[:110], 0)
        c.saveState()
        c.setFillColor(self.color)
        c.roundRect(0, 10, self.width, h, 4, fill=1, stroke=0)
        c.setFillColor(tint(self.color, 0.35))
        c.roundRect(0, 10, 5, h, 2, fill=1, stroke=0)
        x = self.pad
        if self.number:
            c.setFillColor(colors.Color(1, 1, 1, 0.18))
            c.roundRect(self.pad, 10 + h / 2 - 12, 36, 24, 3, fill=1, stroke=0)
            c.setFillColor(colors.white)
            c.setFont('Body-B', 14)
            c.drawCentredString(self.pad + 18, 10 + h / 2 - 5, str(self.number))
            x = self.pad + 44
        y = 10 + h - self.pad - 14
        if self.kicker:
            c.setFillColor(colors.Color(1, 1, 1, 0.75))
            c.setFont('Body', 7.6)
            c.drawString(x, 10 + h - self.pad - 8, self.kicker.upper())
            y -= 11
        c.setFillColor(colors.white)
        c.setFont('Body-B', 15)
        for ln in self._title_lines:
            c.drawString(x, y, ln)
            y -= 19
        c.restoreState()


class SubHead(Flowable):
    """Coloured sub-section heading with a rule underneath."""

    def __init__(self, text, color, level=3, anchor=None, outline=True):
        Flowable.__init__(self)
        self.color = color
        self.level = level
        self.anchor = anchor
        self.outline = outline
        size = 11.2 if level == 3 else 9.6
        self.size = size
        self.para = Paragraph(
            '<font color="%s">%s</font>' % (color.hexval().replace('0x', '#'), text),
            ParagraphStyle('sh', fontName='Body-B', fontSize=size,
                           leading=size * 1.28, textColor=color))
        self.plain = text

    def wrap(self, aw, ah):
        self.width = aw
        w, h = self.para.wrap(aw - 9, ah)
        self.height = h + 7
        return aw, self.height + (7 if self.level == 3 else 4)

    def draw(self):
        c = self.canv
        top = self.height
        c.saveState()
        c.setFillColor(self.color)
        c.rect(0, 6, 3.2, top - 6, fill=1, stroke=0)
        self.para.drawOn(c, 9, 7)
        if self.level == 3:
            c.setStrokeColor(tint(self.color, 0.35))
            c.setLineWidth(0.7)
            c.line(0, 2.5, self.width, 2.5)
        c.restoreState()
        if self.anchor and self.outline:
            note_outline(c.getPageNumber(), 'bm_%s' % self.anchor,
                         plain(self.plain)[:110], 1)


class CodeBlock(Flowable):
    """Monospaced diagram / code block with tinted background; splits on lines."""

    def __init__(self, lines, color, size=None, first=True):
        Flowable.__init__(self)
        self.lines = lines
        self.color = color
        self.pad = 7
        self.gutter = 9
        self.size = size
        self.first = first

    def _fit(self, aw):
        if self.size:
            return self.size
        longest = max((pdfmetrics.stringWidth(l, 'Mono', 10) for l in self.lines),
                      default=1)
        usable = aw - self.pad * 2 - self.gutter - 2
        size = 10.0 * usable / max(longest, 1)
        return max(4.7, min(8.1, size))

    def wrap(self, aw, ah):
        self.width = aw
        self.size = self._fit(aw)
        self.leading = self.size * 1.16
        self.height = self.pad * 2 + self.leading * len(self.lines)
        return aw, self.height + 8

    def split(self, aw, ah):
        self.wrap(aw, ah)
        if ah >= self.height + 8:
            return [self]
        n = int((ah - self.pad * 2 - 8) // self.leading)
        if n < 4 or len(self.lines) - n < 3:
            return []
        a = CodeBlock(self.lines[:n], self.color, self.size, self.first)
        b = CodeBlock(self.lines[n:], self.color, self.size, False)
        return [a, b]

    def draw(self):
        c = self.canv
        h = self.height
        c.saveState()
        c.setFillColor(tint(self.color, 0.055))
        c.setStrokeColor(tint(self.color, 0.22))
        c.setLineWidth(0.6)
        c.roundRect(0, 8, self.width, h, 3, fill=1, stroke=1)
        c.setFillColor(tint(self.color, 0.75))
        c.rect(0, 8, 2.6, h, fill=1, stroke=0)
        c.setFillColor(HexColor('#1F2937'))
        c.setFont('Mono', self.size)
        y = 8 + h - self.pad - self.size
        for ln in self.lines:
            if ln.strip():
                c.drawString(self.pad + self.gutter, y, ln)
            y -= self.leading
        c.restoreState()


def callout(text, accent, label=None, style=None, tint_factor=0.10):
    """Tinted box with a thick coloured left border."""
    style = style or S_CALL
    flows = []
    if label and isinstance(text, str) and \
            plain(text).upper().startswith(label.upper()):
        label = None
    if label:
        flows.append(Paragraph(
            '<font color="%s" size="7.6"><b>%s</b></font>' %
            (accent.hexval().replace('0x', '#'), label.upper()),
            ParagraphStyle('cl', fontName='Body-B', fontSize=7.6, leading=10,
                           spaceAfter=2)))
    flows.append(Paragraph(text, style) if isinstance(text, str) else text)
    t = Table([[flows]], colWidths=[AVAIL_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), tint(accent, tint_factor)),
        ('LINEBEFORE', (0, 0), (0, -1), 3, accent),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t


class Rule(Flowable):
    def __init__(self, color, width=None, thickness=0.8, space=6):
        Flowable.__init__(self)
        self.color, self.thickness, self.space = color, thickness, space
        self._w = width

    def wrap(self, aw, ah):
        self.width = self._w or aw
        self.height = self.thickness
        return self.width, self.thickness + self.space

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.space / 2, self.width, self.space / 2)


# --------------------------------------------------------------------------
# markdown parsing
# --------------------------------------------------------------------------
FENCE = '`' * 3


def parse_blocks(text):
    lines = text.split('\n')
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if stripped.startswith(FENCE):
            lang = stripped[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith(FENCE):
                buf.append(lines[i].rstrip('\n'))
                i += 1
            i += 1
            while buf and not buf[0].strip():
                buf.pop(0)
            while buf and not buf[-1].strip():
                buf.pop()
            blocks.append(('code', buf, lang))
            continue

        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            blocks.append(('h', len(m.group(1)), m.group(2).strip()))
            i += 1
            continue

        if re.match(r'^\s*(-{3,}|\*{3,}|_{3,})\s*$', line):
            blocks.append(('hr',))
            i += 1
            continue

        if stripped.startswith('|'):
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(lines[i].strip())
                i += 1
            blocks.append(('table', rows))
            continue

        if stripped.startswith('>'):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i]).rstrip())
                i += 1
            blocks.append(('quote', buf))
            continue

        if re.match(r'^\s*([-*+]|\d+\.)\s+\S', line):
            items = []
            while i < n:
                cur = lines[i]
                mm = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.*)$', cur.rstrip())
                if mm:
                    indent = len(mm.group(1).expandtabs(4))
                    ordered = mm.group(2)[0].isdigit()
                    marker = mm.group(2)
                    items.append([1 if indent >= 2 else 0, ordered, marker,
                                  mm.group(3).strip()])
                    i += 1
                    continue
                if cur.strip() and items and not cur.strip().startswith(('|', '#', FENCE, '>')) \
                        and cur.startswith((' ', '\t')):
                    items[-1][3] += ' ' + cur.strip()
                    i += 1
                    continue
                break
            blocks.append(('list', items))
            continue

        if not stripped:
            i += 1
            continue

        buf = [stripped]
        i += 1
        while i < n:
            nxt = lines[i].rstrip()
            if not nxt.strip():
                break
            if re.match(r'^(#{1,6})\s', nxt) or nxt.strip().startswith(('|', FENCE, '>')) \
                    or re.match(r'^\s*([-*+]|\d+\.)\s+\S', nxt) \
                    or re.match(r'^\s*(-{3,})\s*$', nxt):
                break
            buf.append(nxt.strip())
            i += 1
        blocks.append(('p', ' '.join(buf)))
    return blocks


def split_table(rows):
    def cells(row):
        row = row.strip()
        row = re.sub(r'^\|', '', row)
        row = re.sub(r'\|$', '', row)
        parts = row.replace('\\|', '\x03').split('|')
        return [p.strip().replace('\x03', '\\|') for p in parts]

    grid = [cells(r) for r in rows]
    body = [r for r in grid
            if not all(re.fullmatch(r':?-{2,}:?', c or '-') for c in r)]
    if not body:
        return None
    width = max(len(r) for r in body)
    for r in body:
        while len(r) < width:
            r.append('')
    return body


def build_table(rows, color):
    grid = split_table(rows)
    if not grid:
        return None
    header, body = grid[0], grid[1:]
    ncols = len(header)
    fs = 7.9 if ncols <= 3 else (7.4 if ncols <= 5 else 6.7)
    th = ParagraphStyle('th%d' % ncols, parent=S_TH, fontSize=fs - 0.2,
                        leading=(fs - 0.2) * 1.25)
    td = ParagraphStyle('td%d' % ncols, parent=S_TD, fontSize=fs,
                        leading=fs * 1.32)

    weights = []
    for c in range(ncols):
        longest_word = 0
        total = 0
        for r in grid:
            plain = strip_marks(re.sub(r'[`*\[\]]|\(https?://[^)]*\)', '', r[c]))
            total = max(total, len(plain))
            for w in plain.split():
                longest_word = max(longest_word, len(w))
        weights.append(max(min(total, 58), min(longest_word, 16), 6))
    scale = AVAIL_W / float(sum(weights))
    widths = [w * scale for w in weights]
    floors = []
    for c in range(ncols):
        head_word = max(strip_marks(re.sub(r'[`*]', '', header[c])).split() or [''],
                        key=len)
        body_word = ''
        for r in grid[1:]:
            cleaned = strip_marks(re.sub(r'[`*\[\]]|\(https?://[^)]*\)', '', r[c]))
            for w in cleaned.split():
                if len(w) > len(body_word):
                    body_word = w
        need = max(pdfmetrics.stringWidth(head_word, 'Body-B', fs - 0.2),
                   pdfmetrics.stringWidth(body_word, 'Body', fs))
        floors.append(max(34.0, min(need + 10.0, 74.0)))
    if sum(floors) > 0.8 * AVAIL_W:
        k = 0.8 * AVAIL_W / sum(floors)
        floors = [f * k for f in floors]
    for _ in range(5):
        short = [i for i, w in enumerate(widths) if w < floors[i] - 0.1]
        if not short:
            break
        deficit = sum(floors[i] - widths[i] for i in short)
        donors = [i for i in range(ncols)
                  if i not in short and widths[i] > floors[i] + 14]
        if not donors:
            break
        pool = sum(widths[i] - floors[i] for i in donors)
        for i in short:
            widths[i] = floors[i]
        for i in donors:
            widths[i] -= deficit * (widths[i] - floors[i]) / pool
    widths = [w * AVAIL_W / sum(widths) for w in widths]

    data = [[Paragraph(inline(c, mono_size=fs - 0.3), th) for c in header]]
    for r in body:
        data.append([Paragraph(inline(c, mono_size=fs - 0.3), td) for c in r])

    style = [
        ('BACKGROUND', (0, 0), (-1, 0), color),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.4, LINE),
        ('LINEBELOW', (0, 0), (-1, 0), 0.9, tint(color, 1.0)),
        ('LEFTPADDING', (0, 0), (-1, -1), 4.5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4.5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.6),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            style.append(('BACKGROUND', (0, r), (-1, r), ZEBRA))
    try:
        t = Table(data, colWidths=widths, repeatRows=1, splitByRow=1,
                  splitInRow=1, hAlign='LEFT')
    except TypeError:
        t = Table(data, colWidths=widths, repeatRows=1, splitByRow=1, hAlign='LEFT')
    t.setStyle(TableStyle(style))
    return t


# --------------------------------------------------------------------------
# document assembly
# --------------------------------------------------------------------------
LEAD_MARK = {
    '\u2705': (GREEN, 'FIX'),
    '\u274c': (RED, 'PROBLEM'),
    '\u26a0': (AMBER, 'CAUTION'),
    '\U0001f6a8': (RED, 'CRITICAL'),
}


def section_key_and_color(title):
    m = re.match(r'^(\d+)\.\s*(.*)$', title)
    if m:
        num = int(m.group(1))
        return num, m.group(2).strip(), SECTION_COLORS.get(num, SILVER)
    up = strip_marks(title).upper()
    if up.startswith('TABLE OF CONTENTS'):
        return 'TOC', title, SECTION_COLORS['TOC']
    if up.startswith('APPENDIX'):
        return 'APPENDIX', title, SECTION_COLORS['APPENDIX']
    return None, title, SILVER


def toc_descriptions(blocks):
    """Pull the 'what it answers' column out of the markdown TOC table."""
    desc = {}
    for kind, *rest in blocks:
        if kind != 'table':
            continue
        grid = split_table(rest[0])
        if not grid or len(grid[0]) < 3:
            continue
        head = [strip_marks(c).lower() for c in grid[0]]
        if head[0].startswith('#') and 'section' in head[1]:
            for row in grid[1:]:
                num = re.sub(r'\D', '', row[0])
                if num:
                    label = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', row[1]).strip()
                    desc[int(num)] = (label, row[2].strip())
            break
    return desc


def toc_table(entries, pages):
    data = [[Paragraph('<font color="#FFFFFF"><b>#</b></font>', S_TOC),
             Paragraph('<font color="#FFFFFF"><b>SECTION</b></font>', S_TOC),
             Paragraph('<font color="#FFFFFF"><b>WHAT IT ANSWERS</b></font>', S_TOC),
             Paragraph('<font color="#FFFFFF"><b>PAGE</b></font>', S_TOC)]]
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), SECTION_COLORS['TOC']),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.35, LINE),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 3.6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.8),
        ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
    ]
    for idx, (key, num, title, color, desc) in enumerate(entries, start=1):
        page = pages.get(key)
        data.append([
            Paragraph('<font color="%s"><b>%s</b></font>' %
                      (color.hexval().replace('0x', '#'), num or '\u00b7'), S_TOC),
            Paragraph(inline(title), S_TOCB),
            Paragraph(inline(desc or ''), S_TOC),
            Paragraph('<b>%s</b>' % (page if page else '\u2013'), S_TOC),
        ])
        style.append(('BACKGROUND', (0, idx), (0, idx), tint(color, 0.16)))
        style.append(('LINEBEFORE', (0, idx), (0, idx), 2.6, color))
        if idx % 2 == 0:
            style.append(('BACKGROUND', (1, idx), (-1, idx), ZEBRA))
    t = Table(data, colWidths=[26, 170, AVAIL_W - 26 - 170 - 38, 38],
              repeatRows=1, hAlign='LEFT')
    t.setStyle(TableStyle(style))
    return t


def legend_flowables():
    out = [SubHead('How to read this document', SECTION_COLORS['TOC'],
                   anchor='legend', outline=True)]
    out.append(Paragraph(
        'Every major section carries its own accent colour. That colour is used for the '
        'section banner, its table headers, the left edge of its diagrams, the page header '
        'rule and the thumb tab printed on the outer edge of each page &mdash; so you can '
        'find a section by its colour alone when the report is printed.', S_BODY))
    out.append(Spacer(1, 4))

    rows = [[Paragraph('<font color="#FFFFFF"><b>MARK</b></font>', S_TD),
             Paragraph('<font color="#FFFFFF"><b>MEANING</b></font>', S_TD),
             Paragraph('<font color="#FFFFFF"><b>MARK</b></font>', S_TD),
             Paragraph('<font color="#FFFFFF"><b>MEANING</b></font>', S_TD)]]
    pairs = [
        (GREEN, 'OK', 'A fix, a verified claim, or a recommended choice',
         RED, 'NO', 'A problem, a rejected option, or a wrong assumption'),
        (AMBER, '!', 'Caution &mdash; a trap, cost or risk to watch',
         RED, '!!', 'Critical warning'),
        (HexColor('#DC2626'), 'MUST', 'Compulsory technology (project fails without it)',
         HexColor('#B45309'), 'REC', 'Strongly recommended'),
        (HexColor('#15803D'), 'OPT', 'Optional / nice-to-have',
         HexColor('#334155'), 'v2', 'Deferred to a future version'),
        (GOLD, '#1', 'Highest-priority dataset or resource',
         BLUE, 'ADOPT', 'Something we take directly from prior work'),
    ]
    for c1, l1, d1, c2, l2, d2 in pairs:
        rows.append([
            Paragraph('<font color="%s"><b>%s</b></font>' % (c1.hexval().replace('0x', '#'), l1), S_TD),
            Paragraph(d1, S_TD),
            Paragraph('<font color="%s"><b>%s</b></font>' % (c2.hexval().replace('0x', '#'), l2), S_TD),
            Paragraph(d2, S_TD)])
    t = Table(rows, colWidths=[42, AVAIL_W / 2 - 42, 42, AVAIL_W / 2 - 42],
              hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), SECTION_COLORS['TOC']),
        ('GRID', (0, 0), (-1, -1), 0.4, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 3.2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.4),
    ]))
    out.append(t)
    out.append(Spacer(1, 8))
    out.append(callout(
        'Diagrams and code are shown in a monospaced block tinted with the section '
        'colour. Long diagrams continue across a page break and keep their alignment. '
        'Numbers, quotes and sources are reproduced from the source report without change.',
        SECTION_COLORS['TOC'], label='Note'))
    return out


def colour_map_flowables(entries):
    """Three-column grid: which colour belongs to which section."""
    out = [Spacer(1, 12),
           SubHead('Section colour map', SECTION_COLORS['TOC'],
                   anchor='colourmap', outline=True)]
    cols = 3
    rows = [[] for _ in range((len(entries) + cols - 1) // cols)]
    style = []
    cell_style = ParagraphStyle('cmap', fontName='Body', fontSize=7.6,
                                leading=9.6, textColor=INK_SOFT)
    for i, (key, num, title, color, _desc) in enumerate(entries):
        r, c = i // cols, i % cols
        rows[r].append('')
        rows[r].append(Paragraph(
            '<b>%s</b>  %s' % (num if num != '' else 'A', _esc(plain(title))),
            cell_style))
        style.append(('BACKGROUND', (c * 2, r), (c * 2, r), color))
    while len(rows[-1]) < cols * 2:
        rows[-1].append('')
    chip = 12
    label = (AVAIL_W - cols * chip) / cols
    t = Table(rows, colWidths=[chip, label] * cols, hAlign='LEFT')
    style += [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEBELOW', (0, 0), (-1, -1), 0.3, LINE),
    ]
    t.setStyle(TableStyle(style))
    out.append(t)
    return out


def build_story(blocks, toc_entries, toc_pages, desc_map):
    story = []
    cur_color = SECTION_COLORS['TOC']
    sub_counter = [0]
    started = False
    skip_table = False

    story.append(Spacer(1, 1))                      # cover page body
    story.append(PageBreak())
    story.append(SectionBand('TOC', None, 'Contents & reading guide',
                             SECTION_COLORS['TOC'],
                             kicker='SETU project report'))
    story.append(Spacer(1, 2))
    story.append(toc_table(toc_entries, toc_pages))
    story.append(PageBreak())
    story.extend(legend_flowables())
    story.extend(colour_map_flowables(toc_entries))

    for blk in blocks:
        kind = blk[0]

        if kind == 'h':
            level, title = blk[1], blk[2]
            if level <= 2:
                key, clean, color = section_key_and_color(title)
                if key is None:
                    continue
                if key == 'TOC':
                    skip_table = True
                    started = True
                    continue
                started = True
                cur_color = color
                sub_counter[0] = 0
                num = key if isinstance(key, int) else None
                kicker = None
                if isinstance(key, int):
                    kicker = 'Section %d of 25' % key
                elif key == 'APPENDIX':
                    kicker = 'Appendix'
                story.append(PageBreak())
                story.append(SectionBand(str(key), num, plain(clean), color,
                                         kicker=kicker))
                dsc = desc_map.get(key, (None, None))[1] if isinstance(key, int) else None
                if dsc:
                    story.append(Paragraph(
                        '<font color="%s"><b>%s</b></font>' %
                        (color.hexval().replace('0x', '#'), inline(dsc)),
                        ParagraphStyle('kick', parent=S_BODY, fontSize=9.2,
                                       leading=12.4, spaceAfter=7)))
                continue
            if not started:
                continue
            accent = cur_color
            lead = title.lstrip('*_ ')
            for ch, (col, _lab) in LEAD_MARK.items():
                if lead.startswith(ch):
                    accent = col
                    title = title.replace(ch, '', 1).replace('\ufe0f', '', 1)
                    title = re.sub(r'^(\*{0,2})\s+', r'\1', title)
                    break
            sub_counter[0] += 1
            anchor = 'sub_%s_%d' % (str(cur_color.hexval()), sub_counter[0])
            story.append(CondPageBreak(74))
            story.append(SubHead(inline(title), accent, level=3 if level == 3 else 4,
                                 anchor=anchor, outline=(level == 3)))
            continue

        if not started:
            continue

        if kind == 'table':
            if skip_table:
                skip_table = False
                continue
            t = build_table(blk[1], cur_color)
            if t is not None:
                story.append(Spacer(1, 2))
                story.append(t)
                story.append(Spacer(1, 8))
            continue

        if kind == 'code':
            lines = [fix_code(l) for l in blk[1]]
            if lines:
                story.append(CodeBlock(lines, cur_color))
                story.append(Spacer(1, 4))
            continue

        if kind == 'quote':
            text = ' '.join(l.strip() for l in blk[1] if l.strip())
            if text:
                story.append(Spacer(1, 2))
                story.append(callout(inline(text), cur_color, style=S_QUOTE,
                                     tint_factor=0.09))
                story.append(Spacer(1, 8))
            continue

        if kind == 'hr':
            continue

        if kind == 'list':
            items = blk[1]
            b1, b2 = bullet_styles(cur_color)
            for lvl, ordered, marker, text in items:
                st = b2 if lvl else b1
                bullet = marker if ordered else ('\u2013' if lvl else '\u2022')
                if text.startswith('\u25a1'):
                    text = text[1:].strip()
                    bullet = '\u25a1'
                story.append(Paragraph(inline(text), st, bulletText=bullet))
            story.append(Spacer(1, 5))
            continue

        if kind == 'p':
            text = blk[1]
            mark = None
            lead = text.lstrip('*_ ')
            for ch, (col, lab) in LEAD_MARK.items():
                if lead.startswith(ch):
                    mark = (col, lab)
                    text = text.replace(ch, '', 1).replace('\ufe0f', '', 1)
                    text = re.sub(r'^(\*{0,2})\s+', r'\1', text)
                    break
            if mark:
                bare = plain(text)
                if len(bare) <= 48:
                    story.append(Paragraph(
                        '<font color="%s">%s</font>' %
                        (mark[0].hexval().replace('0x', '#'), inline(text)),
                        ParagraphStyle('lab', fontName='Body-B', fontSize=9.5,
                                       leading=12.6, textColor=mark[0],
                                       spaceBefore=4, spaceAfter=1)))
                else:
                    story.append(Spacer(1, 2))
                    story.append(callout(inline(text), mark[0], label=mark[1]))
                    story.append(Spacer(1, 7))
            else:
                m = re.match(r'^\*\*(Key principle|The problem|Our edge|What.s missing|'
                             r'Why|Say this|Read the)', text)
                story.append(Paragraph(inline(text),
                                       S_LEAD if m else S_BODY))
            continue

    return story


# --------------------------------------------------------------------------
# page furniture
# --------------------------------------------------------------------------
SEC_ORDER = []      # list of section keys in document order
SEC_META = {}       # key -> (label, color)


def draw_cover(canv, doc):
    canv.saveState()
    canv.setFillColor(NAVY)
    canv.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # colour spectrum strip = the section palette
    keys = [k for k in SEC_ORDER if isinstance(k, int)]
    n = max(len(keys), 1)
    bw = (PAGE_W - 80) / n
    for i, k in enumerate(keys):
        canv.setFillColor(SECTION_COLORS.get(k, SILVER))
        canv.rect(40 + i * bw, PAGE_H - 118, bw - 1.5, 7, fill=1, stroke=0)

    canv.setFillColor(HexColor('#7FB0E8'))
    canv.setFont('Body-B', 10)
    canv.drawString(40, PAGE_H - 96, 'PROJECT REPORT  \u00b7  SMART INDIA HACKATHON')

    canv.setFillColor(colors.white)
    canv.setFont('Body-B', 74)
    canv.drawString(38, PAGE_H - 210, 'SETU')
    canv.setFillColor(HexColor('#4C7FBF'))
    canv.rect(40, PAGE_H - 232, 120, 3.5, fill=1, stroke=0)

    canv.setFillColor(colors.white)
    canv.setFont('Body-B', 20)
    canv.drawString(40, PAGE_H - 268, 'Crowdsourced Road Defect')
    canv.drawString(40, PAGE_H - 292, 'Intelligence for India')
    canv.setFillColor(HexColor('#9DC0E8'))
    canv.setFont('Body-I', 11.5)
    canv.drawString(40, PAGE_H - 316,
                    'Sensor-Enabled Tracking of Urban-road-damage')

    canv.setFillColor(HexColor('#C9DCF2'))
    canv.setFont('Body', 10.4)
    lines = [
        'Millions of phones already ride on Indian roads inside delivery and ride-hailing',
        'driver apps. SETU turns them into a free, always-on road inspection network and',
        'gives municipal engineers a live map of confirmed potholes ranked by severity.',
    ]
    y = PAGE_H - 352
    for ln in lines:
        canv.drawString(40, y, ln)
        y -= 15

    # stat cards
    stats = [('9,438', 'pothole deaths\n2020-2024'),
             ('+53%', 'rise in pothole\ncrashes in 5 years'),
             ('~1.2 cr', 'gig workers =\nour sensor fleet'),
             ('~Rs 3', 'our cost to confirm\none pothole')]
    cw = (PAGE_W - 80 - 3 * 10) / 4
    y0 = PAGE_H - 470
    for i, (big, small) in enumerate(stats):
        x = 40 + i * (cw + 10)
        canv.setFillColor(HexColor('#132844'))
        canv.roundRect(x, y0, cw, 74, 4, fill=1, stroke=0)
        canv.setFillColor(HexColor('#4C7FBF'))
        canv.rect(x, y0, cw, 2.6, fill=1, stroke=0)
        canv.setFillColor(colors.white)
        canv.setFont('Body-B', 19)
        canv.drawString(x + 10, y0 + 44, big)
        canv.setFillColor(HexColor('#93B4D8'))
        canv.setFont('Body', 7.8)
        yy = y0 + 30
        for part in small.split('\n'):
            canv.drawString(x + 10, yy, part)
            yy -= 9.6

    # three-layer summary
    canv.setFillColor(HexColor('#7FB0E8'))
    canv.setFont('Body-B', 9)
    canv.drawString(40, y0 - 40, 'THE COST-GATED ESCALATION LADDER')
    ladder = [
        (HexColor('#2E8B57'), 'LAYER 1', 'Phone sensors detect a bump  \u00b7  cost ~0  \u00b7  noisy'),
        (HexColor('#B8860B'), 'LAYER 2', 'Server clusters many vehicles  \u00b7  cost ~0  \u00b7  kills false alarms'),
        (HexColor('#B03030'), 'LAYER 3', 'Video + YOLO confirms  \u00b7  costly  \u00b7  used at ~0.1% of places'),
    ]
    yy = y0 - 62
    for col, tag, txt in ladder:
        canv.setFillColor(col)
        canv.roundRect(40, yy - 4, 56, 16, 2, fill=1, stroke=0)
        canv.setFillColor(colors.white)
        canv.setFont('Body-B', 8)
        canv.drawCentredString(68, yy + 0.5, tag)
        canv.setFillColor(HexColor('#C9DCF2'))
        canv.setFont('Body', 9)
        canv.drawString(104, yy + 0.5, txt)
        yy -= 22

    canv.setStrokeColor(HexColor('#274867'))
    canv.setLineWidth(0.8)
    canv.line(40, 96, PAGE_W - 40, 96)
    canv.setFillColor(HexColor('#7E9CBD'))
    canv.setFont('Body', 8.6)
    canv.drawString(40, 78, 'Problem \u00b7 research \u00b7 datasets \u00b7 architecture \u00b7 tech stack '
                            '\u00b7 roadmap \u00b7 feasibility \u00b7 business plan \u00b7 risk \u00b7 sources')
    canv.drawString(40, 64, 'Generated from PROJECT.md  \u00b7  %s' %
                    datetime.date.today().strftime('%d %B %Y'))
    canv.setFont('Body-B', 8.6)
    canv.setFillColor(HexColor('#C9DCF2'))
    canv.drawRightString(PAGE_W - 40, 64, '25 sections + appendix')
    canv.restoreState()


class ReportCanvas(pdfcanvas.Canvas):
    def __init__(self, *a, **kw):
        pdfcanvas.Canvas.__init__(self, *a, **kw)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        resolved = self._resolve_sections(total)
        by_page = {}
        for page, key, title, level in OUTLINE_ITEMS:
            by_page.setdefault(page, []).append((key, title, level))
        have_root = False
        for i, state in enumerate(self._saved, start=1):
            self.__dict__.update(state)
            if i > 1:
                self._furniture(i, total, resolved.get(i))
            for key, title, level in by_page.get(i, []):
                if level > 0 and not have_root:
                    continue
                self.bookmarkPage(key)
                self.addOutlineEntry(title, key, level, level == 1)
                if level == 0:
                    have_root = True
            pdfcanvas.Canvas.showPage(self)
        self.showOutline()
        pdfcanvas.Canvas.save(self)

    @staticmethod
    def _resolve_sections(total):
        out = {}
        cur = None
        for p in range(1, total + 1):
            if p in PAGE_SECTION:
                cur = PAGE_SECTION[p]
            out[p] = cur
        return out

    def _furniture(self, page, total, key):
        label, color = SEC_META.get(key, ('Contents', SECTION_COLORS['TOC']))
        self.saveState()
        # header
        self.setFillColor(MUTED)
        self.setFont('Body', 7.6)
        self.drawString(M_L, PAGE_H - 34,
                        'SETU  \u00b7  Crowdsourced Road Defect Intelligence for India')
        self.setFillColor(color)
        self.setFont('Body-B', 7.6)
        self.drawRightString(PAGE_W - M_R, PAGE_H - 34, label.upper()[:74])
        self.setStrokeColor(tint(color, 0.55))
        self.setLineWidth(0.8)
        self.line(M_L, PAGE_H - 41, PAGE_W - M_R, PAGE_H - 41)
        self.setStrokeColor(color)
        self.setLineWidth(2.2)
        self.line(M_L, PAGE_H - 41, M_L + 46, PAGE_H - 41)
        # footer
        self.setStrokeColor(LINE)
        self.setLineWidth(0.6)
        self.line(M_L, 32, PAGE_W - M_R, 32)
        self.setFillColor(MUTED)
        self.setFont('Body', 7.4)
        self.drawString(M_L, 21, 'Project report \u00b7 generated from PROJECT.md')
        self.setFillColor(color)
        self.setFont('Body-B', 8)
        self.drawRightString(PAGE_W - M_R, 21, 'Page %d of %d' % (page, total))
        # thumb tab on the outer edge
        keys = [k for k in SEC_ORDER if isinstance(k, int)]
        num = int(key) if (key or '').isdigit() else None
        if num is not None and num in keys:
            idx = keys.index(num)
            span = PAGE_H - 210
            th = span / max(len(keys), 1)
            y = PAGE_H - 120 - idx * th
            self.setFillColor(color)
            self.rect(PAGE_W - 6.5, y - th * 0.82, 6.5, th * 0.82, fill=1, stroke=0)
            self.setFillColor(colors.white)
            self.setFont('Body-B', 5.6)
            self.drawCentredString(PAGE_W - 3.2, y - th * 0.5, str(num))
        self.restoreState()


class ReportDoc(BaseDocTemplate):
    def __init__(self, path):
        BaseDocTemplate.__init__(
            self, path, pagesize=A4, title='SETU - Crowdsourced Road Defect '
            'Intelligence for India', author='SETU project team',
            subject='Project report: problem, research, architecture, tech stack, '
                    'roadmap, feasibility and business plan',
            leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B)
        cover = PageTemplate('cover', frames=[Frame(M_L, M_B, AVAIL_W, 20, id='c')],
                             onPage=draw_cover)
        body = PageTemplate('body', frames=[Frame(
            M_L, M_B, AVAIL_W, PAGE_H - M_T - M_B, id='b',
            leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)])
        self.addPageTemplates([cover, body])
        self._first = True

    def handle_pageBegin(self):
        BaseDocTemplate.handle_pageBegin(self)
        if self._first:
            self._first = False
            self.handle_nextPageTemplate('body')


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------
def main():
    md = open(SRC, encoding='utf-8').read()
    blocks = parse_blocks(md)
    desc_map = toc_descriptions(blocks)

    # section inventory (drives palette, TOC, thumb tabs, headers)
    entries = []
    for blk in blocks:
        if blk[0] == 'h' and blk[1] <= 2:
            key, clean, color = section_key_and_color(blk[2])
            if key is None or key == 'TOC':
                continue
            label = strip_marks(re.sub(r'\*+', '', clean))
            entries.append((str(key), key if isinstance(key, int) else '',
                            clean, color, desc_map.get(key, ('', ''))[1]))
            SEC_ORDER.append(key)
            SEC_META[str(key)] = (
                ('%d. %s' % (key, label)) if isinstance(key, int) else label, color)
    SEC_META['TOC'] = ('Contents & reading guide', SECTION_COLORS['TOC'])

    for label, pages_target in (('pass 1', SCRATCH), ('pass 2', OUT)):
        PAGE_SECTION.clear()
        OUTLINE_SEEN.clear()
        del OUTLINE_ITEMS[:]
        snapshot = dict(ANCHOR_PAGES)
        ANCHOR_PAGES.clear()
        story = build_story(blocks, entries, snapshot, desc_map)
        doc = ReportDoc(pages_target)
        doc.build(story, canvasmaker=ReportCanvas)
        print('%s -> %s (%d pages)' % (label, os.path.basename(pages_target),
                                       doc.page))
    try:
        os.remove(SCRATCH)
    except OSError:
        pass
    print('done:', OUT)


if __name__ == '__main__':
    main()
