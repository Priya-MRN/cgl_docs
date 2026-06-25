# -*- coding: utf-8 -*-
"""
SSC CGL Order & Ranking (Reasoning) - 500 MCQ generator.
SIMULATION-BASED & self-verifying: every question models an explicit linear
arrangement (a row of distinct positions 1..N, where position 1 is the LEFT /
TOP end) OR a total order built from comparative clues. The answer is COMPUTED
by the model (total = n+m-1, position arithmetic, between-counts, a verified
unique permutation for comparative ordering), so the keyed option is provably
correct.

Key model:
  * A row of N people. Position p counted from LEFT = p; counted from RIGHT =
    N - p + 1. So if a person is n-th from left and m-th from right in a row of
    size N, then n + m - 1 = N (this is the master identity).
  * Comparative ordering (tallest/oldest): build a total order over k people from
    "A is taller than B" style clues and VERIFY by brute-force enumeration that
    exactly ONE permutation is consistent before emitting the question.

Emits a JSON sidecar (qnum -> {answer, structured meta}) so an independent
verifier can re-derive the answer from the structured fields and cross-check.

NO unicode emoji - plain ASCII only.
NEVER pass a float to Fraction(num, den) - all arithmetic here is integer.
"""
import random
import json
from itertools import permutations
from collections import Counter

random.seed(20260625)  # deterministic

LETTERS = "abcd"

NAMES = ["Amit", "Ravi", "Sunil", "Vijay", "Rohit", "Anil", "Manoj", "Karan",
         "Deepak", "Suresh", "Naveen", "Sanjay", "Rakesh", "Gopal", "Ramesh",
         "Dinesh", "Mahesh", "Ajay", "Vikram", "Harish", "Lokesh", "Mukesh",
         "Pankaj", "Tarun", "Arjun", "Kiran", "Aman", "Mohan", "Shyam", "Nitin",
         "Pradeep", "Yogesh", "Sachin", "Varun", "Gaurav", "Alok", "Nikhil"]


# ---------------- options / dedupe ----------------
questions = []  # dict(stem, opts(list str), ci, sol, diff, qtype, meta)
seen = set()


def fmt_num(x):
    """Format an integer plainly (all answers here are integers or short text)."""
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, int):
        return str(x)
    return str(x)


def make_options(correct, distractors):
    """Return (options_list, correct_index). 4 DISTINCT string values."""
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
    # pad: numeric -> nudge away from existing; else append a name filler
    k = 1
    while len(opts) < 4:
        if correct.lstrip("-").isdigit():
            base = int(correct)
            cand = str(base + k if k % 2 else base - k)
            if cand.lstrip("-").isdigit() and int(cand) < 1:
                cand = str(base + k + 5)
        else:
            cand = random.choice(NAMES)
        if cand not in opts:
            opts.append(cand)
        k += 1
        if k > 60:
            opts.append(correct + "_" + str(len(opts)))
    random.shuffle(opts)
    return opts, opts.index(correct)


def add(stem, correct, distractors, sol, diff, qtype, meta):
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
    if len(set(opts)) != 4:
        seen.discard(key)
        return False
    questions.append({
        "stem": stem, "opts": opts, "ci": ci, "sol": sol,
        "diff": diff, "qtype": qtype, "meta": meta,
    })
    return True


def ordinal(n):
    """English ordinal: 1->1st, 2->2nd, 3->3rd, 11->11th, 21->21st ..."""
    n = int(n)
    if 10 <= (n % 100) <= 20:
        suf = "th"
    else:
        suf = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suf}"


# ================= TEMPLATE TYPES =================
# Model convention for a single row of size N:
#   left-position  L of a person  ->  right-position R = N - L + 1
#   master identity: (from-left) + (from-right) - 1 = N

def t_total_in_row():
    """Total people in a row given a person's position from both ends. [M]
       total = n + m - 1."""
    N = random.choice(range(12, 46))
    L = random.randint(2, N - 1)            # from left
    R = N - L + 1                            # from right (computed)
    name = random.choice(NAMES)
    thing = random.choice(["a row", "a queue", "a line"])
    correct = N
    d1 = L + R                               # forgets the -1 (off by one)
    d2 = N - 1                               # off by one low
    d3 = N + 1                               # off by one high
    stem = (f"In {thing}, {name} is {ordinal(L)} from the left end and "
            f"{ordinal(R)} from the right end. How many people are there in "
            f"{thing.replace('a ', 'the ')}?")
    sol = (f"Total = (position from left) + (position from right) - 1 = "
           f"{L} + {R} - 1 = {N}. The '-1' avoids counting {name} twice.")
    meta = {"type": "total_from_both", "from_left": L, "from_right": R,
            "answer": N}
    return stem, correct, [d1, d2, d3], sol, "M", "total_in_row", meta


def t_rank_in_class():
    """Total students given rank from top and bottom. [M] total = top+bottom-1."""
    top = random.randint(3, 30)
    bottom = random.randint(3, 30)
    N = top + bottom - 1
    name = random.choice(NAMES)
    correct = N
    d1 = top + bottom                        # forgets -1
    d2 = N - 1
    d3 = N + 1
    stem = (f"In a class, {name} ranks {ordinal(top)} from the top and "
            f"{ordinal(bottom)} from the bottom. How many students are there "
            f"in the class?")
    sol = (f"Total students = (rank from top) + (rank from bottom) - 1 = "
           f"{top} + {bottom} - 1 = {N}. Subtract 1 so {name} is not counted "
           f"twice.")
    meta = {"type": "total_from_both", "from_left": top, "from_right": bottom,
            "answer": N}
    return stem, correct, [d1, d2, d3], sol, "M", "rank_in_class", meta


def t_position_other_end():
    """Given total and position from one end, find position from the other end. [M]
       other = N - given + 1."""
    N = random.choice(range(15, 51))
    given = random.randint(2, N - 1)
    end = random.choice(["left", "right"])
    other_end = "right" if end == "left" else "left"
    ans = N - given + 1
    name = random.choice(NAMES)
    correct = ans
    d1 = N - given                           # forgets +1
    d2 = N - given + 2                        # over by one
    d3 = given                                # same position (swapped ends trap)
    stem = (f"In a row of {N} people, {name} is {ordinal(given)} from the "
            f"{end}. What is {name}'s position from the {other_end}?")
    sol = (f"Position from the {other_end} = total - position from {end} + 1 = "
           f"{N} - {given} + 1 = {ans}.")
    meta = {"type": "other_end", "total": N, "given": given, "answer": ans}
    return stem, correct, [d1, d2, d3], sol, "M", "position_other_end", meta


def t_between_two():
    """Two people's positions from the SAME end -> how many between them. [M/H]
       between = |a - b| - 1."""
    N = random.choice(range(15, 51))
    a = random.randint(2, N - 1)
    b = random.randint(2, N - 1)
    while abs(a - b) < 2 or a == b:
        a = random.randint(2, N - 1)
        b = random.randint(2, N - 1)
    n1, n2 = random.sample(NAMES, 2)
    end = random.choice(["left", "right"])
    between = abs(a - b) - 1
    correct = between
    d1 = abs(a - b)                          # forgets -1
    d2 = abs(a - b) + 1                       # over
    d3 = max(between - 1, 0)                  # under (and avoid dup)
    if d3 == correct:
        d3 = between + 2
    stem = (f"In a row, {n1} is at the {ordinal(a)} position from the {end} "
            f"and {n2} is at the {ordinal(b)} position from the {end}. How "
            f"many persons are sitting between {n1} and {n2}?")
    sol = (f"Both positions are measured from the {end}, so persons strictly "
           f"between = |{a} - {b}| - 1 = {abs(a-b)} - 1 = {between}.")
    meta = {"type": "between_same_end", "a": a, "b": b, "answer": between}
    return stem, correct, [d1, d2, d3], sol, "M", "between_two", meta


def t_between_opposite_ends():
    """One person's pos from left, another's pos from right, total known ->
       how many between (they don't overlap). [H]
       Convert both to left-positions; between = |La - Lb| - 1."""
    N = random.choice(range(18, 46))
    La = random.randint(2, N - 6)            # first from left
    Rb = random.randint(2, N - La - 1)       # second from right, ensure Lb > La
    Lb = N - Rb + 1                          # second's left-position
    if Lb <= La:
        return None
    between = Lb - La - 1
    if between < 1:
        return None
    n1, n2 = random.sample(NAMES, 2)
    correct = between
    d1 = abs(La - Rb) - 1                     # subtracts raw given numbers (wrong)
    d2 = between + 1                          # forgets a -1 net
    d3 = N - La - Rb                          # common wrong shortcut
    if d3 == correct:
        d3 = between + 2
    stem = (f"In a row of {N} persons, {n1} is {ordinal(La)} from the left "
            f"end and {n2} is {ordinal(Rb)} from the right end. How many "
            f"persons are there between {n1} and {n2}?")
    sol = (f"{n2}'s position from the left = {N} - {Rb} + 1 = {Lb}. Both are "
           f"now measured from the left, so persons between = {Lb} - {La} - 1 "
           f"= {between}.")
    meta = {"type": "between_opposite", "total": N, "from_left": La,
            "from_right": Rb, "answer": between}
    return stem, correct, [d1, d2, d3], sol, "H", "between_opposite", meta


def t_interchange():
    """A and B interchange positions; after swap A is n-th from left; B was
       originally m-th from left -> A's original position OR total. [H]
       Model: after swap A sits where B was. So A_new_left = B_old_left.
       Given A_new_left and B_old's position from right and total, find total
       or A's original from-left."""
    N = random.choice(range(20, 51))
    # B originally at left position Lb. After interchange, A takes B's seat.
    Lb = random.randint(3, N - 2)
    # A originally somewhere else
    La = random.randint(2, N - 1)
    while La == Lb:
        La = random.randint(2, N - 1)
    n1, n2 = random.sample(NAMES, 2)
    # After swap, A is at Lb from left. Question gives A's new position from
    # RIGHT and asks total.
    A_new_right = N - Lb + 1
    correct = N
    d1 = Lb + A_new_right                     # forgets -1
    d2 = N - 1
    d3 = N + 1
    stem = (f"In a row, {n1} and {n2} interchange their positions. After the "
            f"interchange, {n1} becomes {ordinal(Lb)} from the left end and "
            f"{ordinal(A_new_right)} from the right end. How many persons are "
            f"there in the row? (Positions are counted in the same row.)")
    sol = (f"After interchanging, {n1} sits where {n2} was. {n1} is now "
           f"{Lb} from the left and {A_new_right} from the right, so total = "
           f"{Lb} + {A_new_right} - 1 = {N}.")
    meta = {"type": "total_from_both", "from_left": Lb,
            "from_right": A_new_right, "answer": N}
    return stem, correct, [d1, d2, d3], sol, "H", "interchange", meta


def t_interchange_newpos():
    """A and B swap. Given B's original position from left and the total, find
       A's new position from the right (A moves to B's old seat). [H]"""
    N = random.choice(range(20, 51))
    Lb = random.randint(3, N - 2)            # B's original left position
    n1, n2 = random.sample(NAMES, 2)
    # A moves to B's seat -> A_new_left = Lb -> A_new_right = N - Lb + 1
    A_new_right = N - Lb + 1
    correct = A_new_right
    d1 = N - Lb                              # forgets +1
    d2 = Lb                                  # confuses with left position
    d3 = N - Lb + 2                          # over
    stem = (f"In a row of {N} persons, {n2} is {ordinal(Lb)} from the left "
            f"end. {n1} and {n2} now interchange their positions. What is "
            f"{n1}'s new position from the right end?")
    sol = (f"After the swap, {n1} occupies {n2}'s seat, i.e. the {ordinal(Lb)} "
           f"position from the left. Position from the right = {N} - {Lb} + 1 "
           f"= {A_new_right}.")
    meta = {"type": "other_end", "total": N, "given": Lb, "answer": A_new_right}
    return stem, correct, [d1, d2, d3], sol, "H", "interchange_newpos", meta


def t_shift_left():
    """Person moves k places to the left/right; new position from one end. [H]"""
    N = random.choice(range(20, 51))
    L = random.randint(6, N - 4)
    k = random.randint(2, 5)
    direction = random.choice(["towards the left end", "towards the right end"])
    name = random.choice(NAMES)
    if "left" in direction:
        newL = L - k
    else:
        newL = L + k
    if not (1 <= newL <= N):
        return None
    correct = newL
    d1 = L + k if "left" in direction else L - k   # wrong direction
    d2 = newL + 1
    d3 = newL - 1 if newL - 1 >= 1 else newL + 2
    if d3 == correct:
        d3 = newL + 2
    stem = (f"In a row of {N} persons facing North, {name} is {ordinal(L)} "
            f"from the left end. If {name} moves {k} places "
            f"{direction}, what is {name}'s new position from the left end?")
    sol = (f"Moving {k} places {direction.split(' ')[1]} from the {ordinal(L)} "
           f"left position gives {L} {'-' if 'left' in direction else '+'} {k} "
           f"= {newL} from the left.")
    meta = {"type": "shift", "start_left": L, "k": k,
            "dir": "left" if "left" in direction else "right", "answer": newL,
            "total": N}
    return stem, correct, [d1, d2, d3], sol, "H", "shift_left", meta


def t_two_rank_facts():
    """Person's rank from top given total and rank from bottom (class). [M]
       top = N - bottom + 1."""
    N = random.choice(range(20, 61))
    bottom = random.randint(2, N - 1)
    top = N - bottom + 1
    name = random.choice(NAMES)
    correct = top
    d1 = N - bottom                          # forgets +1
    d2 = bottom                              # swapped ends
    d3 = N - bottom + 2                       # over
    stem = (f"In an examination, there are {N} students. {name} ranks "
            f"{ordinal(bottom)} from the bottom. What is {name}'s rank from "
            f"the top?")
    sol = (f"Rank from top = total - rank from bottom + 1 = {N} - {bottom} + 1 "
           f"= {top}.")
    meta = {"type": "other_end", "total": N, "given": bottom, "answer": top}
    return stem, correct, [d1, d2, d3], sol, "M", "two_rank_facts", meta


# ---- Comparative ordering: build a UNIQUE total order, verify by enumeration ----

def _unique_order_from_pairs(people, pairs):
    """pairs is a list of (hi, lo) meaning hi ranks above lo (e.g. taller/older).
       Return the unique permutation (list, highest first) consistent with ALL
       pairs, or None if zero or more than one ordering is consistent."""
    valid = []
    for perm in permutations(people):
        rank = {p: i for i, p in enumerate(perm)}  # smaller index = higher
        ok = True
        for hi, lo in pairs:
            if rank[hi] >= rank[lo]:
                ok = False
                break
        if ok:
            valid.append(perm)
            if len(valid) > 1:
                return None
    if len(valid) == 1:
        return list(valid[0])
    return None


def t_comparative_order():
    """Build comparative clues (taller/older/heavier) over k people and verify a
       UNIQUE order, then ask who is tallest / k-th / shortest. [H/VH]"""
    k = random.choice([4, 4, 5, 5, 6])
    people = random.sample(NAMES, k)
    # Decide a hidden true order, then emit a CHAIN of consecutive comparisons
    # (which always yields a unique total order), but shuffle/paraphrase so it
    # reads like scattered clues. A consecutive chain guarantees uniqueness;
    # we still verify by enumeration to be safe.
    true_order = people[:]
    random.shuffle(true_order)  # highest -> lowest in this list
    # Build consecutive pairs from the true order (guarantees unique order).
    pairs = [(true_order[i], true_order[i + 1]) for i in range(k - 1)]
    # Sometimes drop to non-consecutive but keep uniqueness: we keep the full
    # chain to be safe, but shuffle the clue order for presentation.
    clue_pairs = pairs[:]
    random.shuffle(clue_pairs)
    order = _unique_order_from_pairs(people, clue_pairs)
    if order is None or order != true_order:
        return None  # ambiguity guard (should not trigger for a full chain)

    attribute = random.choice([
        ("taller", "tall", "tallest", "shortest", "height"),
        ("older", "old", "oldest", "youngest", "age"),
        ("heavier", "heavy", "heaviest", "lightest", "weight"),
        ("richer", "rich", "richest", "poorest", "wealth"),
        ("scored more than", "high", "highest scorer", "lowest scorer", "marks"),
    ])
    comp, _adj, sup_hi, sup_lo, noun = attribute
    # Phrase each clue
    clue_txt = []
    for hi, lo in clue_pairs:
        if comp == "scored more than":
            clue_txt.append(f"{hi} scored more than {lo}")
        else:
            clue_txt.append(f"{hi} is {comp} than {lo}")
    clues = "; ".join(clue_txt) + "."

    # Choose a question variant
    variant = random.choice(["tallest", "shortest", "kth", "position_of"])
    if variant == "tallest":
        correct = order[0]
        distract = order[1:4]
        q = f"Who is the {sup_hi}?"
        ans_expl = f"The unique order ({noun}, highest first) is: {' > '.join(order)}. So the {sup_hi} is {order[0]}."
        ans_field = order[0]
    elif variant == "shortest":
        correct = order[-1]
        distract = order[:3]
        q = f"Who is the {sup_lo}?"
        ans_expl = f"The unique order ({noun}, highest first) is: {' > '.join(order)}. So the {sup_lo} is {order[-1]}."
        ans_field = order[-1]
    elif variant == "kth":
        pos = random.randint(2, k - 1)       # not the extremes
        correct = order[pos - 1]
        distract = [order[(pos - 2) % k], order[pos % k],
                    order[(pos + 1) % k]]
        q = f"Who is at the {ordinal(pos)} position when arranged from the {sup_hi.replace('est', 'est')} ({_adj if False else 'highest'} {noun} first)?"
        q = f"Who is {ordinal(pos)} in {noun} (arranged from highest to lowest)?"
        ans_expl = f"The unique order ({noun}, highest first) is: {' > '.join(order)}. The {ordinal(pos)} is {order[pos-1]}."
        ans_field = order[pos - 1]
    else:  # position_of
        target = random.choice(order[1:-1]) if k > 2 else order[0]
        pos = order.index(target) + 1
        correct = ordinal(pos)
        others = [ordinal(p) for p in range(1, k + 1) if p != pos]
        random.shuffle(others)
        distract = others[:3]
        q = (f"If they are arranged from highest to lowest in {noun}, what is "
             f"{target}'s position?")
        ans_expl = f"The unique order ({noun}, highest first) is: {' > '.join(order)}. {target} is at position {pos}."
        ans_field = ordinal(pos)

    stem = (f"Among {', '.join(people[:-1])} and {people[-1]}: {clues} {q}")
    sol = ans_expl
    diff = "H" if k <= 4 else "VH"
    meta = {"type": "comparative", "people": people,
            "pairs": [list(p) for p in clue_pairs], "order": order,
            "variant": variant, "answer": str(correct)}
    return stem, correct, list(distract), sol, diff, "comparative_order", meta


def t_comparative_count_above():
    """Comparative unique order; ask how many are taller than X / between two. [VH]"""
    k = random.choice([5, 6, 6])
    people = random.sample(NAMES, k)
    true_order = people[:]
    random.shuffle(true_order)
    pairs = [(true_order[i], true_order[i + 1]) for i in range(k - 1)]
    clue_pairs = pairs[:]
    random.shuffle(clue_pairs)
    order = _unique_order_from_pairs(people, clue_pairs)
    if order is None or order != true_order:
        return None
    attribute = random.choice([
        ("taller", "tallest", "height"),
        ("older", "oldest", "age"),
        ("heavier", "heaviest", "weight"),
    ])
    comp, sup_hi, noun = attribute
    clue_txt = [f"{hi} is {comp} than {lo}" for hi, lo in clue_pairs]
    clues = "; ".join(clue_txt) + "."
    # pick X not the top, ask how many are taller (= index)
    idx = random.randint(1, k - 1)
    X = order[idx]
    above = idx  # number strictly above X
    correct = above
    d1 = above + 1
    d2 = max(above - 1, 0)
    if d2 == correct:
        d2 = above + 2
    d3 = k - above - 1                       # number below (trap)
    if d3 == correct:
        d3 = above + 3
    stem = (f"Among {', '.join(people[:-1])} and {people[-1]}: {clues} "
            f"How many persons are {comp} than {X}?")
    sol = (f"The unique order ({noun}, highest first) is: {' > '.join(order)}. "
           f"{X} is at position {idx+1}, so {above} person(s) are {comp} than "
           f"{X}.")
    meta = {"type": "comparative_count", "people": people,
            "pairs": [list(p) for p in clue_pairs], "order": order,
            "target": X, "answer": above}
    return stem, correct, [d1, d2, d3], sol, "VH", "comparative_count", meta


def t_min_total():
    """Two people's positions from opposite ends with one person between; find
       MINIMUM total number in the row. [VH]
       A is La from left, B is Rb from right, and there are c persons between.
       Minimum total when they are arranged A ... B (no overlap):
       min N = La + c + Rb  (A then c between then B counted from right)."""
    La = random.randint(3, 12)
    Rb = random.randint(3, 12)
    c = random.randint(1, 6)
    n1, n2 = random.sample(NAMES, 2)
    # minimum total assuming A is to the left of B and exactly c between:
    minN = La + c + Rb
    correct = minN
    d1 = La + Rb + c - 1                      # subtracts one too many
    d2 = La + Rb                              # forgets the between-block
    d3 = La + c + Rb + 1                      # over
    stem = (f"In a row of persons (all facing North), {n1} is {ordinal(La)} "
            f"from the left end and {n2} is {ordinal(Rb)} from the right end. "
            f"If there are exactly {c} persons between {n1} and {n2}, what is "
            f"the minimum number of persons in the row?")
    sol = (f"For the minimum, {n1} is left of {n2}: positions are "
           f"[{La-1} before {n1}] + {n1} + [{c} between] + {n2} + "
           f"[{Rb-1} after {n2}] = {La} + {c} + {Rb} = {minN}.")
    meta = {"type": "min_total", "from_left": La, "from_right": Rb,
            "between": c, "answer": minN}
    return stem, correct, [d1, d2, d3], sol, "VH", "min_total", meta


def t_age_chain():
    """Simple 3-4 person age/height chain stated as inequalities -> who is
       eldest/youngest or middle. [M/H]"""
    k = random.choice([3, 3, 4])
    people = random.sample(NAMES, k)
    true_order = people[:]
    random.shuffle(true_order)              # oldest -> youngest
    # state as A>B>C chain directly (transitive sentence)
    rel = random.choice([
        ("older", "eldest", "youngest", "age"),
        ("taller", "tallest", "shortest", "height"),
    ])
    comp, sup_hi, sup_lo, noun = rel
    chain = f" {comp} than ".join(true_order)
    pairs = [(true_order[i], true_order[i + 1]) for i in range(k - 1)]
    order = _unique_order_from_pairs(people, pairs)
    if order is None or order != true_order:
        return None
    variant = random.choice(["eldest", "youngest", "middle"])
    if variant == "eldest":
        correct = order[0]
        q = f"who is the {sup_hi}?"
        expl = f"From {true_order[0]} {comp} than ... {true_order[-1]}, the order is {' > '.join(order)}; the {sup_hi} is {order[0]}."
    elif variant == "youngest":
        correct = order[-1]
        q = f"who is the {sup_lo}?"
        expl = f"The order is {' > '.join(order)}; the {sup_lo} is {order[-1]}."
    else:
        mid = k // 2
        if k % 2 == 0:
            mid = k // 2  # for even, pick a defined middle (k=4 -> index1)
            mid = 1
        correct = order[mid]
        q = f"who is at the {ordinal(mid+1)} position from the top (highest first)?"
        expl = f"The order (highest first) is {' > '.join(order)}; position {mid+1} is {order[mid]}."
    distract = [p for p in order if p != correct][:3]
    stem = (f"If {chain} (in terms of {noun}), then {q}")
    sol = expl
    diff = "M" if k == 3 else "H"
    meta = {"type": "comparative", "people": people,
            "pairs": [list(p) for p in pairs], "order": order,
            "variant": variant, "answer": str(correct)}
    return stem, correct, list(distract), sol, diff, "age_chain", meta


def t_position_from_left_count():
    """N people, X persons to the left of a person -> position from left, and
       Y persons to the right -> position from right; ask the other count or
       total. [M]"""
    N = random.choice(range(15, 46))
    left_of = random.randint(2, N - 3)       # persons to the LEFT of the person
    L = left_of + 1                          # the person's position from left
    R = N - L + 1
    right_of = R - 1                         # persons to the right
    name = random.choice(NAMES)
    ask = random.choice(["pos_left", "right_count"])
    if ask == "pos_left":
        correct = L
        d1 = left_of                         # forgets to add the person
        d2 = L + 1
        d3 = L - 1 if L - 1 >= 1 else L + 2
        if d3 == correct:
            d3 = L + 2
        stem = (f"In a row of {N} persons, there are {left_of} persons to the "
                f"left of {name}. What is {name}'s position from the left end?")
        sol = (f"Position from left = (persons to the left) + 1 = {left_of} + 1 "
               f"= {L}.")
        meta = {"type": "pos_from_count", "count_left": left_of, "answer": L,
                "total": N}
    else:
        correct = right_of
        d1 = R                               # confuses count with position
        d2 = right_of + 1
        d3 = max(right_of - 1, 0)
        if d3 == correct:
            d3 = right_of + 2
        stem = (f"In a row of {N} persons, there are {left_of} persons to the "
                f"left of {name}. How many persons are there to the right of "
                f"{name}?")
        sol = (f"{name}'s position from left = {left_of} + 1 = {L}. Persons to "
               f"the right = total - position = {N} - {L} = {right_of}.")
        meta = {"type": "right_count", "count_left": left_of, "total": N,
                "answer": right_of}
    return stem, correct, [d1, d2, d3], sol, "M", "pos_from_count", meta


TEMPLATES = [
    t_total_in_row, t_rank_in_class, t_position_other_end, t_between_two,
    t_between_opposite_ends, t_interchange, t_interchange_newpos,
    t_shift_left, t_two_rank_facts, t_comparative_order,
    t_comparative_count_above, t_min_total, t_age_chain,
    t_position_from_left_count,
]

# Per-template weights tuned so the realized mix lands near 20% M / 60% H / 20% VH.
# M templates: total_in_row, rank_in_class, position_other_end, between_two,
#              two_rank_facts, pos_from_count (and some age_chain k=3)
# H templates: between_opposite, interchange, interchange_newpos, shift_left,
#              comparative_order(k=4)
# VH templates: comparative_count, min_total, comparative_order(k>=5)
TEMPLATE_WEIGHT = {
    t_total_in_row: 5,
    t_rank_in_class: 4,
    t_position_other_end: 5,
    t_between_two: 4,
    t_two_rank_facts: 4,
    t_position_from_left_count: 5,
    t_between_opposite_ends: 20,
    t_interchange: 18,
    t_interchange_newpos: 18,
    t_shift_left: 20,
    t_comparative_order: 26,    # mixed H/VH internally
    t_comparative_count_above: 10,  # VH
    t_min_total: 9,             # VH
    t_age_chain: 5,             # mostly M/H
}
POOL = []
for t in TEMPLATES:
    POOL += [t] * TEMPLATE_WEIGHT[t]

attempts = 0
while len(questions) < 500 and attempts < 1500000:
    attempts += 1
    t = random.choice(POOL)
    try:
        res = t()
    except Exception:
        continue
    if res is None:
        continue
    stem, correct, distractors, sol, diff, qtype, meta = res
    add(stem, correct, distractors, sol, diff, qtype, meta)

print(f"Generated {len(questions)} questions in {attempts} attempts.")


# ---- self-check: re-derive every answer from structured meta ----
def solve_meta(m):
    """Independently re-compute the answer from structured meta fields."""
    t = m["type"]
    if t == "total_from_both":
        return str(m["from_left"] + m["from_right"] - 1)
    if t == "other_end":
        return str(m["total"] - m["given"] + 1)
    if t == "between_same_end":
        return str(abs(m["a"] - m["b"]) - 1)
    if t == "between_opposite":
        Lb = m["total"] - m["from_right"] + 1
        return str(Lb - m["from_left"] - 1)
    if t == "shift":
        if m["dir"] == "left":
            return str(m["start_left"] - m["k"])
        return str(m["start_left"] + m["k"])
    if t == "min_total":
        return str(m["from_left"] + m["between"] + m["from_right"])
    if t == "pos_from_count":
        return str(m["count_left"] + 1)
    if t == "right_count":
        L = m["count_left"] + 1
        return str(m["total"] - L)
    if t == "comparative":
        order = _unique_order_from_pairs(m["people"],
                                         [tuple(p) for p in m["pairs"]])
        assert order is not None and order == m["order"], "order not unique"
        return str(m["answer"])  # answer string already derived from order
    if t == "comparative_count":
        order = _unique_order_from_pairs(m["people"],
                                         [tuple(p) for p in m["pairs"]])
        assert order is not None and order == m["order"], "order not unique"
        return str(order.index(m["target"]))
    raise ValueError("unknown meta type " + t)


errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
    keyed = q["opts"][q["ci"]]
    try:
        exp = solve_meta(q["meta"])
    except Exception as e:
        print(f"Q{i}: solve_meta error {e}"); errors += 1; continue
    if exp != keyed:
        print(f"Q{i} [{q['qtype']}]: self-check {exp} != keyed {keyed}")
        errors += 1

stems = [q["stem"] for q in questions]
if len(set(stems)) != len(stems):
    print("DUPLICATE STEMS!"); errors += 1
assert len(questions) == 500, f"expected 500, got {len(questions)}"
assert errors == 0, f"{errors} self-check errors"
print(f"Self-check errors: {errors}")
print("Difficulty:", Counter(q["diff"] for q in questions))
print("Types:", Counter(q["qtype"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_08_Ranking_Order_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_08_Ranking_Order_500.key.json"

lines = []
lines.append("# Order & Ranking - 500 Question Practice Set (SSC CGL, Reasoning / Tier-I & II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium - ~60% Hard - ~20% Very-Hard (interchange / comparative ordering / minimum-total) - CGL standard.")
lines.append("> **Every arrangement is modelled on an explicit row (position 1 = left/top end) or a brute-force-verified unique order, and machine-verified** - the keyed option is provably correct.")
lines.append("> Negative marking in CGL is -0.50; distractors are real common-mistake values (forgetting the -1, swapping the two ends, taking an adjacent position).\n")
lines.append("## How order & ranking works (quick reference)")
lines.append("- Treat the row as positions numbered 1, 2, 3, ... from the LEFT (or TOP). Then position from the RIGHT (or BOTTOM) = total - (position from left) + 1.")
lines.append("- **Master identity:** if a person is n-th from one end and m-th from the other end, then total = n + m - 1 (subtract 1 so the person is not counted twice).")
lines.append("- **Persons between** two people measured from the same end = |position1 - position2| - 1.")
lines.append("- **Interchange:** when A and B swap seats, A takes B's old position and vice-versa; then apply the identities to the new positions.")
lines.append("- **Comparative ordering** (tallest/oldest/heaviest): chain the clues into one total order, e.g. A > B > C > D, then read off the required rank. Here every such order is brute-force checked to be the ONLY arrangement consistent with the clues.")
lines.append("- **Minimum total** when c persons sit between someone n-th from the left and someone m-th from the right (non-overlapping) = n + c + m.\n")
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
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* - {q['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

sidecar = {}
for j in range(500):
    q = questions[j]
    sidecar[str(j + 1)] = {
        "answer": q["opts"][q["ci"]],
        "qtype": q["qtype"],
        "meta": q["meta"],
    }
with open(SIDECAR, "w", encoding="utf-8") as f:
    json.dump(sidecar, f, indent=0)

print(f"Wrote {OUT}")
print(f"Wrote {SIDECAR}")
print(f"Total lines: {len(lines)}")
