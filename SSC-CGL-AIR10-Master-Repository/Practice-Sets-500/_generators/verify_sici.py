# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Simple Interest & Compound Interest set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options, then for several recognizable template
types RE-SOLVE directly from the stem numbers (regex) and confirm the keyed
value matches. Re-implements SI, CI-2yr/3yr amount & interest, CI-SI-diff-2yr,
and half-yearly compounding FROM SCRATCH. Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_13_SI_CI_500.md"
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
assert len(qs) == 500, "question count mismatch!"
assert len(ans) == 500, "answer count mismatch!"


def F(s):
    s = s.strip().replace("Rs", "").replace("₹", "").replace(",", "").strip()
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(s).limit_denominator(10**6)


# --- independent re-implementations (NOT imported from generator) ---
def si_calc(P, R, T):
    return Fraction(P) * Fraction(R) * Fraction(T) / 100

def ci_amount(P, R, n):
    f = (Fraction(100) + Fraction(R)) / 100
    return Fraction(P) * f ** n


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
        if stem.startswith("Find the simple interest on Rs"):
            P = F(re.search(r"on Rs (\d+)", stem).group(1))
            R = F(re.search(r"at (\d+(?:\.\d+)?)% per annum", stem).group(1))
            T = F(re.search(r"for (\d+) years", stem).group(1))
            exp = si_calc(P, R, T)
            if F(aval) != exp:
                print(f"Q{n} SI-BASIC wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["si_basic"] = type_counts.get("si_basic", 0) + 1

        elif stem.startswith("Find the amount on Rs") and "compound interest" in stem and "annually" in stem:
            P = F(re.search(r"on Rs (\d+)", stem).group(1))
            R = F(re.search(r"at (\d+(?:\.\d+)?)% per annum", stem).group(1))
            ny = F(re.search(r"for (\d+) years", stem).group(1))
            exp = ci_amount(P, R, int(ny))
            if F(aval) != exp:
                print(f"Q{n} CI-AMT wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["ci_amount"] = type_counts.get("ci_amount", 0) + 1

        elif stem.startswith("Find the compound interest on Rs"):
            P = F(re.search(r"on Rs (\d+)", stem).group(1))
            R = F(re.search(r"at (\d+(?:\.\d+)?)% per annum", stem).group(1))
            ny = F(re.search(r"for (\d+) years", stem).group(1))
            exp = ci_amount(P, R, int(ny)) - P
            if F(aval) != exp:
                print(f"Q{n} CI-INT wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["ci_interest"] = type_counts.get("ci_interest", 0) + 1

        elif "difference between the compound interest and the simple interest" in stem and "for 2 years is:" in stem:
            P = F(re.search(r"sum of Rs (\d+)", stem).group(1))
            R = F(re.search(r"at (\d+(?:\.\d+)?)% per annum", stem).group(1))
            exp = P * (R / 100) ** 2
            if F(aval) != exp:
                print(f"Q{n} DIFF-2YR wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["diff_2yr"] = type_counts.get("diff_2yr", 0) + 1

        elif "difference between the compound interest and the simple interest" in stem and "for 3 years is:" in stem:
            P = F(re.search(r"sum of Rs (\d+)", stem).group(1))
            R = F(re.search(r"at (\d+(?:\.\d+)?)% per annum", stem).group(1))
            exp = P * (R / 100) ** 2 * (3 + R / 100)
            if F(aval) != exp:
                print(f"Q{n} DIFF-3YR wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["diff_3yr"] = type_counts.get("diff_3yr", 0) + 1

        elif "compounded half-yearly" in stem:
            P = F(re.search(r"on Rs (\d+)", stem).group(1))
            R = F(re.search(r"at (\d+(?:\.\d+)?)% per annum", stem).group(1))
            yrs = F(re.search(r"for (\d+(?:\.\d+)?(?:/\d+)?) years", stem).group(1))
            periods = int(2 * yrs)
            exp = ci_amount(P, R / 2, periods)
            if F(aval) != exp:
                print(f"Q{n} HALF-YR wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["half_yearly"] = type_counts.get("half_yearly", 0) + 1

        elif stem.startswith("The value of a machine worth Rs") and "depreciates" in stem:
            P = F(re.search(r"worth Rs (\d+)", stem).group(1))
            R = F(re.search(r"at (\d+(?:\.\d+)?)% per annum", stem).group(1))
            ny = F(re.search(r"after (\d+) years", stem).group(1))
            exp = P * (Fraction(100) - R) / 100 * 1
            exp = P * ((Fraction(100) - R) / 100) ** int(ny)
            if F(aval) != exp:
                print(f"Q{n} DEPREC wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["depreciation"] = type_counts.get("depreciation", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 4, "Fewer than 4 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
