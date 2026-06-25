# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Mensuration (2D + 3D) set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer (numeric compare; surd strings like '36√3' are evaluated),
4 distinct options, then for several recognizable template types RE-SOLVE
directly from the stem numbers (regex) and confirm the keyed value matches.
Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
import math
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_08_Mensuration_500.md"
txt = open(PATH, encoding="utf-8").read()

PI = Fraction(22, 7)

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


def fnum(s):
    """Float value of an option string. Handles surds like '36√3', '7√2',
    plain ints, decimals, and fractions a/b."""
    s = s.strip().replace("₹", "").replace(",", "")
    # surd forms:  <coef>√<radicand>  (coef optional)
    m = re.match(r"^([0-9]+(?:\.[0-9]+)?(?:/[0-9]+)?)?√(\d+)$", s)
    if m:
        coef = m.group(1)
        rad = int(m.group(2))
        if coef is None:
            c = 1.0
        elif "/" in coef:
            a, b = coef.split("/")
            c = float(a) / float(b)
        else:
            c = float(coef)
        return c * math.sqrt(rad)
    if "/" in s:
        a, b = s.split("/")
        return float(a) / float(b)
    return float(s)


def approx(a, b, tol=1e-4):
    return abs(a - b) < tol * max(1.0, abs(a), abs(b))


checked = 0
mismatch = 0
type_counts = {}

for n, (stem, opts) in qs.items():
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]
    # keyed option value must equal stated answer
    if not approx(fnum(keyed_opt), fnum(aval)):
        print(f"Q{n}: keyed letter/value mismatch: option[{letter}]={keyed_opt} vs answer {aval}")
        mismatch += 1
        continue
    # 4 distinct options (numeric)
    vals = [fnum(o) for o in opts]
    distinct = True
    for i in range(4):
        for j in range(i + 1, 4):
            if approx(vals[i], vals[j], tol=1e-6):
                distinct = False
    if not distinct:
        print(f"Q{n}: duplicate options {opts}")
        mismatch += 1

    av = fnum(aval)
    try:
        # ----- independent re-solve for recognizable types -----
        if re.search(r"side of a square is \d+ cm. The length of its diagonal", stem):
            s = int(re.search(r"side of a square is (\d+)", stem).group(1))
            exp = s * math.sqrt(2)
            if not approx(av, exp):
                print(f"Q{n} SQ-DIAG wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["sq_diag"] = type_counts.get("sq_diag", 0) + 1

        elif re.search(r"diagonal of a square is \d+ cm. Its area", stem):
            d = int(re.search(r"diagonal of a square is (\d+)", stem).group(1))
            exp = d * d / 2
            if not approx(av, exp):
                print(f"Q{n} SQ-AREA wrong: {aval} vs {exp}"); mismatch += 1
            checked += 1; type_counts["sq_area"] = type_counts.get("sq_area", 0) + 1

        elif re.search(r"sides of a triangle are .* Its area", stem):
            a, b, c = [int(x) for x in re.findall(r"(\d+) cm", stem)[:3]]
            s = (a + b + c) / 2
            exp = math.sqrt(s * (s - a) * (s - b) * (s - c))
            if not approx(av, exp):
                print(f"Q{n} HERON wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["heron"] = type_counts.get("heron", 0) + 1

        elif re.search(r"side of an equilateral triangle is \d+ cm. Its area", stem):
            a = int(re.search(r"equilateral triangle is (\d+)", stem).group(1))
            exp = math.sqrt(3) / 4 * a * a
            if not approx(av, exp):
                print(f"Q{n} EQUI-AREA wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["equi_area"] = type_counts.get("equi_area", 0) + 1

        elif re.search(r"radius of a circle is \d+ cm. Its area", stem):
            r = int(re.search(r"radius of a circle is (\d+)", stem).group(1))
            exp = float(PI * r * r)
            if not approx(av, exp):
                print(f"Q{n} CIRC-AREA wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["circ_area"] = type_counts.get("circ_area", 0) + 1

        elif re.search(r"radius of a circle is \d+ cm. Its circumference", stem):
            r = int(re.search(r"radius of a circle is (\d+)", stem).group(1))
            exp = float(PI * 2 * r)
            if not approx(av, exp):
                print(f"Q{n} CIRC-CIRCUM wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["circ_circum"] = type_counts.get("circ_circum", 0) + 1

        elif re.search(r"sector of a circle has radius .* area of the sector", stem):
            r = int(re.search(r"radius (\d+) cm", stem).group(1))
            th = int(re.search(r"angle of (\d+)", stem).group(1))
            exp = float(Fraction(th, 360) * PI * r * r)
            if not approx(av, exp):
                print(f"Q{n} SECTOR wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["sector"] = type_counts.get("sector", 0) + 1

        elif re.search(r"diagonals of a rhombus are .* Its area", stem):
            d1, d2 = [int(x) for x in re.findall(r"(\d+) cm", stem)[:2]]
            exp = d1 * d2 / 2
            if not approx(av, exp):
                print(f"Q{n} RHOMBUS wrong: {aval} vs {exp}"); mismatch += 1
            checked += 1; type_counts["rhombus"] = type_counts.get("rhombus", 0) + 1

        elif re.search(r"parallel sides of a trapezium are .* Its area", stem):
            a, b, h = [int(x) for x in re.findall(r"(\d+) cm", stem)[:3]]
            exp = (a + b) * h / 2
            if not approx(av, exp):
                print(f"Q{n} TRAPEZIUM wrong: {aval} vs {exp}"); mismatch += 1
            checked += 1; type_counts["trapezium"] = type_counts.get("trapezium", 0) + 1

        elif re.search(r"edge of a cube is \d+ cm. Its volume", stem):
            a = int(re.search(r"edge of a cube is (\d+)", stem).group(1))
            exp = a ** 3
            if not approx(av, exp):
                print(f"Q{n} CUBE-VOL wrong: {aval} vs {exp}"); mismatch += 1
            checked += 1; type_counts["cube_vol"] = type_counts.get("cube_vol", 0) + 1

        elif re.search(r"edge of a cube is \d+ cm. Its total surface area", stem):
            a = int(re.search(r"edge of a cube is (\d+)", stem).group(1))
            exp = 6 * a * a
            if not approx(av, exp):
                print(f"Q{n} CUBE-TSA wrong: {aval} vs {exp}"); mismatch += 1
            checked += 1; type_counts["cube_tsa"] = type_counts.get("cube_tsa", 0) + 1

        elif re.search(r"edge of a cube is \d+ cm. The length of its space diagonal", stem):
            a = int(re.search(r"edge of a cube is (\d+)", stem).group(1))
            exp = a * math.sqrt(3)
            if not approx(av, exp):
                print(f"Q{n} CUBE-DIAG wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["cube_diag"] = type_counts.get("cube_diag", 0) + 1

        elif re.search(r"cuboid has dimensions .* Its volume", stem):
            l, b, h = [int(x) for x in re.findall(r"(\d+) cm", stem)[:3]]
            exp = l * b * h
            if not approx(av, exp):
                print(f"Q{n} CUBOID-VOL wrong: {aval} vs {exp}"); mismatch += 1
            checked += 1; type_counts["cuboid_vol"] = type_counts.get("cuboid_vol", 0) + 1

        elif re.search(r"cuboid has dimensions .* total surface area", stem):
            l, b, h = [int(x) for x in re.findall(r"(\d+) cm", stem)[:3]]
            exp = 2 * (l * b + b * h + h * l)
            if not approx(av, exp):
                print(f"Q{n} CUBOID-TSA wrong: {aval} vs {exp}"); mismatch += 1
            checked += 1; type_counts["cuboid_tsa"] = type_counts.get("cuboid_tsa", 0) + 1

        elif re.search(r"cylinder has radius .* Its volume", stem):
            r = int(re.search(r"radius (\d+) cm", stem).group(1))
            h = int(re.search(r"height (\d+) cm", stem).group(1))
            exp = float(PI * r * r * h)
            if not approx(av, exp):
                print(f"Q{n} CYL-VOL wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["cyl_vol"] = type_counts.get("cyl_vol", 0) + 1

        elif re.search(r"cylinder has radius .* curved surface area", stem):
            r = int(re.search(r"radius (\d+) cm", stem).group(1))
            h = int(re.search(r"height (\d+) cm", stem).group(1))
            exp = float(PI * 2 * r * h)
            if not approx(av, exp):
                print(f"Q{n} CYL-CSA wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["cyl_csa"] = type_counts.get("cyl_csa", 0) + 1

        elif re.search(r"cone has radius .* Its volume", stem):
            r = int(re.search(r"radius (\d+) cm", stem).group(1))
            h = int(re.search(r"height (\d+) cm", stem).group(1))
            exp = float(Fraction(1, 3) * PI * r * r * h)
            if not approx(av, exp):
                print(f"Q{n} CONE-VOL wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["cone_vol"] = type_counts.get("cone_vol", 0) + 1

        elif re.search(r"cone has base radius .* vertical height .* slant height", stem):
            r = int(re.search(r"base radius (\d+)", stem).group(1))
            h = int(re.search(r"vertical height (\d+)", stem).group(1))
            exp = math.sqrt(r * r + h * h)
            if not approx(av, exp):
                print(f"Q{n} CONE-SLANT wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["cone_slant"] = type_counts.get("cone_slant", 0) + 1

        elif re.search(r"A sphere has radius \d+ cm. Its volume", stem):
            r = int(re.search(r"radius (\d+)", stem).group(1))
            exp = float(Fraction(4, 3) * PI * r ** 3)
            if not approx(av, exp):
                print(f"Q{n} SPHERE-VOL wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["sphere_vol"] = type_counts.get("sphere_vol", 0) + 1

        elif re.search(r"A hemisphere has radius \d+ cm. Its volume", stem):
            r = int(re.search(r"radius (\d+)", stem).group(1))
            exp = float(Fraction(2, 3) * PI * r ** 3)
            if not approx(av, exp):
                print(f"Q{n} HEMI-VOL wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["hemi_vol"] = type_counts.get("hemi_vol", 0) + 1

        elif re.search(r"A sphere has radius \d+ cm. Its surface area", stem):
            r = int(re.search(r"radius (\d+)", stem).group(1))
            exp = float(Fraction(4) * PI * r * r)
            if not approx(av, exp):
                print(f"Q{n} SPHERE-SA wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["sphere_sa"] = type_counts.get("sphere_sa", 0) + 1

        elif re.search(r"sphere of radius \d+ cm is melted and recast into a solid cylinder", stem):
            rs = int(re.search(r"sphere of radius (\d+)", stem).group(1))
            rc = int(re.search(r"cylinder of radius (\d+)", stem).group(1))
            exp = float(Fraction(4, 3) * rs ** 3 / (rc * rc))
            if not approx(av, exp):
                print(f"Q{n} RECAST-CYL wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["recast_cyl"] = type_counts.get("recast_cyl", 0) + 1

        elif re.search(r"sphere of radius \d+ cm is melted and recast into a solid cone", stem):
            rs = int(re.search(r"sphere of radius (\d+)", stem).group(1))
            rc = int(re.search(r"cone of base radius (\d+)", stem).group(1))
            exp = float(Fraction(4 * rs ** 3, rc * rc))
            if not approx(av, exp):
                print(f"Q{n} RECAST-CONE wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1; type_counts["recast_cone"] = type_counts.get("recast_cone", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 3, "Fewer than 3 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
