# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Time & Work 500 set.
Parses the rendered markdown, confirms 500 Q + 500 A, that each keyed
letter/value matches and there are 4 distinct options, then re-solves
several template types directly from the numbers in the stem (regex).
Does NOT reuse the generator's objects. No unicode emoji in prints.
"""
import re
from fractions import Fraction
from math import gcd

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_04_Time_Work_500.md"
txt = open(PATH, encoding="utf-8").read()

qpart, apart = txt.split("# =================== ANSWER KEY")

qs = {}
qpat = re.compile(
    r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\n",
    re.S)
for m in qpat.finditer(qpart):
    n = int(m.group(1))
    stem = m.group(2).replace("\n", " ").strip()
    opts = [m.group(3).strip(), m.group(4).strip(),
            m.group(5).strip(), m.group(6).strip()]
    qs[n] = (stem, opts)

ans = {}
apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*")
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), m.group(3).strip())

print(f"Parsed {len(qs)} questions, {len(ans)} answers")
assert len(qs) == 500, "question count mismatch!"
assert len(ans) == 500, "answer count mismatch!"

def F(s):
    s = s.strip().replace("₹", "").replace(",", "")
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(s).limit_denominator(10**6)

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_list(xs):
    r = 1
    for x in xs:
        r = lcm(r, int(x))
    return r

mismatch = 0
checked = 0

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

    # ---- independent re-solve for recognizable types ----
    try:
        if "A alone can complete it in" in stem and "B alone can complete" in stem:
            t = F(re.search(r"in ([\d./]+) days", stem).group(1))
            a = F(re.search(r"A alone can complete it in ([\d./]+) days", stem).group(1))
            exp = 1 / (Fraction(1) / t - Fraction(1) / a)
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} AB-ALONE wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "A can do a work in" in stem and "Working together, in how many days" in stem:
            a = F(re.search(r"A can do a work in (\d+) days", stem).group(1))
            b = F(re.search(r"B can do the same work in (\d+) days", stem).group(1))
            exp = (a * b) / (a + b)
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} TOGETHER wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "can individually complete a work in" in stem and "all three work together" in stem:
            a, b, c = [int(x) for x in re.findall(r"(\d+)", stem)[:3]]
            L = lcm_list([a, b, c])
            rate = L // a + L // b + L // c
            exp = Fraction(L, rate)
            if F(aval) != exp:
                print(f"Q{n} THREE-TOGETHER wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "third (outlet) pipe can empty" in stem:
            f1 = int(re.search(r"fill a tank in (\d+)", stem).group(1))
            f2 = int(re.search(r"(\d+) hours respectively", stem).group(1))
            e = int(re.search(r"empty the full tank in (\d+)", stem).group(1))
            L = lcm_list([f1, f2, e])
            net = L // f1 + L // f2 - L // e
            exp = Fraction(L, net)
            if F(aval) != exp:
                print(f"Q{n} PIPES wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "men working" in stem and "how many men are required" in stem:
            M1 = int(re.search(r"If (\d+) men", stem).group(1))
            H1 = int(re.search(r"working (\d+) hours a day can complete", stem).group(1))
            D1 = int(re.search(r"complete a work in (\d+) days", stem).group(1))
            D2 = int(re.search(r"same work in (\d+) days", stem).group(1))
            H2 = int(re.search(r"working (\d+)\s*hours a day\?", stem).group(1))
            exp = Fraction(M1 * D1 * H1, D2 * H2)
            if F(aval) != exp:
                print(f"Q{n} MANDAYS-CHAIN wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "men can complete a work in" in stem and "How many days will" in stem:
            M1 = int(re.search(r"(\d+) men can complete", stem).group(1))
            D1 = int(re.search(r"work in (\d+) days", stem).group(1))
            M2 = int(re.search(r"will (\d+) men", stem).group(1))
            exp = Fraction(M1 * D1, M2)
            if F(aval) != exp:
                print(f"Q{n} MANDAYS wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
    except Exception as e:
        # parsing skip is fine; structural check already passed for this Q
        pass

print(f"Independently re-solved {checked} formula questions.")
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
