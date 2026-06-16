# -*- coding: utf-8 -*-
"""
Squares & Cubes Study Table (1-100) for Aptitude Exams.
Generates: Excel (.xlsx) and PDF (A4 landscape, printable).
"""
import os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from fpdf import FPDF

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Aptitude-Tables")
os.makedirs(OUT_DIR, exist_ok=True)

# ---- Data ----------------------------------------------------------------
NUMS = list(range(1, 101))
SQUARES = {n: n * n for n in NUMS}
CUBES = {n: n ** 3 for n in NUMS}

# Commonly-asked perfect squares (the value, not n) frequently seen in exams
EXAM_SQUARES = {625, 1225, 2025, 3025, 5625, 7225, 9025, 1024, 1089, 1156,
                441, 529, 576, 676, 784, 841, 961, 2916, 4096, 5041, 6561, 8281}
# Commonly-asked perfect cubes frequently seen in exams
EXAM_CUBES = {125, 216, 343, 512, 729, 1331, 1728, 2197, 2744, 3375,
              4096, 4913, 5832, 6859, 8000, 9261, 27, 64, 1000}

# =========================================================================
#  EXCEL
# =========================================================================
def build_excel(path):
    wb = Workbook()

    thin = Side(style="thin", color="BBBBBB")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    hdr_fill = PatternFill("solid", fgColor="1F4E78")
    hdr_font = Font(bold=True, color="FFFFFF", size=12)
    alt_fill = PatternFill("solid", fgColor="DCE6F1")
    sq_fill = PatternFill("solid", fgColor="FFF2CC")   # highlight exam squares
    cube_fill = PatternFill("solid", fgColor="E2EFDA")  # highlight exam cubes
    center = Alignment(horizontal="center", vertical="center")
    title_font = Font(bold=True, size=16, color="1F4E78")

    # ---- Sheet 1: Main table (4 blocks of 25 rows side-by-side) ----------
    ws = wb.active
    ws.title = "Squares & Cubes 1-100"
    ws["A1"] = "SQUARES & CUBES TABLE (1 - 100)  |  Aptitude Exam Revision"
    ws["A1"].font = title_font
    ws.merge_cells("A1:L1")
    ws["A1"].alignment = center

    legend = ws["A2"]
    legend.value = "Yellow = exam-favourite squares    Green = exam-favourite cubes"
    legend.font = Font(italic=True, size=10, color="555555")
    ws.merge_cells("A2:L2")

    headers = ["n", "n²", "n³"]
    blocks = [(1, 25), (26, 50), (51, 75), (76, 100)]
    start_row = 4

    # header row across 4 blocks (3 cols + 1 gap each)
    col = 1
    for bi, _ in enumerate(blocks):
        for h in headers:
            c = ws.cell(row=start_row, column=col, value=h)
            c.font = hdr_font
            c.fill = hdr_fill
            c.alignment = center
            c.border = border
            col += 1
        col += 1  # gap column

    for ri in range(25):
        r = start_row + 1 + ri
        col = 1
        for (lo, hi) in blocks:
            n = lo + ri
            vals = [n, SQUARES[n], CUBES[n]]
            for ci, v in enumerate(vals):
                c = ws.cell(row=r, column=col + ci, value=v)
                c.alignment = center
                c.border = border
                if ci == 1 and v in EXAM_SQUARES:
                    c.fill = sq_fill
                    c.font = Font(bold=True)
                elif ci == 2 and v in EXAM_CUBES:
                    c.fill = cube_fill
                    c.font = Font(bold=True)
                elif ri % 2 == 1:
                    c.fill = alt_fill
            col += 4

    # column widths
    for cl in range(1, 17):
        ws.column_dimensions[get_column_letter(cl)].width = 9 if cl % 4 != 0 else 3

    # ---- Sheet 2: Summary -----------------------------------------------
    ws2 = wb.create_sheet("Summary & Revision")
    ws2["A1"] = "QUICK SUMMARY — Squares 1-30, Cubes 1-20, Roots"
    ws2["A1"].font = title_font
    ws2.merge_cells("A1:H1")

    def write_block(ws, top_left_col, top_row, title, headers, rows):
        c = ws.cell(row=top_row, column=top_left_col, value=title)
        c.font = Font(bold=True, size=12, color="1F4E78")
        hr = top_row + 1
        for i, h in enumerate(headers):
            cc = ws.cell(row=hr, column=top_left_col + i, value=h)
            cc.font = hdr_font
            cc.fill = hdr_fill
            cc.alignment = center
            cc.border = border
        for ridx, row in enumerate(rows):
            for i, v in enumerate(row):
                cc = ws.cell(row=hr + 1 + ridx, column=top_left_col + i, value=v)
                cc.alignment = center
                cc.border = border
                if ridx % 2 == 1:
                    cc.fill = alt_fill

    sq30 = [[n, SQUARES[n]] for n in range(1, 31)]
    cube20 = [[n, CUBES[n]] for n in range(1, 21)]
    write_block(ws2, 1, 3, "Squares 1 - 30", ["n", "n²"], sq30)
    write_block(ws2, 4, 3, "Cubes 1 - 20", ["n", "n³"], cube20)

    roots = [
        ["√625", 25], ["√1225", 35], ["√2025", 45], ["√3025", 55],
        ["√5625", 75], ["√7225", 85], ["√9025", 95], ["√1089", 33],
        ["√1369", 37], ["√1681", 41], ["√4096", 64], ["√6561", 81],
    ]
    croots = [
        ["∛125", 5], ["∛216", 6], ["∛343", 7], ["∛512", 8],
        ["∛729", 9], ["∛1331", 11], ["∛1728", 12], ["∛2197", 13],
        ["∛2744", 14], ["∛3375", 15], ["∛4096", 16], ["∛9261", 21],
    ]
    write_block(ws2, 7, 3, "Square Roots", ["√", "value"], roots)
    write_block(ws2, 10, 3, "Cube Roots", ["∛", "value"], croots)

    for cl in range(1, 13):
        ws2.column_dimensions[get_column_letter(cl)].width = 11

    wb.save(path)
    return path


# =========================================================================
#  PDF  (A4 landscape)
# =========================================================================
class PDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(31, 78, 120)
        self.cell(0, 8, "SQUARES & CUBES TABLE (1-100)  -  Aptitude Exam Revision",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(90, 90, 90)
        self.cell(0, 5, "Yellow = exam-favourite squares    |    Green = exam-favourite cubes",
                  align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, f"Page {self.page_no()}  |  SSC CGL / Banking / Railways / TNPSC / UPSC",
                  align="C")


def build_pdf(path):
    pdf = PDF(orientation="L", unit="mm", format="A4")
    # Manual positioning (set_xy + cell) is used throughout; auto page-break
    # must stay OFF or each cell near the margin spawns a stray page.
    pdf.set_auto_page_break(auto=False, margin=12)
    pdf.add_page()

    HDR = (31, 78, 120)
    ALT = (220, 230, 241)
    SQH = (255, 242, 204)
    CBH = (226, 239, 218)

    blocks = [(1, 25), (26, 50), (51, 75), (76, 100)]
    col_w = [11, 18, 28]            # n, n^2, n^3
    block_w = sum(col_w)
    gap = 6
    total = block_w * 4 + gap * 3
    x0 = (297 - total) / 2
    row_h = 7.0

    def header_row(y):
        x = x0
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(255, 255, 255)
        for _ in range(4):
            labels = ["n", "n2", "n3"]
            for w, lab in zip(col_w, labels):
                pdf.set_fill_color(*HDR)
                pdf.set_xy(x, y)
                pdf.cell(w, row_h, lab, border=1, align="C", fill=True)
                x += w
            x += gap

    y = pdf.get_y()
    header_row(y)
    y += row_h

    pdf.set_font("Helvetica", "", 9)
    for ri in range(25):
        x = x0
        for (lo, hi) in blocks:
            n = lo + ri
            cells = [(str(n), None), (str(SQUARES[n]),
                     SQH if SQUARES[n] in EXAM_SQUARES else None),
                     (str(CUBES[n]), CBH if CUBES[n] in EXAM_CUBES else None)]
            for (w, (txt, fill)) in zip(col_w, cells):
                if fill:
                    pdf.set_fill_color(*fill)
                    pdf.set_font("Helvetica", "B", 9)
                    do_fill = True
                elif ri % 2 == 1:
                    pdf.set_fill_color(*ALT)
                    pdf.set_font("Helvetica", "", 9)
                    do_fill = True
                else:
                    pdf.set_font("Helvetica", "", 9)
                    do_fill = False
                pdf.set_text_color(0, 0, 0)
                pdf.set_xy(x, y)
                pdf.cell(w, row_h, txt, border=1, align="C", fill=do_fill)
                x += w
            x += gap
        y += row_h

    # ---- Page 2: Summary -------------------------------------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(*HDR)
    pdf.cell(0, 8, "QUICK SUMMARY  -  Squares 1-30 | Cubes 1-20 | Roots",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    def mini_table(x, y, title, headers, rows, widths):
        pdf.set_xy(x, y)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*HDR)
        pdf.cell(sum(widths), 6, title, align="C", new_x="LMARGIN", new_y="NEXT")
        ty = y + 6
        cx = x
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(255, 255, 255)
        for w, h in zip(widths, headers):
            pdf.set_fill_color(*HDR)
            pdf.set_xy(cx, ty)
            pdf.cell(w, 5.5, h, border=1, align="C", fill=True)
            cx += w
        ty += 5.5
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(0, 0, 0)
        for ridx, row in enumerate(rows):
            cx = x
            fillrow = ridx % 2 == 1
            if fillrow:
                pdf.set_fill_color(*ALT)
            for w, v in zip(widths, row):
                pdf.set_xy(cx, ty)
                pdf.cell(w, 5.0, str(v), border=1, align="C", fill=fillrow)
                cx += w
            ty += 5.0
        return ty

    top = pdf.get_y()
    # squares 1-30 split into two columns of 15 to stay compact
    sq_a = [[n, SQUARES[n]] for n in range(1, 16)]
    sq_b = [[n, SQUARES[n]] for n in range(16, 31)]
    cb = [[n, CUBES[n]] for n in range(1, 21)]
    mini_table(15, top, "Squares 1-15", ["n", "n2"], sq_a, [12, 22])
    mini_table(55, top, "Squares 16-30", ["n", "n2"], sq_b, [12, 22])
    mini_table(95, top, "Cubes 1-20", ["n", "n3"], cb, [12, 26])

    roots = [["sqrt 625", 25], ["sqrt 1225", 35], ["sqrt 2025", 45],
             ["sqrt 3025", 55], ["sqrt 5625", 75], ["sqrt 7225", 85],
             ["sqrt 9025", 95], ["sqrt 1089", 33], ["sqrt 1369", 37],
             ["sqrt 1681", 41], ["sqrt 4096", 64], ["sqrt 6561", 81]]
    croots = [["cbrt 125", 5], ["cbrt 216", 6], ["cbrt 343", 7],
              ["cbrt 512", 8], ["cbrt 729", 9], ["cbrt 1331", 11],
              ["cbrt 1728", 12], ["cbrt 2197", 13], ["cbrt 2744", 14],
              ["cbrt 3375", 15], ["cbrt 4096", 16], ["cbrt 9261", 21]]
    mini_table(150, top, "Square Roots", ["root", "value"], roots, [26, 18])
    mini_table(200, top, "Cube Roots", ["root", "value"], croots, [26, 18])

    # ---- Page 3: Quick Exam Revision Sheet -------------------------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*HDR)
    pdf.cell(0, 10, "QUICK EXAM REVISION SHEET", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 6, "Most-asked squares & cubes  -  SSC CGL | Banking | Railways | TNPSC | UPSC",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    def section(title, lines):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*HDR)
        pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(0, 0, 0)
        for ln in lines:
            pdf.cell(0, 6, "  -  " + ln, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    section("MUST-MEMORIZE SQUARES (high frequency)", [
        "25^2=625, 35^2=1225, 45^2=2025, 55^2=3025, 75^2=5625, 85^2=7225, 95^2=9025",
        "All ending in 5: take left digit d, answer = d*(d+1) then append 25  (e.g. 65^2 -> 6*7=42 -> 4225)",
        "32^2=1024, 33^2=1089, 41^2=1681, 64^2=4096, 81^2=6561, 99^2=9801",
    ])
    section("MUST-MEMORIZE CUBES (high frequency)", [
        "5^3=125, 6^3=216, 7^3=343, 8^3=512, 9^3=729, 11^3=1331, 12^3=1728",
        "13^3=2197, 14^3=2744, 15^3=3375, 16^3=4096, 20^3=8000, 21^3=9261",
    ])
    section("FAST TRICKS", [
        "Unit digit of a cube uniquely maps back (cube root shortcut): 1->1,2->8,3->7,4->4,5->5,6->6,7->3,8->2,9->9,0->0",
        "Square ending check: squares never end in 2,3,7,8 -> spot wrong options instantly",
        "(a)^2 near base 50/100: 48^2 = (50-2)^2 = 2500 -200 +4 = 2304",
    ])
    section("WHERE THEY APPEAR", [
        "SSC CGL / CHSL: simplification, number system, surds",
        "Banking (IBPS/SBI): approximation & quadratic equations",
        "Railways (RRB): basic arithmetic speed rounds",
        "TNPSC / UPSC CSAT: aptitude & data interpretation",
    ])

    pdf.output(path)
    return path


if __name__ == "__main__":
    xlsx = build_excel(os.path.join(OUT_DIR, "Squares_Cubes_Study_Table.xlsx"))
    pdf = build_pdf(os.path.join(OUT_DIR, "Squares_Cubes_Study_Table.pdf"))
    print("Excel saved:", xlsx)
    print("PDF saved:", pdf)
