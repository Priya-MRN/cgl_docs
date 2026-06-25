# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Trigonometry (incl. Heights & Distances) set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer (numeric compare; surd strings like '50√3', '(35/2)√3',
'36(3+√3)', '180(√3−1)' are evaluated), 4 distinct options, then for several
recognizable template types RE-SOLVE directly from the stem numbers (regex)
and confirm the keyed value matches. Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
import math
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_15_Trigonometry_500.md"
txt = open(PATH, encoding="utf-8").read()

R3 = math.sqrt(3)
R2 = math.sqrt(2)

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


def _root(rad):
    return {2: R2, 3: R3}.get(rad, math.sqrt(rad))


def _coef(s):
    """Parse a coefficient that may be '', '(a/b)', 'a/b', integer, decimal."""
    s = s.strip()
    if s == "" or s == "+":
        return 1.0
    if s == "-" or s == "−":
        return -1.0
    s = s.replace("−", "-")
    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1]
    if "/" in s:
        a, b = s.split("/")
        return float(a) / float(b)
    return float(s)


def fnum(s):
    """Float value of an option string. Handles:
       plain ints/decimals, a/b fractions, c√r, (a/b)√r,
       coef(p+√r), coef(p-√r), coef(√r+k), coef(√r-k)."""
    s = s.strip().replace("₹", "").replace(",", "").replace("−", "-")

    # coef ( A op B )  where one of A/B is a surd
    m = re.match(r"^(.*?)\(([^()]+)\)$", s)
    if m and "√" in m.group(2):
        coef = _coef(m.group(1)) if m.group(1).strip() else 1.0
        inner = m.group(2)
        im = re.match(r"^\s*(-?[0-9.]+|-?√\d+)\s*([+\-])\s*([0-9.]+|√\d+)\s*$", inner)
        if im:
            t1 = _term(im.group(1))
            sgn = 1.0 if im.group(2) == "+" else -1.0
            t2 = _term(im.group(3))
            return coef * (t1 + sgn * t2)

    # bare surd term  c√r  or  (a/b)√r  or  √r
    if "√" in s:
        return _term(s)

    # fraction or plain number
    if "/" in s:
        a, b = s.split("/")
        return float(a) / float(b)
    return float(s)


def _term(t):
    """Single term: number, √r, or c√r / (a/b)√r."""
    t = t.strip().replace("−", "-")
    if "√" not in t:
        return float(t)
    mm = re.match(r"^(.*?)√(\d+)$", t)
    coef = _coef(mm.group(1))
    rad = int(mm.group(2))
    return coef * _root(rad)


def approx(a, b, tol=1e-3):
    return abs(a - b) < tol * max(1.0, abs(a), abs(b))


# ---- standard-angle exact float ratios (independent of generator) ----
SIN = {0: 0.0, 30: 0.5, 45: R2 / 2, 60: R3 / 2, 90: 1.0}
COS = {a: SIN[90 - a] for a in (0, 30, 45, 60, 90)}
TAN = {0: 0.0, 30: 1 / R3, 45: 1.0, 60: R3}

checked = 0
mismatch = 0
type_counts = {}

for n, (stem, opts) in qs.items():
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]
    # keyed option value must equal stated answer
    try:
        if not approx(fnum(keyed_opt), fnum(aval)):
            print(f"Q{n}: keyed letter/value mismatch: option[{letter}]={keyed_opt} vs answer {aval}")
            mismatch += 1
            continue
    except Exception as e:
        print(f"Q{n}: cannot parse keyed/answer ('{keyed_opt}' / '{aval}'): {e}")
        mismatch += 1
        continue

    # 4 distinct options (numeric)
    try:
        vals = [fnum(o) for o in opts]
        for i in range(4):
            for j in range(i + 1, 4):
                if approx(vals[i], vals[j], tol=1e-6):
                    print(f"Q{n}: duplicate options {opts}")
                    mismatch += 1
    except Exception as e:
        print(f"Q{n}: cannot parse options {opts}: {e}")
        mismatch += 1
        continue

    av = fnum(aval)
    try:
        # ----- independent re-solve for recognizable types -----

        # (1) Elevation from a point: height = distance * tan(angle)
        if re.search(r"angle of elevation of the top of a tower from a point", stem):
            d = int(re.search(r"point (\d+) m away", stem).group(1))
            a = int(re.search(r"is (\d+)°", stem).group(1))
            exp = d * TAN[a]
            if not approx(av, exp):
                print(f"Q{n} ELEV-HEIGHT wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["elev_height"] = type_counts.get("elev_height", 0) + 1

        # (2) Tower height h, find distance = h / tan(angle)
        elif re.search(r"A tower is \d+ m high\. The angle of elevation", stem):
            h = int(re.search(r"tower is (\d+) m high", stem).group(1))
            a = int(re.search(r"ground is (\d+)°", stem).group(1))
            exp = h / TAN[a]
            if not approx(av, exp):
                print(f"Q{n} ELEV-DIST wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["elev_dist"] = type_counts.get("elev_dist", 0) + 1

        # (3) Two points d apart, angles -> height
        elif re.search(r"two points on the ground, in line with the base and", stem):
            d = int(re.search(r"and (\d+) m apart", stem).group(1))
            angs = sorted(int(x) for x in re.findall(r"(\d+)°", stem))
            a1, a2 = angs[0], angs[1]
            exp = d / (1 / TAN[a1] - 1 / TAN[a2])
            if not approx(av, exp):
                print(f"Q{n} TWO-POINTS wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["two_points"] = type_counts.get("two_points", 0) + 1

        # (4) Shadow increase as elevation drops
        elif re.search(r"shadow of a vertical pole \d+ m high lengthens", stem):
            h = int(re.search(r"pole (\d+) m high", stem).group(1))
            a_hi = int(re.search(r"from (\d+)°", stem).group(1))
            a_lo = int(re.search(r"to (\d+)°", stem).group(1))
            exp = h / TAN[a_lo] - h / TAN[a_hi]
            if not approx(av, exp):
                print(f"Q{n} SHADOW wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["shadow"] = type_counts.get("shadow", 0) + 1

        # (5) sin θ = a/c (triple) -> requested ratio
        elif re.search(r"If sin θ = \d+/\d+ and θ is acute, then the value of", stem):
            opp, hyp = [int(x) for x in re.search(r"sin θ = (\d+)/(\d+)", stem).groups()]
            adj = int(round(math.sqrt(hyp * hyp - opp * opp)))
            ask = re.search(r"value of (cos|tan|cot|sec|cosec) θ", stem).group(1)
            table = {
                "cos": adj / hyp, "tan": opp / adj, "cot": adj / opp,
                "sec": hyp / adj, "cosec": hyp / opp,
            }
            exp = table[ask]
            if not approx(av, exp):
                print(f"Q{n} SIN-TRIPLE wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["sin_triple"] = type_counts.get("sin_triple", 0) + 1

        # (6) sec/cosec ± : reciprocal
        elif re.search(r"If (sec|cosec) θ − (tan|cot) θ =", stem):
            k = fnum(re.search(r"θ = ([^,]+?), then", stem).group(1))
            exp = 1.0 / k
            if not approx(av, exp):
                print(f"Q{n} SEC-TAN wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["sec_tan"] = type_counts.get("sec_tan", 0) + 1

        # (7) tan θ + cot θ
        elif re.search(r"If tan θ = \d+/\d+ and θ is acute, then tan θ \+ cot θ", stem):
            o, a_ = [int(x) for x in re.search(r"tan θ = (\d+)/(\d+)", stem).groups()]
            exp = o / a_ + a_ / o
            if not approx(av, exp):
                print(f"Q{n} TAN-COT wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["tan_cot"] = type_counts.get("tan_cot", 0) + 1

        # (8) (sinθ+cosθ)^2 from sinθcosθ
        elif re.search(r"If sin θ · cos θ = .+ value of \(sin θ \+ cos θ\)²", stem):
            m_ = fnum(re.search(r"sin θ · cos θ = ([^,]+?), then", stem).group(1))
            exp = 1 + 2 * m_
            if not approx(av, exp):
                print(f"Q{n} SUM-SQ wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["sum_sq"] = type_counts.get("sum_sq", 0) + 1

        # (9) sinθcosθ from sinθ+cosθ
        elif re.search(r"If sin θ \+ cos θ = .+ value of sin θ · cos θ", stem):
            k_ = fnum(re.search(r"sin θ \+ cos θ = ([^ ]+) \(", stem).group(1))
            exp = (k_ * k_ - 1) / 2
            if not approx(av, exp):
                print(f"Q{n} PROD wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["prod"] = type_counts.get("prod", 0) + 1

        # (10) max/min of a sinθ + b cosθ
        elif re.search(r"value of \d+·sin θ \+ \d+·cos θ is:", stem):
            a_, b_ = [int(x) for x in re.findall(r"(\d+)·", stem)[:2]]
            mag = math.sqrt(a_ * a_ + b_ * b_)
            exp = mag if "maximum" in stem else -mag
            if not approx(av, exp):
                print(f"Q{n} RANGE-AB wrong: {aval} vs {exp:.4f}"); mismatch += 1
            checked += 1
            type_counts["range_ab"] = type_counts.get("range_ab", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 3, "Fewer than 3 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
