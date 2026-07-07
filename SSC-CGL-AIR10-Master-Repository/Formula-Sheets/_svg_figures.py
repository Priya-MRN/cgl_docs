# -*- coding: utf-8 -*-
"""Colour-coded before->after figures for Dimension-Change-Relations.

Each function returns a self-contained inline <svg> string (no external assets)
that md_to_pdf.py passes through verbatim and centres. Palette:

    BEFORE  outline #0b5394 (blue)   fill #e8f0fe
    AFTER   outline #38761d (green)  fill #e6f4ea
    CHANGE  arrows / highlighted dim #e69138 (orange)
    dims / centre marks              #134f5c

Run `python _svg_figures.py` to (re)write svg_snippets.md — a lookup of
`<!-- FIG:key -->` blocks the build script splices into the chapter.
"""
from pathlib import Path

BLUE, BLUE_F = "#0b5394", "#e8f0fe"
GREEN, GREEN_F = "#38761d", "#e6f4ea"
ORANGE = "#e69138"
DIM = "#134f5c"
FONT = 'font-family="Segoe UI, Arial, sans-serif"'

# Shared arrowhead defs (orange change-arrow + blue/green dim ticks).
DEFS = f'''
  <defs>
    <marker id="ao" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="{ORANGE}"/></marker>
    <marker id="db" markerWidth="8" markerHeight="8" refX="4" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="{DIM}"/></marker>
    <marker id="ds" markerWidth="8" markerHeight="8" refX="2" refY="3" orient="auto">
      <path d="M6,0 L0,3 L6,6 Z" fill="{DIM}"/></marker>
  </defs>'''


def _svg(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'{FONT} font-size="13" width="{w}">{body}{DEFS}</svg>')


def _arrow(x1, x2, y, label):
    """Orange horizontal change-arrow between the two panels."""
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{ORANGE}" '
            f'stroke-width="2.5" marker-end="url(#ao)"/>'
            f'<text x="{(x1+x2)/2}" y="{y-8}" text-anchor="middle" '
            f'fill="{ORANGE}" font-weight="bold">{label}</text>')


def _cap(x, y, text, colour):
    return f'<text x="{x}" y="{y}" text-anchor="middle" fill="{colour}">{text}</text>'


def _dimline(x1, y1, x2, y2, label, lx, ly):
    """Double-headed dimension line with a label."""
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{DIM}" '
            f'stroke-width="1" marker-start="url(#ds)" marker-end="url(#db)"/>'
            f'<text x="{lx}" y="{ly}" text-anchor="middle" fill="{DIM}" '
            f'font-size="12">{label}</text>')


# ---- 2D ---------------------------------------------------------------------

def square():
    b = (f'<rect x="30" y="70" width="70" height="70" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + _cap(65, 62, "a", BLUE) + _cap(65, 165, "Before", "#555")
         + f'<line x1="30" y1="140" x2="100" y2="70" stroke="{ORANGE}" stroke-width="1" stroke-dasharray="3 2"/>'
         + _cap(52, 100, "d", ORANGE))
    mid = _arrow(140, 200, 105, "Side ×2")
    a = (f'<rect x="240" y="35" width="140" height="140" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + _cap(310, 27, "2a", GREEN) + _cap(310, 192, "Area ×4 · P ×2 · d ×2", "#555"))
    return _svg(410, 205, b + mid + a)


def rectangle():
    b = (f'<rect x="25" y="80" width="90" height="55" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + _cap(70, 74, "l", BLUE) + _cap(128, 112, "b", BLUE) + _cap(70, 160, "Before", "#555"))
    mid = _arrow(140, 205, 105, "l×2, b×½")
    a = (f'<rect x="235" y="92" width="160" height="28" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + _cap(315, 86, "2l", GREEN) + _cap(408, 110, "b/2", GREEN)
         + _cap(315, 160, "Area unchanged (×1)", "#555"))
    return _svg(420, 175, b + mid + a)


def triangle():
    b = (f'<polygon points="30,140 110,140 70,70" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<line x1="70" y1="70" x2="70" y2="140" stroke="{DIM}" stroke-width="1" stroke-dasharray="3 2"/>'
         + _cap(82, 108, "h", DIM) + _cap(70, 158, "b", BLUE) + _cap(70, 175, "Before", "#555"))
    mid = _arrow(140, 200, 110, "b×2, h×3")
    a = (f'<polygon points="235,175 395,175 315,20" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<line x1="315" y1="20" x2="315" y2="175" stroke="{DIM}" stroke-width="1" stroke-dasharray="3 2"/>'
         + _cap(315, 192, "2b", GREEN) + _cap(330, 100, "3h", DIM)
         + _cap(315, 15, "Area ×6", "#555"))
    return _svg(410, 205, b + mid + a)


def equilateral():
    b = (f'<polygon points="30,140 110,140 70,71" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + _cap(70, 158, "a", BLUE) + _cap(70, 175, "Before", "#555"))
    mid = _arrow(140, 200, 110, "Side ×2")
    a = (f'<polygon points="235,175 395,175 315,37" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + _cap(315, 192, "2a", GREEN) + _cap(315, 30, "Area ×4 · P ×2", "#555"))
    return _svg(410, 205, b + mid + a)


def circle():
    b = (f'<circle cx="75" cy="105" r="40" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<circle cx="75" cy="105" r="2.5" fill="{DIM}"/>'
         + f'<line x1="75" y1="105" x2="115" y2="105" stroke="{DIM}" stroke-width="1.2"/>'
         + _cap(96, 100, "r", DIM) + _cap(75, 168, "Before", "#555"))
    mid = _arrow(140, 200, 105, "Radius ×2")
    a = (f'<circle cx="305" cy="105" r="80" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<circle cx="305" cy="105" r="2.5" fill="{DIM}"/>'
         + f'<line x1="305" y1="105" x2="385" y2="105" stroke="{GREEN}" stroke-width="1.4"/>'
         + _cap(345, 100, "2r", GREEN) + _cap(305, 200, "Area ×4 · C ×2", "#555"))
    return _svg(400, 205, b + mid + a)


def semicircle():
    b = (f'<path d="M35,120 A40,40 0 0 1 115,120 Z" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + _cap(75, 100, "r", DIM) + _cap(75, 150, "Before", "#555"))
    mid = _arrow(140, 200, 100, "Radius ×2")
    a = (f'<path d="M225,160 A80,80 0 0 1 385,160 Z" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + _cap(305, 100, "2r", GREEN) + _cap(305, 185, "Area ×4 · P ×2", "#555")
         + f'<text x="305" y="177" text-anchor="middle" fill="{ORANGE}" font-size="11">P = πr + 2r</text>')
    return _svg(410, 195, b + mid + a)


def sector():
    b = (f'<path d="M55,130 L120,130 A65,65 0 0 0 101,84 Z" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<circle cx="55" cy="130" r="2.5" fill="{DIM}"/>' + _cap(88, 124, "r", DIM)
         + _cap(66, 122, "θ", ORANGE) + _cap(85, 155, "Before", "#555"))
    mid = _arrow(150, 210, 105, "r×2 (θ same)")
    a = (f'<path d="M240,160 L370,160 A130,130 0 0 0 332,68 Z" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<circle cx="240" cy="160" r="2.5" fill="{DIM}"/>' + _cap(305, 152, "2r", GREEN)
         + _cap(305, 185, "Area ×4 · Arc ×2", "#555"))
    return _svg(400, 195, b + mid + a)


def rhombus():
    b = (f'<polygon points="70,65 110,105 70,145 30,105" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<line x1="70" y1="65" x2="70" y2="145" stroke="{DIM}" stroke-dasharray="3 2"/>'
         + f'<line x1="30" y1="105" x2="110" y2="105" stroke="{DIM}" stroke-dasharray="3 2"/>'
         + _cap(82, 88, "d₁", DIM) + _cap(45, 100, "d₂", DIM) + _cap(70, 165, "Before", "#555"))
    mid = _arrow(140, 200, 105, "Both d ×2")
    a = (f'<polygon points="305,25 385,105 305,185 225,105" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<line x1="305" y1="25" x2="305" y2="185" stroke="{GREEN}" stroke-dasharray="3 2"/>'
         + f'<line x1="225" y1="105" x2="385" y2="105" stroke="{GREEN}" stroke-dasharray="3 2"/>'
         + _cap(320, 60, "2d₁", GREEN) + _cap(255, 100, "2d₂", GREEN)
         + _cap(305, 200, "Area ×4", "#555"))
    return _svg(400, 205, b + mid + a)


def parallelogram():
    b = (f'<polygon points="35,140 105,140 90,80 20,80" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<line x1="90" y1="80" x2="90" y2="140" stroke="{DIM}" stroke-dasharray="3 2"/>'
         + _cap(100, 112, "h", DIM) + _cap(63, 158, "b", BLUE) + _cap(65, 175, "Before", "#555"))
    mid = _arrow(140, 205, 108, "b×2, h×½")
    a = (f'<polygon points="235,140 395,140 380,110 220,110" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + _cap(310, 158, "2b", GREEN) + _cap(310, 175, "Area unchanged", "#555"))
    return _svg(410, 185, b + mid + a)


def trapezium():
    b = (f'<polygon points="30,140 110,140 92,80 48,80" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + _cap(70, 74, "a", BLUE) + _cap(70, 158, "b", BLUE)
         + f'<line x1="70" y1="80" x2="70" y2="140" stroke="{DIM}" stroke-dasharray="3 2"/>'
         + _cap(80, 114, "h", DIM) + _cap(70, 175, "Before", "#555"))
    mid = _arrow(140, 200, 110, "Height ×2")
    a = (f'<polygon points="235,175 395,175 349,35 281,35" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + _cap(315, 29, "a", GREEN) + _cap(315, 192, "b", GREEN) + _cap(300, 110, "2h", GREEN)
         + _cap(315, 20, "Area ×2", "#555"))
    return _svg(410, 205, b + mid + a)


# ---- 3D ---------------------------------------------------------------------

def _cube(x, y, s, d, fill, stroke):
    """Isometric-ish cube: front face + top + right, top-left origin (x,y)."""
    f = (f'<rect x="{x}" y="{y+d}" width="{s}" height="{s}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    top = (f'<polygon points="{x},{y+d} {x+d},{y} {x+s+d},{y} {x+s},{y+d}" '
           f'fill="{fill}" stroke="{stroke}" stroke-width="2" opacity="0.85"/>')
    right = (f'<polygon points="{x+s},{y+d} {x+s+d},{y} {x+s+d},{y+s} {x+s},{y+s+d}" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="2" opacity="0.7"/>')
    return f + top + right


def cube():
    b = _cube(30, 55, 55, 22, BLUE_F, BLUE) + _cap(58, 150, "a", BLUE) + _cap(70, 172, "Before", "#555")
    mid = _arrow(150, 210, 105, "Side ×2")
    a = _cube(235, 30, 110, 40, GREEN_F, GREEN) + _cap(290, 195, "2a", GREEN) + _cap(320, 175, "V ×8 · SA ×4", "#555")
    return _svg(410, 200, b + mid + a)


def _cuboid(x, y, w, h, d, fill, stroke):
    f = f'<rect x="{x}" y="{y+d}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    top = (f'<polygon points="{x},{y+d} {x+d},{y} {x+w+d},{y} {x+w},{y+d}" '
           f'fill="{fill}" stroke="{stroke}" stroke-width="2" opacity="0.85"/>')
    right = (f'<polygon points="{x+w},{y+d} {x+w+d},{y} {x+w+d},{y+h} {x+w},{y+h+d}" '
             f'fill="{fill}" stroke="{stroke}" stroke-width="2" opacity="0.7"/>')
    return f + top + right


def cuboid():
    b = (_cuboid(30, 60, 70, 45, 22, BLUE_F, BLUE)
         + _cap(65, 138, "l", BLUE) + _cap(112, 92, "b", BLUE) + _cap(20, 92, "h", BLUE)
         + _cap(70, 168, "Before", "#555"))
    mid = _arrow(150, 215, 100, "l×2,b×3,h×½")
    a = (_cuboid(240, 70, 135, 25, 40, GREEN_F, GREEN)
         + _cap(305, 145, "2l", GREEN) + _cap(305, 190, "Volume ×3", "#555"))
    return _svg(420, 200, b + mid + a)


def _cylinder(cx, top, rx, h, ry, fill, stroke):
    body = (f'<path d="M{cx-rx},{top} L{cx-rx},{top+h} A{rx},{ry} 0 0 0 {cx+rx},{top+h} '
            f'L{cx+rx},{top} Z" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    topell = f'<ellipse cx="{cx}" cy="{top}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    return body + topell


def cylinder():
    b = (_cylinder(70, 55, 30, 80, 10, BLUE_F, BLUE)
         + f'<line x1="70" y1="55" x2="100" y2="55" stroke="{DIM}" stroke-width="1.2"/>' + _cap(86, 50, "r", DIM)
         + _cap(112, 100, "h", BLUE) + _cap(70, 168, "Before", "#555"))
    mid = _arrow(150, 210, 100, "r×2, h×½")
    a = (_cylinder(300, 80, 60, 40, 18, GREEN_F, GREEN)
         + f'<line x1="300" y1="80" x2="360" y2="80" stroke="{GREEN}" stroke-width="1.4"/>' + _cap(330, 74, "2r", GREEN)
         + _cap(300, 168, "V ×2 · CSA same", "#555"))
    return _svg(400, 200, b + mid + a)


def cone():
    b = (f'<path d="M70,60 L102,138 A32,10 0 0 1 38,138 Z" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<ellipse cx="70" cy="138" rx="32" ry="10" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<line x1="70" y1="60" x2="70" y2="138" stroke="{DIM}" stroke-dasharray="3 2"/>' + _cap(80, 105, "h", DIM)
         + f'<line x1="70" y1="138" x2="102" y2="138" stroke="{DIM}" stroke-width="1"/>' + _cap(88, 132, "r", DIM)
         + _cap(93, 92, "l", ORANGE) + _cap(70, 168, "Before", "#555"))
    mid = _arrow(150, 210, 100, "r×2, h×½")
    a = (f'<path d="M300,90 L364,150 A64,14 0 0 1 236,150 Z" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<ellipse cx="300" cy="150" rx="64" ry="14" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<line x1="300" y1="150" x2="364" y2="150" stroke="{GREEN}" stroke-width="1.2"/>' + _cap(332, 144, "2r", GREEN)
         + _cap(300, 178, "Volume ×2", "#555"))
    return _svg(400, 195, b + mid + a)


def sphere():
    b = (f'<circle cx="70" cy="100" r="40" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<ellipse cx="70" cy="100" rx="40" ry="12" fill="none" stroke="{BLUE}" stroke-width="1" stroke-dasharray="3 2"/>'
         + f'<line x1="70" y1="100" x2="110" y2="100" stroke="{DIM}" stroke-width="1.2"/>' + _cap(90, 95, "r", DIM)
         + _cap(70, 163, "Before", "#555"))
    mid = _arrow(140, 200, 100, "Radius ×2")
    a = (f'<circle cx="305" cy="100" r="80" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<ellipse cx="305" cy="100" rx="80" ry="22" fill="none" stroke="{GREEN}" stroke-width="1" stroke-dasharray="3 2"/>'
         + f'<line x1="305" y1="100" x2="385" y2="100" stroke="{GREEN}" stroke-width="1.4"/>' + _cap(345, 94, "2r", GREEN)
         + _cap(305, 195, "V ×8 · Surface ×4", "#555"))
    return _svg(400, 200, b + mid + a)


def hemisphere():
    b = (f'<path d="M30,120 A40,40 0 0 1 110,120 Z" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<ellipse cx="70" cy="120" rx="40" ry="10" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="1.5"/>'
         + _cap(90, 105, "r", DIM) + _cap(70, 150, "Before", "#555"))
    mid = _arrow(140, 200, 100, "Radius ×2")
    a = (f'<path d="M225,160 A80,80 0 0 1 385,160 Z" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<ellipse cx="305" cy="160" rx="80" ry="18" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="1.5"/>'
         + _cap(345, 130, "2r", GREEN) + _cap(305, 188, "V ×8 · SA ×4", "#555"))
    return _svg(410, 198, b + mid + a)


def frustum():
    b = (f'<path d="M45,70 L95,70 L110,140 A35,10 0 0 1 30,140 Z" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<ellipse cx="70" cy="70" rx="25" ry="8" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + _cap(70, 64, "r", DIM) + _cap(70, 158, "R", DIM) + _cap(118, 108, "l", ORANGE)
         + _cap(70, 176, "Before", "#555"))
    mid = _arrow(150, 210, 105, "All ×2")
    a = (f'<path d="M255,30 L355,30 L385,170 A65,16 0 0 1 225,170 Z" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<ellipse cx="305" cy="30" rx="50" ry="12" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + _cap(305, 24, "2r", GREEN) + _cap(305, 192, "V ×8 · CSA ×4", "#555"))
    return _svg(410, 205, b + mid + a)


def prism():
    b = (f'<polygon points="30,140 80,140 55,95" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<polygon points="80,140 130,120 105,75 55,95" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2" opacity="0.7"/>'
         + f'<polygon points="55,95 105,75 130,120" fill="none" stroke="{BLUE}" stroke-width="1" opacity="0.5"/>'
         + _cap(90, 158, "base B", BLUE) + _cap(120, 105, "h", DIM) + _cap(80, 175, "Before", "#555"))
    mid = _arrow(160, 220, 108, "Length ×2")
    a = (f'<polygon points="245,140 295,140 270,95" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<polygon points="295,140 395,110 370,65 270,95" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2" opacity="0.7"/>'
         + _cap(340, 175, "2h length", GREEN) + _cap(320, 158, "Volume ×2", "#555"))
    return _svg(410, 185, b + mid + a)


def pyramid():
    b = (f'<polygon points="70,60 105,135 35,135" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2"/>'
         + f'<polygon points="70,60 105,135 130,118 95,45" fill="{BLUE_F}" stroke="{BLUE}" stroke-width="2" opacity="0.7"/>'
         + f'<line x1="70" y1="60" x2="70" y2="135" stroke="{DIM}" stroke-dasharray="3 2"/>' + _cap(80, 105, "h", DIM)
         + _cap(70, 152, "base", BLUE) + _cap(75, 172, "Before", "#555"))
    mid = _arrow(155, 215, 100, "Height ×2")
    a = (f'<polygon points="305,25 340,150 270,150" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2"/>'
         + f'<polygon points="305,25 340,150 365,133 330,10" fill="{GREEN_F}" stroke="{GREEN}" stroke-width="2" opacity="0.7"/>'
         + f'<line x1="305" y1="25" x2="305" y2="150" stroke="{GREEN}" stroke-dasharray="3 2"/>' + _cap(292, 95, "2h", GREEN)
         + _cap(310, 172, "Volume ×2", "#555"))
    return _svg(410, 185, b + mid + a)


FIGS = {
    "square": square, "rectangle": rectangle, "triangle": triangle,
    "equilateral": equilateral, "circle": circle, "semicircle": semicircle,
    "sector": sector, "rhombus": rhombus, "parallelogram": parallelogram,
    "trapezium": trapezium, "cube": cube, "cuboid": cuboid,
    "cylinder": cylinder, "cone": cone, "sphere": sphere,
    "hemisphere": hemisphere, "frustum": frustum, "prism": prism,
    "pyramid": pyramid,
}


def build():
    out = ["<!-- generated by _svg_figures.py — do not edit by hand -->"]
    for key, fn in FIGS.items():
        out.append(f"<!-- FIG:{key} -->")
        out.append(fn())
        out.append("")
    Path(__file__).with_name("_svg_snippets.md").write_text("\n".join(out), encoding="utf-8")
    print(f"wrote _svg_snippets.md ({len(FIGS)} figures)")


if __name__ == "__main__":
    build()
