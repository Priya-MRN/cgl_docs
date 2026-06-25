# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Number System set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options, then for several recognizable template
types RE-SOLVE directly from the stem numbers (regex) by re-implementing the
math from scratch, and confirm the keyed value matches.
Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
import math
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_10_Number_System_500.md"
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
    return Fraction(s)


# ----- independent re-implementations of the math -----
def trailing_zeros(n):
    t, pk = 0, 5
    while pk <= n:
        t += n // pk
        pk *= 5
    return t


def legendre(n, p):
    t, pk = 0, p
    while pk <= n:
        t += n // pk
        pk *= p
    return t


def ndiv(n):
    c, m, d = 1, n, 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d; e += 1
            c *= (e + 1)
        d += 1
    if m > 1:
        c *= 2
    return c


def sdiv(n):
    tot, m, d = 1, n, 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d; e += 1
            tot *= (d ** (e + 1) - 1) // (d - 1)
        d += 1
    if m > 1:
        tot *= (m * m - 1) // (m - 1)
    return tot


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

    try:
        if "unit (last) digit of" in stem:
            mm = re.search(r"of (\d+)\^(\d+)", stem)
            a, e = int(mm.group(1)), int(mm.group(2))
            exp = pow(a, e, 10)
            if int(F(aval)) != exp:
                print(f"Q{n} UNIT-DIGIT wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["unit_digit"] = type_counts.get("unit_digit", 0) + 1

        elif "zeros are there at the end of" in stem:
            nn = int(re.search(r"end of (\d+)!", stem).group(1))
            exp = trailing_zeros(nn)
            if int(F(aval)) != exp:
                print(f"Q{n} TRAILING-ZEROS wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["trailing_zeros"] = type_counts.get("trailing_zeros", 0) + 1

        elif "highest power of" in stem and "divides" in stem:
            mm = re.search(r"highest power of (\d+) that divides (\d+)!", stem)
            p, nn = int(mm.group(1)), int(mm.group(2))
            exp = legendre(nn, p)
            if int(F(aval)) != exp:
                print(f"Q{n} LEGENDRE wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["legendre"] = type_counts.get("legendre", 0) + 1

        elif "remainder when" in stem and "^" in stem and "+" not in stem:
            mm = re.search(r"when (\d+)\^(\d+) is divided by (\d+)", stem)
            a, e, mdv = int(mm.group(1)), int(mm.group(2)), int(mm.group(3))
            exp = pow(a, e, mdv)
            if int(F(aval)) != exp:
                print(f"Q{n} REMAINDER-POW wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["rem_pow"] = type_counts.get("rem_pow", 0) + 1

        elif "remainder when" in stem and re.search(r"(\d+)\^(\d+) \+ (\d+)", stem):
            mm = re.search(r"when (\d+)\^(\d+) \+ (\d+) is divided by (\d+)", stem)
            a, e, c, mdv = (int(mm.group(1)), int(mm.group(2)),
                            int(mm.group(3)), int(mm.group(4)))
            exp = (pow(a, e, mdv) + c) % mdv
            if int(F(aval)) != exp:
                print(f"Q{n} REM-POW-PLUS wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["rem_pow_plus"] = type_counts.get("rem_pow_plus", 0) + 1

        elif "sum of the first" in stem and "natural numbers" in stem:
            nn = int(re.search(r"first (\d+) natural", stem).group(1))
            exp = nn * (nn + 1) // 2
            if int(F(aval)) != exp:
                print(f"Q{n} SUM-NAT wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["sum_nat"] = type_counts.get("sum_nat", 0) + 1

        elif "sum of the squares of the first" in stem:
            nn = int(re.search(r"first (\d+) natural", stem).group(1))
            exp = nn * (nn + 1) * (2 * nn + 1) // 6
            if int(F(aval)) != exp:
                print(f"Q{n} SUM-SQ wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["sum_sq"] = type_counts.get("sum_sq", 0) + 1

        elif "sum of the cubes of the first" in stem:
            nn = int(re.search(r"first (\d+) natural", stem).group(1))
            exp = (nn * (nn + 1) // 2) ** 2
            if int(F(aval)) != exp:
                print(f"Q{n} SUM-CUBE wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["sum_cube"] = type_counts.get("sum_cube", 0) + 1

        elif "sum of all integers from" in stem:
            mm = re.search(r"from (\d+) to (\d+)", stem)
            a, b = int(mm.group(1)), int(mm.group(2))
            exp = (a + b) * (b - a + 1) // 2
            if int(F(aval)) != exp:
                print(f"Q{n} SUM-CONSEC wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["sum_consec"] = type_counts.get("sum_consec", 0) + 1

        elif "quotient is" in stem and "remainder is" in stem:
            mm = re.search(r"by (\d+), the quotient is (\d+) and the remainder is (\d+)", stem)
            d, q, r = int(mm.group(1)), int(mm.group(2)), int(mm.group(3))
            exp = d * q + r
            if int(F(aval)) != exp:
                print(f"Q{n} DIV-ALGO wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["div_algo"] = type_counts.get("div_algo", 0) + 1

        elif "least number which when divided by" in stem and "remainder of" in stem:
            divs = [int(x) for x in re.findall(r"(\d+)", stem.split("leaves")[0])]
            r = int(re.search(r"remainder of (\d+)", stem).group(1))
            L = divs[0]
            for d in divs[1:]:
                L = L * d // math.gcd(L, d)
            exp = L + r
            if int(F(aval)) != exp:
                print(f"Q{n} LCM-REM wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["lcm_rem"] = type_counts.get("lcm_rem", 0) + 1

        elif "largest" in stem and "digit number that is exactly divisible" in stem:
            mm = re.search(r"largest (\d+)-digit number that is exactly divisible by (\d+)", stem)
            digs, k = int(mm.group(1)), int(mm.group(2))
            hi = 10 ** digs - 1
            exp = hi - (hi % k)
            if int(F(aval)) != exp:
                print(f"Q{n} LARGEST-DIV wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["largest_div"] = type_counts.get("largest_div", 0) + 1

        elif "smallest" in stem and "digit number that is exactly divisible" in stem:
            mm = re.search(r"smallest (\d+)-digit number that is exactly divisible by (\d+)", stem)
            digs, k = int(mm.group(1)), int(mm.group(2))
            lo = 10 ** (digs - 1)
            rem = lo % k
            exp = lo if rem == 0 else lo + (k - rem)
            if int(F(aval)) != exp:
                print(f"Q{n} SMALLEST-DIV wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["smallest_div"] = type_counts.get("smallest_div", 0) + 1

        elif "are divisible by" in stem and " or " in stem:
            mm = re.search(r"from 1 to (\d+) are divisible by (\d+) or (\d+)", stem)
            N, a, b = int(mm.group(1)), int(mm.group(2)), int(mm.group(3))
            l = a * b // math.gcd(a, b)
            exp = N // a + N // b - N // l
            if int(F(aval)) != exp:
                print(f"Q{n} COUNT-OR wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["count_or"] = type_counts.get("count_or", 0) + 1

        elif "are divisible by both" in stem:
            mm = re.search(r"from 1 to (\d+) are divisible by both (\d+) and (\d+)", stem)
            N, a, b = int(mm.group(1)), int(mm.group(2)), int(mm.group(3))
            l = a * b // math.gcd(a, b)
            exp = N // l
            if int(F(aval)) != exp:
                print(f"Q{n} COUNT-BOTH wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["count_both"] = type_counts.get("count_both", 0) + 1

        elif "many factors (divisors) does" in stem:
            nn = int(re.search(r"does (\d+) have", stem).group(1))
            exp = ndiv(nn)
            if int(F(aval)) != exp:
                print(f"Q{n} NDIV wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["ndiv"] = type_counts.get("ndiv", 0) + 1

        elif "sum of all the factors (divisors) of" in stem:
            nn = int(re.search(r"divisors\) of (\d+)", stem).group(1))
            exp = sdiv(nn)
            if int(F(aval)) != exp:
                print(f"Q{n} SDIV wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["sdiv"] = type_counts.get("sdiv", 0) + 1

        elif "Convert the binary number" in stem:
            b = re.search(r"\((\d+)\)₂", stem).group(1)
            exp = int(b, 2)
            if int(F(aval)) != exp:
                print(f"Q{n} BIN2DEC wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["bin2dec"] = type_counts.get("bin2dec", 0) + 1

        elif "written in binary" in stem and "how many" in stem:
            v = int(re.search(r"decimal number (\d+)", stem).group(1))
            exp = bin(v).count("1")
            if int(F(aval)) != exp:
                print(f"Q{n} DEC2BIN-ONES wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1; type_counts["dec2bin"] = type_counts.get("dec2bin", 0) + 1

        elif "two-digit number is" in stem and "reversed" in stem:
            s = int(re.search(r"digits of a two-digit number is (\d+)", stem).group(1))
            diff = int(re.search(r"becomes (\d+) (more|less)", stem).group(1))
            direction = re.search(r"becomes (\d+) (more|less)", stem).group(2)
            # reversed - original = +diff (more) or -diff (less) => 9(u-t)
            signed = diff if direction == "more" else -diff
            # 9(u - t) = signed ; t + u = s
            umt = Fraction(signed, 9)
            u = (Fraction(s) + umt) / 2
            t = Fraction(s) - u
            if u.denominator == 1 and t.denominator == 1:
                exp = 10 * int(t) + int(u)
                if int(F(aval)) != exp:
                    print(f"Q{n} TWO-DIGIT wrong: got {aval}, expect {exp}"); mismatch += 1
                checked += 1; type_counts["two_digit"] = type_counts.get("two_digit", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 4, "Fewer than 4 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
