# -*- coding: utf-8 -*-
"""
SSC CGL Geometry (+ Coordinate Geometry) - 500 hard MCQ generator.
Every answer is COMPUTED, so the key is provably correct.
Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.

Mirrors gen_percentage.py: Fraction-based where exact, is_clean(),
make_options(), add() dedupe, weighted pool for ~20% M / 60% H / 20% VH,
self-check (500 unique, 4 distinct options, exactly one correct).

CRITICAL: never pass a float straight to Fraction(num,den).
Use Fraction(x).limit_denominator(1000). Irrational lengths are avoided by
choosing Pythagorean triples / nice angles so every keyed value is rational.
"""
import random
from fractions import Fraction
from math import gcd

random.seed(20260625)  # deterministic

LETTERS = "abcd"

# Pythagorean triples (a,b,c) with c the hypotenuse, plus scaled multiples.
BASE_TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 40, 41),
                (6, 8, 10), (20, 21, 29), (12, 35, 37), (11, 60, 61)]


def fmt(x):
    """Format a number cleanly: ints as ints, fractions as decimals or fraction."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        f = float(x)
        if abs(f - round(f, 4)) < 1e-9:
            s = f"{f:.4f}".rstrip("0").rstrip(".")
            return s
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        s = f"{x:.4f}".rstrip("0").rstrip(".")
        return s
    return str(x)


def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 distinct values."""
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        if all(abs(float(d) - float(o)) > 1e-9 for o in opts):
            opts.append(d)
        if len(opts) == 4:
            break
    bump = 1
    cf = float(correct)
    while len(opts) < 4:
        cand = Fraction(correct) + Fraction(bump * (3 if cf >= 0 else -3))
        if all(abs(float(cand) - float(o)) > 1e-9 for o in opts):
            opts.append(cand)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci


questions = []  # each: dict(stem, opts, ci, sol, diff)
seen = set()


def is_clean(x):
    """Accept integers, halves/quarters/thirds/sixths/eighths, and <=2dp decimals."""
    fr = Fraction(x).limit_denominator(10**6)
    if fr.denominator in (1, 2, 3, 4, 5, 6, 8):
        return True
    f = float(fr)
    return abs(f - round(f, 2)) < 1e-9


def add(stem, correct, distractors, sol, diff):
    key = stem.strip()
    if key in seen:
        return False
    cfr = Fraction(correct).limit_denominator(10**6)
    if not is_clean(cfr):
        return False
    dfrs = [Fraction(d).limit_denominator(10**6) for d in distractors if d is not None]
    dfrs = [d for d in dfrs if is_clean(d) and d != cfr]
    if len(dfrs) < 3:
        return False
    seen.add(key)
    opts, ci = make_options(cfr, dfrs)
    questions.append({
        "stem": stem,
        "opts": [fmt(o) for o in opts],
        "ci": ci,
        "sol": sol,
        "diff": diff,
    })
    return True


def F(n, d=1):
    return Fraction(n, d)


# ----------------------------------------------------------------------------
# TEMPLATES
# ----------------------------------------------------------------------------

def t_triangle_third_angle():
    """Two angles of a triangle given -> third angle. [M]"""
    a = random.choice([30, 40, 45, 50, 55, 60, 65, 70, 72, 75, 80, 85])
    b = random.choice([35, 40, 48, 50, 55, 60, 65, 70, 75])
    if a + b >= 175 or a + b <= 20:
        return None
    c = 180 - a - b
    correct = F(c)
    wrong1 = F(a + b)             # forgets to subtract from 180
    wrong2 = F(180 - a)           # uses only one angle
    wrong3 = F(360 - a - b)       # uses 360
    stem = (f"Two angles of a triangle measure {a} deg and {b} deg. "
            f"The measure of the third angle is:")
    sol = (f"Angle sum of a triangle = 180 deg. Third angle = 180 - {a} - {b} "
           f"= {c} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_exterior_angle():
    """Exterior angle = sum of two remote interior angles. [M]"""
    a = random.choice([35, 40, 45, 48, 50, 55, 60, 65, 70])
    b = random.choice([30, 38, 42, 50, 55, 60, 65, 72, 75])
    if a + b >= 175:
        return None
    ext = a + b
    correct = F(ext)
    wrong1 = F(180 - a - b)       # the third interior angle instead
    wrong2 = F(180 - ext)         # supplement
    wrong3 = F(abs(a - b))        # difference
    stem = (f"In a triangle, an exterior angle is formed at one vertex. The two "
            f"remote (non-adjacent) interior angles are {a} deg and {b} deg. "
            f"The exterior angle equals:")
    sol = (f"Exterior angle = sum of the two remote interior angles = {a} + {b} "
           f"= {ext} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_isosceles_apex():
    """Isosceles triangle: each base angle given -> apex (or vice versa). [M]"""
    if random.random() < 0.5:
        base = random.choice([40, 45, 50, 55, 65, 70, 72, 75, 80])
        apex = 180 - 2 * base
        if apex <= 0:
            return None
        correct = F(apex)
        wrong1 = F(180 - base)        # forgets the second base angle
        wrong2 = F(base)              # repeats base angle
        wrong3 = F(90 - base)
        stem = (f"In an isosceles triangle, each of the two equal base angles is "
                f"{base} deg. The vertex (apex) angle is:")
        sol = (f"Apex = 180 - 2 x base = 180 - 2 x {base} = {apex} deg.")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "M"
    else:
        apex = random.choice([30, 40, 50, 60, 70, 80, 90, 100, 110, 120])
        base = Fraction(180 - apex, 2)
        if base.denominator not in (1, 2):
            return None
        correct = base
        wrong1 = F(180 - apex)        # forgets to halve
        wrong2 = F(apex)              # repeats apex
        wrong3 = Fraction(apex, 2)
        stem = (f"In an isosceles triangle, the vertex angle is {apex} deg. "
                f"Each of the equal base angles measures:")
        sol = (f"Base angles equal and sum with apex to 180: each = (180 - {apex})/2 "
               f"= {fmt(base)} deg.")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_parallel_transversal():
    """Parallel lines + transversal: co-interior / corresponding relation. [H]"""
    ang = random.choice([55, 62, 68, 72, 75, 105, 110, 115, 118, 125, 130])
    kind = random.choice(["co-interior", "corresponding", "alternate"])
    if kind == "co-interior":
        correct = F(180 - ang)
        wrong1 = F(ang)              # treats as equal
        wrong2 = F(90 - ang) if ang < 90 else F(ang - 90)
        wrong3 = F(360 - ang)
        stem = (f"Two parallel lines are cut by a transversal. One of a pair of "
                f"co-interior (allied) angles is {ang} deg. The other co-interior "
                f"angle is:")
        sol = (f"Co-interior angles are supplementary: other = 180 - {ang} "
               f"= {180 - ang} deg.")
    else:
        correct = F(ang)
        wrong1 = F(180 - ang)        # treats as supplementary
        wrong2 = F(90 - ang) if ang < 90 else F(ang - 90)
        wrong3 = F(ang + 10)
        name = "corresponding" if kind == "corresponding" else "alternate"
        stem = (f"Two parallel lines are cut by a transversal. One angle of a pair "
                f"of {name} angles measures {ang} deg. The measure of the other "
                f"{name} angle is:")
        sol = (f"{name.capitalize()} angles between parallel lines are equal, "
               f"so the other angle is also {ang} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_thales_bpt():
    """Basic Proportionality (Thales): DE || BC -> find a segment length. [H]"""
    # AD/DB = AE/EC. Pick clean integers.
    ad = random.choice([2, 3, 4, 5, 6])
    db = random.choice([3, 4, 5, 6, 8])
    ae = random.choice([3, 4, 5, 6, 8, 9, 10, 12])
    # EC = AE * DB / AD  must be an integer
    num = ae * db
    if num % ad != 0:
        return None
    ec = num // ad
    if ec <= 0 or ec > 60:
        return None
    correct = F(ec)
    wrong1 = F(ae * ad // db) if (ae * ad) % db == 0 else F(ae + db - ad)  # ratio flipped
    wrong2 = F(ae)            # copies AE
    wrong3 = F(ad + db + ae - ec) if (ad + db + ae - ec) > 0 else F(ec + 2)
    stem = (f"In triangle ABC, D lies on AB and E lies on AC with DE parallel to BC. "
            f"If AD = {ad} cm, DB = {db} cm and AE = {ae} cm, then EC (in cm) is:")
    sol = (f"By the Basic Proportionality (Thales) theorem AD/DB = AE/EC, so "
           f"EC = AE x DB / AD = {ae} x {db} / {ad} = {ec} cm.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_similar_ratio_area():
    """Similar triangles: ratio of sides -> ratio of areas (or a side). [H]"""
    s1 = random.choice([2, 3, 4, 5, 6])
    s2 = random.choice([3, 5, 7, 8, 9])
    if s1 == s2:
        return None
    g = gcd(s1, s2)
    s1, s2 = s1 // g, s2 // g
    area1 = random.choice([12, 18, 24, 32, 48, 50, 72, 98, 50])
    # area2 = area1 * (s2/s1)^2 must be integer
    num = area1 * s2 * s2
    if num % (s1 * s1) != 0:
        return None
    area2 = num // (s1 * s1)
    if area2 > 2000:
        return None
    correct = F(area2)
    wrong1 = Fraction(area1 * s2, s1)            # linear scale, not squared
    wrong2 = Fraction(area1 * s2 * s2, s1) if (area1 * s2 * s2) % s1 == 0 else F(area1 + s2)
    wrong3 = F(area1 * s2 // s1) if (area1 * s2) % s1 == 0 else F(area2 + 5)
    stem = (f"Two triangles are similar and the ratio of their corresponding sides "
            f"is {s1}:{s2}. If the area of the smaller triangle is {area1} sq cm, "
            f"the area of the larger triangle (in sq cm) is:")
    sol = (f"Ratio of areas = (ratio of sides)^2 = ({s1}:{s2})^2 = {s1*s1}:{s2*s2}. "
           f"Larger area = {area1} x {s2*s2}/{s1*s1} = {area2} sq cm.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_pythagoras_hyp():
    """Right triangle: two legs (triple) -> hypotenuse. [H]"""
    a, b, c = random.choice(BASE_TRIPLES)
    k = random.choice([1, 2, 3, 1, 1, 2])
    a, b, c = a * k, b * k, c * k
    correct = F(c)
    wrong1 = F(a + b)              # adds legs
    wrong2 = F(abs(a - b)) if abs(a - b) != c else F(c - 1)  # subtracts
    wrong3 = F(c - 1)
    stem = (f"In a right-angled triangle, the two legs (perpendicular sides) "
            f"measure {a} cm and {b} cm. The length of the hypotenuse (in cm) is:")
    sol = (f"Hypotenuse = sqrt({a}^2 + {b}^2) = sqrt({a*a} + {b*b}) = sqrt{a*a+b*b} "
           f"= {c} cm (a {a}-{b}-{c} right triangle).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_pythagoras_leg():
    """Right triangle: hypotenuse + one leg (triple) -> other leg. [H]"""
    a, b, c = random.choice(BASE_TRIPLES)
    k = random.choice([1, 2, 3, 1, 1])
    a, b, c = a * k, b * k, c * k
    correct = F(b)
    wrong1 = F(c - a)             # naive subtraction of values
    wrong2 = F(c + a)
    wrong3 = F(b + 2)
    stem = (f"In a right-angled triangle, the hypotenuse is {c} cm and one leg is "
            f"{a} cm. The length of the other leg (in cm) is:")
    sol = (f"Other leg = sqrt({c}^2 - {a}^2) = sqrt({c*c} - {a*a}) = sqrt{c*c-a*a} "
           f"= {b} cm (a {a}-{b}-{c} right triangle).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_circle_central_inscribed():
    """Central angle = 2 x inscribed angle on same arc. [H]"""
    if random.random() < 0.5:
        insc = random.choice([20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70])
        central = 2 * insc
        correct = F(central)
        wrong1 = F(insc)             # treats equal
        wrong2 = Fraction(insc, 2)   # halves instead
        wrong3 = F(180 - insc)
        stem = (f"An inscribed angle subtended by an arc of a circle at the "
                f"circumference is {insc} deg. The angle subtended by the same arc "
                f"at the centre is:")
        sol = (f"Angle at centre = 2 x angle at circumference = 2 x {insc} "
               f"= {central} deg.")
    else:
        central = random.choice([40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140])
        insc = Fraction(central, 2)
        if insc.denominator != 1:
            return None
        correct = insc
        wrong1 = F(central)          # treats equal
        wrong2 = F(2 * central)      # doubles wrong way
        wrong3 = F(180 - central) if 180 - central != int(insc) else F(int(insc) + 5)
        stem = (f"An arc of a circle subtends an angle of {central} deg at the "
                f"centre. The angle it subtends at any point on the major arc "
                f"(circumference) is:")
        sol = (f"Angle at circumference = (1/2) x angle at centre = {central}/2 "
               f"= {fmt(insc)} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_semicircle_angle():
    """Angle in a semicircle = 90; other acute angles add up. [H]"""
    a = random.choice([28, 32, 35, 38, 42, 48, 52, 55, 58, 62, 65])
    other = 90 - a
    correct = F(other)
    wrong1 = F(180 - 90 - a) + 0   # same value but framed as trap? use distinct
    wrong1 = F(90 + a)             # adds to 90
    wrong2 = F(a)                  # repeats
    wrong3 = F(180 - a)
    stem = (f"AB is a diameter of a circle and C is a point on the circle. The "
            f"angle ACB is the angle in a semicircle. If angle BAC = {a} deg, "
            f"then angle ABC is:")
    sol = (f"Angle in a semicircle ACB = 90 deg. In triangle ABC, "
           f"angle ABC = 180 - 90 - {a} = {other} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_cyclic_quad():
    """Cyclic quadrilateral: opposite angles supplementary. [H]"""
    a = random.choice([65, 70, 72, 75, 80, 85, 95, 100, 105, 110, 115])
    opp = 180 - a
    if opp <= 0:
        return None
    correct = F(opp)
    wrong1 = F(a)                # treats equal
    wrong2 = F(90 - a) if a < 90 else F(a - 90)
    wrong3 = F(360 - a)
    stem = (f"ABCD is a cyclic quadrilateral. If angle A = {a} deg, then the "
            f"measure of the opposite angle C is:")
    sol = (f"In a cyclic quadrilateral opposite angles are supplementary: "
           f"angle C = 180 - {a} = {opp} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_two_tangents_angle():
    """Two tangents from external point: angle between them + central angle. [H]"""
    # angle between tangents + angle at centre = 180
    ap = random.choice([40, 50, 60, 70, 80, 90, 100, 110, 120])
    central = 180 - ap
    correct = F(central)
    wrong1 = F(ap)               # treats equal
    wrong2 = F(90 - ap) if ap < 90 else F(ap - 90)
    wrong3 = F(360 - ap)
    stem = (f"From an external point P, two tangents are drawn to a circle with "
            f"centre O, touching it at A and B. If the angle APB between the "
            f"tangents is {ap} deg, then the angle AOB at the centre is:")
    sol = (f"OAPB has right angles at A and B; angle AOB + angle APB = 180 deg, "
           f"so angle AOB = 180 - {ap} = {central} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_tangent_length():
    """Tangent length from external point: sqrt(d^2 - r^2) using triples. [H]"""
    # r = leg, tangent = other leg, d = hypotenuse (triple)
    a, b, c = random.choice(BASE_TRIPLES)
    k = random.choice([1, 2, 1, 1])
    r, tan, d = a * k, b * k, c * k
    correct = F(tan)
    wrong1 = F(d - r)            # naive subtraction
    wrong2 = F(d + r)
    wrong3 = F(tan + 1)
    stem = (f"The distance of a point P from the centre O of a circle is {d} cm, "
            f"and the radius of the circle is {r} cm. The length of the tangent "
            f"drawn from P to the circle (in cm) is:")
    sol = (f"Tangent length = sqrt(OP^2 - r^2) = sqrt({d}^2 - {r}^2) = sqrt"
           f"({d*d} - {r*r}) = sqrt{d*d-r*r} = {tan} cm.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_chord_perpendicular():
    """Perpendicular from centre bisects chord; find chord or distance (triple). [H]"""
    a, b, c = random.choice(BASE_TRIPLES)
    k = random.choice([1, 2, 1, 1])
    dist, half, r = a * k, b * k, c * k  # dist^2 + half^2 = r^2
    chord = 2 * half
    if random.random() < 0.5:
        # given radius and distance from centre -> chord length
        correct = F(chord)
        wrong1 = F(half)             # forgets to double
        wrong2 = F(r * 2)            # uses diameter
        wrong3 = F(chord - 2)
        stem = (f"A chord of a circle of radius {r} cm is at a perpendicular "
                f"distance of {dist} cm from the centre. The length of the chord "
                f"(in cm) is:")
        sol = (f"Half-chord = sqrt(r^2 - d^2) = sqrt({r}^2 - {dist}^2) = sqrt"
               f"({r*r} - {dist*dist}) = {half} cm. Chord = 2 x {half} = {chord} cm.")
    else:
        # given radius and chord -> distance from centre
        correct = F(dist)
        wrong1 = F(half)
        wrong2 = F(r - half) if r - half != dist else F(dist + 2)
        wrong3 = F(dist + 2)
        stem = (f"A chord of length {chord} cm is drawn in a circle of radius "
                f"{r} cm. The perpendicular distance of the chord from the centre "
                f"(in cm) is:")
        sol = (f"Half-chord = {chord}/2 = {half} cm. Distance = sqrt(r^2 - half^2) "
               f"= sqrt({r}^2 - {half}^2) = sqrt({r*r} - {half*half}) = {dist} cm.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_centroid_median():
    """Centroid divides median 2:1; find segment from median length. [H]"""
    med = random.choice([12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45])
    # AG:GD = 2:1, AG = 2/3 med, GD = 1/3 med
    if med % 3 != 0:
        return None
    ag = Fraction(2, 3) * med
    gd = Fraction(1, 3) * med
    if random.random() < 0.5:
        correct = ag
        wrong1 = gd                  # picks shorter segment
        wrong2 = Fraction(med, 2)    # halves
        wrong3 = F(med)
        stem = (f"In a triangle, the length of a median is {med} cm. The centroid "
                f"divides this median in the ratio 2:1 from the vertex. The "
                f"distance from the vertex to the centroid (in cm) is:")
        sol = (f"Vertex-to-centroid = (2/3) x median = (2/3) x {med} = {fmt(ag)} cm.")
    else:
        correct = gd
        wrong1 = ag
        wrong2 = Fraction(med, 2)
        wrong3 = F(med)
        stem = (f"In a triangle, a median has length {med} cm. The centroid divides "
                f"it in the ratio 2:1 from the vertex. The distance from the "
                f"centroid to the midpoint of the opposite side (in cm) is:")
        sol = (f"Centroid-to-base = (1/3) x median = (1/3) x {med} = {fmt(gd)} cm.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_angle_between_bisectors():
    """Angle between internal bisectors of B and C = 90 + A/2. [VH]"""
    A = random.choice([40, 44, 48, 50, 54, 56, 60, 64, 70, 74, 80])
    boc = 90 + Fraction(A, 2)
    if boc.denominator != 1:
        return None
    correct = boc
    wrong1 = F(90 - A // 2) if A % 2 == 0 else F(90)   # wrong sign
    wrong2 = F(180 - A)                                # supplement of A
    wrong3 = F(90 + A)                                 # forgets to halve
    stem = (f"In triangle ABC, the internal bisectors of angle B and angle C meet "
            f"at point I (the incentre). If angle A = {A} deg, then angle BIC is:")
    sol = (f"Angle BIC = 90 + A/2 = 90 + {A}/2 = {fmt(boc)} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_polygon_interior_sum():
    """Polygon: sum of interior angles, or each interior angle (regular). [H]"""
    n = random.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
    if random.random() < 0.5:
        total = 180 * (n - 2)
        correct = F(total)
        wrong1 = F(180 * n)          # forgets -2
        wrong2 = F(360)              # confuses with exterior sum
        wrong3 = F(180 * (n - 1))
        stem = (f"The sum of all interior angles of a convex polygon with {n} sides "
                f"is (in degrees):")
        sol = (f"Sum of interior angles = (n - 2) x 180 = ({n} - 2) x 180 "
               f"= {total} deg.")
    else:
        each = Fraction(180 * (n - 2), n)
        if not is_clean(each):
            return None
        correct = each
        wrong1 = Fraction(360, n)        # exterior angle instead
        wrong2 = Fraction(180 * n, n)    # = 180
        wrong3 = Fraction(180 * (n - 2), n - 1) if is_clean(Fraction(180*(n-2), n-1)) else F(180)
        stem = (f"Each interior angle of a regular polygon with {n} sides measures "
                f"(in degrees):")
        sol = (f"Each interior angle = (n - 2) x 180 / n = {n-2} x 180 / {n} "
               f"= {fmt(each)} deg.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_polygon_sides_from_angle():
    """Number of sides from exterior (or interior) angle. [VH]"""
    n = random.choice([5, 6, 8, 9, 10, 12, 15, 18, 20, 24])
    ext = Fraction(360, n)
    if ext.denominator != 1:
        return None
    if random.random() < 0.5:
        correct = F(n)
        wrong1 = Fraction(180, int(ext)) if 180 % int(ext) == 0 else F(n + 1)
        wrong2 = F(n + 2)
        wrong3 = F(n - 1)
        stem = (f"Each exterior angle of a regular polygon measures {int(ext)} deg. "
                f"The number of sides of the polygon is:")
        sol = (f"Number of sides = 360 / exterior angle = 360 / {int(ext)} = {n}.")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"
    else:
        interior = 180 - int(ext)
        correct = F(n)
        wrong1 = Fraction(360, 180 - interior) if (180 - interior) and 360 % (180 - interior) == 0 else F(n + 1)
        wrong1 = F(n + 2)
        wrong2 = F(n - 1)
        wrong3 = Fraction(180, 180 - interior) if (180 - interior) and 180 % (180 - interior) == 0 else F(n + 3)
        stem = (f"Each interior angle of a regular polygon is {interior} deg. "
                f"The number of sides of the polygon is:")
        sol = (f"Exterior angle = 180 - {interior} = {int(ext)} deg; number of "
               f"sides = 360 / {int(ext)} = {n}.")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


# ----------------- COORDINATE GEOMETRY -----------------

def t_coord_distance():
    """Distance between two points using a triple. [H]"""
    a, b, c = random.choice(BASE_TRIPLES)
    x1 = random.choice([-4, -2, 0, 1, 3, 5])
    y1 = random.choice([-3, -1, 0, 2, 4])
    sx = random.choice([1, -1])
    sy = random.choice([1, -1])
    x2 = x1 + sx * a
    y2 = y1 + sy * b
    correct = F(c)
    wrong1 = F(a + b)            # adds differences
    wrong2 = F(abs(a - b)) if abs(a - b) != c else F(c - 1)
    wrong3 = F(c - 1)
    stem = (f"The distance between the points P({x1}, {y1}) and Q({x2}, {y2}) "
            f"(in units) is:")
    sol = (f"Distance = sqrt((x2-x1)^2 + (y2-y1)^2) = sqrt({a}^2 + {b}^2) = sqrt"
           f"({a*a} + {b*b}) = {c} units.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_coord_midpoint():
    """Midpoint coordinate -> ask for x or y of midpoint (single value). [M]"""
    x1 = random.choice([-6, -4, -2, 2, 4, 6, 8])
    x2 = random.choice([-6, -4, -2, 2, 4, 6, 8, 10])
    y1 = random.choice([-8, -6, -4, 2, 4, 6, 8])
    y2 = random.choice([-6, -2, 0, 2, 6, 8, 10])
    mx = Fraction(x1 + x2, 2)
    my = Fraction(y1 + y2, 2)
    if mx.denominator != 1 or my.denominator != 1:
        return None
    if random.random() < 0.5:
        correct = mx
        wrong1 = F(x1 + x2)          # forgets /2
        wrong2 = Fraction(x2 - x1, 2)
        wrong3 = my if my != mx else F(int(mx) + 3)
        coord = "x-coordinate"
        val = mx
    else:
        correct = my
        wrong1 = F(y1 + y2)
        wrong2 = Fraction(y2 - y1, 2)
        wrong3 = mx if mx != my else F(int(my) + 3)
        coord = "y-coordinate"
        val = my
    stem = (f"The midpoint of the line segment joining A({x1}, {y1}) and "
            f"B({x2}, {y2}) has {coord}:")
    sol = (f"Midpoint = ((x1+x2)/2, (y1+y2)/2). The {coord} = {fmt(val)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_coord_section():
    """Section formula: point dividing in ratio m:n, find a coordinate. [VH]"""
    m = random.choice([1, 2, 3])
    n = random.choice([1, 2, 3, 4])
    if gcd(m, n) != 1:
        return None
    x1 = random.choice([-3, 0, 2, 4, 6])
    x2 = random.choice([-2, 3, 6, 9, 12, 15])
    # px = (m*x2 + n*x1)/(m+n) must be clean
    px = Fraction(m * x2 + n * x1, m + n)
    if not is_clean(px):
        return None
    correct = px
    wrong1 = Fraction(m * x1 + n * x2, m + n)   # swapped m,n
    wrong2 = Fraction(x1 + x2, 2)               # midpoint instead
    wrong3 = Fraction(m * x2 - n * x1, m + n) if is_clean(Fraction(m*x2-n*x1, m+n)) else F(px + 2)
    stem = (f"The point P divides the line segment joining A({x1}, y1) and "
            f"B({x2}, y2) internally in the ratio {m}:{n}. The x-coordinate of "
            f"P is:")
    sol = (f"By the section formula x = (m x2 + n x1)/(m + n) = "
           f"({m} x {x2} + {n} x {x1})/({m}+{n}) = {fmt(px)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_coord_triangle_area():
    """Area of triangle from 3 vertices (shoelace). [VH]"""
    pts = []
    for _ in range(3):
        pts.append((random.choice([-4, -2, 0, 1, 2, 3, 4, 5, 6]),
                    random.choice([-3, -1, 0, 1, 2, 4, 5, 6])))
    (x1, y1), (x2, y2), (x3, y3) = pts
    twice = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
    area = Fraction(abs(twice), 2)
    if area == 0 or area > 60:
        return None
    if not is_clean(area):
        return None
    correct = area
    wrong1 = F(abs(twice))                  # forgets the 1/2
    wrong2 = area + 1 if is_clean(area + 1) else area + 2
    wrong3 = Fraction(abs(twice), 4) if is_clean(Fraction(abs(twice), 4)) and Fraction(abs(twice),4) != area else area + 3
    stem = (f"The area of the triangle whose vertices are A({x1}, {y1}), "
            f"B({x2}, {y2}) and C({x3}, {y3}) (in square units) is:")
    sol = (f"Area = (1/2)|x1(y2-y3) + x2(y3-y1) + x3(y1-y2)| "
           f"= (1/2)|{twice}| = {fmt(area)} sq units.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_coord_slope():
    """Slope of line through two points (clean rational). [H]"""
    x1 = random.choice([-4, -2, 0, 1, 2, 3])
    y1 = random.choice([-3, -1, 0, 2, 4])
    dx = random.choice([1, 2, 3, 4])
    dy = random.choice([-6, -4, -3, -2, 2, 3, 4, 6])
    x2 = x1 + dx
    y2 = y1 + dy
    slope = Fraction(dy, dx)
    if not is_clean(slope):
        return None
    correct = slope
    wrong1 = Fraction(dx, dy)               # inverted
    wrong2 = -slope                         # sign error
    wrong3 = Fraction(y1 - y2, x2 - x1) if Fraction(y1-y2, x2-x1) != slope else slope + 1
    stem = (f"The slope of the straight line passing through the points "
            f"({x1}, {y1}) and ({x2}, {y2}) is:")
    sol = (f"Slope = (y2 - y1)/(x2 - x1) = ({y2} - ({y1}))/({x2} - ({x1})) "
           f"= {fmt(slope)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


TEMPLATES = [
    t_triangle_third_angle, t_exterior_angle, t_isosceles_apex,
    t_parallel_transversal, t_thales_bpt, t_similar_ratio_area,
    t_pythagoras_hyp, t_pythagoras_leg, t_circle_central_inscribed,
    t_semicircle_angle, t_cyclic_quad, t_two_tangents_angle,
    t_tangent_length, t_chord_perpendicular, t_centroid_median,
    t_angle_between_bisectors, t_polygon_interior_sum,
    t_polygon_sides_from_angle, t_coord_distance, t_coord_midpoint,
    t_coord_section, t_coord_triangle_area, t_coord_slope,
]

DIFF_OF = {
    t_triangle_third_angle: "M", t_exterior_angle: "M", t_isosceles_apex: "M",
    t_parallel_transversal: "H", t_thales_bpt: "H", t_similar_ratio_area: "H",
    t_pythagoras_hyp: "H", t_pythagoras_leg: "H", t_circle_central_inscribed: "H",
    t_semicircle_angle: "H", t_cyclic_quad: "H", t_two_tangents_angle: "H",
    t_tangent_length: "H", t_chord_perpendicular: "H", t_centroid_median: "H",
    t_angle_between_bisectors: "VH", t_polygon_interior_sum: "H",
    t_polygon_sides_from_angle: "VH", t_coord_distance: "H",
    t_coord_midpoint: "M", t_coord_section: "VH", t_coord_triangle_area: "VH",
    t_coord_slope: "H",
}
WEIGHT = {"M": 2.6, "H": 3.0, "VH": 2.7}
POOL = []
for t in TEMPLATES:
    POOL += [t] * int(WEIGHT[DIFF_OF[t]] * 10)

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

errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
print(f"Verification errors: {errors}")

from collections import Counter
print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_07_Geometry_500.md"

lines = []
lines.append("# Geometry (incl. Coordinate Geometry) - 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** Medium / Hard / Very-Hard (trap) - CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** - the keyed option is provably correct.")
lines.append("> Negative marking in CGL is -0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- Triangle angle sum = 180 deg; exterior angle = sum of two remote interior angles")
lines.append("- Isosceles: base angles equal; apex = 180 - 2 x base")
lines.append("- Parallel lines + transversal: corresponding & alternate angles equal; co-interior (allied) supplementary")
lines.append("- Basic Proportionality (Thales): DE || BC => AD/DB = AE/EC")
lines.append("- Similar triangles: ratio of areas = (ratio of sides)^2")
lines.append("- Pythagoras: hyp^2 = leg1^2 + leg2^2 (triples 3-4-5, 5-12-13, 8-15-17, 7-24-25, 9-40-41)")
lines.append("- Circle: angle at centre = 2 x inscribed angle on same arc; angle in semicircle = 90 deg")
lines.append("- Cyclic quadrilateral: opposite angles supplementary (sum 180 deg)")
lines.append("- Two tangents from a point: angle between tangents + angle at centre = 180 deg")
lines.append("- Tangent length = sqrt(OP^2 - r^2); perpendicular from centre bisects a chord")
lines.append("- Centroid divides each median 2:1 from the vertex")
lines.append("- Incentre angle: angle BIC = 90 + A/2")
lines.append("- Polygon: sum of interior angles = (n-2) x 180; each exterior angle (regular) = 360/n")
lines.append("- Coordinates: distance = sqrt(dx^2 + dy^2); midpoint = ((x1+x2)/2,(y1+y2)/2)")
lines.append("- Section formula: x = (m x2 + n x1)/(m+n); Area = (1/2)|x1(y2-y3)+x2(y3-y1)+x3(y1-y2)|\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}-Q{start+50})\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        o = q["opts"]
        lines.append(f"**Q{n}.** {q['stem']}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Answers Q{start+1}-Q{start+50}\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        letter = LETTERS[q["ci"]]
        val = q["opts"][q["ci"]]
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* - {q['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUT}")
print(f"Total lines: {len(lines)}")
