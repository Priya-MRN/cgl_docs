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


def html_to_pdf(html_path, delete_html: bool = True, log=None):
    """Convert one HTML file to a same-named PDF. See module docstring."""
    html_path = Path(html_path)
    pdf_path = html_path.with_suffix(".pdf")

    def _say(msg):
        (log or (lambda m: print(m)))(msg)

    if not html_path.exists():
        _say(f"html_to_pdf: source missing, skipped: {html_path.name}")
        return None

    browser = _find_browser()
    if not browser:
        _say("html_to_pdf: no Chrome/Edge found; leaving HTML in place")
        return None

    uri = html_path.resolve().as_uri()
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
