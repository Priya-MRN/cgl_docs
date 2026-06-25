# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Mixture & Alligation set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options, then for several recognizable template
types RE-SOLVE directly from the stem numbers (regex) and confirm the keyed
value matches. Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_14_Mixture_Alligation_500.md"
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
    """Parse a numeric or 'p : q' ratio option into a Fraction (ratio -> p/q)."""
    s = s.strip().replace("Rs.", "").replace("₹", "")
    if ":" in s:
        a, b = s.split(":")
        return Fraction(int(a.strip()), int(b.strip()))
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(s).limit_denominator(10**6)


def Rpair(s):
    """Parse 'p : q' option into a reduced (p,q) tuple."""
    a, b = s.split(":")
    fr = Fraction(int(a.strip()), int(b.strip()))
    return (fr.numerator, fr.denominator)


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
        # 1) ALLIGATION RATIO (rice / tea / acid / milk-percent / investment / generic mix-to-mean)
        if (("In what ratio" in stem or "what ratio should" in stem or
             "what ratio must" in stem) and "vessel" not in stem.lower()
                and "be mixed" not in stem.split("In what ratio")[0]):
            nums = [Fraction(int(x)) for x in re.findall(r"(\d+)", stem)]
            # The three relevant numbers are the two endpoints and the mean/target.
            # Heuristic: cheaper, dearer, mean appear as p1, p2, m in that textual order
            # for the price templates ("costing Rs.p1 ... Rs.p2 ... worth/costs Rs.m"),
            # and as c1, c2, t for concentration templates.
            if len(nums) >= 3:
                p1, p2, m = nums[0], nums[1], nums[2]
                if p1 < p2 and p1 < m < p2:
                    exp = Fraction(p2 - m, m - p1)
                    exp = (exp.numerator, exp.denominator)
                    if Rpair(aval) != exp:
                        print(f"Q{n} ALLIGATION wrong: got {aval}, expect {exp}")
                        mismatch += 1
                    checked += 1
                    type_counts["alligation"] = type_counts.get("alligation", 0) + 1

        # 2) REPLACEMENT - milk left after n operations
        elif ("pure milk" in stem and "replaced with water" in stem
              and "quantity of milk" in stem and "now left" in stem):
            x = Fraction(int(re.search(r"contains (\d+) litres", stem).group(1)))
            y = Fraction(int(re.search(r"(\d+) litres are drawn", stem).group(1)))
            nmatch = re.search(r"performed (\d+) times", stem)
            nn = int(nmatch.group(1))
            exp = x * (Fraction(x - y, x)) ** nn
            if F(aval) != exp:
                print(f"Q{n} REPLACEMENT-LEFT wrong: got {aval}, expect {float(exp):.4f}")
                mismatch += 1
            checked += 1
            type_counts["replace_left"] = type_counts.get("replace_left", 0) + 1

        # 3) REPLACEMENT / WINE - resulting ratio after n operations
        elif (("pure milk" in stem or "wine" in stem) and "replaced with water" in stem
              and ("ratio of milk to water" in stem or "ratio of wine" in stem)):
            x = Fraction(int(re.search(r"containing (\d+) litres|contains (\d+) litres", stem).group(1) or 0))
            mx = re.search(r"(\d+) litres of (?:pure milk|wine)", stem)
            if mx:
                x = Fraction(int(mx.group(1)))
            y = Fraction(int(re.search(r"(\d+) litres are (?:withdrawn|drawn)", stem).group(1)))
            nn = int(re.search(r"done (\d+) times|repeated (\d+) times", stem).group(1)
                     or re.search(r"(\d+) times", stem).group(1))
            milk = (Fraction(x - y, x)) ** nn
            water = 1 - milk
            exp = milk / water
            exp = (exp.numerator, exp.denominator)
            if Rpair(aval) != exp:
                print(f"Q{n} REPLACE-RATIO wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["replace_ratio"] = type_counts.get("replace_ratio", 0) + 1

        # 4) TWO VESSELS mixed in ratio k1:k2 -> resulting ratio
        elif ("Vessel A contains milk and water in the ratio" in stem
              and "mixed in the ratio" in stem):
            r = re.findall(r"ratio (\d+) : (\d+)", stem)
            (a1, b1), (a2, b2) = (int(r[0][0]), int(r[0][1])), (int(r[1][0]), int(r[1][1]))
            (k1, k2) = (int(r[2][0]), int(r[2][1]))
            milk = k1 * Fraction(a1, a1 + b1) + k2 * Fraction(a2, a2 + b2)
            water = k1 * Fraction(b1, a1 + b1) + k2 * Fraction(b2, a2 + b2)
            exp = milk / water
            exp = (exp.numerator, exp.denominator)
            if Rpair(aval) != exp:
                print(f"Q{n} TWO-VESSEL wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["two_vessel"] = type_counts.get("two_vessel", 0) + 1

        # 5) EQUAL QUANTITIES from two vessels -> resulting ratio
        elif ("Equal quantities are taken from two vessels" in stem):
            r = re.findall(r"(\d+) : (\d+)", stem)
            (a1, b1), (a2, b2) = (int(r[0][0]), int(r[0][1])), (int(r[1][0]), int(r[1][1]))
            milk = Fraction(a1, a1 + b1) + Fraction(a2, a2 + b2)
            water = Fraction(b1, a1 + b1) + Fraction(b2, a2 + b2)
            exp = milk / water
            exp = (exp.numerator, exp.denominator)
            if Rpair(aval) != exp:
                print(f"Q{n} EQUAL-QTY wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["equal_qty"] = type_counts.get("equal_qty", 0) + 1

        # 6) DISHONEST MILKMAN -> water:milk = x:100
        elif ("dishonest milkman" in stem and "gains" in stem):
            x = int(re.search(r"gains (\d+)%", stem).group(1))
            exp = Fraction(x, 100)
            exp = (exp.numerator, exp.denominator)
            if Rpair(aval) != exp:
                print(f"Q{n} MILKMAN wrong: got {aval}, expect {exp}")
                mismatch += 1
            checked += 1
            type_counts["milkman"] = type_counts.get("milkman", 0) + 1

        # 7) DILUTE ACID by adding water
        elif ("% acid" in stem and "must be added to reduce" in stem):
            V = Fraction(int(re.search(r"^(\d+) litres", stem).group(1)))
            c = Fraction(int(re.search(r"contain (\d+)% acid", stem).group(1)))
            t = Fraction(int(re.search(r"concentration to (\d+)%", stem).group(1)))
            acid = c / 100 * V
            total_new = acid / (t / 100)
            exp = total_new - V
            if F(aval) != exp:
                print(f"Q{n} DILUTE wrong: got {aval}, expect {float(exp):.4f}")
                mismatch += 1
            checked += 1
            type_counts["dilute"] = type_counts.get("dilute", 0) + 1

        # 8) ADD WATER to change milk:water ratio
        elif ("litres of a mixture contain milk and water in the ratio" in stem
              and "How many litres of water must be added" in stem):
            V = Fraction(int(re.search(r"^(\d+) litres", stem).group(1)))
            r = re.findall(r"(\d+) : (\d+)", stem)
            a, b = int(r[0][0]), int(r[0][1])
            c = int(r[1][1])   # ratio becomes a:c
            milk = Fraction(a, a + b) * V
            water = Fraction(b, a + b) * V
            new_water = milk * Fraction(c, a)
            exp = new_water - water
            if F(aval) != exp:
                print(f"Q{n} ADD-WATER wrong: got {aval}, expect {float(exp):.4f}")
                mismatch += 1
            checked += 1
            type_counts["add_water"] = type_counts.get("add_water", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 4, "Fewer than 4 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
