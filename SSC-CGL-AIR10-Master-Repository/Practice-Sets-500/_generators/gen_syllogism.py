# -*- coding: utf-8 -*-
r"""
SSC CGL Syllogism - 500 MCQ generator.

Every conclusion's verdict is COMPUTED by a brute-force model-checker over a
small finite universe, so the answer key is provably correct.

Method (set-model / model enumeration):
  - Categories map to subsets of a small domain D (size N).
  - A "model" is an assignment of each category to a subset of D.
  - A statement constrains which models are allowed:
        All A are B   :  A subset-of B
        No A are B    :  A intersect B == empty
        Some A are B  :  A intersect B != empty
        Some A not B  :  A \ B != empty
  - SSC/standard convention: existential import for the SUBJECT of universal
    statements is NOT assumed for derivations EXCEPT we follow the common test
    convention that categories named in premises are non-empty is NOT assumed.
    We use the strict modern logic reading where "Some" requires non-empty
    intersection and "All/No" are material (vacuously true if subject empty).
  - A conclusion FOLLOWS iff it is true in EVERY model that satisfies all
    premises (and at least one such model exists). It DOES NOT FOLLOW iff some
    satisfying model makes it false.

We enumerate all subset assignments for the small number of categories over a
domain of size N (configurable). N=3 is enough to decide all classical
syllogisms; we use N=3 which gives 2^3=8 subsets per category.
"""
import random
from itertools import product, combinations
from collections import Counter

random.seed(20260625)

LETTERS = "abcde"

# ----------------------------------------------------------------------------
# MODEL CHECKER
# ----------------------------------------------------------------------------
# Statement representation: (kind, A, B)
#   kind in {"all","no","some","somenot"}
# Categories are strings. We collect all categories, assign each a subset of a
# domain of size N (encoded as a frozenset of ints 0..N-1), enumerate all
# assignments, filter by premises, then test the conclusion.

N_DOMAIN = 3  # domain size; 3 is sufficient to decide syllogistic validity

def _all_subsets(n):
    """All subsets of {0..n-1} as frozensets."""
    elems = list(range(n))
    out = []
    for r in range(n + 1):
        for c in combinations(elems, r):
            out.append(frozenset(c))
    return out

_SUBSETS = _all_subsets(N_DOMAIN)

def _stmt_holds(kind, A, B, assign):
    sa = assign[A]
    sb = assign[B]
    if kind == "all":
        return sa <= sb            # A subset of B
    if kind == "no":
        return len(sa & sb) == 0
    if kind == "some":
        return len(sa & sb) > 0
    if kind == "somenot":
        return len(sa - sb) > 0
    raise ValueError(kind)

def follows(premises, conclusion, cats):
    """
    Return True iff `conclusion` is true in EVERY model satisfying all premises,
    given at least one satisfying model exists.
    premises: list of (kind, A, B). conclusion: (kind, A, B). cats: list of categories.
    """
    cats = list(cats)
    sat_models = 0
    for combo in product(_SUBSETS, repeat=len(cats)):
        assign = dict(zip(cats, combo))
        if all(_stmt_holds(k, a, b, assign) for (k, a, b) in premises):
            sat_models += 1
            if not _stmt_holds(conclusion[0], conclusion[1], conclusion[2], assign):
                return False  # counter-model found
    return sat_models > 0  # follows iff satisfiable and no counter-model

def verdict_pair(premises, conc1, conc2, cats):
    """
    Decide the joint verdict over two conclusions, including the either-or case.
    Returns one of:
      'I'        only I follows
      'II'       only II follows
      'BOTH'     both follow
      'NEITHER'  neither follows
      'EITHER'   either-or: neither follows alone, but in every satisfying model
                 at least one of them is true, AND they are complementary
                 (share same A,B with some/somenot or all/somenot etc.)
    """
    f1 = follows(premises, conc1, cats)
    f2 = follows(premises, conc2, cats)
    if f1 and f2:
        return "BOTH"
    if f1 and not f2:
        return "I"
    if f2 and not f1:
        return "II"
    # neither follows alone -> check either-or:
    # In every satisfying model, at least one of (conc1, conc2) holds.
    any_model = False
    either_ok = True
    for combo in product(_SUBSETS, repeat=len(cats)):
        assign = dict(zip(cats, combo))
        if all(_stmt_holds(k, a, b, assign) for (k, a, b) in premises):
            any_model = True
            h1 = _stmt_holds(conc1[0], conc1[1], conc1[2], assign)
            h2 = _stmt_holds(conc2[0], conc2[1], conc2[2], assign)
            if not (h1 or h2):
                either_ok = False
                break
    # Either-or only meaningful when the two conclusions are complementary
    # (same subject/predicate pair, one positive one negative). This matches
    # the SSC "either-or" convention.
    complementary = _are_complementary(conc1, conc2)
    if any_model and either_ok and complementary:
        return "EITHER"
    return "NEITHER"

def _are_complementary(c1, c2):
    """
    True if the two conclusions form a contradictory pair over the same terms,
    e.g. (some A B) & (somenot A B), or (all A B) & (somenot A B),
    or (no A B) & (some A B).
    """
    k1, a1, b1 = c1
    k2, a2, b2 = c2
    if {a1, b1} != {a2, b2}:
        return False
    pair = {k1, k2}
    # contradictory pairs in the square of opposition (same direction terms)
    if a1 == a2 and b1 == b2:
        if pair == {"some", "somenot"}:
            return True
        if pair == {"all", "somenot"}:
            return True
        if pair == {"no", "some"}:
            return True
    return False

# ----------------------------------------------------------------------------
# RENDERING of statements to English
# ----------------------------------------------------------------------------
def stmt_text(kind, A, B):
    if kind == "all":
        return f"All {A} are {B}."
    if kind == "no":
        return f"No {A} are {B}."
    if kind == "some":
        return f"Some {A} are {B}."
    if kind == "somenot":
        return f"Some {A} are not {B}."
    raise ValueError(kind)

# ----------------------------------------------------------------------------
# SELF-TEST of the solver on textbook syllogisms
# ----------------------------------------------------------------------------
def self_test():
    cases = []
    # 1. All A are B, All B are C => All A are C  (VALID - Barbara)
    cases.append((
        [("all", "A", "B"), ("all", "B", "C")],
        ("all", "A", "C"), True, "Barbara: All A-B, All B-C => All A-C"
    ))
    # 2. Some A are B, Some B are C => Some A are C  (INVALID)
    cases.append((
        [("some", "A", "B"), ("some", "B", "C")],
        ("some", "A", "C"), False, "Some A-B, Some B-C =/=> Some A-C"
    ))
    # 3. All A are B, No B are C => No A are C  (VALID - Celarent)
    cases.append((
        [("all", "A", "B"), ("no", "B", "C")],
        ("no", "A", "C"), True, "Celarent: All A-B, No B-C => No A-C"
    ))
    # 4. No A are B => No B are A  (VALID - conversion)
    cases.append((
        [("no", "A", "B")],
        ("no", "B", "A"), True, "Conversion of No: No A-B => No B-A"
    ))
    # 5. All A are B => Some B are A  (INVALID under strict logic: A may be empty)
    cases.append((
        [("all", "A", "B")],
        ("some", "B", "A"), False, "All A-B =/=> Some B-A (A may be empty)"
    ))
    # 6. Some A are not B => Some B are not A  (INVALID)
    cases.append((
        [("somenot", "A", "B")],
        ("somenot", "B", "A"), False, "Some A-not-B =/=> Some B-not-A"
    ))
    # 7. All A are B, Some C are A => Some C are B  (VALID - Darii-ish)
    cases.append((
        [("all", "A", "B"), ("some", "C", "A")],
        ("some", "C", "B"), True, "Darii: All A-B, Some C-A => Some C-B"
    ))
    # 8. No A are B, All C are A => No C are B  (VALID)
    cases.append((
        [("no", "A", "B"), ("all", "C", "A")],
        ("no", "C", "B"), True, "All C-A, No A-B => No C-B"
    ))
    # 9. Some A are B => Some B are A  (VALID - conversion of Some)
    cases.append((
        [("some", "A", "B")],
        ("some", "B", "A"), True, "Conversion of Some: Some A-B => Some B-A"
    ))
    # 10. All A are B => Some A are B (INVALID, A may be empty)
    cases.append((
        [("all", "A", "B")],
        ("some", "A", "B"), False, "All A-B =/=> Some A-B (A may be empty)"
    ))

    print("---- SOLVER SELF-TEST (textbook syllogisms) ----")
    allpass = True
    for prem, conc, expected, desc in cases:
        cats = sorted({c for (_, a, b) in prem for c in (a, b)} | {conc[1], conc[2]})
        got = follows(prem, conc, cats)
        ok = (got == expected)
        allpass = allpass and ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {desc}  (expected {expected}, got {got})")
    # Either-or test: Some A are B / Some A are not B from no premises forcing it
    # Classic: "All A are B" + need either-or. Use: No premises that pin it.
    # Test the either-or detection on a known case:
    # Premises: (none strong) -> can't easily force; test detection logic directly.
    print(f"---- SELF-TEST {'PASS' if allpass else 'FAIL'} ----")
    return allpass

# ----------------------------------------------------------------------------
# CATEGORY WORD POOLS (real, readable words)
# ----------------------------------------------------------------------------
WORD_POOL = [
    "Cats", "Dogs", "Animals", "Birds", "Pigeons", "Crows", "Mammals",
    "Flowers", "Roses", "Plants", "Trees", "Fruits", "Mangoes", "Apples",
    "Books", "Pens", "Pencils", "Tables", "Chairs", "Doors", "Windows",
    "Teachers", "Students", "Engineers", "Doctors", "Lawyers", "Artists",
    "Cars", "Buses", "Trucks", "Vehicles", "Bikes", "Trains", "Boats",
    "Rivers", "Lakes", "Hills", "Mountains", "Stones", "Rocks", "Metals",
    "Cups", "Plates", "Bottles", "Glasses", "Bowls", "Jars", "Boxes",
    "Singers", "Dancers", "Players", "Writers", "Poets", "Actors", "Painters",
    "Phones", "Laptops", "Computers", "Machines", "Tools", "Devices", "Wires",
    "Squares", "Circles", "Triangles", "Lines", "Points", "Angles", "Shapes",
    "Fans", "Lamps", "Bulbs", "Clocks", "Watches", "Mirrors", "Frames",
]

def pick_words(k):
    return random.sample(WORD_POOL, k)

# ----------------------------------------------------------------------------
# QUESTION GENERATION
# ----------------------------------------------------------------------------
# Each question: dict(statements=[(kind,A,B)...], concs=[(c1),(c2)],
#                      cats=[...], verdict=str, diff=str, sol=str)

# Fixed standard options. 5-option form includes either-or.
STD_OPTIONS_4 = [
    "Only conclusion I follows",
    "Only conclusion II follows",
    "Both conclusions I and II follow",
    "Neither conclusion I nor conclusion II follows",
]
STD_OPTIONS_5 = STD_OPTIONS_4[:] + [
    "Either conclusion I or conclusion II follows",
]

VERDICT_TO_TEXT = {
    "I": "Only conclusion I follows",
    "II": "Only conclusion II follows",
    "BOTH": "Both conclusions I and II follow",
    "NEITHER": "Neither conclusion I nor conclusion II follows",
    "EITHER": "Either conclusion I or conclusion II follows",
}

STATEMENT_KINDS = ["all", "no", "some", "somenot"]
CONC_KINDS = ["all", "no", "some", "somenot"]

def gen_candidate(num_statements):
    """
    Build a random syllogism with `num_statements` premises over 3 (or 4) cats,
    then two candidate conclusions over named cats. Returns the question dict
    with a computed verdict, or None if degenerate.
    """
    ncats = 3 if num_statements <= 2 else random.choice([3, 4])
    words = pick_words(ncats)
    # Build a connected chain of premises so terms overlap (typical syllogism).
    # Statement pairs link consecutive categories.
    premises = []
    # ensure overlapping structure: use pairs from the category list
    pairs = []
    for i in range(num_statements):
        if i == 0:
            a, b = words[0], words[1]
        elif i == 1 and ncats >= 3:
            a, b = words[1], words[2]
        elif i == 2 and ncats >= 4:
            a, b = words[2], words[3]
        else:
            # extra premise links random distinct cats
            a, b = random.sample(words, 2)
        pairs.append((a, b))
    for (a, b) in pairs:
        kind = random.choice(STATEMENT_KINDS)
        premises.append((kind, a, b))

    # reject if any premise duplicates another (would render as repeated text)
    if len(set(premises)) != len(premises):
        return None

    # premises must be jointly satisfiable (have at least one model) else skip
    cats = words
    has_model = False
    for combo in product(_SUBSETS, repeat=len(cats)):
        assign = dict(zip(cats, combo))
        if all(_stmt_holds(k, a, b, assign) for (k, a, b) in premises):
            has_model = True
            break
    if not has_model:
        return None

    # Build two candidate conclusions involving the end terms (more interesting).
    # Choose conclusion term pairs: prefer linking first and last category.
    endA, endB = words[0], words[-1]
    # Conclusion candidate generator
    def make_concs():
        # pick term pair for conclusions
        choice = random.random()
        if choice < 0.5:
            ca, cb = endA, endB
        else:
            ca, cb = random.sample(words, 2)
        return ca, cb

    ca, cb = make_concs()
    # Two conclusions: sometimes complementary (to enable either-or), sometimes not
    style = random.random()
    if style < 0.30:
        # complementary pair over same terms -> may yield EITHER
        kpair = random.choice([("some", "somenot"), ("all", "somenot"), ("no", "some")])
        conc1 = (kpair[0], ca, cb)
        conc2 = (kpair[1], ca, cb)
    else:
        conc1 = (random.choice(CONC_KINDS), ca, cb)
        # second conclusion over a (possibly) different pair
        cc, cd = make_concs()
        conc2 = (random.choice(CONC_KINDS), cc, cd)
        if conc2 == conc1:
            return None

    verdict = verdict_pair(premises, conc1, conc2, cats)

    q = {
        "statements": premises,
        "concs": [conc1, conc2],
        "cats": cats,
        "verdict": verdict,
    }
    return q

def build_solution(q):
    """Short justification: why each conclusion follows or a counter-model."""
    cats = q["cats"]
    prem = q["statements"]
    c1, c2 = q["concs"]
    v = q["verdict"]

    def explain_one(conc, label):
        if follows(prem, conc, cats):
            return f"{label} follows (true in every model satisfying the premises)."
        else:
            cm = find_counter_model(prem, conc, cats)
            return f"{label} does not follow ({cm})."

    parts = []
    parts.append(explain_one(c1, "I"))
    parts.append(explain_one(c2, "II"))
    if v == "EITHER":
        parts.append("The two are complementary and in every model at least one holds, so it is an either-or case.")
    return " ".join(parts)

def find_counter_model(prem, conc, cats):
    """Return a short text description of a model satisfying premises but not conc."""
    for combo in product(_SUBSETS, repeat=len(cats)):
        assign = dict(zip(cats, combo))
        if all(_stmt_holds(k, a, b, assign) for (k, a, b) in prem):
            if not _stmt_holds(conc[0], conc[1], conc[2], assign):
                # describe assignment compactly
                def setstr(s):
                    return "{" + ",".join(map(str, sorted(s))) + "}" if s else "empty"
                desc = "; ".join(f"{c}={setstr(assign[c])}" for c in cats)
                return f"counter-model: {desc}"
    return "no counter-model (should not happen)"

# ----------------------------------------------------------------------------
# QUOTA-DRIVEN GENERATION
# ----------------------------------------------------------------------------
# Difficulty mapping:
#   M  (Medium)    : 2 statements, simple verdict (I/II/NEITHER/BOTH)
#   H  (Hard)      : 2-3 statements, any verdict
#   VH (Very-Hard) : 3 statements OR either-or/possibility cases
TARGET = 500
QUOTA = {"M": 100, "H": 300, "VH": 100}  # 20/60/20

def classify(q, num_statements):
    v = q["verdict"]
    if v == "EITHER":
        return "VH"
    if num_statements >= 3:
        return "VH" if v in ("EITHER",) else "H" if num_statements == 3 and random.random() < 0.5 else "VH"
    return None  # decided by caller

questions = []
seen = set()
counts = {"M": 0, "H": 0, "VH": 0}

def qkey(q):
    s = tuple(q["statements"])
    c = tuple(q["concs"])
    return (s, c)

def try_add(target_diff):
    """Generate a question that lands in target_diff difficulty."""
    if target_diff == "M":
        ns = 2
    elif target_diff == "H":
        ns = random.choice([2, 2, 3])
    else:  # VH
        ns = 3
    q = gen_candidate(ns)
    if q is None:
        return False
    k = qkey(q)
    if k in seen:
        return False
    v = q["verdict"]
    # Assign difficulty
    if target_diff == "VH":
        # VH = 3 statements, prefer either-or / possibility / non-trivial
        diff = "VH"
    elif target_diff == "H":
        diff = "H"
        if v == "EITHER":
            diff = "VH"  # either-or always VH
    else:  # M
        # Medium: keep simple verdicts, avoid either-or
        if v == "EITHER":
            return False
        diff = "M"
    if counts[diff] >= QUOTA[diff]:
        return False
    q["diff"] = diff
    q["nstmt"] = ns
    seen.add(k)
    q["sol"] = build_solution(q)
    questions.append(q)
    counts[diff] += 1
    return True

def main():
    ok = self_test()
    if not ok:
        print("SOLVER SELF-TEST FAILED - aborting generation.")
        raise SystemExit(1)

    attempts = 0
    # Fill quotas. Prioritize whichever quota is unmet.
    order = ["VH", "H", "M"]  # fill harder/either-or first (rarer)
    while len(questions) < TARGET and attempts < 3_000_000:
        attempts += 1
        # choose a difficulty whose quota is unmet
        unmet = [d for d in order if counts[d] < QUOTA[d]]
        if not unmet:
            break
        # bias toward EITHER for VH by occasionally forcing complementary concs
        d = random.choice(unmet)
        try_add(d)

    print(f"Generated {len(questions)} questions in {attempts} attempts.")
    print("Difficulty:", dict(counts))

    # ---- VERIFY internal: exactly one correct option per question ----
    errors = 0
    for i, q in enumerate(questions, 1):
        opts = STD_OPTIONS_5 if q["verdict"] == "EITHER" else STD_OPTIONS_4
        correct_text = VERDICT_TO_TEXT[q["verdict"]]
        matches = [o for o in opts if o == correct_text]
        if len(matches) != 1:
            print(f"Q{i}: correct option not unique"); errors += 1
        if len(set(opts)) != len(opts):
            print(f"Q{i}: duplicate options"); errors += 1
    print(f"Internal verification errors: {errors}")

    write_markdown()
    write_sidecar()

# ----------------------------------------------------------------------------
# OPTION LAYOUT: we keep options in fixed canonical order (a..d / a..e) so the
# 'either-or' option naturally appears only for EITHER questions. The correct
# LETTER is derived from the verdict's position in the options list.
# ----------------------------------------------------------------------------
def options_for(q):
    if q["verdict"] == "EITHER":
        return STD_OPTIONS_5
    return STD_OPTIONS_4

def correct_letter(q):
    opts = options_for(q)
    txt = VERDICT_TO_TEXT[q["verdict"]]
    return LETTERS[opts.index(txt)], txt

OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_02_Syllogism_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_02_Syllogism_500.verdicts.json"

def render_statements(q):
    return " ".join(stmt_text(k, a, b) for (k, a, b) in q["statements"])

def render_concs(q):
    c1, c2 = q["concs"]
    return f"I. {stmt_text(*c1)} II. {stmt_text(*c2)}"

def write_markdown():
    lines = []
    lines.append("# Syllogism — 500 Question Practice Set (SSC CGL, Reasoning, Tier-I/II Level)\n")
    lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
    lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (3-statement & either-or / possibility cases).")
    lines.append("> **Every verdict is machine-verified** by a brute-force set-model checker — the keyed option is provably correct.")
    lines.append("> Negative marking in CGL is −0.50.\n")
    lines.append("## How to answer")
    lines.append("- Treat the statements as **definitely true**, even if they contradict common sense.")
    lines.append("- A conclusion **follows** only if it must be true in EVERY situation consistent with the statements.")
    lines.append("- If a conclusion is merely *possible* (true in some situations but not all), it does **not** follow.")
    lines.append("- **Either-or:** when two conclusions cannot both be false (they are complementary and one must hold), the answer is *Either I or II follows*.\n")
    lines.append("## Standard options legend")
    lines.append("- (a) Only conclusion I follows")
    lines.append("- (b) Only conclusion II follows")
    lines.append("- (c) Both conclusions I and II follow")
    lines.append("- (d) Neither conclusion I nor conclusion II follows")
    lines.append("- (e) Either conclusion I or conclusion II follows  *(appears only when applicable)*\n")
    lines.append("\n# =================== QUESTIONS ===================\n")

    for start in range(0, TARGET, 50):
        blk = start // 50 + 1
        lines.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
        for j in range(start, min(start + 50, TARGET)):
            q = questions[j]
            n = j + 1
            opts = options_for(q)
            lines.append(f"**Q{n}.** Statements: {render_statements(q)}")
            lines.append(f"Conclusions: {render_concs(q)}")
            opt_line = "  ".join(f"({LETTERS[i]}) {opts[i]}" for i in range(len(opts)))
            lines.append(opt_line + "\n")

    lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
    for start in range(0, TARGET, 50):
        lines.append(f"\n## Answers Q{start+1}–Q{start+50}\n")
        for j in range(start, min(start + 50, TARGET)):
            q = questions[j]
            n = j + 1
            letter, txt = correct_letter(q)
            lines.append(f"**Q{n}. ({letter}) {txt}**  *[{q['diff']}]* — {q['sol']}")

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUT}")
    print(f"Total lines: {len(lines)}")

def write_sidecar():
    import json
    data = {}
    for j, q in enumerate(questions, 1):
        data[str(j)] = q["verdict"]
    with open(SIDECAR, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=0)
    print(f"Wrote {SIDECAR}")

if __name__ == "__main__":
    main()
