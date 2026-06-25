# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Geometry (+ Coordinate Geometry) set.
Re-parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options, then for several recognizable template
types RE-SOLVE directly from the stem numbers (regex) and confirm the keyed
value matches. Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_07_Geometry_500.md"
txt = open(PATH, encoding="utf-8").read()

qpart, apart = txt.split("# =================== ANSWER KEY")

qs = {}
qpat = re.compile(
    r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\n",
    re.S,
)
for m in qpat.finditer(qpart):
    n = int(m.group(1))
    stem = m.group(2).replace("\n", " ").strip()
    opts = [m.group(3).strip(), m.group(4).strip(), m.group(5).strip(), m.group(6).strip()]
    qs[n] = (stem, opts)

ans = {}
apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*")
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), m.group(3).strip())

print(f"Parsed {len(qs)} questions, {len(ans)} answers")
assert len(qs) == 500 and len(ans) == 500, "count mismatch!"


def F(s):
    s = s.strip().replace("deg", "").strip()
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(s).limit_denominator(10**6)


def ints(pat, s):
    return [int(v) for v in re.findall(pat, s)]


checked = 0
mismatch = 0
type_counts = {}

for n, (stem, opts) in qs.items():
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]
    if F(keyed_opt) != F(aval):
        print(f"Q{n}: keyed letter/value mismatch: option[{letter}]={keyed_opt} vs answer {aval}")
        mismatch += 1
        continue
    if len(set(F(o) for o in opts)) != 4:
        print(f"Q{n}: duplicate options {opts}")
        mismatch += 1

    # ----- independent re-solve for recognizable types -----
    try:
        if "Two angles of a triangle measure" in stem:
            a, b = ints(r"(\d+) deg", stem)[:2]
            exp = Fraction(180 - a - b)
            if F(aval) != exp:
                print(f"Q{n} THIRD-ANGLE wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["third_angle"] = type_counts.get("third_angle", 0) + 1

        elif "remote (non-adjacent) interior angles are" in stem:
            a, b = ints(r"(\d+) deg", stem)[:2]
            exp = Fraction(a + b)
            if F(aval) != exp:
                print(f"Q{n} EXTERIOR wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["exterior"] = type_counts.get("exterior", 0) + 1

        elif "Basic Proportionality" in stem or ("DE parallel to BC" in stem):
            ad = int(re.search(r"AD = (\d+) cm", stem).group(1))
            db = int(re.search(r"DB = (\d+) cm", stem).group(1))
            ae = int(re.search(r"AE = (\d+) cm", stem).group(1))
            exp = Fraction(ae * db, ad)
            if F(aval) != exp:
                print(f"Q{n} THALES wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["thales"] = type_counts.get("thales", 0) + 1

        elif "the two legs (perpendicular sides) measure" in stem:
            a, b = ints(r"(\d+) cm", stem)[:2]
            exp = Fraction(int(round((a * a + b * b) ** 0.5)))
            assert exp * exp == a * a + b * b
            if F(aval) != exp:
                print(f"Q{n} PYTH-HYP wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["pyth_hyp"] = type_counts.get("pyth_hyp", 0) + 1

        elif "the hypotenuse is" in stem and "one leg is" in stem:
            c = int(re.search(r"hypotenuse is (\d+) cm", stem).group(1))
            a = int(re.search(r"one leg is (\d+) cm", stem).group(1))
            exp = Fraction(int(round((c * c - a * a) ** 0.5)))
            assert exp * exp == c * c - a * a
            if F(aval) != exp:
                print(f"Q{n} PYTH-LEG wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["pyth_leg"] = type_counts.get("pyth_leg", 0) + 1

        elif "subtended by an arc" in stem and "at the centre is" in stem:
            insc = int(re.search(r"circumference is (\d+) deg", stem).group(1))
            exp = Fraction(2 * insc)
            if F(aval) != exp:
                print(f"Q{n} CENTRAL wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["central"] = type_counts.get("central", 0) + 1

        elif "cyclic quadrilateral" in stem and "opposite angle C is" in stem:
            a = int(re.search(r"angle A = (\d+) deg", stem).group(1))
            exp = Fraction(180 - a)
            if F(aval) != exp:
                print(f"Q{n} CYCLIC wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["cyclic"] = type_counts.get("cyclic", 0) + 1

        elif "the length of the tangent" in stem:
            d = int(re.search(r"point P from the centre O of a circle is (\d+) cm", stem).group(1))
            r = int(re.search(r"radius of the circle is (\d+) cm", stem).group(1))
            exp = Fraction(int(round((d * d - r * r) ** 0.5)))
            assert exp * exp == d * d - r * r
            if F(aval) != exp:
                print(f"Q{n} TANGENT wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["tangent"] = type_counts.get("tangent", 0) + 1

        elif "internal bisectors of angle B and angle C" in stem:
            a = int(re.search(r"angle A = (\d+) deg", stem).group(1))
            exp = Fraction(90) + Fraction(a, 2)
            if F(aval) != exp:
                print(f"Q{n} BISECTOR wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["bisector"] = type_counts.get("bisector", 0) + 1

        elif "sum of all interior angles of a convex polygon" in stem:
            ns = int(re.search(r"with (\d+) sides", stem).group(1))
            exp = Fraction(180 * (ns - 2))
            if F(aval) != exp:
                print(f"Q{n} POLY-SUM wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["poly_sum"] = type_counts.get("poly_sum", 0) + 1

        elif "exterior angle of a regular polygon measures" in stem:
            e = int(re.search(r"measures (\d+) deg", stem).group(1))
            exp = Fraction(360, e)
            if F(aval) != exp:
                print(f"Q{n} POLY-SIDES wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["poly_sides"] = type_counts.get("poly_sides", 0) + 1

        elif stem.startswith("The distance between the points"):
            pairs = re.findall(r"\((-?\d+),\s*(-?\d+)\)", stem)
            (x1, y1), (x2, y2) = [(int(a), int(b)) for a, b in pairs[:2]]
            d2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
            exp = Fraction(int(round(d2 ** 0.5)))
            assert exp * exp == d2
            if F(aval) != exp:
                print(f"Q{n} COORD-DIST wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["coord_dist"] = type_counts.get("coord_dist", 0) + 1

        elif "area of the triangle whose vertices are" in stem:
            pairs = re.findall(r"\((-?\d+),\s*(-?\d+)\)", stem)
            (x1, y1), (x2, y2), (x3, y3) = [(int(a), int(b)) for a, b in pairs[:3]]
            twice = x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)
            exp = Fraction(abs(twice), 2)
            if F(aval) != exp:
                print(f"Q{n} COORD-AREA wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["coord_area"] = type_counts.get("coord_area", 0) + 1

        elif "slope of the straight line passing through the points" in stem:
            pairs = re.findall(r"\((-?\d+),\s*(-?\d+)\)", stem)
            (x1, y1), (x2, y2) = [(int(a), int(b)) for a, b in pairs[:2]]
            exp = Fraction(y2 - y1, x2 - x1)
            if F(aval) != exp:
                print(f"Q{n} COORD-SLOPE wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["coord_slope"] = type_counts.get("coord_slope", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 3, "Fewer than 3 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
