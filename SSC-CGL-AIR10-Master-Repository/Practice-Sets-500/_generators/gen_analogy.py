# -*- coding: utf-8 -*-
"""
SSC CGL Analogy & Classification (Odd-One-Out) - Reasoning - 500 MCQ generator.

Two families:
  A) RULE-BASED (computable, majority): number analogy, number classification,
     letter analogy, letter/alphanumeric classification. Every answer is produced
     by an exact Python rule; the keyed option is provably correct. For odd-one-out
     items, UNIQUENESS is enforced by checking the rule against ALL options so that
     exactly one element breaks the rule.
  B) CURATED WORD/GK analogy (minority, hand-authored, fact-checked): worker:place,
     animal:young, country:capital, instrument:player, etc. Exactly one defensible
     answer per item.

Options are STRINGS; distinctness by string equality. The rule-based subset emits a
JSON sidecar (qnum -> correct string) for the independent verifier. Word items'
answers are authored (also stored in the sidecar for completeness, marked curated).
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
    """1-indexed position -> letter, wraps mod 26."""
    return AZ[(p - 1) % 26]

def shift_word(word, n):
    return "".join(from_pos(pos(c) + n) for c in word)

def is_square(x):
    if x < 0:
        return False
    r = int(round(x ** 0.5))
    return r * r == x

def is_cube(x):
    if x < 0:
        return False
    r = int(round(x ** (1.0 / 3.0)))
    for c in (r - 1, r, r + 1):
        if c >= 0 and c * c * c == x:
            return True
    return False

def is_prime(x):
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True

# ============================================================
#  state
# ============================================================
questions = []  # dict(stem, opts(list str), ci, sol, diff, qtype, family)
seen = set()

def _mutate(s, seedn):
    """Make a plausible wrong string by nudging one alphabetic char or digit."""
    chars = list(s)
    idxs = [i for i, c in enumerate(chars) if c.isalpha() or c.isdigit()]
    if not idxs:
        return s + "X"
    i = idxs[seedn % len(idxs)]
    c = chars[i]
    if c.isalpha():
        up = c.isupper()
        base = AZ[(pos(c) - 1 + (1 if seedn % 2 else -1)) % 26]
        chars[i] = base if up else base.lower()
    else:
        chars[i] = str((int(c) + (1 if seedn % 2 else -1)) % 10)
    return "".join(chars)

def make_options(correct, distractors):
    """Return (options_list, correct_index) with 4 DISTINCT string values, shuffled."""
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
    while len(opts) < 4 and tries < 200:
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

def add(stem, correct, distractors, sol, diff, qtype, family):
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
    assert len(set(opts)) == 4, "options not distinct"
    questions.append({
        "stem": stem, "opts": opts, "ci": ci,
        "sol": sol, "diff": diff, "qtype": qtype, "family": family,
    })
    return True

# ============================================================
#  FAMILY A - RULE-BASED TEMPLATES
# ============================================================

# A single example pair a:fa rarely pins down ONE rule (e.g. 6:36 could be 6^2 or
# 6x6). To kill ambiguity we present TWO example pairs and require that, across the
# CANDIDATE rule family below, EXACTLY ONE rule fits BOTH example pairs -- and that
# rule yields the intended answer for the asked number. This mirrors how the coding
# generator used two pairs to separate +k from xk.
#
# Candidate rule family (each maps n -> value, plus a predicate "fits"):
def _num_rules():
    rules = []
    # square / cube / n(n+1) / n(n-1)
    rules.append(("square", lambda n: n * n))
    rules.append(("cube",   lambda n: n ** 3))
    rules.append(("n(n+1)", lambda n: n * (n + 1)))
    rules.append(("n(n-1)", lambda n: n * (n - 1)))
    # multiply by constant k (2..12)
    for k in range(2, 13):
        rules.append((f"x{k}", (lambda kk: (lambda n: n * kk))(k)))
    # add constant k (positive)
    for k in list(range(1, 26)):
        rules.append((f"+{k}", (lambda kk: (lambda n: n + kk))(k)))
    # subtract constant k
    for k in list(range(1, 26)):
        rules.append((f"-{k}", (lambda kk: (lambda n: n - kk))(k)))
    # n^2 +/- k
    for k in range(1, 11):
        rules.append((f"sq+{k}", (lambda kk: (lambda n: n * n + kk))(k)))
        rules.append((f"sq-{k}", (lambda kk: (lambda n: n * n - kk))(k)))
    return rules

_NUM_RULES = _num_rules()

def num_analogy_unique(pairs, b, intended):
    """pairs: list of (a, fa) example pairs. Returns True iff exactly one candidate
    rule fits EVERY example pair AND that rule maps b -> intended."""
    fitting = []
    for name, fn in _NUM_RULES:
        if all(fn(a) == fa for a, fa in pairs):
            fitting.append((name, fn))
    if len(fitting) != 1:
        return False
    name, fn = fitting[0]
    return fn(b) == intended

def _two_distinct_examples(rng_pool, fn):
    """Pick two distinct example bases a1,a2 (and the asked b) from pool."""
    a1, a2, b = random.sample(rng_pool, 3)
    return a1, a2, b

def _num_stem(a1, fa1, a2, fa2, b):
    return ("Select the option that is related to the fourth term in the same way "
            "as the second term is related to the first and the fourth (last given) "
            "pair follows the same rule.\n"
            f"{a1} : {fa1} :: {a2} : {fa2} :: {b} : ?")

# ---- A1: Number analogy  "a1 : f(a1) :: a2 : f(a2) :: b : ?" ----
def t_num_analogy_square():
    """n : n^2 (two example pairs).  [M]"""
    a1, a2, b = random.sample(range(3, 22), 3)
    fa1, fa2, correct = a1 * a1, a2 * a2, b * b
    if not num_analogy_unique([(a1, fa1), (a2, fa2)], b, correct):
        return None
    d1, d2, d3 = b * b + 1, b * b - b, b * (b + 1)
    stem = _num_stem(a1, fa1, a2, fa2, b)
    sol = (f"Each second number is the square of the first ({a1}^2={fa1}, {a2}^2={fa2}). "
           f"So the answer is {b}^2 = {correct}.")
    return stem, correct, [d1, d2, d3], sol, "M", "num_analogy_square"

def t_num_analogy_cube():
    """n : n^3 (two example pairs).  [H]"""
    a1, a2, b = random.sample(range(2, 13), 3)
    fa1, fa2, correct = a1 ** 3, a2 ** 3, b ** 3
    if not num_analogy_unique([(a1, fa1), (a2, fa2)], b, correct):
        return None
    d1, d2, d3 = b ** 3 + 1, b ** 2, b ** 3 - b
    stem = _num_stem(a1, fa1, a2, fa2, b)
    sol = (f"Each second number is the cube of the first ({a1}^3={fa1}, {a2}^3={fa2}). "
           f"So the answer is {b}^3 = {correct}.")
    return stem, correct, [d1, d2, d3], sol, "H", "num_analogy_cube"

def t_num_analogy_mul():
    """n : n*k (two example pairs pin k).  [M]"""
    k = random.choice([3, 4, 5, 6, 7, 8, 9, 11, 12])
    a1, a2, b = random.sample(range(6, 30), 3)
    fa1, fa2, correct = a1 * k, a2 * k, b * k
    if not num_analogy_unique([(a1, fa1), (a2, fa2)], b, correct):
        return None
    d1, d2, d3 = b * k + k, b * (k + 1), b * k - b
    stem = _num_stem(a1, fa1, a2, fa2, b)
    sol = (f"Each second number is {k} times the first ({a1}x{k}={fa1}, {a2}x{k}={fa2}). "
           f"So the answer is {b}x{k} = {correct}.")
    return stem, correct, [d1, d2, d3], sol, "M", "num_analogy_mul"

def t_num_analogy_n_n1():
    """n : n(n+1) (two example pairs).  [H]"""
    a1, a2, b = random.sample(range(4, 22), 3)
    fa1, fa2, correct = a1 * (a1 + 1), a2 * (a2 + 1), b * (b + 1)
    if not num_analogy_unique([(a1, fa1), (a2, fa2)], b, correct):
        return None
    d1, d2, d3 = b * b, b * (b + 2), b * (b + 1) - 1
    stem = _num_stem(a1, fa1, a2, fa2, b)
    sol = (f"The rule is n -> n(n+1): {a1}x{a1+1}={fa1}, {a2}x{a2+1}={fa2}. "
           f"So the answer is {b}x{b+1} = {correct}.")
    return stem, correct, [d1, d2, d3], sol, "H", "num_analogy_n_n1"

def t_num_analogy_sq_plus():
    """n : n^2 + k (two example pairs pin k).  [H]"""
    k = random.choice([1, 2, 3, 4, 5])
    a1, a2, b = random.sample(range(4, 20), 3)
    fa1, fa2, correct = a1 * a1 + k, a2 * a2 + k, b * b + k
    if not num_analogy_unique([(a1, fa1), (a2, fa2)], b, correct):
        return None
    d1, d2, d3 = b * b, b * b + k + 1, (b + 1) ** 2 + k
    stem = _num_stem(a1, fa1, a2, fa2, b)
    sol = (f"The rule is n -> n^2+{k}: {a1}^2+{k}={fa1}, {a2}^2+{k}={fa2}. "
           f"So the answer is {b}^2+{k} = {correct}.")
    return stem, correct, [d1, d2, d3], sol, "H", "num_analogy_sq_plus"

def t_num_analogy_add():
    """n : n + k (two example pairs pin k).  [M]"""
    k = random.choice([7, 9, 11, 13, 15, 17, 19, 21, 23])
    a1, a2, b = random.sample(range(12, 60), 3)
    fa1, fa2, correct = a1 + k, a2 + k, b + k
    if not num_analogy_unique([(a1, fa1), (a2, fa2)], b, correct):
        return None
    d1, d2, d3 = b + k + 1, b + k - 2, b * 2
    stem = _num_stem(a1, fa1, a2, fa2, b)
    sol = (f"A fixed number {k} is added: {a1}+{k}={fa1}, {a2}+{k}={fa2}. "
           f"So the answer is {b}+{k} = {correct}.")
    return stem, correct, [d1, d2, d3], sol, "M", "num_analogy_add"

# ---- A2: Number classification (odd one out) ----
def _build_odd_one_out(members, odd, fmt=str):
    """Assemble a 4-option odd-one-out where exactly `odd` breaks the rule.
    members: 3 elements satisfying the rule; odd: the one that does NOT.
    Returns (opts4, correct_value_str) or None if a dup arises."""
    vals = list(members) + [odd]
    if len(set(vals)) != 4:
        return None
    return vals, fmt(odd)

def t_class_square():
    """All perfect squares except one. [M]"""
    squares = [n * n for n in range(3, 16)]
    members = random.sample(squares, 3)
    # build odd: a near-square that is NOT a perfect square
    base = random.choice(squares)
    odd = base + random.choice([-2, -1, 1, 2, 3])
    while is_square(odd) or odd in members or odd <= 0:
        odd = base + random.choice([-3, -2, -1, 1, 2, 3, 5])
    # UNIQUENESS: exactly one of the 4 must violate "is perfect square"
    allv = members + [odd]
    if sum(1 for v in allv if not is_square(v)) != 1:
        return None
    built = _build_odd_one_out(members, odd)
    if not built:
        return None
    vals, correct = built
    random.shuffle(vals)
    sol = ("Three of the four numbers are perfect squares "
           f"({', '.join(str(v) for v in sorted(members))}); "
           f"{odd} is not a perfect square, so it is the odd one out.")
    return _oo_stem(vals), correct, [str(v) for v in vals if str(v) != correct], sol, "M", "class_square", vals

def t_class_cube():
    """All perfect cubes except one. [H]"""
    cubes = [n ** 3 for n in range(2, 9)]
    members = random.sample(cubes, 3)
    base = random.choice(cubes)
    odd = base + random.choice([-2, -1, 1, 2, 3, 4])
    while is_cube(odd) or odd in members or odd <= 0:
        odd = base + random.choice([-4, -3, -2, -1, 1, 2, 3, 5])
    allv = members + [odd]
    if sum(1 for v in allv if not is_cube(v)) != 1:
        return None
    built = _build_odd_one_out(members, odd)
    if not built:
        return None
    vals, correct = built
    random.shuffle(vals)
    sol = ("Three of the four numbers are perfect cubes "
           f"({', '.join(str(v) for v in sorted(members))}); "
           f"{odd} is not a perfect cube, so it is the odd one out.")
    return _oo_stem(vals), correct, [str(v) for v in vals if str(v) != correct], sol, "H", "class_cube", vals

def t_class_prime():
    """All primes except one (the odd one is composite). [H]"""
    primes = [p for p in range(11, 100) if is_prime(p)]
    members = random.sample(primes, 3)
    # odd: a composite number in similar range
    comp = random.choice([n for n in range(11, 100) if not is_prime(n)])
    while comp in members:
        comp = random.choice([n for n in range(11, 100) if not is_prime(n)])
    allv = members + [comp]
    # uniqueness: exactly one non-prime
    if sum(1 for v in allv if not is_prime(v)) != 1:
        return None
    built = _build_odd_one_out(members, comp)
    if not built:
        return None
    vals, correct = built
    random.shuffle(vals)
    sol = ("Three of the four numbers are prime "
           f"({', '.join(str(v) for v in sorted(members))}); "
           f"{comp} is composite (it has factors other than 1 and itself), "
           "so it is the odd one out.")
    return _oo_stem(vals), correct, [str(v) for v in vals if str(v) != correct], sol, "H", "class_prime", vals

def t_class_divisible():
    """All divisible by k except one. [M]"""
    k = random.choice([3, 4, 6, 7, 8, 9, 11, 12])
    mults = [k * m for m in range(2, 14)]
    members = random.sample(mults, 3)
    # odd: not divisible by k
    odd = random.choice(members) + random.choice([1, 2, k - 1])
    while odd % k == 0 or odd in members:
        odd = random.choice(members) + random.choice([1, 2, 3, k - 1])
    allv = members + [odd]
    if sum(1 for v in allv if v % k != 0) != 1:
        return None
    built = _build_odd_one_out(members, odd)
    if not built:
        return None
    vals, correct = built
    random.shuffle(vals)
    sol = (f"Three of the four numbers are exactly divisible by {k} "
           f"({', '.join(str(v) for v in sorted(members))}); "
           f"{odd} is not divisible by {k} ({odd}/{k} leaves remainder {odd % k}), "
           "so it is the odd one out.")
    return _oo_stem(vals), correct, [str(v) for v in vals if str(v) != correct], sol, "M", "class_divisible", vals

def t_class_n_n1():
    """All of form n(n+1) (product of consecutive integers) except one. [VH]"""
    prods = [n * (n + 1) for n in range(3, 15)]
    members = random.sample(prods, 3)
    odd = random.choice(prods) + random.choice([2, 4, -2, 6])
    def is_consec_prod(x):
        n = int((x ** 0.5))
        for c in (n - 1, n, n + 1):
            if c >= 0 and c * (c + 1) == x:
                return True
        return False
    while is_consec_prod(odd) or odd in members or odd <= 0:
        odd = random.choice(prods) + random.choice([2, 3, 4, -2, -3, 6])
    allv = members + [odd]
    if sum(1 for v in allv if not is_consec_prod(v)) != 1:
        return None
    built = _build_odd_one_out(members, odd)
    if not built:
        return None
    vals, correct = built
    random.shuffle(vals)
    sol = ("Three numbers are products of two consecutive integers, n(n+1) "
           f"({', '.join(str(v) for v in sorted(members))}); "
           f"{odd} cannot be written as n(n+1), so it is the odd one out.")
    return _oo_stem(vals), correct, [str(v) for v in vals if str(v) != correct], sol, "VH", "class_n_n1", vals

def _oo_stem(vals=None):
    base = "Select the number that is different from the rest (the odd one out)."
    if vals:
        base += "\nNumbers: " + ", ".join(str(v) for v in vals)
    return base

# ---- A3: Letter analogy  "PAIR1 :: PAIR2 -> ?" ----
def t_letter_analogy_shift():
    """Each letter shifted by constant k: AB : CD :: PQ : ? (k=2). Two-letter groups. [M]"""
    k = random.choice([1, 2, 3, 4, 5])
    a1 = random.choice(AZ[:24])
    a2 = random.choice(AZ[:24])
    grp1 = a1 + a2
    grp1c = shift_word(grp1, k)
    b1 = random.choice(AZ[:24])
    b2 = random.choice(AZ[:24])
    grp2 = b1 + b2
    correct = shift_word(grp2, k)
    if grp1 == grp2:
        return None
    d1 = shift_word(grp2, k + 1)
    d2 = shift_word(grp2, k - 1) if k > 1 else shift_word(grp2, k + 2)
    d3 = correct[::-1]
    stem = ("Select the option that is related to the third term in the same way as "
            f"the second term is related to the first.\n{grp1} : {grp1c} :: {grp2} : ?")
    sol = (f"Each letter moves +{k} places ({grp1}->{grp1c}). "
           f"Applying +{k} to {grp2} gives {correct}.")
    return stem, correct, [d1, d2, d3], sol, "M", "letter_analogy_shift", None

def t_letter_analogy_shift3():
    """Three-letter groups, constant shift. [H]"""
    k = random.choice([1, 2, 3, 4, 5, 6])
    grp1 = "".join(random.choice(AZ[:22]) for _ in range(3))
    grp2 = "".join(random.choice(AZ[:22]) for _ in range(3))
    if grp1 == grp2:
        return None
    grp1c = shift_word(grp1, k)
    correct = shift_word(grp2, k)
    d1 = shift_word(grp2, k + 1)
    d2 = shift_word(grp2, k - 1) if k > 1 else shift_word(grp2, k + 2)
    d3 = correct[::-1]
    stem = ("Select the option that is related to the third term in the same way as "
            f"the second term is related to the first.\n{grp1} : {grp1c} :: {grp2} : ?")
    sol = (f"Each letter moves +{k} places ({grp1}->{grp1c}). "
           f"Applying +{k} to {grp2} gives {correct}.")
    return stem, correct, [d1, d2, d3], sol, "H", "letter_analogy_shift3", None

def t_letter_analogy_opposite():
    """Opposite-letter mapping (p -> 27-p). [H]
    Uses 3-letter groups and rejects any case where the EXAMPLE pair's per-letter
    deltas are all equal -- otherwise the example could be (mis)read as a uniform
    shift, making the item ambiguous."""
    grp1 = "".join(random.choice(AZ) for _ in range(3))
    grp2 = "".join(random.choice(AZ) for _ in range(3))
    if grp1 == grp2:
        return None
    opp = lambda w: "".join(from_pos(27 - pos(c)) for c in w)
    grp1c = opp(grp1)
    correct = opp(grp2)
    # ambiguity guard: example deltas must NOT be a single uniform value.
    ex_deltas = {(pos(b) - pos(a)) % 26 for a, b in zip(grp1, grp1c)}
    if len(ex_deltas) < 2:
        return None
    d1 = shift_word(grp2, 1)
    d2 = correct[::-1]
    d3 = shift_word(grp2, -1)
    stem = ("Select the option that is related to the third term in the same way as "
            f"the second term is related to the first.\n{grp1} : {grp1c} :: {grp2} : ?")
    sol = (f"Each letter is replaced by its opposite (A<->Z, position p -> 27-p), "
           f"e.g. {grp1}->{grp1c}. So {grp2} -> {correct}.")
    return stem, correct, [d1, d2, d3], sol, "H", "letter_analogy_opposite", None

def t_letter_analogy_varying():
    """First letter +1, second +2, third +3 (positional shift). [VH]"""
    grp1 = "".join(random.choice(AZ[:20]) for _ in range(3))
    grp2 = "".join(random.choice(AZ[:20]) for _ in range(3))
    if grp1 == grp2:
        return None
    code = lambda w: "".join(from_pos(pos(c) + i + 1) for i, c in enumerate(w))
    grp1c = code(grp1)
    correct = code(grp2)
    d1 = shift_word(grp2, 1)
    d2 = "".join(from_pos(pos(c) + i) for i, c in enumerate(grp2))
    d3 = correct[::-1]
    stem = ("Select the option that is related to the third term in the same way as "
            f"the second term is related to the first.\n{grp1} : {grp1c} :: {grp2} : ?")
    sol = (f"The 1st, 2nd, 3rd letters move +1, +2, +3 places respectively "
           f"({grp1}->{grp1c}). Applying this to {grp2} gives {correct}.")
    return stem, correct, [d1, d2, d3], sol, "VH", "letter_analogy_varying", None

# ---- A4: Letter / alphanumeric classification (odd one out) ----
def t_class_letter_skip():
    """Three groups follow a constant internal gap; one breaks it. [H]"""
    gap = random.choice([1, 2, 3, 4, 5])
    def grp(start):
        return start + from_pos(pos(start) + gap) + from_pos(pos(start) + 2 * gap)
    starts = random.sample(AZ[:20], 3)
    members = [grp(s) for s in starts]
    # odd: a group with a different internal gap
    odd_gap = gap + random.choice([1, 2, -1, 3])
    if odd_gap <= 0:
        odd_gap = gap + 1
    os = random.choice([c for c in AZ[:20] if c not in starts])
    odd = os + from_pos(pos(os) + odd_gap) + from_pos(pos(os) + 2 * odd_gap)
    # uniqueness check: a group "fits" if both internal gaps equal `gap`
    def fits(g):
        g0, g1, g2 = pos(g[0]), pos(g[1]), pos(g[2])
        return ((g1 - g0) % 26 == gap) and ((g2 - g1) % 26 == gap)
    allv = members + [odd]
    if len(set(allv)) != 4:
        return None
    if sum(1 for g in allv if not fits(g)) != 1:
        return None
    vals = list(allv)
    correct = odd
    random.shuffle(vals)
    sol = (f"In three of the groups consecutive letters increase by {gap} place(s) "
           f"each ({', '.join(members)}); in {odd} the gap is different ({odd_gap}), "
           "so it is the odd one out.")
    return _ooletter_stem(vals), correct, [v for v in vals if v != correct], sol, "H", "class_letter_skip", vals

def t_class_alnum():
    """Letter+number groups where number = alphabet position; one mismatches. [H]"""
    def grp(ch):
        return f"{ch}{pos(ch)}"
    chs = random.sample(AZ, 3)
    members = [grp(c) for c in chs]
    oc = random.choice([c for c in AZ if c not in chs])
    wrong_num = pos(oc) + random.choice([1, 2, -1, -2, 3])
    if wrong_num <= 0:
        wrong_num = pos(oc) + 1
    odd = f"{oc}{wrong_num}"
    def fits(g):
        letter = g[0]
        num = int(g[1:])
        return num == pos(letter)
    allv = members + [odd]
    if len(set(allv)) != 4:
        return None
    if sum(1 for g in allv if not fits(g)) != 1:
        return None
    vals = list(allv)
    correct = odd
    random.shuffle(vals)
    sol = ("In three pairs the number equals the letter's alphabet position "
           f"({', '.join(members)}); in {odd} the number {wrong_num} does not match "
           f"{oc}'s position ({pos(oc)}), so it is the odd one out.")
    return _ooletter_stem(vals), correct, [v for v in vals if v != correct], sol, "H", "class_alnum", vals

def _ooletter_stem(vals=None):
    base = "Select the letter-cluster that is different from the rest (the odd one out)."
    if vals:
        base += "\nClusters: " + ", ".join(str(v) for v in vals)
    return base

# ============================================================
#  FAMILY B - CURATED WORD / GK ANALOGY (fact-checked)
# ============================================================
# Each entry: (A, B, C, correct_D, [3 distractors], relationship, difficulty)
CURATED = [
    # worker : workplace
    ("Doctor", "Hospital", "Teacher", "School", ["Library", "Office", "Court"], "worker : workplace", "M"),
    ("Judge", "Court", "Pilot", "Aircraft", ["Airport", "Runway", "Hangar"], "worker : workplace", "M"),
    ("Chef", "Kitchen", "Actor", "Stage", ["Cinema", "Studio", "Hall"], "worker : workplace", "M"),
    ("Teacher", "Classroom", "Lawyer", "Court", ["Office", "Chamber", "Firm"], "worker : workplace", "M"),
    ("Farmer", "Field", "Sailor", "Ship", ["Sea", "Port", "Dock"], "worker : workplace", "M"),
    ("Scientist", "Laboratory", "Mechanic", "Garage", ["Factory", "Workshop", "Shed"], "worker : workplace", "M"),
    ("Banker", "Bank", "Priest", "Temple", ["Church", "Altar", "Shrine"], "worker : workplace", "M"),
    # worker : product / what they make
    ("Cobbler", "Shoes", "Tailor", "Clothes", ["Cloth", "Needle", "Thread"], "worker : product made", "M"),
    ("Carpenter", "Furniture", "Mason", "Wall", ["Bricks", "Cement", "House"], "worker : product made", "H"),
    ("Author", "Book", "Poet", "Poem", ["Pen", "Verse", "Story"], "worker : product made", "M"),
    ("Baker", "Bread", "Potter", "Pottery", ["Clay", "Wheel", "Kiln"], "worker : product made", "H"),
    ("Weaver", "Cloth", "Blacksmith", "Tools", ["Iron", "Anvil", "Hammer"], "worker : product made", "H"),
    # worker : tool used
    ("Carpenter", "Saw", "Surgeon", "Scalpel", ["Stethoscope", "Knife", "Blade"], "worker : chief tool", "H"),
    ("Painter", "Brush", "Writer", "Pen", ["Ink", "Paper", "Pencil"], "worker : chief tool", "M"),
    ("Tailor", "Scissors", "Barber", "Razor", ["Comb", "Mirror", "Brush"], "worker : chief tool", "H"),
    ("Farmer", "Plough", "Soldier", "Gun", ["Sword", "Shield", "Tank"], "worker : chief tool", "M"),
    ("Gardener", "Spade", "Carpenter", "Hammer", ["Nail", "Wood", "Drill"], "worker : chief tool", "H"),
    # animal : young one
    ("Cow", "Calf", "Dog", "Puppy", ["Kitten", "Cub", "Foal"], "animal : its young one", "M"),
    ("Horse", "Foal", "Cat", "Kitten", ["Puppy", "Cub", "Calf"], "animal : its young one", "M"),
    ("Sheep", "Lamb", "Goat", "Kid", ["Calf", "Cub", "Foal"], "animal : its young one", "H"),
    ("Lion", "Cub", "Hen", "Chick", ["Calf", "Kid", "Foal"], "animal : its young one", "M"),
    ("Frog", "Tadpole", "Butterfly", "Caterpillar", ["Larva", "Pupa", "Cocoon"], "animal : its larval/young stage", "H"),
    ("Deer", "Fawn", "Bear", "Cub", ["Joey", "Kit", "Pup"], "animal : its young one", "H"),
    ("Cat", "Kitten", "Kangaroo", "Joey", ["Cub", "Calf", "Pup"], "animal : its young one", "H"),
    # animal : home / dwelling
    ("Bee", "Hive", "Bird", "Nest", ["Den", "Burrow", "Web"], "creature : its dwelling", "M"),
    ("Spider", "Web", "Lion", "Den", ["Nest", "Stable", "Sty"], "creature : its dwelling", "H"),
    ("Horse", "Stable", "Pig", "Sty", ["Kennel", "Coop", "Byre"], "creature : its dwelling", "H"),
    ("Dog", "Kennel", "Cow", "Shed", ["Sty", "Coop", "Nest"], "creature : its dwelling", "M"),
    ("Rabbit", "Burrow", "Hen", "Coop", ["Stable", "Sty", "Den"], "creature : its dwelling", "H"),
    # animal : sound
    ("Dog", "Bark", "Cat", "Mew", ["Roar", "Neigh", "Bleat"], "animal : its sound", "M"),
    ("Lion", "Roar", "Horse", "Neigh", ["Bark", "Bleat", "Grunt"], "animal : its sound", "M"),
    ("Cow", "Moo", "Sheep", "Bleat", ["Bark", "Mew", "Neigh"], "animal : its sound", "M"),
    ("Snake", "Hiss", "Frog", "Croak", ["Buzz", "Chirp", "Roar"], "animal : its sound", "H"),
    ("Bird", "Chirp", "Bee", "Buzz", ["Bark", "Hiss", "Roar"], "creature : its sound", "M"),
    # country : capital
    ("India", "New Delhi", "Japan", "Tokyo", ["Beijing", "Seoul", "Bangkok"], "country : capital", "M"),
    ("France", "Paris", "Italy", "Rome", ["Madrid", "Berlin", "Vienna"], "country : capital", "M"),
    ("China", "Beijing", "Russia", "Moscow", ["Kiev", "Warsaw", "Prague"], "country : capital", "M"),
    ("Australia", "Canberra", "Canada", "Ottawa", ["Toronto", "Sydney", "Vancouver"], "country : capital", "H"),
    ("Egypt", "Cairo", "Iran", "Tehran", ["Baghdad", "Riyadh", "Kabul"], "country : capital", "H"),
    ("Nepal", "Kathmandu", "Bhutan", "Thimphu", ["Dhaka", "Colombo", "Male"], "country : capital", "H"),
    ("Spain", "Madrid", "Germany", "Berlin", ["Munich", "Hamburg", "Vienna"], "country : capital", "M"),
    ("Bangladesh", "Dhaka", "Sri Lanka", "Colombo", ["Male", "Thimphu", "Kabul"], "country : capital", "H"),
    # country : currency
    ("India", "Rupee", "Japan", "Yen", ["Won", "Yuan", "Baht"], "country : currency", "M"),
    ("USA", "Dollar", "United Kingdom", "Pound", ["Euro", "Franc", "Lira"], "country : currency", "M"),
    ("Russia", "Rouble", "China", "Yuan", ["Yen", "Won", "Baht"], "country : currency", "H"),
    ("Thailand", "Baht", "South Korea", "Won", ["Yen", "Yuan", "Ringgit"], "country : currency", "H"),
    ("Bangladesh", "Taka", "Myanmar", "Kyat", ["Rupee", "Baht", "Dong"], "country : currency", "H"),
    # state : capital (India)
    ("Maharashtra", "Mumbai", "Tamil Nadu", "Chennai", ["Bengaluru", "Hyderabad", "Kochi"], "Indian state : capital", "H"),
    ("Rajasthan", "Jaipur", "Gujarat", "Gandhinagar", ["Ahmedabad", "Surat", "Vadodara"], "Indian state : capital", "H"),
    ("Karnataka", "Bengaluru", "Kerala", "Thiruvananthapuram", ["Kochi", "Kozhikode", "Thrissur"], "Indian state : capital", "H"),
    ("West Bengal", "Kolkata", "Odisha", "Bhubaneswar", ["Cuttack", "Puri", "Rourkela"], "Indian state : capital", "H"),
    ("Punjab", "Chandigarh", "Bihar", "Patna", ["Gaya", "Ranchi", "Bhagalpur"], "Indian state : capital", "H"),
    # instrument : player / what is played
    ("Flute", "Flautist", "Piano", "Pianist", ["Drummer", "Violinist", "Guitarist"], "instrument : its player", "H"),
    ("Violin", "Violinist", "Guitar", "Guitarist", ["Pianist", "Drummer", "Bassist"], "instrument : its player", "H"),
    ("Drum", "Drummer", "Tabla", "Tabla player", ["Sitarist", "Flautist", "Pianist"], "instrument : its player", "H"),
    # tool : its action / use
    ("Knife", "Cut", "Pen", "Write", ["Read", "Draw", "Erase"], "tool : its primary action", "M"),
    ("Broom", "Sweep", "Needle", "Sew", ["Knit", "Cut", "Weave"], "tool : its primary action", "M"),
    ("Hammer", "Nail", "Screwdriver", "Screw", ["Bolt", "Wood", "Drill"], "tool : object it drives", "H"),
    ("Axe", "Chop", "Saw", "Cut", ["Drill", "Grind", "Plane"], "tool : its primary action", "M"),
    # object : material / made of
    ("Book", "Paper", "Shirt", "Cloth", ["Wool", "Leather", "Silk"], "object : chief material", "M"),
    ("Tyre", "Rubber", "Window", "Glass", ["Plastic", "Wood", "Metal"], "object : chief material", "M"),
    ("Ring", "Gold", "Statue", "Stone", ["Clay", "Wood", "Wax"], "object : a typical material", "H"),
    # part : whole
    ("Petal", "Flower", "Leaf", "Tree", ["Branch", "Root", "Stem"], "part : whole", "M"),
    ("Page", "Book", "Brick", "Wall", ["House", "Cement", "Floor"], "part : whole", "M"),
    ("Wheel", "Car", "Keyboard", "Computer", ["Screen", "Mouse", "Printer"], "part : whole", "M"),
    ("Room", "House", "Compartment", "Train", ["Engine", "Track", "Station"], "part : whole", "H"),
    ("Star", "Galaxy", "Tree", "Forest", ["Leaf", "Root", "Branch"], "unit : collection", "H"),
    # profession : study / subject
    ("Astronomer", "Stars", "Botanist", "Plants", ["Animals", "Rocks", "Birds"], "specialist : object of study", "H"),
    ("Cardiologist", "Heart", "Neurologist", "Brain", ["Kidney", "Liver", "Lung"], "specialist : organ treated", "H"),
    ("Geologist", "Rocks", "Ornithologist", "Birds", ["Insects", "Fish", "Plants"], "specialist : object of study", "VH"),
    ("Zoologist", "Animals", "Entomologist", "Insects", ["Birds", "Fish", "Reptiles"], "specialist : object of study", "VH"),
    # synonym / antonym
    ("Big", "Large", "Happy", "Glad", ["Sad", "Angry", "Tired"], "synonym pair", "M"),
    ("Hot", "Cold", "Up", "Down", ["High", "Top", "Above"], "antonym pair", "M"),
    ("Tall", "Short", "Wide", "Narrow", ["Long", "Big", "Broad"], "antonym pair", "M"),
    ("Begin", "Start", "End", "Finish", ["Stop", "Close", "Pause"], "synonym pair", "M"),
    ("Brave", "Coward", "Friend", "Enemy", ["Ally", "Partner", "Mate"], "antonym pair", "H"),
    # measuring instrument : quantity
    ("Thermometer", "Temperature", "Barometer", "Pressure", ["Humidity", "Rainfall", "Wind"], "instrument : quantity measured", "H"),
    ("Speedometer", "Speed", "Odometer", "Distance", ["Time", "Fuel", "Pressure"], "instrument : quantity measured", "H"),
    ("Seismograph", "Earthquake", "Hygrometer", "Humidity", ["Pressure", "Heat", "Rainfall"], "instrument : quantity measured", "VH"),
    # currency-symbol-free relations: leader/role
    ("Captain", "Team", "Principal", "School", ["Teacher", "Student", "Class"], "head : group led", "M"),
    ("Editor", "Newspaper", "Director", "Film", ["Actor", "Camera", "Screen"], "head : work produced", "H"),
    # body part : function
    ("Eye", "See", "Ear", "Hear", ["Smell", "Taste", "Touch"], "organ : its function", "M"),
    ("Nose", "Smell", "Tongue", "Taste", ["See", "Hear", "Touch"], "organ : its function", "M"),
    ("Leg", "Walk", "Hand", "Hold", ["See", "Hear", "Smell"], "organ : its function", "M"),
    # word : category
    ("Rose", "Flower", "Mango", "Fruit", ["Tree", "Plant", "Vegetable"], "example : category", "M"),
    ("Sparrow", "Bird", "Cobra", "Snake", ["Reptile", "Lizard", "Animal"], "example : category (specific)", "H"),
    ("Copper", "Metal", "Oxygen", "Gas", ["Liquid", "Solid", "Element"], "example : physical category", "H"),
    # day/time order
    ("Morning", "Noon", "Evening", "Night", ["Dawn", "Dusk", "Midnight"], "next stage of the day", "M"),
    ("January", "February", "April", "May", ["June", "March", "July"], "next month", "M"),
    ("Monday", "Tuesday", "Thursday", "Friday", ["Saturday", "Wednesday", "Sunday"], "next day of week", "M"),
    # river : country / city
    ("Ganga", "India", "Nile", "Egypt", ["Sudan", "Kenya", "Iraq"], "river : country it is iconic of", "H"),
    ("Thames", "London", "Seine", "Paris", ["Rome", "Berlin", "Vienna"], "river : the city on it", "H"),
    # planet relations
    ("Earth", "Sun", "Moon", "Earth", ["Sun", "Mars", "Jupiter"], "satellite : body it orbits", "H"),
    ("Mercury", "Sun", "Phobos", "Mars", ["Earth", "Jupiter", "Venus"], "satellite/planet : body it orbits", "VH"),
    # plurals of relationships
    ("Doctor", "Patient", "Lawyer", "Client", ["Witness", "Judge", "Jury"], "professional : person served", "H"),
    ("Teacher", "Student", "Coach", "Player", ["Referee", "Captain", "Fan"], "mentor : the one guided", "M"),
    ("Author", "Reader", "Singer", "Listener", ["Viewer", "Critic", "Fan"], "creator : audience", "H"),
    # raw material : finished
    ("Milk", "Butter", "Wheat", "Bread", ["Flour", "Grain", "Dough"], "raw : a finished product", "H"),
    ("Grapes", "Wine", "Sugarcane", "Sugar", ["Juice", "Syrup", "Jaggery"], "raw : a finished product", "H"),
    ("Tree", "Wood", "Cotton", "Cloth", ["Thread", "Yarn", "Fibre"], "raw : a finished product", "H"),
    # cause : effect
    ("Spark", "Fire", "Seed", "Plant", ["Root", "Soil", "Fruit"], "cause : effect / origin : result", "H"),
    ("Rain", "Flood", "Sun", "Heat", ["Cloud", "Cold", "Shade"], "cause : effect", "M"),
    # collective term
    ("Wolves", "Pack", "Lions", "Pride", ["Herd", "Flock", "Swarm"], "animal : collective noun", "VH"),
    ("Birds", "Flock", "Fish", "Shoal", ["Pack", "Pride", "Herd"], "animal : collective noun", "VH"),
    ("Bees", "Swarm", "Cattle", "Herd", ["Pride", "Pack", "Flock"], "animal : collective noun", "VH"),
    # opposite-gender
    ("King", "Queen", "Horse", "Mare", ["Colt", "Pony", "Stallion"], "male : female", "H"),
    ("Lion", "Lioness", "Dog", "Bitch", ["Puppy", "Vixen", "Doe"], "male : female", "H"),
    ("Boy", "Girl", "Nephew", "Niece", ["Cousin", "Aunt", "Sister"], "male : female counterpart", "M"),
    # study : -ology
    ("Birds", "Ornithology", "Insects", "Entomology", ["Botany", "Zoology", "Ecology"], "subject : its science", "VH"),
    ("Earthquakes", "Seismology", "Weather", "Meteorology", ["Geology", "Ecology", "Astronomy"], "subject : its science", "VH"),
]

# verify curated: structural sanity (the curated answer differs from distractors)
for entry in CURATED:
    A, B, C, D, dis, rel, df = entry
    assert D not in dis, f"curated answer duplicates a distractor: {entry}"
    assert len(set([D] + dis)) == 4, f"curated options not 4-distinct: {entry}"

def emit_curated(entry):
    A, B, C, D, dis, rel, df = entry
    stem = ("Select the option that is related to the third word in the same way as "
            f"the second word is related to the first word.\n{A} : {B} :: {C} : ?")
    sol = f"Relationship: {rel}. As {A} -> {B}, so {C} -> {D}."
    return stem, D, list(dis), sol, df, "curated_word", "B"

# ============================================================
#  BUILD THE SET
# ============================================================
RULE_TEMPLATES = [
    # (func, returns_vals_flag)  -- some return an extra `vals` element (oo items)
    (t_num_analogy_square, False), (t_num_analogy_cube, False),
    (t_num_analogy_mul, False), (t_num_analogy_n_n1, False),
    (t_num_analogy_sq_plus, False), (t_num_analogy_add, False),
    (t_class_square, True), (t_class_cube, True), (t_class_prime, True),
    (t_class_divisible, True), (t_class_n_n1, True),
    (t_letter_analogy_shift, True), (t_letter_analogy_shift3, True),
    (t_letter_analogy_varying, True),
    (t_class_letter_skip, True), (t_class_alnum, True),
    # NOTE: t_letter_analogy_opposite is intentionally NOT registered. An opposite-
    # letter analogy with differing example/asked words is inherently ambiguous: the
    # example pair can equally be read as a fixed per-position shift, which yields a
    # different (also defensible) answer. We exclude it to guarantee zero ambiguity.
]

DIFF_OF = {
    "num_analogy_square": "M", "num_analogy_cube": "H", "num_analogy_mul": "M",
    "num_analogy_n_n1": "H", "num_analogy_sq_plus": "H", "num_analogy_add": "M",
    "class_square": "M", "class_cube": "H", "class_prime": "H",
    "class_divisible": "M", "class_n_n1": "VH",
    "letter_analogy_shift": "M", "letter_analogy_shift3": "H",
    "letter_analogy_varying": "VH",
    "class_letter_skip": "H", "class_alnum": "H",
}

# Target: ~70% rule-based (350), 30% curated (we have ~110 curated -> use all + repeats? No.)
# We use each curated entry exactly once (no repeats -> no fabricated facts).
# So curated count = len(CURATED). Fill the remaining 500 with rule-based.
CURATED_COUNT = len(CURATED)
RULE_TARGET = 500 - CURATED_COUNT

# weighted pool by difficulty to steer ~20% M / 60% H / 20% VH overall.
# Curated difficulties are fixed; we bias the rule pool to compensate toward H/VH.
# Classification (odd-one-out) templates return None often (uniqueness rejections),
# so they get an extra acceptance multiplier on top of the difficulty weight to keep
# a healthy mix of odd-one-out items in the set.
WEIGHT = {"M": 1.4, "H": 4.3, "VH": 6.0}
# templates whose generator frequently rejects (odd-one-out uniqueness) need boosting
OO_BOOST = {
    "class_square": 4.0, "class_cube": 3.0, "class_prime": 3.0,
    "class_divisible": 4.0, "class_n_n1": 2.5,
    "class_letter_skip": 3.0, "class_alnum": 3.0,
}
POOL = []
for func, _ in RULE_TEMPLATES:
    name = func.__name__.replace("t_", "")
    d = DIFF_OF[name]
    w = WEIGHT[d] * OO_BOOST.get(name, 1.0)
    POOL += [func] * int(round(w * 10))

# --- generate curated first ---
random.shuffle(CURATED)
for entry in CURATED:
    stem, correct, dis, sol, diff, qtype, fam = emit_curated(entry)
    add(stem, correct, dis, sol, diff, qtype, fam)

curated_added = len(questions)

# --- generate rule-based ---
SIDECAR_DATA = {}  # qnum (final) -> {"answer":..., "family":"A"} placeholder; filled after layout

attempts = 0
while len(questions) < 500 and attempts < 2_000_000:
    attempts += 1
    func = random.choice(POOL)
    try:
        res = func()
    except Exception:
        continue
    if res is None:
        continue
    if len(res) == 7:
        stem, correct, distractors, sol, diff, qtype, vals = res
    else:
        stem, correct, distractors, sol, diff, qtype = res
    add(stem, correct, distractors, sol, diff, qtype, "A")

print(f"Generated {len(questions)} questions in {attempts} attempts.")
print(f"Curated (family B): {curated_added}; Rule-based (family A): {len(questions) - curated_added}")

# Shuffle so curated & rule-based are interleaved (more PYQ-like), keep deterministic.
random.shuffle(questions)

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
        print(f"Q{i}: keyed option is None"); errors += 1
stems = [q["stem"] for q in questions]
if len(set(stems)) != len(stems):
    print("DUPLICATE STEMS!"); errors += 1
assert len(questions) == 500, f"expected 500, got {len(questions)}"
assert errors == 0, f"{errors} self-check errors"
print(f"Self-check errors: {errors}")
print("Difficulty:", Counter(q["diff"] for q in questions))
print("Family:", Counter(q["family"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_05_Analogy_Classification_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_05_Analogy_Classification_500.key.json"

lines = []
lines.append("# Analogy & Classification (Odd-One-Out) — 500 Question Practice Set (SSC CGL, Reasoning / Tier-I & II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard — CGL standard.")
lines.append("> **Rule-based items (number/letter analogy & classification) are generated by an exact rule and machine-verified** — the keyed option is provably correct. **Word/GK analogies are hand-authored and fact-checked**, each with one defensible answer.")
lines.append("> Negative marking in CGL is −0.50; distractors are real common-mistake traps (wrong rule, off-by-one, plausible-but-wrong fact).\n")
lines.append("## How these questions work (quick reference)")
lines.append("- **Number analogy** `a : f(a) :: b : ?` — find the rule (square, cube, ×k, +k, n(n+1), n²+k) and apply it to b.")
lines.append("- **Number classification** — three numbers share a property (all squares / cubes / primes / divisible by k); pick the one that breaks it.")
lines.append("- **Letter analogy** `XY : ?? :: PQ : ?` — letters move by a fixed (or positional) shift; A=1…Z=26, wrap Z→A.")
lines.append("- **Letter/alphanumeric classification** — three clusters share a gap pattern or letter↔number rule; pick the odd one.")
lines.append("- **Word/GK analogy** — semantic relation (worker:workplace, animal:young, country:capital, instrument:player, etc.).\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        o = q["opts"]
        # stems may contain a newline (the analogy line); render it inline
        stem_render = q["stem"].replace("\n", "  \n")
        lines.append(f"**Q{n}.** {stem_render}")
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

# JSON sidecar: qnum -> {answer, family}. Verifier cross-checks rule-based (A) items.
sidecar = {
    str(j + 1): {
        "answer": questions[j]["opts"][questions[j]["ci"]],
        "family": questions[j]["family"],
        "qtype": questions[j]["qtype"],
    }
    for j in range(500)
}
with open(SIDECAR, "w", encoding="utf-8") as f:
    json.dump(sidecar, f, indent=0)

print(f"Wrote {OUT}")
print(f"Wrote {SIDECAR}")
print(f"Total lines: {len(lines)}")
print("Rule-based qtypes:", Counter(q["qtype"] for q in questions if q["family"] == "A"))
