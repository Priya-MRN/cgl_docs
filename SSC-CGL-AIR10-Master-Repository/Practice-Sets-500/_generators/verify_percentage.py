# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier: parse the rendered markdown, then for the
formula-based question types, re-solve directly from the numbers in the
stem text (regex) and confirm the keyed option matches. This does NOT
reuse the generator's objects.
"""
import re, sys
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_01_Percentage_500.md"
txt = open(PATH, encoding="utf-8").read()

# split into questions and answers halves
qpart, apart = txt.split("# =================== ANSWER KEY")
# parse questions: Q<n>. stem  /  (a) .. (b) .. (c) .. (d) ..
qs = {}
qpat = re.compile(r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\n", re.S)
for m in qpat.finditer(qpart):
    n = int(m.group(1))
    stem = m.group(2).replace("\n"," ").strip()
    opts = [m.group(3).strip(), m.group(4).strip(), m.group(5).strip(), m.group(6).strip()]
    qs[n] = (stem, opts)

# parse answers: **Q<n>. (x) value** ...
ans = {}
apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*")
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), m.group(3).strip())

print(f"Parsed {len(qs)} questions, {len(ans)} answers")
assert len(qs) == 500 and len(ans) == 500, "count mismatch!"

def F(s):
    s = s.strip().replace("₹","")
    if "/" in s:
        a,b = s.split("/"); return Fraction(int(a),int(b))
    return Fraction(s).limit_denominator(10**6)

def nums(stem):
    return [x for x in re.findall(r"-?\d+\.?\d*", stem)]

checked = 0
mismatch = 0
# Re-solve the deterministic formula types we can identify from stem wording.
for n,(stem,opts) in qs.items():
    letter, aval = ans[n]
    # the keyed option must equal the answer value AND be one of the 4 options
    li = "abcd".index(letter)
    keyed_opt = opts[li]
    if F(keyed_opt) != F(aval):
        print(f"Q{n}: keyed letter/value mismatch: option[{letter}]={keyed_opt} vs answer {aval}")
        mismatch += 1
        continue
    # also ensure 4 distinct options
    if len(set(F(o) for o in opts)) != 4:
        print(f"Q{n}: duplicate options {opts}")
        mismatch += 1

    # independent re-solve for a few recognizable types:
    try:
        if "must a family reduce its consumption" in stem:
            x = F(re.search(r"increases by ([\d.]+)%", stem).group(1))
            exp = x/(100+x)*100
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} CONSUMPTION wrong: got {aval}, expect {float(exp):.4f}"); mismatch+=1
            checked+=1
        elif "won by" in stem and "total number of valid votes" in stem:
            p = F(re.search(r"secured (\d+)%", stem).group(1))
            margin = F(re.search(r"won by ([\d,]+) votes", stem).group(1).replace(",",""))
            exp = margin*100/(2*p-100)
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} ELECTION wrong: got {aval}, expect {float(exp):.2f}"); mismatch+=1
            checked+=1
        elif "increases at" in stem and "after 2 years" in stem:
            P = F(re.search(r"town is (\d+)", stem).group(1))
            r = F(re.search(r"at (\d+)% per annum", stem).group(1))
            exp = P*(100+r)**2/Fraction(10000)
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} POPULATION wrong: got {aval}, expect {float(exp):.2f}"); mismatch+=1
            checked+=1
        elif "passed in both subjects" in stem:
            a,b,both = [F(x) for x in re.findall(r"(\d+)%", stem)[:3]]
            exp = 100-(a+b-both)
            if F(aval) != exp:
                print(f"Q{n} BOTH-PASS wrong: got {aval}, expect {exp}"); mismatch+=1
            checked+=1
        elif "reduce its consumption" not in stem and "reduced" in stem and "restore it to the original" in stem:
            x = F(re.search(r"reduced by ([\d.]+)%", stem).group(1))
            exp = x/(100-x)*100
            if F(aval) != exp.limit_denominator(10**6):
                print(f"Q{n} RESTORE wrong: got {aval}, expect {float(exp):.4f}"); mismatch+=1
            checked+=1
    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS ✅" if mismatch==0 else "FAIL ❌")
