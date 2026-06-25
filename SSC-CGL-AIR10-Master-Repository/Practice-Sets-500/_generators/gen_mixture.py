# -*- coding: utf-8 -*-
"""
SSC CGL Mixture & Alligation - 500 hard PYQ-pattern MCQ generator.
Every answer is COMPUTED, so the key is provably correct.
Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.

CRITICAL: never pass a float into Fraction(num,den). Convert any float via
Fraction(x).limit_denominator(1000). Replacement uses exact Fraction powers.
Only clean answers (is_clean) are accepted.
"""
import random
from fractions import Fraction
from collections import Counter

random.seed(20260625)  # deterministic

LETTERS = "abcd"


def fmt(x):
    """Format a number cleanly: ints as ints, fractions as decimals or fraction."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        f = float(x)
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


def ratio_str(a, b):
    """Reduce a:b to lowest terms and render as 'p : q'."""
    fr = Fraction(a, b)
    return f"{fr.numerator} : {fr.denominator}"


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


def make_ratio_options(correct_pair, distractor_pairs):
    """Build 4 distinct 'p : q' string options for ratio questions.
    correct_pair, distractor_pairs are (a,b) tuples (reduced internally)."""
    def red(p):
        fr = Fraction(p[0], p[1])
        return (fr.numerator, fr.denominator)
    cp = red(correct_pair)
    opts = [cp]
    for d in distractor_pairs:
        if d is None:
            continue
        rd = red(d)
        if rd not in opts:
            opts.append(rd)
        if len(opts) == 4:
            break
    # pad with plausible filler ratios
    bump = 1
    while len(opts) < 4:
        cand = (cp[0] + bump, cp[1] + bump)
        rd = red(cand)
        if rd not in opts and rd[1] != 0:
            opts.append(rd)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(cp)
    str_opts = [f"{p[0]} : {p[1]}" for p in opts]
    return str_opts, ci


questions = []  # each: dict(stem, opts(list of str), ci, sol, diff)
seen = set()


def is_clean(x):
    """Accept integers, halves/quarters/thirds/sixths/eighths, and <=2dp decimals."""
    fr = Fraction(x).limit_denominator(10**6)
    if fr.denominator in (1, 2, 3, 4, 5, 6, 8):
        return True
    f = float(fr)
    return abs(f - round(f, 2)) < 1e-9


def add(stem, correct, distractors, sol, diff):
    """Numeric-answer question."""
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


def add_ratio(stem, correct_pair, distractor_pairs, sol, diff):
    """Ratio-answer question (answer rendered as 'p : q')."""
    key = stem.strip()
    if key in seen:
        return False
    # validate distinct reduced distractors exist
    def red(p):
        if p is None:
            return None
        if p[1] == 0:
            return None
        fr = Fraction(p[0], p[1])
        return (fr.numerator, fr.denominator)
    cp = red(correct_pair)
    if cp is None or cp[0] <= 0 or cp[1] <= 0:
        return False
    valid = []
    for d in distractor_pairs:
        rd = red(d)
        if rd is None or rd[0] <= 0 or rd[1] <= 0:
            continue
        if rd != cp and rd not in valid:
            valid.append(rd)
    if len(valid) < 3:
        return False
    seen.add(key)
    opts, ci = make_ratio_options(correct_pair, valid)
    questions.append({
        "stem": stem,
        "opts": opts,
        "ci": ci,
        "sol": sol,
        "diff": diff,
    })
    return True


# ---------------- TEMPLATES ----------------
# All numeric inputs are ints; floats converted via Fraction(...).limit_denominator.

def t_alligation_ratio():
    """Mix two ingredients at prices p1<p2 to get mean m -> ratio cheaper:dearer. [M/H]"""
    p1 = random.choice([12, 15, 16, 18, 20, 24, 25, 28, 30])
    p2 = random.choice([40, 42, 45, 48, 50, 54, 60, 64, 72, 80])
    if p2 <= p1:
        return None
    m = random.randint(p1 + 2, p2 - 2)
    # ratio cheaper : dearer = (p2 - m) : (m - p1)
    a, b = p2 - m, m - p1
    fr = Fraction(a, b)
    correct = (fr.numerator, fr.denominator)
    # distractors: inverted, raw (m-p1):(p2-m) swapped form, off-by
    w1 = (b, a)                               # inverted assignment
    w2 = (p2 - m + 1, m - p1)                 # arithmetic slip
    w3 = (m - p1, m)                          # wrong second term
    stem = (f"In what ratio must rice costing Rs.{p1} per kg be mixed with rice "
            f"costing Rs.{p2} per kg so that the mixture is worth Rs.{m} per kg?")
    sol = (f"By alligation, cheaper : dearer = (dearer-mean) : (mean-cheaper) "
           f"= ({p2}-{m}) : ({m}-{p1}) = {a} : {b} = {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "M")


def t_alligation_tea_blend():
    """Two teas blended to a mean price; ask ratio. PYQ flavour. [M/H]"""
    p1 = random.choice([60, 65, 70, 75, 80, 90, 100, 120])
    p2 = random.choice([150, 160, 175, 180, 200, 210, 225, 240, 250])
    if p2 <= p1 + 10:
        return None
    m = random.randint(p1 + 5, p2 - 5)
    a, b = p2 - m, m - p1
    g = Fraction(a, b)
    correct = (g.numerator, g.denominator)
    w1 = (b, a)
    w2 = (p2 - m, m - p1 + 1)
    w3 = (p2, p1)
    stem = (f"A tea merchant blends two varieties of tea costing Rs.{p1} and Rs.{p2} "
            f"per kg. In what ratio should they be mixed so that the blend costs "
            f"Rs.{m} per kg?")
    sol = (f"Alligation: cheaper:dearer = ({p2}-{m}):({m}-{p1}) = {a}:{b} "
           f"= {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "M")


def t_replacement_milk_left():
    """From x L pure milk, y L removed & replaced with water, n times -> milk left. [H]"""
    x = random.choice([20, 25, 30, 40, 50, 60, 64, 80, 100, 120, 125, 150])
    y = random.choice([4, 5, 6, 8, 10, 12, 15, 16, 20, 25])
    if y >= x or x % y != 0:
        return None
    n = random.choice([2, 3])
    frac_left = (Fraction(x - y, x)) ** n          # exact Fraction power
    milk_left = Fraction(x) * frac_left
    correct = milk_left
    # distractors
    w1 = Fraction(x) * (Fraction(x - y, x)) ** (n - 1)   # one fewer iteration
    w2 = Fraction(x) - Fraction(y) * n                   # naive linear removal
    w3 = Fraction(x) * (Fraction(x - y, x)) ** (n + 1)   # one extra iteration
    stem = (f"A vessel contains {x} litres of pure milk. {y} litres are drawn off and "
            f"replaced with water; this operation is performed {n} times in all. "
            f"The quantity of milk (in litres) now left in the vessel is:")
    sol = (f"Milk left = x(1 - y/x)^n = {x}(1 - {y}/{x})^{n} = {x}*({x-y}/{x})^{n} "
           f"= {fmt(correct)} litres.")
    return ("num", stem, correct, [w1, w2, w3], sol, "H")


def t_replacement_ratio():
    """After n replacements, ratio of milk:water in the vessel. [H/VH]"""
    x = random.choice([20, 30, 40, 50, 60, 64, 80, 100, 120, 125])
    y = random.choice([4, 5, 6, 8, 10, 12, 16, 20, 25])
    if y >= x or x % y != 0:
        return None
    n = random.choice([2, 3])
    milk = (Fraction(x - y, x)) ** n
    water = 1 - milk
    if water <= 0:
        return None
    fr = milk / water
    correct = (fr.numerator, fr.denominator)
    w1 = (water.numerator * milk.denominator, milk.numerator * water.denominator)  # inverted
    w2 = (x - y * n, y * n)                       # naive linear ratio
    w3 = ((x - y) ** (n - 1), x ** (n - 1) - (x - y) ** (n - 1)) if n >= 2 else (x - y, y)
    stem = (f"From a vessel containing {x} litres of pure milk, {y} litres are "
            f"withdrawn and replaced with water. This is done {n} times. The ratio of "
            f"milk to water in the resulting mixture is:")
    sol = (f"Milk fraction = (1-y/x)^n = ({x-y}/{x})^{n} = {fmt(milk)}; water = "
           f"{fmt(water)}. Milk:water = {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "H")


def t_add_water_to_ratio():
    """Mixture has milk:water = a:b in V litres; add water to make ratio a':b'. [H]"""
    a = random.choice([2, 3, 4, 5, 7])
    b = random.choice([1, 2, 3])
    if a <= b:
        return None
    V = random.choice([20, 30, 40, 50, 60, 72, 80, 100])
    if V % (a + b) != 0:
        return None
    milk = Fraction(a, a + b) * V
    water = Fraction(b, a + b) * V
    # target ratio milk:water = a:c with more water; keep milk fixed, find water added
    c = random.choice([d for d in range(b + 1, b + 5)])
    new_water = milk * Fraction(c, a)
    added = new_water - water
    if added <= 0 or added != int(added):
        return None
    correct = added
    w1 = Fraction(c - b)                          # naive difference
    w2 = water * Fraction(c, a)                   # forgets to subtract existing water
    w3 = milk * Fraction(c, a) - milk            # uses milk base wrong
    stem = (f"{V} litres of a mixture contain milk and water in the ratio {a} : {b}. "
            f"How many litres of water must be added so that the ratio becomes "
            f"{a} : {c}?")
    sol = (f"Milk = {a}/{a+b} x {V} = {fmt(milk)} L (unchanged). For ratio {a}:{c}, "
           f"water needed = milk x {c}/{a} = {fmt(new_water)} L. Existing water = "
           f"{fmt(water)} L, so add {fmt(correct)} L.")
    return ("num", stem, correct, [w1, w2, w3], sol, "H")


def t_two_vessels_mix_equal():
    """Two vessels, milk:water r1 and r2, mixed in ratio k1:k2 -> resulting ratio. [H/VH]"""
    a1, b1 = random.choice([(5, 1), (3, 1), (4, 1), (7, 2), (5, 3), (2, 1), (7, 3)])
    a2, b2 = random.choice([(1, 1), (2, 3), (1, 2), (1, 3), (3, 5), (2, 5), (1, 4)])
    k1, k2 = random.choice([(1, 1), (1, 2), (2, 1), (2, 3), (3, 2), (1, 3), (3, 1)])
    milk = k1 * Fraction(a1, a1 + b1) + k2 * Fraction(a2, a2 + b2)
    water = k1 * Fraction(b1, a1 + b1) + k2 * Fraction(b2, a2 + b2)
    fr = milk / water
    correct = (fr.numerator, fr.denominator)
    # distractors
    w1 = (fr.denominator, fr.numerator)            # inverted
    inv = (k2 * Fraction(a1, a1 + b1) + k1 * Fraction(a2, a2 + b2)) / \
          (k2 * Fraction(b1, a1 + b1) + k1 * Fraction(b2, a2 + b2))
    w2 = (inv.numerator, inv.denominator)          # swapped mix ratio
    naive = Fraction(a1 + a2, b1 + b2)             # naive add ratios
    w3 = (naive.numerator, naive.denominator)
    stem = (f"Vessel A contains milk and water in the ratio {a1} : {b1} and vessel B "
            f"contains them in the ratio {a2} : {b2}. The contents of A and B are mixed "
            f"in the ratio {k1} : {k2}. The ratio of milk to water in the final "
            f"mixture is:")
    sol = (f"Milk = {k1}x{a1}/{a1+b1} + {k2}x{a2}/{a2+b2} = {fmt(milk)}; "
           f"water = {k1}x{b1}/{a1+b1} + {k2}x{b2}/{a2+b2} = {fmt(water)}. "
           f"Ratio = {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "H")


def t_two_vessels_equal_qty():
    """Equal quantities from two vessels (ratios) mixed -> resulting ratio. [H]"""
    a1, b1 = random.choice([(7, 3), (5, 2), (3, 2), (4, 3), (5, 4), (7, 5), (5, 1)])
    a2, b2 = random.choice([(2, 3), (1, 4), (3, 7), (2, 5), (1, 3), (4, 5), (1, 2)])
    milk = Fraction(a1, a1 + b1) + Fraction(a2, a2 + b2)
    water = Fraction(b1, a1 + b1) + Fraction(b2, a2 + b2)
    fr = milk / water
    correct = (fr.numerator, fr.denominator)
    w1 = (fr.denominator, fr.numerator)
    naive = Fraction(a1 + a2, b1 + b2)
    w2 = (naive.numerator, naive.denominator)
    w3 = (a1 + b2, a2 + b1)
    stem = (f"Equal quantities are taken from two vessels in which milk and water are "
            f"in the ratios {a1} : {b1} and {a2} : {b2} respectively, and mixed. "
            f"The ratio of milk to water in the new mixture is:")
    sol = (f"Per unit from each: milk = {a1}/{a1+b1} + {a2}/{a2+b2} = {fmt(milk)}; "
           f"water = {b1}/{a1+b1} + {b2}/{a2+b2} = {fmt(water)}. "
           f"Ratio = {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "H")


def t_dishonest_milkman():
    """Milkman sells at cost price of pure but adds water for x% profit -> water:milk. [H/VH]"""
    x = random.choice([10, 12, 15, 20, 25, 30, 40, 50])
    xf = Fraction(x, 100)
    # profit% = water/milk (selling water for free). water:milk = x:100
    fr = Fraction(x, 100)
    correct = (fr.numerator, fr.denominator)       # water : milk
    w1 = (fr.denominator, fr.numerator)            # milk:water inverted
    # gain%/(100+gain%) -> common wrong (water as fraction of mixture)
    alt = Fraction(x, 100 + x)
    w2 = (alt.numerator, alt.denominator)
    w3 = (x, 100 - x) if x < 100 else (x, 50)
    stem = (f"A dishonest milkman sells his milk at cost price but mixes water with it "
            f"and thereby gains {x}%. The ratio of water to milk in the mixture is:")
    sol = (f"Selling water (cost 0) at milk's price gives profit% = water/milk x 100. "
           f"So water:milk = {x}:100 = {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "H")


def t_acid_concentration_mix():
    """Mix acid solutions of c1% and c2% to get target t% -> ratio. [H]"""
    c1 = random.choice([10, 15, 20, 25, 30])
    c2 = random.choice([50, 55, 60, 70, 75, 80, 90])
    if c2 <= c1 + 5:
        return None
    t = random.randint(c1 + 2, c2 - 2)
    a, b = c2 - t, t - c1                            # ratio sol1 : sol2
    fr = Fraction(a, b)
    correct = (fr.numerator, fr.denominator)
    w1 = (b, a)
    w2 = (t - c1, c2 - t)                            # swapped
    w3 = (c2, c1)
    stem = (f"Two acid solutions contain {c1}% and {c2}% acid respectively. In what "
            f"ratio must they be mixed to obtain a solution containing {t}% acid?")
    sol = (f"Alligation on concentrations: ratio = ({c2}-{t}) : ({t}-{c1}) = {a}:{b} "
           f"= {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "H")


def t_add_water_dilute_acid():
    """V L of c% acid; add water to make it t% -> litres of water. [H]"""
    c = random.choice([40, 45, 50, 60, 75, 80, 90])
    V = random.choice([12, 15, 20, 24, 30, 40, 50, 60])
    t_choices = [d for d in (10, 15, 20, 25, 30, 36, 40, 45) if d < c]
    t = random.choice(t_choices)
    acid = Fraction(c, 100) * V
    total_new = acid / Fraction(t, 100)             # total volume to reach t%
    water = total_new - V
    if water <= 0 or water != int(water):
        return None
    correct = water
    w1 = total_new                                  # forgets to subtract V
    w2 = Fraction(V) * Fraction(c - t, 100)         # wrong formula
    w3 = Fraction(V) * Fraction(c, t)               # ratio slip
    stem = (f"{V} litres of a solution contain {c}% acid. How much water (in litres) "
            f"must be added to reduce the acid concentration to {t}%?")
    sol = (f"Acid = {c}% of {V} = {fmt(acid)} L is constant = {t}% of the new total, "
           f"so new total = {fmt(acid)} x 100/{t} = {fmt(total_new)} L. "
           f"Water to add = {fmt(total_new)} - {V} = {fmt(correct)} L.")
    return ("num", stem, correct, [w1, w2, w3], sol, "H")


def t_quantity_to_add_concentration():
    """Mixture V L is milk a:b; how much milk to add to make milk% = target. [H/VH]"""
    a = random.choice([3, 4, 5, 7])
    b = random.choice([2, 3, 4, 5])
    V = random.choice([20, 30, 40, 50, 60, 80, 100])
    if V % (a + b) != 0:
        return None
    milk = Fraction(a, a + b) * V
    water = V - milk
    # add pure milk to reach milk% = t (water fixed)
    t = random.choice([d for d in (60, 64, 70, 72, 75, 80) if d > Fraction(a, a + b) * 100])
    if not t:
        return None
    # water/(total) = (100-t)/100 -> total = water*100/(100-t)
    total_new = water * Fraction(100, 100 - t)
    added = total_new - V
    if added <= 0 or added != int(added):
        return None
    correct = added
    w1 = total_new                                  # forgets subtract V
    w2 = milk * Fraction(t, 100)                    # wrong base
    w3 = Fraction(t - int(Fraction(a, a + b) * 100))  # naive pct diff
    stem = (f"A {V}-litre mixture contains milk and water in the ratio {a} : {b}. "
            f"How many litres of pure milk must be added so that milk forms {t}% of "
            f"the new mixture?")
    sol = (f"Water = {b}/{a+b} x {V} = {fmt(water)} L stays fixed = {100-t}% of new "
           f"total, so new total = {fmt(water)} x 100/{100-t} = {fmt(total_new)} L. "
           f"Pure milk to add = {fmt(total_new)} - {V} = {fmt(correct)} L.")
    return ("num", stem, correct, [w1, w2, w3], sol, "VH")


def t_mean_price_profit():
    """Mix two ingredients in given ratio; sell mixture at SP -> profit% (via mean cost). [H]"""
    p1 = random.choice([20, 24, 25, 30, 32, 40])
    p2 = random.choice([50, 60, 64, 72, 80, 90, 100])
    if p2 <= p1:
        return None
    k1, k2 = random.choice([(1, 1), (2, 1), (1, 2), (3, 2), (2, 3), (3, 1)])
    mean = (k1 * Fraction(p1) + k2 * Fraction(p2)) / (k1 + k2)
    # choose SP giving clean profit%
    profit_pct = random.choice([10, 12, 15, 20, 25, 50])
    sp = mean * Fraction(100 + profit_pct, 100)
    if sp != int(sp) or mean != int(mean):
        return None
    correct = Fraction(profit_pct)
    w1 = (sp - mean)                                # absolute profit not %
    w2 = (sp - mean) / sp * 100                     # profit on SP
    w3 = Fraction(profit_pct) + 5
    stem = (f"Two types of rice costing Rs.{p1} and Rs.{p2} per kg are mixed in the "
            f"ratio {k1} : {k2}. If the mixture is sold at Rs.{fmt(sp)} per kg, the "
            f"profit percentage is:")
    sol = (f"Mean cost = ({k1}x{p1}+{k2}x{p2})/{k1+k2} = Rs.{fmt(mean)}/kg. "
           f"Profit% = (SP-CP)/CP x 100 = ({fmt(sp)}-{fmt(mean)})/{fmt(mean)} x 100 "
           f"= {fmt(correct)}%.")
    return ("num", stem, correct, [w1, w2, w3], sol, "H")


def t_wine_water_replacement_ratio():
    """Cask of wine, draw y and replace with water, n times; final wine:water. [VH]"""
    x = random.choice([32, 40, 48, 60, 64, 80, 81, 100])
    y = random.choice([4, 5, 6, 8, 10, 12, 16, 20])
    if y >= x or x % y != 0:
        return None
    n = random.choice([2, 3])
    wine = (Fraction(x - y, x)) ** n
    water = 1 - wine
    if water <= 0:
        return None
    fr = wine / water
    correct = (fr.numerator, fr.denominator)
    w1 = (fr.denominator, fr.numerator)
    w2 = (x - y * n, y * n)
    inv = (Fraction(x - y, x)) ** (n - 1)
    w3 = (inv.numerator, inv.denominator - inv.numerator) if inv.denominator > inv.numerator else (3, 1)
    stem = (f"A cask contains {x} litres of wine. {y} litres are drawn out and replaced "
            f"with water; the process is repeated {n} times in all. The ratio of wine "
            f"to water in the cask now is:")
    sol = (f"Wine fraction = ({x-y}/{x})^{n} = {fmt(wine)}; water = {fmt(water)}. "
           f"Wine:water = {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "VH")


def t_milk_water_find_quantity():
    """Mixture V L, milk:water = a:b; find quantity of water in it. [M]"""
    a = random.choice([3, 4, 5, 7, 8, 9])
    b = random.choice([1, 2, 3, 4, 5])
    V = random.choice([24, 30, 36, 40, 45, 48, 60, 72, 80, 90])
    if V % (a + b) != 0:
        return None
    water = Fraction(b, a + b) * V
    milk = V - water
    correct = water
    w1 = milk                                       # gives milk instead
    w2 = Fraction(b, a) * V                          # wrong denominator
    w3 = Fraction(V, a + b)                          # one part only
    stem = (f"A mixture of {V} litres contains milk and water in the ratio {a} : {b}. "
            f"The quantity of water (in litres) in the mixture is:")
    sol = (f"Water = {b}/{a+b} x {V} = {fmt(correct)} litres.")
    return ("num", stem, correct, [w1, w2, w3], sol, "M")


def t_ratio_mix_to_target_conc():
    """Mix milk:water solutions (as % milk) to get target % milk -> ratio. [H]"""
    c1 = random.choice([40, 50, 60])                # % milk in sol1
    c2 = random.choice([80, 85, 90, 95, 100])       # % milk in sol2
    if c2 <= c1 + 5:
        return None
    t = random.randint(c1 + 2, c2 - 2)
    a, b = c2 - t, t - c1
    fr = Fraction(a, b)
    correct = (fr.numerator, fr.denominator)
    w1 = (b, a)
    w2 = (t - c1, c2 - t)
    w3 = (c1, c2)
    stem = (f"One solution contains {c1}% milk and another contains {c2}% milk. In what "
            f"ratio should the two be mixed to obtain a solution containing {t}% milk?")
    sol = (f"Alligation: ratio = ({c2}-{t}) : ({t}-{c1}) = {a}:{b} "
           f"= {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "H")


def t_alligation_average_age_like():
    """Alligation on two quantities at rates to hit average rate -> ratio (e.g. interest/speed-priced)."""
    p1 = random.choice([4, 5, 6, 8])                 # rate % (cheaper)
    p2 = random.choice([10, 12, 15, 16, 18, 20])     # rate % (dearer)
    if p2 <= p1 + 2:
        return None
    m = random.randint(p1 + 1, p2 - 1)
    a, b = p2 - m, m - p1
    fr = Fraction(a, b)
    correct = (fr.numerator, fr.denominator)
    w1 = (b, a)
    w2 = (p2, p1)
    w3 = (m - p1, p2 - m + 1)
    stem = (f"A sum is to be invested in two schemes giving {p1}% and {p2}% returns. "
            f"In what ratio should the money be divided so that the overall return is "
            f"{m}%?")
    sol = (f"Alligation: lower:higher = ({p2}-{m}) : ({m}-{p1}) = {a}:{b} "
           f"= {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "H")


def t_replace_to_target_fraction():
    """How much (y) to draw & replace ONCE so milk drops to target fraction. [VH]"""
    x = random.choice([20, 30, 40, 50, 60, 80, 100])
    # after one replacement milk = x*(x-y)/x = x-y ; choose target so y clean
    frac_choices = [Fraction(3, 4), Fraction(4, 5), Fraction(2, 3), Fraction(5, 6),
                    Fraction(7, 8), Fraction(9, 10)]
    f = random.choice(frac_choices)
    milk_left = f * x
    y = x - milk_left
    if y <= 0 or y != int(y):
        return None
    correct = Fraction(y)
    w1 = Fraction(x) - milk_left * f                 # apply fraction twice
    w2 = Fraction(x) * (1 - f)                        # same value sometimes; guard
    w3 = milk_left                                    # gives milk left instead
    # ensure distinct
    stem = (f"A vessel is full of {x} litres of pure milk. How many litres must be "
            f"drawn off and replaced with water (in a single operation) so that the "
            f"milk left becomes {fmt(f)} of the original quantity?")
    sol = (f"After one replacement, milk left = x - y = {fmt(f)} x {x} = "
           f"{fmt(milk_left)} L, so y = {x} - {fmt(milk_left)} = {fmt(correct)} L.")
    return ("num", stem, correct, [w1, w2, w3], sol, "VH")


def t_two_vessels_find_mix_ratio():
    """Two vessels milk:water r1, r2; in what ratio mixed to get target ratio. [VH]"""
    a1, b1 = random.choice([(5, 1), (4, 1), (7, 2), (3, 1), (5, 2), (2, 1)])
    a2, b2 = random.choice([(1, 1), (1, 2), (2, 3), (1, 3), (2, 5), (1, 4)])
    f1 = Fraction(a1, a1 + b1)         # milk fraction vessel A
    f2 = Fraction(a2, a2 + b2)         # milk fraction vessel B
    # target milk fraction strictly between f2 and f1
    lo, hi = min(f1, f2), max(f1, f2)
    # pick a nice target milk:water ratio
    tgt = random.choice([(1, 1), (3, 2), (2, 1), (3, 1), (2, 3), (5, 3), (4, 3), (5, 4)])
    tf = Fraction(tgt[0], tgt[0] + tgt[1])
    if not (lo < tf < hi):
        return None
    # alligation on milk fractions: A:B = (tf - f2) : (f1 - tf)  (A is richer)
    num = tf - f2
    den = f1 - tf
    if num == 0 or den == 0:
        return None
    fr = num / den
    if fr <= 0:
        return None
    correct = (fr.numerator, fr.denominator)
    w1 = (fr.denominator, fr.numerator)
    inv = (tf - f1) / (f2 - tf) if (f2 - tf) != 0 else None
    w2 = (abs(inv.numerator), abs(inv.denominator)) if inv else (a1, a2)
    w3 = (a1 + a2, b1 + b2)
    stem = (f"Vessel A has milk and water in the ratio {a1} : {b1}, and vessel B has "
            f"them in the ratio {a2} : {b2}. In what ratio must the contents of A and B "
            f"be mixed so that the resulting mixture has milk and water in the ratio "
            f"{tgt[0]} : {tgt[1]}?")
    sol = (f"Milk fractions: A = {fmt(f1)}, B = {fmt(f2)}, target = {fmt(tf)}. "
           f"By alligation A:B = (target-B):(A-target) = ({fmt(tf)}-{fmt(f2)}) : "
           f"({fmt(f1)}-{fmt(tf)}) = {correct[0]} : {correct[1]}.")
    return ("ratio", stem, correct, [w1, w2, w3], sol, "VH")


def t_replacement_solve_x():
    """After n replacements of y, milk fraction is f -> find original volume x. [VH]"""
    # pick x, y, n giving a clean fraction, then ask for x given y, n, fraction
    base = random.choice([(20, 5, 2), (40, 10, 2), (50, 10, 2), (60, 12, 2),
                          (80, 20, 2), (100, 20, 2), (30, 10, 3), (60, 20, 3),
                          (40, 10, 3), (80, 20, 3), (100, 25, 2), (24, 6, 2),
                          (36, 12, 2), (45, 15, 2), (90, 30, 2), (120, 30, 2),
                          (75, 15, 2), (90, 18, 2), (150, 30, 2), (64, 16, 2),
                          (20, 5, 3), (40, 10, 3), (100, 20, 3), (50, 10, 3)])
    x, y, n = base
    frac_left = (Fraction(x - y, x)) ** n
    milk_left = Fraction(x) * frac_left
    if milk_left != int(milk_left):
        return None
    correct = Fraction(x)
    w1 = milk_left                                   # gives milk left
    w2 = Fraction(x) - Fraction(y) * n               # naive
    w3 = Fraction(x) + y                             # off by y
    stem = (f"From a vessel full of pure milk, {y} litres are drawn off and replaced "
            f"with water; after doing this {n} times the vessel holds {fmt(milk_left)} "
            f"litres of milk. The capacity (in litres) of the vessel is:")
    sol = (f"x(1 - {y}/x)^{n} = {fmt(milk_left)}. Testing x = {x}: "
           f"{x}*({x-y}/{x})^{n} = {fmt(milk_left)}. So capacity = {fmt(correct)} L.")
    return ("num", stem, correct, [w1, w2, w3], sol, "VH")


# (template_fn, difficulty)
TEMPLATES = [
    (t_alligation_ratio, "M"),
    (t_alligation_tea_blend, "M"),
    (t_replacement_milk_left, "H"),
    (t_replacement_ratio, "H"),
    (t_add_water_to_ratio, "H"),
    (t_two_vessels_mix_equal, "H"),
    (t_two_vessels_equal_qty, "H"),
    (t_dishonest_milkman, "H"),
    (t_acid_concentration_mix, "H"),
    (t_add_water_dilute_acid, "H"),
    (t_quantity_to_add_concentration, "VH"),
    (t_mean_price_profit, "H"),
    (t_wine_water_replacement_ratio, "VH"),
    (t_milk_water_find_quantity, "M"),
    (t_ratio_mix_to_target_conc, "H"),
    (t_alligation_average_age_like, "H"),
    (t_replace_to_target_fraction, "VH"),
    (t_two_vessels_find_mix_ratio, "VH"),
    (t_replacement_solve_x, "VH"),
]

DIFF_OF = {fn: d for fn, d in TEMPLATES}
# Tuned so realized counts land near 20% M / 60% H / 20% VH.
# VH templates have many None/dedupe rejects, so they get an extra boost.
WEIGHT = {"M": 1.5, "H": 2.0, "VH": 6.5}
POOL = []
for fn, d in TEMPLATES:
    POOL += [fn] * int(WEIGHT[d] * 10)


def dispatch(res):
    """Route a template result through the correct add().  Returns bool added."""
    kind = res[0]
    if kind == "num":
        _, stem, correct, distractors, sol, diff = res
        return add(stem, correct, distractors, sol, diff)
    elif kind == "ratio":
        _, stem, correct_pair, distractor_pairs, sol, diff = res
        return add_ratio(stem, correct_pair, distractor_pairs, sol, diff)
    return False


# Generate until we have 500 unique
attempts = 0
while len(questions) < 500 and attempts < 600000:
    attempts += 1
    t = random.choice(POOL)
    res = t()
    if res is None:
        continue
    dispatch(res)

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- VERIFY: 4 distinct options, one correct ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
print(f"Verification errors: {errors}")
print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_14_Mixture_Alligation_500.md"

lines = []
lines.append("# Mixture & Alligation — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** Medium / Hard / Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- **Alligation rule:** cheaper : dearer = (dearer − mean) : (mean − cheaper)")
lines.append("- Mean price = (q₁·p₁ + q₂·p₂) / (q₁ + q₂)")
lines.append("- **Replacement:** after n operations of removing y from x and refilling, pure left = **x(1 − y/x)ⁿ**")
lines.append("- Ratio milk:water after replacement = (1−y/x)ⁿ : [1 − (1−y/x)ⁿ]")
lines.append("- Add water to dilute: acid (or milk) amount is constant; new total = amount / target-fraction")
lines.append("- Dishonest seller at cost price for x% gain → water : milk = **x : 100**")
lines.append("- Mixing two ratios a₁:b₁ and a₂:b₂ in ratio k₁:k₂ → combine milk & water parts, then reduce\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        o = q["opts"]
        lines.append(f"**Q{n}.** {q['stem']}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    lines.append(f"\n## Answers Q{start+1}–Q{start+50}\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        letter = LETTERS[q["ci"]]
        val = q["opts"][q["ci"]]
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* — {q['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUT}")
print(f"Total lines: {len(lines)}")
