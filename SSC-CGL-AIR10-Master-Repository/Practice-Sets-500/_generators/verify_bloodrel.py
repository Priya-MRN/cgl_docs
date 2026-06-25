# -*- coding: utf-8 -*-
r"""
INDEPENDENT verifier for Reasoning_04_Blood_Relations_500.md

Checks (all must PASS):
  1. Re-parse the WRITTEN markdown: exactly 500 questions + 500 answers.
  2. Every question has 4 DISTINCT options.
  3. The keyed answer letter points to the option text stated in the key line,
     and that text matches the relation.
  4. Cross-check against the JSON sidecar (qnum -> relation): written == computed.
  5. Difficulty distribution is roughly 20/60/20.
  6. INDEPENDENT re-derivation: a SEPARATE mini family-graph engine (written
     here from scratch, not imported from the generator) parses the natural-
     language statements / coded chains for as many questions as it can and
     recomputes the relation, asserting it equals the keyed answer. Must cover
     >= 100 questions.

A self-test of THIS file's independent resolver runs first on 6 known trees.
NO unicode emoji: plain "PASS"/"FAIL".
"""
import re
import json
import sys

MD = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_04_Blood_Relations_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_04_Blood_Relations_500.key.json"

LETTERS = "abcd"

# ===========================================================================
# INDEPENDENT family-graph engine (separate implementation)
# ===========================================================================
class G:
    def __init__(self):
        self.g = {}      # person -> 'M'/'F'
        self.dad = {}    # person -> father
        self.mom = {}    # person -> mother
        self.sp = {}     # person -> spouse

    def set_gender(self, p, gender):
        self.g[p] = gender

    def set_father(self, child, f):
        self.dad[child] = f
        self.g[f] = 'M'

    def set_mother(self, child, m):
        self.mom[child] = m
        self.g[m] = 'F'

    def wed(self, a, b):
        self.sp[a] = b
        self.sp[b] = a

    def par(self, x):
        r = []
        if x in self.dad: r.append(self.dad[x])
        if x in self.mom: r.append(self.mom[x])
        return r

    def kids(self, x):
        return [c for c in self.g if self.dad.get(c) == x or self.mom.get(c) == x]

    def sibs(self, x):
        px = set(self.par(x))
        if not px:
            return []
        return [c for c in self.g if c != x and (set(self.par(c)) & px)]


def relate(G_, A, B):
    """How is B related to A? Independent re-implementation."""
    if A == B:
        return "self"
    if B not in G_.g:
        return None
    gb = G_.g[B]

    if G_.sp.get(A) == B:
        return "husband" if gb == 'M' else "wife"
    if B in G_.par(A):
        return "father" if gb == 'M' else "mother"
    if B in G_.kids(A):
        return "son" if gb == 'M' else "daughter"
    if B in G_.sibs(A):
        return "brother" if gb == 'M' else "sister"
    # grandparent
    gps = []
    for p in G_.par(A):
        gps += G_.par(p)
    if B in gps:
        return "grandfather" if gb == 'M' else "grandmother"
    # grandchild
    gcs = []
    for c in G_.kids(A):
        gcs += G_.kids(c)
    if B in gcs:
        return "grandson" if gb == 'M' else "granddaughter"
    # uncle/aunt
    for p in G_.par(A):
        if B in G_.sibs(p):
            return "uncle" if gb == 'M' else "aunt"
        for s in G_.sibs(p):
            if G_.sp.get(s) == B:
                return "uncle" if gb == 'M' else "aunt"
    # nephew/niece (own sibling's child, or spouse's sibling's child)
    for s in G_.sibs(A):
        if B in G_.kids(s):
            return "nephew" if gb == 'M' else "niece"
    sp = G_.sp.get(A)
    if sp is not None:
        for s in G_.sibs(sp):
            if B in G_.kids(s):
                return "nephew" if gb == 'M' else "niece"
    # in-laws via spouse
    if sp is not None:
        if B in G_.par(sp):
            return "father-in-law" if gb == 'M' else "mother-in-law"
        if B in G_.sibs(sp):
            return "brother-in-law" if gb == 'M' else "sister-in-law"
        for s in G_.sibs(sp):
            if G_.sp.get(s) == B:
                return "brother-in-law" if gb == 'M' else "sister-in-law"
    # child's spouse
    for c in G_.kids(A):
        if G_.sp.get(c) == B:
            return "son-in-law" if gb == 'M' else "daughter-in-law"
    # own sibling's spouse
    for s in G_.sibs(A):
        if G_.sp.get(s) == B:
            return "brother-in-law" if gb == 'M' else "sister-in-law"
    # cousin
    for p in G_.par(A):
        for s in G_.sibs(p):
            if B in G_.kids(s):
                return "cousin"
            ss = G_.sp.get(s)
            if ss is not None and B in G_.kids(ss):
                return "cousin"
    return None


# ===========================================================================
# SELF-TEST of THIS resolver (6 known trees)
# ===========================================================================
def self_test():
    print("---- INDEPENDENT RESOLVER SELF-TEST ----")
    cases = []
    g = G(); g.set_gender("GF", 'M'); g.set_father("F", "GF"); g.set_gender("F", 'M'); g.set_father("C", "F"); g.set_gender("C", 'M')
    cases.append((g, "C", "GF", "grandfather"))
    g = G(); g.set_gender("GM", 'F'); g.set_mother("M", "GM"); g.set_gender("M", 'F'); g.set_mother("C", "M"); g.set_gender("C", 'F')
    cases.append((g, "GM", "C", "granddaughter"))
    g = G(); g.set_gender("Gp", 'M'); g.set_father("F", "Gp"); g.set_gender("F", 'M'); g.set_father("U", "Gp"); g.set_gender("U", 'M'); g.set_father("A", "F"); g.set_gender("A", 'F')
    cases.append((g, "A", "U", "uncle"))
    g = G(); g.set_gender("P", 'F'); g.set_mother("A", "P"); g.set_gender("A", 'M'); g.set_mother("B", "P"); g.set_gender("B", 'M'); g.set_father("D", "B"); g.set_gender("D", 'F')
    cases.append((g, "A", "D", "niece"))
    g = G(); g.set_gender("WF", 'M'); g.set_father("W", "WF"); g.set_gender("W", 'F'); g.set_father("BR", "WF"); g.set_gender("BR", 'M'); g.set_gender("H", 'M'); g.wed("H", "W")
    cases.append((g, "H", "BR", "brother-in-law"))
    g = G(); g.set_gender("Gp", 'M'); g.set_father("F1", "Gp"); g.set_gender("F1", 'M'); g.set_father("F2", "Gp"); g.set_gender("F2", 'M'); g.set_father("A", "F1"); g.set_gender("A", 'F'); g.set_father("C", "F2"); g.set_gender("C", 'M')
    cases.append((g, "A", "C", "cousin"))

    allpass = True
    for g, A, B, exp in cases:
        got = relate(g, A, B)
        ok = got == exp
        allpass = allpass and ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {A}->{B}: expected {exp}, got {got}")
    print(f"---- SELF-TEST {'PASS' if allpass else 'FAIL'} ----")
    return allpass


# ===========================================================================
# PARSERS for the written statements -> independent graph -> relation
# Each returns (computed_relation) or None if the form isn't handled.
# ===========================================================================

def parse_coded(stem):
    """Coded form: '... Given 'P + Q - R', how is P related to R?'"""
    m = re.search(r"Given '([^']+)', how is (\w+) related to (\w+)\?", stem)
    if not m:
        return None
    expr, first, last = m.group(1), m.group(2), m.group(3)
    tokens = expr.split()
    # tokens: name op name op name ...
    g = G()
    names = tokens[0::2]
    ops = tokens[1::2]
    # apply
    for i, op in enumerate(ops):
        L, R = names[i], names[i + 1]
        if op == "+":      # L father of R
            g.set_father(R, L)
        elif op == "-":    # L mother of R
            g.set_mother(R, L)
        elif op == "*":    # L brother of R -> share R's parents (or L's)
            g.g[L] = 'M'
            anchor = R if (R in g.dad or R in g.mom) else (L if (L in g.dad or L in g.mom) else None)
            if anchor is None:
                return None
            other = L if anchor == R else R
            if anchor in g.dad: g.dad[other] = g.dad[anchor]
            if anchor in g.mom: g.mom[other] = g.mom[anchor]
        elif op == "/":    # L sister of R
            g.g[L] = 'F'
            anchor = R if (R in g.dad or R in g.mom) else (L if (L in g.dad or L in g.mom) else None)
            if anchor is None:
                return None
            other = L if anchor == R else R
            if anchor in g.dad: g.dad[other] = g.dad[anchor]
            if anchor in g.mom: g.mom[other] = g.mom[anchor]
        elif op == "=":    # L husband of R
            g.g[L] = 'M'
            g.wed(L, R)
        else:
            return None
    # ask how `first` related to `last`
    return relate(g, last, first)


REL_WORDS = {
    "father": ("father", 'M'), "mother": ("mother", 'F'),
    "son": ("son", 'M'), "daughter": ("daughter", 'F'),
    "brother": ("brother", 'M'), "sister": ("sister", 'F'),
}

def parse_two_step_sibling(stem):
    """'{A} is the brother/sister of {B}. {B} is the father/mother of {C}. How is {A} related to {C}?'
    Gender of A is explicit (brother/sister); B's role gives B's gender."""
    m = re.match(
        r"(\w+) is the (brother|sister) of (\w+)\. (\w+) is the (father|mother) of (\w+)\. "
        r"How is (\w+) related to (\w+)\?", stem)
    if m:
        A, ag, B, B2, bg, C, askA, askC = m.groups()
        if B2 != B or askA != A or askC != C:
            return None
        g = G()
        g.g[A] = 'M' if ag == "brother" else 'F'
        # A and B share a parent (anchor)
        g.g["P0"] = 'M'
        g.dad[A] = "P0"; g.dad[B] = "P0"
        # B is parent of C
        if bg == "father":
            g.set_father(C, B)
        else:
            g.set_mother(C, B)
        return relate(g, C, A)
    return None


def parse_photo_fathers_father(stem):
    """'He is the father of my father.' -> grandfather (X gender irrelevant)."""
    if "the father of my father" in stem:
        return "grandfather"
    if "the father of my father" in stem.lower():
        return "grandfather"
    return None

def parse_photo_brother_of_mother(stem):
    if 'He is the brother of my mother.' in stem:
        return "uncle"
    return None

def parse_photo_wife_of_brother(stem):
    if 'She is the wife of my brother.' in stem:
        return "sister-in-law"
    return None

def parse_photo_only_son(stem):
    if "daughter of the only son of my grandmother" in stem:
        return "sister"
    return None

def parse_photo_fathers_only_son(stem):
    if "son of my father's only son" in stem:
        return "nephew"
    return None


def parse_chain_inlaw(stem):
    """'{A} is married to {W}. {B} is the brother of {W}. How is {B} related to {A}?'"""
    m = re.match(r"(\w+) is married to (\w+)\. (\w+) is the brother of (\w+)\. "
                 r"How is (\w+) related to (\w+)\?", stem)
    if m:
        A, W, B, W2, askB, askA = m.groups()
        if W2 == W and askB == B and askA == A:
            g = G()
            g.g[A] = 'M'; g.g[W] = 'F'; g.wed(A, W)
            # B brother of W -> give W and B a shared father (anchor)
            g.g[B] = 'M'
            g.dad[W] = "P0"; g.dad[B] = "P0"; g.g["P0"] = 'M'
            return relate(g, A, B)
    return None

def parse_chain_grandmother(stem):
    """'{GM} is the mother of {F}. {F} is the father of {A}. How is {GM} related to {A}?'"""
    m = re.match(r"(\w+) is the mother of (\w+)\. (\w+) is the father of (\w+)\. "
                 r"How is (\w+) related to (\w+)\?", stem)
    if m:
        GM, F, F2, A, askGM, askA = m.groups()
        if F2 == F and askGM == GM and askA == A:
            g = G()
            g.set_mother(F, GM)
            g.set_father(A, F)
            return relate(g, A, GM)
    return None

def parse_chain_uncle(stem):
    """'{G} is the father of {F} and {U}. {F} is the father of {A}. How is {U} related to {A}?'"""
    m = re.match(r"(\w+) is the father of (\w+) and (\w+)\. (\w+) is the father of (\w+)\. "
                 r"How is (\w+) related to (\w+)\?", stem)
    if m:
        Gp, F, U, F2, A, askU, askA = m.groups()
        if F2 == F and askU == U and askA == A:
            g = G()
            g.set_father(F, Gp); g.set_father(U, Gp)
            g.set_father(A, F)
            return relate(g, A, U)
    return None

def parse_chain_cousin(stem):
    """'{G} is the father of {F} and {U}. {F} is the father of {A}, and {U} is the father of {X}. How is {X} related to {A}?'"""
    m = re.match(r"(\w+) is the father of (\w+) and (\w+)\. (\w+) is the father of (\w+), "
                 r"and (\w+) is the father of (\w+)\. How is (\w+) related to (\w+)\?", stem)
    if m:
        Gp, F, U, F2, A, U2, X, askX, askA = m.groups()
        if F2 == F and U2 == U and askX == X and askA == A:
            g = G()
            g.set_father(F, Gp); g.set_father(U, Gp)
            g.set_father(A, F); g.set_father(X, U)
            return relate(g, A, X)
    return None


INDEP_PARSERS = [
    parse_coded,
    parse_two_step_sibling,
    parse_photo_fathers_father,
    parse_photo_brother_of_mother,
    parse_photo_wife_of_brother,
    parse_photo_only_son,
    parse_photo_fathers_only_son,
    parse_chain_inlaw,
    parse_chain_grandmother,
    parse_chain_uncle,
    parse_chain_cousin,
]

def independent_relation(stem):
    for p in INDEP_PARSERS:
        try:
            r = p(stem)
        except Exception:
            r = None
        if r is not None:
            return r
    return None


# ===========================================================================
# PARSE the markdown file
# ===========================================================================
def parse_md(text):
    """Return questions = {n: {'stem':..., 'opts':[...]}}, answers = {n:(letter,text,diff)}"""
    parts = text.split("# =================== ANSWER KEY & EXPLANATIONS ===================")
    assert len(parts) == 2, "could not split QUESTIONS / ANSWERS sections"
    qsec, asec = parts

    questions = {}
    # Question blocks: **Qn.** stem\n(a) .. (b) .. (c) .. (d) ..
    qpat = re.compile(r"\*\*Q(\d+)\.\*\*\s*(.+?)\n\(a\)\s*(.+?)\s{2}\(b\)\s*(.+?)\s{2}\(c\)\s*(.+?)\s{2}\(d\)\s*(.+?)(?:\n|$)",
                      re.DOTALL)
    for m in qpat.finditer(qsec):
        n = int(m.group(1))
        stem = m.group(2).strip()
        opts = [m.group(3).strip(), m.group(4).strip(), m.group(5).strip(), m.group(6).strip()]
        questions[n] = {"stem": stem, "opts": opts}

    answers = {}
    apat = re.compile(r"\*\*Q(\d+)\.\s*\(([a-d])\)\s*(.+?)\*\*\s*\*\[(M|H|VH)\]\*")
    for m in apat.finditer(asec):
        n = int(m.group(1))
        letter = m.group(2)
        text = m.group(3).strip()
        diff = m.group(4)
        answers[n] = (letter, text, diff)

    return questions, answers


def main():
    ok_self = self_test()

    with open(MD, encoding="utf-8") as f:
        text = f.read()
    with open(SIDECAR, encoding="utf-8") as f:
        sidecar = json.load(f)

    questions, answers = parse_md(text)

    fails = []
    def check(cond, msg):
        if not cond:
            fails.append(msg)

    check(len(questions) == 500, f"expected 500 questions, parsed {len(questions)}")
    check(len(answers) == 500, f"expected 500 answers, parsed {len(answers)}")
    check(len(sidecar) == 500, f"sidecar has {len(sidecar)} entries")

    diff_counts = {"M": 0, "H": 0, "VH": 0}
    indep_checked = 0
    indep_fail = 0

    for n in range(1, 501):
        if n not in questions:
            fails.append(f"Q{n}: missing question"); continue
        if n not in answers:
            fails.append(f"Q{n}: missing answer"); continue
        q = questions[n]
        letter, atext, diff = answers[n]
        diff_counts[diff] += 1

        # 4 distinct options
        if len(set(q["opts"])) != 4:
            fails.append(f"Q{n}: options not distinct: {q['opts']}")

        # keyed letter points to the option equal to the stated answer text
        idx = LETTERS.index(letter)
        if idx >= len(q["opts"]):
            fails.append(f"Q{n}: letter out of range"); continue
        keyed_opt = q["opts"][idx]
        if keyed_opt != atext:
            fails.append(f"Q{n}: keyed option '{keyed_opt}' != answer text '{atext}'")

        # cross-check sidecar (written == computed relation)
        sc = sidecar.get(str(n))
        if sc != atext:
            fails.append(f"Q{n}: sidecar '{sc}' != answer '{atext}'")

        # INDEPENDENT re-derivation where possible
        ir = independent_relation(q["stem"])
        if ir is not None:
            indep_checked += 1
            if ir != atext:
                indep_fail += 1
                fails.append(f"Q{n}: INDEPENDENT resolver got '{ir}' != keyed '{atext}'  | {q['stem'][:80]}")

    # difficulty distribution sanity (allow tolerance)
    total = sum(diff_counts.values())
    print(f"Parsed {len(questions)} questions / {len(answers)} answers.")
    print(f"Difficulty: {diff_counts}  (M={diff_counts['M']/total:.0%} "
          f"H={diff_counts['H']/total:.0%} VH={diff_counts['VH']/total:.0%})")
    print(f"Independent re-derivation: checked {indep_checked} questions, {indep_fail} mismatches.")

    check(indep_checked >= 100, f"independent resolver only covered {indep_checked} (<100)")
    # skew tolerance: M 15-25, H 55-65, VH 15-25
    check(0.15 <= diff_counts['M']/total <= 0.25, "M skew out of band")
    check(0.55 <= diff_counts['H']/total <= 0.65, "H skew out of band")
    check(0.15 <= diff_counts['VH']/total <= 0.25, "VH skew out of band")

    print()
    if fails:
        print(f"VERIFY: FAIL  ({len(fails)} problems)")
        for msg in fails[:40]:
            print("  -", msg)
        sys.exit(1)
    elif not ok_self:
        print("VERIFY: FAIL  (independent resolver self-test failed)")
        sys.exit(1)
    else:
        print("VERIFY: PASS  (500 Q + 500 A, options distinct, keys match sidecar, "
              f"independent resolver agreed on {indep_checked} questions)")


if __name__ == "__main__":
    main()
