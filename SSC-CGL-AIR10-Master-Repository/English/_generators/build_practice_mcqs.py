# -*- coding: utf-8 -*-
"""Merge the English MCQ practice banks into one 'English Practice MCQs' PDF.

Each source file: ## EASY/MEDIUM/HARD/SSC PYQ sections, with
  **Qn.** question text
  (a) .. (b) .. (c) .. (d) ..
  **Answer: (x) ...**
  *Solution: ...*
RC file additionally has ### Passage N blocks.

Run:  python English/_generators/build_practice_mcqs.py
"""
import re, sys, html
from pathlib import Path

ENG = Path(__file__).resolve().parent.parent   # .../English
REPO = ENG.parent
sys.path.insert(0, str(REPO))
from html_to_pdf import html_to_pdf

FILES = [
    ("01_Vocabulary_Synonyms_Antonyms.md", "Synonyms & Antonyms"),
    ("03_One_Word_Substitution.md",        "One-Word Substitution"),
    ("04_Spelling_Spotting.md",            "Spelling Spotting"),
    ("05_Error_Detection.md",              "Error Detection"),
    ("06_Fill_Blanks_Cloze.md",            "Fill in the Blanks / Cloze"),
    ("07_Sentence_Improvement.md",         "Sentence Improvement"),
    ("08_Voice_Narration.md",              "Voice & Narration"),
    ("09_Reading_Comprehension.md",        "Reading Comprehension"),
]

def esc(s): return html.escape(s or "", quote=False)

def inline(t):
    t = esc(t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\*(?!\s)(.+?)(?<!\s)\*", r"<em>\1</em>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    return t

Q = re.compile(r"^\*\*Q\d+\.\*\*\s*(.*)$")
ANS = re.compile(r"^\*\*Answer:\s*(.*?)\*\*\s*$")
SOL = re.compile(r"^\*(?:Solution|Explanation):\*?\s*(.*?)\*?$")
OPT = re.compile(r"^\([a-d]\)")

def parse(path):
    """Return list of (section, [items]) where item is dict or ('passage', text)."""
    lines = path.read_text(encoding="utf-8").split("\n")
    sections = []
    cur_sec, items = None, []
    i = 0
    def flush():
        if cur_sec is not None:
            sections.append((cur_sec, items))
    while i < len(lines):
        ln = lines[i].rstrip()
        s = ln.strip()
        h2 = re.match(r"^##\s+(.*)$", s)
        h3 = re.match(r"^###\s+(.*)$", s)
        if h2:
            title = h2.group(1)
            if title in ("Key Rules",) or title.startswith("🔑"):
                # skip these sections
                flush(); cur_sec = None; items = []; i += 1; continue
            flush()
            cur_sec = title; items = []; i += 1; continue
        if h3 and cur_sec is not None:
            t = h3.group(1)
            if t.startswith("🔑"):
                i += 1; continue
            items.append({"kind": "sub", "text": t}); i += 1; continue
        mq = Q.match(s)
        if mq and cur_sec is not None:
            q = {"kind": "q", "q": mq.group(1), "opts": [], "ans": "", "sol": ""}
            i += 1
            # gather until next Q/heading; capture options, answer, solution, passage lines
            buf_passage = []
            while i < len(lines):
                s2 = lines[i].strip()
                if Q.match(s2) or re.match(r"^#{2,3}\s", s2): break
                if OPT.match(s2):
                    # split combined "(a) x  (b) y" into parts
                    parts = re.findall(r"\([a-d]\)\s*[^()]*", s2)
                    q["opts"].extend(p.strip() for p in parts)
                elif ANS.match(s2):
                    q["ans"] = ANS.match(s2).group(1)
                elif SOL.match(s2):
                    q["sol"] = SOL.match(s2).group(1)
                i += 1
            items.append(q); continue
        # passage / intro paragraph inside a section (RC): keep non-empty prose
        if cur_sec is not None and s and not s.startswith(">") and not s.startswith("**Answer") \
           and not OPT.match(s) and not s.startswith("*Solution") and not s.startswith("["):
            # treat as passage/context line
            items.append({"kind": "prose", "text": s}); i += 1; continue
        i += 1
    flush()
    return sections

# build HTML
blocks = []
total_q = 0
for fname, title in FILES:
    secs = parse(ENG / fname)
    qcount = sum(1 for _, items in secs for it in items if it.get("kind")=="q")
    total_q += qcount
    blocks.append(f'<h2>{esc(title)} <span class="qc">{qcount} Q</span></h2>')
    for sec, items in secs:
        if not any(it.get("kind")=="q" for it in items):
            continue
        blocks.append(f'<h3>{esc(sec)}</h3>')
        for it in items:
            k = it.get("kind")
            if k == "sub":
                blocks.append(f'<p class="sub2">{inline(it["text"])}</p>')
            elif k == "prose":
                blocks.append(f'<p class="passage">{inline(it["text"])}</p>')
            elif k == "q":
                opts = "".join(f'<span class="opt">{inline(o)}</span>' for o in it["opts"])
                blocks.append(
                    '<div class="q">'
                    f'<div class="qt">{inline(it["q"])}</div>'
                    f'<div class="opts">{opts}</div>'
                    f'<div class="ans"><b>Answer:</b> {inline(it["ans"])}</div>'
                    + (f'<div class="sol"><b>Solution:</b> {inline(it["sol"])}</div>' if it["sol"] else "")
                    + '</div>'
                )
body = "\n".join(blocks)

doc = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SSC CGL — English Practice MCQs</title>
<style>
  :root{{ --ink:#1a1a1a; --blue:#0b5394; --teal:#134f5c; --good:#137333; --amber:#f1c232; --cream:#fff8e1; }}
  *{{ box-sizing:border-box; }}
  body{{ font-family:"Segoe UI",Arial,sans-serif; color:var(--ink); font-size:12px; line-height:1.5;
        max-width:900px; margin:0 auto; padding:0 8px; }}
  h1{{ font-size:23px; color:var(--blue); margin:6px 0 2px; }}
  .sub{{ color:#555; margin:2px 0 10px; font-size:12px; }}
  h2{{ font-size:17px; color:#fff; background:var(--blue); margin:22px 0 8px; padding:5px 12px;
      border-radius:4px; page-break-after:avoid; }}
  h2 .qc{{ float:right; font-size:12px; font-weight:normal; opacity:.85; }}
  h3{{ font-size:13px; color:var(--teal); margin:14px 0 6px; border-bottom:1px solid #cfe2f3;
      padding-bottom:2px; page-break-after:avoid; }}
  .sub2{{ font-weight:600; color:#134f5c; margin:8px 0 4px; }}
  .passage{{ background:#f4f8fc; border-left:3px solid #9fc0dd; padding:6px 10px; margin:6px 0;
            font-size:11.5px; color:#333; border-radius:0 3px 3px 0; }}
  .q{{ margin:7px 0 9px; padding:2px 0; page-break-inside:avoid; }}
  .qt{{ font-weight:600; }}
  .opts{{ margin:2px 0; }}
  .opt{{ display:inline-block; margin:1px 16px 1px 0; color:#333; }}
  .ans{{ color:var(--good); }}
  .ans b{{ color:var(--good); }}
  .sol{{ background:var(--cream); border-left:3px solid var(--amber); padding:3px 9px; margin-top:3px;
        font-size:11px; color:#555; border-radius:0 3px 3px 0; }}
  code{{ font-family:Consolas,monospace; background:#eef; padding:1px 4px; border-radius:3px; }}
  .foot{{ margin-top:22px; padding-top:8px; border-top:1px solid #ddd; font-size:10px; color:#777; text-align:center; }}
</style></head><body>
<h1>📝 SSC CGL — English Practice MCQs</h1>
<p class="sub"><b>{total_q} solved questions</b> across 9 topics — Synonyms/Antonyms, Idioms, One-Word Substitution, Spelling, Error Detection, Cloze, Sentence Improvement, Voice/Narration &amp; Reading Comprehension. Each question has the answer and a one-line solution.</p>
{body}
<p class="foot">SSC-CGL-AIR10-Master-Repository · English Practice MCQs · consolidated from the 01–09 solved question banks.</p>
</body></html>"""

out = ENG / "English-Practice-MCQs.html"
out.write_text(doc, encoding="utf-8")
print("total questions:", total_q, "| HTML bytes:", len(doc))
res = html_to_pdf(out, delete_html=False)
print("PDF:", res)
