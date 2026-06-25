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


class PDF(FPDF):
    def header(self):
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

    pdf.output(path)


if __name__ == "__main__":
    out = os.path.join(OUT_DIR, "Multiplication_Tables_1_to_30.pdf")
    build_pdf(out)
    print(f"Created: {out}")
