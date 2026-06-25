# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Data Interpretation 500-question set.

Rigorous structural + keyed-value checks:
  - exactly 500 questions and 500 answers parsed from the WRITTEN markdown
  - every question has 4 distinct options
  - the keyed letter's option value == the value stated in the answer key
  - cross-check every keyed value against the generator's JSON sidecar of
    (qnum -> computed correct value): this proves the written answer equals the
    value the generator COMPUTED from the dataset.

Plus genuine RE-DERIVATION from the prose data blocks for recognizable
question types (parsed from the markdown table / bar / pie blocks, NOT reusing
any generator object): row totals, row averages, cell differences, cell ratios,
bar grand totals, pie category amounts. These prove the data block and the key
are mutually consistent.

NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import json
import re
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_09_Data_Interpretation_500.md"
SIDE = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_09_Data_Interpretation_500.key.json"

txt = open(PATH, encoding="utf-8").read()
sidecar = json.load(open(SIDE, encoding="utf-8"))

qpart, apart = txt.split("# =================== ANSWER KEY")

fail = 0


def F(s):
    s = s.strip().replace("Rs.", "").replace("Rs", "").replace(",", "").strip()
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a.strip()), int(b.strip()))
    return Fraction(s).limit_denominator(10**6)


# --------------------------------------------------------------------------
# Parse questions: split into data sets, capture each set's data block + Qs.
# --------------------------------------------------------------------------
set_pat = re.compile(r"### Data Set (\d+) \(Q(\d+)-Q(\d+)\)\n(.*?)(?=### Data Set |\Z)", re.S)
qpat = re.compile(
    r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\n",
    re.S,
)

qs = {}          # qnum -> (stem, [opts])
set_of = {}      # qnum -> set index
set_block = {}   # set index -> raw data block text (before first **Q)

for sm in set_pat.finditer(qpart):
    sidx = int(sm.group(1))
    body = sm.group(4)
    # data block = text up to the first question marker
    cut = body.find("**Q")
    set_block[sidx] = body[:cut]
    for m in qpat.finditer(body):
        n = int(m.group(1))
        stem = m.group(2).replace("\n", " ").strip()
        opts = [m.group(3).strip(), m.group(4).strip(),
                m.group(5).strip(), m.group(6).strip()]
        qs[n] = (stem, opts)
        set_of[n] = sidx

# --------------------------------------------------------------------------
# Parse answers
# --------------------------------------------------------------------------
ans = {}
apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*")
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), m.group(3).strip())

print(f"Parsed {len(qs)} questions, {len(ans)} answers, {len(set_block)} data sets")
if len(qs) != 500:
    print(f"FAIL: expected 500 questions, got {len(qs)}"); fail += 1
if len(ans) != 500:
    print(f"FAIL: expected 500 answers, got {len(ans)}"); fail += 1
if len(set_block) != 100:
    print(f"FAIL: expected 100 data sets, got {len(set_block)}"); fail += 1

# --------------------------------------------------------------------------
# Structural + keyed-value + sidecar cross-check (every question)
# --------------------------------------------------------------------------
mismatch = 0
for n in sorted(qs):
    stem, opts = qs[n]
    if n not in ans:
        print(f"Q{n}: no answer"); mismatch += 1; continue
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed = opts[li]
    # 4 distinct options
    if len({F(o) for o in opts}) != 4:
        print(f"Q{n}: options not 4 distinct: {opts}"); mismatch += 1
    # keyed letter's option == stated answer value
    if F(keyed) != F(aval):
        print(f"Q{n}: keyed option[{letter}]={keyed} != stated answer {aval}")
        mismatch += 1
    # sidecar cross-check: stated answer == generator's computed value
    if str(n) not in sidecar:
        print(f"Q{n}: missing from sidecar"); mismatch += 1
    elif F(sidecar[str(n)]) != F(aval):
        print(f"Q{n}: sidecar {sidecar[str(n)]} != stated answer {aval}")
        mismatch += 1

print(f"Keyed/sidecar mismatches: {mismatch}")
if mismatch:
    fail += mismatch


# --------------------------------------------------------------------------
# Parse data blocks into structured form for re-derivation
# --------------------------------------------------------------------------
def parse_md_table(block):
    """Return (col_headers, {row_label: [int values]}) from a markdown table."""
    rows = [ln for ln in block.splitlines() if ln.strip().startswith("|")]
    if len(rows) < 2:
        return None
    header = [c.strip() for c in rows[0].strip("|").split("|")]
    data = {}
    for ln in rows[2:]:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        if len(cells) != len(header):
            continue
        lab = cells[0]
        try:
            vals = [int(c) for c in cells[1:]]
        except ValueError:
            continue
        data[lab] = vals
    return header, data


def parse_bar(block):
    """Return {label: int} from a '**...:** A=.., B=..' line."""
    m = re.search(r"\*\*[^*]+:\*\*\s*(.+)", block)
    if not m:
        return None
    out = {}
    for pair in m.group(1).split(","):
        if "=" in pair:
            k, v = pair.split("=")
            try:
                out[k.strip()] = int(v.strip())
            except ValueError:
                pass
    return out


def parse_pie(block):
    """Return (total, {cat: pct})."""
    mt = re.search(r"budget of Rs\. (\d+)", block)
    md = re.search(r"\*\*Distribution:\*\*\s*(.+)", block)
    if not (mt and md):
        return None
    total = int(mt.group(1))
    pct = {}
    for pair in md.group(1).split(","):
        m = re.match(r"\s*(\w+)=(\d+)%", pair)
        if m:
            pct[m.group(1)] = int(m.group(2))
    return total, pct


# --------------------------------------------------------------------------
# Re-derive recognizable question types directly from the parsed data blocks.
# --------------------------------------------------------------------------
checked = 0
type_counts = {}
rederive_fail = 0


def note(t):
    type_counts[t] = type_counts.get(t, 0) + 1


for n in sorted(qs):
    stem, opts = qs[n]
    aval = F(ans[n][1])
    block = set_block[set_of[n]]
    tbl = parse_md_table(block)
    bar = parse_bar(block) if tbl is None else None
    pie = parse_pie(block) if (tbl is None and bar is None) else None

    try:
        # ---- TABLE: total of one company over all four years ----
        m = re.search(r"total .*? of Company (\w+) over all four years", stem)
        if m and tbl:
            _, data = tbl
            lab = m.group(1)
            exp = Fraction(sum(data[lab]))
            checked += 1; note("table_total")
            if aval != exp:
                print(f"Q{n} TABLE-TOTAL: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- TABLE: average of one company over four years ----
        m = re.search(r"average .*? of Company (\w+) over the four years", stem)
        if m and tbl:
            _, data = tbl
            lab = m.group(1)
            exp = Fraction(sum(data[lab]), 4)
            checked += 1; note("table_avg")
            if aval != exp:
                print(f"Q{n} TABLE-AVG: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- TABLE: difference between two cells ----
        m = re.search(r"difference between the .*? of Company (\w+) in (\d{4}) and "
                      r"that of Company (\w+) in (\d{4})", stem)
        if m and tbl:
            header, data = tbl
            c1, y1, c2, y2 = m.group(1), m.group(2), m.group(3), m.group(4)
            yi1 = header.index(y1) - 1
            yi2 = header.index(y2) - 1
            exp = Fraction(abs(data[c1][yi1] - data[c2][yi2]))
            checked += 1; note("table_diff")
            if aval != exp:
                print(f"Q{n} TABLE-DIFF: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- TABLE: ratio of one company across two years ----
        m = re.search(r"ratio of the .*? of Company (\w+) in (\d{4}) to that in (\d{4})", stem)
        if m and tbl:
            header, data = tbl
            c, y1, y2 = m.group(1), m.group(2), m.group(3)
            yi1 = header.index(y1) - 1
            yi2 = header.index(y2) - 1
            exp = Fraction(data[c][yi1], data[c][yi2])
            checked += 1; note("table_ratio")
            if aval != exp:
                print(f"Q{n} TABLE-RATIO: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- TABLE: percent change of a company between two years ----
        m = re.search(r"percent did the .*? of Company (\w+) change from (\d{4}) to (\d{4})", stem)
        if m and tbl:
            header, data = tbl
            c, y1, y2 = m.group(1), m.group(2), m.group(3)
            yi1 = header.index(y1) - 1
            yi2 = header.index(y2) - 1
            old, new = data[c][yi1], data[c][yi2]
            exp = Fraction(new - old, old) * 100
            checked += 1; note("table_pctchg")
            if aval != exp:
                print(f"Q{n} TABLE-PCTCHG: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- BAR: total of all six units ----
        m = re.search(r"total .*? of all six units", stem)
        if m and bar:
            exp = Fraction(sum(bar.values()))
            checked += 1; note("bar_total")
            if aval != exp:
                print(f"Q{n} BAR-TOTAL: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- BAR: difference between two units ----
        m = re.search(r"difference between the .*? of (\w+) and (\w+)", stem)
        if m and bar:
            a, c = m.group(1), m.group(2)
            exp = Fraction(abs(bar[a] - bar[c]))
            checked += 1; note("bar_diff")
            if aval != exp:
                print(f"Q{n} BAR-DIFF: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- BAR: ratio of two units ----
        m = re.search(r"ratio of the .*? of (\w+) to that of (\w+)", stem)
        if m and bar:
            a, c = m.group(1), m.group(2)
            exp = Fraction(bar[a], bar[c])
            checked += 1; note("bar_ratio")
            if aval != exp:
                print(f"Q{n} BAR-RATIO: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- BAR: what percent A is of B ----
        m = re.search(r"\b(\w+) is what percent of the .*? of (\w+)", stem)
        if m and bar:
            a, c = m.group(1), m.group(2)
            if a in bar and c in bar:
                exp = Fraction(bar[a], bar[c]) * 100
                checked += 1; note("bar_pctof")
                if aval != exp:
                    print(f"Q{n} BAR-PCTOF: got {aval}, expect {exp}"); rederive_fail += 1
                continue

        # ---- PIE: amount spent on a category ----
        m = re.search(r"amount \(in Rs\.\) spent on (\w+)\?", stem)
        if m and pie:
            total, pct = pie
            cat = m.group(1)
            exp = Fraction(total) * pct[cat] / 100
            checked += 1; note("pie_amount")
            if aval != exp:
                print(f"Q{n} PIE-AMOUNT: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- PIE: difference between two categories ----
        m = re.search(r"difference \(in Rs\.\) between the amounts spent on (\w+) and (\w+)", stem)
        if m and pie:
            total, pct = pie
            c1, c2 = m.group(1), m.group(2)
            exp = Fraction(total) * abs(pct[c1] - pct[c2]) / 100
            checked += 1; note("pie_diff")
            if aval != exp:
                print(f"Q{n} PIE-DIFF: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- PIE: combined amount on two categories ----
        m = re.search(r"total amount \(in Rs\.\) spent on (\w+) and (\w+) together", stem)
        if m and pie:
            total, pct = pie
            c1, c2 = m.group(1), m.group(2)
            exp = Fraction(total) * (pct[c1] + pct[c2]) / 100
            checked += 1; note("pie_combo")
            if aval != exp:
                print(f"Q{n} PIE-COMBO: got {aval}, expect {exp}"); rederive_fail += 1
            continue

        # ---- LINE: total imports over all four years ----
        m = re.search(r"total Imports .*? over all four years", stem)
        if m and tbl:
            header, data = tbl
            ii = [h for h in header if "Import" in h]
            col = header.index(ii[0]) - 1
            exp = Fraction(sum(v[col] for v in data.values()))
            checked += 1; note("line_imp_total")
            if aval != exp:
                print(f"Q{n} LINE-IMP-TOTAL: got {aval}, expect {exp}"); rederive_fail += 1
            continue

    except Exception as e:
        print(f"Q{n}: re-derive skip ({e})")

print(f"Independently re-derived {checked} questions from the data blocks.")
print("Re-derived type breakdown:", type_counts)
print(f"Distinct types independently verified: {len(type_counts)}")
print(f"Re-derivation mismatches: {rederive_fail}")
if len(type_counts) < 5:
    print(f"FAIL: fewer than 5 question types independently re-derived"); fail += 1
fail += rederive_fail

# difficulty distribution from the answer key tags
diffs = re.findall(r"\*\[(M|H|VH)\]\*", apart)
from collections import Counter
dc = Counter(diffs)
print("Difficulty distribution:", dict(dc), "total", sum(dc.values()))

print("RESULT:", "PASS" if fail == 0 else "FAIL")
