# -*- coding: utf-8 -*-
"""
Multiplication Tables (1-30) for Aptitude Exams.
Generates a clean, printable PDF (A4 portrait) with tables 1 to 30,
each showing n x 1 ... n x 10, laid out in a grid for quick revision.
"""
import os
from fpdf import FPDF

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Aptitude-Tables")
os.makedirs(OUT_DIR, exist_ok=True)

MAX_TABLE = 30      # tables 1..30
MULTIPLIER = 10     # n x 1 .. n x 10

# Layout: grid of small table-cards on each page
COLS = 3            # cards per row
NAVY = (31, 78, 120)
LIGHT = (220, 230, 241)
ALT = (242, 247, 252)
GREY = (120, 120, 120)
GREEN = (33, 102, 60)        # header for the factor-pairs section

# Highly-factorable / composite numbers worth memorising for SSC aptitude
# (ratio, LCM/HCF, simplification, square-root spotting).
FACTOR_NUMBERS = [
    12, 16, 18, 24, 36, 48, 60, 64, 72, 84, 90, 96, 100,
    108, 120, 144, 168, 180, 196, 210, 216, 240, 256, 288,
    300, 324, 360, 400, 420, 480, 576, 600, 625, 720, 900,
]


def factor_pairs(n):
    """Return all unordered factor pairs (a, b) with a <= b and a*b = n."""
    pairs = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            pairs.append((i, n // i))
        i += 1
    return pairs


class PDF(FPDF):
    in_factor_section = False

    def header(self):
        if self.in_factor_section:
            self.set_font("Helvetica", "B", 14)
            self.set_text_color(*GREEN)
            self.cell(0, 9, "FACTOR PAIRS  -  Highly-Factorable Numbers", ln=1, align="C")
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(*GREY)
            self.cell(0, 5, "All ways to write each number as a x b   (sq = perfect square)", ln=1, align="C")
            self.ln(2)
            return
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*NAVY)
        self.cell(0, 9, "MULTIPLICATION TABLES (1 - 30)", ln=1, align="C")
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*GREY)
        self.cell(0, 5, "Aptitude Exam Revision  -  each table x1 to x10", ln=1, align="C")
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GREY)
        self.cell(0, 8, f"Page {self.page_no()}", align="C")


def draw_card(pdf, n, x, y, w):
    """Draw one table card for number n at position (x, y) with width w."""
    row_h = 6.2
    title_h = 7.5
    pdf.set_xy(x, y)

    # Title bar
    pdf.set_fill_color(*NAVY)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(w, title_h, f"Table of {n}", border=0, ln=2, align="C", fill=True)

    # Rows: n x i = result
    pdf.set_font("Helvetica", "", 10)
    for i in range(1, MULTIPLIER + 1):
        pdf.set_x(x)
        fill = (i % 2 == 0)
        if fill:
            pdf.set_fill_color(*ALT)
        pdf.set_text_color(50, 50, 50)
        line = f"{n}  x  {i:>2}  =  {n * i}"
        pdf.cell(w, row_h, line, border="LR", ln=2, align="C", fill=fill)

    # bottom border
    pdf.set_x(x)
    pdf.cell(w, 0, "", border="T", ln=2)
    return title_h + row_h * MULTIPLIER


def draw_factor_card(pdf, n, x, y, w):
    """Draw one factor-pairs card for number n. Returns the card height used."""
    row_h = 6.2
    title_h = 7.5
    pairs = factor_pairs(n)
    # Skip the trivial 1 x n line to save space when the number is rich in factors.
    body = pairs[1:] if len(pairs) > 1 else pairs

    pdf.set_xy(x, y)
    # Title bar
    pdf.set_fill_color(*GREEN)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(w, title_h, f"{n}", border=0, ln=2, align="C", fill=True)

    pdf.set_font("Helvetica", "", 10)
    for idx, (a, b) in enumerate(body):
        pdf.set_x(x)
        fill = (idx % 2 == 1)
        if fill:
            pdf.set_fill_color(*ALT)
        pdf.set_text_color(50, 50, 50)
        mark = "  (sq)" if a == b else ""
        line = f"{a:>3}  x  {b:<3}{mark}"
        pdf.cell(w, row_h, line, border="LR", ln=2, align="C", fill=fill)

    pdf.set_x(x)
    pdf.cell(w, 0, "", border="T", ln=2)
    return title_h + row_h * len(body)


def draw_factor_section(pdf):
    """New page(s): factor pairs for highly-factorable numbers."""
    pdf.in_factor_section = True
    pdf.add_page()  # header() now renders the factor-section title

    margin = 12
    gap = 6
    usable = 210 - 2 * margin
    fcols = 4  # these cards are narrower than the tables
    card_w = (usable - gap * (fcols - 1)) / fcols

    start_x = margin
    x = start_x
    y = pdf.get_y()
    page_bottom = 297 - 15
    col = 0
    row_max_h = 0

    for n in FACTOR_NUMBERS:
        body_len = max(1, len(factor_pairs(n)) - 1)
        card_h = 7.5 + 6.2 * body_len + 4

        if col == fcols:
            col = 0
            x = start_x
            y += row_max_h + gap
            row_max_h = 0
        if y + card_h > page_bottom:
            pdf.add_page()
            y = pdf.get_y()
            x = start_x
            col = 0
            row_max_h = 0

        draw_factor_card(pdf, n, x, y, card_w)
        row_max_h = max(row_max_h, card_h)
        x += card_w + gap
        col += 1


def build_pdf(path):
    pdf = PDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    margin = 12
    gap = 6
    usable = 210 - 2 * margin
    card_w = (usable - gap * (COLS - 1)) / COLS
    card_h = 7.5 + 6.2 * MULTIPLIER + 4  # title + rows + breathing room

    start_x = margin
    x = start_x
    y = pdf.get_y()
    page_bottom = 297 - 15
    col = 0

    for n in range(1, MAX_TABLE + 1):
        # New row of cards?
        if col == COLS:
            col = 0
            x = start_x
            y += card_h + gap
        # New page if card won't fit
        if y + card_h > page_bottom:
            pdf.add_page()
            y = pdf.get_y()
            x = start_x
            col = 0

        draw_card(pdf, n, x, y, card_w)
        x += card_w + gap
        col += 1

    # New section: factor pairs of highly-factorable numbers
    draw_factor_section(pdf)

    pdf.output(path)


if __name__ == "__main__":
    out = os.path.join(OUT_DIR, "Multiplication_Tables_1_to_30.pdf")
    build_pdf(out)
    print(f"Created: {out}")
