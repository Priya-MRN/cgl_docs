# -*- coding: utf-8 -*-
r"""
Verifier for Reasoning_07_Venn_Diagrams_500.md.

Re-parses the WRITTEN markdown file and asserts:
  * 500 questions and 500 answers present
  * each question has 4 distinct options (a,b,c,d)
  * the keyed option letter in the answer key maps to an option whose TEXT
    matches the stated answer value in the answer line
  * cross-checks every numeric answer against the JSON sidecar
  * INDEPENDENTLY re-solves >=100 numeric set-counting questions by re-parsing
    the counts straight out of the stem and re-applying inclusion-exclusion
    from scratch (no reuse of generator code).

Plain PASS/FAIL only. No unicode emoji.
"""
import re
import json
import sys

MD = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_07_Venn_Diagrams_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_07_Venn_Diagrams_500.answers.json"

failures = []


def fail(msg):
    failures.append(msg)


def main():
    with open(MD, "r", encoding="utf-8") as f:
        text = f.read()

    parts = text.split("# =================== ANSWER KEY & EXPLANATIONS ===================")
    if len(parts) != 2:
        fail("Could not split QUESTIONS / ANSWER KEY sections.")
        report(); return
    qsec, asec = parts

    # ---- parse questions ----
    # **Qn.** stem  (may span; stem ends before option line)
    # option line: (a) ...  (b) ...  (c) ...  (d) ...
    q_blocks = re.split(r"\*\*Q(\d+)\.\*\*", qsec)
    # q_blocks: [pre, '1', body1, '2', body2, ...]
    questions = {}
    for i in range(1, len(q_blocks), 2):
        qn = int(q_blocks[i])
        body = q_blocks[i + 1]
        questions[qn] = body

    if len(questions) != 500:
        fail(f"Expected 500 questions, found {len(questions)}.")

    opt_re = re.compile(
        r"\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\s*$",
        re.S | re.M)

    parsed_opts = {}
    parsed_stem = {}
    for qn, body in questions.items():
        m = opt_re.search(body)
        if not m:
            fail(f"Q{qn}: cannot parse 4 options.")
            continue
        opts = [m.group(1).strip(), m.group(2).strip(),
                m.group(3).strip(), m.group(4).strip()]
        # stem is everything before the option line
        stem = body[:m.start()].strip()
        parsed_opts[qn] = opts
        parsed_stem[qn] = stem
        if len(set(opts)) != 4:
            fail(f"Q{qn}: options not distinct: {opts}")

    # ---- parse answers ----
    # **Qn. (x) VALUE**  *[DIFF]* — explanation
    ans_re = re.compile(
        r"\*\*Q(\d+)\.\s*\(([a-d])\)\s*(.*?)\*\*\s*\*\[(M|H|VH)\]\*\s*[—-]\s*(.*)")
    answers = {}
    for line in asec.splitlines():
        m = ans_re.search(line)
        if m:
            qn = int(m.group(1))
            letter = m.group(2)
            val = m.group(3).strip()
            diff = m.group(4)
            answers[qn] = (letter, val, diff)

    if len(answers) != 500:
        fail(f"Expected 500 answers, found {len(answers)}.")

    # ---- keyed option text matches stated answer value ----
    L2I = {"a": 0, "b": 1, "c": 2, "d": 3}
    for qn in range(1, 501):
        if qn not in answers or qn not in parsed_opts:
            continue
        letter, val, diff = answers[qn]
        idx = L2I[letter]
        keyed_opt = parsed_opts[qn][idx]
        if keyed_opt.strip() != val.strip():
            fail(f"Q{qn}: keyed option ({letter})='{keyed_opt}' != answer value '{val}'.")

    # ---- difficulty distribution ----
    from collections import Counter
    dc = Counter(answers[q][2] for q in answers)
    total = sum(dc.values())
    print(f"Difficulty distribution: {dict(dc)}  (M%={100*dc['M']//total} "
          f"H%={100*dc['H']//total} VH%={100*dc['VH']//total})")

    # ---- sidecar cross-check ----
    with open(SIDECAR, "r", encoding="utf-8") as f:
        sidecar = json.load(f)
    sc_checked = 0
    for k, v in sidecar.items():
        qn = int(k)
        if qn not in answers:
            fail(f"Q{qn}: in sidecar but no answer parsed."); continue
        letter, val, diff = answers[qn]
        if val.strip() != str(v):
            fail(f"Q{qn}: sidecar={v} but keyed answer value={val}.")
        sc_checked += 1
    print(f"Sidecar numeric answers cross-checked: {sc_checked}")

    # ---- INDEPENDENT re-solve of numeric set-counting questions ----
    independent_ok = 0
    independent_attempt = 0
    for qn in range(1, 501):
        if qn not in parsed_stem or qn not in answers:
            continue
        stem = re.sub(r"\s+", " ", parsed_stem[qn])
        expected = answers[qn][1].strip()
        solved = resolve(stem)
        if solved is None:
            continue
        independent_attempt += 1
        if str(solved) == expected:
            independent_ok += 1
        else:
            fail(f"Q{qn}: independent re-solve = {solved} but key = {expected}. STEM: {stem[:160]}")
    print(f"Independent re-solves attempted: {independent_attempt}, matched: {independent_ok}")
    if independent_attempt < 100:
        fail(f"Independent re-solve count {independent_attempt} < 100.")

    report()


def grab(label_regexes, stem):
    """Return first integer following any of the regex patterns, else None."""
    for rx in label_regexes:
        m = re.search(rx, stem)
        if m:
            return int(m.group(1))
    return None


def resolve(stem):
    """
    Independently re-solve a numeric set-counting question by parsing the counts
    from the stem text and applying inclusion-exclusion from scratch.
    Handles three families:
      - 3-set worded survey (n(A),n(B),n(C),pairwise,all,question)
      - 3-set diagram (region values)
      - 2-set worded survey
    Returns an integer answer or None if not a recognized numeric stem.
    """
    s = stem

    # ---------- 3-set DIAGRAM style ----------
    if "the region values are" in s:
        m_aonly = re.search(r"only ([A-Z]) = (\d+), only ([A-Z]) = (\d+), only ([A-Z]) = (\d+)", s)
        m_pairs = re.search(r"([A-Z])∩([A-Z]) only = (\d+), ([A-Z])∩([A-Z]) only = (\d+), ([A-Z])∩([A-Z]) only = (\d+)", s)
        m_abc = re.search(r"∩[A-Z]∩[A-Z] = (\d+)", s)
        m_out = re.search(r"outside all = (\d+)", s)
        if not (m_aonly and m_pairs and m_abc and m_out):
            return None
        nameA, va, nameB, vb, nameC, vc = m_aonly.group(1), int(m_aonly.group(2)), \
            m_aonly.group(3), int(m_aonly.group(4)), m_aonly.group(5), int(m_aonly.group(6))
        only = {nameA: va, nameB: vb, nameC: vc}
        p1a, p1b, p1v = m_pairs.group(1), m_pairs.group(2), int(m_pairs.group(3))
        p2a, p2b, p2v = m_pairs.group(4), m_pairs.group(5), int(m_pairs.group(6))
        p3a, p3b, p3v = m_pairs.group(7), m_pairs.group(8), int(m_pairs.group(9))
        pair = {frozenset((p1a, p1b)): p1v, frozenset((p2a, p2b)): p2v, frozenset((p3a, p3b)): p3v}
        abc = int(m_abc.group(1))
        out = int(m_out.group(1))
        inner = va + vb + vc + p1v + p2v + p3v + abc
        # which question?
        mq = re.search(r"What is n\(([A-Z])\)\?", s)
        if mq:
            X = mq.group(1)
            res = only[X] + abc
            for k, v in pair.items():
                if X in k:
                    res += v
            return res
        if "at least one set" in s:
            return inner
        if "total (universal set size)" in s:
            return inner + out
        if "exactly two of the three sets" in s:
            return p1v + p2v + p3v
        return None

    # ---------- 3-set WORDED survey ----------
    # detect three "do both (X and Y)" phrases + "do all three"
    pair_matches = re.findall(r"(\d+) do both \(([^)]+) and ([^)]+)\)", s)
    all_three = re.search(r"(\d+) do all three", s)
    if len(pair_matches) == 3 and all_three:
        abc = int(all_three.group(1))
        # parse n(A),n(B),n(C): the three leading "N <verb>" counts. We need a
        # robust mapping. The stem pattern: "<N1> <act A>, <N2> <act B> and <N3> <act C>."
        # We instead recover nA,nB,nC,nAB,nBC,nCA by name using the pair labels.
        # The pairwise counts are labelled by category names X,Y.
        pair = {}
        for cnt, x, y in pair_matches:
            pair[frozenset((x.strip(), y.strip()))] = int(cnt)
        cats = set()
        for k in pair:
            cats |= set(k)
        cats = list(cats)
        if len(cats) != 3:
            return None
        # n(category): find "<num> <something containing category>" — but the
        # survey uses verbs not names for the singles. Instead, the three big
        # numbers appear as: ", <nB> " etc. Use the structured lead:
        # "In <pop>, <nA> <fa>, <nB> <fb> and <nC> <fc>."
        lead = re.search(r"In .*?, (\d+) .*?, (\d+) .*? and (\d+) .*?\. \d+ do both", s)
        if not lead:
            return None
        n1, n2, n3 = int(lead.group(1)), int(lead.group(2)), int(lead.group(3))
        # Map n1->A, n2->B, n3->C by the order categories appear in the pair
        # labels. The generator labels pairs as (A,B),(B,C),(C,A). Determine A,B,C
        # from question phrasing: "ONLY <X>", or pair order.
        # Build ordering A,B,C: A appears in pairs[0] & pairs[2]; etc.
        # Reconstruct from pair_matches order (AB, BC, CA):
        (ab_x, ab_y) = pair_matches[0][1].strip(), pair_matches[0][2].strip()
        (bc_x, bc_y) = pair_matches[1][1].strip(), pair_matches[1][2].strip()
        (ca_x, ca_y) = pair_matches[2][1].strip(), pair_matches[2][2].strip()
        A = ab_x; B = ab_y; C = bc_y
        # sanity
        if not (frozenset((A, B)) in pair and frozenset((B, C)) in pair and frozenset((C, A)) in pair):
            return None
        nA, nB, nC = n1, n2, n3
        nAB = pair[frozenset((A, B))]
        nBC = pair[frozenset((B, C))]
        nCA = pair[frozenset((C, A))]
        at_least_one = nA + nB + nC - nAB - nBC - nCA + abc
        only_A = nA - nAB - nCA + abc
        only_B = nB - nAB - nBC + abc
        only_C = nC - nBC - nCA + abc
        exactly_two = (nAB - abc) + (nBC - abc) + (nCA - abc)
        exactly_one = only_A + only_B + only_C

        mq = re.search(r"How many do ONLY (\S+) \(", s)
        if mq:
            X = mq.group(1).strip()
            if X == A: return only_A
            if X == B: return only_B
            if X == C: return only_C
            return None
        if "EXACTLY two" in s:
            return exactly_two
        if "at least one of the three" in s:
            return at_least_one
        if "EXACTLY one" in s:
            return exactly_one
        if "NONE of the three" in s:
            mt = re.search(r"total = (\d+)", s)
            if mt:
                return int(mt.group(1)) - at_least_one
            return None
        return None

    # ---------- 2-set WORDED survey ----------
    both_m = re.search(r"(\d+) did both", s)
    # union form: "If <U> ... at least one ..., how many did BOTH?"
    if "how many did BOTH" in s:
        m = re.search(r", (\d+) .*? and (\d+) .*?\.", s)
        mu = re.search(r"If (\d+) ", s)
        if m and mu:
            nA, nB = int(m.group(1)), int(m.group(2))
            union = int(mu.group(1))
            return nA + nB - union
        return None
    if both_m:
        both = int(both_m.group(1))
        # need nA, nB: "In <pop>, <nA> <fa>, <nB> <fb>, and <both> did both."
        lead = re.search(r"In .*?, (\d+) .*?, (\d+) .*?, and \d+ did both", s)
        if not lead:
            return None
        nA, nB = int(lead.group(1)), int(lead.group(2))
        union = nA + nB - both
        if "EXACTLY ONE" in s:
            return (nA - both) + (nB - both)
        if "AT LEAST ONE" in s:
            return union
        if "NEITHER" in s:
            mt = re.search(r"total = (\d+)", s)
            if mt:
                return int(mt.group(1)) - union
            return None
        return None

    return None


def report():
    if failures:
        print("---- FAILURES ----")
        for fmsg in failures[:60]:
            print("  " + fmsg)
        print(f"TOTAL FAILURES: {len(failures)}")
        print("FAIL")
        sys.exit(1)
    else:
        print("All checks passed.")
        print("PASS")


if __name__ == "__main__":
    main()
