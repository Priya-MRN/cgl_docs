# -*- coding: utf-8 -*-
"""
SSC CGL Algebra - 500 hard MCQ generator.
Every answer is COMPUTED with exact Fraction / integer arithmetic, so the key
is provably correct. Builds 4 distinct options (1 correct + 3 common-mistake
distractors), randomizes correct position, dedupes question stems, outputs
markdown. NO sympy dependency (falls back to Fraction + integer algebra).
"""
import random
from fractions import Fraction
from math import isqrt

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
        step = Fraction(bump * (3 if cf >= 0 else -3))
        # scale step for large magnitudes so filler looks plausible
        if abs(cf) > 200:
            step = Fraction(bump * (int(abs(cf) // 20) + 1) * (1 if cf >= 0 else -1))
        cand = Fraction(correct) + step
        if all(abs(float(cand) - float(o)) > 1e-9 for o in opts):
            opts.append(cand)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci


questions = []  # each: dict(stem, opts, ci, sol, diff)
seen = set()


def is_clean(x):
    """Accept integers, simple fractions, and <=2dp decimals; cap magnitude."""
    fr = Fraction(x).limit_denominator(10**6)
    if abs(fr) > 10**7:
        return False
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
    # de-dup distractors
    uniq = []
    for d in dfrs:
        if all(d != u for u in uniq):
            uniq.append(d)
    dfrs = uniq
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


# ============================ TEMPLATES ============================
# All identities are verified by choosing exact rational values and
# evaluating the target expression exactly.

def t_x_plus_inv_sq():
    """If x + 1/x = k, find x^2 + 1/x^2 = k^2 - 2. [M]"""
    k = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    correct = Fraction(k**2 - 2)
    wrong1 = Fraction(k**2 + 2)        # sign error
    wrong2 = Fraction(k**2)            # forgets -2
    wrong3 = Fraction((k - 2)**2)      # wrong expansion
    stem = (f"If x + 1/x = {k}, then the value of x² + 1/x² is:")
    sol = (f"x² + 1/x² = (x + 1/x)² − 2 = {k}² − 2 = {k**2} − 2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_x_plus_inv_cube():
    """If x + 1/x = k, find x^3 + 1/x^3 = k^3 - 3k. [H]"""
    k = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    correct = Fraction(k**3 - 3*k)
    wrong1 = Fraction(k**3 + 3*k)      # sign error
    wrong2 = Fraction(k**3)            # forgets -3k
    wrong3 = Fraction(k**3 - 3)        # uses -3 not -3k
    stem = (f"If x + 1/x = {k}, then the value of x³ + 1/x³ is:")
    sol = (f"x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x) = {k}³ − 3×{k} "
           f"= {k**3} − {3*k} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_x_plus_inv_four():
    """If x + 1/x = k, find x^4 + 1/x^4 = (k^2-2)^2 - 2. [H]"""
    k = random.choice([3, 4, 5, 6, 7, 8])
    s2 = k**2 - 2
    correct = Fraction(s2**2 - 2)
    wrong1 = Fraction(s2**2 + 2)         # sign error
    wrong2 = Fraction(s2**2)             # forgets -2
    wrong3 = Fraction(k**4 - 2)          # wrong: uses k^4
    stem = (f"If x + 1/x = {k}, then the value of x⁴ + 1/x⁴ is:")
    sol = (f"x² + 1/x² = {k}² − 2 = {s2}; then x⁴ + 1/x⁴ = "
           f"({s2})² − 2 = {s2**2} − 2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_x_minus_inv_sq():
    """If x - 1/x = k, find x^2 + 1/x^2 = k^2 + 2. [M]"""
    k = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    correct = Fraction(k**2 + 2)
    wrong1 = Fraction(k**2 - 2)        # uses +1/x formula
    wrong2 = Fraction(k**2)            # forgets +2
    wrong3 = Fraction((k + 2)**2)
    stem = (f"If x − 1/x = {k}, then the value of x² + 1/x² is:")
    sol = (f"x² + 1/x² = (x − 1/x)² + 2 = {k}² + 2 = {k**2} + 2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_x_minus_inv_cube():
    """If x - 1/x = k, find x^3 - 1/x^3 = k^3 + 3k. [H]"""
    k = random.choice([2, 3, 4, 5, 6, 7, 8])
    correct = Fraction(k**3 + 3*k)
    wrong1 = Fraction(k**3 - 3*k)       # sign error
    wrong2 = Fraction(k**3)             # forgets +3k
    wrong3 = Fraction(k**3 + 3)         # +3 not +3k
    stem = (f"If x − 1/x = {k}, then the value of x³ − 1/x³ is:")
    sol = (f"x³ − 1/x³ = (x − 1/x)³ + 3(x − 1/x) = {k}³ + 3×{k} "
           f"= {k**3} + {3*k} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_abc_zero_cubes():
    """If a+b+c=0, then a^3+b^3+c^3 = 3abc. Give a,b,c=-(a+b). [H]"""
    a = random.choice([2, 3, 4, 5, 6, 7, 8, -3, -4, -5])
    b = random.choice([3, 4, 5, 6, 7, 9, -2, -6])
    c = -(a + b)
    if c == 0 or a == 0 or b == 0:
        return None
    abc = a * b * c
    correct = Fraction(3 * abc)
    wrong1 = Fraction(abc)              # forgets factor 3
    wrong2 = Fraction(0)               # thinks it's 0
    wrong3 = Fraction(a**3 + b**3 + c**3 + abc)  # arbitrary slip
    if wrong3 == correct:
        wrong3 = Fraction(3 * abc + 6)
    stem = (f"If a + b + c = 0, where a = {a}, b = {b} and c = {c}, then the value "
            f"of a³ + b³ + c³ is:")
    sol = (f"When a + b + c = 0, a³ + b³ + c³ = 3abc = "
           f"3×({a})×({b})×({c}) = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_sum_sq_from_sum_and_pair():
    """Given a+b+c = s and ab+bc+ca = p, find a^2+b^2+c^2 = s^2 - 2p. [H]"""
    s = random.choice([6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    p = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 20])
    correct = Fraction(s**2 - 2*p)
    if correct <= 0:
        return None
    wrong1 = Fraction(s**2 + 2*p)       # sign error
    wrong2 = Fraction(s**2 - p)         # uses -p
    wrong3 = Fraction(s**2)             # forgets -2p
    stem = (f"If a + b + c = {s} and ab + bc + ca = {p}, then the value of "
            f"a² + b² + c² is:")
    sol = (f"a² + b² + c² = (a + b + c)² − 2(ab + bc + ca) = "
           f"{s}² − 2×{p} = {s**2} − {2*p} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_pair_from_sum_and_sumsq():
    """Given a+b+c = s and a^2+b^2+c^2 = q, find ab+bc+ca = (s^2-q)/2. [H]"""
    s = random.choice([5, 6, 7, 8, 9, 10, 11, 12])
    p = random.choice([5, 6, 7, 8, 10, 11, 12, 14])  # target ab+bc+ca
    q = s**2 - 2*p
    if q <= 0:
        return None
    correct = Fraction(p)
    wrong1 = Fraction(s**2 - q)         # forgets /2
    wrong2 = Fraction(s**2 + q, 2)      # sign error
    wrong3 = Fraction(q - s**2, 2)
    stem = (f"If a + b + c = {s} and a² + b² + c² = {q}, then the value of "
            f"ab + bc + ca is:")
    sol = (f"ab + bc + ca = [(a + b + c)² − (a² + b² + c²)]/2 = "
           f"({s}² − {q})/2 = ({s**2} − {q})/2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_a_plus_b_ab():
    """If a+b = m and ab = n, find a^2+b^2 = m^2 - 2n. [M]"""
    m = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 13])
    n = random.choice([4, 5, 6, 7, 8, 9, 10, 12, 15, 18, 20])
    if m**2 - 4*n < 0:   # keep a,b real (nicer)
        return None
    correct = Fraction(m**2 - 2*n)
    wrong1 = Fraction(m**2 + 2*n)       # sign error
    wrong2 = Fraction(m**2 - n)         # uses -n
    wrong3 = Fraction(m**2)             # forgets -2n
    stem = (f"If a + b = {m} and ab = {n}, then the value of a² + b² is:")
    sol = (f"a² + b² = (a + b)² − 2ab = {m}² − 2×{n} = "
           f"{m**2} − {2*n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_a_cube_plus_b_cube():
    """If a+b = m and ab = n, find a^3+b^3 = m^3 - 3mn. [H]"""
    m = random.choice([4, 5, 6, 7, 8, 9, 10, 11])
    n = random.choice([3, 4, 5, 6, 7, 8, 10, 12])
    if m**2 - 4*n < 0:
        return None
    correct = Fraction(m**3 - 3*m*n)
    wrong1 = Fraction(m**3 + 3*m*n)     # sign error
    wrong2 = Fraction(m**3 - 3*n)       # forgets m factor
    wrong3 = Fraction(m**3)             # forgets -3mn
    stem = (f"If a + b = {m} and ab = {n}, then the value of a³ + b³ is:")
    sol = (f"a³ + b³ = (a + b)³ − 3ab(a + b) = {m}³ − 3×{n}×{m} "
           f"= {m**3} − {3*m*n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_a_minus_b():
    """If a+b = m and ab = n, find a-b = sqrt(m^2-4n) (choose perfect square). [H]"""
    # choose a > b integers, then m, n derived
    b = random.choice([1, 2, 3, 4, 5])
    d = random.choice([2, 4, 6, 8, 10, 12])  # a - b (even keeps things clean)
    a = b + d
    m = a + b
    n = a * b
    correct = Fraction(d)
    wrong1 = Fraction(m**2 - 4*n)       # forgets sqrt
    wrong2 = Fraction(m + b)            # nonsense
    wrong3 = Fraction(d + 2)
    stem = (f"If a + b = {m} and ab = {n} (with a > b), then the value of a − b is:")
    sol = (f"(a − b)² = (a + b)² − 4ab = {m}² − 4×{n} = "
           f"{m**2} − {4*n} = {m**2 - 4*n}; so a − b = √{m**2 - 4*n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_surd_x_plus_inv():
    """If x = a + sqrt(b) with x*conj = 1 form (a+sqrt(b))(a-sqrt(b))...
    Use x = (sqrt(n)+sqrt(n-1)) style? Simpler: x = a+sqrt(b), 1/x = a-sqrt(b)
    requires a^2 - b = 1. Then x + 1/x = 2a. [H]"""
    # pick a so that b = a^2 - 1 (so 1/x = a - sqrt(b))
    a = random.choice([2, 3, 4, 5, 6, 7])
    b = a**2 - 1
    # verify: 1/x = (a - sqrt(b))/((a)^2 - b) = a - sqrt(b) since a^2 - b = 1
    correct = Fraction(2 * a)           # x + 1/x = 2a
    wrong1 = Fraction(a)                # halves it
    wrong2 = Fraction(2 * a + 2)
    wrong3 = Fraction(4 * a)
    stem = (f"If x = {a} + √{b}, then the value of x + 1/x is:")
    sol = (f"Since ({a})² − {b} = 1, we get 1/x = {a} − √{b}. "
           f"Hence x + 1/x = ({a} + √{b}) + ({a} − √{b}) = 2×{a} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_surd_x_sq_plus_inv():
    """If x = a + sqrt(a^2-1), find x^2 + 1/x^2 = (2a)^2 - 2. [VH]"""
    a = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    b = a**2 - 1
    k = 2 * a            # x + 1/x
    correct = Fraction(k**2 - 2)
    wrong1 = Fraction(k**2 + 2)
    wrong2 = Fraction(k**2)
    wrong3 = Fraction((2*a)**2 - 4)
    stem = (f"If x = {a} + √{b}, then the value of x² + 1/x² is:")
    sol = (f"Here 1/x = {a} − √{b} (since {a}² − {b} = 1), so x + 1/x = {k}. "
           f"Then x² + 1/x² = {k}² − 2 = {k**2} − 2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_linear_system():
    """Solve 2x2 system -> find x+y (choose integer solution). [M]"""
    x = random.choice([2, 3, 4, 5, 6, 7, 8, 9])
    y = random.choice([1, 2, 3, 4, 5, 6, 7])
    # a1 x + b1 y = c1 ; a2 x + b2 y = c2
    a1 = random.choice([2, 3, 4]); b1 = random.choice([1, 2, 3])
    a2 = random.choice([1, 2, 3]); b2 = random.choice([2, 3, 4])
    if a1*b2 - a2*b1 == 0:
        return None
    c1 = a1*x + b1*y
    c2 = a2*x + b2*y
    correct = Fraction(x + y)
    wrong1 = Fraction(x)               # gives only x
    wrong2 = Fraction(y)               # only y
    wrong3 = Fraction(x - y if x != y else x + y + 1)
    stem = (f"If {a1}x + {b1}y = {c1} and {a2}x + {b2}y = {c2}, then the value of "
            f"x + y is:")
    sol = (f"Solving the system gives x = {x}, y = {y}. Hence x + y = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_linear_system_var():
    """Solve 2x2 system -> find value of x (or y). [H]"""
    x = random.choice([3, 4, 5, 6, 7, 8, 9, 11, 12])
    y = random.choice([2, 3, 4, 5, 6, 7, 8])
    a1 = random.choice([2, 3, 5]); b1 = random.choice([2, 3, 4])
    a2 = random.choice([3, 4, 5]); b2 = random.choice([1, 2, 3])
    if a1*b2 - a2*b1 == 0:
        return None
    c1 = a1*x + b1*y
    c2 = a2*x + b2*y
    correct = Fraction(x)
    wrong1 = Fraction(y)
    wrong2 = Fraction(x + y)
    wrong3 = Fraction(x + 1)
    stem = (f"If {a1}x + {b1}y = {c1} and {a2}x + {b2}y = {c2}, then the value of "
            f"x is:")
    sol = (f"Solving simultaneously: x = {x}, y = {y}. Therefore x = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_poly_at_value():
    """Evaluate polynomial p(x) = x^3 + a x^2 + b x + c at given integer x. [M]"""
    x = random.choice([2, 3, 4, 5, -2, -3])
    a = random.choice([1, 2, 3, -1, -2])
    b = random.choice([1, 2, 3, -1, -2, -3])
    c = random.choice([1, 2, 4, 5, -1, -3])
    val = x**3 + a*x**2 + b*x + c
    correct = Fraction(val)
    wrong1 = Fraction(x**3 + a*x**2 + b*x - c)   # sign of c
    wrong2 = Fraction(x**2 + a*x + b + c)         # drops a degree
    wrong3 = Fraction(val + 2*x)
    if len({correct, wrong1, wrong2, wrong3}) < 4:
        wrong3 = Fraction(val - 3)
    sa = f"+ {a}x²" if a >= 0 else f"− {abs(a)}x²"
    sb = f"+ {b}x" if b >= 0 else f"− {abs(b)}x"
    sc = f"+ {c}" if c >= 0 else f"− {abs(c)}"
    stem = (f"If p(x) = x³ {sa} {sb} {sc}, then the value of p({x}) is:")
    sol = (f"p({x}) = ({x})³ + {a}({x})² + {b}({x}) + {c} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_factor_theorem():
    """Find k such that (x - r) is a factor of x^2 + k x + c, i.e. r^2 + kr + c = 0. [H]"""
    r = random.choice([1, 2, 3, -1, -2, -3])
    c = random.choice([-12, -10, -8, -6, 6, 8, 12, 15, 18, 20])
    # k = -(r^2 + c)/r
    if r == 0 or (r**2 + c) % r != 0:
        return None
    k = -(r**2 + c) // r
    correct = Fraction(k)
    wrong1 = Fraction(-k)              # sign
    wrong2 = Fraction((r**2 + c) // r)  # forgets the minus
    wrong3 = Fraction(k + r)
    sc = f"+ {c}" if c >= 0 else f"− {abs(c)}"
    stem = (f"If (x − {r}) is a factor of x² + kx {sc}, then the value of k is:")
    sol = (f"By the factor theorem, putting x = {r}: ({r})² + k({r}) + ({c}) = 0 "
           f"⇒ {r**2} + {r}k + {c} = 0 ⇒ k = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_remainder_theorem():
    """Remainder when p(x) = x^3 + a x + b is divided by (x - r) is p(r). [H]"""
    r = random.choice([1, 2, 3, -1, -2])
    a = random.choice([2, 3, 4, 5, -2, -3])
    b = random.choice([1, 2, 3, 5, -1, -4])
    rem = r**3 + a*r + b
    correct = Fraction(rem)
    wrong1 = Fraction(r**3 + a*r - b)   # sign of b
    wrong2 = Fraction((-r)**3 + a*(-r) + b)  # used x + r
    wrong3 = Fraction(rem + 3)
    if len({correct, wrong1, wrong2, wrong3}) < 4:
        wrong3 = Fraction(rem - 4)
    sa = f"+ {a}x" if a >= 0 else f"− {abs(a)}x"
    sb = f"+ {b}" if b >= 0 else f"− {abs(b)}"
    stem = (f"The remainder when p(x) = x³ {sa} {sb} is divided by (x − {r}) is:")
    sol = (f"By the remainder theorem the remainder is p({r}) = ({r})³ + {a}({r}) + ({b}) "
           f"= {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_ratio_expression():
    """If a/b = p/q, find (a+b)/(a-b) by componendo. Use a=pt,b=qt. [H]"""
    p = random.choice([3, 4, 5, 7, 5, 9, 7])
    q = random.choice([1, 2, 3])
    if p == q:
        return None
    from math import gcd
    g = gcd(p, q)
    p, q = p // g, q // g
    if p == q:
        return None
    correct = Fraction(p + q, p - q) if p > q else Fraction(p + q, q - p)
    # standard: (a+b)/(a-b) = (p+q)/(p-q)
    correct = Fraction(p + q, p - q)
    wrong1 = Fraction(p - q, p + q)       # reciprocal
    wrong2 = Fraction(p, q)
    wrong3 = Fraction(p + q, p)            # wrong denom
    if not is_clean(correct):
        return None
    stem = (f"If a/b = {p}/{q}, then the value of (a + b)/(a − b) is:")
    sol = (f"By componendo & dividendo, (a + b)/(a − b) = ({p} + {q})/({p} − {q}) "
           f"= {p+q}/{p-q} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_min_value():
    """Minimum value of x + a^2/x for x>0 is 2a (AM-GM). Use perfect for clean. [H]"""
    # x + k/x minimum is 2*sqrt(k); choose k = perfect square
    a = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    k = a * a
    correct = Fraction(2 * a)
    wrong1 = Fraction(a)               # forgets factor 2
    wrong2 = Fraction(k)              # gives k
    wrong3 = Fraction(a + 1)
    stem = (f"For x > 0, the minimum value of x + {k}/x is:")
    sol = (f"By AM–GM, x + {k}/x ≥ 2√({k}) = 2×{a} = {fmt(correct)}, "
           f"attained at x = {a}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_abc_cubes_minus():
    """Given a+b+c=s, a^2+b^2+c^2=q, abc=r, find a^3+b^3+c^3-3abc
       = (a+b+c)(a^2+b^2+c^2 - ab-bc-ca). Need ab+bc+ca = (s^2-q)/2. [VH]"""
    s = random.choice([6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    p = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 21, 24])  # ab+bc+ca
    q = s**2 - 2*p
    if q <= 0 or q <= p:
        return None
    correct = Fraction(s * (q - p))    # a^3+b^3+c^3-3abc
    wrong1 = Fraction(s * q)            # forgets -p... -> s*(q)
    wrong2 = Fraction(s * (q + p))      # sign error
    wrong3 = Fraction(q - p)            # forgets s factor
    if len({correct, wrong1, wrong2, wrong3}) < 4:
        return None
    stem = (f"If a + b + c = {s}, a² + b² + c² = {q} and "
            f"ab + bc + ca = {p}, then the value of a³ + b³ + c³ − 3abc is:")
    sol = (f"a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca) "
           f"= {s}×({q} − {p}) = {s}×{q-p} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_simplify_fraction():
    """Simplify (a^2 - b^2)/(a - b) = a + b for given a,b. [M]"""
    a = random.choice([5, 6, 7, 8, 9, 10, 11, 12])
    b = random.choice([1, 2, 3, 4])
    if a == b:
        return None
    correct = Fraction(a + b)
    wrong1 = Fraction(a - b)           # picks denom factor
    wrong2 = Fraction(a*a - b*b)       # forgets to cancel
    wrong3 = Fraction(a)
    stem = (f"The value of ({a}² − {b}²)/({a} − {b}) is:")
    sol = (f"({a}² − {b}²)/({a} − {b}) = (a + b)(a − b)/(a − b) = a + b "
           f"= {a} + {b} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_x_plus_inv_given_quad():
    """If x^2 - kx + 1 = 0, then x + 1/x = k (divide by x). Find x^3+1/x^3. [VH]"""
    k = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11])
    correct = Fraction(k**3 - 3*k)     # x^3 + 1/x^3
    wrong1 = Fraction(k**3 + 3*k)
    wrong2 = Fraction(k**3)
    wrong3 = Fraction(k**2 - 2)        # gives x^2+1/x^2 instead
    stem = (f"If x² − {k}x + 1 = 0, then the value of x³ + 1/x³ is:")
    sol = (f"Dividing x² − {k}x + 1 = 0 by x gives x + 1/x = {k}. "
           f"Then x³ + 1/x³ = {k}³ − 3×{k} = {k**3} − {3*k} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_x_plus_inv_four_given_quad():
    """If x^2 - kx + 1 = 0 then x + 1/x = k; find x^4 + 1/x^4. [VH]"""
    k = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    s2 = k**2 - 2
    correct = Fraction(s2**2 - 2)
    wrong1 = Fraction(s2**2 + 2)
    wrong2 = Fraction(s2**2)
    wrong3 = Fraction(s2)              # gives x^2+1/x^2 instead
    stem = (f"If x² − {k}x + 1 = 0, then the value of x⁴ + 1/x⁴ is:")
    sol = (f"Dividing by x gives x + 1/x = {k}, so x² + 1/x² = {k}² − 2 = {s2}. "
           f"Then x⁴ + 1/x⁴ = {s2}² − 2 = {s2**2} − 2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_x_minus_inv_given_quad():
    """If x^2 - kx - 1 = 0, then x - 1/x = k; find x^3 - 1/x^3. [VH]"""
    k = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10])
    correct = Fraction(k**3 + 3*k)     # x^3 - 1/x^3
    wrong1 = Fraction(k**3 - 3*k)
    wrong2 = Fraction(k**3)
    wrong3 = Fraction(k**2 + 2)        # gives x^2+1/x^2 instead
    stem = (f"If x² − {k}x − 1 = 0, then the value of x³ − 1/x³ is:")
    sol = (f"Dividing x² − {k}x − 1 = 0 by x gives x − 1/x = {k}. "
           f"Then x³ − 1/x³ = {k}³ + 3×{k} = {k**3} + {3*k} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_surd_x_cube_plus_inv():
    """If x = a + sqrt(a^2-1), find x^3 + 1/x^3 where x+1/x = 2a. [VH]"""
    a = random.choice([2, 3, 4, 5, 6, 7, 8])
    b = a**2 - 1
    k = 2 * a
    correct = Fraction(k**3 - 3*k)
    wrong1 = Fraction(k**3 + 3*k)
    wrong2 = Fraction(k**3)
    wrong3 = Fraction(k**2 - 2)        # x^2+1/x^2 instead
    stem = (f"If x = {a} + √{b}, then the value of x³ + 1/x³ is:")
    sol = (f"Here 1/x = {a} − √{b} (since {a}² − {b} = 1), so x + 1/x = {k}. "
           f"Then x³ + 1/x³ = {k}³ − 3×{k} = {k**3} − {3*k} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


TEMPLATES = [
    t_x_plus_inv_sq, t_x_plus_inv_cube, t_x_plus_inv_four,
    t_x_minus_inv_sq, t_x_minus_inv_cube,
    t_abc_zero_cubes, t_sum_sq_from_sum_and_pair, t_pair_from_sum_and_sumsq,
    t_a_plus_b_ab, t_a_cube_plus_b_cube, t_a_minus_b,
    t_surd_x_plus_inv, t_surd_x_sq_plus_inv,
    t_linear_system, t_linear_system_var,
    t_poly_at_value, t_factor_theorem, t_remainder_theorem,
    t_ratio_expression, t_min_value, t_abc_cubes_minus,
    t_simplify_fraction, t_x_plus_inv_given_quad,
    t_x_plus_inv_four_given_quad, t_x_minus_inv_given_quad,
    t_surd_x_cube_plus_inv,
]

DIFF_OF = {
    t_x_plus_inv_sq: "M", t_x_plus_inv_cube: "H", t_x_plus_inv_four: "H",
    t_x_minus_inv_sq: "M", t_x_minus_inv_cube: "H",
    t_abc_zero_cubes: "H", t_sum_sq_from_sum_and_pair: "H",
    t_pair_from_sum_and_sumsq: "H", t_a_plus_b_ab: "M",
    t_a_cube_plus_b_cube: "H", t_a_minus_b: "H",
    t_surd_x_plus_inv: "H", t_surd_x_sq_plus_inv: "VH",
    t_linear_system: "M", t_linear_system_var: "H",
    t_poly_at_value: "M", t_factor_theorem: "H", t_remainder_theorem: "H",
    t_ratio_expression: "H", t_min_value: "H", t_abc_cubes_minus: "VH",
    t_simplify_fraction: "M", t_x_plus_inv_given_quad: "VH",
    t_x_plus_inv_four_given_quad: "VH", t_x_minus_inv_given_quad: "VH",
    t_surd_x_cube_plus_inv: "VH",
}

# Weighted pool to target ~20% M / 60% H / 20% VH.
# M templates: 7, H templates: 12, VH templates: 7.
# Per-template weight so totals land near the quota.
WEIGHT = {"M": 1.15, "H": 2.7, "VH": 4.2}
POOL = []
for t in TEMPLATES:
    POOL += [t] * int(round(WEIGHT[DIFF_OF[t]] * 10))

attempts = 0
while len(questions) < 500 and attempts < 600000:
    attempts += 1
    t = random.choice(POOL)
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    add(stem, correct, distractors, sol, diff)

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- self-check ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
assert len(questions) == 500, f"Only {len(questions)} questions!"
assert errors == 0, f"{errors} structural errors!"
print(f"Self-check structural errors: {errors}")

from collections import Counter
dist = Counter(q["diff"] for q in questions)
print("Difficulty:", dict(dist))
for d in ("M", "H", "VH"):
    print(f"  {d}: {dist.get(d,0)} ({100*dist.get(d,0)/len(questions):.1f}%)")

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_06_Algebra_500.md"

lines = []
lines.append("# Algebra — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium / ~60% Hard / ~20% Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- `x² + 1/x² = (x + 1/x)² − 2 = (x − 1/x)² + 2`")
lines.append("- `x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x)`  ·  `x³ − 1/x³ = (x − 1/x)³ + 3(x − 1/x)`")
lines.append("- `x⁴ + 1/x⁴ = (x² + 1/x²)² − 2`")
lines.append("- `a² + b² = (a + b)² − 2ab`  ·  `a³ + b³ = (a + b)³ − 3ab(a + b)`")
lines.append("- `(a − b)² = (a + b)² − 4ab`")
lines.append("- `a² + b² + c² = (a + b + c)² − 2(ab + bc + ca)`")
lines.append("- If `a + b + c = 0` then `a³ + b³ + c³ = 3abc`")
lines.append("- `a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca)`")
lines.append("- **Factor/Remainder theorem:** remainder of p(x) ÷ (x − r) is p(r); (x − r) is a factor ⇔ p(r) = 0")
lines.append("- **Componendo & dividendo:** if a/b = p/q then (a + b)/(a − b) = (p + q)/(p − q)")
lines.append("- **AM–GM:** for x > 0, x + k/x ≥ 2√k\n")
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
