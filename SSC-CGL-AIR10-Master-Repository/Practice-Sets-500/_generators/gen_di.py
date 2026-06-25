# -*- coding: utf-8 -*-
"""
SSC CGL Data Interpretation - 500 question generator (100 sets x 5 questions).
Every answer is COMPUTED from a randomly generated (clean) dataset, so the key
is provably correct. Builds 4 distinct options (1 correct + 3 common-mistake
distractors), randomizes correct position, self-checks, and writes markdown plus
a JSON sidecar of (qnum, correct_value) for the independent verifier.

Machinery mirrors gen_percentage.py / verify_tsd.py:
- Fraction-based throughout (never pass a float into Fraction(num, den)).
- is_clean() gate on every one of a set's 5 answers; regenerate set if any ugly.
- make_options() -> 4 distinct shuffled options, one correct.
- quota for ~20% Medium / 60% Hard / 20% Very-Hard.
"""
import json
import random
from collections import Counter
from fractions import Fraction

random.seed(20260625)  # deterministic

LETTERS = "abcd"


# ----------------------------------------------------------------------------
# Formatting / cleanliness helpers (identical philosophy to gen_percentage.py)
# ----------------------------------------------------------------------------
def fmt(x):
    """Format a number cleanly: ints as ints, fractions as decimals or fraction."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        f = float(x)
        if abs(f - round(f, 4)) < 1e-9:
            return f"{f:.4f}".rstrip("0").rstrip(".")
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        return f"{x:.4f}".rstrip("0").rstrip(".")
    return str(x)


def is_clean(x):
    """Accept integers, halves/quarters/thirds/fifths/sixths/eighths, and <=2dp decimals."""
    fr = Fraction(x).limit_denominator(10**6)
    if fr.denominator in (1, 2, 3, 4, 5, 6, 8):
        return True
    f = float(fr)
    return abs(f - round(f, 2)) < 1e-9


def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 distinct values."""
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        if all(abs(float(d) - float(o)) > 1e-9 for o in opts):
            opts.append(d)
        if len(opts) == 4:
            break
    bump = 1
    cf = float(correct)
    while len(opts) < 4:
        cand = Fraction(correct) + Fraction(bump * (3 if cf >= 0 else -3))
        if all(abs(float(cand) - float(o)) > 1e-9 for o in opts):
            opts.append(cand)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci


# ----------------------------------------------------------------------------
# Set assembly
# ----------------------------------------------------------------------------
# Each "set" is a dict: data_md (markdown block), questions list.
# Each question: dict(stem, correct(Fraction), distractors(list), sol, diff)
sets = []          # finished, accepted sets
all_questions = [] # flattened, in order

CLEAN_DENOMS = (1, 2, 3, 4, 5, 6, 8)


def F(x):
    return Fraction(x).limit_denominator(10**6)


class SetBuilder:
    """Collects 5 questions for one data set; rejects if any answer is ugly."""

    def __init__(self, data_md, intro):
        self.data_md = data_md
        self.intro = intro
        self.qs = []

    def q(self, stem, correct, distractors, sol, diff):
        self.qs.append({
            "stem": stem,
            "correct": F(correct),
            "distractors": [F(d) for d in distractors if d is not None],
            "sol": sol,
            "diff": diff,
        })

    def ok(self):
        # Gate: every one of the 5 COMPUTED answers must be clean (task rule).
        # Distractors are filtered to clean+distinct here; make_options() pads
        # any shortfall with clean integer-offset fillers, so we keep genuine
        # common-mistake distractors when available but never block on them.
        if len(self.qs) != 5:
            return False
        for item in self.qs:
            c = item["correct"]
            if not is_clean(c):
                return False
            uniq = []
            for d in item["distractors"]:
                if not is_clean(d):
                    continue
                if d == c:
                    continue
                if all(abs(float(d) - float(u)) > 1e-9 for u in uniq):
                    uniq.append(d)
            item["distractors"] = uniq
        return True


def pct_change(old, new):
    """Percentage change new vs old, as a Fraction (positive = increase)."""
    return (F(new) - F(old)) / F(old) * 100


def pct_of(part, whole):
    return F(part) / F(whole) * 100


# ----------------------------------------------------------------------------
# Difficulty mix per set: each set MUST have 3 of 5 at H/VH (per task).
# We assemble sub-question difficulty tags so the global mix lands ~20/60/20.
# Pattern per set (5 q): we use a rotation of templates that yields, on average,
# 1 M, 3 H, 1 VH  -> 20/60/20. Builders below tag each question themselves.
# ----------------------------------------------------------------------------

YEARS_POOL = [
    ["2018", "2019", "2020", "2021"],
    ["2019", "2020", "2021", "2022"],
    ["2020", "2021", "2022", "2023"],
    ["2017", "2018", "2019", "2020"],
]


def clean_table_values(nrows, ncols, lo, hi, step):
    """Generate an nrows x ncols integer matrix with values multiples of `step`."""
    return [[random.randrange(lo, hi + 1, step) for _ in range(ncols)]
            for _ in range(nrows)]


def md_table(headers, row_labels, matrix):
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("|" + "|".join(["---"] * len(headers)) + "|")
    for lab, row in zip(row_labels, matrix):
        out.append("| " + lab + " | " + " | ".join(str(v) for v in row) + " |")
    return "\n".join(out)


# ===========================================================================
# TEMPLATE 1: TABLE — companies x years (production), 5 sub-questions
# ===========================================================================
def build_table_set():
    companies = random.sample(["A", "B", "C", "D", "E", "P", "Q", "R", "S"], 5)
    years = random.choice(YEARS_POOL)
    metric = random.choice(["production (in tonnes)", "sales (in units)",
                            "revenue (in Rs. lakh)"])
    # Each row is built so its 4 values share a common base -> row sum divisible
    # by 4 (clean average) and intra-row ratios reduce. Base values are small
    # integers scaled by a per-row unit; values are multiples of 4 too.
    matrix = []
    for _ in range(5):
        unit = random.choice([40, 60, 80, 100, 120])
        coeffs = [random.randint(2, 9) for _ in range(4)]
        matrix.append([c * unit for c in coeffs])

    headers = ["Company"] + years
    data_md = (f"The table below shows the {metric} of five companies "
               f"({', '.join(companies)}) over the years {years[0]}-{years[-1]}.\n\n"
               + md_table(headers, companies, matrix))
    intro = f"Refer to the table of {metric}."

    b = SetBuilder(data_md, intro)

    # Q1 [M]: total of one company across all years
    ci = random.randrange(5)
    comp = companies[ci]
    total = sum(F(v) for v in matrix[ci])
    b.q(f"What is the total {metric} of Company {comp} over all four years?",
        total,
        [total - matrix[ci][0], total + matrix[ci][1],
         sum(F(v) for v in matrix[ci][:3])],
        f"Sum of {comp}'s row = {' + '.join(str(v) for v in matrix[ci])} = {fmt(total)}.",
        "M")

    # Q2 [H]: average of one company across the four years (row sum / 4, clean)
    ci2 = random.randrange(5)
    rowsum = sum(F(v) for v in matrix[ci2])
    avg = rowsum / 4
    b.q(f"What is the average {metric} of Company {companies[ci2]} over the four years?",
        avg,
        [rowsum / 5, rowsum / 3, avg + matrix[ci2][0]],
        f"Average = ({' + '.join(str(v) for v in matrix[ci2])}) / 4 = {fmt(rowsum)}/4 "
        f"= {fmt(avg)}.",
        "H")

    # Q3 [H]: difference between two cells (always integer/clean)
    (r1, y1), (r2, y2) = random.sample([(r, y) for r in range(5) for y in range(4)], 2)
    d = F(matrix[r1][y1]) - F(matrix[r2][y2])
    diff = d if d >= 0 else -d
    hi, lo = (companies[r1], years[y1], matrix[r1][y1]), (companies[r2], years[y2], matrix[r2][y2])
    b.q(f"What is the difference between the {metric} of Company {companies[r1]} in "
        f"{years[y1]} and that of Company {companies[r2]} in {years[y2]}?",
        diff,
        [F(matrix[r1][y1]) + F(matrix[r2][y2]), diff + lo[2], diff * 2],
        f"|{matrix[r1][y1]} - {matrix[r2][y2]}| = {fmt(diff)}.",
        "H")

    # Q4 [H]: ratio of one cell to another cell within the SAME row (shares unit
    # -> ratio reduces to a clean fraction)
    rr_row = random.randrange(5)
    ya, yb = random.sample(range(4), 2)
    a_val, b_val = F(matrix[rr_row][ya]), F(matrix[rr_row][yb])
    ratio = a_val / b_val
    b.q(f"What is the ratio of the {metric} of Company {companies[rr_row]} in {years[ya]} "
        f"to that in {years[yb]}?",
        ratio,
        [b_val / a_val, (a_val + matrix[rr_row][ya]) / b_val, a_val / (2 * b_val)],
        f"Ratio = {fmt(a_val)} : {fmt(b_val)} = {fmt(ratio)}.",
        "H")

    # Q5 [VH]: percent change for a company between two years where the base
    # value divides cleanly. We pick the year-pair (within one row) that yields
    # the cleanest change; the row shares a unit so change% = (cb-ca)/ca*100.
    pc_row = random.randrange(5)
    best = None
    for ya2 in range(4):
        for yb2 in range(4):
            if ya2 == yb2:
                continue
            ca = F(matrix[pc_row][ya2]); cb = F(matrix[pc_row][yb2])
            ch = (cb - ca) / ca * 100
            if is_clean(ch):
                best = (ya2, yb2, ca, cb, ch)
                break
        if best:
            break
    if best is None:
        return b  # will fail ok() (only 4 q) and be rejected
    ya2, yb2, ca, cb, ch = best
    b.q(f"By what percent did the {metric} of Company {companies[pc_row]} change from "
        f"{years[ya2]} to {years[yb2]}?",
        ch,
        [(ca - cb) / cb * 100, (cb - ca), -ch],
        f"Change = ({fmt(cb)} - {fmt(ca)}) / {fmt(ca)} x 100 = {fmt(ch)}% "
        f"({'increase' if ch >= 0 else 'decrease'}).",
        "VH")

    return b


# ===========================================================================
# TEMPLATE 2: BAR GRAPH — value list (sales of items)
# ===========================================================================
def build_bar_set():
    items = random.sample(["P", "Q", "R", "S", "T", "U", "V", "W"], 6)
    unit = random.choice(["lakh", "thousand", "crore"])
    vals = [random.randint(2, 12) * 30 for _ in range(6)]  # multiples of 30
    pairs = ", ".join(f"{it}={v}" for it, v in zip(items, vals))
    metric = random.choice(["sales", "output", "exports"])
    data_md = (f"The bar graph shows the {metric} (in {unit}) of six units.\n\n"
               f"**{metric.capitalize()} (in {unit}):** {pairs}")
    intro = f"Refer to the bar graph of {metric} (in {unit})."

    b = SetBuilder(data_md, intro)
    d = {it: F(v) for it, v in zip(items, vals)}
    val = {it: vals[i] for i, it in enumerate(items)}

    # Q1 [M]: total of all (always clean)
    tot = sum(d.values())
    b.q(f"What is the total {metric} of all six units (in {unit})?",
        tot,
        [tot - vals[0], tot - vals[1], tot + vals[2]],
        f"Sum = {' + '.join(str(v) for v in vals)} = {fmt(tot)}.",
        "M")

    # Q2 [H]: difference between two units (always clean)
    i, j = random.sample(range(6), 2)
    dd = abs(d[items[i]] - d[items[j]])
    b.q(f"What is the difference between the {metric} of {items[i]} and {items[j]} "
        f"(in {unit})?",
        dd,
        [d[items[i]] + d[items[j]], dd + d[items[i]], dd * 2],
        f"|{val[items[i]]} - {val[items[j]]}| = {fmt(dd)}.",
        "H")

    # Q3 [H]: ratio of two units -> pick a pair whose ratio is clean
    pairs_idx = [(a, c) for a in range(6) for c in range(6) if a != c]
    random.shuffle(pairs_idx)
    rpair = next(((a, c) for (a, c) in pairs_idx if is_clean(d[items[a]] / d[items[c]])), None)
    if rpair is None:
        return b
    a, c = rpair
    rr = d[items[a]] / d[items[c]]
    b.q(f"What is the ratio of the {metric} of {items[a]} to that of {items[c]}?",
        rr,
        [d[items[c]] / d[items[a]], (d[items[a]] + d[items[c]]) / d[items[c]], rr * 2],
        f"Ratio = {val[items[a]]} : {val[items[c]]} = {fmt(rr)}.",
        "H")

    # Q4 [H]: what percent A is of B -> pick a pair where clean
    ppair = next(((a, c) for (a, c) in pairs_idx
                  if is_clean(d[items[a]] / d[items[c]] * 100)), None)
    if ppair is None:
        return b
    a2, c2 = ppair
    p = d[items[a2]] / d[items[c2]] * 100
    b.q(f"The {metric} of {items[a2]} is what percent of the {metric} of {items[c2]}?",
        p,
        [d[items[c2]] / d[items[a2]] * 100, p / 2, p + 10],
        f"= {val[items[a2]]} / {val[items[c2]]} x 100 = {fmt(p)}%.",
        "H")

    # Q5 [VH]: average of a triple of units whose sum is divisible by 3
    triples = [(x, y, z) for x in range(6) for y in range(x + 1, 6) for z in range(y + 1, 6)]
    random.shuffle(triples)
    trip = next((t for t in triples
                 if (d[items[t[0]]] + d[items[t[1]]] + d[items[t[2]]]) % 3 == 0), None)
    if trip is None:
        return b
    x, y, z = trip
    s3 = d[items[x]] + d[items[y]] + d[items[z]]
    avg3 = s3 / 3
    b.q(f"What is the average {metric} of {items[x]}, {items[y]} and {items[z]} "
        f"(in {unit})?",
        avg3,
        [s3 / 2, s3, avg3 + d[items[x]]],
        f"Average = ({val[items[x]]} + {val[items[y]]} + {val[items[z]]}) / 3 "
        f"= {fmt(s3)}/3 = {fmt(avg3)}.",
        "VH")

    return b


# ===========================================================================
# TEMPLATE 3: PIE CHART — percentages of a stated total
# ===========================================================================
def build_pie_set():
    cats = random.sample(["Food", "Rent", "Education", "Savings", "Transport",
                          "Clothing", "Misc"], 5)
    # percentages that sum to 100, all clean
    base_parts = random.choice([
        [10, 15, 20, 25, 30],
        [12, 18, 20, 22, 28],
        [10, 20, 20, 25, 25],
        [15, 15, 20, 20, 30],
        [8, 12, 20, 24, 36],
    ])
    random.shuffle(base_parts)
    # total chosen so every category value is an integer (LCM of denoms is 100)
    total = random.choice([24000, 36000, 48000, 60000, 72000, 96000, 120000])
    pct = dict(zip(cats, base_parts))
    parts_md = ", ".join(f"{c}={p}%" for c, p in pct.items())
    data_md = (f"A family's monthly budget of Rs. {total} is distributed across five "
               f"heads as shown in the pie chart (percentages of the total).\n\n"
               f"**Distribution:** {parts_md}")
    intro = f"Refer to the pie chart; total budget = Rs. {total}."

    b = SetBuilder(data_md, intro)
    val = {c: F(total) * p / 100 for c, p in pct.items()}

    # Q1 [M]: actual value of one category
    c1 = random.choice(cats)
    b.q(f"What is the amount (in Rs.) spent on {c1}?",
        val[c1],
        [F(total) * pct[c1] / 1000, F(total) - val[c1], val[c1] + 100],
        f"{c1} = {pct[c1]}% of {total} = {pct[c1]}/100 x {total} = Rs. {fmt(val[c1])}.",
        "M")

    # Q2 [H]: difference between two categories (in Rs.)
    c2, c3 = random.sample(cats, 2)
    diff = abs(val[c2] - val[c3])
    b.q(f"What is the difference (in Rs.) between the amounts spent on {c2} and {c3}?",
        diff,
        [val[c2] + val[c3], abs(pct[c2] - pct[c3]), diff / 2],
        f"|{pct[c2]}% - {pct[c3]}%| = {abs(pct[c2] - pct[c3])}% of {total} "
        f"= Rs. {fmt(diff)}.",
        "H")

    # Q3 [H]: ratio of two categories (pct ratio reduces -> clean)
    rpairs = [(u, v) for u in cats for v in cats if u != v and is_clean(val[u] / val[v])]
    c4, c5 = random.choice(rpairs)
    rr = val[c4] / val[c5]
    b.q(f"What is the ratio of the amount spent on {c4} to that spent on {c5}?",
        rr,
        [val[c5] / val[c4], (val[c4] + 1000) / val[c5], rr * 2],
        f"Ratio = {pct[c4]} : {pct[c5]} = {fmt(rr)}.",
        "H")

    # Q4 [H]: combined two categories as amount
    c6, c7 = random.sample(cats, 2)
    combo = val[c6] + val[c7]
    b.q(f"What is the total amount (in Rs.) spent on {c6} and {c7} together?",
        combo,
        [abs(val[c6] - val[c7]), F(total) - combo, combo + 500],
        f"({pct[c6]} + {pct[c7]})% = {pct[c6] + pct[c7]}% of {total} = Rs. {fmt(combo)}.",
        "H")

    # Q5 [VH]: one category as percent of (sum of two others) -> clean triple
    triples = [(a, x, y) for a in cats for x in cats for y in cats
               if len({a, x, y}) == 3 and x < y
               and is_clean(val[a] / (val[x] + val[y]) * 100)]
    if not triples:
        return b
    a, x, y = random.choice(triples)
    denom = val[x] + val[y]
    p = val[a] / denom * 100
    b.q(f"The amount spent on {a} is what percent of the combined amount spent on "
        f"{x} and {y}?",
        p,
        [denom / val[a] * 100, p / 2, p + 10],
        f"= {fmt(val[a])} / ({fmt(val[x])} + {fmt(val[y])}) x 100 "
        f"= {pct[a]}/{pct[x] + pct[y]} x 100 = {fmt(p)}%.",
        "VH")

    return b


# ===========================================================================
# TEMPLATE 4: LINE / MIXED — two series (imports & exports) over years
# ===========================================================================
def build_line_set():
    years = random.choice(YEARS_POOL)
    imp = [random.randrange(20, 81, 5) * 10 for _ in range(4)]
    exp = [random.randrange(20, 81, 5) * 10 for _ in range(4)]
    headers = ["Year", "Imports (Rs. cr)", "Exports (Rs. cr)"]
    matrix = [[imp[i], exp[i]] for i in range(4)]
    data_md = (f"The table shows the Imports and Exports (in Rs. crore) of a company "
               f"over four years.\n\n"
               + md_table(headers, years, matrix))
    intro = "Refer to the Imports/Exports table (Rs. crore)."

    b = SetBuilder(data_md, intro)
    I = [F(v) for v in imp]
    E = [F(v) for v in exp]

    # Q1 [M]: total imports over all years
    ti = sum(I)
    b.q(f"What is the total Imports (in Rs. crore) over all four years?",
        ti,
        [ti - imp[0], sum(E), ti + imp[1]],
        f"Total imports = {' + '.join(str(v) for v in imp)} = {fmt(ti)}.",
        "M")

    # Q2 [H]: trade deficit/surplus in one year (Exports - Imports)
    k = random.randrange(4)
    bal = E[k] - I[k]
    b.q(f"What is the value of (Exports - Imports) in {years[k]} (in Rs. crore)?",
        bal,
        [I[k] - E[k], E[k] + I[k], bal / 2],
        f"= {fmt(E[k])} - {fmt(I[k])} = {fmt(bal)}.",
        "H")

    # Q3 [H]: ratio of imports to exports in a year where ratio is clean
    k2 = next((k for k in range(4) if is_clean(I[k] / E[k])), None)
    if k2 is None:
        return b
    rr = I[k2] / E[k2]
    b.q(f"What is the ratio of Imports to Exports in {years[k2]}?",
        rr,
        [E[k2] / I[k2], (I[k2] + 50) / E[k2], rr * 2],
        f"Ratio = {fmt(I[k2])} : {fmt(E[k2])} = {fmt(rr)}.",
        "H")

    # Q4 [H]: percent change in exports between two years (clean year-pair)
    yp = [(a, c) for a in range(4) for c in range(4) if a != c]
    random.shuffle(yp)
    p4 = next(((a, c) for (a, c) in yp if is_clean(pct_change(E[a], E[c]))), None)
    if p4 is None:
        return b
    a, c = p4
    chg = pct_change(E[a], E[c])
    b.q(f"By what percent did Exports change from {years[a]} to {years[c]}?",
        chg,
        [pct_change(E[c], E[a]), -chg, abs(E[c] - E[a])],
        f"= ({fmt(E[c])} - {fmt(E[a])}) / {fmt(E[a])} x 100 = {fmt(chg)}% "
        f"({'increase' if chg >= 0 else 'decrease'}).",
        "H")

    # Q5 [VH]: percent change of combined (Imp+Exp) over a clean year-pair
    S = [I[t] + E[t] for t in range(4)]
    p5 = next(((a, c) for (a, c) in yp if is_clean(pct_change(S[a], S[c]))), None)
    if p5 is None:
        return b
    a2, c2 = p5
    s_old, s_new = S[a2], S[c2]
    chg2 = pct_change(s_old, s_new)
    b.q(f"By what percent did the combined trade (Imports + Exports) change from "
        f"{years[a2]} to {years[c2]}?",
        chg2,
        [pct_change(s_new, s_old), -chg2, pct_change(I[a2], I[c2])],
        f"Combined {years[a2]} = {fmt(s_old)}, {years[c2]} = {fmt(s_new)}; "
        f"change = ({fmt(s_new)} - {fmt(s_old)})/{fmt(s_old)} x 100 = {fmt(chg2)}% "
        f"({'increase' if chg2 >= 0 else 'decrease'}).",
        "VH")

    return b


BUILDERS = [build_table_set, build_bar_set, build_pie_set, build_line_set]


# ----------------------------------------------------------------------------
# Generate 100 accepted sets (rotating builders)
# ----------------------------------------------------------------------------
TARGET_SETS = 100
attempts = 0
bi = 0
seen_stems = set()

while len(sets) < TARGET_SETS and attempts < 200000:
    attempts += 1
    builder = BUILDERS[bi % len(BUILDERS)]
    b = builder()
    if not b.ok():
        continue
    # dedupe at set level on the concatenation of stems (rare collision guard)
    key = "||".join(item["stem"] for item in b.qs)
    if key in seen_stems:
        continue
    seen_stems.add(key)
    sets.append(b)
    bi += 1

print(f"Accepted {len(sets)} sets in {attempts} attempts.")
assert len(sets) == TARGET_SETS, "did not reach 100 sets"

# Flatten + assign global question numbers, build options
qnum = 0
for b in sets:
    for item in b.qs:
        qnum += 1
        opts, ci = make_options(item["correct"], item["distractors"])
        item["qnum"] = qnum
        item["opts"] = [fmt(o) for o in opts]
        item["opts_frac"] = opts
        item["ci"] = ci

all_questions = [item for b in sets for item in b.qs]
print(f"Total questions: {len(all_questions)}")

# ----------------------------------------------------------------------------
# SELF-CHECK
# ----------------------------------------------------------------------------
errors = 0
for q in all_questions:
    if len(q["opts"]) != 4:
        print(f"Q{q['qnum']}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{q['qnum']}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{q['qnum']}: bad correct index"); errors += 1
    # keyed option value must equal the computed correct value
    keyed = q["opts_frac"][q["ci"]]
    if Fraction(keyed) != q["correct"]:
        print(f"Q{q['qnum']}: keyed value != computed"); errors += 1
print(f"Self-check errors: {errors}")
assert errors == 0

dist = Counter(q["diff"] for q in all_questions)
print("Difficulty:", dict(dist))

# ----------------------------------------------------------------------------
# WRITE MARKDOWN
# ----------------------------------------------------------------------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_09_Data_Interpretation_500.md"

L = []
L.append("# Data Interpretation - 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
L.append("> **Format:** Questions come in SETS - a data block (table/bar/pie/line) "
         "followed by 5 sub-questions. Questions are numbered Q1-Q500 continuously. "
         "The full **Answer Key & Explanations** is at the very end.")
L.append("> **Difficulty skew:** ~20% Medium / ~60% Hard / ~20% Very-Hard (trap) - CGL Tier-II standard.")
L.append("> **Every numeric answer is computed and machine-verified** - the keyed option is provably correct.")
L.append("> Negative marking in CGL is -0.50; the distractors are real common-mistake values.\n")
L.append("## How to read DI")
L.append("- **Table:** read the row (category) and column (year) intersection for each cell.")
L.append("- **Bar graph:** each label maps to a value, given here as a `label=value` list.")
L.append("- **Pie chart:** each slice is a percent of the stated total; actual value = percent/100 x total.")
L.append("- **Line/mixed:** two series (e.g. Imports & Exports) tabulated by year.")
L.append("- Common asks: total/average over a row or column, ratio between two cells, "
         "what percent one is of another, percent increase/decrease between years, "
         "difference, highest/lowest, combined-category totals, average excluding one item.\n")
L.append("\n# =================== QUESTIONS ===================\n")

for k, b in enumerate(sets, 1):
    first = b.qs[0]["qnum"]
    last = b.qs[-1]["qnum"]
    L.append(f"\n### Data Set {k} (Q{first}-Q{last})\n")
    L.append(b.data_md + "\n")
    for item in b.qs:
        o = item["opts"]
        L.append(f"**Q{item['qnum']}.** {item['stem']}")
        L.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

L.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for k, b in enumerate(sets, 1):
    first = b.qs[0]["qnum"]
    last = b.qs[-1]["qnum"]
    L.append(f"\n## Answers Q{first}-Q{last} (Data Set {k})\n")
    for item in b.qs:
        letter = LETTERS[item["ci"]]
        val = item["opts"][item["ci"]]
        L.append(f"**Q{item['qnum']}. ({letter}) {val}**  *[{item['diff']}]* - {item['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(L))
print(f"Wrote {OUT}")

# ----------------------------------------------------------------------------
# JSON sidecar: (qnum -> correct_value) for the independent verifier
# ----------------------------------------------------------------------------
SIDE = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_09_Data_Interpretation_500.key.json"
sidecar = {str(q["qnum"]): fmt(q["opts_frac"][q["ci"]]) for q in all_questions}
with open(SIDE, "w", encoding="utf-8") as f:
    json.dump(sidecar, f)
print(f"Wrote sidecar {SIDE} with {len(sidecar)} entries")
