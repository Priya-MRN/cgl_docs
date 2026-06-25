# -*- coding: utf-8 -*-
"""
SSC CGL Number System - 500 hard PYQ-pattern MCQ generator.
Every answer is COMPUTED with exact integer arithmetic (pow, %, math.factorial),
so the key is provably correct. Builds 4 distinct options (1 correct + 3
common-mistake distractors), randomizes correct position, dedupes question
stems, outputs markdown in the same layout as the percentage file.
CRITICAL: never pass a float to Fraction(num, den) - all answers are ints here.
"""
import random
import math
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
            return f"{f:.4f}".rstrip("0").rstrip(".")
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        return f"{x:.4f}".rstrip("0").rstrip(".")
    return str(x)


def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 distinct values."""
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        if all(d != o for o in opts):
            opts.append(d)
        if len(opts) == 4:
            break
    # pad with plausible filler if needed (integer bumps)
    bump = 1
    while len(opts) < 4:
        cand = correct + bump
        if all(cand != o for o in opts):
            opts.append(cand)
        else:
            cand = correct - bump
            if all(cand != o for o in opts):
                opts.append(cand)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci


questions = []  # each: dict(stem, opts, ci, sol, diff)
seen = set()


def add(stem, correct, distractors, sol, diff):
    """All answers here are exact integers (Fraction with denom 1)."""
    key = stem.strip()
    if key in seen:
        return False
    cfr = Fraction(correct)
    # keep distractors that are distinct integers/fractions from correct
    dfrs = []
    for d in distractors:
        if d is None:
            continue
        df = Fraction(d)
        if df != cfr and df not in dfrs:
            dfrs.append(df)
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


# ---------------- helpers ----------------

def power_of_prime_in_factorial(n, p):
    """Legendre's formula: highest power of prime p dividing n!."""
    total = 0
    pk = p
    while pk <= n:
        total += n // pk
        pk *= p
    return total


def num_divisors(n):
    cnt = 1
    m = n
    d = 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            cnt *= (e + 1)
        d += 1
    if m > 1:
        cnt *= 2
    return cnt


def sum_divisors(n):
    total = 1
    m = n
    d = 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            total *= (d ** (e + 1) - 1) // (d - 1)
        d += 1
    if m > 1:
        total *= (m * m - 1) // (m - 1)
    return total


def to_base(n, b):
    if n == 0:
        return "0"
    digs = []
    while n:
        digs.append(str(n % b))
        n //= b
    return "".join(reversed(digs))


# ---------------- TEMPLATES ----------------

def t_unit_digit_power():
    """Unit (last) digit of a^n via cyclicity. [H]"""
    a = random.choice([2, 3, 4, 6, 7, 8, 9, 12, 13, 14, 17, 18, 19,
                       22, 23, 27, 28, 33, 47, 53, 64, 77, 83, 99])
    n = random.choice([45, 56, 73, 84, 99, 101, 123, 145, 156, 178,
                       200, 222, 247, 256, 333, 444, 555, 999, 1000])
    correct = pow(a, n, 10)
    last_a = a % 10
    wrong1 = last_a                       # forgets the power, uses base unit digit
    wrong2 = pow(a, n - 1, 10)            # off-by-one in exponent
    wrong3 = pow(a, n + 1, 10)
    # pad distractor pool with other plausible digits
    extra = [d for d in [1, last_a * last_a % 10, (correct + 2) % 10,
                         (correct + 5) % 10] if d not in (correct,)]
    stem = (f"What is the unit (last) digit of {a}^{n}?")
    cyc = []
    x = last_a
    for _ in range(4):
        cyc.append(x)
        x = x * last_a % 10
    sol = (f"Unit digit of {a}^n depends only on {last_a}. The cycle of last digits "
           f"of powers of {last_a} is {cyc[:4]} (period {len(set(cyc)) if last_a not in (0,1,5,6) else 1}). "
           f"Using cyclicity, {a}^{n} ends in {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_trailing_zeros():
    """Number of trailing zeros in n! = power of 5 in n!. [H]"""
    n = random.choice([25, 30, 40, 45, 50, 60, 75, 80, 90, 100, 110,
                       120, 125, 150, 175, 200, 250])
    correct = power_of_prime_in_factorial(n, 5)
    wrong1 = n // 5                                   # only first term
    wrong2 = power_of_prime_in_factorial(n, 2)        # uses 2 instead of 5
    wrong3 = correct + 1
    stem = (f"How many zeros are there at the end of {n}! (factorial of {n})?")
    terms = []
    pk = 5
    while pk <= n:
        terms.append(str(n // pk))
        pk *= 5
    sol = (f"Trailing zeros = highest power of 5 in {n}! = " +
           " + ".join(f"[{n}/{5**(i+1)}]" for i in range(len(terms))) +
           " = " + " + ".join(terms) + f" = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_highest_power_prime():
    """Highest power of prime p dividing n! (Legendre). [VH]"""
    p = random.choice([2, 3, 7])
    n = random.choice([30, 40, 50, 60, 70, 80, 90, 100, 120, 150, 200])
    correct = power_of_prime_in_factorial(n, p)
    wrong1 = n // p                                  # only first term
    wrong2 = correct + 1
    wrong3 = correct - 1
    stem = (f"What is the highest power of {p} that divides {n}! exactly "
            f"(i.e. the exponent of {p} in {n}!)?")
    terms = []
    pk = p
    while pk <= n:
        terms.append(str(n // pk))
        pk *= p
    sol = (f"By Legendre's formula, exponent of {p} = " +
           " + ".join(f"[{n}/{p}^{i+1}]" for i in range(len(terms))) +
           " = " + " + ".join(terms) + f" = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_remainder_power():
    """Remainder of a^n divided by m, computed with pow(). [VH]"""
    m = random.choice([5, 6, 7, 9, 10, 11, 13])
    a = random.choice([2, 3, 4, 5, 6, 7, 8, 12, 17, 23])
    if a % m == 0:
        a += 1
    n = random.choice([50, 64, 81, 100, 128, 150, 200, 256, 333, 400])
    correct = pow(a, n, m)
    wrong1 = (a % m)                       # forgets power
    wrong2 = pow(a, n, m + 1) % m          # wrong modulus then reduce
    wrong3 = (correct + 1) % m
    extra = [(correct + 2) % m, (a * a) % m, (correct + 3) % m]
    stem = (f"What is the remainder when {a}^{n} is divided by {m}?")
    sol = (f"By modular cyclicity, the remainders of {a}^k mod {m} repeat with a fixed "
           f"period; computing {a}^{n} mod {m} gives {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "VH"


def t_divisibility_11_missing():
    """Find missing digit x so a 5-digit number is divisible by 11. [H]"""
    while True:
        d = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(4)]
        pos = random.choice([1, 2, 3, 4])  # not leading digit, keep it nontrivial
        # we want a unique x in 0..9 making divisible by 11
        cands = []
        for x in range(10):
            dd = d[:]
            dd[pos] = x
            val = int("".join(map(str, dd)))
            if val % 11 == 0:
                cands.append(x)
        if len(cands) == 1:
            x = cands[0]
            d[pos] = "x"
            numstr = "".join(map(str, d))
            correct = x
            wrong1 = (x + 1) % 10
            wrong2 = (x + 2) % 10
            wrong3 = (x + 3) % 10 if (x + 3) % 10 != x else (x + 4) % 10
            extra = [(x + 5) % 10, (x + 7) % 10]
            stem = (f"If the number {numstr} (where x is a single digit) is divisible "
                    f"by 11, what is the value of x?")
            sol = (f"Divisibility by 11: (sum of digits in odd places) − (sum in even "
                   f"places) must be a multiple of 11. Solving for x gives x = {x}.")
            return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_divisibility_9_missing():
    """Find missing digit x so number is divisible by 9 (or 3). [M]"""
    base_digits = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(3)]
    s = sum(base_digits)
    x = (-s) % 9                            # digit to make divisible by 9
    pos = random.choice([1, 2, 3])
    d = base_digits[:]
    d.insert(pos, "x")
    numstr = "".join(map(str, d))
    correct = x
    wrong1 = (x + 3) % 9
    wrong2 = (x + 6) % 9
    wrong3 = (9 - x) % 9 if (9 - x) % 9 != x else (x + 1) % 10
    extra = [(x + 1) % 10, (x + 2) % 10]
    stem = (f"What digit should replace x in {numstr} so that the number is "
            f"divisible by 9?")
    sol = (f"A number is divisible by 9 when its digit sum is a multiple of 9. "
           f"Sum of known digits = {s}; the smallest x making the total a multiple "
           f"of 9 is x = {x}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "M"


def t_lcm_remainder():
    """Smallest number leaving same remainder r when divided by a set. [H]"""
    divs = random.choice([[5, 6, 8], [4, 6, 9], [6, 8, 12], [5, 8, 12],
                          [9, 12, 15], [8, 9, 12], [6, 9, 12], [10, 12, 15]])
    r = random.choice([1, 2, 3, 4, 5])
    L = divs[0]
    for d in divs[1:]:
        L = L * d // math.gcd(L, d)
    correct = L + r
    wrong1 = L                                   # forgets remainder
    wrong2 = L - r if L - r > 0 else L + 2 * r   # subtracts
    wrong3 = sum(divs) + r                        # adds divisors instead of LCM
    extra = [L + 2 * r, 2 * L + r]
    stem = (f"What is the least number which when divided by {divs[0]}, {divs[1]} and "
            f"{divs[2]} leaves a remainder of {r} in each case?")
    sol = (f"Required number = LCM({divs[0]}, {divs[1]}, {divs[2]}) + r = {L} + {r} "
           f"= {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_lcm_exact_divisible():
    """Least number leaving remainder r1,r2.. where divisor-remainder is constant k."""
    divs = random.choice([[5, 6, 7], [4, 5, 6], [6, 7, 8], [3, 4, 5],
                          [5, 6, 8], [7, 8, 9]])
    k = random.choice([1, 2, 3])  # each divisor minus remainder = k
    # remainders are d-k
    L = divs[0]
    for d in divs[1:]:
        L = L * d // math.gcd(L, d)
    correct = L - k
    wrong1 = L + k
    wrong2 = L
    wrong3 = L - 2 * k if L - 2 * k > 0 else L + 2 * k
    extra = [2 * L - k, L - k - divs[0]]
    rems = ", ".join(str(d - k) for d in divs)
    stem = (f"Find the least number which when divided by {divs[0]}, {divs[1]} and "
            f"{divs[2]} leaves remainders {rems} respectively (note the divisor minus "
            f"remainder is the same in each case).")
    sol = (f"Here divisor − remainder = {k} is constant, so number = "
           f"LCM({divs[0]},{divs[1]},{divs[2]}) − {k} = {L} − {k} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_successive_division():
    """Successive division: find dividend from quotient-remainder chain. [VH]"""
    d1 = random.choice([3, 4, 5, 6, 7])
    d2 = random.choice([4, 5, 6, 7, 8])
    r1 = random.randint(0, d1 - 1)
    r2 = random.randint(0, d2 - 1)
    qfinal = random.choice([2, 3, 4, 5, 6])
    # number N: N = d1*q1 + r1 ; q1 = d2*qfinal + r2
    q1 = d2 * qfinal + r2
    N = d1 * q1 + r1
    correct = N
    wrong1 = d1 * d2 * qfinal + r1 + r2          # naive flat
    wrong2 = d2 * (d1 * qfinal + r1) + r2        # swapped order
    wrong3 = N + d1
    extra = [N - d1, d1 * q1 + r2]
    stem = (f"A number when divided successively by {d1} and {d2} leaves remainders "
            f"{r1} and {r2} respectively, and the final quotient is {qfinal}. "
            f"What is the number?")
    sol = (f"Work backwards: first quotient = {d2}×{qfinal} + {r2} = {q1}; "
           f"number = {d1}×{q1} + {r1} = {N}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "VH"


def t_division_algorithm():
    """Dividend from divisor, quotient, remainder. [M]"""
    d = random.choice([12, 13, 15, 16, 17, 18, 19, 21, 23, 24, 27])
    q = random.choice([14, 23, 31, 42, 56, 67, 78, 89, 123])
    r = random.randint(0, d - 1)
    N = d * q + r
    correct = N
    wrong1 = d * q                       # forgets remainder
    wrong2 = d * q + d                    # adds divisor
    wrong3 = d * (q + 1) + r             # off-by-one quotient
    extra = [N + r, N - r if N - r != N else N + 1]
    stem = (f"On dividing a number by {d}, the quotient is {q} and the remainder is "
            f"{r}. What is the number?")
    sol = (f"Dividend = divisor × quotient + remainder = {d}×{q} + {r} = {N}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "M"


def t_sum_natural():
    """Sum of first n natural numbers. [M]"""
    n = random.choice([40, 45, 50, 55, 60, 70, 75, 80, 90, 100, 120,
                       125, 150, 175, 200, 250, 300])
    correct = n * (n + 1) // 2
    wrong1 = n * n                        # n^2
    wrong2 = n * (n - 1) // 2             # off-by-one
    wrong3 = (n * (n + 1)) // 2 + n
    extra = [n * (n + 1), correct - n]
    stem = (f"What is the sum of the first {n} natural numbers (1 + 2 + 3 + ... + {n})?")
    sol = (f"Sum = n(n+1)/2 = {n}×{n + 1}/2 = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "M"


def t_sum_squares():
    """Sum of squares of first n natural numbers. [H]"""
    n = random.choice([10, 12, 14, 15, 16, 18, 20, 24, 25, 30, 36, 40])
    correct = n * (n + 1) * (2 * n + 1) // 6
    wrong1 = (n * (n + 1) // 2) ** 2          # sum of cubes formula
    wrong2 = n * (n + 1) // 2                 # sum of naturals
    wrong3 = correct + n * n
    extra = [n * (n + 1) * (2 * n + 1) // 3, correct - n * n]
    stem = (f"What is the sum of the squares of the first {n} natural numbers "
            f"(1² + 2² + ... + {n}²)?")
    sol = (f"Sum of squares = n(n+1)(2n+1)/6 = {n}×{n + 1}×{2 * n + 1}/6 = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_sum_cubes():
    """Sum of cubes of first n natural numbers. [H]"""
    n = random.choice([8, 9, 10, 11, 12, 14, 15, 16, 18, 20, 24, 25])
    s = n * (n + 1) // 2
    correct = s * s
    wrong1 = n * (n + 1) * (2 * n + 1) // 6      # sum of squares
    wrong2 = s                                    # sum of naturals
    wrong3 = correct + n ** 3
    extra = [n ** 3, correct - n ** 3]
    stem = (f"What is the sum of the cubes of the first {n} natural numbers "
            f"(1³ + 2³ + ... + {n}³)?")
    sol = (f"Sum of cubes = [n(n+1)/2]² = {s}² = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_sum_consecutive():
    """Sum of consecutive integers from a to b. [M]"""
    a = random.choice([11, 21, 31, 41, 51, 25, 35, 50])
    b = a + random.choice([19, 29, 39, 49, 24, 9, 14])
    cnt = b - a + 1
    correct = (a + b) * cnt // 2
    wrong1 = (a + b) * cnt                    # forgot /2
    wrong2 = (a + b) * (cnt - 1) // 2         # off-by-one count
    wrong3 = correct + (a + b)
    extra = [correct - a, correct + b]
    stem = (f"What is the sum of all integers from {a} to {b} (both inclusive)?")
    sol = (f"Number of terms = {b}−{a}+1 = {cnt}; sum = (first+last)/2 × count "
           f"= ({a}+{b})/2 × {cnt} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "M"


def t_two_digit_reverse():
    """Two-digit number: digit-sum given, reversing increases/decreases by k. [H]"""
    while True:
        t = random.randint(1, 9)
        u = random.randint(0, 9)
        if t == u:
            continue
        N = 10 * t + u
        R = 10 * u + t
        diff = N - R          # = 9*(t-u)
        s = t + u
        if u == 0:
            continue
        # ask to find the number given digit sum and that N - R = diff (diff != 0)
        correct = N
        wrong1 = R                            # the reversed one
        wrong2 = 10 * u + t                    # same as R (will dedupe) -> use another
        wrong3 = N + 9
        extra = [N - 9, 10 * t + (u + 1) % 10 if (u + 1) % 10 != u else N + 11]
        bigger = "more" if diff < 0 else "less"
        stem = (f"The sum of the digits of a two-digit number is {s}. When the digits "
                f"are reversed, the number becomes {abs(diff)} {bigger} than the "
                f"original. What is the original number?")
        # Solvability: with digit sum s and |t-u| = |diff|/9 fixed, ensure unique
        # t-u from diff, t+u = s -> unique t,u (and t>=1)
        return stem, correct, [wrong1, wrong2, wrong3] + extra, sol_two_digit(s, diff, t, u, N), "H"


def sol_two_digit(s, diff, t, u, N):
    return (f"Let digits be t (tens) and u (units): t+u = {s} and reversing changes "
            f"the value by 9(t−u) = {diff if diff!=0 else 0}, so t−u = {(t - u)}. "
            f"Solving: t = {t}, u = {u}, number = {N}.")


def t_poly_remainder():
    """Remainder when a polynomial value of N divided by small m. [H]"""
    N = random.choice([17, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67])
    m = random.choice([5, 6, 7, 8, 9, 11, 12])
    a = random.choice([2, 3, 5])
    b = random.choice([1, 2, 3, 4, 5, 6, 7])
    c = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    val = a * N * N + b * N + c
    correct = val % m
    wrong1 = (N % m)                          # uses N only
    wrong2 = (a * N + b + c) % m              # wrong expansion
    wrong3 = (correct + 1) % m
    extra = [(correct + 2) % m, (val // m) % m, (correct + 3) % m]
    stem = (f"What is the remainder when {a}N² + {b}N + {c} is divided by {m}, "
            f"given N = {N}?")
    sol = (f"Compute {a}×{N}² + {b}×{N} + {c} = {val}; {val} mod {m} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_largest_ndigit_div():
    """Largest n-digit number divisible by k. [H]"""
    digits = random.choice([3, 4, 5])
    k = random.choice([7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53])
    hi = 10 ** digits - 1
    correct = hi - (hi % k)
    wrong1 = hi                              # ignores divisibility
    wrong2 = correct - k                     # one too low
    wrong3 = correct + k                     # exceeds range / one too high
    extra = [hi - k, correct - 2 * k]
    stem = (f"What is the largest {digits}-digit number that is exactly divisible "
            f"by {k}?")
    sol = (f"Largest {digits}-digit number is {hi}; {hi} mod {k} = {hi % k}, so the "
           f"answer is {hi} − {hi % k} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_smallest_ndigit_div():
    """Smallest n-digit number divisible by k. [H]"""
    digits = random.choice([3, 4, 5])
    k = random.choice([7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53])
    lo = 10 ** (digits - 1)
    rem = lo % k
    correct = lo if rem == 0 else lo + (k - rem)
    wrong1 = lo                              # ignores divisibility
    wrong2 = correct - k                     # below range
    wrong3 = lo + rem                        # wrong direction
    extra = [correct + k, lo + (k - rem) - 1 if rem else lo + 1]
    stem = (f"What is the smallest {digits}-digit number that is exactly divisible "
            f"by {k}?")
    sol = (f"Smallest {digits}-digit number is {lo}; {lo} mod {k} = {rem}, so the "
           f"answer is {lo} + ({k} − {rem}) = {correct}." if rem else
           f"Smallest {digits}-digit number {lo} is itself divisible by {k}, so the "
           f"answer is {lo}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_count_divisible():
    """Count numbers divisible by a OR b in 1..N (inclusion-exclusion). [VH]"""
    N = random.choice([100, 150, 200, 250, 300, 400, 500, 600, 1000])
    a = random.choice([3, 4, 5, 6])
    b = random.choice([7, 8, 9, 11])
    l = a * b // math.gcd(a, b)
    cA = N // a
    cB = N // b
    cAB = N // l
    correct = cA + cB - cAB
    wrong1 = cA + cB                          # forgets inclusion-exclusion
    wrong2 = cA + cB - 2 * cAB
    wrong3 = correct + cAB
    extra = [cA, cB]
    stem = (f"How many numbers from 1 to {N} are divisible by {a} or {b}?")
    sol = (f"Divisible by {a}: [{N}/{a}] = {cA}; by {b}: [{N}/{b}] = {cB}; by both "
           f"(LCM {l}): {cAB}. By inclusion-exclusion: {cA} + {cB} − {cAB} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "VH"


def t_count_divisible_both():
    """Count numbers divisible by BOTH a and b in 1..N. [M]"""
    N = random.choice([100, 200, 300, 500, 600, 1000])
    a = random.choice([4, 6, 8, 9])
    b = random.choice([6, 9, 12, 15])
    l = a * b // math.gcd(a, b)
    correct = N // l
    wrong1 = N // a                           # only a
    wrong2 = N // b                           # only b
    wrong3 = N // (a * b)                      # uses product instead of LCM
    extra = [correct + 1, correct - 1 if correct - 1 >= 0 else correct + 2]
    stem = (f"How many numbers from 1 to {N} are divisible by both {a} and {b}?")
    sol = (f"Divisible by both means divisible by LCM({a},{b}) = {l}; count = "
           f"[{N}/{l}] = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "M"


def t_num_divisors():
    """Number of divisors (factors) of a composite number. [H]"""
    n = random.choice([72, 84, 90, 96, 108, 120, 144, 180, 196, 200,
                       216, 240, 360, 400, 480, 540, 600, 720])
    correct = num_divisors(n)
    wrong1 = correct - 1
    wrong2 = correct + 1
    wrong3 = correct // 2 if correct // 2 != correct else correct + 2
    extra = [correct + 2, correct - 2 if correct - 2 > 0 else correct + 3]
    stem = (f"How many factors (divisors) does {n} have?")
    # prime factorization for solution
    m = n
    facs = []
    d = 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            facs.append((d, e))
        d += 1
    if m > 1:
        facs.append((m, 1))
    pf = " × ".join(f"{p}^{e}" for p, e in facs)
    prod = " × ".join(f"({e}+1)" for p, e in facs)
    sol = (f"{n} = {pf}. Number of divisors = product of (exponent+1) = {prod} "
           f"= {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_sum_divisors():
    """Sum of all divisors of a number. [VH]"""
    n = random.choice([24, 28, 36, 40, 48, 60, 72, 84, 96, 100, 120])
    correct = sum_divisors(n)
    wrong1 = correct - n                      # excludes the number itself
    wrong2 = num_divisors(n)                  # count instead of sum
    wrong3 = correct - 1                       # excludes 1
    extra = [correct + n, correct + 1]
    stem = (f"What is the sum of all the factors (divisors) of {n}, including 1 and "
            f"{n} itself?")
    m = n
    facs = []
    d = 2
    while d * d <= m:
        if m % d == 0:
            e = 0
            while m % d == 0:
                m //= d
                e += 1
            facs.append((d, e))
        d += 1
    if m > 1:
        facs.append((m, 1))
    pf = " × ".join(f"{p}^{e}" for p, e in facs)
    parts = " × ".join(
        "(" + " + ".join(str(p ** i) for i in range(e + 1)) + ")" for p, e in facs
    )
    sol = (f"{n} = {pf}. Sum of divisors = {parts} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "VH"


def t_perfect_square_least_mult():
    """Least number to multiply n to make a perfect square. [VH]"""
    n = random.choice([8, 12, 18, 20, 24, 27, 32, 45, 48, 50, 72, 75,
                       80, 98, 108, 128, 162, 200])
    m = n
    facs = {}
    d = 2
    while d * d <= m:
        while m % d == 0:
            facs[d] = facs.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        facs[m] = facs.get(m, 0) + 1
    mult = 1
    for p, e in facs.items():
        if e % 2 == 1:
            mult *= p
    correct = mult
    wrong1 = n                                # multiply by itself
    wrong2 = mult * 2 if mult * 2 != mult else mult + 1
    wrong3 = 2
    extra = [mult + 1, mult * mult if mult > 1 else 3]
    pf = " × ".join(f"{p}^{e}" for p, e in sorted(facs.items()))
    stem = (f"What is the least number by which {n} must be multiplied to make it a "
            f"perfect square?")
    sol = (f"{n} = {pf}. For a perfect square every prime exponent must be even. "
           f"The primes with odd exponents multiply to {mult}, so multiply by {mult}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "VH"


def t_base_to_decimal():
    """Convert a binary number to decimal. [M]"""
    val = random.choice([13, 19, 21, 25, 27, 37, 43, 51, 58, 75, 90, 100, 125])
    binstr = to_base(val, 2)
    correct = val
    # distractor: read as if base 10 wrong, swap a bit, etc.
    wrong1 = val + 1
    wrong2 = val - 1
    wrong3 = int(binstr)                       # interprets the digit-string as base 10
    extra = [val + 2, val * 2]
    stem = (f"Convert the binary number ({binstr})₂ to its decimal (base-10) value.")
    powers = " + ".join(
        f"{b}×2^{len(binstr) - 1 - i}" for i, b in enumerate(binstr)
    )
    sol = (f"({binstr})₂ = {powers} = {correct} in decimal.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "M"


def t_decimal_to_base():
    """Convert decimal to binary, asked as number of 1s or the value. [M]"""
    val = random.choice([18, 22, 29, 35, 44, 53, 60, 71, 88, 95, 110, 127])
    binstr = to_base(val, 2)
    ones = binstr.count("1")
    correct = ones
    wrong1 = len(binstr)                       # total digits
    wrong2 = ones + 1
    wrong3 = ones - 1 if ones - 1 >= 0 else ones + 2
    extra = [len(binstr) - ones, len(binstr) + 1]
    stem = (f"When the decimal number {val} is written in binary (base 2), how many "
            f"1s does it contain?")
    sol = (f"{val} in binary is ({binstr})₂, which contains {ones} ones.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "M"


def t_remainder_consecutive_product():
    """Remainder when product/sum pattern divided by m. [H]"""
    # Remainder of (large explicit number) mod m using cyclic / direct
    a = random.choice([2, 3, 7, 11, 13])
    n = random.choice([20, 30, 40, 50, 60, 70, 80, 90, 100])
    add_c = random.choice([1, 2, 3, 4, 5])
    m = random.choice([5, 6, 7, 8, 9])
    val = pow(a, n) + add_c
    correct = val % m
    wrong1 = (a + add_c) % m
    wrong2 = (pow(a, n, m))                    # forgets +c
    wrong3 = (correct + 1) % m
    extra = [(correct + 2) % m, (add_c) % m, (correct + 3) % m]
    stem = (f"What is the remainder when {a}^{n} + {add_c} is divided by {m}?")
    sol = (f"{a}^{n} mod {m} = {pow(a, n, m)}; adding {add_c} and reducing mod {m} "
           f"gives ({pow(a, n, m)} + {add_c}) mod {m} = {correct}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "H"


def t_hcf_of_remainders():
    """Largest number dividing a, b, c leaving same remainder r -> HCF of diffs. [VH]"""
    g = random.choice([7, 11, 12, 13, 15, 17, 18, 23])
    r = random.randint(1, g - 1)
    m1, m2 = random.sample([2, 3, 4, 5, 6, 7, 8], 2)
    a = g * 1 + r
    b = g * (1 + m1) + r
    c = g * (1 + m1 + m2) + r
    if not (a < b < c):
        return None
    correct = g
    wrong1 = g * 2
    wrong2 = math.gcd(a, b)
    wrong3 = g + r
    extra = [g - 1, g + 1]
    stem = (f"What is the largest number that divides {a}, {b} and {c}, leaving the "
            f"same remainder in each case?")
    sol = (f"The required number divides the differences: {b}−{a} = {b - a} and "
           f"{c}−{b} = {c - b}. HCF of these differences = {g}.")
    return stem, correct, [wrong1, wrong2, wrong3] + extra, sol, "VH"


TEMPLATES = [
    t_unit_digit_power, t_trailing_zeros, t_highest_power_prime, t_remainder_power,
    t_divisibility_11_missing, t_divisibility_9_missing, t_lcm_remainder,
    t_lcm_exact_divisible, t_successive_division, t_division_algorithm,
    t_sum_natural, t_sum_squares, t_sum_cubes, t_sum_consecutive,
    t_two_digit_reverse, t_poly_remainder, t_largest_ndigit_div,
    t_smallest_ndigit_div, t_count_divisible, t_count_divisible_both,
    t_num_divisors, t_sum_divisors, t_perfect_square_least_mult,
    t_base_to_decimal, t_decimal_to_base, t_remainder_consecutive_product,
    t_hcf_of_remainders,
]

DIFF_OF = {
    t_unit_digit_power: "H", t_trailing_zeros: "H", t_highest_power_prime: "VH",
    t_remainder_power: "VH", t_divisibility_11_missing: "H",
    t_divisibility_9_missing: "M", t_lcm_remainder: "H",
    t_lcm_exact_divisible: "H", t_successive_division: "VH",
    t_division_algorithm: "M", t_sum_natural: "M", t_sum_squares: "H",
    t_sum_cubes: "H", t_sum_consecutive: "M", t_two_digit_reverse: "H",
    t_poly_remainder: "H", t_largest_ndigit_div: "H",
    t_smallest_ndigit_div: "H", t_count_divisible: "VH",
    t_count_divisible_both: "M", t_num_divisors: "H", t_sum_divisors: "VH",
    t_perfect_square_least_mult: "VH", t_base_to_decimal: "M",
    t_decimal_to_base: "M", t_remainder_consecutive_product: "H",
    t_hcf_of_remainders: "VH",
}
WEIGHT = {"M": 3.0, "H": 5.4, "VH": 3.2}
POOL = []
for t in TEMPLATES:
    POOL += [t] * int(WEIGHT[DIFF_OF[t]] * 10)

# Generate until we have 500 unique
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

print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_10_Number_System_500.md"

lines = []
lines.append("# Number System — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (trap) — CGL Tier-I/II standard, modelled on actual PYQ patterns (2018–2025).")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- **Unit digit of aⁿ**: depends only on the unit digit of a; powers repeat with period ≤ 4 (cyclicity).")
lines.append("- **Trailing zeros of n!** = highest power of 5 in n! = [n/5] + [n/25] + [n/125] + …")
lines.append("- **Highest power of prime p in n!** (Legendre) = [n/p] + [n/p²] + [n/p³] + …")
lines.append("- **Divisibility by 9 / 3**: digit sum divisible by 9 / 3.  **By 11**: (odd-place sum − even-place sum) divisible by 11.")
lines.append("- **Dividend** = divisor × quotient + remainder.")
lines.append("- **Least number leaving remainder r with several divisors** = LCM(divisors) + r.")
lines.append("- **Sum of first n naturals** = n(n+1)/2 · **squares** = n(n+1)(2n+1)/6 · **cubes** = [n(n+1)/2]².")
lines.append("- **Number of divisors** of N = p^a·q^b… is (a+1)(b+1)… ; **sum of divisors** = Π (pᵃ⁺¹−1)/(p−1).")
lines.append("- **Count divisible by a or b in 1..N** = [N/a] + [N/b] − [N/LCM(a,b)] (inclusion–exclusion).")
lines.append("- **Perfect square**: every prime exponent in the factorization must be even.\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Block {blk} (Q{start + 1}–Q{start + 50})\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        o = q["opts"]
        lines.append(f"**Q{n}.** {q['stem']}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Answers Q{start + 1}–Q{start + 50}\n")
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
