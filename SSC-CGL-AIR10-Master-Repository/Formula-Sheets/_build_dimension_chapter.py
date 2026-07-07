# -*- coding: utf-8 -*-
"""Build the Dimension-Change-Relations PDF.

Reads the marker source (Dimension-Change-Relations.md), replaces each
`<!-- FIG:key -->` line with the inline SVG produced by _svg_figures.FIGS,
writes a resolved temp .md, then renders it to the committed PDF via
md_to_pdf. Source .md stays gitignored (PDF-only policy); the resolved
temp file is deleted after rendering.

Usage:  python Formula-Sheets/_build_dimension_chapter.py
"""
import re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))     # _svg_figures
sys.path.insert(0, str(REPO))     # md_to_pdf

from _svg_figures import FIGS
import md_to_pdf

SRC = HERE / "Dimension-Change-Relations.md"
MARKER = re.compile(r"^<!--\s*FIG:([a-z]+)\s*-->\s*$")


def resolve(text):
    out, missing = [], []
    for line in text.split("\n"):
        m = MARKER.match(line)
        if m:
            key = m.group(1)
            fn = FIGS.get(key)
            if fn is None:
                missing.append(key)
                out.append(line)          # leave marker visible if unknown
            else:
                out.append(fn())
        else:
            out.append(line)
    if missing:
        print("WARNING unknown FIG keys:", ", ".join(missing))
    return "\n".join(out)


def main():
    resolved = resolve(SRC.read_text(encoding="utf-8"))
    tmp = HERE / "_Dimension-Change-Relations.resolved.md"
    tmp.write_text(resolved, encoding="utf-8")
    try:
        # Render, then move the PDF onto the canonical name.
        pdf = md_to_pdf.convert(tmp)
        if pdf:
            final = SRC.with_suffix(".pdf")
            Path(pdf).replace(final)
            print("FINAL PDF:", final)
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
