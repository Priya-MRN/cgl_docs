# -*- coding: utf-8 -*-
"""
SSC CGL Number & Alphabet Series (Reasoning) - 500 MCQ generator.
RULE-BASED & self-verifying: every series is built by an EXACT rule, so the
missing/next term is provably correct. Distractors are near-misses (off-by-one,
wrong-rule, adjacent term). Options are STRINGS (numbers or letter groups).
Emits a JSON sidecar (qnum -> correct term string) for the independent verifier.
"""
import random
import json
from collections import Counter

random.seed(20260625)  # deterministic

LETTERS = "abcd"
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# ---------------- letter helpers ----------------
def pos(ch):
    """1-indexed alphabet position, A=1 .. Z=26."""
    return ord(ch.upper()) - ord('A') + 1

def from_pos(p):
    """1-indexed position -> letter, wraps mod 26 (1..26)."""
    return AZ[(p - 1) % 26]

def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

PRIMES = [n for n in range(2, 400) if is_prime(n)]

questions = []  # dict(stem, opts(list str), ci, sol, diff, qtype)
seen = set()

def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 DISTINCT string values.
    correct + up to 3 distractors; pad with mutated fillers if needed."""
    correct = str(correct)
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        d = str(d)
        if d not in opts:
            opts.append(d)
        if len(opts) == 4:
            break
    tries = 0
    while len(opts) < 4 and tries < 300:
        tries += 1
        cand = _mutate(correct, tries)
        if cand not in opts:
            opts.append(cand)
    k = 0
    while len(opts) < 4:
        cand = correct + "_" + str(k)
        if cand not in opts:
            opts.append(cand)
        k += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci

def _mutate(s, seedn):
    """Plausible wrong string: nudge a digit or letter."""
    chars = list(s)
    idxs = [i for i, c in enumerate(chars) if c.isalpha() or c.isdigit()]
    if not idxs:
        return s + "X"
    i = idxs[seedn % len(idxs)]
    c = chars[i]
    # vary the offset with seedn so single-char strings get many candidates
    off = ((seedn // len(idxs)) % 12) + 1
    sgn = 1 if seedn % 2 else -1
    if c.isdigit():
        chars[i] = str((int(c) + sgn * off) % 10)
    else:
        up = c.isupper()
        base = AZ[(pos(c) - 1 + sgn * off) % 26]
        chars[i] = base if up else base.lower()
    return "".join(chars)

def add(stem, correct, distractors, sol, diff, qtype):
    key = stem.strip()
    if key in seen:
        return False
    correct = str(correct)
    clean = []
    for d in distractors:
        if d is None:
            continue
        d = str(d)
        if d != correct and d not in clean:
            clean.append(d)
    if len(clean) < 1:
        return False
    seen.add(key)
    opts, ci = make_options(correct, clean)
    assert opts[ci] == correct, "keyed option != correct"
    questions.append({
        "stem": stem, "opts": opts, "ci": ci,
        "sol": sol, "diff": diff, "qtype": qtype,
    })
    return True

def series_str(terms, hide_idx):
    """Render a series with '?' at hide_idx."""
    out = []
    for i, t in enumerate(terms):
        out.append("?" if i == hide_idx else str(t))
    return ", ".join(out)

def ordinal(i):
    return {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth",
            5: "sixth", 6: "seventh", 7: "eighth"}.get(i, f"{i+1}th")

# ================= NUMBER SERIES TYPES =================

def t_arithmetic():
    """Constant difference. [M]"""
    a0 = random.randint(2, 30)
    d = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 11, 12, -3, -4, -5])
    n = random.choice([6, 7])
    terms = [a0 + i * d for i in range(n)]
    if any(t < -50 for t in terms):
        return None
    hide = random.choice([2, 3, n - 1])  # middle or next
    ans = terms[hide]
    d1, d2, d3 = ans + d, ans - d, ans + 1
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"The series is an arithmetic progression with a common difference of "
           f"{d:+d}. So the missing ({ordinal(hide)}) term = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "M", "arithmetic"

def t_geometric():
    """Constant ratio. [M]"""
    a0 = random.choice([1, 2, 3, 4, 5, 6])
    r = random.choice([2, 3, 4, 5])
    n = 6
    terms = [a0 * (r ** i) for i in range(n)]
    if terms[-1] > 200000:
        return None
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    d1, d2, d3 = ans * r, ans // r if ans % r == 0 else ans + 1, ans + r
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"Each term is the previous term multiplied by {r} (geometric, ratio {r}). "
           f"So the missing ({ordinal(hide)}) term = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "M", "geometric"

def t_diff_in_ap():
    """Differences themselves form an AP (2nd-level). [VH]"""
    a0 = random.randint(2, 15)
    d0 = random.choice([2, 3, 4, 5, 6])
    step = random.choice([1, 2, 3, 4])
    n = 6
    terms = [a0]
    d = d0
    for i in range(1, n):
        terms.append(terms[-1] + d)
        d += step
    hide = random.choice([2, 3, 4])
    ans = terms[hide]
    d1 = ans + step
    d2 = ans - step
    d3 = ans + 1
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    diffs = [terms[i+1] - terms[i] for i in range(n - 1)]
    sol = (f"The differences between consecutive terms are {', '.join(str(x) for x in diffs)} "
           f"— they increase by {step} each time (an AP of differences). "
           f"So the missing ({ordinal(hide)}) term = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "VH", "diff_in_ap"

def t_squares_pm():
    """n^2 +/- k. [H]"""
    k = random.choice([0, 1, -1, 2, -2, 3])
    start = random.randint(2, 8)
    n = 6
    terms = [(start + i) ** 2 + k for i in range(n)]
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    base = start + hide
    d1 = (base + 1) ** 2 + k
    d2 = (base - 1) ** 2 + k
    d3 = ans + 1
    shown = list(terms); shown[hide] = "?"
    ksig = "" if k == 0 else f" {k:+d}"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"The terms are perfect squares of consecutive integers"
           f"{(' plus ' + str(k)) if k>0 else (' minus ' + str(-k)) if k<0 else ''}: "
           f"n^2{ksig} for n = {start},{start+1},.... "
           f"The missing ({ordinal(hide)}) term = {base}^2{ksig} = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "H", "squares_pm"

def t_cubes_pm():
    """n^3 +/- k. [H]"""
    k = random.choice([0, 1, -1, 2, -2])
    start = random.randint(1, 5)
    n = 6
    terms = [(start + i) ** 3 + k for i in range(n)]
    if terms[-1] > 100000:
        return None
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    base = start + hide
    d1 = (base + 1) ** 3 + k
    d2 = (base - 1) ** 3 + k
    d3 = ans + 1
    shown = list(terms); shown[hide] = "?"
    ksig = "" if k == 0 else f" {k:+d}"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"The terms are perfect cubes of consecutive integers"
           f"{(' (with '+f'{k:+d}'+')') if k else ''}: n^3{ksig} for n = {start},{start+1},.... "
           f"The missing ({ordinal(hide)}) term = {base}^3{ksig} = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "H", "cubes_pm"

def t_interleaved():
    """Two interleaved arithmetic series. [VH]"""
    a0 = random.randint(2, 20)
    da = random.choice([3, 4, 5, 6, 7])
    b0 = random.randint(40, 90)
    db = random.choice([-3, -4, -5, -6])
    n = 8
    terms = []
    for i in range(n):
        if i % 2 == 0:
            terms.append(a0 + (i // 2) * da)
        else:
            terms.append(b0 + (i // 2) * db)
    # hide an element from the first interleaved series (even index, middle)
    hide = random.choice([4, 6])
    ans = terms[hide]
    d1 = ans + da
    d2 = ans - da
    d3 = terms[hide - 1]  # neighbour from other series
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"Two series are interleaved. Terms at odd positions (1st,3rd,5th...) form "
           f"one progression (start {a0}, step {da:+d}); terms at even positions form "
           f"another (start {b0}, step {db:+d}). The missing term belongs to the first "
           f"series, giving {ans}.")
    return stem, ans, [d1, d2, d3], sol, "VH", "interleaved"

def t_prime():
    """Prime number sequence. [H]"""
    start = random.randint(0, 20)
    n = 6
    seq = PRIMES[start:start + n]
    hide = random.choice([2, 3, n - 1])
    ans = seq[hide]
    # distractors: nearby non-primes / next prime
    d1 = ans + 2
    d2 = ans - 1
    d3 = ans + 1 if (ans + 1) != ans else ans + 4
    shown = list(seq); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"The series lists consecutive prime numbers. The prime between "
           f"{seq[hide-1]} and {seq[hide+1] if hide+1 < n else seq[hide]+2} is {ans}, "
           f"so the missing ({ordinal(hide)}) term = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "H", "prime"

def t_add_then_mul():
    """Alternating: +n then xm. [H]"""
    a0 = random.randint(2, 8)
    add_n = random.choice([2, 3, 4, 5])
    mul_m = random.choice([2, 3])
    n = 6
    terms = [a0]
    for i in range(1, n):
        if i % 2 == 1:
            terms.append(terms[-1] + add_n)
        else:
            terms.append(terms[-1] * mul_m)
    if terms[-1] > 100000:
        return None
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    d1 = ans + add_n
    d2 = ans + mul_m
    d3 = ans + 1
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"The operations alternate: +{add_n}, then x{mul_m}, then +{add_n}, .... "
           f"Applying this, the missing ({ordinal(hide)}) term = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "H", "add_then_mul"

def t_fibonacci():
    """Fibonacci-like: each term = sum of previous two. [H]"""
    a, b = random.randint(1, 8), random.randint(2, 10)
    n = 7
    terms = [a, b]
    for i in range(2, n):
        terms.append(terms[-1] + terms[-2])
    hide = random.choice([3, 4, n - 1])
    ans = terms[hide]
    d1 = ans + 1
    d2 = terms[hide - 1] + terms[hide - 2] + 1
    d3 = ans - 2
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"Each term is the sum of the two preceding terms (Fibonacci-type). "
           f"{terms[hide-2]} + {terms[hide-1]} = {ans}, so the missing "
           f"({ordinal(hide)}) term = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "H", "fibonacci"

def t_nsq_plus_n():
    """n^2 + 1 / n^2 - 1 patterns (explicit position rule). [H]"""
    sign = random.choice([1, -1])
    n = 6
    start = random.randint(2, 6)
    terms = [(start + i) ** 2 + sign for i in range(n)]
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    base = start + hide
    d1 = (base + 1) ** 2 + sign
    d2 = base ** 2 - sign
    d3 = ans + 2
    shown = list(terms); shown[hide] = "?"
    label = "n^2 + 1" if sign == 1 else "n^2 - 1"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"The terms follow {label} for consecutive n starting at {start}. "
           f"For n = {base}: {base}^2 {'+' if sign==1 else '-'} 1 = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "H", "nsq_plus_n"

def t_product_position():
    """Term = n x (n+1) style (product of position). [H]"""
    n = 6
    start = random.randint(1, 5)
    mode = random.choice(["nn1", "nn2"])
    if mode == "nn1":
        terms = [(start + i) * (start + i + 1) for i in range(n)]
        rule = "n x (n+1)"
        f = lambda m: m * (m + 1)
    else:
        terms = [(start + i) * (start + i + 2) for i in range(n)]
        rule = "n x (n+2)"
        f = lambda m: m * (m + 2)
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    base = start + hide
    d1 = f(base + 1)
    d2 = f(base - 1)
    d3 = ans + base
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"Each term is {rule} for consecutive n starting at {start}. "
           f"For n = {base}: {ans}.")
    return stem, ans, [d1, d2, d3], sol, "H", "product_position"

def t_mul2_plus1():
    """x2+1 style recurrence. [H]"""
    a0 = random.randint(1, 6)
    m = random.choice([2, 3])
    k = random.choice([1, 2, 3])
    n = 6
    terms = [a0]
    for i in range(1, n):
        terms.append(terms[-1] * m + k)
    if terms[-1] > 200000:
        return None
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    d1 = terms[hide - 1] * m + k + 1
    d2 = terms[hide - 1] * m
    d3 = ans + 1
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"Each term = (previous term) x {m} + {k}. "
           f"{terms[hide-1]} x {m} + {k} = {ans}, the missing ({ordinal(hide)}) term.")
    return stem, ans, [d1, d2, d3], sol, "H", "mul2_plus1"

def t_double_difference():
    """Differences multiply by a constant (x2 each). [VH]"""
    a0 = random.randint(2, 12)
    d0 = random.choice([2, 3, 4, 5])
    r = random.choice([2, 3])
    n = 6
    terms = [a0]
    d = d0
    for i in range(1, n):
        terms.append(terms[-1] + d)
        d *= r
    if terms[-1] > 200000:
        return None
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    d1 = ans + d0
    d2 = ans - d0
    d3 = ans + 1
    shown = list(terms); shown[hide] = "?"
    diffs = [terms[i+1] - terms[i] for i in range(n - 1)]
    stem = (f"Find the missing term in the series: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"The differences between terms are {', '.join(str(x) for x in diffs)} — "
           f"each difference is {r} times the previous one. "
           f"So the missing ({ordinal(hide)}) term = {ans}.")
    return stem, ans, [d1, d2, d3], sol, "VH", "double_difference"

def t_wrong_number():
    """Find the WRONG number in an otherwise-arithmetic/geometric series. [VH]"""
    mode = random.choice(["ap", "gp", "sq"])
    n = 6
    if mode == "ap":
        a0 = random.randint(3, 20)
        d = random.choice([4, 5, 6, 7, 8, 9])
        terms = [a0 + i * d for i in range(n)]
        rule = f"an arithmetic progression with common difference {d}"
    elif mode == "gp":
        a0 = random.choice([2, 3, 4])
        r = random.choice([2, 3])
        terms = [a0 * (r ** i) for i in range(n)]
        rule = f"a geometric progression with ratio {r}"
    else:
        start = random.randint(2, 6)
        terms = [(start + i) ** 2 for i in range(n)]
        rule = "the squares of consecutive integers"
    # corrupt one interior term
    bad_idx = random.choice([1, 2, 3, 4])
    correct_term = terms[bad_idx]
    delta = random.choice([1, 2, -1, -2, 3, -3])
    wrong_val = correct_term + delta
    while wrong_val in terms or wrong_val == correct_term:
        delta += 1
        wrong_val = correct_term + delta
    shown = list(terms)
    shown[bad_idx] = wrong_val
    ans = wrong_val  # the wrong number IS the answer to spot
    # distractors: other (correct) terms
    others = [t for i, t in enumerate(shown) if i != bad_idx]
    random.shuffle(others)
    d1, d2, d3 = others[0], others[1], others[2]
    stem = (f"One number in the following series is wrong. Find the wrong number: "
            f"{', '.join(str(x) for x in shown)}")
    sol = (f"The series should be {rule}: {', '.join(str(x) for x in terms)}. "
           f"The value {wrong_val} breaks the pattern (it should be {correct_term}), "
           f"so {wrong_val} is the wrong number.")
    return stem, ans, [d1, d2, d3], sol, "VH", "wrong_number"

# ================= ALPHABET / ALPHANUMERIC SERIES =================

def t_letter_skip():
    """Letters with constant skip, e.g. A, C, E, ... [M]"""
    start = random.randint(0, 10)  # 0->A
    skip = random.choice([1, 2, 3, 4])
    n = 6
    poss = [start + i * skip for i in range(n)]
    if poss[-1] > 25:
        return None
    terms = [AZ[p] for p in poss]
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    p = poss[hide]
    d1 = AZ[(p + 1) % 26]
    d2 = AZ[(p - 1) % 26]
    d3 = AZ[(p + skip) % 26] if AZ[(p + skip) % 26] not in (d1, d2) else AZ[(p + 2) % 26]
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing letter in the series: "
            f"{', '.join(shown)}")
    sol = (f"Each letter advances by {skip} position(s) in the alphabet "
           f"(skip of {skip-1} letter(s)). The missing ({ordinal(hide)}) letter is "
           f"'{ans}' (position {p+1}).")
    return stem, ans, [d1, d2, d3], sol, "M", "letter_skip"

def t_letter_varying_skip():
    """Letters with increasing skip, e.g. A, B, D, G, ... [H]"""
    start = random.randint(0, 4)
    d0 = random.choice([1, 2])
    step = random.choice([1, 2])
    n = 6
    poss = [start]
    d = d0
    for i in range(1, n):
        poss.append(poss[-1] + d)
        d += step
    if poss[-1] > 25:
        return None
    terms = [AZ[p] for p in poss]
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    p = poss[hide]
    d1 = AZ[(p + 1) % 26]
    d2 = AZ[(p - 1) % 26]
    d3 = AZ[(p + step) % 26]
    shown = list(terms); shown[hide] = "?"
    gaps = [poss[i+1] - poss[i] for i in range(n - 1)]
    stem = (f"Find the missing letter in the series: "
            f"{', '.join(shown)}")
    sol = (f"The gaps between letters increase: {', '.join(str(g) for g in gaps)} "
           f"(each gap rises by {step}). The missing ({ordinal(hide)}) letter is "
           f"'{ans}' (position {p+1}).")
    return stem, ans, [d1, d2, d3], sol, "H", "letter_varying_skip"

def t_reverse_alpha():
    """Reverse-alphabet steps, e.g. Z, X, V, ... [H]"""
    start = random.randint(20, 25)  # high
    skip = random.choice([1, 2, 3])
    n = 6
    poss = [start - i * skip for i in range(n)]
    if poss[-1] < 0:
        return None
    terms = [AZ[p] for p in poss]
    hide = random.choice([2, 3, n - 1])
    ans = terms[hide]
    p = poss[hide]
    d1 = AZ[(p + 1) % 26]
    d2 = AZ[(p - 1) % 26]
    d3 = AZ[(p - skip) % 26]
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing letter in the series: "
            f"{', '.join(shown)}")
    sol = (f"The letters move backward through the alphabet by {skip} position(s) "
           f"each step. The missing ({ordinal(hide)}) letter is '{ans}' (position {p+1}).")
    return stem, ans, [d1, d2, d3], sol, "H", "reverse_alpha"

def t_letter_pairs_opposite():
    """Pairs like AZ, BY, CX (first +1, second -1). [H]"""
    n = 5
    start = random.randint(0, 4)
    terms = [AZ[start + i] + AZ[25 - (start + i)] for i in range(n)]
    hide = random.choice([2, 3])
    ans = terms[hide]
    p1 = start + hide
    p2 = 25 - (start + hide)
    d1 = AZ[(p1 + 1) % 26] + AZ[p2 % 26]
    d2 = AZ[p1 % 26] + AZ[(p2 - 1) % 26]
    d3 = AZ[(p1) % 26] + AZ[(25 - p1 + 1) % 26]
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the letter series: "
            f"{', '.join(shown)}")
    sol = (f"In each pair the first letter moves forward (A,B,C,...) while the second "
           f"moves backward (Z,Y,X,...) — they are 'opposite' letters (positions sum "
           f"to 27). The missing ({ordinal(hide)}) term is '{ans}'.")
    return stem, ans, [d1, d2, d3], sol, "H", "letter_pairs_opposite"

def t_letter_number_pair():
    """Letter+number pairs, e.g. A1, C3, E5 (letter skips, number tracks). [H]"""
    start = random.randint(0, 8)
    skip = random.choice([1, 2, 3])
    n = 6
    if start + (n - 1) * skip > 25:
        return None
    terms = [f"{AZ[start + i*skip]}{start + i*skip + 1}" for i in range(n)]
    hide = random.choice([2, 3, n - 1])
    p = start + hide * skip
    ans = f"{AZ[p]}{p+1}"
    d1 = f"{AZ[(p+1)%26]}{p+2}"
    d2 = f"{AZ[(p-1)%26]}{p}"
    d3 = f"{AZ[p]}{p+2}"
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing term in the series: "
            f"{', '.join(shown)}")
    sol = (f"Each term is a letter paired with its alphabet position number; the letter "
           f"advances by {skip} each step (A=1, B=2, ...). The missing ({ordinal(hide)}) "
           f"term is '{ans}'.")
    return stem, ans, [d1, d2, d3], sol, "H", "letter_number_pair"

def t_alpha_two_streams():
    """Interleaved alphabet: forward and backward streams. [VH]"""
    fstart = random.randint(0, 6)
    fskip = random.choice([1, 2])
    bstart = random.randint(19, 25)
    bskip = random.choice([1, 2])
    n = 6
    terms = []
    fp = fstart
    bp = bstart
    poslist = []
    for i in range(n):
        if i % 2 == 0:
            terms.append(AZ[fp % 26]); poslist.append(("F", fp)); fp += fskip
        else:
            terms.append(AZ[bp % 26]); poslist.append(("B", bp)); bp -= bskip
    hide = random.choice([2, 4])  # forward-stream element
    ans = terms[hide]
    p = poslist[hide][1]
    d1 = AZ[(p + 1) % 26]
    d2 = AZ[(p - 1) % 26]
    d3 = AZ[(p + fskip) % 26]
    shown = list(terms); shown[hide] = "?"
    stem = (f"Find the missing letter in the series: "
            f"{', '.join(shown)}")
    sol = (f"Two letter-streams are interleaved: positions 1,3,5,... move forward "
           f"(step +{fskip}) and positions 2,4,6,... move backward (step -{bskip}). "
           f"The missing letter belongs to the forward stream, giving '{ans}'.")
    return stem, ans, [d1, d2, d3], sol, "VH", "alpha_two_streams"

# ---------------- registry ----------------
TEMPLATES = [
    t_arithmetic, t_geometric, t_diff_in_ap, t_squares_pm, t_cubes_pm,
    t_interleaved, t_prime, t_add_then_mul, t_fibonacci, t_nsq_plus_n,
    t_product_position, t_mul2_plus1, t_double_difference, t_wrong_number,
    t_letter_skip, t_letter_varying_skip, t_reverse_alpha,
    t_letter_pairs_opposite, t_letter_number_pair, t_alpha_two_streams,
]

DIFF_OF = {
    t_arithmetic: "M", t_geometric: "M", t_diff_in_ap: "VH", t_squares_pm: "H",
    t_cubes_pm: "H", t_interleaved: "VH", t_prime: "H", t_add_then_mul: "H",
    t_fibonacci: "H", t_nsq_plus_n: "H", t_product_position: "H",
    t_mul2_plus1: "H", t_double_difference: "VH", t_wrong_number: "VH",
    t_letter_skip: "M", t_letter_varying_skip: "H", t_reverse_alpha: "H",
    t_letter_pairs_opposite: "H", t_letter_number_pair: "H",
    t_alpha_two_streams: "VH",
}
# M templates (3): arithmetic, geometric, letter_skip
# VH templates (4): diff_in_ap, interleaved, double_difference, wrong_number, alpha_two_streams (5)
# H templates: the rest (12)
# Target ~20% M / 60% H / 20% VH. Tune per-difficulty weights.
WEIGHT = {"M": 3.2, "H": 2.6, "VH": 1.7}
POOL = []
for t in TEMPLATES:
    POOL += [t] * int(round(WEIGHT[DIFF_OF[t]] * 10))

attempts = 0
while len(questions) < 500 and attempts < 800000:
    attempts += 1
    t = random.choice(POOL)
    try:
        res = t()
    except Exception:
        continue
    if res is None:
        continue
    stem, correct, distractors, sol, diff, qtype = res
    add(stem, correct, distractors, sol, diff, qtype)

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
    if q["opts"][q["ci"]] is None:
        print(f"Q{i}: keyed option None"); errors += 1
stems = [q["stem"] for q in questions]
if len(set(stems)) != len(stems):
    print("DUPLICATE STEMS!"); errors += 1
assert len(questions) == 500, f"expected 500, got {len(questions)}"
assert errors == 0, f"{errors} self-check errors"
print(f"Self-check errors: {errors}")
print("Difficulty:", Counter(q["diff"] for q in questions))
print("Types:", Counter(q["qtype"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_03_Series_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_03_Series_500.key.json"

lines = []
lines.append("# Number & Alphabet Series — 500 Question Practice Set (SSC CGL, Reasoning / Tier-I & II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium - ~60% Hard - ~20% Very-Hard (2nd-level / interleaved / wrong-term) — CGL standard.")
lines.append("> **Every series is generated by an exact rule and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is -0.50; the distractors are real common-mistake values (off-by-one, wrong rule, adjacent term).\n")
lines.append("## How series questions work (quick reference)")
lines.append("- **Arithmetic:** constant difference between consecutive terms.")
lines.append("- **Geometric:** constant ratio (each term = previous x r).")
lines.append("- **2nd-level differences:** the differences themselves form a pattern (AP, or x constant).")
lines.append("- **Squares / cubes +/- k:** terms are n^2 or n^3, possibly shifted by a constant.")
lines.append("- **Interleaved:** two independent series alternate position by position.")
lines.append("- **Mixed operations:** alternate +n and xm, or term = previous x m + k.")
lines.append("- **Fibonacci-type:** each term = sum of the previous two.")
lines.append("- **Alphabet:** letters move by fixed/varying skips (A=1...Z=26); pairs like AZ, BY, CX use opposite letters (positions sum to 27).")
lines.append("- **Wrong-term:** all terms but one fit an exact rule; identify the one that breaks it.\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}-Q{start+50})\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        o = q["opts"]
        lines.append(f"**Q{n}.** {q['stem']}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    lines.append(f"\n## Answers Q{start+1}-Q{start+50}\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        letter = LETTERS[q["ci"]]
        val = q["opts"][q["ci"]]
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* — {q['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

sidecar = {str(j + 1): questions[j]["opts"][questions[j]["ci"]] for j in range(500)}
with open(SIDECAR, "w", encoding="utf-8") as f:
    json.dump(sidecar, f, indent=0)

print(f"Wrote {OUT}")
print(f"Wrote {SIDECAR}")
print(f"Total lines: {len(lines)}")
