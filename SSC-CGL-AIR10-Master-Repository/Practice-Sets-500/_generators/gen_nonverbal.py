# -*- coding: utf-8 -*-
"""
SSC CGL Non-Verbal Reasoning - 500 MCQ generator (TEXT-REPRESENTABLE subset).

Figures cannot be drawn in markdown, so this set is restricted to the subset of
non-verbal reasoning whose answers are UNAMBIGUOUS and COMPUTABLE from a precise
text description.  Every answer is produced by an exact Python function, so the
keyed option is provably correct.  A JSON sidecar (qnum -> correct string) is
emitted for the independent verifier.

Conventions used (also printed in the markdown intro note):

  MIRROR IMAGE of a letter/number string  -- reflection about a VERTICAL line.
      Standard CGL convention: the order of characters is reversed left-to-right.
      We use strings made of the vertically-symmetric capital letters
      {A,H,I,M,O,T,U,V,W,X,Y} and digits {0,1,8} so that each individual glyph
      is unchanged by a vertical mirror and ONLY the left-right order flips.
      => mirror("WAX") = "XAW".  This is exact and computable.

  WATER IMAGE of a letter/number string  -- reflection about a HORIZONTAL line.
      Standard CGL convention: the left-to-right order is UNCHANGED; each glyph
      flips top-to-bottom.  We use strings made only of glyphs that are
      vertically (top-bottom) symmetric: letters {B,C,D,E,H,I,K,O,X} and digits
      {0,1,3,8}.  For these glyphs the water image is the SAME string.  To keep
      it non-trivial and still computable we instead ask water-image questions
      using the subset where the glyph is unchanged, so the water image equals
      the original string -- and we verify that claim.  (Used sparingly.)

  DICE  -- a standard cube.  Given two surface views (each = top face + two
      adjacent side faces in clockwise order) we deduce, by the rule that any
      face NOT seen sharing an edge with a given face must be checked across
      both views, the face OPPOSITE to a queried face.  Fully computable.

  COUNTING FIGURES -- the figure is described precisely in words and the count
      follows a closed-form formula:
        * squares in an n x n grid of unit squares = sum_{k=1}^{n} k^2.
        * rectangles in an m x n grid               = C(m+1,2) * C(n+1,2).
        * triangles in a triangle divided by lines parallel to all three sides
          into n rows of small triangles:
              n even : n(n+2)(2n+1)/8
              n odd  : (n(n+2)(2n+1) - 1)/8
        * line segments / total triangles in a "fan" of k cevians, etc.

  PAPER FOLDING (punching) -- a square sheet folded f times then a single punch
      through all layers yields 2^f holes when unfolded (clean symmetric folds).
      Generalised: p punches through L layers -> p * L holes.  Computable.

  SERIES / ANALOGY of letter-strings under an exact transform (rotate, reverse,
      shift) -- computable.

  EMBEDDED (letter form) -- whether a short string occurs contiguously inside a
      longer string; count occurrences -- computable.
"""
import random
import json
from collections import Counter
from math import comb

random.seed(20260625)  # deterministic

LETTERS = "abcd"
AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Glyph sets ----------------------------------------------------------------
# Vertically-symmetric (unchanged by a VERTICAL mirror) capitals + digits.
VMIRROR_SAFE = "AHIMOTUVWXY"          # left-right symmetric glyphs
VMIRROR_SAFE_DIG = "018"
# Horizontally-symmetric (unchanged by a HORIZONTAL/water mirror).
WATER_SAFE = "BCDEHIKOX"             # top-bottom symmetric glyphs
WATER_SAFE_DIG = "0138"

def pos(ch):
    return ord(ch) - ord('A') + 1

def from_pos(p):
    return AZ[(p - 1) % 26]

def shift_word(word, n):
    return "".join(from_pos(pos(c) + n) for c in word)

# ---------------- option / dedupe machinery (string based) ----------------
def _mutate(s, seedn):
    """Deterministically perturb a string to make a distinct filler distractor."""
    chars = list(s)
    idxs = [i for i, c in enumerate(chars) if c.isalpha() or c.isdigit()]
    if not idxs:
        return s + "X"
    i = idxs[seedn % len(idxs)]
    c = chars[i]
    if c.isalpha():
        up = c.isupper()
        base = AZ[(pos(c.upper()) - 1 + (1 if seedn % 2 else -1)) % 26]
        chars[i] = base if up else base.lower()
    else:
        chars[i] = str((int(c) + (1 if seedn % 2 else -1)) % 10)
    return "".join(chars)

def make_options(correct, distractors):
    """Return (options_list, correct_index) with 4 DISTINCT string values."""
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
    while len(opts) < 4 and tries < 400:
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

def _num_distractors(correct, candidates):
    """Return 3 distinct integer-string distractors != correct, drawn from the
    given candidate list first, then padded with nearby integers. Guarantees
    clean numeric options (no _mutate fillers)."""
    correct = int(correct)
    out = []
    for c in candidates:
        c = int(c)
        if c != correct and c > 0 and c not in out:
            out.append(c)
        if len(out) == 3:
            break
    delta = 1
    while len(out) < 3:
        for cand in (correct + delta, correct - delta):
            if cand > 0 and cand != correct and cand not in out:
                out.append(cand)
                if len(out) == 3:
                    break
        delta += 1
    return [str(x) for x in out[:3]]

questions = []  # dict(stem, opts, ci, sol, diff, qtype)
seen = set()

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

# =========================================================================
#  TEMPLATES
# =========================================================================

# ---- 1. MIRROR IMAGE of a vertically-symmetric string -> reverse order ----
def _rand_vmirror_string(minlen=4, maxlen=7):
    n = random.randint(minlen, maxlen)
    pool = VMIRROR_SAFE + VMIRROR_SAFE_DIG
    return "".join(random.choice(pool) for _ in range(n))

def t_mirror_string():
    """Mirror image (vertical line) of a symmetric-glyph string = reversed string."""
    s = _rand_vmirror_string()
    while s == s[::-1]:                # avoid palindrome (ambiguous distractor)
        s = _rand_vmirror_string()
    correct = s[::-1]
    d1 = s                              # forgot to reverse
    d2 = s[1:] + s[:1]                  # rotated
    d3 = correct[1:] + correct[:1]      # rotated reverse
    stem = (f"All the characters below are drawn from the set of glyphs that look "
            f"the SAME under a vertical mirror (so only their left-right order "
            f"changes). What is the MIRROR IMAGE (reflection about a vertical line "
            f"held to the right) of the string '{s}'?")
    diff = "M" if len(s) <= 5 else "H"
    sol = (f"Each glyph in '{s}' is vertically symmetric, so a vertical mirror only "
           f"reverses the left-to-right order. Reverse '{s}' -> '{correct}'.")
    return stem, correct, [d1, d2, d3], sol, diff, "mirror_string"

def t_mirror_choose_letter():
    """Which single capital letter looks the SAME in a vertical mirror? (concept)"""
    same = list("AHIMOTUVWXY")
    diffr = [c for c in AZ if c not in same]
    correct = random.choice(same)
    d = random.sample(diffr, 3)
    stem = ("Under reflection about a vertical line (mirror image), which one of the "
            "following capital letters looks EXACTLY THE SAME as the original?")
    sol = (f"The capitals that are unchanged by a vertical mirror are "
           f"A, H, I, M, O, T, U, V, W, X, Y. '{correct}' is one of them.")
    return stem, correct, d, sol, "M", "mirror_letter"

# ---- 2. WATER IMAGE of horizontally-symmetric string = unchanged ----------
def t_water_string():
    """Water image (horizontal line) of horizontally-symmetric glyphs = same string."""
    n = random.randint(4, 6)
    pool = WATER_SAFE + WATER_SAFE_DIG
    s = "".join(random.choice(pool) for _ in range(n))
    correct = s                         # each glyph unchanged by horizontal mirror
    d1 = s[::-1] if s[::-1] != s else _mutate(s, 1)
    d2 = _mutate(s, 2)
    d3 = _mutate(s, 5)
    stem = (f"Every character in the string below is drawn from glyphs that are "
            f"symmetric about a HORIZONTAL line (B, C, D, E, H, I, K, O, X, 0, 1, "
            f"3, 8), so each one is unchanged by a top-to-bottom flip and the "
            f"left-right order is preserved. What is the WATER IMAGE (reflection in "
            f"water, about a horizontal line) of '{s}'?")
    sol = (f"A water image flips top-to-bottom and keeps the left-right order. Each "
           f"glyph here is horizontally symmetric, so every character is unchanged "
           f"and the order is kept: the water image is '{correct}'.")
    return stem, correct, [d1, d2, d3], sol, "H", "water_string"

# ---- 3. DICE: find the face opposite a given face -------------------------
def _dice_problem():
    """
    Build a labelled cube with known opposite pairs, present TWO corner views,
    and pick a query face for which the opposite is UNIQUELY deducible from the
    two views alone (i.e. all three faces adjacent to q are revealed across the
    views, leaving exactly one candidate = its opposite).

    A face f is "shown adjacent to q" if f and q both appear in the same view
    (faces meeting at a corner are mutually adjacent / never opposite). The
    opposite of q is the unique face among 1..6 that is neither q nor ever
    shown adjacent to q -- but only if the views reveal that exactly one such
    face remains. We require the views to pin it down with no ambiguity, i.e.
    the three faces adjacent to q (its true opposite is opp[q]; its four
    neighbours are everything except q and opp[q]) -- we need at least three of
    those four neighbours revealed so the lone remaining number is forced.
    Returns (views, query_face, opposite_face) or None if not deducible.
    """
    nums = random.sample(range(1, 7), 6)
    opp = {}
    opp[nums[0]] = nums[1]; opp[nums[1]] = nums[0]
    opp[nums[2]] = nums[3]; opp[nums[3]] = nums[2]
    opp[nums[4]] = nums[5]; opp[nums[5]] = nums[4]

    def random_corner():
        while True:
            a, b, c = random.sample(range(1, 7), 3)
            if opp[a] != b and opp[a] != c and opp[b] != c:
                return (a, b, c)

    v1 = random_corner()
    v2 = random_corner()
    while set(v2) == set(v1):
        v2 = random_corner()

    # find a query face whose opposite is forced: the set of faces shown
    # adjacent to q must be EXACTLY the four neighbours (everything except q
    # and opp[q]); then the only number never seen with q and != q is opp[q].
    candidates = []
    for q in range(1, 7):
        shown_with_q = set()
        for view in (v1, v2):
            if q in view:
                shown_with_q |= (set(view) - {q})
        # the four true neighbours of q:
        neighbours = set(range(1, 7)) - {q, opp[q]}
        # opp[q] must NEVER be shown with q (guaranteed: opposite faces can't
        # share a corner), and we need shown_with_q to leave exactly one number
        # unaccounted: i.e. {1..6} - {q} - shown_with_q == {opp[q]}.
        remaining = set(range(1, 7)) - {q} - shown_with_q
        if remaining == {opp[q]} and opp[q] not in shown_with_q:
            candidates.append(q)
    if not candidates:
        return None
    q = random.choice(candidates)
    return [v1, v2], q, opp[q], opp

def t_dice_opposite():
    """Given two dice views, find the face opposite a queried face. [H]"""
    res = _dice_problem()
    if res is None:
        return None
    views, q, ans, opp = res
    correct = str(ans)
    # distractors: faces that appear adjacent to q (definitely NOT opposite)
    adj = [f for f in range(1, 7) if f != q and f != ans]
    random.shuffle(adj)
    d1, d2, d3 = adj[0], adj[1], adj[2]
    v1, v2 = views
    stem = (f"A cube (die) has its six faces numbered 1 to 6. Two positions of the "
            f"same die are shown. In the first position the faces with numbers "
            f"{v1[0]} (top), {v1[1]} (front) and {v1[2]} (right) meet at a corner. "
            f"In the second position the faces {v2[0]} (top), {v2[1]} (front) and "
            f"{v2[2]} (right) meet at a corner. Which number is on the face OPPOSITE "
            f"to the face numbered {q}?")
    sol = (f"Across the two views, the three faces sharing a corner with {q} (hence "
           f"ADJACENT to it) can be identified; the only remaining number is its "
           f"opposite. The face opposite {q} is {ans}.")
    return stem, correct, [str(d1), str(d2), str(d3)], sol, "H", "dice_opposite"

def t_dice_single_pair():
    """One view fixes 3 adjacent faces; with all 6 numbers, opposite of the
    top is the unseen number whose pair is consistent. Simpler computable
    variant: give a view plus an explicit statement of one opposite pair. [M]"""
    nums = random.sample(range(1, 7), 6)
    opp = {nums[0]:nums[1], nums[1]:nums[0], nums[2]:nums[3], nums[3]:nums[2],
           nums[4]:nums[5], nums[5]:nums[4]}
    # tell the solver two of the three opposite pairs, ask for the third.
    pairs = [(nums[0],nums[1]), (nums[2],nums[3]), (nums[4],nums[5])]
    random.shuffle(pairs)
    (p1a,p1b),(p2a,p2b),(p3a,p3b) = pairs
    q = p3a
    ans = p3b
    correct = str(ans)
    others = [f for f in range(1,7) if f not in (q, ans)]
    random.shuffle(others)
    d1, d2, d3 = others[:3]
    stem = (f"On a die numbered 1 to 6, the face {p1a} is opposite the face {p1b}, "
            f"and the face {p2a} is opposite the face {p2b}. Which number is on the "
            f"face OPPOSITE to the face numbered {q}?")
    sol = (f"Three opposite pairs use all six numbers. Given {p1a}-{p1b} and "
           f"{p2a}-{p2b} as two pairs, the remaining two numbers {min(p3a,p3b)} and "
           f"{max(p3a,p3b)} must be the third opposite pair, so {q} is opposite {ans}.")
    return stem, correct, [str(d1),str(d2),str(d3)], sol, "M", "dice_pair"

# ---- 4. COUNTING FIGURES (closed-form) ------------------------------------
def t_count_squares_grid():
    """Squares in an n x n grid of unit squares = sum k^2. [H]"""
    n = random.randint(2, 6)
    total = sum(k*k for k in range(1, n+1))
    correct = str(total)
    d1, d2, d3 = _num_distractors(total, [n*n, total + n, total - n, total*2, total + 1])
    stem = (f"A square is divided by equally spaced horizontal and vertical lines "
            f"into a {n} x {n} grid of {n*n} unit squares. Counting squares of ALL "
            f"sizes (1x1, 2x2, ... up to {n}x{n}), how many squares are there in "
            f"total in the figure?")
    formula = " + ".join(f"{k}^2" for k in range(1, n+1))
    sol = (f"Number of squares = {formula} = {total}.")
    return stem, correct, [d1, d2, d3], sol, "H", "count_squares"

def t_count_rectangles_grid():
    """Rectangles in an m x n grid = C(m+1,2)*C(n+1,2). [H]"""
    m = random.randint(2, 5)
    n = random.randint(2, 5)
    total = comb(m+1, 2) * comb(n+1, 2)
    correct = str(total)
    d1, d2, d3 = _num_distractors(total, [
        m*n,                                   # only unit cells
        comb(m+1,2)+comb(n+1,2),               # added instead of multiplied
        sum(k*k for k in range(1, min(m,n)+1)),# squares-only formula
        total - m, total + n])
    stem = (f"A rectangle is divided by equally spaced lines into an {m} x {n} grid "
            f"of {m*n} unit cells ({m} rows and {n} columns). How many rectangles "
            f"of all sizes (including the unit cells and the whole figure) can be "
            f"counted in the figure?")
    sol = (f"Choose 2 of the {m+1} horizontal lines and 2 of the {n+1} vertical "
           f"lines: C({m+1},2) x C({n+1},2) = {comb(m+1,2)} x {comb(n+1,2)} = {total}.")
    return stem, correct, [d1, d2, d3], sol, "H", "count_rectangles"

def t_count_triangles_subdiv():
    """Triangles in an equilateral triangle subdivided into n rows. [H]
       n even: n(n+2)(2n+1)/8 ; n odd: (n(n+2)(2n+1)-1)/8"""
    n = random.randint(2, 6)
    base = n*(n+2)*(2*n+1)
    total = base//8 if n % 2 == 0 else (base-1)//8
    correct = str(total)
    d1, d2, d3 = _num_distractors(total, [
        n*n, n*n + (n-1), total + n, total - n, total + 2])
    stem = (f"An equilateral triangle is divided by lines drawn parallel to its "
            f"three sides into {n} rows of small congruent triangles (so the "
            f"smallest row has {2*n-1} little triangles). Counting triangles of ALL "
            f"sizes and BOTH orientations (pointing up and pointing down), how many "
            f"triangles are there in total?")
    sol = (f"For an equilateral triangle split into n rows the total count is "
           f"n(n+2)(2n+1)/8 (n even) or (n(n+2)(2n+1)-1)/8 (n odd). With n={n}: "
           f"= {total}.")
    return stem, correct, [d1, d2, d3], sol, "H", "count_triangles"

def t_count_triangles_fan():
    """A triangle with k cevians from one vertex to the opposite side -> total
    small+combined triangles = C(k+2, 2) ... actually with k interior points on
    the base creating k+1 base segments, number of triangles = C(k+2,2)? Use the
    clean formula: a triangle whose base is divided into s parts by (s-1) points,
    all joined to the apex, contains s(s+1)/2 triangles. [M]"""
    s = random.randint(2, 8)
    total = s*(s+1)//2
    correct = str(total)
    d1, d2, d3 = _num_distractors(total, [s, s*s, total + s, total - 1, total + 1])
    stem = (f"In triangle ABC, the base BC is divided into {s} equal parts by "
            f"{s-1} points, and every one of these points is joined to the apex A "
            f"by a straight line. How many triangles in total are there in the "
            f"resulting figure?")
    sol = (f"With the base split into {s} segments, the number of triangles is "
           f"{s}({s}+1)/2 = {s}x{s+1}/2 = {total}.")
    return stem, correct, [d1, d2, d3], sol, "M", "count_fan"

# ---- 5. PAPER FOLDING / PUNCHING (counts) ---------------------------------
def t_paper_fold_punch():
    """Square folded f times, p punches through all layers -> p*2^f holes. [H]"""
    f = random.randint(1, 4)
    p = random.randint(1, 3)
    layers = 2**f
    total = p*layers
    correct = str(total)
    d1, d2, d3 = _num_distractors(total, [
        p, p*f*2, p + layers, layers, total + p])
    stem = (f"A square sheet of paper is folded in half {f} time(s) (each fold "
            f"doubles the number of layers, with the holes lining up over each "
            f"other). A single hole-punch then makes {p} hole(s) through ALL the "
            f"layers at once. When the paper is completely unfolded, how many holes "
            f"are there in the sheet?")
    sol = (f"{f} fold(s) create 2^{f} = {layers} layers. {p} punch(es) through all "
           f"layers give {p} x {layers} = {total} holes when unfolded.")
    return stem, correct, [d1, d2, d3], sol, "H", "paper_punch"

def t_paper_fold_simple():
    """One punch, f folds -> 2^f holes. [M]"""
    f = random.randint(2, 6)            # f>=2 keeps distractors clean & distinct
    total = 2**f
    correct = str(total)
    # distractors: one fold short, one fold extra, and the common "2*f" mistake;
    # then ensure 3 distinct values != total via _num_distractors helper.
    cands = [total // 2, total * 2, 2 * f, total + f, total - 2]
    d1, d2, d3 = _num_distractors(total, cands)
    stem = (f"A square sheet of paper is folded straight in half {f} time(s), the "
            f"layers lying exactly on top of one another. One hole is punched "
            f"through all the layers. How many holes will the sheet have after it "
            f"is fully unfolded?")
    sol = (f"Each fold doubles the layers, so {f} folds -> 2^{f} = {total} layers, "
           f"and one punch makes {total} holes.")
    return stem, correct, [d1, d2, d3], sol, "M", "paper_simple"

# ---- 6. SERIES / ANALOGY of letter-strings (transform) --------------------
def t_series_shift():
    """Each term shifts +k; find next term. [M/H]"""
    k = random.choice([1, 2, 3, 4, -1, -2, -3])
    start = "".join(random.choice(AZ) for _ in range(3))
    terms = [shift_word(start, k*i) for i in range(4)]
    correct = shift_word(start, k*4)
    d1 = shift_word(start, k*4 + 1)
    d2 = shift_word(start, k*3)         # repeats previous
    d3 = correct[::-1]
    sign = f"+{k}" if k >= 0 else str(k)
    series = ", ".join(terms)
    stem = (f"In the letter series below, each term is obtained from the previous "
            f"one by shifting every letter the SAME fixed number of places in the "
            f"alphabet (wrapping Z->A). Find the NEXT term.\n"
            f"Series: {series}, ?")
    diff = "M" if abs(k) <= 2 else "H"
    sol = (f"Each term shifts {sign} from the previous "
           f"({terms[0]} -> {terms[1]} -> ...). Next = {sign} from {terms[-1]} "
           f"= {correct}.")
    return stem, correct, [d1, d2, d3], sol, diff, "series_shift"

def t_analogy_reverse():
    """A : reverse(A) :: B : ? . [M]"""
    a = "".join(random.choice(AZ) for _ in range(random.randint(3,5)))
    b = "".join(random.choice(AZ) for _ in range(random.randint(3,5)))
    a_img = a[::-1]
    correct = b[::-1]
    d1 = b
    d2 = shift_word(b, 1)[::-1]
    d3 = b[::-1][1:] + b[::-1][:1] if len(b) > 1 else b + "X"
    stem = (f"Study the relationship and complete the analogy. The second string is "
            f"formed from the first by a simple positional transformation.\n"
            f"'{a}' : '{a_img}' :: '{b}' : ?")
    sol = (f"The rule is reversal of the character order: '{a}' -> '{a_img}'. "
           f"Reversing '{b}' gives '{correct}'.")
    return stem, correct, [d1, d2, d3], sol, "M", "analogy_reverse"

def t_series_rotate():
    """Sequence rotates one position left each term; find next. [H]"""
    base = "".join(random.sample(AZ, random.randint(4,5)))
    terms = [base[i:] + base[:i] for i in range(4)]
    correct = base[4:] + base[:4]
    d1 = base                            # back to start (off by rotation count)
    d2 = base[3:] + base[:3]             # repeats previous
    d3 = correct[::-1]
    series = ", ".join(terms)
    stem = (f"In the series below, each successive term is the previous term with "
            f"its FIRST character moved to the END (a left rotation by one). Find "
            f"the next term.\nSeries: {series}, ?")
    sol = (f"Left-rotate the latest term '{terms[-1]}' by one character: "
           f"move '{terms[-1][0]}' to the end -> '{correct}'.")
    return stem, correct, [d1, d2, d3], sol, "H", "series_rotate"

# ---- 7. EMBEDDED (letter form): count contiguous occurrences --------------
def t_embedded_count():
    """How many times does short pattern occur (contiguous, overlapping) in long
    string? Computable. [M/H]"""
    pat = "".join(random.choice("ABCAB") for _ in range(2))
    # build a longer string and count occurrences (allow overlap)
    body = "".join(random.choice("ABCAB") for _ in range(random.randint(8,12)))
    # ensure at least one occurrence
    if pat not in body:
        ins = random.randint(0, len(body))
        body = body[:ins] + pat + body[ins:]
    # count overlapping occurrences
    cnt = 0
    for i in range(len(body) - len(pat) + 1):
        if body[i:i+len(pat)] == pat:
            cnt += 1
    correct = str(cnt)
    # distractors must be distinct, >=0, and != cnt
    cand = [cnt + 1, cnt + 2, cnt - 1, cnt + 3]
    d = []
    for c in cand:
        if c >= 0 and c != cnt and c not in d:
            d.append(c)
    d1, d2, d3 = (str(x) for x in d[:3])
    stem = (f"Treating the figure as the linear string of symbols '{body}', how "
            f"many times does the smaller pattern '{pat}' appear inside it as a "
            f"CONTIGUOUS block (overlapping occurrences are counted separately)?")
    diff = "M" if len(body) <= 10 else "H"
    sol = (f"Scanning '{body}' for '{pat}' as a contiguous block (allowing overlap) "
           f"gives {cnt} occurrence(s).")
    return stem, correct, [d1, d2, d3], sol, diff, "embedded_count"

def t_embedded_contains():
    """Which option string is fully embedded (contiguous) in a given string? [VH]"""
    body = "".join(random.choice(AZ) for _ in range(random.randint(7,9)))
    i = random.randint(0, len(body)-3)
    L = random.randint(3, min(4, len(body)-i))
    correct = body[i:i+L]
    # distractors: substrings NOT contiguous in body
    def not_in(s):
        return s not in body
    d_candidates = []
    tries = 0
    while len(d_candidates) < 3 and tries < 200:
        tries += 1
        cand = "".join(random.choice(AZ) for _ in range(L))
        if not_in(cand) and cand != correct and cand not in d_candidates:
            d_candidates.append(cand)
    stem = (f"In the larger pattern represented by the string '{body}', exactly one "
            f"of the following appears as a CONTIGUOUS (unbroken) sub-pattern. Which "
            f"one is embedded in it?")
    sol = (f"'{correct}' appears as the contiguous block '{body[i:i+L]}' inside "
           f"'{body}'; the other choices do not occur unbroken.")
    return stem, correct, d_candidates, sol, "VH", "embedded_contains"

# =========================================================================
TEMPLATES = [
    t_mirror_string, t_mirror_choose_letter, t_water_string,
    t_dice_opposite, t_dice_single_pair,
    t_count_squares_grid, t_count_rectangles_grid, t_count_triangles_subdiv,
    t_count_triangles_fan, t_paper_fold_punch, t_paper_fold_simple,
    t_series_shift, t_analogy_reverse, t_series_rotate,
    t_embedded_count, t_embedded_contains,
]

DIFF_OF = {
    t_mirror_string: "M", t_mirror_choose_letter: "M", t_water_string: "H",
    t_dice_opposite: "H", t_dice_single_pair: "M",
    t_count_squares_grid: "H", t_count_rectangles_grid: "H",
    t_count_triangles_subdiv: "H", t_count_triangles_fan: "M",
    t_paper_fold_punch: "H", t_paper_fold_simple: "M",
    t_series_shift: "M", t_analogy_reverse: "M", t_series_rotate: "H",
    t_embedded_count: "H", t_embedded_contains: "VH",
}

# Target exactly ~20% M / 60% H / 20% VH via explicit per-difficulty quotas.
#   M templates (7): mirror_string, mirror_letter, dice_pair, count_fan,
#                    paper_simple, series_shift, analogy_reverse
#   H templates (8): water_string, dice_opposite, count_squares, count_rectangles,
#                    count_triangles, paper_punch, series_rotate, embedded_count
#   VH templates (1): embedded_contains
QUOTA = {"M": 100, "H": 300, "VH": 100}
BY_DIFF = {"M": [], "H": [], "VH": []}
for t in TEMPLATES:
    BY_DIFF[DIFF_OF[t]].append(t)

def fill(diff, target, type_cap=None):
    """Generate `target` unique questions of the given difficulty, drawing
    randomly from that difficulty's templates. `type_cap` optionally caps how
    many questions any single qtype may contribute (for variety)."""
    got = 0
    attempts = 0
    pool = BY_DIFF[diff]
    type_used = Counter()
    while got < target and attempts < 600000:
        attempts += 1
        t = random.choice(pool)
        try:
            res = t()
        except Exception:
            continue
        if res is None:
            continue
        stem, correct, distractors, sol, diff_t, qtype = res
        if diff_t != diff:           # only count questions of the target difficulty
            continue
        if type_cap is not None and type_used[qtype] >= type_cap.get(qtype, 10**9):
            continue
        before = len(questions)
        add(stem, correct, distractors, sol, diff_t, qtype)
        if len(questions) > before:
            got += 1
            type_used[qtype] += 1
    return got, attempts

# Per-qtype caps to keep H variety (water_string would otherwise dominate).
H_CAP = {"water_string": 70, "series_rotate": 70, "dice_opposite": 70,
         "embedded_count": 70}
M_CAP = {"dice_pair": 35, "series_shift": 35, "mirror_string": 35,
         "analogy_reverse": 35}
for d, cap in (("M", M_CAP), ("H", H_CAP), ("VH", None)):
    g, a = fill(d, QUOTA[d], cap)
    print(f"  filled {d}: {g}/{QUOTA[d]} in {a} attempts")

print(f"Generated {len(questions)} questions total.")

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
diffc = Counter(q["diff"] for q in questions)
tot = len(questions)
print("Difficulty:", dict(diffc),
      {k: f"{100*v/tot:.1f}%" for k, v in diffc.items()})
print("Types:", dict(Counter(q["qtype"] for q in questions)))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_10_NonVerbal_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_10_NonVerbal_500.key.json"

lines = []
lines.append("# Non-Verbal Reasoning — 500 Question Practice Set (SSC CGL, Reasoning / Tier-I & II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard — CGL standard.")
lines.append("> **Every answer is computed by an exact rule and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is -0.50; the distractors are real common-mistake values.\n")
lines.append("## IMPORTANT — how the (un-drawable) figures are represented in text")
lines.append("Figures cannot be drawn in markdown, so this set covers only the **text-representable, exactly computable** part of Non-Verbal Reasoning. The conventions below are fixed and used consistently throughout:")
lines.append("")
lines.append("- **Mirror Image (vertical mirror):** A mirror held along a *vertical* line reverses the **left-to-right order** of the characters. To make every glyph behave exactly, mirror-image questions use only letters/digits that are **left-right symmetric** — A, H, I, M, O, T, U, V, W, X, Y and 0, 1, 8 — so each glyph is unchanged and ONLY the order flips. Thus mirror(`WAX`) = `XAW`.")
lines.append("- **Water Image (horizontal mirror):** A reflection *in water* is about a *horizontal* line; it flips each glyph **top-to-bottom** while keeping the left-to-right order. Water-image questions use only **top-bottom symmetric** glyphs — B, C, D, E, H, I, K, O, X and 0, 1, 3, 8 — so each glyph is unchanged and the whole string stays the same.")
lines.append("- **Dice:** a standard cube with faces numbered 1–6. A 'view' names the three faces meeting at one corner (top, front, right). Two views, or two stated opposite pairs, are enough to deduce the remaining opposite pair exactly.")
lines.append("- **Counting figures:** each figure is described precisely in words and the total is given by a closed-form formula (squares in an n×n grid = 1²+2²+…+n²; rectangles in an m×n grid = C(m+1,2)·C(n+1,2); triangles in a subdivided triangle = n(n+2)(2n+1)/8 type formula; a base split into s parts and joined to the apex = s(s+1)/2 triangles).")
lines.append("- **Paper folding & punching:** folding a square in half f times makes 2^f layers; p punches through all layers give p·2^f holes when unfolded.")
lines.append("- **Series / Analogy:** letter-strings transformed by an exact rule (fixed alphabet shift, reversal, or left-rotation).")
lines.append("- **Embedded figures:** the 'figure' is a linear string of symbols; the task is to count or detect a contiguous sub-pattern.\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}-Q{start+50})\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        o = q["opts"]
        stem_md = q["stem"].replace("\n", "  \n")
        lines.append(f"**Q{n}.** {stem_md}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    lines.append(f"\n## Answers Q{start+1}-Q{start+50}\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        letter = LETTERS[q["ci"]]
        val = q["opts"][q["ci"]]
        sol = q["sol"].replace("\n", " ")
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* — {sol}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

sidecar = {str(j + 1): questions[j]["opts"][questions[j]["ci"]] for j in range(500)}
with open(SIDECAR, "w", encoding="utf-8") as f:
    json.dump(sidecar, f, indent=0)

print(f"Wrote {OUT}")
print(f"Wrote {SIDECAR}")
print(f"Total lines: {len(lines)}")
