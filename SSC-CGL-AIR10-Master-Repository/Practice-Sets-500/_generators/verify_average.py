# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Average set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options, then for several recognizable template
types RE-SOLVE directly from the stem numbers (regex) and confirm the keyed
value matches. Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_12_Average_500.md"
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
    s = s.strip().replace("₹", "").replace(",", "")
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(s).limit_denominator(10**6)


def ints(pattern, stem):
    return [int(x) for x in re.findall(pattern, stem)]


checked = 0
mismatch = 0
type_counts = {}

for n, (stem, opts) in qs.items():
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]
    # keyed option value must equal stated answer
    try:
        if F(keyed_opt) != F(aval):
            print(f"Q{n}: keyed letter/value mismatch: option[{letter}]={keyed_opt} vs answer {aval}")
            mismatch += 1
            continue
    except Exception as e:
        print(f"Q{n}: cannot parse keyed/answer ({e})")
        mismatch += 1
        continue
    # 4 distinct options
    try:
        if len(set(F(o) for o in opts)) != 4:
            print(f"Q{n}: duplicate options {opts}")
            mismatch += 1
    except Exception as e:
        print(f"Q{n}: cannot parse options ({e})")
        mismatch += 1

    # ----- independent re-solve for recognizable types -----
    try:
        # 1) Basic average of explicit listed numbers
        m = re.match(r"The average of the numbers (.+) is:", stem)
        if m:
            nums = [int(x) for x in re.findall(r"-?\d+", m.group(1))]
            exp = Fraction(sum(nums), len(nums))
            if F(aval) != exp:
                print(f"Q{n} BASIC-AVG wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["basic_avg"] = type_counts.get("basic_avg", 0) + 1
            continue

        # 2) Average of first n natural numbers
        m = re.match(r"The average of the first (\d+) natural numbers is:", stem)
        if m:
            nn = int(m.group(1))
            exp = Fraction(nn + 1, 2)
            if F(aval) != exp:
                print(f"Q{n} NAT wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["natural"] = type_counts.get("natural", 0) + 1
            continue

        # 3) Average of first n multiples of k
        m = re.match(r"The average of the first (\d+) multiples of (\d+) is:", stem)
        if m:
            nn, k = int(m.group(1)), int(m.group(2))
            exp = Fraction(k * (nn + 1), 2)
            if F(aval) != exp:
                print(f"Q{n} MULT wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["multiples"] = type_counts.get("multiples", 0) + 1
            continue

        # 4) Average of n consecutive integers starting from s
        m = re.match(r"The average of (\d+) consecutive integers starting from (\d+) is:", stem)
        if m:
            nn, s = int(m.group(1)), int(m.group(2))
            exp = Fraction(s + (s + nn - 1), 2)
            if F(aval) != exp:
                print(f"Q{n} CONSEC wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["consec"] = type_counts.get("consec", 0) + 1
            continue

        # 5) Average of n consecutive even/odd starting from s
        m = re.match(r"The average of (\d+) consecutive (?:even|odd) numbers starting from (\d+) is:", stem)
        if m:
            nn, s = int(m.group(1)), int(m.group(2))
            last = s + 2 * (nn - 1)
            exp = Fraction(s + last, 2)
            if F(aval) != exp:
                print(f"Q{n} EVENODD wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["even_odd"] = type_counts.get("even_odd", 0) + 1
            continue

        # 6) Element added: avg of n is A, include new -> new avg
        m = re.match(r"The average of (\d+) numbers is (\d+)\. If a new number (\d+) is included, the average", stem)
        if m:
            nn, a, v = int(m.group(1)), int(m.group(2)), int(m.group(3))
            exp = Fraction(a * nn + v, nn + 1)
            if F(aval) != exp:
                print(f"Q{n} ADDED wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["added"] = type_counts.get("added", 0) + 1
            continue

        # 7) Element removed: avg of n is A, remove v -> new avg
        m = re.match(r"The average of (\d+) numbers is (\d+)\. If one number (\d+) is removed", stem)
        if m:
            nn, a, v = int(m.group(1)), int(m.group(2)), int(m.group(3))
            exp = Fraction(a * nn - v, nn - 1)
            if F(aval) != exp:
                print(f"Q{n} REMOVED wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["removed"] = type_counts.get("removed", 0) + 1
            continue

        # 8) Excluded number: avg of n is A, rest avg is B -> excluded
        m = re.match(r"The average of (\d+) numbers is (\d+)\. If one of the numbers is excluded, the average of the remaining \d+ numbers is (\d+)\.", stem)
        if m:
            nn, a, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
            exp = Fraction(a * nn - b * (nn - 1))
            if F(aval) != exp:
                print(f"Q{n} EXCLUDED wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["excluded"] = type_counts.get("excluded", 0) + 1
            continue

        # 9) Weighted average boys/girls
        m = re.match(r"In a class, the average marks of (\d+) boys is (\d+) and the average marks of (\d+) girls is (\d+)\.", stem)
        if m:
            n1, a1, n2, a2 = (int(m.group(i)) for i in range(1, 5))
            exp = Fraction(n1 * a1 + n2 * a2, n1 + n2)
            if F(aval) != exp:
                print(f"Q{n} WEIGHTED wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["weighted"] = type_counts.get("weighted", 0) + 1
            continue

        # 10) a,b,c avg X; a,b avg Y -> c
        m = re.match(r"The average of three numbers a, b and c is (\d+)\. If the average of a and b is (\d+),", stem)
        if m:
            x, y = int(m.group(1)), int(m.group(2))
            exp = Fraction(3 * x - 2 * y)
            if F(aval) != exp:
                print(f"Q{n} ABC wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["abc"] = type_counts.get("abc", 0) + 1
            continue

        # 11) Innings raise average
        m = re.match(r"A batsman has an average of (\d+) runs in (\d+) innings\. How many runs must he score in his next innings to raise his average to (\d+)\?", stem)
        if m:
            cur, played, new = int(m.group(1)), int(m.group(2)), int(m.group(3))
            exp = Fraction(new * (played + 1) - cur * played)
            if F(aval) != exp:
                print(f"Q{n} INNINGS-RAISE wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["innings_raise"] = type_counts.get("innings_raise", 0) + 1
            continue

        # 12) Innings drop/new average after scoring
        m = re.match(r"A cricketer has a batting average of (\d+) runs in (\d+) innings\. In the next innings he scores (\d+) runs\.", stem)
        if m:
            cur, played, score = int(m.group(1)), int(m.group(2)), int(m.group(3))
            exp = Fraction(cur * played + score, played + 1)
            if F(aval) != exp:
                print(f"Q{n} INNINGS-NEW wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["innings_new"] = type_counts.get("innings_new", 0) + 1
            continue

        # 13) Age person joins -> new average
        m = re.match(r"The average age of (\d+) members of a club is (\d+) years\. If a new member aged (\d+) years joins", stem)
        if m:
            nn, a, j = int(m.group(1)), int(m.group(2)), int(m.group(3))
            exp = Fraction(a * nn + j, nn + 1)
            if F(aval) != exp:
                print(f"Q{n} AGE-JOIN wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["age_join"] = type_counts.get("age_join", 0) + 1
            continue

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 4, "Fewer than 4 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
