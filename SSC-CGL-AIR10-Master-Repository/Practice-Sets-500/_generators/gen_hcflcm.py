# -*- coding: utf-8 -*-
"""
SSC CGL HCF & LCM - 500 PYQ-pattern MCQ generator.
Every answer is COMPUTED with math.gcd / lcm helpers, so the key is provably
correct. Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.
Mirrors gen_percentage.py.  NEVER passes a float to Fraction(num, den).
"""
import random
import math
from fractions import Fraction
from functools import reduce

random.seed(20260625)  # deterministic

LETTERS = "abcd"


# ---------------- exact gcd / lcm helpers ----------------
def gcd(*nums):
    return reduce(math.gcd, nums)


def lcm2(a, b):
    return a * b // math.gcd(a, b)


def lcm(*nums):
    return reduce(lcm2, nums)


def fmt(x):
    """Format cleanly: ints as ints, Fractions as p/q (or int if whole)."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
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
        if all(abs(float(d) - float(o)) > 1e-9 for o in opts):
            opts.append(d)
        if len(opts) == 4:
            break
    # pad with plausible filler if needed
    bump = 1
    cf = float(correct)
    while len(opts) < 4:
        step = bump * (correct if float(correct) != 0 else 1)
        cand = correct + (Fraction(bump) if isinstance(correct, Fraction) else bump)
        # bias filler to nearby multiples for HCF/LCM feel
        if isinstance(correct, Fraction):
            cand = correct + Fraction(bump)
        else:
            cand = int(correct) + bump
        if all(abs(float(cand) - float(o)) > 1e-9 for o in opts):
            opts.append(cand)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci


questions = []  # each: dict(stem, opts, ci, sol, diff)
seen = set()


def add(stem, correct, distractors, sol, diff):
    key = stem.strip()
    if key in seen:
        return False
    # normalise to Fraction for comparison/storage
    cfr = correct if isinstance(correct, Fraction) else Fraction(correct)
    dfrs = []
    for d in distractors:
        if d is None:
            continue
        dfr = d if isinstance(d, Fraction) else Fraction(d)
        if dfr != cfr and dfr not in dfrs:
            dfrs.append(dfr)
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


# small helper pools
SMALL = [6, 8, 9, 12, 14, 15, 16, 18, 20, 21, 24, 25, 27, 28, 30, 32,
         35, 36, 40, 42, 45, 48, 50, 54, 56, 60, 63, 64, 70, 72, 75,
         80, 84, 90, 96, 100, 108, 120, 144]


# ---------------- TEMPLATES ----------------

def t_hcf_two():
    """HCF of two numbers. [M]"""
    g = random.choice([4, 6, 8, 9, 12, 14, 15, 16, 18, 21, 24])
    p, q = random.choice([(3, 4), (4, 5), (5, 6), (3, 5), (5, 7), (7, 8),
                          (4, 9), (5, 8), (3, 7), (8, 9)])
    a, b = g * p, g * q
    if a == b:
        return None
    correct = gcd(a, b)
    wrong1 = lcm(a, b)              # gives LCM instead
    wrong2 = abs(a - b)            # difference
    wrong3 = min(a, b)            # smaller number
    stem = f"Find the HCF (GCD) of {a} and {b}."
    sol = (f"{a} = {g}x{p}, {b} = {g}x{q}; the common factor is {correct}. "
           f"So HCF({a},{b}) = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_lcm_two():
    """LCM of two numbers. [M]"""
    a = random.choice(SMALL)
    b = random.choice(SMALL)
    if a == b:
        return None
    correct = lcm(a, b)
    wrong1 = gcd(a, b)             # gives HCF instead
    wrong2 = a * b                 # product (forgets to divide by HCF)
    wrong3 = max(a, b) * 2
    stem = f"Find the LCM of {a} and {b}."
    g = gcd(a, b)
    sol = (f"LCM = (a x b)/HCF = ({a} x {b})/{g} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_hcf_three():
    """HCF of three numbers. [H]"""
    g = random.choice([4, 6, 8, 9, 12, 14, 15, 16, 18])
    p, q, r = random.sample([3, 4, 5, 7, 8, 9, 11], 3)
    a, b, c = g * p, g * q, g * r
    correct = gcd(a, b, c)
    wrong1 = lcm(a, b, c)
    wrong2 = gcd(a, b)            # only two of them
    wrong3 = min(a, b, c)
    stem = f"Find the HCF of {a}, {b} and {c}."
    sol = (f"Common factor of {a}, {b}, {c} = {correct}. "
           f"(Each is {correct} times a co-prime quotient.) HCF = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_lcm_three():
    """LCM of three numbers. [H]"""
    a, b, c = random.sample([6, 8, 9, 12, 14, 15, 16, 18, 20, 21, 24, 25,
                             27, 28, 30, 32, 35, 36, 40, 45], 3)
    correct = lcm(a, b, c)
    wrong1 = gcd(a, b, c)
    wrong2 = lcm(a, b)           # only two
    wrong3 = a * b * c // gcd(a, b, c)
    stem = f"Find the LCM of {a}, {b} and {c}."
    sol = (f"LCM({a}, {b}, {c}) = {correct} (take each prime to its highest power).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_product_hcf_lcm():
    """Product of two numbers = HCF x LCM; given product/HCF/LCM and one num. [H]"""
    g = random.choice([3, 4, 6, 8, 9, 12, 15, 16])
    p, q = random.choice([(4, 5), (5, 7), (7, 9), (5, 8), (8, 9), (7, 11),
                          (4, 7), (9, 11), (5, 9)])
    a, b = g * p, g * q
    H = gcd(a, b)
    L = lcm(a, b)
    # given HCF, LCM, and one number -> find the other
    correct = b
    wrong1 = H * L // a + 1
    wrong2 = L // a
    wrong3 = H * a // L if L != 0 else a + 2
    stem = (f"The HCF and LCM of two numbers are {H} and {L} respectively. "
            f"If one of the numbers is {a}, find the other number.")
    sol = (f"Product of two numbers = HCF x LCM = {H} x {L} = {H*L}. "
           f"Other number = {H*L}/{a} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_product_given():
    """Product of two numbers and HCF given -> find LCM. [H]"""
    g = random.choice([3, 4, 6, 8, 9, 12])
    p, q = random.choice([(4, 5), (5, 7), (7, 9), (5, 8), (8, 9), (4, 7)])
    a, b = g * p, g * q
    H = gcd(a, b)
    prod = a * b
    correct = prod // H            # = LCM
    wrong1 = prod * H
    wrong2 = prod // (H * H) if prod % (H * H) == 0 else prod - H
    wrong3 = H * 2
    stem = (f"The product of two numbers is {prod} and their HCF is {H}. "
            f"Find their LCM.")
    sol = (f"LCM = product/HCF = {prod}/{H} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_coprime_ratio_lcm():
    """Two numbers are in ratio p:q with HCF h -> find LCM. [H]"""
    h = random.choice([3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15])
    p, q = random.choice([(2, 3), (3, 4), (4, 5), (3, 5), (5, 7), (5, 6),
                          (7, 8), (2, 5), (3, 7), (4, 7)])
    a, b = h * p, h * q
    correct = lcm(a, b)           # = h*p*q
    wrong1 = h * p * q + h
    wrong2 = h * (p + q)
    wrong3 = h * h * p * q
    stem = (f"Two numbers are in the ratio {p}:{q} and their HCF is {h}. "
            f"Find their LCM.")
    sol = (f"Numbers are {h}x{p}={a} and {h}x{q}={b} (since p, q are co-prime). "
           f"LCM = {h} x {p} x {q} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_coprime_ratio_sum():
    """Two numbers in ratio p:q with HCF h -> find their sum. [M]"""
    h = random.choice([4, 5, 6, 7, 8, 9, 11, 12, 13, 14])
    p, q = random.choice([(2, 3), (3, 4), (4, 5), (3, 5), (5, 7), (5, 6),
                          (7, 9), (2, 7), (3, 8)])
    a, b = h * p, h * q
    correct = a + b
    wrong1 = abs(a - b)
    wrong2 = h * p * q          # LCM instead
    wrong3 = a * b
    stem = (f"Two numbers are in the ratio {p}:{q}. If their HCF is {h}, "
            f"find the sum of the two numbers.")
    sol = (f"Numbers = {h}x{p}={a} and {h}x{q}={b}. Sum = {a}+{b} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_largest_divides_remainders():
    """Largest number dividing a,b,c leaving remainders r1,r2,r3 = HCF of (a-r1),(b-r2),(c-r3). [VH]"""
    g = random.choice([7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 23])
    m1, m2, m3 = random.sample(range(3, 14), 3)
    r1 = random.randint(1, g - 1)
    r2 = random.randint(1, g - 1)
    r3 = random.randint(1, g - 1)
    a, b, c = g * m1 + r1, g * m2 + r2, g * m3 + r3
    diffs = (a - r1, b - r2, c - r3)
    correct = gcd(*diffs)
    if correct <= max(r1, r2, r3):
        return None
    wrong1 = gcd(a, b, c)              # forgets remainders
    wrong2 = gcd(a - r1, b - r2)       # only two
    wrong3 = correct + 1
    stem = (f"Find the greatest number that divides {a}, {b} and {c} leaving "
            f"remainders {r1}, {r2} and {r3} respectively.")
    sol = (f"Subtract the remainders: {a}-{r1}={a-r1}, {b}-{r2}={b-r2}, "
           f"{c}-{r3}={c-r3}. Required number = HCF({a-r1}, {b-r2}, {c-r3}) = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_largest_same_remainder():
    """Largest number dividing a,b,c leaving the SAME remainder = HCF of pairwise differences. [VH]"""
    g = random.choice([7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 23])
    m1, m2, m3 = sorted(random.sample(range(4, 16), 3))
    r = random.randint(1, g - 1)
    a, b, c = g * m1 + r, g * m2 + r, g * m3 + r
    diffs = (b - a, c - b, c - a)
    correct = gcd(*diffs)
    if correct <= r:
        return None
    wrong1 = gcd(a, b, c)
    wrong2 = b - a
    wrong3 = correct + 2
    stem = (f"Find the greatest number which divides {a}, {b} and {c} leaving "
            f"the same remainder in each case.")
    sol = (f"Required number = HCF of the differences = HCF({b}-{a}, {c}-{b}, "
           f"{c}-{a}) = HCF({b-a}, {c-b}, {c-a}) = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_smallest_same_remainder():
    """Smallest number which when divided by a,b,c leaves remainder r each = LCM + r. [H]"""
    nums = random.sample([6, 8, 9, 12, 15, 16, 18, 20, 24], 3)
    a, b, c = nums
    L = lcm(a, b, c)
    r = random.choice([1, 2, 3, 4, 5, 7])
    if r >= min(nums):
        return None
    correct = L + r
    wrong1 = L                    # forgets +r
    wrong2 = L - r
    wrong3 = lcm(a, b) + r        # only two
    stem = (f"Find the least number which when divided by {a}, {b} and {c} "
            f"leaves a remainder {r} in each case.")
    sol = (f"LCM({a}, {b}, {c}) = {L}. The required number = LCM + remainder "
           f"= {L} + {r} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_smallest_common_diff():
    """Smallest number divided by a,b,c leaves remainders (a-k),(b-k),(c-k) = LCM - k. [VH]"""
    nums = random.sample([6, 8, 9, 12, 15, 16, 18, 20, 24], 3)
    a, b, c = nums
    L = lcm(a, b, c)
    k = random.choice([1, 2, 3, 4, 5])
    if k >= min(nums):
        return None
    correct = L - k
    wrong1 = L                    # forgets -k
    wrong2 = L + k
    wrong3 = lcm(a, b) - k
    ra, rb, rc = a - k, b - k, c - k
    stem = (f"Find the least number which when divided by {a}, {b} and {c} "
            f"leaves remainders {ra}, {rb} and {rc} respectively.")
    sol = (f"The remainders are each {k} less than the divisor "
           f"({a}-{k}={ra}, {b}-{k}={rb}, {c}-{k}={rc}). So required number "
           f"= LCM({a}, {b}, {c}) - {k} = {L} - {k} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_bells_toll():
    """Bells toll together every LCM seconds; how many times in T minutes (incl. start). [H]"""
    nums = random.sample([2, 3, 4, 5, 6, 8, 9, 10, 12, 15], random.choice([3, 4]))
    L = lcm(*nums)
    Tmin = random.choice([30, 36, 42, 48, 54, 60, 72, 90])
    Tsec = Tmin * 60
    if Tsec % L != 0:
        return None
    times = Tsec // L + 1          # including the start
    correct = times
    wrong1 = Tsec // L            # forgets the initial toll
    wrong2 = times + 1
    wrong3 = L
    nlist = ", ".join(str(n) for n in nums)
    stem = (f"Several bells toll at intervals of {nlist} seconds respectively. "
            f"If they all toll together at the start, how many times will they "
            f"toll together in {Tmin} minutes (including the start)?")
    sol = (f"They toll together every LCM({nlist}) = {L} seconds. In "
           f"{Tmin} min = {Tsec} s, count = {Tsec}/{L} + 1 (for the start) = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_fraction_hcf():
    """HCF of fractions = HCF(numerators)/LCM(denominators). [VH]"""
    a1, a2 = random.sample([2, 3, 4, 5, 6, 8, 9, 10, 12], 2)
    b1, b2 = random.sample([3, 4, 5, 6, 7, 8, 9, 10], 2)
    n = gcd(a1, a2)
    d = lcm(b1, b2)
    correct = Fraction(n, d)
    wrong1 = Fraction(lcm(a1, a2), gcd(b1, b2))     # swapped (this is LCM of fractions)
    wrong2 = Fraction(gcd(a1, a2), gcd(b1, b2))
    wrong3 = Fraction(lcm(a1, a2), lcm(b1, b2))
    stem = (f"Find the HCF of the fractions {a1}/{b1} and {a2}/{b2}.")
    sol = (f"HCF of fractions = HCF(numerators)/LCM(denominators) "
           f"= HCF({a1},{a2})/LCM({b1},{b2}) = {n}/{d} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_fraction_lcm():
    """LCM of fractions = LCM(numerators)/HCF(denominators). [VH]"""
    a1, a2 = random.sample([2, 3, 4, 5, 6, 8, 9, 10], 2)
    b1, b2 = random.sample([3, 4, 5, 6, 7, 8, 9], 2)
    n = lcm(a1, a2)
    d = gcd(b1, b2)
    correct = Fraction(n, d)
    wrong1 = Fraction(gcd(a1, a2), lcm(b1, b2))     # swapped (HCF of fractions)
    wrong2 = Fraction(lcm(a1, a2), lcm(b1, b2))
    wrong3 = Fraction(gcd(a1, a2), gcd(b1, b2))
    stem = (f"Find the LCM of the fractions {a1}/{b1} and {a2}/{b2}.")
    sol = (f"LCM of fractions = LCM(numerators)/HCF(denominators) "
           f"= LCM({a1},{a2})/HCF({b1},{b2}) = {n}/{d} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_greatest_tape():
    """Greatest length of tape that measures given lengths exactly = HCF. [H]"""
    g = random.choice([3, 4, 5, 6, 7, 8, 9, 12, 15])
    p, q, r = random.sample([4, 5, 7, 8, 9, 11, 13], 3)
    a, b, c = g * p, g * q, g * r
    correct = gcd(a, b, c)
    wrong1 = lcm(a, b, c)
    wrong2 = gcd(a, b)
    wrong3 = min(a, b, c)
    stem = (f"Find the greatest possible length (in cm) of a measuring tape that "
            f"can measure the lengths {a} cm, {b} cm and {c} cm exactly.")
    sol = (f"Greatest exact measuring length = HCF({a}, {b}, {c}) = {correct} cm.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_square_tiles():
    """Least number of square tiles to pave a floor LxB = (L*B)/HCF(L,B)^2. [VH]"""
    g = random.choice([2, 3, 4, 5, 6, 7, 8])
    p, q = random.choice([(3, 5), (4, 7), (5, 8), (3, 7), (4, 9), (5, 9),
                          (6, 7), (3, 8), (5, 6)])
    L, B = g * p, g * q
    side = gcd(L, B)
    correct = (L * B) // (side * side)
    wrong1 = (L * B) // side          # divides once only
    wrong2 = L * B // lcm(L, B)
    wrong3 = p * q + 1
    stem = (f"What is the least number of square tiles required to pave the "
            f"floor of a room {L} cm long and {B} cm broad?")
    sol = (f"Largest square tile side = HCF({L}, {B}) = {side} cm. "
           f"Number of tiles = ({L} x {B})/({side} x {side}) = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_hcf_lcm_one_number():
    """Find a number given HCF, LCM and the other number. [H]"""
    g = random.choice([4, 6, 8, 9, 12, 15, 16, 18])
    p, q = random.choice([(5, 7), (7, 9), (5, 8), (8, 9), (4, 7), (9, 11), (5, 9)])
    a, b = g * p, g * q
    H = gcd(a, b)
    L = lcm(a, b)
    correct = a
    wrong1 = L // b + 1
    wrong2 = H * b
    wrong3 = L - b
    stem = (f"The HCF of two numbers is {H} and their LCM is {L}. "
            f"If one number is {b}, the other number is:")
    sol = (f"a x b = HCF x LCM = {H} x {L} = {H*L}. "
           f"Other = {H*L}/{b} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_greatest_divides_exactly():
    """Greatest number that divides a, b, c exactly = HCF. [M]"""
    g = random.choice([6, 8, 9, 12, 14, 15, 16, 18, 21, 24])
    p, q, r = random.sample([2, 3, 4, 5, 7, 8, 9, 11], 3)
    a, b, c = g * p, g * q, g * r
    correct = gcd(a, b, c)
    wrong1 = lcm(a, b, c)
    wrong2 = gcd(a, b)
    wrong3 = min(a, b, c)
    stem = (f"What is the greatest number that divides {a}, {b} and {c} exactly "
            f"(leaving no remainder)?")
    sol = (f"Greatest exact divisor = HCF({a}, {b}, {c}) = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_smallest_divisible():
    """Least number exactly divisible by a, b, c = LCM. [M]"""
    nums = random.sample([6, 8, 9, 12, 14, 15, 16, 18, 20, 21, 24], 3)
    a, b, c = nums
    correct = lcm(a, b, c)
    wrong1 = gcd(a, b, c)
    wrong2 = a * b * c
    wrong3 = lcm(a, b)
    stem = (f"Find the least number which is exactly divisible by {a}, {b} and {c}.")
    sol = (f"Least number divisible by all = LCM({a}, {b}, {c}) = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


TEMPLATES = [
    t_hcf_two, t_lcm_two, t_hcf_three, t_lcm_three, t_product_hcf_lcm,
    t_product_given, t_coprime_ratio_lcm, t_coprime_ratio_sum,
    t_largest_divides_remainders, t_largest_same_remainder,
    t_smallest_same_remainder, t_smallest_common_diff, t_bells_toll,
    t_fraction_hcf, t_fraction_lcm, t_greatest_tape, t_square_tiles,
    t_hcf_lcm_one_number, t_greatest_divides_exactly, t_smallest_divisible,
]

DIFF_OF = {
    t_hcf_two: "M", t_lcm_two: "M", t_hcf_three: "H", t_lcm_three: "H",
    t_product_hcf_lcm: "H", t_product_given: "H", t_coprime_ratio_lcm: "H",
    t_coprime_ratio_sum: "M", t_largest_divides_remainders: "VH",
    t_largest_same_remainder: "VH", t_smallest_same_remainder: "H",
    t_smallest_common_diff: "VH", t_bells_toll: "H", t_fraction_hcf: "VH",
    t_fraction_lcm: "VH", t_greatest_tape: "H", t_square_tiles: "VH",
    t_hcf_lcm_one_number: "H", t_greatest_divides_exactly: "M",
    t_smallest_divisible: "M",
}
# Target ~20% M / 60% H / 20% VH. Use hard per-difficulty quotas rather than
# pure weighting, because the VH templates have huge unique spaces and would
# otherwise dominate while the M pool saturates early.
QUOTA = {"M": 100, "H": 300, "VH": 100}
POOL_BY_DIFF = {"M": [], "H": [], "VH": []}
for t in TEMPLATES:
    POOL_BY_DIFF[DIFF_OF[t]].append(t)

count_by_diff = {"M": 0, "H": 0, "VH": 0}


def need_diffs():
    return [d for d in ("M", "H", "VH") if count_by_diff[d] < QUOTA[d]]


# Generate until we have 500 unique, honouring per-difficulty quotas
attempts = 0
while len(questions) < 500 and attempts < 1000000:
    attempts += 1
    avail = need_diffs()
    if not avail:
        break
    d = random.choice(avail)
    t = random.choice(POOL_BY_DIFF[d])
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    before = len(questions)
    if add(stem, correct, distractors, sol, diff):
        if len(questions) > before:
            count_by_diff[diff] += 1

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- VERIFY: each has exactly 4 distinct options, exactly one correct ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options")
        errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}")
        errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index")
        errors += 1
print(f"Verification errors: {errors}")

from collections import Counter
print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_11_HCF_LCM_500.md"

lines = []
lines.append("# HCF & LCM — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- **Product of two numbers = HCF × LCM** → other number = (HCF × LCM)/one number")
lines.append("- LCM(a, b) = (a × b)/HCF(a, b)")
lines.append("- Numbers in ratio p:q (co-prime) with HCF h → numbers are hp, hq; LCM = h·p·q")
lines.append("- Greatest number dividing a, b, c leaving remainders r1, r2, r3 = **HCF(a−r1, b−r2, c−r3)**")
lines.append("- Greatest number dividing a, b, c leaving the **same** remainder = **HCF of the differences**")
lines.append("- Least number leaving remainder r when divided by a, b, c = **LCM(a,b,c) + r**")
lines.append("- Least number leaving remainders (a−k),(b−k),(c−k) = **LCM(a,b,c) − k**")
lines.append("- HCF of fractions = **HCF(numerators)/LCM(denominators)**")
lines.append("- LCM of fractions = **LCM(numerators)/HCF(denominators)**")
lines.append("- Bells toll together every LCM seconds; count in T = T/LCM + 1 (include the start)")
lines.append("- Least square tiles for L×B floor = (L×B)/HCF(L,B)²\n")
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
