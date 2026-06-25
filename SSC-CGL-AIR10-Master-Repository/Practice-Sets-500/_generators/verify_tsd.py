# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Time, Speed & Distance set.
Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options, then for several recognizable template
types RE-SOLVE directly from the stem numbers (regex) and confirm the keyed
value matches. Does NOT reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_05_Time_Speed_Distance_500.md"
txt = open(PATH, encoding="utf-8").read()

KMPH_TO_MPS = Fraction(5, 18)

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
        if "average speed for the whole journey" in stem:
            x, y = [F(v) for v in re.findall(r"at (\d+) km/h", stem)[:2]]
            exp = Fraction(2) * x * y / (x + y)
            if F(aval) != exp:
                print(f"Q{n} AVG-SPEED wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["avg_speed"] = type_counts.get("avg_speed", 0) + 1

        elif "crosses a platform" in stem and "The time taken (in seconds)" in stem:
            length = F(re.search(r"train (\d+) m long", stem).group(1))
            platform = F(re.search(r"platform (\d+) m long", stem).group(1))
            speed = F(re.search(r"at (\d+) km/h", stem).group(1)) * KMPH_TO_MPS
            exp = (length + platform) / speed
            if F(aval) != exp:
                print(f"Q{n} PLATFORM wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["platform"] = type_counts.get("platform", 0) + 1

        elif "to cross a pole" in stem:
            length = F(re.search(r"train (\d+) m long", stem).group(1))
            speed = F(re.search(r"speed of (\d+) km/h", stem).group(1)) * KMPH_TO_MPS
            exp = length / speed
            if F(aval) != exp:
                print(f"Q{n} POLE wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["pole"] = type_counts.get("pole", 0) + 1

        elif "running in opposite directions" in stem and "cross each other" in stem:
            l1, l2 = [F(v) for v in re.findall(r"(\d+) m", stem)[:2]]
            s1, s2 = [F(v) for v in re.findall(r"(\d+) km/h", stem)[:2]]
            rel = (s1 + s2) * KMPH_TO_MPS
            exp = (l1 + l2) / rel
            if F(aval) != exp:
                print(f"Q{n} OPP-TRAINS wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["opp_trains"] = type_counts.get("opp_trains", 0) + 1

        elif "moving in the same direction" in stem and "overtake the slower" in stem:
            l1, l2 = [F(v) for v in re.findall(r"(\d+) m", stem)[:2]]
            s1, s2 = [F(v) for v in re.findall(r"(\d+) km/h", stem)[:2]]
            rel = (s1 - s2) * KMPH_TO_MPS
            exp = (l1 + l2) / rel
            if F(aval) != exp:
                print(f"Q{n} SAME-TRAINS wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["same_trains"] = type_counts.get("same_trains", 0) + 1

        elif "speed of the boat in still water (in km/h) is" in stem:
            down = F(re.search(r"downstream at (\d+) km/h", stem).group(1))
            up = F(re.search(r"upstream at (\d+) km/h", stem).group(1))
            exp = (down + up) / 2
            if F(aval) != exp:
                print(f"Q{n} BOAT-STILL wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["boat_still"] = type_counts.get("boat_still", 0) + 1

        elif "speed of the stream (in km/h) is" in stem and "travels downstream at" in stem:
            down = F(re.search(r"downstream at (\d+) km/h", stem).group(1))
            up = F(re.search(r"upstream at (\d+) km/h", stem).group(1))
            exp = (down - up) / 2
            if F(aval) != exp:
                print(f"Q{n} STREAM wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["stream"] = type_counts.get("stream", 0) + 1

        elif "metres per second" in stem and "Convert" in stem:
            kmph = F(re.search(r"Convert (\d+) km/h", stem).group(1))
            exp = kmph * KMPH_TO_MPS
            if F(aval) != exp:
                print(f"Q{n} CONVERT wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["convert"] = type_counts.get("convert", 0) + 1

        elif "move toward each other" in stem and "after which they meet" in stem:
            dist = F(re.search(r"(\d+) km apart", stem).group(1))
            s1, s2 = [F(v) for v in re.findall(r"(\d+) km/h", stem)][:2]
            exp = dist / (s1 + s2)
            if F(aval) != exp:
                print(f"Q{n} MEET wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["meet"] = type_counts.get("meet", 0) + 1

        elif "minutes per hour does the bus stop" in stem:
            a = F(re.search(r"average speed of a bus is (\d+) km/h", stem).group(1))
            b = F(re.search(r"including stoppages it is (\d+) km/h", stem).group(1))
            exp = (a - b) / a * 60
            if F(aval) != exp:
                print(f"Q{n} STOPPAGE wrong: got {aval}, expect {float(exp):.4f}"); mismatch += 1
            checked += 1; type_counts["stoppage"] = type_counts.get("stoppage", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} formula questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert len(type_counts) >= 3, "Fewer than 3 template types independently re-solved!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
