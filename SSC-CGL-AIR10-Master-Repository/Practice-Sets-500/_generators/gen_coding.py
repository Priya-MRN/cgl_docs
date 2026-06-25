# -*- coding: utf-8 -*-
"""
SSC CGL Coding-Decoding (Reasoning) - 500 MCQ generator.
RULE-BASED & self-verifying: every code is produced by an exact Python
function, so the keyed option is provably correct. Distractors are
near-misses (off-by-one shift, reversed, wrong operation).
Options are STRINGS (coded words / numbers), distinctness by string equality.
Emits a JSON sidecar (qnum -> correct string) for the independent verifier.
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
    return ord(ch) - ord('A') + 1

def from_pos(p):
    """1-indexed position -> letter, wraps mod 26."""
    return AZ[(p - 1) % 26]

def shift_word(word, n):
    """Shift each letter by +n (mod 26)."""
    return "".join(from_pos(pos(c) + n) for c in word)

def opposite_word(word):
    """A<->Z, B<->Y, ... (27 - position)."""
    return "".join(from_pos(27 - pos(c)) for c in word)

# random word bank (uppercase, alphabetic)
WORDBANK = [
    "CAT","DOG","SUN","MOON","STAR","FISH","BIRD","TREE","LEAF","ROCK",
    "RAIN","WIND","FIRE","GOLD","IRON","BOOK","PAGE","DESK","LAMP","DOOR",
    "RING","BELL","KING","LION","TIGER","HORSE","SNAKE","EAGLE","ZEBRA","CAMEL",
    "MANGO","APPLE","GRAPE","LEMON","BERRY","WATER","EARTH","CLOUD","STORM","LIGHT",
    "NIGHT","MORNING","FRIEND","FAMILY","SCHOOL","TEACHER","STUDENT","PENCIL","FLOWER","GARDEN",
    "RIVER","OCEAN","BEACH","FOREST","DESERT","BRIDGE","CASTLE","KNIGHT","SHIELD","SWORD",
    "MOTHER","FATHER","SISTER","BROTHER","DOCTOR","FARMER","SINGER","DANCER","PAINTER","WRITER",
    "MONKEY","RABBIT","DONKEY","TURTLE","PARROT","PEACOCK","SPARROW","PIGEON","BUTTER","CHEESE",
    "TABLE","CHAIR","CLOCK","PHONE","RADIO","PAPER","GLASS","PLATE","SPOON","KNIFE",
    "TRAIN","PLANE","TRUCK","CYCLE","ROCKET","ENGINE","WHEEL","MOTOR","CABLE","METAL",
    "GREEN","BLACK","WHITE","BROWN","CREAM","SHADE","SHINE","BLAZE","FROST","SLEET",
    "MUSIC","DANCE","DRAMA","STAGE","SCENE","STORY","NOVEL","POEM","VERSE","RHYME",
    "BRAIN","HEART","NERVE","BONE","BLOOD","SKULL","SPINE","ANKLE","WRIST","THUMB",
]

DAYS = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
MONTHS = ["JANUARY","FEBRUARY","MARCH","APRIL","JUNE","JULY","AUGUST","OCTOBER","DECEMBER"]

questions = []  # dict(stem, opts(list str), ci, sol, diff, qtype)
seen = set()

def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 DISTINCT string values.
    correct + up to 3 plausible distractors; pad with mutated fillers if needed.
    """
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
    # pad with deterministic mutated fillers (perturb the correct string)
    tries = 0
    while len(opts) < 4 and tries < 200:
        tries += 1
        cand = _mutate(correct, tries)
        if cand not in opts:
            opts.append(cand)
    # absolute fallback (should never trigger): append index-suffixed copies
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
    """Make a plausible wrong string by nudging one alphabetic char or a digit."""
    chars = list(s)
    # find indices that are letters or digits
    idxs = [i for i, c in enumerate(chars) if c.isalpha() or c.isdigit()]
    if not idxs:
        return s + "X"
    i = idxs[seedn % len(idxs)]
    c = chars[i]
    if c.isalpha():
        up = c.isupper()
        base = AZ[(pos(c.upper()) - 1 + (1 if seedn % 2 else -1)) % 26]
        chars[i] = base if up else base.lower()
    else:  # digit
        chars[i] = str((int(c) + (1 if seedn % 2 else -1)) % 10)
    return "".join(chars)

def add(stem, correct, distractors, sol, diff, qtype):
    key = stem.strip()
    if key in seen:
        return False
    correct = str(correct)
    # clean distractors: strings, not equal to correct, distinct among themselves
    clean = []
    for d in distractors:
        if d is None:
            continue
        d = str(d)
        if d != correct and d not in clean:
            clean.append(d)
    # we can pad, but require at least 1 genuine distractor for quality
    if len(clean) < 1:
        return False
    seen.add(key)
    opts, ci = make_options(correct, clean)
    # internal consistency: keyed option must equal the computed correct string
    assert opts[ci] == correct, "keyed option != correct"
    questions.append({
        "stem": stem, "opts": opts, "ci": ci,
        "sol": sol, "diff": diff, "qtype": qtype,
    })
    return True

# ================= TEMPLATE TYPES =================

def t_letter_shift():
    """Each letter +n (or -n). Show example mapping, ask code for a new word. [M/H]"""
    n = random.choice([1, 2, 3, 4, 5, -1, -2, -3, -4])
    ex, ask = random.sample(WORDBANK, 2)
    ex_code = shift_word(ex, n)
    correct = shift_word(ask, n)
    sign = f"+{n}" if n >= 0 else str(n)
    # distractors: off-by-one shift, opposite-sign shift, reversed correct
    d1 = shift_word(ask, n + 1)
    d2 = shift_word(ask, -n) if n != 0 else shift_word(ask, 1)
    d3 = correct[::-1]
    stem = (f"In a certain code language, '{ex}' is written as '{ex_code}'. "
            f"How will '{ask}' be written in that same code?")
    diff = "M" if abs(n) <= 2 else "H"
    sol = (f"Each letter is shifted by {sign} in the alphabet "
           f"(e.g. {ex}->{ex_code}). Applying {sign} to {ask}: "
           f"{ask} -> {correct}.")
    return stem, correct, [d1, d2, d3], sol, diff, "letter_shift"

def t_letter_opposite():
    """Opposite-letter code (A<->Z). [H]"""
    ex, ask = random.sample(WORDBANK, 2)
    ex_code = opposite_word(ex)
    correct = opposite_word(ask)
    d1 = shift_word(ask, 1)          # wrong: shift
    d2 = correct[::-1]               # reversed
    d3 = shift_word(ask, -1)
    stem = (f"In a certain code, '{ex}' is coded as '{ex_code}'. "
            f"Using the same rule, how is '{ask}' coded?")
    sol = (f"Each letter is replaced by its opposite letter (A<->Z, B<->Y, ..., "
           f"position p -> 27-p), e.g. {ex}->{ex_code}. So {ask} -> {correct}.")
    return stem, correct, [d1, d2, d3], sol, "H", "letter_opposite"

def t_word_to_sum():
    """Word -> SUM of letter positions. [M/H]"""
    ask = random.choice(WORDBANK)
    total = sum(pos(c) for c in ask)
    # show one example
    ex = random.choice([w for w in WORDBANK if w != ask])
    ex_sum = sum(pos(c) for c in ex)
    correct = str(total)
    d1 = str(total + 1)
    d2 = str(total - len(ask))
    d3 = str(total * 1 + random.choice([2, 3, 5]))
    stem = (f"If the letters of a word are given values equal to their positions "
            f"in the English alphabet (A=1, B=2, ..., Z=26) and a word is coded as "
            f"the SUM of these values, then '{ex}' is coded as {ex_sum}. "
            f"What is the code for '{ask}'?")
    diff = "M" if len(ask) <= 4 else "H"
    parts = " + ".join(f"{c}({pos(c)})" for c in ask)
    sol = (f"Add the alphabet positions: {ask} = {parts} = {total}.")
    return stem, correct, [d1, d2, d3], sol, diff, "word_to_sum"

def t_word_to_product():
    """Word (<=4 letters) -> PRODUCT of letter positions. [H]"""
    ask = random.choice([w for w in WORDBANK if len(w) <= 4])
    prod = 1
    for c in ask:
        prod *= pos(c)
    ex = random.choice([w for w in WORDBANK if len(w) <= 4 and w != ask])
    ex_prod = 1
    for c in ex:
        ex_prod *= pos(c)
    correct = str(prod)
    d1 = str(prod + pos(ask[0]))
    d2 = str(sum(pos(c) for c in ask))   # used sum instead
    d3 = str(prod // pos(ask[-1]) if pos(ask[-1]) else prod + 1)
    stem = (f"In a code where A=1, B=2, ..., Z=26 and a word equals the PRODUCT of "
            f"its letters' positions, '{ex}' = {ex_prod}. What is the code for '{ask}'?")
    parts = " * ".join(f"{c}({pos(c)})" for c in ask)
    sol = (f"Multiply the alphabet positions: {ask} = {parts} = {prod}.")
    return stem, correct, [d1, d2, d3], sol, "H", "word_to_product"

def t_letter_to_position_digits():
    """Each letter -> its position number, concatenated. [M/H]"""
    ask = random.choice([w for w in WORDBANK if len(w) <= 5])
    ex = random.choice([w for w in WORDBANK if len(w) <= 5 and w != ask])
    code_of = lambda w: "-".join(str(pos(c)) for c in w)
    ex_code = code_of(ex)
    correct = code_of(ask)
    d1 = "-".join(str(pos(c) + 1) for c in ask)      # off by one
    d2 = "-".join(str(pos(c)) for c in ask[::-1])    # reversed order
    d3 = "-".join(str(27 - pos(c)) for c in ask)     # opposite position
    stem = (f"If each letter of a word is replaced by its position in the alphabet "
            f"(A=1, ..., Z=26), then '{ex}' is written as '{ex_code}'. "
            f"How is '{ask}' written?")
    diff = "M" if len(ask) <= 4 else "H"
    parts = ", ".join(f"{c}={pos(c)}" for c in ask)
    sol = (f"Replace each letter by its position ({parts}), giving '{correct}'.")
    return stem, correct, [d1, d2, d3], sol, diff, "letter_to_position"

def t_analogy_shift():
    """If WORD1 -> code (shift n), then WORD2 -> ? (same shift). Uses day/month words. [H]"""
    n = random.choice([1, 2, 3, 4, 5, -2, -3])
    pool = DAYS + MONTHS + WORDBANK
    a, b = random.sample(pool, 2)
    a_code = shift_word(a, n)
    correct = shift_word(b, n)
    sign = f"+{n}" if n >= 0 else str(n)
    d1 = shift_word(b, n + 1)
    d2 = shift_word(b, n - 1)
    d3 = correct[::-1]
    stem = (f"In a certain code, '{a}' is written as '{a_code}'. "
            f"Following the same logic, '{b}' will be written as?")
    sol = (f"The rule is a constant alphabet shift of {sign} "
           f"({a}->{a_code}). Applying {sign} to {b} gives {correct}.")
    return stem, correct, [d1, d2, d3], sol, "H", "analogy_shift"

def t_rearrange_shift():
    """Reverse the word, then shift each letter +n. [VH]"""
    n = random.choice([1, 2, 3, -1, -2])
    ex, ask = random.sample(WORDBANK, 2)
    rule = lambda w: shift_word(w[::-1], n)
    ex_code = rule(ex)
    correct = rule(ask)
    sign = f"+{n}" if n >= 0 else str(n)
    d1 = shift_word(ask, n)            # forgot to reverse
    d2 = shift_word(ask[::-1], n + 1)  # off-by-one shift
    d3 = ask[::-1]                     # reversed only, no shift
    stem = (f"In a certain code, '{ex}' is coded as '{ex_code}'. "
            f"Using the same rule, how is '{ask}' coded?")
    sol = (f"Rule: reverse the word, then shift every letter by {sign}. "
           f"{ask} -> reverse '{ask[::-1]}' -> shift {sign} -> {correct} "
           f"(verify with {ex} -> {ex_code}).")
    return stem, correct, [d1, d2, d3], sol, "VH", "rearrange_shift"

def t_number_reverse():
    """Number coding: reverse the digits. [M]"""
    ex = random.randint(123, 987)
    ask = random.randint(123, 987)
    while ask == ex:
        ask = random.randint(123, 987)
    rev = lambda x: int(str(x)[::-1])
    ex_code = rev(ex)
    correct = str(rev(ask))
    d1 = str(ask)                   # not reversed
    d2 = str(rev(ask) + 1)
    d3 = str((rev(ask) + 100) % 1000)
    stem = (f"In a certain code, the number {ex} is written as {ex_code}. "
            f"How is {ask} written in the same code?")
    sol = (f"The digits of the number are written in reverse order "
           f"({ex} -> {ex_code}). So {ask} -> {correct}.")
    return stem, correct, [d1, d2, d3], sol, "M", "number_reverse"

def t_number_arith():
    """Number coding: add k (or multiply by k). TWO example pairs make the
    rule unambiguous (a single pair like 33->66 could be +33 or *2). [H]"""
    op = random.choice(["add", "mul"])
    nums = random.sample(range(20, 99), 3)
    ex1, ex2, ask = nums
    if op == "add":
        k = random.choice([7, 11, 13, 17, 23, 29])
        f = lambda x: x + k
        desc = f"adding {k}"
    else:
        k = random.choice([2, 3, 4])
        f = lambda x: x * k
        desc = f"multiplying by {k}"
    e1, e2 = f(ex1), f(ex2)
    correct = str(f(ask))
    d1 = str(f(ask) + 1)
    d2 = str(ask)                     # unchanged
    # alternate-operation distractor: whichever op the user might confuse it with
    if op == "add":
        d3 = str(ask * 2)
    else:
        d3 = str(ask + (e1 - ex1))    # they treat the +-difference as additive
    stem = (f"If {ex1} is coded as {e1} and {ex2} is coded as {e2} in a certain code, "
            f"then {ask} will be coded as?")
    sol = (f"Both examples follow the rule of {desc} the number "
           f"({ex1}->{e1}, {ex2}->{e2}). So {ask} -> {correct}.")
    return stem, correct, [d1, d2, d3], sol, "H", "number_arith"

def t_substitution_chain():
    """Word=word substitution language; ask which word stands for a concept. [H]"""
    # build a consistent dictionary: real concept -> code word
    concepts = ["sky", "water", "air", "tree", "cloud", "rain", "fire",
                "earth", "river", "stone", "leaf", "bird"]
    codes = ["blue", "yellow", "green", "white", "red", "pink", "black",
             "brown", "grey", "orange", "violet", "gold"]
    random.shuffle(concepts)
    random.shuffle(codes)
    k = 5
    mapping = list(zip(concepts[:k], codes[:k]))  # (concept, codeword)
    # statements: "concept is called codeword"
    stmts = "; ".join(f"'{c}' is called '{w}'" for c, w in mapping)
    # pick a concept to ask the code word for
    concept, codeword = random.choice(mapping)
    correct = codeword
    others = [w for c, w in mapping if w != codeword]
    d1, d2, d3 = (others + codes[k:])[:3]
    stem = (f"In a certain language, {stmts}. "
            f"In that language, what is '{concept}' called?")
    sol = (f"From the given substitutions, '{concept}' is called '{codeword}'.")
    return stem, correct, [d1, d2, d3], sol, "H", "substitution"

def t_symbol_code():
    """Each letter -> a fixed symbol; encode a short string. [H]"""
    symbols = ["@", "#", "$", "%", "&", "*", "+", "=", "?", "!", "<", ">"]
    # pick distinct letters and assign symbols
    word = random.choice([w for w in WORDBANK if len(set(w)) == len(w) and len(w) <= 5])
    letters = list(dict.fromkeys(word))  # unique, order preserved
    # also add a couple decoy letters to the legend
    extra = [c for c in AZ if c not in letters]
    legend_letters = letters + random.sample(extra, min(3, len(extra)))
    syms = random.sample(symbols, len(legend_letters))
    code_map = dict(zip(legend_letters, syms))
    correct = "".join(code_map[c] for c in word)
    legend = ", ".join(f"{c}={code_map[c]}" for c in legend_letters)
    # distractors: swap two symbols, reverse, off legend
    swapped = correct
    if len(word) >= 2:
        lst = list(correct)
        lst[0], lst[1] = lst[1], lst[0]
        swapped = "".join(lst)
    d1 = swapped
    d2 = correct[::-1]
    d3 = correct[:-1] + random.choice([s for s in syms if s != (correct[-1] if correct else "")] + ["~"])
    stem = (f"In a code, letters are represented by symbols as follows: {legend}. "
            f"How is the word '{word}' written in this code?")
    sol = (f"Replace each letter of '{word}' by its symbol "
           f"({', '.join(f'{c}->{code_map[c]}' for c in word)}), giving '{correct}'.")
    return stem, correct, [d1, d2, d3], sol, "H", "symbol_code"

def t_mixed_letter_number():
    """Each letter -> (letter shifted +1) followed by its position. Mixed code. [VH]"""
    ask = random.choice([w for w in WORDBANK if len(w) <= 4])
    ex = random.choice([w for w in WORDBANK if len(w) <= 4 and w != ask])
    code_of = lambda w: "".join(f"{from_pos(pos(c)+1)}{pos(c)}" for c in w)
    ex_code = code_of(ex)
    correct = code_of(ask)
    # distractors
    d1 = "".join(f"{from_pos(pos(c)+1)}{pos(c)+1}" for c in ask)  # number off by one
    d2 = "".join(f"{c}{pos(c)}" for c in ask)                    # letter not shifted
    d3 = code_of(ask[::-1])                                       # reversed word
    stem = (f"In a certain code, '{ex}' is written as '{ex_code}'. "
            f"On the same pattern, how is '{ask}' written?")
    detail = ", ".join(f"{c}->{from_pos(pos(c)+1)}{pos(c)}" for c in ask)
    sol = (f"Each letter is replaced by (next letter)(its alphabet position): "
           f"{detail}. So '{ask}' -> '{correct}' (check {ex}->{ex_code}).")
    return stem, correct, [d1, d2, d3], sol, "VH", "mixed_letter_number"

def t_position_arith():
    """Each letter -> letter at (position + position_of_first_letter). Positional arithmetic. [VH]"""
    # Rule: shift each letter by +index (0-based) within the word, then show example.
    ask = random.choice([w for w in WORDBANK if len(w) <= 5])
    ex = random.choice([w for w in WORDBANK if len(w) <= 5 and w != ask])
    code_of = lambda w: "".join(from_pos(pos(c) + i) for i, c in enumerate(w))
    ex_code = code_of(ex)
    correct = code_of(ask)
    d1 = "".join(from_pos(pos(c) - i) for i, c in enumerate(ask))   # subtract index
    d2 = "".join(from_pos(pos(c) + i + 1) for i, c in enumerate(ask))  # +1 offset
    d3 = shift_word(ask, 1)                                          # constant shift
    stem = (f"In a certain code, '{ex}' is written as '{ex_code}'. "
            f"Following the same rule, how is '{ask}' coded?")
    detail = ", ".join(f"{c}(+{i})->{from_pos(pos(c)+i)}" for i, c in enumerate(ask))
    sol = (f"The k-th letter (k = 0,1,2,...) is shifted forward by k places: "
           f"{detail}. So '{ask}' -> '{correct}' (verify {ex}->{ex_code}).")
    return stem, correct, [d1, d2, d3], sol, "VH", "position_arith"

TEMPLATES = [
    t_letter_shift, t_letter_opposite, t_word_to_sum, t_word_to_product,
    t_letter_to_position_digits, t_analogy_shift, t_rearrange_shift,
    t_number_reverse, t_number_arith, t_substitution_chain, t_symbol_code,
    t_mixed_letter_number, t_position_arith,
]

DIFF_OF = {
    t_letter_shift: "M", t_letter_opposite: "H", t_word_to_sum: "M",
    t_word_to_product: "H", t_letter_to_position_digits: "M",
    t_analogy_shift: "H", t_rearrange_shift: "VH", t_number_reverse: "M",
    t_number_arith: "H", t_substitution_chain: "H", t_symbol_code: "H",
    t_mixed_letter_number: "VH", t_position_arith: "VH",
}
# Weights to target ~20% M / 60% H / 20% VH.
# M templates: letter_shift, word_to_sum, letter_to_position, number_reverse (4)
# H templates: opposite, product, analogy, number_arith, substitution, symbol (6)
# VH templates: rearrange_shift, mixed_letter_number, position_arith (3)
# Per-difficulty target counts and weights tuned so the realized mix
# lands near ~20% M / 60% H / 20% VH after dedupe.
WEIGHT = {"M": 3.4, "H": 1.7, "VH": 2.3}
POOL = []
for t in TEMPLATES:
    POOL += [t] * int(round(WEIGHT[DIFF_OF[t]] * 10))

attempts = 0
while len(questions) < 500 and attempts < 600000:
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
        print(f"Q{i}: keyed option is None"); errors += 1
stems = [q["stem"] for q in questions]
if len(set(stems)) != len(stems):
    print("DUPLICATE STEMS!"); errors += 1
assert len(questions) == 500, f"expected 500, got {len(questions)}"
assert errors == 0, f"{errors} self-check errors"
print(f"Self-check errors: {errors}")
print("Difficulty:", Counter(q["diff"] for q in questions))
print("Types:", Counter(q["qtype"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_01_Coding_Decoding_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_01_Coding_Decoding_500.key.json"

lines = []
lines.append("# Coding-Decoding — 500 Question Practice Set (SSC CGL, Reasoning / Tier-I & II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (multi-operation) — CGL standard.")
lines.append("> **Every code is generated by an exact rule and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is -0.50; the distractors are real common-mistake codes (off-by-one shift, reversed, wrong operation).\n")
lines.append("## How coding works (quick reference)")
lines.append("- **Letter shift:** each letter moves a fixed number of places (A=1...Z=26, wrap around Z->A).")
lines.append("- **Opposite letter:** position p -> 27-p (A<->Z, B<->Y, M<->N).")
lines.append("- **Positional value:** A=1, B=2, ..., Z=26; a word may be coded as the SUM or PRODUCT of these.")
lines.append("- **Number coding:** reverse the digits, or apply a fixed arithmetic operation.")
lines.append("- **Substitution:** real words are replaced by other (code) words; follow the chain.")
lines.append("- **Symbol coding:** each letter maps to a fixed symbol.")
lines.append("- **Mixed / multi-step (Very-Hard):** combine two rules, e.g. reverse then shift, or letter+position.\n")
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

# JSON sidecar: qnum -> correct string (for the independent verifier)
sidecar = {str(j + 1): questions[j]["opts"][questions[j]["ci"]] for j in range(500)}
with open(SIDECAR, "w", encoding="utf-8") as f:
    json.dump(sidecar, f, indent=0)

print(f"Wrote {OUT}")
print(f"Wrote {SIDECAR}")
print(f"Total lines: {len(lines)}")
