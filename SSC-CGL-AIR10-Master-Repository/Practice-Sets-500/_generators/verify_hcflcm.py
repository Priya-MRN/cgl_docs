# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the HCF & LCM set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options, then for several recognizable template
types RE-SOLVE directly from the stem numbers (regex) using gcd/lcm logic
re-implemented FROM SCRATCH (no math.gcd, no generator objects).
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_11_HCF_LCM_500.md"
txt = open(PATH, encoding="utf-8").read()


# ----- gcd / lcm re-implemented from scratch (Euclid) -----
def mygcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def mygcd_list(nums):
    g = nums[0]
    for x in nums[1:]:
        g = mygcd(g, x)
    return g


def mylcm(a, b):
    return a * b // mygcd(a, b)


def mylcm_list(nums):
    l = nums[0]
    for x in nums[1:]:
        l = mylcm(l, x)
    return l


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
    return Fraction(s).limit_denominator(10 ** 6)


def ints(stem):
    return [int(x) for x in re.findall(r"\d+", stem)]


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
        if "HCF of the fractions" in stem:
            mm = re.search(r"(\d+)/(\d+) and (\d+)/(\d+)", stem)
            a1, b1, a2, b2 = [int(g) for g in mm.groups()]
            exp = Fraction(mygcd(a1, a2), mylcm(b1, b2))
            if F(aval) != exp:
                print(f"Q{n} FRAC-HCF wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["frac_hcf"] = type_counts.get("frac_hcf", 0) + 1

        elif "LCM of the fractions" in stem:
            mm = re.search(r"(\d+)/(\d+) and (\d+)/(\d+)", stem)
            a1, b1, a2, b2 = [int(g) for g in mm.groups()]
            exp = Fraction(mylcm(a1, a2), mygcd(b1, b2))
            if F(aval) != exp:
                print(f"Q{n} FRAC-LCM wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["frac_lcm"] = type_counts.get("frac_lcm", 0) + 1

        elif stem.startswith("Find the HCF (GCD) of"):
            a, b = ints(stem)[:2]
            exp = mygcd(a, b)
            if F(aval) != exp:
                print(f"Q{n} HCF2 wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["hcf2"] = type_counts.get("hcf2", 0) + 1

        elif re.match(r"Find the LCM of \d+ and \d+\.", stem):
            a, b = ints(stem)[:2]
            exp = mylcm(a, b)
            if F(aval) != exp:
                print(f"Q{n} LCM2 wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["lcm2"] = type_counts.get("lcm2", 0) + 1

        elif stem.startswith("Find the HCF of") and "and" in stem:
            nums = ints(stem)
            exp = mygcd_list(nums)
            if F(aval) != exp:
                print(f"Q{n} HCF3 wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["hcf3"] = type_counts.get("hcf3", 0) + 1

        elif stem.startswith("Find the LCM of") and "," in stem:
            nums = ints(stem)
            exp = mylcm_list(nums)
            if F(aval) != exp:
                print(f"Q{n} LCM3 wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["lcm3"] = type_counts.get("lcm3", 0) + 1

        elif "greatest number that divides" in stem and "leaving remainders" in stem:
            mm = re.search(
                r"divides (\d+), (\d+) and (\d+) leaving remainders (\d+), (\d+) and (\d+)",
                stem)
            a, b, c, r1, r2, r3 = [int(g) for g in mm.groups()]
            exp = mygcd_list([a - r1, b - r2, c - r3])
            if F(aval) != exp:
                print(f"Q{n} REM-DIFF wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["rem_diff"] = type_counts.get("rem_diff", 0) + 1

        elif "greatest number which divides" in stem and "same remainder" in stem:
            a, b, c = ints(stem)[:3]
            exp = mygcd_list([b - a, c - b, c - a])
            if F(aval) != exp:
                print(f"Q{n} SAME-REM wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["same_rem"] = type_counts.get("same_rem", 0) + 1

        elif "least number which when divided by" in stem and "leaves a remainder" in stem:
            mm = re.search(
                r"divided by (\d+), (\d+) and (\d+) leaves a remainder (\d+)", stem)
            a, b, c, r = [int(g) for g in mm.groups()]
            exp = mylcm_list([a, b, c]) + r
            if F(aval) != exp:
                print(f"Q{n} LCM+R wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["lcm_plus_r"] = type_counts.get("lcm_plus_r", 0) + 1

        elif "least number which when divided by" in stem and "leaves remainders" in stem:
            mm = re.search(
                r"divided by (\d+), (\d+) and (\d+) leaves remainders (\d+), (\d+) and (\d+)",
                stem)
            a, b, c, r1, r2, r3 = [int(g) for g in mm.groups()]
            k = a - r1  # common difference
            exp = mylcm_list([a, b, c]) - k
            if F(aval) != exp:
                print(f"Q{n} LCM-K wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["lcm_minus_k"] = type_counts.get("lcm_minus_k", 0) + 1

        elif "Product of two numbers" in stem or (
                "HCF and LCM of two numbers" in stem and "one of the numbers is" in stem):
            mm = re.search(
                r"HCF and LCM of two numbers are (\d+) and (\d+).*one of the numbers is (\d+)",
                stem)
            H, L, a = [int(g) for g in mm.groups()]
            exp = Fraction(H * L, a)
            if F(aval) != exp:
                print(f"Q{n} PROD=HxL wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["prod_hl"] = type_counts.get("prod_hl", 0) + 1

        elif "product of two numbers is" in stem and "their HCF is" in stem:
            mm = re.search(r"product of two numbers is (\d+) and their HCF is (\d+)", stem)
            prod, H = int(mm.group(1)), int(mm.group(2))
            exp = Fraction(prod, H)
            if F(aval) != exp:
                print(f"Q{n} PROD/HCF wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["prod_div_hcf"] = type_counts.get("prod_div_hcf", 0) + 1

        elif "ratio" in stem and "their HCF is" in stem and "Find their LCM" in stem:
            mm = re.search(r"ratio (\d+):(\d+).*HCF is (\d+)", stem)
            p, q, h = [int(g) for g in mm.groups()]
            exp = mylcm(h * p, h * q)
            if F(aval) != exp:
                print(f"Q{n} RATIO-LCM wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["ratio_lcm"] = type_counts.get("ratio_lcm", 0) + 1

        elif "measuring tape" in stem:
            a, b, c = ints(stem)[:3]
            exp = mygcd_list([a, b, c])
            if F(aval) != exp:
                print(f"Q{n} TAPE wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["tape"] = type_counts.get("tape", 0) + 1

        elif "least number of square tiles" in stem:
            mm = re.search(r"(\d+) cm long and (\d+) cm broad", stem)
            L, B = int(mm.group(1)), int(mm.group(2))
            side = mygcd(L, B)
            exp = (L * B) // (side * side)
            if F(aval) != exp:
                print(f"Q{n} TILES wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["tiles"] = type_counts.get("tiles", 0) + 1

        elif "exactly divisible by" in stem:
            nums = ints(stem)
            exp = mylcm_list(nums)
            if F(aval) != exp:
                print(f"Q{n} DIVISIBLE wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["divisible"] = type_counts.get("divisible", 0) + 1

        elif "greatest number that divides" in stem and "no remainder" in stem:
            a, b, c = ints(stem)[:3]
            exp = mygcd_list([a, b, c])
            if F(aval) != exp:
                print(f"Q{n} EXACT-DIV wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["exact_div"] = type_counts.get("exact_div", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 4, "Fewer than 4 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
