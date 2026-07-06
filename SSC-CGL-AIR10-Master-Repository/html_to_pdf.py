"""
Shared HTML->PDF helper for the daily study-material scripts.

Prints a styled HTML file to PDF via headless Chrome / Edge (whichever is
installed), so the committed, mobile-friendly artifact is always a PDF.
GitHub renders PDFs reliably on phones; local HTML does not.

Usage from a daily script:
    from html_to_pdf import html_to_pdf
    html_to_pdf(html_path, delete_html=True)   # stateless scripts
    html_to_pdf(html_path, delete_html=False)  # stateful scripts (keep+gitignore)

Returns the Path to the PDF on success, or None on failure (never raises;
a failed conversion must not break the daily pipeline).
"""
from __future__ import annotations

import re
import sys
import time
import shutil
import tempfile
import subprocess
from pathlib import Path

# Common install locations on Windows; first hit wins.
_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]


def _find_browser() -> str | None:
    for p in _CANDIDATES:
        if Path(p).exists():
            return p
    for name in ("chrome", "chrome.exe", "msedge", "msedge.exe"):
        found = shutil.which(name)
        if found:
            return found
    return None


# Print-safety net injected into EVERY document just before rendering.
#
# Chrome's --print-to-pdf does NOT scale overflowing content to fit the page --
# it silently CLIPS anything wider than the printable area (and drops the
# off-page glyphs entirely, so the text is unrecoverable from the PDF). A wide
# multi-column table therefore loses its rightmost column(s) with no warning.
#
# This stylesheet makes tables shrink-to-fit the page instead of overflowing:
#   * table-layout:fixed + width:100%  -> columns share the page width, never
#     grow past it based on content;
#   * overflow-wrap/word-break on cells -> long words and unbroken strings wrap
#     rather than forcing the table wider;
#   * max-width:100% on the page body   -> a doc-level max-width (e.g. 1000px)
#     can't push content past a narrower printable area.
# It is deliberately generic and !important so it wins over each doc's own CSS
# without needing to edit the (often generated or unavailable) source.
_SAFETY_STYLE_BODY = """
@media print {
  html, body { max-width: 100% !important; }
  /* Neutralise a fixed min-width on tables (e.g. min-width:1050px) and any
     overflow-x scroll wrapper — both let a table stay wider than the page, so
     Chrome clips the overflow in print. Force everything to shrink-to-fit. */
  table { table-layout: fixed !important; width: 100% !important;
          max-width: 100% !important; min-width: 0 !important; }
  div, section, figure { overflow-x: visible !important; }
  th, td { overflow-wrap: anywhere !important; word-break: break-word !important;
           min-width: 0 !important; white-space: normal !important; }
  pre, code { white-space: pre-wrap !important; overflow-wrap: anywhere !important; }
  img, svg { max-width: 100% !important; height: auto !important; }
}
"""

# A doc with a genuinely wide table (many columns) reads better in landscape
# than squeezed shrink-to-fit into portrait. When we pick landscape we set the
# @page size so Chrome lays the whole page out wider before the same shrink-to-
# fit net applies -- so columns get real room instead of being crushed.
_LANDSCAPE_PAGE = "@page { size: landscape; }\n"

_SAFETY_MARKER = 'id="pdf-print-safety"'

# At or above this many columns in any single table, auto mode flips the page to
# landscape. Four-column tables fit portrait comfortably; five start to crowd.
_LANDSCAPE_COL_THRESHOLD = 5


def _max_table_cols(source: str) -> int:
    """Largest number of cells in any single table row across the document.

    A cheap regex scan (no real HTML parse): count <th>/<td> opening tags within
    each <tr>...</tr> and return the maximum. Good enough to decide orientation.
    """
    best = 0
    for row in re.findall(r"<tr\b[^>]*>(.*?)</tr>", source, re.I | re.S):
        cells = len(re.findall(r"<t[hd]\b", row, re.I))
        best = max(best, cells)
    return best


def _build_safety_css(source: str, orientation: str) -> tuple[str, bool]:
    """Return (style-block, landscape?) for the given orientation policy.

    orientation: "auto" -> landscape iff the widest table is wide enough;
                 "landscape"/"portrait" -> forced.
    """
    if orientation == "landscape":
        landscape = True
    elif orientation == "portrait":
        landscape = False
    else:  # auto
        landscape = _max_table_cols(source) >= _LANDSCAPE_COL_THRESHOLD
    page = _LANDSCAPE_PAGE if landscape else ""
    block = f'<style id="pdf-print-safety">\n{page}{_SAFETY_STYLE_BODY}</style>\n'
    return block, landscape


def _inject_safety_css(source: str, orientation: str = "auto") -> tuple[str, bool]:
    """Return (html-with-safety-stylesheet, landscape?) -- idempotent.

    Prefer inserting just before </head>; fall back to before <body>, then to
    the very top so even a fragment (no <head>/<body>) still gets it.
    """
    if _SAFETY_MARKER in source:
        return source, "size: landscape" in source
    block, landscape = _build_safety_css(source, orientation)
    for anchor in ("</head>", "<body", "<html"):
        idx = source.lower().find(anchor)
        if idx != -1:
            if anchor == "</head>":
                return source[:idx] + block + source[idx:], landscape
            end = source.find(">", idx)
            if end != -1:
                return source[:end + 1] + block + source[end + 1:], landscape
    return block + source, landscape


def html_to_pdf(html_path, delete_html: bool = True, log=None,
                orientation: str = "auto"):
    """Convert one HTML file to a same-named PDF. See module docstring.

    orientation: "auto" (default) prints landscape when the widest table has
    >= 5 columns, else portrait; pass "landscape"/"portrait" to force it.
    """
    html_path = Path(html_path)
    # Absolute output path: Chrome's --print-to-pdf resolves a RELATIVE path
    # against its own working directory, not ours, and fails with "cannot find
    # the path specified" when called with a relative html_path.
    pdf_path = html_path.with_suffix(".pdf").resolve()

    def _say(msg):
        (log or (lambda m: print(m)))(msg)

    if not html_path.exists():
        _say(f"html_to_pdf: source missing, skipped: {html_path.name}")
        return None

    browser = _find_browser()
    if not browser:
        _say("html_to_pdf: no Chrome/Edge found; leaving HTML in place")
        return None

    # Render from a temp copy with the print-safety CSS injected, so wide tables
    # shrink-to-fit instead of being clipped. Rendering a copy keeps the on-disk
    # HTML byte-for-byte intact -- the stateful daily scripts patch that file in
    # place each run and must not pick up our injected <style>.
    try:
        original = html_path.read_text(encoding="utf-8")
        safe_html, landscape = _inject_safety_css(original, orientation)
    except OSError as exc:
        _say(f"html_to_pdf: could not read {html_path.name} ({exc}); HTML kept")
        return None
    if landscape:
        _say(f"html_to_pdf: wide table detected -> landscape for {html_path.name}")

    render_path = html_path.with_name(f".{html_path.stem}.pdfsafe.html")
    try:
        render_path.write_text(safe_html, encoding="utf-8")
    except OSError as exc:
        _say(f"html_to_pdf: could not stage safe copy ({exc}); rendering original")
        render_path = html_path

    uri = render_path.resolve().as_uri()
    profile = Path(tempfile.gettempdir()) / f"chrome-pdf-{html_path.stem}"
    if profile.exists():
        shutil.rmtree(profile, ignore_errors=True)

    try:
        subprocess.run(
            [
                browser,
                "--headless=new",
                "--disable-gpu",
                "--no-pdf-header-footer",
                "--virtual-time-budget=8000",
                f"--user-data-dir={profile}",
                f"--print-to-pdf={pdf_path}",
                uri,
            ],
            timeout=60,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        _say(f"html_to_pdf: browser run failed ({exc}); HTML kept")
        return None
    finally:
        shutil.rmtree(profile, ignore_errors=True)
        if render_path != html_path:
            render_path.unlink(missing_ok=True)

    # Validate output before we consider deleting the source.
    time.sleep(0.2)
    ok = pdf_path.exists() and pdf_path.stat().st_size > 1000
    if ok:
        try:
            with open(pdf_path, "rb") as fh:
                ok = fh.read(4) == b"%PDF"
        except OSError:
            ok = False

    if not ok:
        _say(f"html_to_pdf: PDF invalid/empty for {html_path.name}; HTML kept")
        return None

    _say(f"html_to_pdf: wrote {pdf_path.name} ({pdf_path.stat().st_size} bytes)")

    if delete_html:
        try:
            html_path.unlink()
            _say(f"html_to_pdf: removed {html_path.name}")
        except OSError as exc:
            _say(f"html_to_pdf: could not delete {html_path.name} ({exc})")

    return pdf_path


if __name__ == "__main__":
    # CLI: python html_to_pdf.py <file.html> [--keep]
    if len(sys.argv) < 2:
        print("usage: python html_to_pdf.py <file.html> [--keep]")
        raise SystemExit(2)
    keep = "--keep" in sys.argv[2:]
    result = html_to_pdf(sys.argv[1], delete_html=not keep)
    raise SystemExit(0 if result else 1)
