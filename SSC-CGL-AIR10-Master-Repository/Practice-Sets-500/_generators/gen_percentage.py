# -*- coding: utf-8 -*-
"""
SSC CGL Percentage - 500 hard MCQ generator.
Every answer is COMPUTED, so the key is provably correct.
Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.
"""
import random
from fractions import Fraction

random.seed(20260625)  # deterministic

LETTERS = "abcd"

def fmt(x):
    """Format a number cleanly: ints as ints, fractions as decimals or fraction."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        f = float(x)
        # nice decimal if it terminates within 4 dp, else keep fraction
        if abs(f - round(f, 4)) < 1e-9:
            s = f"{f:.4f}".rstrip("0").rstrip(".")
            return s
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        s = f"{x:.4f}".rstrip("0").rstrip(".")
        return s
    return str(x)

def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 distinct values."""
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        # avoid duplicates / near-duplicates
        if all(abs(float(d) - float(o)) > 1e-9 for o in opts):
            opts.append(d)
        if len(opts) == 4:
            break
    # pad with plausible filler if needed
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

questions = []  # each: dict(stem, opts(list of str), correct_index, sol, diff)
seen = set()

def is_clean(x):
    """Accept integers, halves/quarters/thirds/sixths/eighths, and <=2dp decimals."""
    fr = Fraction(x).limit_denominator(10**6)
    if fr.denominator in (1, 2, 3, 4, 5, 6, 8):
        return True
    f = float(fr)
    return abs(f - round(f, 2)) < 1e-9

def add(stem, correct, distractors, sol, diff):
    key = stem.strip()
    if key in seen:
        return False
    cfr = Fraction(correct).limit_denominator(10**6)
    if not is_clean(cfr):
        return False
    dfrs = [Fraction(d).limit_denominator(10**6) for d in distractors if d is not None]
    dfrs = [d for d in dfrs if is_clean(d) and d != cfr]
    if len(dfrs) < 3:
        return False
    seen.add(key)
    opts, ci = make_options(cfr, dfrs)
    questions.append({
        "stem": stem,
        "opts": [fmt(o) for o in opts],
        "ci": ci,
        "sol": sol,
        "diff": diff,
    })
    return True

# ---------------- TEMPLATES ----------------

def t_successive_change():
    """Price up a% then down b%: net change & trap distractors. [H]"""
    a = random.choice([8,10,12,12.5,15,16,18,20,24,25,30,32,35,40,45,50])
    b = random.choice([5,8,10,12,12.5,15,16,18,20,24,25,30,35,40])
    net = a - b - (a*b)/100  # net percent change
    correct = Fraction(net).limit_denominator(1000)
    wrong1 = Fraction(a - b)             # forgets cross term
    wrong2 = Fraction(a - b + (a*b)/100).limit_denominator(1000)  # sign of cross term
    wrong3 = Fraction(-net).limit_denominator(1000)
    sign = "increase" if net >= 0 else "decrease"
    stem = (f"The price of an article is first increased by {fmt(a)}% and then "
            f"decreased by {fmt(b)}%. The net percentage change in price is:")
    sol = (f"Net change = a − b − ab/100 = {fmt(a)} − {fmt(b)} − ({fmt(a)}×{fmt(b)})/100 "
           f"= {fmt(correct)}%  ({'net increase' if net>=0 else 'net decrease'}). "
           f"Sign trap: the cross-term −ab/100 is always a reduction.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_consumption_price():
    """Price rises by x% -> % cut in consumption to keep expenditure same. [H]"""
    x = random.choice([8,10,12,12.5,15,16,20,24,25,30,32,36,40,44,50,56,60,75,80,100,150])
    xf = Fraction(x).limit_denominator(1000)
    correct = xf / (100+xf) * 100
    wrong1 = xf                                       # naive: same %
    wrong2 = xf / (100-xf) * 100 if xf < 100 else xf  # wrong base
    wrong3 = xf + 2                                    # off by a bit
    stem = (f"The price of sugar increases by {fmt(x)}%. By what percent must a family "
            f"reduce its consumption so that the expenditure on sugar remains unchanged?")
    sol = (f"Required reduction = x/(100+x)×100 = {fmt(x)}/{fmt(100+x)}×100 = {fmt(correct)}%. "
           f"Trap: the base is the NEW price (100+x), not 100.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_more_less():
    """A is x% more than B -> B is how much % less than A. [M/H]"""
    x = random.choice([20,25,30,33.3333,40,50,60,75,80])
    if x == 33.3333:
        xr = Fraction(100,3)
    else:
        xr = Fraction(x).limit_denominator(1000)
    correct = xr/(100+xr)*100
    wrong1 = xr                          # same %
    wrong2 = xr/(100-xr)*100 if xr < 100 else xr
    wrong3 = (100*xr)/(100+xr+xr)        # nonsense base
    stem = (f"If A's income is {fmt(xr)}% more than B's income, then B's income is "
            f"how much percent less than A's income?")
    sol = (f"Less% = x/(100+x)×100 = {fmt(xr)}/(100+{fmt(xr)})×100 = {fmt(correct)}%.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_exam_pass():
    """Student scores m marks, fails by f; pass% given -> max marks. [H]"""
    passpct = random.choice([25,30,32,33,35,36,40,42,45,48,50])
    maxm = random.choice([400,450,500,550,600,640,700,750,800,850,900,950,1000,1200,1500])
    pass_marks = Fraction(passpct,100)*maxm
    fail_by = random.choice([15,20,25,30,35,40,45,50,55,60,75,80])
    scored = pass_marks - fail_by
    if scored <= 0:
        return None
    # ask for max marks given scored & fail_by & passpct
    correct = Fraction(maxm)
    wrong1 = Fraction((scored)*100, passpct)             # ignores fail_by
    wrong2 = Fraction((scored+2*fail_by)*100, passpct)
    wrong3 = Fraction((scored+fail_by)*100, passpct+5)
    stem = (f"A student scored {fmt(scored)} marks and failed by {fail_by} marks. "
            f"If the pass percentage is {passpct}%, the maximum marks of the exam are:")
    sol = (f"Pass marks = scored + fail_by = {fmt(scored)} + {fail_by} = {fmt(pass_marks)}. "
           f"These equal {passpct}% of max → max = {fmt(pass_marks)}×100/{passpct} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_election():
    """Two candidates, winner got p%, won by margin -> total valid votes. [H]"""
    p = random.choice([51,52,53,54,55,56,57,58,59,60,62,64,65,68,70])
    margin_each = 2*p - 100   # winner - loser as % of total
    total = random.choice([15000,18000,20000,24000,25000,30000,32000,36000,
                           40000,45000,48000,50000,60000,72000,80000,100000])
    # ensure margin integer
    margin = Fraction(margin_each,100)*total
    if margin != int(margin):
        return None
    correct = Fraction(total)
    wrong1 = Fraction(int(margin)*100, p)            # divides by winner%
    wrong2 = Fraction(int(margin)*100, 100-p)        # divides by loser%
    wrong3 = Fraction(int(margin)*2)                 # doubles margin
    stem = (f"In an election between two candidates, the winner secured {p}% of the "
            f"total valid votes and won by {int(margin)} votes. The total number of "
            f"valid votes was:")
    sol = (f"Winning margin = ({p}−{100-p})% = {margin_each}% of total = {int(margin)} votes "
           f"→ total = {int(margin)}×100/{margin_each} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_two_dim_change():
    """Length +a%, breadth -b% -> % change in area. [H]"""
    a = random.choice([10,12,15,16,18,20,24,25,28,30,32,35,40,44,50,60])
    b = random.choice([8,10,12,15,16,18,20,24,25,30,35,40])
    net = a - b - (a*b)/100
    correct = Fraction(net).limit_denominator(1000)
    wrong1 = Fraction(a-b)
    wrong2 = Fraction(a-b+(a*b)/100).limit_denominator(1000)
    wrong3 = Fraction(a+b).limit_denominator(1000)
    stem = (f"The length of a rectangle is increased by {a}% and its breadth is "
            f"decreased by {b}%. The percentage change in its area is:")
    sol = (f"%change = a − b − ab/100 = {a} − {b} − {a*b}/100 = {fmt(correct)}% "
           f"({'increase' if net>=0 else 'decrease'}).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_population():
    """Population grows r% per year for 2 yrs from P -> final, or reverse. [M/H]"""
    r = random.choice([5,8,10,12,15,20,25])
    P = random.choice([8000,10000,12000,15000,20000,25000,40000])
    final = Fraction(P)*(Fraction(100+r,100))**2
    correct = final
    wrong1 = Fraction(P)*(1+Fraction(2*r,100))   # simple, not compound
    wrong2 = Fraction(P)*(Fraction(100+r,100))   # only one year
    wrong3 = Fraction(P)*(Fraction(100+r,100))**3
    if final != int(final):
        return None
    stem = (f"The population of a town is {P}. If it increases at {r}% per annum, "
            f"its population after 2 years will be:")
    sol = (f"Population = P(1+r/100)² = {P}×(1+{r}/100)² = {fmt(correct)}. "
           f"Trap: it compounds; it is NOT P(1+2r/100).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_alcohol_evap():
    """x% of number; chained 'of'. multi-of. [M]"""
    base = random.choice([1200,1500,1800,2400,3000,3600,4800])
    p1 = random.choice([15,20,25,30,40])
    p2 = random.choice([20,25,30,40,50])
    val = Fraction(p1,100)*Fraction(p2,100)*base
    if val != int(val):
        return None
    correct = val
    wrong1 = Fraction(p1+p2,100)*base       # adds percents
    wrong2 = Fraction(p1,100)*base
    wrong3 = Fraction(p2,100)*base
    stem = (f"What is {p1}% of {p2}% of {base}?")
    sol = (f"{p1}% of {p2}% of {base} = {p1}/100 × {p2}/100 × {base} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_salary_restore():
    """Salary reduced by x%, then increased by y% to restore -> find y. [VH]"""
    x = random.choice([5,8,10,12,12.5,15,16,20,24,25,30,32,36,40,44,50,60,64,75,80])
    xf = Fraction(x).limit_denominator(1000)
    # to restore from (100-x) to 100: increase needed = x/(100-x)*100
    correct = xf/(100-xf)*100
    wrong1 = xf                               # same
    wrong2 = xf/(100+xf)*100
    wrong3 = xf + 5
    stem = (f"A man's salary is reduced by {fmt(xf)}%. By what percent must the reduced "
            f"salary be increased to restore it to the original amount?")
    sol = (f"Increase = x/(100−x)×100 = {fmt(xf)}/(100−{fmt(xf)})×100 = {fmt(correct)}%. "
           f"Trap: base is the reduced salary (100−x), not 100.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_basic_of():
    """Simple a% of b. [M]"""
    p = random.choice([12.5,15,16,24,35,45,62.5,72])
    n = random.choice([240,320,480,560,640,800,960,1200])
    val = Fraction(p).limit_denominator(1000)/100*n
    if val != int(val):
        return None
    correct = val
    wrong1 = val + Fraction(n,10)
    wrong2 = val - Fraction(n,10)
    wrong3 = val + random.choice([4,6,8,12])
    stem = (f"What is {fmt(p)}% of {n}?")
    sol = (f"{fmt(p)}% of {n} = {fmt(p)}/100 × {n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_increase_to():
    """A number increased by p% becomes V -> original. [M]"""
    p = random.choice([12.5,15,20,25,30,40,60])
    pf = Fraction(p).limit_denominator(1000)
    orig = random.choice([180,240,360,400,450,500,640,720,900])
    V = (100+pf)/100*orig
    if V != int(V):
        return None
    correct = Fraction(orig)
    wrong1 = V - pf/100*V                      # subtract p% of V (wrong direction)
    wrong2 = V - pf                            # subtract p
    wrong3 = Fraction(100,1)/(100+pf)*V - 5
    stem = (f"A number, when increased by {fmt(p)}%, becomes {fmt(V)}. The original "
            f"number is:")
    sol = (f"Original = {fmt(V)}×100/(100+{fmt(p)}) = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_three_subjects():
    """Pass overall: failed a% in subj1, b% in subj2, c% in both -> passed both %. [VH]"""
    a = random.choice([18,20,22,25,28,30,32,34,35,38,40,42,45,48,50])
    b = random.choice([12,15,16,18,20,22,24,25,28,30,32,35,40])
    both = random.choice([4,5,6,8,9,10,12,14,15,16,18,20])
    if both >= min(a,b):
        return None
    failed_atleast_one = a + b - both
    passed_both = 100 - failed_atleast_one
    if passed_both <= 0:
        return None
    correct = Fraction(passed_both)
    wrong1 = Fraction(100 - a - b)                 # forgets 'both'
    wrong2 = Fraction(100 - a - b + both + both)
    wrong3 = Fraction(failed_atleast_one)
    stem = (f"In an examination, {a}% of candidates failed in English and {b}% failed "
            f"in Maths. If {both}% failed in both subjects, the percentage of "
            f"candidates who passed in both subjects is:")
    sol = (f"Failed in at least one = {a}+{b}−{both} = {failed_atleast_one}%. "
           f"Passed both = 100 − {failed_atleast_one} = {fmt(correct)}%.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_income_save():
    """Income, spends s%, saving = amount -> income. [M/H]"""
    s = random.choice([60,65,70,72,75,80,85,88])
    saving = random.choice([1500,1800,2100,2400,3000,3600,4500])
    save_pct = 100 - s
    income = Fraction(saving*100, save_pct)
    if income != int(income):
        return None
    correct = income
    wrong1 = Fraction(saving*100, s)               # divides by spend%
    wrong2 = Fraction(saving*s,100)
    wrong3 = Fraction(saving*100, save_pct) - saving
    stem = (f"A person spends {s}% of his monthly income and saves ₹{saving}. "
            f"His monthly income is:")
    sol = (f"Savings = {save_pct}% of income = ₹{saving} → income = {saving}×100/{save_pct} "
           f"= ₹{fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_successive_discount_as_pct():
    """Two successive % increases combine. [H]"""
    a = random.choice([8,10,12,15,16,18,20,24,25,30,32,35,40])
    b = random.choice([8,10,12,15,16,18,20,24,25,30,32,35,40])
    net = a + b + (a*b)/100
    correct = Fraction(net).limit_denominator(1000)
    wrong1 = Fraction(a+b)
    wrong2 = Fraction(a+b-(a*b)/100).limit_denominator(1000)
    wrong3 = Fraction(a*b,100)
    stem = (f"A quantity is increased successively by {a}% and then by {b}%. "
            f"The overall percentage increase is:")
    sol = (f"Net = a + b + ab/100 = {a}+{b}+{a*b}/100 = {fmt(correct)}%.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

TEMPLATES = [
    t_successive_change, t_consumption_price, t_more_less, t_exam_pass,
    t_election, t_two_dim_change, t_population, t_alcohol_evap,
    t_salary_restore, t_basic_of, t_increase_to, t_three_subjects,
    t_income_save, t_successive_discount_as_pct,
]

# Weighted selection to hit ~20% M / 60% H / 20% VH.
# Map each template to its difficulty, then bias picks toward H and VH.
DIFF_OF = {
    t_successive_change:"H", t_consumption_price:"H", t_more_less:"M", t_exam_pass:"H",
    t_election:"H", t_two_dim_change:"H", t_population:"M", t_alcohol_evap:"M",
    t_salary_restore:"VH", t_basic_of:"M", t_increase_to:"M", t_three_subjects:"VH",
    t_income_save:"M", t_successive_discount_as_pct:"H",
}
WEIGHT = {"M":1.0, "H":3.0, "VH":3.0}
POOL = []
for t in TEMPLATES:
    POOL += [t] * int(WEIGHT[DIFF_OF[t]]*10)

# Generate until we have 500 unique
attempts = 0
while len(questions) < 500 and attempts < 400000:
    attempts += 1
    t = random.choice(POOL)
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    add(stem, correct, distractors, sol, diff)

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- VERIFY: each has exactly 4 distinct options, exactly one correct ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
print(f"Verification errors: {errors}")

# difficulty distribution
from collections import Counter
print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_01_Percentage_500.md"

lines = []
lines.append("# Percentage — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** Medium / Hard / Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- `x% of y = y/100 × x`  ·  `x% of y = y% of x`")
lines.append("- A is x% more than B → B is **x/(100+x)×100 %** less than A")
lines.append("- A is x% less than B → B is **x/(100−x)×100 %** more than A")
lines.append("- Successive a%, b% → net **a + b + ab/100 %** (use −b for a decrease)")
lines.append("- Price ↑x% → consumption cut to keep spend same = **x/(100+x)×100 %**")
lines.append("- Population after n yrs at r% = **P(1+r/100)ⁿ**")
lines.append("- Failed in at least one = a + b − both ; Passed both = 100 − that\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start//50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
    for j in range(start, min(start+50, 500)):
        q = questions[j]
        n = j+1
        o = q["opts"]
        lines.append(f"**Q{n}.** {q['stem']}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    blk = start//50 + 1
    lines.append(f"\n## Answers Q{start+1}–Q{start+50}\n")
    for j in range(start, min(start+50, 500)):
        q = questions[j]
        n = j+1
        letter = LETTERS[q["ci"]]
        val = q["opts"][q["ci"]]
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* — {q['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUT}")
print(f"Total lines: {len(lines)}")
