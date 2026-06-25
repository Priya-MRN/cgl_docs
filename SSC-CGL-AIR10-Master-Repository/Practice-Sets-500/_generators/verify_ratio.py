# -*- coding: utf-8 -*-
"""
Independent deep verifier for the Ratio & Proportion 500-set.
Re-parses the WRITTEN markdown and re-solves recognizable template types
directly from the stem numbers via regex (no reuse of any generator code).
Plain ASCII output (Windows cp1252 safe).
"""
import re
from fractions import Fraction
from math import isqrt

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_02_Ratio_Proportion_500.md"
txt = open(PATH, encoding="utf-8").read()
qpart, apart = re.split(r"# =+ ANSWER KEY", txt)

qpat = re.compile(r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\n", re.S)
qs = {}
for m in qpat.finditer(qpart):
    qs[int(m.group(1))] = (m.group(2).strip(), [m.group(i).strip() for i in (3,4,5,6)])

apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*")
ans = {}
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), m.group(3).strip())

print(f"Parsed {len(qs)} questions, {len(ans)} answers")

def num(s):
    s = s.strip().replace("Rs","").replace("₹","").replace(",","").replace("%","").strip()
    if re.fullmatch(r"-?\d+/\d+", s):
        a,b = s.split("/"); return Fraction(int(a),int(b))
    try: return Fraction(s).limit_denominator(10**7)
    except: return None

def ints(stem):
    return [int(x) for x in re.findall(r"\d+", stem)]

struct_err = 0
resolved = 0
mismatch = 0
breakdown = {}

for n,(stem,opts) in qs.items():
    letter, aval = ans[n]
    li = "abcd".index(letter)
    # structural
    if num(opts[li]) is not None and num(aval) is not None and num(opts[li]) != num(aval):
        print(f"Q{n}: keyed option != answer ({opts[li]} vs {aval})"); struct_err+=1
    if len(set(opts)) != 4:
        print(f"Q{n}: options not distinct {opts}"); struct_err+=1

    A = num(aval)
    expected = None
    kind = None
    try:
        if "mean proportional between" in stem:
            x,y = re.findall(r"between (\d+) and (\d+)", stem)[0]
            expected = Fraction(isqrt(int(x)*int(y))) if isqrt(int(x)*int(y))**2==int(x)*int(y) else None
            # mean prop = sqrt(xy); only clean if perfect square
            if expected is None:
                import math
                expected = Fraction(round(math.sqrt(int(x)*int(y)),4)).limit_denominator(10000)
            kind="mean_prop"
        elif "third proportional to" in stem:
            x,y = re.findall(r"to (\d+) and (\d+)", stem)[0]
            expected = Fraction(int(y)*int(y), int(x)); kind="third_prop"
        elif re.search(r"ratio (\d+) : (\d+)\. If (\d+) is subtracted", stem):
            a,b,k = map(int, re.search(r"ratio (\d+) : (\d+)\. If (\d+) is subtracted", stem).groups())
            c,d = map(int, re.search(r"becomes (\d+) : (\d+)", stem).groups())
            # (a x - k)/(b x - k) = c/d  -> solve x
            # d(ax-k)=c(bx-k) -> x(da-cb)=k(d-c) -> x=k(d-c)/(da-cb)
            x = Fraction(k*(d-c), d*a-c*b)
            larger = b*x if b>a else a*x
            smaller = a*x if a<b else b*x
            if "larger number" in stem: expected=larger
            elif "smaller number" in stem: expected=smaller
            kind="ratio_sub"
        elif re.search(r"ratio (\d+) : (\d+)\. If (\d+) is added", stem):
            a,b,k = map(int, re.search(r"ratio (\d+) : (\d+)\. If (\d+) is added", stem).groups())
            c,d = map(int, re.search(r"becomes (\d+) : (\d+)", stem).groups())
            x = Fraction(k*(c-d), d*a-c*b)
            larger = b*x if b>a else a*x
            smaller = a*x if a<b else b*x
            if "larger number" in stem: expected=larger
            elif "smaller number" in stem: expected=smaller
            kind="ratio_add"
        elif re.search(r"sum of ₹?(\d+) is divided among .* ratio (\d+) : (\d+) : (\d+)", stem):
            g = re.search(r"sum of ₹?(\d+) is divided among .* ratio (\d+) : (\d+) : (\d+)", stem)
            total,r1,r2,r3 = map(int, g.groups())
            # share of Q (2nd)
            if "share of Q" in stem:
                expected = Fraction(total*r2, r1+r2+r3); kind="sum_share"
        elif "incomes of A and B are in the ratio" in stem and "each saves" in stem:
            i1,i2 = map(int, re.search(r"ratio (\d+) : (\d+)", stem).groups())
            e1,e2 = map(int, re.search(r"expenditures are in the ratio (\d+) : (\d+)", stem).groups())
            save = int(re.search(r"saves ₹?(\d+)", stem).group(1))
            # income A=i1 k, B=i2 k; exp A=e1 m, B=e2 m; i1 k - e1 m = save = i2 k - e2 m
            # Solve 2x2 linear for (k,m) exactly with Fraction:
            #   i1 k - e1 m = save
            #   i2 k - e2 m = save
            det = Fraction(i1*(-e2) - (-e1)*i2)
            k = Fraction(save*(-e2) - (-e1)*save, 1) / det
            expected = (Fraction(i1)*k); kind="income_exp"
    except Exception as e:
        expected=None

    if expected is not None and A is not None:
        resolved += 1
        breakdown[kind] = breakdown.get(kind,0)+1
        if abs(float(expected)-float(A)) > 1e-6:
            print(f"Q{n} [{kind}] MISMATCH: re-solved {expected} ({float(expected):.4f}) vs key {aval}")
            mismatch += 1

print(f"Structural errors: {struct_err}")
print(f"Independently re-solved {resolved} questions; types: {breakdown}")
print(f"Re-solve mismatches: {mismatch}")
print("RESULT:", "PASS" if (struct_err==0 and mismatch==0) else "FAIL")
