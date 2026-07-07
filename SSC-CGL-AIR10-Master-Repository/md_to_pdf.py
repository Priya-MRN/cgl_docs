# -*- coding: utf-8 -*-
"""Minimal Markdown -> styled HTML -> PDF for consolidated study files.

Handles: #..###### headings, tables, **bold**, *italic*, - lists, 1. lists,
> blockquotes, --- rules, [text](link), inline `code`. Good enough for our docs.

PDF-only policy: keep the .md as the local editable source (gitignored) and
commit only the rendered PDF.

Usage:  python md_to_pdf.py <path-to-file.md>
"""
import re, sys, html
from pathlib import Path

REPO = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))
from html_to_pdf import html_to_pdf

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
    t = re.sub(r"\*(?!\s)(.+?)(?<!\s)\*", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    return t

def render(md):
    lines = md.split("\n")
    out, i = [], 0
    in_ul = in_ol = False
    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul: out.append("</ul>"); in_ul = False
        if in_ol: out.append("</ol>"); in_ol = False
    while i < len(lines):
        ln = lines[i].rstrip("\n")
        s = ln.strip()
        # raw inline SVG block: pass through verbatim, centred (labelled figures)
        if s.startswith("<svg"):
            close_lists()
            buf = []
            while i < len(lines):
                buf.append(lines[i])
                if "</svg>" in lines[i]:
                    i += 1
                    break
                i += 1
            out.append('<div class="figure">' + "\n".join(buf) + "</div>")
            continue
        # fenced code block ``` ... ``` -> <pre> (preserves ASCII-art alignment)
        if s.startswith("```"):
            close_lists()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(html.escape(lines[i].rstrip("\n"), quote=False))
                i += 1
            i += 1  # skip closing fence
            out.append("<pre>" + "\n".join(buf) + "</pre>")
            continue
        # table block
        if "|" in ln and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]+$", lines[i+1]):
            close_lists()
            header = [c.strip() for c in ln.strip().strip("|").split("|")]
            out.append('<table><thead><tr>' + "".join(f"<th>{inline(c)}</th>" for c in header) + "</tr></thead><tbody>")
            i += 2
            while i < len(lines) and "|" in lines[i]:
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue
        if not s:
            close_lists(); out.append(""); i += 1; continue
        m = re.match(r"^(#{1,6})\s+(.*)$", s)
        if m:
            close_lists(); lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>"); i += 1; continue
        if s in ("---", "***", "___"):
            close_lists(); out.append("<hr>"); i += 1; continue
        if s.startswith(">"):
            close_lists(); out.append(f"<blockquote>{inline(s.lstrip('> ').strip())}</blockquote>"); i += 1; continue
        m = re.match(r"^(\d+)\.\s+(.*)$", s)
        if m:
            if not in_ol: close_lists(); out.append("<ol>"); in_ol = True
            out.append(f"<li>{inline(m.group(2))}</li>"); i += 1; continue
        if s.startswith("- ") or s.startswith("* "):
            if not in_ul: close_lists(); out.append("<ul>"); in_ul = True
            out.append(f"<li>{inline(s[2:])}</li>"); i += 1; continue
        close_lists(); out.append(f"<p>{inline(s)}</p>"); i += 1
    close_lists()
    return "\n".join(out)

CSS = """
<style>
@page { margin: 14mm 12mm; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 12px; line-height: 1.5;
       color: #1a1a1a; max-width: 900px; margin: 0 auto; padding: 0 6px; }
h1 { font-size: 24px; color: #0b5394; border-bottom: 3px solid #0b5394; padding-bottom: 6px; }
h2 { font-size: 18px; color: #0b5394; margin-top: 22px; border-bottom: 1px solid #cfe2f3; padding-bottom: 3px; page-break-after: avoid; }
h3 { font-size: 14px; color: #134f5c; margin-top: 14px; page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; table-layout: fixed; margin: 8px 0; font-size: 11px; page-break-inside: avoid; }
th, td { border: 1px solid #b7c9d9; padding: 4px 7px; text-align: left; vertical-align: top;
         overflow-wrap: anywhere; word-break: break-word; }
th { background: #0b5394; color: #fff; }
tr:nth-child(even) td { background: #f1f6fb; }
blockquote { background: #fff8e1; border-left: 4px solid #f1c232; margin: 8px 0; padding: 6px 12px; color: #444; }
pre { background: #f7f9fc; border: 1px solid #cfe2f3; border-left: 4px solid #6fa8dc; border-radius: 4px;
      padding: 8px 12px; margin: 8px 0; font-family: Consolas, 'Courier New', monospace; font-size: 11px;
      line-height: 1.35; white-space: pre; overflow-x: auto; color: #0b3a5c; page-break-inside: avoid; }
.figure { text-align: center; margin: 10px 0; page-break-inside: avoid; }
.figure svg { max-width: 100%; height: auto; }
code { background: #eef; padding: 1px 4px; border-radius: 3px; font-family: Consolas, monospace; font-size: 11px; }
a { color: #1155cc; text-decoration: none; }
ul, ol { margin: 6px 0 6px 4px; padding-left: 20px; }
li { margin: 2px 0; }
strong { color: #073763; }
hr { border: none; border-top: 1px solid #ddd; margin: 14px 0; }
</style>
"""

def convert(src_path):
    """Render a Markdown file to a sibling PDF; returns the PDF path (or None)."""
    src = Path(src_path).resolve()
    html_out = src.with_suffix(".html")
    body = render(src.read_text(encoding="utf-8"))
    title = src.stem.replace("-", " ")
    doc = (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
           f"<title>{title}</title>{CSS}</head><body>{body}</body></html>")
    html_out.write_text(doc, encoding="utf-8")
    print("HTML written:", html_out.name, len(doc), "bytes")
    res = html_to_pdf(html_out, delete_html=True)
    print("PDF:", res)
    return res


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python md_to_pdf.py <file.md>")
        raise SystemExit(2)
    convert(sys.argv[1])
