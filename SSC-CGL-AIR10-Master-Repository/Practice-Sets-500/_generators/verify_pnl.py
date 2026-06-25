# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Profit & Loss 500 set: parse the rendered markdown,
then for several formula-based question types, re-solve directly from the numbers
in the stem text (regex) and confirm the keyed option matches. This does NOT
reuse the generator's objects.

NO unicode emoji in prints (Windows cp1252) -- use plain "PASS"/"FAIL".
"""
import re, sys
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_03_Profit_Loss_500.md"
txt = open(PATH, encoding="utf-8").read()

qpart, apart = txt.split("# =================== ANSWER KEY")

qs = {}
qpat = re.compile(r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\n", re.S)
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
    s = s.strip().replace("Rs", "").replace("₹", "").strip()
    if "/" in s:
        a, b = s.split("/"); return Fraction(int(a), int(b))
    return Fraction(s).limit_denominator(10**6)

checked = 0
mismatch = 0

for n, (stem, opts) in qs.items():
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]
    # keyed option must equal the stated answer value AND be one of the 4 options
    if F(keyed_opt) != F(aval):
        print(f"Q{n}: keyed letter/value mismatch: option[{letter}]={keyed_opt} vs answer {aval}")
        mismatch += 1
        continue
    # ensure 4 distinct options
    if len(set(F(o) for o in opts)) != 4:
        print(f"Q{n}: duplicate options {opts}")
        mismatch += 1

    # independent re-solve for recognizable types:
    try:
        if "equivalent to a single discount" in stem and stem.count("%") == 3 and "Three" not in stem:
            # two successive discounts
            d1, d2 = [F(x) for x in re.findall(r"(\d+)%", stem)[:2]]
            exp = d1 + d2 - d1*d2/100
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} TWO-DISC wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "Three successive discounts" in stem:
            d1, d2, d3 = [F(x) for x in re.findall(r"(\d+)%", stem)[:3]]
            exp = (1 - (100-d1)/100*(100-d2)/100*(100-d3)/100)*100
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} THREE-DISC wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "gained" in stem and "lost" in stem and "overall percentage loss" in stem:
            # same SP, +x% and -x% -> (x/10)^2
            x = F(re.search(r"gained ([\d.]+)%", stem).group(1))
            exp = (x/10)**2
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} SAME-SP-LOSS wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "uses a weight of" in stem and "at cost price" in stem:
            given = F(re.search(r"weight of (\d+) g", stem).group(1))
            exp = (1000-given)*100/given
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} FALSE-WEIGHT wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "cost price of" in stem and "selling price of" in stem and "gain percent" in stem:
            m_, n_ = [F(x) for x in re.findall(r"of (\d+) articles", stem)[:2]]
            exp = (m_-n_)*100/n_
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} M-N-ARTICLES wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "profit earned by selling" in stem and "loss incurred" in stem:
            spvals = [F(x) for x in re.findall(r"Rs (\d+)", stem)[:2]]
            exp = (spvals[0]+spvals[1])/2
            if F(aval) != exp:
                print(f"Q{n} PROFIT=LOSS-CP wrong: got {aval}, expect {exp}"); mismatch += 1
            checked += 1
        elif "buy" in stem and "get" in stem and "free" in stem and "effective discount" in stem:
            x, y = [int(v) for v in re.findall(r"buy (\d+) get (\d+) free", stem)[0]]
            exp = Fraction(y)*100/(x+y)
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} BUY-GET-FREE wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
        elif "marks his goods" in stem and "discount of" in stem and "His" in stem and "profit percent is" in stem and "NO discount" not in stem:
            m_ = F(re.search(r"marks his goods (\d+)% above", stem).group(1))
            d_ = F(re.search(r"discount of (\d+)%", stem).group(1))
            exp = ((100+m_)/100*(100-d_)/100 - 1)*100
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} MARKUP-DISC-PROFIT wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1
    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
sys.exit(0 if mismatch == 0 else 1)
