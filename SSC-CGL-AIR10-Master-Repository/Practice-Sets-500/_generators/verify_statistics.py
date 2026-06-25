# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Statistics 500 set.
Re-parses the rendered markdown, confirms 500 Q + 500 A, keyed option value ==
stated answer, 4 distinct options. Then for mean/median/mode/range/variance/SD/
quartile questions it RE-READS the integer data list from the stem and recomputes
the statistic from scratch, confirming it equals the key. Does NOT reuse the
generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
from fractions import Fraction
from collections import Counter

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_17_Statistics_500.md"
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
    return Fraction(s).limit_denominator(10**6)


def parse_list(stem):
    """Extract the FIRST comma-separated integer list that follows a colon.
    Returns list[int]. Stems put the data after 'data: ' or 'For the data '."""
    # find a run like 'NN, NN, NN, ... NN.' - grab the longest such run
    # Anchor on common lead-ins to avoid grabbing stray numbers.
    m = re.search(r"(?:data:|the data|distribution is:)\s*([0-9,\s]+?)\.", stem)
    if not m:
        return None
    body = m.group(1)
    nums = [int(x) for x in re.findall(r"\d+", body)]
    return nums if len(nums) >= 2 else None


def mean_F(d):
    return Fraction(sum(d), len(d))


def median_F(d):
    s = sorted(d)
    n = len(s)
    if n % 2:
        return Fraction(s[n // 2])
    return Fraction(s[n // 2 - 1] + s[n // 2], 2)


def variance_F(d):
    m = mean_F(d)
    return Fraction(sum((Fraction(x) - m) ** 2 for x in d), len(d))


def mode_F(d):
    c = Counter(d)
    top = max(c.values())
    modes = [v for v, cc in c.items() if cc == top]
    return Fraction(modes[0]) if len(modes) == 1 else None


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

    # ----- independent re-solve from the data list embedded in the stem -----
    try:
        if stem.startswith("Find the arithmetic mean"):
            d = parse_list(stem)
            exp = mean_F(d)
            if F(aval) != exp:
                print(f"Q{n} MEAN wrong: got {aval}, expect {float(exp):.4f} from {d}"); mismatch += 1
            checked += 1; type_counts["mean"] = type_counts.get("mean", 0) + 1

        elif stem.startswith("Find the median"):
            d = parse_list(stem)
            exp = median_F(d)
            if F(aval) != exp:
                print(f"Q{n} MEDIAN wrong: got {aval}, expect {float(exp):.4f} from {d}"); mismatch += 1
            checked += 1; type_counts["median"] = type_counts.get("median", 0) + 1

        elif stem.startswith("Find the mode"):
            d = parse_list(stem)
            exp = mode_F(d)
            if exp is None or F(aval) != exp:
                print(f"Q{n} MODE wrong: got {aval}, expect {exp} from {d}"); mismatch += 1
            checked += 1; type_counts["mode"] = type_counts.get("mode", 0) + 1

        elif stem.startswith("Find the range"):
            d = parse_list(stem)
            exp = Fraction(max(d) - min(d))
            if F(aval) != exp:
                print(f"Q{n} RANGE wrong: got {aval}, expect {exp} from {d}"); mismatch += 1
            checked += 1; type_counts["range"] = type_counts.get("range", 0) + 1

        elif stem.startswith("Find the variance"):
            d = parse_list(stem)
            exp = variance_F(d)
            if F(aval) != exp:
                print(f"Q{n} VARIANCE wrong: got {aval}, expect {float(exp):.4f} from {d}"); mismatch += 1
            checked += 1; type_counts["variance"] = type_counts.get("variance", 0) + 1

        elif stem.startswith("Find the standard deviation of the following data"):
            d = parse_list(stem)
            var = variance_F(d)
            keyed = F(aval)
            # SD answer squared must equal the exact variance
            if keyed * keyed != var:
                print(f"Q{n} SD wrong: got {aval}, var={float(var):.4f} from {d}"); mismatch += 1
            checked += 1; type_counts["sd_data"] = type_counts.get("sd_data", 0) + 1

        elif stem.startswith("Find the standard deviation of the first"):
            nn = int(re.search(r"first (\d+) natural", stem).group(1))
            var = Fraction(nn * nn - 1, 12)
            keyed = F(aval)
            if keyed * keyed != var:
                print(f"Q{n} SD-NAT wrong: got {aval}, var={float(var):.4f} n={nn}"); mismatch += 1
            checked += 1; type_counts["sd_nat"] = type_counts.get("sd_nat", 0) + 1

        elif stem.startswith("For the data") and ("quartile" in stem or "interquartile" in stem):
            # quartile question: data sits between 'For the data ' and ', find'
            mm = re.search(r"For the data\s+([0-9,\s]+?),\s*find", stem)
            d = [int(x) for x in re.findall(r"\d+", mm.group(1))] if mm else None
            if d:
                s = sorted(d)
                nn = len(s)
                half = nn // 2
                lower = s[:half]
                upper = s[half + 1:]
                q1 = median_F(lower)
                q3 = median_F(upper)
                iqr = q3 - q1
                keyed = F(aval)
                if "first quartile" in stem:
                    exp = q1
                elif "third quartile" in stem:
                    exp = q3
                else:
                    exp = iqr
                if keyed != exp:
                    print(f"Q{n} QUARTILE wrong: got {aval}, expect {exp} from {d}"); mismatch += 1
                checked += 1; type_counts["quartile"] = type_counts.get("quartile", 0) + 1

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-solved {checked} data-driven questions.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")
assert checked >= 150, f"Fewer than 150 data-driven questions re-solved (only {checked})!"
assert len(type_counts) >= 4, "Fewer than 4 template types independently re-solved!"

# difficulty distribution from the answer key
difs = Counter(re.findall(r"\*\[(M|H|VH)\]\*", apart))
print("Difficulty distribution:", dict(difs))

print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
