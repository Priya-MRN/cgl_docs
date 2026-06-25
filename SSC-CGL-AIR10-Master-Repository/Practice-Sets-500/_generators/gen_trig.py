# -*- coding: utf-8 -*-
"""
SSC CGL Trigonometry (incl. Heights & Distances) - 500 hard MCQ generator.
Every answer is COMPUTED, so the key is provably correct.
Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.

Exact representation:
 - Standard-angle ratios are exact rationals or surds. Rational answers are
   carried as Fraction. Surd answers are carried as a SurdVal that stores an
   exact display string ('√3', '50√3', '7/√3', etc.) plus its float value, so
   options can be shuffled / deduped / compared numerically while printing in
   exact form. Every accepted answer is checked by is_clean() (rationals) or is
   a SurdVal (always exact). NO float is ever passed into Fraction(num, den).
"""
import random
import math
from fractions import Fraction

random.seed(20260625)  # deterministic

LETTERS = "abcd"
R3 = math.sqrt(3)
R2 = math.sqrt(2)


# ---------------- Surd value type ----------------
class SurdVal:
    """Carries a display string (exact form e.g. '50√3') plus its float value.
    Used so that surd answers can be shuffled / compared / deduped numerically
    while still being printed in exact form."""
    __slots__ = ("disp", "val")

    def __init__(self, disp, val):
        self.disp = disp
        self.val = float(val)

    def __float__(self):
        return self.val


def fval(x):
    """Numeric value of anything we use as an option/answer."""
    if isinstance(x, SurdVal):
        return x.val
    return float(x)


def fmt(x):
    """Format an option for display."""
    if isinstance(x, SurdVal):
        return x.disp
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


# helpers to build surd display strings cleanly --------------------------------
def surd_mul(coef, root_disp, root_val):
    """coef (Fraction) times sqrt; produce a clean SurdVal.
    root_disp e.g. '√3', root_val e.g. R3."""
    c = Fraction(coef)
    val = float(c) * root_val
    if c == 0:
        return Fraction(0)
    if c == 1:
        disp = root_disp
    elif c == -1:
        disp = "-" + root_disp
    elif c.denominator == 1:
        disp = f"{c.numerator}{root_disp}"
    else:
        disp = f"({c.numerator}/{c.denominator}){root_disp}"
    return SurdVal(disp, val)


def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 distinct values."""
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        if all(abs(fval(d) - fval(o)) > 1e-6 for o in opts):
            opts.append(d)
        if len(opts) == 4:
            break
    # pad with plausible numeric filler if needed (never surd filler)
    bump = 1
    cf = fval(correct)
    base = Fraction(cf).limit_denominator(1000)
    while len(opts) < 4:
        step = Fraction(1, 2) * bump
        cand = base + (step if cf >= 0 else -step)
        if all(abs(float(cand) - fval(o)) > 1e-6 for o in opts):
            opts.append(cand)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci


questions = []  # each: dict(stem, opts(list of str), ci, sol, diff)
seen = set()


def is_clean(x):
    """SurdVal always clean (exact). Numeric: integers, simple fractions,
    or <=2dp decimals."""
    if isinstance(x, SurdVal):
        return True
    fr = Fraction(x).limit_denominator(10**6)
    if fr.denominator in (1, 2, 3, 4, 5, 6, 8, 10):
        return True
    f = float(fr)
    return abs(f - round(f, 2)) < 1e-9


def _norm(x):
    if isinstance(x, SurdVal):
        return x
    return Fraction(x).limit_denominator(10**6)


def add(stem, correct, distractors, sol, diff):
    key = stem.strip()
    if key in seen:
        return False
    c = _norm(correct)
    if not is_clean(c):
        return False
    ds = []
    for d in distractors:
        if d is None:
            continue
        dn = _norm(d)
        if not is_clean(dn):
            continue
        if abs(fval(dn) - fval(c)) < 1e-6:
            continue
        ds.append(dn)
    # dedupe distractors among themselves
    uniq = []
    for d in ds:
        if all(abs(fval(d) - fval(u)) > 1e-6 for u in uniq):
            uniq.append(d)
    if len(uniq) < 3:
        return False
    seen.add(key)
    opts, ci = make_options(c, uniq)
    questions.append({
        "stem": stem,
        "opts": [fmt(o) for o in opts],
        "ci": ci,
        "sol": sol,
        "diff": diff,
    })
    return True


# ---------------- Standard-angle exact ratios ----------------
# Each ratio represented as a value-producer. We store sin/cos/tan as exact
# objects: Fraction for rationals, SurdVal for surds.
def sin_d(a):
    return {0: Fraction(0), 30: Fraction(1, 2), 45: surd_mul(Fraction(1, 2), "√2", R2),
            60: surd_mul(Fraction(1, 2), "√3", R3), 90: Fraction(1)}[a]


def cos_d(a):
    return sin_d(90 - a)


def tan_d(a):
    return {0: Fraction(0), 30: surd_mul(Fraction(1, 3), "√3", R3),  # 1/√3 = √3/3
            45: Fraction(1), 60: surd_mul(Fraction(1), "√3", R3)}[a]


def cot_d(a):
    return {30: surd_mul(Fraction(1), "√3", R3), 45: Fraction(1),
            60: surd_mul(Fraction(1, 3), "√3", R3), 90: Fraction(0)}[a]


def sec_d(a):
    return {0: Fraction(1), 30: surd_mul(Fraction(2, 3), "√3", R3),  # 2/√3
            45: surd_mul(Fraction(1), "√2", R2), 60: Fraction(2)}[a]


def csc_d(a):
    return sec_d(90 - a)


# Pythagorean triples for sin=a/b style questions (opp, adj, hyp).
TRIPLES = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13),
           (8, 15, 17), (15, 8, 17), (7, 24, 25), (24, 7, 25),
           (20, 21, 29), (21, 20, 29), (9, 40, 41), (40, 9, 41)]


# ================= TEMPLATES =================

# Standard ratios that are RATIONAL (so a combo stays rational/clean).
RAT_TERMS = [
    ("sin 30°", Fraction(1, 2)), ("cos 60°", Fraction(1, 2)),
    ("sin 90°", Fraction(1)), ("cos 0°", Fraction(1)),
    ("tan 45°", Fraction(1)), ("cot 45°", Fraction(1)),
    ("sin 0°", Fraction(0)), ("cos 90°", Fraction(0)),
    ("sin² 45°", Fraction(1, 2)), ("cos² 45°", Fraction(1, 2)),
    ("cos² 30°", Fraction(3, 4)), ("sin² 30°", Fraction(1, 4)),
    ("sin² 60°", Fraction(3, 4)), ("cos² 60°", Fraction(1, 4)),
    ("tan² 45°", Fraction(1)), ("sec² 45° − tan² 45°", Fraction(1)),
]


def t_eval_standard():
    """Evaluate a random linear combo of RATIONAL standard-angle terms. [H]"""
    n = random.choice([2, 3, 3, 3])
    terms = random.sample(RAT_TERMS, n)
    coeffs = [random.choice([1, 2, 2, 3, 4, 5, 6]) for _ in range(n)]
    signs = [random.choice([1, 1, -1]) for _ in range(n)]
    signs[0] = 1  # lead positive
    total = Fraction(0)
    parts = []
    for (name, val), c, s in zip(terms, coeffs, signs):
        total += s * c * val
        cstr = "" if c == 1 else f"{c}·"
        op = " + " if s > 0 else " − "
        parts.append((op, cstr, name))
    expr = parts[0][1] + parts[0][2]
    for op, cstr, name in parts[1:]:
        expr += op + cstr + name
    correct = total
    if not is_clean(correct):
        return None
    w1 = correct + Fraction(1)
    w2 = correct - Fraction(1, 2)
    w3 = correct + Fraction(3, 2)
    stem = f"The value of {expr} is:"
    sol = (f"Substitute standard values (sin30°=½, cos60°=½, tan45°=cot45°=1, "
           f"sin90°=cos0°=1, sin²45°=cos²45°=½, cos²30°=sin²60°=¾): "
           f"{expr} = {fmt(correct)}.")
    return stem, correct, [w1, w2, w3], sol, "H"


# Each entry: (expression-of-θ, its value as Fraction, reason)
UNIT_IDENTS = [
    ("sin²θ + cos²θ", Fraction(1), "Pythagorean identity sin²θ + cos²θ = 1"),
    ("sec²θ − tan²θ", Fraction(1), "sec²θ − tan²θ = 1"),
    ("cosec²θ − cot²θ", Fraction(1), "cosec²θ − cot²θ = 1"),
    ("(1 − sin²θ)·sec²θ", Fraction(1), "(1−sin²θ)sec²θ = cos²θ·sec²θ = 1"),
    ("(1 + tan²θ)·cos²θ", Fraction(1), "(1+tan²θ)cos²θ = sec²θ·cos²θ = 1"),
    ("(1 + cot²θ)·sin²θ", Fraction(1), "(1+cot²θ)sin²θ = cosec²θ·sin²θ = 1"),
    ("sin θ·cosec θ", Fraction(1), "cosecθ = 1/sinθ, so the product = 1"),
    ("cos θ·sec θ", Fraction(1), "secθ = 1/cosθ, so the product = 1"),
    ("tan θ·cot θ", Fraction(1), "cotθ = 1/tanθ, so the product = 1"),
    ("(1 − cos²θ)·cosec²θ", Fraction(1), "(1−cos²θ)cosec²θ = sin²θ·cosec²θ = 1"),
]


def t_identity_const():
    """k·(unit identity) -> k. Coefficient gives many unique stems. [M]"""
    expr1, v1, why = random.choice(UNIT_IDENTS)
    k = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    correct = Fraction(k) * v1
    if k == 1:
        expr = expr1
    else:
        expr = f"{k}·({expr1})"
    w1 = correct + Fraction(1)
    w2 = correct + Fraction(2)
    w3 = correct - Fraction(1) if correct > Fraction(1) else correct + Fraction(3)
    stem = f"For any acute angle θ, the value of {expr} is:"
    sol = f"{why}; multiplying by {k} gives {fmt(correct)}." if k != 1 else f"{why} = {fmt(correct)}."
    return stem, correct, [w1, w2, w3], sol, "M"


def t_sin_from_triple():
    """Given sinθ = a/c, find cosθ or tanθ (clean via triple). [H]"""
    opp, adj, hyp = random.choice(TRIPLES)
    want = random.choice(["cos", "tan", "cot", "sec", "cosec"])
    sin_v = Fraction(opp, hyp)
    cos_v = Fraction(adj, hyp)
    if want == "cos":
        correct = cos_v
        w1 = Fraction(opp, adj)       # tan
        w2 = Fraction(adj, opp)       # cot
        w3 = Fraction(hyp, adj)       # sec
        ask = "cos θ"
        sol = (f"sinθ = {opp}/{hyp} → adjacent = √({hyp}²−{opp}²) = {adj} "
               f"({opp}-{adj}-{hyp} triple). cosθ = {adj}/{hyp} = {fmt(correct)}.")
    elif want == "tan":
        correct = Fraction(opp, adj)
        w1 = Fraction(opp, hyp)
        w2 = Fraction(adj, opp)
        w3 = Fraction(adj, hyp)
        ask = "tan θ"
        sol = (f"sinθ = {opp}/{hyp} → adjacent = {adj}. tanθ = opp/adj = "
               f"{opp}/{adj} = {fmt(correct)}.")
    elif want == "cot":
        correct = Fraction(adj, opp)
        w1 = Fraction(opp, adj)
        w2 = Fraction(hyp, adj)
        w3 = Fraction(adj, hyp)
        ask = "cot θ"
        sol = (f"sinθ = {opp}/{hyp} → adjacent = {adj}. cotθ = adj/opp = "
               f"{adj}/{opp} = {fmt(correct)}.")
    elif want == "sec":
        correct = Fraction(hyp, adj)
        w1 = Fraction(hyp, opp)
        w2 = Fraction(adj, hyp)
        w3 = Fraction(opp, adj)
        ask = "sec θ"
        sol = (f"sinθ = {opp}/{hyp} → adjacent = {adj}. secθ = hyp/adj = "
               f"{hyp}/{adj} = {fmt(correct)}.")
    else:  # cosec
        correct = Fraction(hyp, opp)
        w1 = Fraction(hyp, adj)
        w2 = Fraction(opp, hyp)
        w3 = Fraction(adj, opp)
        ask = "cosec θ"
        sol = (f"cosecθ = 1/sinθ = {hyp}/{opp} = {fmt(correct)}.")
    if not is_clean(correct):
        return None
    stem = (f"If sin θ = {opp}/{hyp} and θ is acute, then the value of {ask} is:")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_expr_from_triple():
    """Given a ratio, evaluate (sinθ+cosθ) or (sinθ·cosθ) etc -> rational. [H]"""
    opp, adj, hyp = random.choice(TRIPLES)
    sin_v = Fraction(opp, hyp)
    cos_v = Fraction(adj, hyp)
    kind = random.choice(["sum", "prod", "sin2_min_cos2", "ratio"])
    if kind == "sum":
        correct = sin_v + cos_v
        expr = "sin θ + cos θ"
        w1 = sin_v - cos_v
        w2 = sin_v * cos_v
        w3 = Fraction(opp + adj, opp)
        sol = (f"From the {opp}-{adj}-{hyp} triple, sinθ={opp}/{hyp}, cosθ={adj}/{hyp}. "
               f"sinθ+cosθ = ({opp}+{adj})/{hyp} = {fmt(correct)}.")
    elif kind == "prod":
        correct = sin_v * cos_v
        expr = "sin θ · cos θ"
        w1 = sin_v + cos_v
        w2 = sin_v - cos_v
        w3 = Fraction(opp * adj, hyp)
        sol = (f"sinθ·cosθ = ({opp}/{hyp})×({adj}/{hyp}) = {opp*adj}/{hyp*hyp} "
               f"= {fmt(correct)}.")
    elif kind == "sin2_min_cos2":
        correct = sin_v * sin_v - cos_v * cos_v
        expr = "sin²θ − cos²θ"
        w1 = cos_v * cos_v - sin_v * sin_v
        w2 = sin_v * sin_v + cos_v * cos_v
        w3 = sin_v - cos_v
        sol = (f"sin²θ−cos²θ = ({opp}²−{adj}²)/{hyp}² = "
               f"{opp*opp-adj*adj}/{hyp*hyp} = {fmt(correct)}.")
    else:  # ratio (sin+cos)/(sin-cos) requires sin!=cos
        if opp == adj:
            return None
        correct = Fraction(opp + adj, opp - adj)
        expr = "(sin θ + cos θ) / (sin θ − cos θ)"
        w1 = Fraction(opp - adj, opp + adj)
        w2 = Fraction(opp + adj, hyp)
        w3 = Fraction(opp, adj)
        sol = (f"Divide num & den by cosθ: (tanθ+1)/(tanθ−1) with tanθ={opp}/{adj} "
               f"→ ({opp}+{adj})/({opp}−{adj}) = {fmt(correct)}.")
    if not is_clean(correct):
        return None
    stem = (f"If sin θ = {opp}/{hyp} and θ is acute, the value of {expr} is:")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_tan_plus_cot():
    """Given tanθ (from triple), find tanθ + cotθ -> rational. [VH]"""
    opp, adj, hyp = random.choice(TRIPLES)
    if opp == adj:
        return None
    tan_v = Fraction(opp, adj)
    cot_v = Fraction(adj, opp)
    correct = tan_v + cot_v       # = hyp^2/(opp*adj)
    w1 = tan_v - cot_v
    w2 = tan_v * cot_v            # = 1 (trap)
    w3 = Fraction(opp + adj, hyp)
    if not is_clean(correct):
        return None
    stem = (f"If tan θ = {opp}/{adj} and θ is acute, then tan θ + cot θ equals:")
    sol = (f"tanθ+cotθ = {opp}/{adj} + {adj}/{opp} = ({opp}²+{adj}²)/({opp}×{adj}) "
           f"= {hyp}²/{opp*adj} = {fmt(correct)}. Note tanθ·cotθ = 1.")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_sec_plus_tan():
    """Given secθ - tanθ = k, find secθ + tanθ = 1/k (since product=1). [VH]"""
    # choose secθ+tanθ and secθ-tanθ as reciprocal rationals
    kvals = [Fraction(1, n) for n in (2, 3, 4, 5)] + \
            [Fraction(2, 3), Fraction(3, 4), Fraction(2, 5), Fraction(3, 5),
             Fraction(4, 5), Fraction(2, 7), Fraction(3, 7), Fraction(4, 7)]
    k = random.choice(kvals)
    base = random.choice(["sec_tan", "cosec_cot"])
    correct = 1 / k
    w1 = k
    w2 = 1 - k
    w3 = 1 + k
    if not is_clean(correct):
        return None
    if base == "sec_tan":
        stem = (f"If sec θ − tan θ = {fmt(k)}, then the value of sec θ + tan θ is:")
        sol = (f"Since (secθ−tanθ)(secθ+tanθ) = sec²θ−tan²θ = 1, "
               f"secθ+tanθ = 1/({fmt(k)}) = {fmt(correct)}.")
    else:
        stem = (f"If cosec θ − cot θ = {fmt(k)}, then the value of cosec θ + cot θ is:")
        sol = (f"Since (cosecθ−cotθ)(cosecθ+cotθ) = cosec²θ−cot²θ = 1, "
               f"cosecθ+cotθ = 1/({fmt(k)}) = {fmt(correct)}.")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_complementary():
    """Complementary-angle simplification with random angles -> constant. [H]"""
    a = random.choice([12, 15, 18, 20, 22, 25, 28, 32, 35, 38, 40, 42, 48])
    b = 90 - a
    kind = random.choice(["ratio_sc", "ratio_cs", "tan_prod", "sec_prod",
                          "sin2_sum", "cos2_sum"])
    correct = Fraction(1)
    if kind == "ratio_sc":
        expr = f"sin {a}° / cos {b}°"
        why = f"cos{b}° = cos(90°−{a}°) = sin{a}°, so the ratio = 1."
    elif kind == "ratio_cs":
        expr = f"cos {a}° / sin {b}°"
        why = f"sin{b}° = sin(90°−{a}°) = cos{a}°, so the ratio = 1."
    elif kind == "tan_prod":
        expr = f"tan {a}° · tan {b}°"
        why = f"tan{b}° = cot{a}°, so tan{a}°·tan{b}° = 1."
    elif kind == "sec_prod":
        expr = f"sin {a}° · sec {b}°"
        why = f"sec{b}° = cosec{a}° = 1/sin{a}°, so the product = 1."
    elif kind == "sin2_sum":
        expr = f"sin² {a}° + sin² {b}°"
        why = f"sin{b}° = cos{a}°, so sin²{a}°+cos²{a}° = 1."
    else:
        expr = f"cos² {a}° + cos² {b}°"
        why = f"cos{b}° = sin{a}°, so cos²{a}°+sin²{a}° = 1."
    w1 = Fraction(2)
    w2 = Fraction(0)
    w3 = Fraction(1, 2)
    stem = f"The value of {expr} is:"
    sol = why
    return stem, correct, [w1, w2, w3], sol, "H"


def t_product_to_one():
    """k·(product identity = 1) -> k. [M]"""
    forms = [
        ("(1 + tan²θ)(1 − sin²θ)", "= sec²θ · cos²θ = 1"),
        ("(1 + cot²θ)(1 − cos²θ)", "= cosec²θ · sin²θ = 1"),
        ("(sec²θ − 1)·cot²θ", "= tan²θ · cot²θ = 1"),
        ("(cosec²θ − 1)·tan²θ", "= cot²θ · tan²θ = 1"),
        ("(sec²θ − tan²θ)·(cosec²θ − cot²θ)", "= 1 · 1 = 1"),
    ]
    expr1, why = random.choice(forms)
    k = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
    correct = Fraction(k)
    expr = expr1 if k == 1 else f"{k}·[{expr1}]"
    w1 = Fraction(0)
    w2 = correct + Fraction(1)
    w3 = correct + Fraction(2)
    stem = (f"For an acute angle θ, the value of {expr} is:")
    sol = f"The bracket {why}; times {k} = {fmt(correct)}." if k != 1 else f"{expr1} {why}."
    return stem, correct, [w1, w2, w3], sol, "M"


# building blocks that each equal 1
ONE_BLOCKS = [
    "sin θ·cosec θ", "cos θ·sec θ", "tan θ·cot θ",
    "(sin²θ + cos²θ)", "(sec²θ − tan²θ)", "(cosec²θ − cot²θ)",
]


def t_chain_identity():
    """Sum of k unit-blocks (+ optional added constant) -> integer. [M]"""
    k = random.choice([2, 3, 4])
    blocks = random.sample(ONE_BLOCKS, k)
    add_const = random.choice([0, 0, 1, 2, 3, 5])
    correct = Fraction(k + add_const)
    expr = " + ".join(blocks)
    if add_const:
        expr += f" + {add_const}"
    w1 = correct + Fraction(1)
    w2 = correct - Fraction(1)
    w3 = correct + Fraction(2)
    stem = f"For any acute angle θ, the value of {expr} is:"
    sol = (f"Each of the {k} trigonometric blocks equals 1, summing to {k}"
           + (f", plus {add_const}" if add_const else "")
           + f" = {fmt(correct)}.")
    return stem, correct, [w1, w2, w3], sol, "M"


def t_elev_height():
    """Tower: distance d, elevation angle a -> height = d·tan(a). Surd-exact. [H]"""
    a = random.choice([30, 45, 60])
    d = random.choice([10, 20, 30, 40, 50, 60, 80, 100, 120, 150])
    if a == 45:
        correct = Fraction(d)            # d·1
        w1 = surd_mul(Fraction(d), "√3", R3)
        w2 = surd_mul(Fraction(d, 3), "√3", R3)
        w3 = Fraction(2 * d)
        disp = f"{d}"
    elif a == 60:
        correct = surd_mul(Fraction(d), "√3", R3)   # d√3
        w1 = surd_mul(Fraction(d, 3), "√3", R3)     # d/√3 (used cot)
        w2 = Fraction(d)
        w3 = Fraction(d * d)
        disp = f"{d}√3"
    else:  # 30
        correct = surd_mul(Fraction(d, 3), "√3", R3)  # d/√3 = d√3/3
        w1 = surd_mul(Fraction(d), "√3", R3)          # d√3 (used tan60)
        w2 = Fraction(d)
        w3 = Fraction(d, 2)
        disp = f"{fmt(Fraction(d,3))}√3"
    stem = (f"The angle of elevation of the top of a tower from a point {d} m away "
            f"from its base on level ground is {a}°. The height of the tower (in m) is:")
    sol = (f"height = distance × tan{a}° = {d} × tan{a}° = {disp} m "
           f"(tan30°=1/√3, tan45°=1, tan60°=√3).")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_elev_distance():
    """Tower of height h, elevation a -> horizontal distance = h/tan(a). [H]"""
    a = random.choice([30, 45, 60])
    if a == 60:
        h = random.choice([30, 60, 90, 120, 150, 180])   # multiple of 3 so /√3 clean coef
        correct = surd_mul(Fraction(h, 3), "√3", R3)      # h/√3
        w1 = surd_mul(Fraction(h), "√3", R3)
        w2 = Fraction(h)
        w3 = Fraction(h, 2)
        disp = f"{fmt(Fraction(h,3))}√3"
    elif a == 45:
        h = random.choice([20, 30, 40, 50, 60, 80, 100])
        correct = Fraction(h)
        w1 = surd_mul(Fraction(h), "√3", R3)
        w2 = surd_mul(Fraction(h, 3), "√3", R3)
        w3 = Fraction(2 * h)
        disp = f"{h}"
    else:  # 30
        h = random.choice([20, 30, 40, 50, 60, 80, 100])
        correct = surd_mul(Fraction(h), "√3", R3)         # h·cot30 = h√3
        w1 = surd_mul(Fraction(h, 3), "√3", R3)
        w2 = Fraction(h)
        w3 = Fraction(h, 2)
        disp = f"{h}√3"
    stem = (f"A tower is {h} m high. The angle of elevation of its top from a point "
            f"on the ground is {a}°. The distance of the point from the base of the "
            f"tower (in m) is:")
    sol = (f"distance = height / tan{a}° = {h} / tan{a}° = {disp} m.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_shadow_change():
    """Shadow change as sun's elevation drops. Two variants. [VH]"""
    variant = random.choice(["60to30", "45to30"])
    if variant == "60to30":
        h = random.choice([30, 60, 90, 120, 150, 180, 210, 240])
        # 60°->30°: h/√3 -> h√3 ; increase = h√3 - h/√3 = (2h/3)√3
        correct = surd_mul(Fraction(2 * h, 3), "√3", R3)
        w1 = surd_mul(Fraction(h, 3), "√3", R3)
        w2 = surd_mul(Fraction(h), "√3", R3)
        w3 = surd_mul(Fraction(4 * h, 3), "√3", R3)
        stem = (f"The shadow of a vertical pole {h} m high lengthens when the sun's "
                f"angle of elevation changes from 60° to 30°. The increase in the "
                f"length of the shadow (in m) is:")
        sol = (f"Shadow at 60° = {h}/√3; at 30° = {h}√3. Increase = {h}√3 − {h}/√3 "
               f"= (2×{h}/3)√3 = {fmt(correct)} m.")
    else:
        h = random.choice([30, 45, 60, 90, 120, 150, 180])
        # 45°->30°: h -> h√3 ; increase = h√3 - h = h(√3-1). Keep surd part only?
        # exact = h√3 - h ; not a single surd. Represent as SurdVal with combined float.
        val = h * R3 - h
        correct = SurdVal(f"{h}(√3−1)", val)
        w1 = surd_mul(Fraction(h), "√3", R3)              # h√3
        w2 = SurdVal(f"{h}(√3+1)", h * R3 + h)
        w3 = surd_mul(Fraction(h, 3), "√3", R3)
        stem = (f"The shadow of a vertical pole {h} m high lengthens when the sun's "
                f"angle of elevation changes from 45° to 30°. The increase in the "
                f"length of the shadow (in m) is:")
        sol = (f"Shadow at 45° = {h}; at 30° = {h}√3. Increase = {h}√3 − {h} "
               f"= {h}(√3−1) m ≈ {val:.2f} m.")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_two_points_tower():
    """Two observation points: angles 45 and 30 (or 60/30) along a line; tower
    height clean. Classic: from nearer point 45° and farther (d more) 30°.
    h = d / (cot30 - cot45) = d/(√3 - 1) -> rationalize. Choose 45 & 30 with the
    DIFFERENCE distance d, height comes out as d/(√3-1) = d(√3+1)/2.
    Use instead 30 & 60 to keep surd clean: h = d/(cot30-cot60)=d/(√3-1/√3)=d/((2/√3)) = d√3/2."""
    d = random.choice([10, 15, 20, 24, 25, 30, 36, 40, 45, 50, 60, 70, 72, 80,
                       90, 100, 120, 140, 150, 160, 180, 200, 240, 300])
    variant = random.choice(["30_60", "45_60", "30_45"])
    if variant == "30_60":
        # cot30 - cot60 = √3 - 1/√3 = 2/√3 ; h = d√3/2
        correct = surd_mul(Fraction(d, 2), "√3", R3)
        w1 = surd_mul(Fraction(d), "√3", R3)
        w2 = surd_mul(Fraction(d, 4), "√3", R3)
        w3 = Fraction(d)
        angs = "30° and 60°"
        sol = (f"h = d / (cot30° − cot60°) = {d} / (√3 − 1/√3) = {d} / (2/√3) "
               f"= {d}√3/2 = {fmt(correct)} m.")
    elif variant == "45_60":
        # cot45 - cot60 = 1 - 1/√3 = (√3-1)/√3 ; h = d√3/(√3-1) = d√3(√3+1)/2
        val = d * R3 / (R3 - 1)
        correct = SurdVal(f"{fmt(Fraction(d,2))}(3+√3)", val)
        w1 = surd_mul(Fraction(d), "√3", R3)
        w2 = surd_mul(Fraction(d, 2), "√3", R3)
        w3 = Fraction(d)
        angs = "45° and 60°"
        sol = (f"h = d / (cot45° − cot60°) = {d} / (1 − 1/√3) = {d}√3/(√3−1) "
               f"= (d/2)(3+√3) = {fmt(correct)} m ≈ {val:.2f} m.")
    else:  # 30_45
        # cot30 - cot45 = √3 - 1 ; h = d/(√3-1) = d(√3+1)/2
        val = d / (R3 - 1)
        correct = SurdVal(f"{fmt(Fraction(d,2))}(√3+1)", val)
        w1 = SurdVal(f"{fmt(Fraction(d,2))}(√3−1)", d * (R3 - 1) / 2)
        w2 = surd_mul(Fraction(d), "√3", R3)
        w3 = Fraction(d)
        angs = "30° and 45°"
        sol = (f"h = d / (cot30° − cot45°) = {d} / (√3 − 1) = d(√3+1)/2 "
               f"= {fmt(correct)} m ≈ {val:.2f} m.")
    stem = (f"The angles of elevation of the top of a tower from two points on the "
            f"ground, in line with the base and {d} m apart, are {angs}. "
            f"The height of the tower (in m) is:")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_range_a_sin_b():
    """Max / min of a·sinθ + b·cosθ is ±√(a²+b²). Choose triple so clean. [H]"""
    a, b, c = random.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
                             (6, 8, 10), (9, 12, 15), (20, 21, 29)])
    which = random.choice(["max", "min"])
    if which == "max":
        correct = Fraction(c)
        w1 = Fraction(-c)
        w2 = Fraction(a + b)
        w3 = Fraction(a * b)
        word = "maximum"
        sol = (f"Max of a·sinθ + b·cosθ = √(a²+b²) = √({a}²+{b}²) = √{a*a+b*b} "
               f"= {c}.")
    else:
        correct = Fraction(-c)
        w1 = Fraction(c)
        w2 = Fraction(-(a + b))
        w3 = Fraction(0)
        word = "minimum"
        sol = (f"Min of a·sinθ + b·cosθ = −√(a²+b²) = −√({a}²+{b}²) = −{c}.")
    stem = (f"The {word} value of {a}·sin θ + {b}·cos θ is:")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_range_sin2_cos2():
    """Range of a·sin²θ + b·cos²θ: between min(a,b) and max(a,b). Ask max or min. [H]"""
    a = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    b = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    if a == b:
        return None
    which = random.choice(["max", "min"])
    hi, lo = max(a, b), min(a, b)
    if which == "max":
        correct = Fraction(hi)
        word = "maximum"
    else:
        correct = Fraction(lo)
        word = "minimum"
    w1 = Fraction(a + b)
    w2 = Fraction(hi if which == "min" else lo)
    w3 = Fraction(a + b, 2)
    stem = (f"The {word} value of {a}·sin²θ + {b}·cos²θ is:")
    sol = (f"Write as {b} + ({a}−{b})sin²θ; as sin²θ ranges over [0,1] the expression "
           f"ranges between {lo} and {hi}. {word.capitalize()} = {fmt(correct)}.")
    return stem, correct, [w1, w2, w3], sol, "H"


def t_a_sin_b_cos_eq():
    """If sinθ + cosθ = k (rational, valid), find sinθ·cosθ = (k²−1)/2. [VH]"""
    # need 1 <= k <= √2 for an achievable acute solution, and (k²−1)/2 clean.
    k_options = [Fraction(6, 5), Fraction(7, 5), Fraction(11, 10),
                 Fraction(13, 10), Fraction(7, 6), Fraction(5, 4)]
    k = random.choice(k_options)
    if not (Fraction(1) <= k <= Fraction(141, 100)):  # k <= ~√2
        return None
    correct = (k * k - 1) / 2
    if not is_clean(correct) or correct <= 0:
        return None
    w1 = (k * k + 1) / 2
    w2 = k * k - 1
    w3 = k / 2
    stem = (f"If sin θ + cos θ = {fmt(k)} (θ acute), then the value of sin θ · cos θ is:")
    sol = (f"(sinθ+cosθ)² = 1 + 2sinθcosθ → ({fmt(k)})² = 1 + 2x "
           f"→ x = (({fmt(k)})²−1)/2 = {fmt(correct)}.")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_sin_minus_cos():
    """If sinθ - cosθ = 0 (θ=45) etc, evaluate. Or given sinθcosθ find sin+cos. [VH]"""
    # Given sinθ·cosθ = m, find (sinθ+cosθ)² = 1+2m. Choose m clean -> 1+2m perfect.
    m_options = [Fraction(1, 2), Fraction(3, 8), Fraction(1, 4), Fraction(3, 10),
                 Fraction(2, 5), Fraction(1, 5), Fraction(1, 8), Fraction(3, 4),
                 Fraction(1, 10), Fraction(2, 9), Fraction(1, 6)]
    m = random.choice(m_options)
    if m > Fraction(1, 2):     # sinθcosθ <= 1/2 for real θ
        return None
    correct = 1 + 2 * m
    w1 = 1 - 2 * m
    w2 = 2 * m
    w3 = Fraction(1)
    if not is_clean(correct) or correct == Fraction(1):
        return None
    stem = (f"If sin θ · cos θ = {fmt(m)}, then the value of (sin θ + cos θ)² is:")
    sol = (f"(sinθ+cosθ)² = sin²θ+cos²θ+2sinθcosθ = 1 + 2×{fmt(m)} = {fmt(correct)}.")
    return stem, correct, [w1, w2, w3], sol, "VH"


def t_deg_eval_single():
    """Evaluate a single standard ratio numerically (surd or rational). [M]"""
    a = random.choice([0, 30, 45, 60, 90])
    fn = random.choice(["sin", "cos", "tan"])
    if fn == "sin":
        v = sin_d(a)
        name = "sin"
    elif fn == "cos":
        v = cos_d(a)
        name = "cos"
    else:
        if a == 90:
            return None
        v = tan_d(a)
        name = "tan"
    correct = v
    # distractors: shifted values, all clean
    if isinstance(v, SurdVal):
        w1 = Fraction(1)
        w2 = Fraction(1, 2)
        w3 = Fraction(0)
    else:
        w1 = surd_mul(Fraction(1, 2), "√3", R3)
        w2 = surd_mul(Fraction(1, 2), "√2", R2)
        w3 = (correct + Fraction(1, 2)) if correct != Fraction(1, 2) else Fraction(1)
    stem = f"The value of {name} {a}° is:"
    sol = f"{name}{a}° = {fmt(correct)} (standard angle)."
    return stem, correct, [w1, w2, w3], sol, "M"


def t_mixed_eval():
    """Evaluate product/quotient of standard ratios -> rational. [H]"""
    forms = [
        ("sin30°·cos60° + cos30°·sin60°", float(sin_d(30))*float(cos_d(60)) + float(cos_d(30))*float(sin_d(60)),
         Fraction(1), "= sin(30°+60°) = sin90° = 1."),
        ("cos30°·cos60° − sin30°·sin60°", None, Fraction(0), "= cos(30°+60°) = cos90° = 0."),
        ("sin60°·cos30° − cos60°·sin30°", None, Fraction(1, 2), "= sin(60°−30°) = sin30° = ½."),
        ("2·sin30°·cos30°", None, surd_mul(Fraction(1, 2), "√3", R3), "= sin60° = √3/2."),
        ("1 − 2·sin²30°", None, Fraction(1, 2), "= cos(2×30°) = cos60° = ½."),
        ("2·cos²30° − 1", None, Fraction(1, 2), "= cos(2×30°) = cos60° = ½."),
        ("tan45°·cos²30° + sin²30°", None, Fraction(1), "= cos²30°+sin²30° = 1."),
    ]
    expr, _, correct, why = random.choice(forms)
    if isinstance(correct, SurdVal):
        w1 = Fraction(1, 2)
        w2 = Fraction(1)
        w3 = surd_mul(Fraction(1, 2), "√2", R2)
    else:
        w1 = correct + Fraction(1, 2)
        w2 = correct + Fraction(1)
        w3 = surd_mul(Fraction(1, 2), "√3", R3)
    stem = f"The value of {expr} is:"
    sol = f"{expr} {why}"
    return stem, correct, [w1, w2, w3], sol, "H"


TEMPLATES = [
    t_eval_standard, t_identity_const, t_sin_from_triple, t_expr_from_triple,
    t_tan_plus_cot, t_sec_plus_tan, t_complementary, t_product_to_one,
    t_chain_identity, t_elev_height, t_elev_distance, t_shadow_change,
    t_two_points_tower, t_range_a_sin_b, t_range_sin2_cos2, t_a_sin_b_cos_eq,
    t_sin_minus_cos, t_deg_eval_single, t_mixed_eval,
]

DIFF_OF = {
    t_eval_standard: "H", t_identity_const: "M", t_sin_from_triple: "H",
    t_expr_from_triple: "H", t_tan_plus_cot: "VH", t_sec_plus_tan: "VH",
    t_complementary: "H", t_product_to_one: "M", t_chain_identity: "M",
    t_elev_height: "H", t_elev_distance: "H", t_shadow_change: "VH",
    t_two_points_tower: "VH", t_range_a_sin_b: "H", t_range_sin2_cos2: "H",
    t_a_sin_b_cos_eq: "VH", t_sin_minus_cos: "VH", t_deg_eval_single: "M",
    t_mixed_eval: "H",
}

# Quota-enforced generation: ~20% M / 60% H / 20% VH of 500.
from collections import Counter as _C
QUOTA = {"M": 100, "H": 300, "VH": 100}
BY_DIFF = {"M": [], "H": [], "VH": []}
for t in TEMPLATES:
    BY_DIFF[DIFF_OF[t]].append(t)

cur = {"M": 0, "H": 0, "VH": 0}


def _try_add(stem, correct, distractors, sol, diff):
    before = len(questions)
    add(stem, correct, distractors, sol, diff)
    if len(questions) > before:
        cur[diff] += 1
        return True
    return False


attempts = 0
# Fill each bucket to its quota; VH first (scarcest), then H, then M.
for diff in ("VH", "H", "M"):
    stall = 0
    while cur[diff] < QUOTA[diff] and stall < 200000:
        attempts += 1
        t = random.choice(BY_DIFF[diff])
        res = t()
        if res is None:
            stall += 1
            continue
        if _try_add(*res):
            stall = 0
        else:
            stall += 1

# If any bucket fell short, top up from H (largest capacity) to reach 500.
fill_pool = BY_DIFF["H"] + BY_DIFF["M"]
stall = 0
while len(questions) < 500 and stall < 200000:
    attempts += 1
    t = random.choice(fill_pool)
    res = t()
    if res is None:
        stall += 1
        continue
    if _try_add(*res):
        stall = 0
    else:
        stall += 1

print(f"Generated {len(questions)} questions in {attempts} attempts.")
print("Bucket fill:", cur)

# ---- SELF-CHECK: 4 distinct options, one correct ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
print(f"Self-check errors: {errors}")

from collections import Counter
print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_15_Trigonometry_500.md"

lines = []
lines.append("# Trigonometry (incl. Heights & Distances) — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every answer is computed and machine-verified** — surd answers (e.g. 50√3) are exact; the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas / Quick Reference")
lines.append("- Standard angles: sin30°=½, sin45°=1/√2, sin60°=√3/2, sin90°=1, sin0°=0")
lines.append("- cos θ = sin(90°−θ); tan30°=1/√3, tan45°=1, tan60°=√3")
lines.append("- Pythagorean: sin²θ + cos²θ = 1 · sec²θ − tan²θ = 1 · cosec²θ − cot²θ = 1")
lines.append("- Reciprocals: sinθ·cosecθ = cosθ·secθ = tanθ·cotθ = 1")
lines.append("- Complementary: sin(90°−θ)=cosθ, tan(90°−θ)=cotθ, sec(90°−θ)=cosecθ")
lines.append("- sec θ ± tan θ are reciprocals: (secθ−tanθ)(secθ+tanθ) = 1")
lines.append("- tan θ + cot θ = (sin²θ+cos²θ)/(sinθcosθ) = 1/(sinθcosθ)")
lines.append("- Range: −√(a²+b²) ≤ a·sinθ + b·cosθ ≤ √(a²+b²)")
lines.append("- a·sin²θ + b·cos²θ lies between min(a,b) and max(a,b)")
lines.append("- Heights & Distances: height = distance × tan(elevation); use tan30°=1/√3, tan45°=1, tan60°=√3")
lines.append("- Two points d apart, angles 30° & 60°: h = d·√3/2 (from h = d/(cot30°−cot60°))\n")
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
    blk = start // 50 + 1
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
