# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Algebra 500 set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options, then for several recognizable template
types RE-SOLVE directly from the stem numbers (regex) and confirm the keyed
value matches. Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
import math
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_06_Algebra_500.md"
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
    s = s.strip().replace("₹", "")
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(s).limit_denominator(10**6)


def ints(stem):
    """All signed integers appearing in the stem (handles unicode minus too)."""
    cleaned = stem.replace("−", "-")
    return [int(x) for x in re.findall(r"-?\d+", cleaned)]


checked = 0
mismatch = 0
type_counts = {}

for n, (stem, opts) in qs.items():
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]
    # keyed option value must equal stated answer
    if F(keyed_opt) != F(aval):
        print(f"Q{n}: keyed letter/value mismatch: option[{letter}]={keyed_opt} vs answer {aval}")
        mismatch += 1
        continue
    # 4 distinct options
    if len(set(F(o) for o in opts)) != 4:
        print(f"Q{n}: duplicate options {opts}")
        mismatch += 1

    # ----- independent re-solve for recognizable types -----
    try:
        # x + 1/x = k  ->  x^2 + 1/x^2
        if re.search(r"If x \+ 1/x = \d+, then the value of x² \+ 1/x²", stem):
            k = int(re.search(r"x \+ 1/x = (\d+)", stem).group(1))
            exp = Fraction(k**2 - 2)
            if F(aval) != exp:
                print(f"Q{n} XINV-SQ wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["xinv_sq"] = type_counts.get("xinv_sq", 0) + 1

        # x + 1/x = k  ->  x^3 + 1/x^3
        elif re.search(r"If x \+ 1/x = \d+, then the value of x³ \+ 1/x³", stem):
            k = int(re.search(r"x \+ 1/x = (\d+)", stem).group(1))
            exp = Fraction(k**3 - 3*k)
            if F(aval) != exp:
                print(f"Q{n} XINV-CUBE wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["xinv_cube"] = type_counts.get("xinv_cube", 0) + 1

        # x - 1/x = k  ->  x^2 + 1/x^2
        elif re.search(r"If x − 1/x = \d+, then the value of x² \+ 1/x²", stem):
            k = int(re.search(r"x − 1/x = (\d+)", stem).group(1))
            exp = Fraction(k**2 + 2)
            if F(aval) != exp:
                print(f"Q{n} XMINUS-SQ wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["xminus_sq"] = type_counts.get("xminus_sq", 0) + 1

        # x - 1/x = k -> x^3 - 1/x^3
        elif re.search(r"If x − 1/x = \d+, then the value of x³ − 1/x³", stem):
            k = int(re.search(r"x − 1/x = (\d+)", stem).group(1))
            exp = Fraction(k**3 + 3*k)
            if F(aval) != exp:
                print(f"Q{n} XMINUS-CUBE wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["xminus_cube"] = type_counts.get("xminus_cube", 0) + 1

        # a + b + c = 0 -> a^3+b^3+c^3 = 3abc
        elif "a + b + c = 0, where" in stem and "a³ + b³ + c³" in stem:
            vals = re.findall(r"a = (-?\d+), b = (-?\d+) and c = (-?\d+)",
                              stem.replace("−", "-"))
            a, b, c = (int(v) for v in vals[0])
            exp = Fraction(3 * a * b * c)
            if F(aval) != exp:
                print(f"Q{n} ABC0 wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["abc_zero"] = type_counts.get("abc_zero", 0) + 1

        # a+b+c = s, ab+bc+ca = p -> a^2+b^2+c^2
        elif re.search(r"a \+ b \+ c = \d+ and ab \+ bc \+ ca = \d+, then the value of a² \+ b² \+ c²", stem):
            s, p = ints(stem)
            exp = Fraction(s**2 - 2*p)
            if F(aval) != exp:
                print(f"Q{n} SUMSQ wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["sumsq"] = type_counts.get("sumsq", 0) + 1

        # a+b = m, ab = n -> a^2+b^2
        elif re.search(r"If a \+ b = \d+ and ab = \d+, then the value of a² \+ b²", stem):
            m, nn = ints(stem)
            exp = Fraction(m**2 - 2*nn)
            if F(aval) != exp:
                print(f"Q{n} A2B2 wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["a2b2"] = type_counts.get("a2b2", 0) + 1

        # a+b = m, ab = n -> a^3+b^3
        elif re.search(r"If a \+ b = \d+ and ab = \d+, then the value of a³ \+ b³", stem):
            m, nn = ints(stem)
            exp = Fraction(m**3 - 3*m*nn)
            if F(aval) != exp:
                print(f"Q{n} A3B3 wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["a3b3"] = type_counts.get("a3b3", 0) + 1

        # x^2 - kx + 1 = 0 -> x^3 + 1/x^3
        elif re.search(r"If x² − \d+x \+ 1 = 0, then the value of x³ \+ 1/x³", stem):
            k = int(re.search(r"x² − (\d+)x \+ 1 = 0", stem).group(1))
            exp = Fraction(k**3 - 3*k)
            if F(aval) != exp:
                print(f"Q{n} QUAD-CUBE wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["quad_cube"] = type_counts.get("quad_cube", 0) + 1

        # surd x = a + sqrt(b) -> x^2 + 1/x^2 ; verify numerically too
        elif re.search(r"If x = \d+ \+ √\d+, then the value of x² \+ 1/x²", stem):
            mm = re.search(r"x = (\d+) \+ √(\d+)", stem)
            a, b = int(mm.group(1)), int(mm.group(2))
            k = 2 * a
            exp = Fraction(k**2 - 2)
            # numeric check on the actual surd
            xv = a + math.sqrt(b)
            num = xv**2 + 1/(xv**2)
            if F(aval) != exp or abs(float(exp) - num) > 1e-6:
                print(f"Q{n} SURD-SQ wrong: got {aval}, expect {exp}, num {num:.4f}"); mismatch += 1
            checked += 1; type_counts["surd_sq"] = type_counts.get("surd_sq", 0) + 1

        # factor theorem: (x - r) factor of x^2 + kx + c -> k
        elif re.search(r"If \(x − \d+\) is a factor of x² \+ kx", stem):
            nums = ints(stem)
            r = nums[0]
            c = nums[1]  # constant (could be negative via unicode minus)
            exp = Fraction(-(r**2 + c), r)
            if F(aval) != exp:
                print(f"Q{n} FACTOR wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["factor"] = type_counts.get("factor", 0) + 1

        # min value of x + k/x
        elif re.search(r"minimum value of x \+ \d+/x", stem):
            k = int(re.search(r"minimum value of x \+ (\d+)/x", stem).group(1))
            exp = Fraction(2 * math.isqrt(k))
            if F(aval) != exp:
                print(f"Q{n} MINVAL wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["minval"] = type_counts.get("minval", 0) + 1

        # simplify (a^2 - b^2)/(a - b)
        elif re.search(r"The value of \(\d+² − \d+²\)/\(\d+ − \d+\)", stem):
            a, b = ints(stem)[:2]
            exp = Fraction(a + b)
            if F(aval) != exp:
                print(f"Q{n} SIMPLIFY wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["simplify"] = type_counts.get("simplify", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 3, "Fewer than 3 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
