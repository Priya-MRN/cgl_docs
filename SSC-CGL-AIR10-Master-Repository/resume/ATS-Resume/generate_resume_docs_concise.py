"""
ATS-optimized resume generator for Priyadharshini Arumugam — CONCISE variant.

Same clean layout as generate_resume_docs.py, but with tightened bullets
(each ≤ 2 lines) and a shorter summary for a punchier, faster-scanning read.
Produces a polished, single-column, ATS-friendly resume in both DOCX and PDF
from one shared content source. Design goals:
  - ATS-safe: real text, standard fonts, standard headings, no layout tables.
  - Clean typography: consistent sizing, breathable leading, thin rule under headings.
  - High-impact bullets: ownership, rapid end-to-end delivery, and team collaboration.
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.shared import Pt, RGBColor, Inches
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable,
    KeepTogether,
)
from pathlib import Path

# ----------------------------------------------------------------------------
# Output location
# ----------------------------------------------------------------------------
OUT_DIR = Path(r'd:\Documents\cgl_docs\SSC-CGL-AIR10-Master-Repository\resume\ATS-Resume')
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------------
# Contact / header
# ----------------------------------------------------------------------------
NAME = 'PRIYADHARSHINI ARUMUGAM'
TAGLINE = 'Full Stack Developer  |  Laravel & PHP  |  REST APIs & ERP Systems  |  Python / FastAPI (In Progress)'
PHONE = '+91 95971 86254'
EMAIL = 'priyadharshiniarumugam52@gmail.com'
LOCATION = 'Puducherry, India'
LINKEDIN = 'linkedin.com/in/priyadharshini-arumugam-a43973229'

# Brand colors
INK = '1A1A1A'        # near-black body text
ACCENT = '1F4E79'     # deep professional blue for headings / name
MUTED = '555555'      # secondary text (roles, dates, contact line)
RULE = 'B7C4D4'       # thin divider under section headings

# ----------------------------------------------------------------------------
# Content
#   Experience entry = (company, role, dates, [bullets])
# ----------------------------------------------------------------------------
SUMMARY = (
    'Full Stack Developer with 6+ years shipping production web apps in Laravel, PHP, and MySQL '
    'across ERP, healthcare (EMR), and education platforms. Owns features end to end at startup '
    'speed and navigates large, interwoven codebases safely — now extending into Python, FastAPI, '
    'and AI agent development.'
)

SKILLS = [
    ('Languages & Frameworks',
     'PHP, Laravel, Symfony, JavaScript, Node.js, Express.js, Python, FastAPI (learning)'),
    ('Frontend & Mobile',
     'HTML5, CSS3, Bootstrap, jQuery, Flutter'),
    ('Databases & APIs',
     'MySQL, schema design, query optimization, REST API design, third-party integrations, Postman'),
    ('Auth & Reliability',
     'Firebase Auth, subscription / billing systems, multi-system integration, end-to-end ownership'),
    ('Tools & Platforms',
     'Git, GitHub, Jira, Confluence, VS Code, Linux deployment, Figma'),
    ('AI & Practices',
     'AI agent development, Claude AI, GitHub Copilot, Augment Code, Agile / Scrum, cross-functional collaboration'),
]

EXPERIENCE = [
    ('Interconnected Pty Ltd', 'PHP / Full Stack Developer', 'Remote, Australia  •  2025 – Present', [
        'Scoped, built, and shipped the REST API and Express.js layers powering a full-stack '
        'mindfulness meditation web and mobile app.',
        'Unified web and mobile auth with Firebase Auth, replacing fragmented sign-in flows '
        'with a single reliable system.',
        'Owned subscription-system health, resolving billing/access issues before customers '
        'hit them and cutting downtime.',
        'Rebuilt the legacy Hjarnfokus app from scratch in Flutter with a modernized '
        'architecture and improved UX.',
        'Delivered CMS, portal, and scheduling modules for an education platform, and '
        'converted onboarding flowcharts to Mermaid diagrams.',
    ]),
    ('Crontus Pty Ltd', 'PHP Developer', 'Remote, Australia  •  2024 – 2025', [
        'Worked across interwoven projects unified into one system, changing any unit safely '
        'without breaking the rest.',
        'Built scalable Laravel backends, designed REST APIs, and integrated third-party '
        'services.',
        'Collaborated in Agile sprint planning and iterative, team-based feature delivery.',
    ]),
    ('MRN Technologies Pvt. Ltd.', 'Web Developer', 'India  •  2022 – Present', [
        'Owned Clinoa (dental EMR) end to end — schema design plus the REST APIs behind the '
        'admin portal and Flutter app.',
        'Built Fishball ERP modules automating sales and inventory, and led UI/UX planning '
        'for its Figma redesign.',
        'Delivered full-stack web apps from scratch across multiple ERP and portal products.',
    ]),
    ('eSales Software Solutions LLP', 'Software Engineer', 'India  •  2018 – 2020', [
        'Delivered the SchoolSoftERP Marks Module with a mobile API and DB sync — recognized '
        'as Employee of the Month.',
        'Built the SSS Balvikas e-card feature, led its WordPress migration, and engineered '
        'the Rate Shopper shipping-rate API.',
    ]),
]

INTERNSHIP = [
    ('CodeAlpha', 'Python Intern', 'Remote  •  Ongoing', [
        'Built a Jira-integrated AI agent to automate issue workflows.',
        'Built a Support Agent AI for customer-support responses, plus a Python Hangman game '
        'reinforcing core OOP logic.',
    ]),
]

EDUCATION = ('B.Tech, Biomedical Engineering',
             'Rajiv Gandhi College of Engineering & Technology',
             '2014 – 2018')


# ============================================================================
# DOCX BUILDER
# ============================================================================
def _set_margins(doc, inches=0.7):
    for section in doc.sections:
        section.top_margin = Inches(inches)
        section.bottom_margin = Inches(inches)
        section.left_margin = Inches(inches + 0.05)
        section.right_margin = Inches(inches + 0.05)


def _no_space(paragraph, before=0, after=0, line=1.2):
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = line


def _bottom_border(paragraph, color=RULE, size=6):
    p = paragraph._p
    pPr = p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(size))
    bottom.set(qn('w:space'), '2')
    bottom.set(qn('w:color'), color)
    pbdr.append(bottom)
    pPr.append(pbdr)


def _heading(doc, text):
    p = doc.add_paragraph()
    _no_space(p, before=14, after=5)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(11.5)
    run.font.name = 'Calibri'
    run.font.color.rgb = RGBColor.from_string(ACCENT)
    # letter spacing for headings
    _bottom_border(p)
    return p


def build_docx(path):
    doc = Document()
    _set_margins(doc)

    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(10.5)
    normal.font.color.rgb = RGBColor.from_string(INK)

    # --- Header: name ---
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _no_space(p, after=2)
    run = p.add_run(NAME)
    run.bold = True
    run.font.size = Pt(22)
    run.font.color.rgb = RGBColor.from_string(ACCENT)

    # tagline
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _no_space(p, after=3)
    run = p.add_run(TAGLINE)
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor.from_string(MUTED)

    # contact line
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _no_space(p, after=6)
    contact = f'{LOCATION}   |   {PHONE}   |   {EMAIL}   |   {LINKEDIN}'
    run = p.add_run(contact)
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor.from_string(MUTED)

    # --- Summary ---
    _heading(doc, 'PROFESSIONAL SUMMARY')
    p = doc.add_paragraph()
    _no_space(p, after=3, line=1.3)
    run = p.add_run(SUMMARY)
    run.font.size = Pt(10.5)

    # --- Skills ---
    _heading(doc, 'TECHNICAL SKILLS')
    for label, items in SKILLS:
        p = doc.add_paragraph()
        _no_space(p, after=3, line=1.2)
        r1 = p.add_run(f'{label}:  ')
        r1.bold = True
        r1.font.size = Pt(10.5)
        r2 = p.add_run(items)
        r2.font.size = Pt(10.5)

    # --- Experience ---
    _heading(doc, 'PROFESSIONAL EXPERIENCE')
    for company, role, dates, bullets in EXPERIENCE:
        p = doc.add_paragraph()
        _no_space(p, before=9, after=0)
        r = p.add_run(company)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor.from_string(INK)
        tab = p.add_run(f'\t{dates}')
        tab.font.size = Pt(9.5)
        tab.font.color.rgb = RGBColor.from_string(MUTED)
        # right-align the dates via a tab stop
        p.paragraph_format.tab_stops.add_tab_stop(Inches(7.15), 2)  # 2 = RIGHT

        pr = doc.add_paragraph()
        _no_space(pr, after=4)
        rr = pr.add_run(role)
        rr.italic = True
        rr.font.size = Pt(10)
        rr.font.color.rgb = RGBColor.from_string(MUTED)

        for b in bullets:
            pb = doc.add_paragraph(style='List Bullet')
            _no_space(pb, after=4, line=1.2)
            pb.paragraph_format.left_indent = Inches(0.25)
            pb.paragraph_format.first_line_indent = Inches(-0.15)
            rb = pb.add_run(b)
            rb.font.size = Pt(10.5)

    # --- Internship ---
    _heading(doc, 'REMOTE INTERNSHIP')
    for company, role, dates, bullets in INTERNSHIP:
        p = doc.add_paragraph()
        _no_space(p, before=6, after=0)
        r = p.add_run(company)
        r.bold = True
        r.font.size = Pt(11)
        tab = p.add_run(f'\t{dates}')
        tab.font.size = Pt(9.5)
        tab.font.color.rgb = RGBColor.from_string(MUTED)
        p.paragraph_format.tab_stops.add_tab_stop(Inches(7.15), 2)

        pr = doc.add_paragraph()
        _no_space(pr, after=4)
        rr = pr.add_run(role)
        rr.italic = True
        rr.font.size = Pt(10)
        rr.font.color.rgb = RGBColor.from_string(MUTED)

        for b in bullets:
            pb = doc.add_paragraph(style='List Bullet')
            _no_space(pb, after=4, line=1.2)
            pb.paragraph_format.left_indent = Inches(0.25)
            pb.paragraph_format.first_line_indent = Inches(-0.15)
            rb = pb.add_run(b)
            rb.font.size = Pt(10.5)

    # --- Education ---
    _heading(doc, 'EDUCATION')
    p = doc.add_paragraph()
    _no_space(p, after=2)
    r = p.add_run(EDUCATION[0])
    r.bold = True
    r.font.size = Pt(10.5)
    tab = p.add_run(f'\t{EDUCATION[2]}')
    tab.font.size = Pt(9.5)
    tab.font.color.rgb = RGBColor.from_string(MUTED)
    p.paragraph_format.tab_stops.add_tab_stop(Inches(7.15), 2)
    p2 = doc.add_paragraph()
    _no_space(p2, after=2)
    r2 = p2.add_run(EDUCATION[1])
    r2.font.size = Pt(10)
    r2.font.color.rgb = RGBColor.from_string(MUTED)

    doc.save(path)


# ============================================================================
# PDF BUILDER
# ============================================================================
class HRule(Flowable):
    """Thin horizontal rule used under section headings."""
    def __init__(self, width, thickness=0.6, color=RULE):
        super().__init__()
        self.width = width
        self.thickness = thickness
        self.color = HexColor('#' + color)

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)


def build_pdf(path):
    page_w, _ = letter
    left = right = 0.7 * inch
    content_w = page_w - left - right

    styles = {
        'name': ParagraphStyle(
            'name', fontName='Helvetica-Bold', fontSize=23, leading=27,
            alignment=TA_CENTER, textColor=HexColor('#' + ACCENT), spaceAfter=5),
        'tagline': ParagraphStyle(
            'tagline', fontName='Helvetica', fontSize=9.5, leading=13,
            alignment=TA_CENTER, textColor=HexColor('#' + MUTED), spaceAfter=5),
        'contact': ParagraphStyle(
            'contact', fontName='Helvetica', fontSize=9, leading=12,
            alignment=TA_CENTER, textColor=HexColor('#' + MUTED), spaceAfter=3),
        'heading': ParagraphStyle(
            'heading', fontName='Helvetica-Bold', fontSize=11.5, leading=14,
            textColor=HexColor('#' + ACCENT), spaceBefore=14, spaceAfter=3),
        'summary': ParagraphStyle(
            'summary', fontName='Helvetica', fontSize=10, leading=14.5,
            textColor=HexColor('#' + INK), alignment=TA_LEFT, spaceAfter=2),
        'skill': ParagraphStyle(
            'skill', fontName='Helvetica', fontSize=10, leading=14,
            textColor=HexColor('#' + INK), spaceAfter=3),
        'company': ParagraphStyle(
            'company', fontName='Helvetica-Bold', fontSize=11, leading=14,
            textColor=HexColor('#' + INK)),
        'dates': ParagraphStyle(
            'dates', fontName='Helvetica', fontSize=9.5, leading=14,
            textColor=HexColor('#' + MUTED), alignment=2),  # right
        'role': ParagraphStyle(
            'role', fontName='Helvetica-Oblique', fontSize=10, leading=13,
            textColor=HexColor('#' + MUTED), spaceAfter=3),
        'bullet': ParagraphStyle(
            'bullet', fontName='Helvetica', fontSize=10, leading=13.5,
            textColor=HexColor('#' + INK), leftIndent=15, firstLineIndent=-12,
            spaceAfter=4, bulletIndent=3),
    }

    def company_row(company, dates):
        """Two-column row: company left (bold), dates right (muted)."""
        t = Table(
            [[Paragraph(company, styles['company']),
              Paragraph(dates, styles['dates'])]],
            colWidths=[content_w * 0.62, content_w * 0.38])
        t.setStyle(TableStyle([
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ]))
        return t

    def heading(text):
        return [Paragraph(text, styles['heading']), HRule(content_w), Spacer(1, 6)]

    doc = SimpleDocTemplate(
        str(path), pagesize=letter,
        leftMargin=left, rightMargin=right,
        topMargin=0.55 * inch, bottomMargin=0.55 * inch,
        title='Priyadharshini Arumugam — Resume',
        author='Priyadharshini Arumugam')

    F = []
    F.append(Paragraph(NAME, styles['name']))
    F.append(Paragraph(TAGLINE, styles['tagline']))
    F.append(Paragraph(
        f'{LOCATION} &nbsp;|&nbsp; {PHONE} &nbsp;|&nbsp; {EMAIL} &nbsp;|&nbsp; {LINKEDIN}',
        styles['contact']))

    F += heading('PROFESSIONAL SUMMARY')
    F.append(Paragraph(SUMMARY, styles['summary']))

    F += heading('TECHNICAL SKILLS')
    for label, items in SKILLS:
        F.append(Paragraph(f'<b>{label}:</b>&nbsp; {items}', styles['skill']))

    def entry(company, role, dates, bullets, keep=True):
        """Company header + role + first bullet; kept together to avoid orphaning."""
        head = [
            company_row(company, dates),
            Paragraph(role, styles['role']),
            Paragraph(f'<bullet>&bull;</bullet>{bullets[0]}', styles['bullet']),
        ]
        F.append(KeepTogether(head) if keep else head[0])
        if not keep:
            F.extend(head[1:])
        for b in bullets[1:]:
            F.append(Paragraph(f'<bullet>&bull;</bullet>{b}', styles['bullet']))

    F += heading('PROFESSIONAL EXPERIENCE')
    for company, role, dates, bullets in EXPERIENCE:
        entry(company, role, dates, bullets)

    F += heading('REMOTE INTERNSHIP')
    for company, role, dates, bullets in INTERNSHIP:
        entry(company, role, dates, bullets, keep=False)

    edu_inst = EDUCATION[1].replace('&', '&amp;')
    edu_style = ParagraphStyle(
        'edu', fontName='Helvetica', fontSize=9.5, leading=12.5,
        textColor=HexColor('#' + INK))
    F += heading('EDUCATION')
    F.append(Paragraph(
        f'<b>{EDUCATION[0]}</b> &nbsp;—&nbsp; {edu_inst}, Puducherry '
        f'&nbsp;<font color="#{MUTED}" size="9">({EDUCATION[2]})</font>',
        edu_style))

    doc.build(F)


# ============================================================================
# MAIN
# ============================================================================
if __name__ == '__main__':
    docx_path = OUT_DIR / 'Priyadharshini_Arumugam_Resume_Concise.docx'
    pdf_path = OUT_DIR / 'Priyadharshini_Arumugam_Resume_Concise.pdf'

    build_docx(docx_path)
    build_pdf(pdf_path)

    print('Generated:')
    print(' ', docx_path)
    print(' ', pdf_path)
