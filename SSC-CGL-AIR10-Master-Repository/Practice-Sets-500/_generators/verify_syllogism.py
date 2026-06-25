# -*- coding: utf-8 -*-
r"""
Independent verifier for the Syllogism 500 set.

Re-parses the WRITTEN markdown file (no shared state with the generator), then:
  1. asserts 500 questions and 500 answers,
  2. checks each question's options are distinct and in standard form,
  3. checks the keyed answer letter matches the option text it names,
  4. re-runs an INDEPENDENT model-checker on the parsed statements + conclusions
     for >= 100 questions and confirms the computed verdict matches the key,
  5. cross-checks every question against the JSON sidecar (qnum -> verdict).

Emits plain "PASS"/"FAIL" only (no unicode emoji).
"""
import re
import json
import sys
from itertools import product, combinations

MD = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_02_Syllogism_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_02_Syllogism_500.verdicts.json"

# ---------------------------------------------------------------------------
# INDEPENDENT model checker (re-implemented from scratch, not imported)
# ---------------------------------------------------------------------------
N = 3

def subsets(n):
    out = []
    for r in range(n + 1):
        for c in combinations(range(n), r):
            out.append(frozenset(c))
    return out

SUBS = subsets(N)

def holds(kind, A, B, asg):
    sa, sb = asg[A], asg[B]
    if kind == "all":
        return sa <= sb
    if kind == "no":
        return not (sa & sb)
    if kind == "some":
        return bool(sa & sb)
    if kind == "somenot":
        return bool(sa - sb)
    raise ValueError(kind)

def follows(prem, conc, cats):
    cats = list(cats)
    sat = 0
    for combo in product(SUBS, repeat=len(cats)):
        asg = dict(zip(cats, combo))
        if all(holds(k, a, b, asg) for (k, a, b) in prem):
            sat += 1
            if not holds(conc[0], conc[1], conc[2], asg):
                return False
    return sat > 0

def complementary(c1, c2):
    k1, a1, b1 = c1
    k2, a2, b2 = c2
    if a1 != a2 or b1 != b2:
        return False
    pair = {k1, k2}
    return pair in ({"some", "somenot"}, {"all", "somenot"}, {"no", "some"})

def compute_verdict(prem, c1, c2, cats):
    f1 = follows(prem, c1, cats)
    f2 = follows(prem, c2, cats)
    if f1 and f2:
        return "BOTH"
    if f1:
        return "I"
    if f2:
        return "II"
    any_model = False
    either = True
    for combo in product(SUBS, repeat=len(cats)):
        asg = dict(zip(cats, combo))
        if all(holds(k, a, b, asg) for (k, a, b) in prem):
            any_model = True
            if not (holds(*c1, asg) if False else holds(c1[0], c1[1], c1[2], asg)
                    or holds(c2[0], c2[1], c2[2], asg)):
                either = False
                break
    if any_model and either and complementary(c1, c2):
        return "EITHER"
    return "NEITHER"

# ---------------------------------------------------------------------------
# PARSING the English statements back into (kind, A, B)
# ---------------------------------------------------------------------------
RE_ALL = re.compile(r"^All (.+?) are (.+?)\.$")
RE_NO = re.compile(r"^No (.+?) are (.+?)\.$")
RE_SOMENOT = re.compile(r"^Some (.+?) are not (.+?)\.$")
RE_SOME = re.compile(r"^Some (.+?) are (.+?)\.$")

def parse_stmt(s):
    s = s.strip()
    m = RE_SOMENOT.match(s)
    if m:
        return ("somenot", m.group(1), m.group(2))
    m = RE_ALL.match(s)
    if m:
        return ("all", m.group(1), m.group(2))
    m = RE_NO.match(s)
    if m:
        return ("no", m.group(1), m.group(2))
    m = RE_SOME.match(s)
    if m:
        return ("some", m.group(1), m.group(2))
    raise ValueError(f"cannot parse statement: {s!r}")

def split_sentences(text):
    """Split a run of 'X. Y. Z.' into individual sentence strings (with period)."""
    parts = re.findall(r"[^.]*\.", text)
    return [p.strip() for p in parts if p.strip()]

TEXT_TO_VERDICT = {
    "Only conclusion I follows": "I",
    "Only conclusion II follows": "II",
    "Both conclusions I and II follow": "BOTH",
    "Neither conclusion I nor conclusion II follows": "NEITHER",
    "Either conclusion I or conclusion II follows": "EITHER",
}

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

def main():
    with open(MD, encoding="utf-8") as f:
        text = f.read()

    # ---- parse QUESTIONS ----
    # Each question block:
    #   **Qn.** Statements: ...
    #   Conclusions: I. ... II. ...
    #   (a) ...  (b) ...  ...
    q_re = re.compile(
        r"\*\*Q(\d+)\.\*\*\s+Statements:\s*(.+?)\n"
        r"Conclusions:\s*(.+?)\n"
        r"((?:\([a-e]\)[^\n]*\n?)+)",
        re.DOTALL,
    )
    questions = {}
    for m in q_re.finditer(text):
        n = int(m.group(1))
        stmts_raw = m.group(2).strip()
        concs_raw = m.group(3).strip()
        opts_raw = m.group(4).strip()
        # options
        opts = dict(re.findall(r"\(([a-e])\)\s*([^\n(]+?)(?=\s*\([a-e]\)|\s*$)", opts_raw))
        opts = {k: v.strip() for k, v in opts.items()}
        # conclusions: "I. <s1> II. <s2>"
        cm = re.match(r"I\.\s*(.+?)\s*II\.\s*(.+)$", concs_raw)
        if not cm:
            fail(f"Q{n}: cannot parse conclusions: {concs_raw!r}")
        c1 = parse_stmt(cm.group(1))
        c2 = parse_stmt(cm.group(2))
        stmts = [parse_stmt(s) for s in split_sentences(stmts_raw)]
        questions[n] = {
            "stmts": stmts,
            "concs": [c1, c2],
            "opts": opts,
        }

    nq = len(questions)
    print(f"Parsed {nq} questions.")
    if nq != 500:
        fail(f"expected 500 questions, got {nq}")

    # ---- parse ANSWERS ----
    # **Qn. (x) <text>**  *[DIFF]* — <sol>
    a_re = re.compile(
        r"\*\*Q(\d+)\.\s*\(([a-e])\)\s*(.+?)\*\*\s*\*\[(M|H|VH)\]\*",
    )
    answers = {}
    diffs = {}
    for m in a_re.finditer(text):
        n = int(m.group(1))
        letter = m.group(2)
        atext = m.group(3).strip()
        answers[n] = (letter, atext)
        diffs[n] = m.group(4)
    na = len(answers)
    print(f"Parsed {na} answers.")
    if na != 500:
        fail(f"expected 500 answers, got {na}")

    # ---- sidecar ----
    with open(SIDECAR, encoding="utf-8") as f:
        sidecar = json.load(f)
    if len(sidecar) != 500:
        fail(f"sidecar has {len(sidecar)} entries, expected 500")

    # ---- per-question structural + key checks ----
    errors = 0
    for n in range(1, 501):
        if n not in questions:
            fail(f"missing question {n}")
        if n not in answers:
            fail(f"missing answer {n}")
        q = questions[n]
        letter, atext = answers[n]
        opts = q["opts"]
        # options distinct
        vals = list(opts.values())
        if len(set(vals)) != len(vals):
            print(f"Q{n}: duplicate option text {vals}"); errors += 1
        # answer letter present and text matches the option it names
        if letter not in opts:
            print(f"Q{n}: answer letter {letter} not among options"); errors += 1
            continue
        if opts[letter] != atext:
            print(f"Q{n}: keyed letter ({letter}) text {opts[letter]!r} != answer text {atext!r}")
            errors += 1
        # answer text must be a valid standard option text
        if atext not in TEXT_TO_VERDICT:
            print(f"Q{n}: answer text not a standard option: {atext!r}"); errors += 1
            continue
        # sidecar verdict must match the answer text's verdict
        key_verdict = TEXT_TO_VERDICT[atext]
        if sidecar.get(str(n)) != key_verdict:
            print(f"Q{n}: sidecar {sidecar.get(str(n))} != key verdict {key_verdict}")
            errors += 1

    if errors:
        fail(f"{errors} structural/key errors")
    print("Structural + key + sidecar checks: PASS")

    # ---- INDEPENDENT re-solve for >= 100 questions across difficulties ----
    # Cover every question for maximum confidence (cheap enough at N=3).
    re_solved = 0
    mismatches = 0
    for n in range(1, 501):
        q = questions[n]
        cats = sorted({c for (_, a, b) in q["stmts"] for c in (a, b)}
                      | {q["concs"][0][1], q["concs"][0][2],
                         q["concs"][1][1], q["concs"][1][2]})
        v = compute_verdict(q["stmts"], q["concs"][0], q["concs"][1], cats)
        re_solved += 1
        key_verdict = TEXT_TO_VERDICT[answers[n][1]]
        if v != key_verdict:
            print(f"Q{n}: INDEPENDENT verdict {v} != key {key_verdict}")
            print(f"     stmts={q['stmts']} concs={q['concs']}")
            mismatches += 1
    print(f"Independently re-solved {re_solved} questions; {mismatches} mismatches.")
    if mismatches:
        fail(f"{mismatches} verdict mismatches between independent solver and key")

    # ---- difficulty distribution ----
    from collections import Counter
    dist = Counter(diffs.values())
    print("Difficulty distribution:", dict(dist))

    print("ALL CHECKS PASS")
    print("PASS")

if __name__ == "__main__":
    main()
