# -*- coding: utf-8 -*-
"""
SSC CGL Mensuration (2D + 3D) - 500 hard MCQ generator.
Every answer is COMPUTED, so the key is provably correct.
Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.

pi is taken as Fraction(22,7); radii are multiples of 7 so areas/volumes
stay exact.  Surd answers (sqrt2 / sqrt3) are represented as a SurdVal carrying
both an exact display string and its float value, so options/dedup stay numeric.
"""
import random
import math
from fractions import Fraction

random.seed(20260625)  # deterministic

LETTERS = "abcd"
PI = Fraction(22, 7)


# ---------------- Surd value type ----------------
class SurdVal:
    """Carries a display string (exact form e.g. '36√3') plus its float value.
    Used so that surd answers can be shuffled / compared / deduped numerically
    while still being printed in exact form."""
    __slots__ = ("disp", "val")

    def __init__(self, disp, val):
        self.disp = disp
        self.val = float(val)

    def __float__(self):
        return self.val


def fval(x):
    """Numeric value of anything we use as an option/answer."""
    if isinstance(x, SurdVal):
        return x.val
    return float(x)


def fmt(x):
    """Format an option for display."""
    if isinstance(x, SurdVal):
        return x.disp
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        f = float(x)
        if abs(f - round(f, 4)) < 1e-9:
            return f"{f:.4f}".rstrip("0").rstrip(".")
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        return f"{x:.4f}".rstrip("0").rstrip(".")
    return str(x)


def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 distinct values."""
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        if all(abs(fval(d) - fval(o)) > 1e-6 for o in opts):
            opts.append(d)
        if len(opts) == 4:
            break
    # pad with plausible numeric filler if needed (never surd filler)
    bump = 1
    cf = fval(correct)
    base = Fraction(cf).limit_denominator(1000)
    while len(opts) < 4:
        step = Fraction(max(1, abs(int(cf)) // 7 + 1)) * bump
        cand = base + (step if cf >= 0 else -step)
        if all(abs(float(cand) - fval(o)) > 1e-6 for o in opts):
            opts.append(cand)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci


questions = []  # each: dict(stem, opts(list of str), ci, sol, diff)
seen = set()


def is_clean(x):
    """SurdVal always clean (exact). Numeric: integers, simple fractions,
    or <=2dp decimals."""
    if isinstance(x, SurdVal):
        return True
    fr = Fraction(x).limit_denominator(10**6)
    if fr.denominator in (1, 2, 3, 4, 5, 6, 7, 8, 11, 14):
        return True
    f = float(fr)
    return abs(f - round(f, 2)) < 1e-9


def _norm(x):
    if isinstance(x, SurdVal):
        return x
    return Fraction(x).limit_denominator(10**6)


def add(stem, correct, distractors, sol, diff):
    key = stem.strip()
    if key in seen:
        return False
    c = _norm(correct)
    if not is_clean(c):
        return False
    ds = []
    for d in distractors:
        if d is None:
            continue
        dn = _norm(d)
        if not is_clean(dn):
            continue
        if abs(fval(dn) - fval(c)) < 1e-6:
            continue
        ds.append(dn)
    # dedupe distractors among themselves
    uniq = []
    for d in ds:
        if all(abs(fval(d) - fval(u)) > 1e-6 for u in uniq):
            uniq.append(d)
    if len(uniq) < 3:
        return False
    seen.add(key)
    opts, ci = make_options(c, uniq)
    questions.append({
        "stem": stem,
        "opts": [fmt(o) for o in opts],
        "ci": ci,
        "sol": sol,
        "diff": diff,
    })
    return True


# Pythagorean triples & integer-area Heron triples
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
           (6, 8, 10), (9, 12, 15), (20, 21, 29), (9, 40, 41)]
HERON = [(13, 14, 15, 84), (3, 4, 5, 6), (5, 12, 13, 30),
         (9, 10, 17, 36), (10, 13, 13, 60), (25, 25, 30, 300),
         (5, 5, 6, 12), (8, 15, 17, 60), (6, 25, 29, 60)]


# ================= 2D TEMPLATES =================

def t_square_diag():
    """Square: side given -> diagonal (surd) OR diagonal given -> area/perimeter. [M]"""
    s = random.choice([4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 25, 30])
    correct = SurdVal(f"{s}√2", s * math.sqrt(2))
    w1 = Fraction(2 * s)              # 2s (forgets sqrt)
    w2 = SurdVal(f"{2*s}√2", 2 * s * math.sqrt(2))
    w3 = Fraction(s * s)             # area
    stem = f"The side of a square is {s} cm. The length of its diagonal (in cm) is:"
    sol = (f"Diagonal = side×√2 = {s}√2 cm ≈ {s*math.sqrt(2):.3f} cm. "
           f"Trap: diagonal is s√2, not 2s.")
    return stem, correct, [w1, w2, w3], sol, "M"


def t_square_from_diag():
    """Square: diagonal given -> area. [M]"""
    d = random.choice([6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 30])
    area = Fraction(d * d, 2)        # d^2/2
    correct = area
    w1 = Fraction(d * d)             # d^2 (forgets /2)
    w2 = Fraction(d * d, 4)
    w3 = Fraction(2 * d * d)
    stem = f"The diagonal of a square is {d} cm. Its area (in cm²) is:"
    sol = (f"Area = d²/2 = {d}²/2 = {fmt(area)} cm². "
           f"Trap: area = d²/2, since side = d/√2.")
    return stem, correct, [w1, w2, w3], sol, "M"


def t_rectangle_perim_area():
    """Rectangle: length, breadth -> diagonal (triple) and area. Ask diagonal. [M]"""
    a, b, c = random.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
                             (6, 8, 10), (9, 12, 15), (20, 21, 29)])
    k = random.choice([1, 2, 3, 5])
    L, B, D = a * k, b * k, c * k
    correct = Fraction(D)
    w1 = Fraction(L + B)             # perimeter-ish
    w2 = Fraction(L * B).limit_denominator()  # area
    w3 = Fraction(L + B, 2)
    stem = (f"A rectangle has length {L} cm and breadth {B} cm. "
            f"The length of its diagonal (in cm) is:")
    sol = (f"Diagonal = √(L²+B²) = √({L}²+{B}²) = √{L*L+B*B} = {D} cm "
           f"(a {a}-{b}-{c} triple scaled).")
    return stem, correct, [w1, w2, w3], sol, "M"


def t_rect_area_from_ratio():
    """Rectangle: perimeter and ratio l:b -> area. [H]"""
    rl, rb = random.choice([(3, 2), (4, 3), (5, 3), (5, 4), (7, 5), (5, 2), (3, 1)])
    mult = random.choice([2, 3, 4, 5, 6, 8, 10])
    L, B = rl * mult, rb * mult
    perim = 2 * (L + B)
    area = Fraction(L * B)
    correct = area
    w1 = Fraction(perim)             # gives perimeter
    w2 = Fraction(L * B, 2)
    w3 = Fraction((perim // 2) ** 2, 4)
    stem = (f"The perimeter of a rectangle is {perim} cm and the ratio of its "
            f"length to breadth is {rl}:{rb}. Its area (in cm²) is:")
    sol = (f"l+b = {perim}/2 = {perim//2}. With l:b = {rl}:{rb}, one part = "
           f"{perim//2}/{rl+rb} = {(perim//2)//(rl+rb)}. So l={L}, b={B}, "
           f"area = {L}×{B} = {fmt(area)} cm².")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_triangle_heron():
    """Triangle by Heron with integer area triple. [H]"""
    a, b, c, ar = random.choice(HERON)
    k = random.choice([1, 1, 2, 3])
    A, B, C = a * k, b * k, c * k
    area = Fraction(ar * k * k)
    correct = area
    s = Fraction(A + B + C, 2)
    w1 = Fraction(A * B, 2)          # treats as right triangle base*height/2
    w2 = Fraction(A + B + C)         # perimeter
    w3 = area * 2
    stem = (f"The sides of a triangle are {A} cm, {B} cm and {C} cm. "
            f"Its area (in cm²) is:")
    sol = (f"s = ({A}+{B}+{C})/2 = {fmt(s)}. "
           f"Area = √(s(s−a)(s−b)(s−c)) = {fmt(area)} cm² (Heron's formula).")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_equilateral():
    """Equilateral triangle area = (√3/4)a². Present exact surd. [H]"""
    a = random.choice([4, 6, 8, 10, 12, 14, 16, 18, 20, 24])
    coef = Fraction(a * a, 4)        # coefficient of √3
    correct = SurdVal(f"{fmt(coef)}√3", float(coef) * math.sqrt(3))
    w1 = SurdVal(f"{fmt(Fraction(a*a,2))}√3", float(Fraction(a * a, 2)) * math.sqrt(3))
    w2 = Fraction(a * a)             # forgets √3/4
    w3 = SurdVal(f"{a*a}√3", a * a * math.sqrt(3))
    stem = (f"The side of an equilateral triangle is {a} cm. "
            f"Its area (in cm²) is:")
    sol = (f"Area = (√3/4)a² = (√3/4)×{a}² = {fmt(coef)}√3 cm² "
           f"≈ {float(coef)*math.sqrt(3):.3f} cm².")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_equilateral_height():
    """Equilateral triangle height = (√3/2)a. [M]"""
    a = random.choice([4, 6, 8, 10, 12, 14, 16, 18, 20])
    coef = Fraction(a, 2)
    correct = SurdVal(f"{fmt(coef)}√3", float(coef) * math.sqrt(3))
    w1 = SurdVal(f"{a}√3", a * math.sqrt(3))
    w2 = Fraction(a, 2)
    w3 = SurdVal(f"{fmt(Fraction(a,2))}√2", float(Fraction(a, 2)) * math.sqrt(2))
    stem = (f"The side of an equilateral triangle is {a} cm. "
            f"Its height (in cm) is:")
    sol = (f"Height = (√3/2)a = (√3/2)×{a} = {fmt(coef)}√3 cm "
           f"≈ {float(coef)*math.sqrt(3):.3f} cm.")
    return stem, correct, [w1, w2, w3], sol, "M"


def t_circle_area():
    """Circle area, r multiple of 7. (Take pi=22/7). [M]"""
    r = random.choice([7, 14, 21, 28, 35, 42])
    area = PI * r * r
    correct = area
    w1 = PI * 2 * r                  # circumference instead
    w2 = Fraction(r * r)             # forgets pi
    w3 = PI * r                      # half-baked
    stem = (f"The radius of a circle is {r} cm. Its area (in cm²) is: (Take π = 22/7)")
    sol = (f"Area = πr² = 22/7 × {r}² = {fmt(area)} cm².")
    return stem, correct, [w1, w2, w3], sol, "M"


def t_circle_circum():
    """Circle circumference, r multiple of 7. [M]"""
    r = random.choice([7, 14, 21, 28, 35, 42, 49])
    circ = PI * 2 * r
    correct = circ
    w1 = PI * r * r                  # area
    w2 = PI * r                      # forgets 2
    w3 = Fraction(2 * r)             # forgets pi
    stem = (f"The radius of a circle is {r} cm. Its circumference (in cm) is: (Take π = 22/7)")
    sol = (f"Circumference = 2πr = 2 × 22/7 × {r} = {fmt(circ)} cm.")
    return stem, correct, [w1, w2, w3], sol, "M"


def t_sector_area():
    """Sector area = (theta/360)pi r^2, r mult of 7, theta divides nicely. [VH]"""
    r = random.choice([7, 14, 21, 42])
    theta = random.choice([30, 45, 60, 90, 120, 135, 180, 270])
    area = Fraction(theta, 360) * PI * r * r
    if area.denominator not in (1, 2, 4, 7, 14):
        return None
    correct = area
    w1 = Fraction(theta, 360) * PI * 2 * r       # arc-based mistake
    w2 = PI * r * r                              # full circle
    w3 = Fraction(theta, 180) * PI * r * r       # wrong /180
    stem = (f"A sector of a circle has radius {r} cm and a central angle of "
            f"{theta}°. The area of the sector (in cm²) is: (Take π = 22/7)")
    sol = (f"Sector area = (θ/360)×πr² = ({theta}/360)×(22/7)×{r}² = {fmt(area)} cm².")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_arc_length():
    """Arc length = (theta/360)*2 pi r. [H]"""
    r = random.choice([7, 14, 21, 42])
    theta = random.choice([60, 90, 120, 180, 270])
    arc = Fraction(theta, 360) * PI * 2 * r
    if arc.denominator not in (1, 2, 4, 7, 14):
        return None
    correct = arc
    w1 = Fraction(theta, 360) * PI * r * r       # sector area
    w2 = PI * 2 * r                              # full circumference
    w3 = Fraction(theta, 180) * PI * r
    stem = (f"The radius of a circle is {r} cm. The length of an arc subtending "
            f"a central angle of {theta}° (in cm) is: (Take π = 22/7)")
    sol = (f"Arc = (θ/360)×2πr = ({theta}/360)×2×(22/7)×{r} = {fmt(arc)} cm.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_rhombus():
    """Rhombus area from diagonals = d1*d2/2; also side via Pythagoras. [H]"""
    d1 = random.choice([12, 16, 24, 10, 30, 18, 48])
    d2 = random.choice([16, 30, 10, 24, 40, 14, 20])
    if d1 == d2:
        return None
    area = Fraction(d1 * d2, 2)
    correct = area
    w1 = Fraction(d1 * d2)           # forgets /2
    w2 = Fraction(d1 * d2, 4)
    w3 = Fraction(2 * (d1 + d2))
    stem = (f"The diagonals of a rhombus are {d1} cm and {d2} cm. "
            f"Its area (in cm²) is:")
    sol = (f"Area = ½ × d₁ × d₂ = ½ × {d1} × {d2} = {fmt(area)} cm².")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_rhombus_side():
    """Rhombus: diagonals -> side (Pythagoras on half-diagonals). [H]"""
    # choose half diagonals forming a triple
    a, b, c = random.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17),
                             (9, 12, 15)])
    d1, d2 = 2 * a, 2 * b
    side = Fraction(c)
    correct = side
    w1 = Fraction(d1 * d2, 2)        # area
    w2 = Fraction(a + b)             # sum of halves
    w3 = Fraction(d1 + d2, 2)
    stem = (f"The diagonals of a rhombus are {d1} cm and {d2} cm. "
            f"The length of each side (in cm) is:")
    sol = (f"Side = √((d₁/2)²+(d₂/2)²) = √({a}²+{b}²) = √{a*a+b*b} = {c} cm.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_trapezium():
    """Trapezium area = ½(a+b)h. [H]"""
    a = random.choice([10, 12, 15, 16, 18, 20, 24])
    b = random.choice([6, 8, 10, 12, 14, 22, 26])
    if a == b:
        return None
    h = random.choice([4, 6, 8, 10, 12, 14])
    area = Fraction((a + b) * h, 2)
    correct = area
    w1 = Fraction((a + b) * h)       # forgets /2
    w2 = Fraction(a * b * h, 2)
    w3 = Fraction((a + b) * h, 4)
    stem = (f"The parallel sides of a trapezium are {a} cm and {b} cm, and the "
            f"distance between them is {h} cm. Its area (in cm²) is:")
    sol = (f"Area = ½(a+b)h = ½×({a}+{b})×{h} = {fmt(area)} cm².")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_path_around_rect():
    """Path of width w OUTSIDE a rectangle -> area of path. [VH]"""
    L = random.choice([40, 50, 60, 80, 100, 120])
    B = random.choice([20, 30, 40, 50, 60, 70])
    w = random.choice([2, 3, 5])
    outerL, outerB = L + 2 * w, B + 2 * w
    area = Fraction(outerL * outerB - L * B)
    correct = area
    w1 = Fraction((L + w) * (B + w) - L * B)     # width added once
    w2 = Fraction(outerL * outerB)               # whole outer
    w3 = Fraction(2 * w * (L + B))               # forgets corners
    stem = (f"A rectangular field is {L} m long and {B} m wide. A path of "
            f"uniform width {w} m runs all around it on the outside. "
            f"The area of the path (in m²) is:")
    sol = (f"Outer = ({L}+2×{w})×({B}+2×{w}) = {outerL}×{outerB} = {outerL*outerB}. "
           f"Path = {outerL*outerB} − {L}×{B} = {fmt(area)} m².")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_circle_ring():
    """Area between two concentric circles. (pi=22/7), radii mult of 7. [H]"""
    R = random.choice([14, 21, 28, 35])
    r = random.choice([7, 14, 21])
    if r >= R:
        return None
    area = PI * (R * R - r * r)
    correct = area
    w1 = PI * (R - r) * (R - r)
    w2 = PI * (R * R + r * r)
    w3 = PI * 2 * (R - r)
    stem = (f"Two concentric circles have radii {R} cm and {r} cm. The area of "
            f"the ring between them (in cm²) is: (Take π = 22/7)")
    sol = (f"Ring = π(R²−r²) = 22/7×({R}²−{r}²) = 22/7×{R*R-r*r} = {fmt(area)} cm².")
    return stem, correct, [w1, w2, w3], sol, "H"


# ================= 3D TEMPLATES =================

def t_cube_volume():
    """Cube volume from edge. [M]"""
    a = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    vol = Fraction(a ** 3)
    correct = vol
    w1 = Fraction(6 * a * a)         # TSA
    w2 = Fraction(a * a)
    w3 = Fraction(12 * a)            # total edge length
    stem = f"The edge of a cube is {a} cm. Its volume (in cm³) is:"
    sol = f"Volume = a³ = {a}³ = {fmt(vol)} cm³."
    return stem, correct, [w1, w2, w3], sol, "M"


def t_cube_tsa():
    """Cube TSA from edge. [M]"""
    a = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12, 15])
    tsa = Fraction(6 * a * a)
    correct = tsa
    w1 = Fraction(a ** 3)            # volume
    w2 = Fraction(4 * a * a)         # LSA
    w3 = Fraction(a * a)             # one face
    stem = f"The edge of a cube is {a} cm. Its total surface area (in cm²) is:"
    sol = f"TSA = 6a² = 6×{a}² = {fmt(tsa)} cm²."
    return stem, correct, [w1, w2, w3], sol, "M"


def t_cube_diagonal():
    """Cube diagonal = a√3 (surd). [H]"""
    a = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 12])
    correct = SurdVal(f"{a}√3", a * math.sqrt(3))
    w1 = SurdVal(f"{a}√2", a * math.sqrt(2))     # face diagonal mistake
    w2 = Fraction(a)
    w3 = Fraction(3 * a)
    stem = f"The edge of a cube is {a} cm. The length of its space diagonal (in cm) is:"
    sol = (f"Space diagonal = a√3 = {a}√3 cm ≈ {a*math.sqrt(3):.3f} cm "
           f"(face diagonal is a√2).")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_cuboid_volume():
    """Cuboid volume. [M]"""
    l = random.choice([6, 8, 10, 12, 15, 16, 20])
    b = random.choice([4, 5, 6, 8, 9, 10, 12])
    h = random.choice([2, 3, 4, 5, 6, 8])
    vol = Fraction(l * b * h)
    correct = vol
    w1 = Fraction(2 * (l * b + b * h + h * l))   # TSA
    w2 = Fraction(l * b)
    w3 = Fraction(l + b + h)
    stem = (f"A cuboid has dimensions {l} cm × {b} cm × {h} cm. "
            f"Its volume (in cm³) is:")
    sol = f"Volume = l×b×h = {l}×{b}×{h} = {fmt(vol)} cm³."
    return stem, correct, [w1, w2, w3], sol, "M"


def t_cuboid_tsa():
    """Cuboid TSA. [H]"""
    l = random.choice([6, 8, 10, 12, 15, 16, 20])
    b = random.choice([4, 5, 6, 8, 9, 10])
    h = random.choice([2, 3, 4, 5, 6])
    tsa = Fraction(2 * (l * b + b * h + h * l))
    correct = tsa
    w1 = Fraction(l * b * h)         # volume
    w2 = Fraction(l * b + b * h + h * l)  # forgets 2
    w3 = Fraction(2 * (l + b + h))
    stem = (f"A cuboid has dimensions {l} cm × {b} cm × {h} cm. "
            f"Its total surface area (in cm²) is:")
    sol = (f"TSA = 2(lb+bh+hl) = 2({l}×{b}+{b}×{h}+{h}×{l}) = {fmt(tsa)} cm².")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_cuboid_diagonal():
    """Cuboid space diagonal via integer (l,b,h)->d if exists, else surd. [H]"""
    # quadruples with integer diagonal
    l, b, h, d = random.choice([(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9),
                                (4, 4, 7, 9), (3, 4, 12, 13), (2, 6, 9, 11),
                                (6, 6, 7, 11), (12, 15, 16, 25)])
    k = random.choice([1, 1, 2, 3])
    L, B, H, D = l * k, b * k, h * k, d * k
    correct = Fraction(D)
    w1 = Fraction(L + B + H)
    w2 = Fraction(L * B * H).limit_denominator()
    w3 = Fraction(2 * (L + B + H))
    stem = (f"A cuboid has dimensions {L} cm × {B} cm × {H} cm. "
            f"The length of its longest diagonal (in cm) is:")
    sol = (f"Diagonal = √(l²+b²+h²) = √({L}²+{B}²+{H}²) = √{L*L+B*B+H*H} = {D} cm.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_cuboid_paint():
    """Cost of painting all faces of a cuboid at rate r per m^2. [VH]"""
    l = random.choice([4, 5, 6, 8, 10])
    b = random.choice([3, 4, 5, 6])
    h = random.choice([2, 3, 4, 5])
    rate = random.choice([5, 8, 10, 12, 15, 20, 25])
    tsa = 2 * (l * b + b * h + h * l)
    cost = Fraction(tsa * rate)
    correct = cost
    w1 = Fraction(l * b * h * rate)              # uses volume
    w2 = Fraction((l * b + b * h + h * l) * rate)  # forgets 2
    w3 = Fraction(4 * (l + b) * h * rate)        # only walls
    stem = (f"A closed wooden box measures {l} m × {b} m × {h} m. "
            f"The cost of painting all its outer faces at ₹{rate} per m² is:")
    sol = (f"TSA = 2(lb+bh+hl) = {tsa} m². Cost = {tsa}×₹{rate} = ₹{fmt(cost)}.")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_cylinder_volume():
    """Cylinder volume, r mult of 7. [H]"""
    r = random.choice([7, 14, 21])
    h = random.choice([5, 10, 12, 15, 20, 6, 9])
    vol = PI * r * r * h
    correct = vol
    w1 = PI * 2 * r * h              # CSA
    w2 = PI * r * h
    w3 = Fraction(r * r * h)         # forgets pi
    stem = (f"A cylinder has radius {r} cm and height {h} cm. "
            f"Its volume (in cm³) is: (Take π = 22/7)")
    sol = (f"Volume = πr²h = 22/7×{r}²×{h} = {fmt(vol)} cm³.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_cylinder_csa():
    """Cylinder CSA. [H]"""
    r = random.choice([7, 14, 21])
    h = random.choice([5, 10, 12, 15, 20, 8])
    csa = PI * 2 * r * h
    correct = csa
    w1 = PI * r * r * h              # volume
    w2 = PI * r * h                  # forgets 2
    w3 = PI * 2 * r * (r + h)        # TSA
    stem = (f"A cylinder has radius {r} cm and height {h} cm. Its curved "
            f"surface area (in cm²) is: (Take π = 22/7)")
    sol = (f"CSA = 2πrh = 2×22/7×{r}×{h} = {fmt(csa)} cm².")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_cylinder_tsa():
    """Cylinder TSA = 2 pi r (r+h). [VH]"""
    r = random.choice([7, 14, 21])
    h = random.choice([5, 7, 10, 14, 21, 8])
    tsa = PI * 2 * r * (r + h)
    correct = tsa
    w1 = PI * 2 * r * h              # CSA only
    w2 = PI * r * r * h              # volume
    w3 = PI * 2 * r * r + PI * r * h
    stem = (f"A solid cylinder has radius {r} cm and height {h} cm. "
            f"Its total surface area (in cm²) is: (Take π = 22/7)")
    sol = (f"TSA = 2πr(r+h) = 2×22/7×{r}×({r}+{h}) = {fmt(tsa)} cm².")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_cone_volume():
    """Cone volume = 1/3 pi r^2 h, r mult of 7, h mult of 3. [H]"""
    r = random.choice([7, 14, 21])
    h = random.choice([3, 6, 9, 12, 15, 24])
    vol = Fraction(1, 3) * PI * r * r * h
    correct = vol
    w1 = PI * r * r * h              # forgets 1/3 (cylinder)
    w2 = Fraction(1, 3) * PI * 2 * r * h
    w3 = Fraction(r * r * h, 3)      # forgets pi
    stem = (f"A cone has radius {r} cm and height {h} cm. "
            f"Its volume (in cm³) is: (Take π = 22/7)")
    sol = (f"Volume = ⅓πr²h = ⅓×22/7×{r}²×{h} = {fmt(vol)} cm³.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_cone_slant():
    """Cone: r & h form a triple -> slant height l. [H]"""
    a, b, c = random.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
                             (6, 8, 10), (9, 12, 15), (20, 21, 29)])
    r, h, l = a, b, c
    correct = Fraction(l)
    w1 = Fraction(r + h)
    w2 = Fraction(r * h, 2)
    w3 = Fraction(r + h, 2)
    stem = (f"A cone has base radius {r} cm and vertical height {h} cm. "
            f"Its slant height (in cm) is:")
    sol = (f"Slant l = √(r²+h²) = √({r}²+{h}²) = √{r*r+h*h} = {l} cm.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_cone_csa():
    """Cone CSA = pi r l, with r mult of 7 and (r,h,l) a triple scaled. [VH]"""
    # triples with r a multiple of 7
    r, h, l = random.choice([(7, 24, 25), (21, 28, 35), (14, 48, 50), (7, 7 * 0 + 24, 25)])
    if r % 7 != 0:
        return None
    csa = PI * r * l
    correct = csa
    w1 = PI * r * h                  # uses height not slant
    w2 = PI * r * r                  # base area
    w3 = Fraction(1, 3) * PI * r * r * h  # volume
    stem = (f"A cone has base radius {r} cm and slant height {l} cm. "
            f"Its curved surface area (in cm²) is: (Take π = 22/7)")
    sol = (f"CSA = πrl = 22/7×{r}×{l} = {fmt(csa)} cm².")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_sphere_volume():
    """Sphere volume = 4/3 pi r^3, r mult of 7. [H]"""
    r = random.choice([7, 14, 21])
    vol = Fraction(4, 3) * PI * r ** 3
    correct = vol
    w1 = Fraction(4) * PI * r * r    # surface area
    w2 = Fraction(1, 3) * PI * r ** 3
    w3 = Fraction(4, 3) * PI * r * r  # power slip
    stem = (f"A sphere has radius {r} cm. Its volume (in cm³) is: (Take π = 22/7)")
    sol = (f"Volume = 4/3 πr³ = 4/3×22/7×{r}³ = {fmt(vol)} cm³.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_sphere_surface():
    """Sphere surface area = 4 pi r^2. [H]"""
    r = random.choice([7, 14, 21, 28])
    sa = Fraction(4) * PI * r * r
    correct = sa
    w1 = PI * r * r                  # forgets 4
    w2 = Fraction(4, 3) * PI * r ** 3  # volume
    w3 = Fraction(2) * PI * r * r    # hemisphere curved
    stem = (f"A sphere has radius {r} cm. Its surface area (in cm²) is: (Take π = 22/7)")
    sol = (f"Surface area = 4πr² = 4×22/7×{r}² = {fmt(sa)} cm².")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_hemisphere_tsa():
    """Hemisphere TSA = 3 pi r^2. [VH]"""
    r = random.choice([7, 14, 21])
    tsa = Fraction(3) * PI * r * r
    correct = tsa
    w1 = Fraction(2) * PI * r * r    # curved only
    w2 = Fraction(4) * PI * r * r    # full sphere
    w3 = PI * r * r                  # base only
    stem = (f"A solid hemisphere has radius {r} cm. Its total surface area "
            f"(in cm²) is: (Take π = 22/7)")
    sol = (f"TSA of solid hemisphere = 3πr² = 3×22/7×{r}² = {fmt(tsa)} cm² "
           f"(curved 2πr² + flat base πr²).")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_hemisphere_volume():
    """Hemisphere volume = 2/3 pi r^3. [H]"""
    r = random.choice([7, 14, 21])
    vol = Fraction(2, 3) * PI * r ** 3
    correct = vol
    w1 = Fraction(4, 3) * PI * r ** 3  # full sphere
    w2 = Fraction(3) * PI * r * r    # TSA
    w3 = Fraction(2) * PI * r * r    # curved
    stem = (f"A hemisphere has radius {r} cm. Its volume (in cm³) is: (Take π = 22/7)")
    sol = (f"Volume = 2/3 πr³ = 2/3×22/7×{r}³ = {fmt(vol)} cm³.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_recast_sphere_to_cyl():
    """Melt a sphere -> cylinder of given radius, find height (volume equality). [VH]"""
    rs = random.choice([3, 6, 9, 12])         # sphere radius
    rc = random.choice([4, 6, 8, 9])          # cylinder radius
    # height = (4/3 r_s^3) / r_c^2
    h = Fraction(4, 3) * rs ** 3 / (rc * rc)
    if not is_clean(h) or h <= 0:
        return None
    correct = h
    w1 = Fraction(4, 3) * rs ** 3 / rc        # forgets square
    w2 = Fraction(rs ** 3, rc * rc)           # forgets 4/3
    w3 = Fraction(4) * rs ** 3 / (rc * rc)    # forgets /3
    stem = (f"A solid metallic sphere of radius {rs} cm is melted and recast "
            f"into a solid cylinder of radius {rc} cm. The height of the "
            f"cylinder (in cm) is:")
    sol = (f"Volume equality: 4/3 πr_s³ = πr_c²h → h = (4/3×{rs}³)/{rc}² "
           f"= {fmt(correct)} cm. (π cancels.)")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_recast_sphere_to_cone():
    """Melt sphere -> cone of given radius, find height. [VH]"""
    rs = random.choice([3, 6, 9, 12])
    rc = random.choice([4, 6, 9, 12])
    # 4/3 r_s^3 = 1/3 r_c^2 h -> h = 4 r_s^3 / r_c^2
    h = Fraction(4 * rs ** 3, rc * rc)
    if not is_clean(h) or h <= 0:
        return None
    correct = h
    w1 = Fraction(4, 3) * rs ** 3 / (rc * rc)   # keeps both 1/3 & 4/3
    w2 = Fraction(rs ** 3, rc * rc)
    w3 = Fraction(4 * rs ** 3, rc)
    stem = (f"A solid metallic sphere of radius {rs} cm is melted and recast "
            f"into a solid cone of base radius {rc} cm. The height of the cone "
            f"(in cm) is:")
    sol = (f"4/3 πr_s³ = 1/3 πr_c²h → h = 4r_s³/r_c² = 4×{rs}³/{rc}² "
           f"= {fmt(correct)} cm.")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_recast_cyl_to_spheres():
    """Melt a cylinder -> number of small spheres. [VH]"""
    rc = random.choice([6, 9, 12, 18])
    hc = random.choice([4, 6, 8, 12, 18, 27])
    rsph = random.choice([1, 2, 3])
    vol_cyl = rc * rc * hc                   # /pi factored
    vol_sph = Fraction(4, 3) * rsph ** 3
    n = Fraction(vol_cyl) / vol_sph
    if n.denominator != 1 or n <= 1:
        return None
    correct = n
    w1 = Fraction(vol_cyl, rsph ** 3)        # forgets 4/3
    w2 = Fraction(vol_cyl * 3, 4 * rsph ** 3) * 2
    w3 = n + random.choice([3, 5, 8])
    stem = (f"A solid metallic cylinder of radius {rc} cm and height {hc} cm is "
            f"melted and recast into solid spheres each of radius {rsph} cm. "
            f"The number of spheres formed is:")
    sol = (f"n = (πr_c²h)/(4/3 πr_s³) = ({rc}²×{hc})/(4/3×{rsph}³) "
           f"= {fmt(correct)}.")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_volume_scale():
    """Each edge of a cube increased by p% -> % change in volume. [H]"""
    p = random.choice([10, 20, 25, 50, 100, 5, 40])
    f = Fraction(100 + p, 100)
    change = (f ** 3 - 1) * 100
    correct = change.limit_denominator(1000)
    w1 = Fraction(3 * p)             # linear x3
    w2 = Fraction(p)                 # same as edge
    w3 = (f ** 2 - 1) * 100          # area scaling
    stem = (f"If each edge of a cube is increased by {p}%, the percentage "
            f"increase in its volume is:")
    sol = (f"New volume factor = (1+{p}/100)³. %increase = ((1+{p}/100)³−1)×100 "
           f"= {fmt(correct)}%.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_cyl_cone_combo():
    """Solid = cylinder + cone on top, same radius -> total volume. [VH]"""
    r = random.choice([7, 14, 21])
    hcyl = random.choice([6, 9, 12, 15])
    hcone = random.choice([3, 6, 9, 12])
    vol = PI * r * r * hcyl + Fraction(1, 3) * PI * r * r * hcone
    correct = vol
    w1 = PI * r * r * hcyl + PI * r * r * hcone        # cone as cylinder
    w2 = PI * r * r * (hcyl + hcone)
    w3 = PI * r * r * hcyl                              # forgets cone
    stem = (f"A solid consists of a cylinder of radius {r} cm and height {hcyl} cm "
            f"surmounted by a cone of the same radius and height {hcone} cm. "
            f"The total volume (in cm³) is: (Take π = 22/7)")
    sol = (f"V = πr²h_cyl + ⅓πr²h_cone = 22/7×{r}²×{hcyl} + ⅓×22/7×{r}²×{hcone} "
           f"= {fmt(vol)} cm³.")
    return stem, correct, [w1, w2, w3], sol, "VH"


TEMPLATES = [
    t_square_diag, t_square_from_diag, t_rectangle_perim_area, t_rect_area_from_ratio,
    t_triangle_heron, t_equilateral, t_equilateral_height, t_circle_area,
    t_circle_circum, t_sector_area, t_arc_length, t_rhombus, t_rhombus_side,
    t_trapezium, t_path_around_rect, t_circle_ring,
    t_cube_volume, t_cube_tsa, t_cube_diagonal, t_cuboid_volume, t_cuboid_tsa,
    t_cuboid_diagonal, t_cuboid_paint, t_cylinder_volume, t_cylinder_csa,
    t_cylinder_tsa, t_cone_volume, t_cone_slant, t_cone_csa, t_sphere_volume,
    t_sphere_surface, t_hemisphere_tsa, t_hemisphere_volume,
    t_recast_sphere_to_cyl, t_recast_sphere_to_cone, t_recast_cyl_to_spheres,
    t_volume_scale, t_cyl_cone_combo,
]

DIFF_OF = {
    t_square_diag: "M", t_square_from_diag: "M", t_rectangle_perim_area: "M",
    t_rect_area_from_ratio: "H", t_triangle_heron: "H", t_equilateral: "H",
    t_equilateral_height: "M", t_circle_area: "M", t_circle_circum: "M",
    t_sector_area: "VH", t_arc_length: "H", t_rhombus: "H", t_rhombus_side: "H",
    t_trapezium: "H", t_path_around_rect: "VH", t_circle_ring: "H",
    t_cube_volume: "M", t_cube_tsa: "M", t_cube_diagonal: "H",
    t_cuboid_volume: "M", t_cuboid_tsa: "H", t_cuboid_diagonal: "H",
    t_cuboid_paint: "VH", t_cylinder_volume: "H", t_cylinder_csa: "H",
    t_cylinder_tsa: "VH", t_cone_volume: "H", t_cone_slant: "H",
    t_cone_csa: "VH", t_sphere_volume: "H", t_sphere_surface: "H",
    t_hemisphere_tsa: "VH", t_hemisphere_volume: "H",
    t_recast_sphere_to_cyl: "VH", t_recast_sphere_to_cone: "VH",
    t_recast_cyl_to_spheres: "VH", t_volume_scale: "H", t_cyl_cone_combo: "VH",
}
# Tune so per-difficulty TOTAL share ~ 20% M / 60% H / 20% VH.
# Weight is per-template; multiply by template count per difficulty to balance.
from collections import Counter as _C
_dc = _C(DIFF_OF[t] for t in TEMPLATES)   # template counts per difficulty
# target shares
_target = {"M": 0.20, "H": 0.60, "VH": 0.20}
WEIGHT = {d: _target[d] / _dc[d] for d in _dc}
POOL = []
for t in TEMPLATES:
    POOL += [t] * max(1, int(round(WEIGHT[DIFF_OF[t]] * 1000)))

attempts = 0
while len(questions) < 500 and attempts < 600000:
    attempts += 1
    t = random.choice(POOL)
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    add(stem, correct, distractors, sol, diff)

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- SELF-CHECK: 4 distinct options, one correct ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
print(f"Self-check errors: {errors}")

from collections import Counter
print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_08_Mensuration_500.md"

lines = []
lines.append("# Mensuration (2D + 3D) — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Where stated, **π = 22/7** and radii are chosen so areas/volumes are exact.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- Square: diagonal = a√2 · area from diagonal = d²/2")
lines.append("- Rectangle: diagonal = √(l²+b²) · area = l×b · perimeter = 2(l+b)")
lines.append("- Triangle (Heron): s = (a+b+c)/2, area = √(s(s−a)(s−b)(s−c))")
lines.append("- Equilateral side a: area = (√3/4)a² · height = (√3/2)a")
lines.append("- Circle: area = πr² · circumference = 2πr · ring = π(R²−r²)")
lines.append("- Sector (angle θ): area = (θ/360)πr² · arc = (θ/360)·2πr")
lines.append("- Rhombus: area = ½d₁d₂ · side = √((d₁/2)²+(d₂/2)²)")
lines.append("- Trapezium: area = ½(a+b)h")
lines.append("- Cube: V = a³ · TSA = 6a² · space diagonal = a√3")
lines.append("- Cuboid: V = lbh · TSA = 2(lb+bh+hl) · diagonal = √(l²+b²+h²)")
lines.append("- Cylinder: V = πr²h · CSA = 2πrh · TSA = 2πr(r+h)")
lines.append("- Cone: V = ⅓πr²h · slant l = √(r²+h²) · CSA = πrl")
lines.append("- Sphere: V = 4/3 πr³ · SA = 4πr² | Hemisphere: V = 2/3 πr³ · TSA = 3πr²")
lines.append("- Recasting: total VOLUME is conserved (π cancels) — equate volumes\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        o = q["opts"]
        lines.append(f"**Q{n}.** {q['stem']}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Answers Q{start+1}–Q{start+50}\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        letter = LETTERS[q["ci"]]
        val = q["opts"][q["ci"]]
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* — {q['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUT}")
print(f"Total lines: {len(lines)}")
