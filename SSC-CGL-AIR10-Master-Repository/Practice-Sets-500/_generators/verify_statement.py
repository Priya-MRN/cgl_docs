# -*- coding: utf-8 -*-
r"""
Independent verifier for the Statement & Conclusion / Assumption / Inference /
Cause-Effect / Course-of-Action 500 set.

Re-parses the WRITTEN markdown (no shared state with the generator), then:
  1. asserts 500 questions and 500 answers,
  2. checks every question's options are distinct and the keyed letter's text
     equals the stated answer text,
  3. checks the keyed answer text is one of the legal standard option-sets for
     that sub-type and that EXACTLY ONE keyed option is present,
  4. for the FAMILY A (Statement & Conclusion) subset, re-runs an INDEPENDENT
     model-checker on the parsed statements + conclusions and confirms the
     computed verdict matches both the key and the JSON sidecar,
  5. confirms the sidecar covers exactly the computable subset.

Emits plain PASS/FAIL only (no unicode emoji).
"""
import re
import json
import sys
from itertools import product, combinations
from collections import Counter

MD = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_09_Statement_Conclusion_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_09_Statement_Conclusion_500.verdicts.json"

def fail(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# INDEPENDENT model checker (re-implemented from scratch)
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
    return {k1, k2} in ({"some", "somenot"}, {"all", "somenot"}, {"no", "some"})

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
            if not (holds(c1[0], c1[1], c1[2], asg) or holds(c2[0], c2[1], c2[2], asg)):
                either = False
                break
    if any_model and either and complementary(c1, c2):
        return "EITHER"
    return "NEITHER"

# ---------------------------------------------------------------------------
# parse statements back to (kind, A, B)
# ---------------------------------------------------------------------------
RE_ALL = re.compile(r"^All (.+?) are (.+?)\.$")
RE_NO = re.compile(r"^No (.+?) are (.+?)\.$")
RE_SOMENOT = re.compile(r"^Some (.+?) are not (.+?)\.$")
RE_SOME = re.compile(r"^Some (.+?) are (.+?)\.$")

def parse_stmt(s):
    s = s.strip()
    for rx, kind, gi in ((RE_SOMENOT, "somenot", 1), (RE_ALL, "all", 1),
                         (RE_NO, "no", 1), (RE_SOME, "some", 1)):
        m = rx.match(s)
        if m:
            return (kind, m.group(1), m.group(2))
    raise ValueError(f"cannot parse statement: {s!r}")

def split_sentences(text):
    return [p.strip() for p in re.findall(r"[^.]*\.", text) if p.strip()]

# legal answer texts per sub-type
CONC_TEXT_TO_VERDICT = {
    "Only conclusion I follows": "I",
    "Only conclusion II follows": "II",
    "Both conclusions I and II follow": "BOTH",
    "Neither conclusion I nor conclusion II follows": "NEITHER",
    "Either conclusion I or conclusion II follows": "EITHER",
}
ASSUM_SET = {"Only assumption I is implicit", "Only assumption II is implicit",
             "Both I and II are implicit", "Neither I nor II is implicit"}
INFER_SET = {"Definitely true", "Definitely false",
             "Cannot be determined from the statement",
             "Probably true but not certain"}
COA_SET = {"Only course of action I follows", "Only course of action II follows",
           "Both I and II follow", "Neither I nor II follows"}
CE_SET = {"Statement I is the cause and statement II is its effect",
          "Statement II is the cause and statement I is its effect",
          "Both statements are independent causes",
          "Both statements are effects of a common cause"}
ALL_LEGAL = set(CONC_TEXT_TO_VERDICT) | ASSUM_SET | INFER_SET | COA_SET | CE_SET

def main():
    with open(MD, encoding="utf-8") as f:
        text = f.read()

    # ---- isolate the QUESTIONS section vs the ANSWER section ----
    marker = "# =================== ANSWER KEY & EXPLANATIONS ==================="
    if marker not in text:
        fail("answer-key marker not found")
    q_section, a_section = text.split(marker, 1)

    # ---- parse questions ----
    # A question block starts at '**Qn.**' and runs until the next '**Qn'
    # marker or end of the questions section. The option line is the LAST
    # non-empty line of the block beginning with '(a)'.
    q_blocks = re.split(r"(?=^\*\*Q\d+\.\*\*)", q_section, flags=re.M)
    questions = {}
    for blk in q_blocks:
        m = re.match(r"\*\*Q(\d+)\.\*\*", blk)
        if not m:
            continue
        n = int(m.group(1))
        lines = [ln for ln in blk.splitlines() if ln.strip()]
        # find option line
        opt_lines = [ln for ln in lines if re.match(r"^\([a-e]\)", ln.strip())]
        if not opt_lines:
            fail(f"Q{n}: no option line")
        opt_line = opt_lines[-1].strip()
        opts = dict(re.findall(r"\(([a-e])\)\s*(.+?)(?=\s*\([a-e]\)|\s*$)", opt_line))
        opts = {k: v.strip() for k, v in opts.items()}
        # determine sub-type and (for Family A) the statements/conclusions
        is_conc = "Statement & Conclusion" in blk
        rec = {"opts": opts, "is_conc": is_conc, "block": blk}
        if is_conc:
            sm = re.search(r"Statements:\s*(.+)", blk)
            cm = re.search(r"Conclusions:\s*I\.\s*(.+?)\s*II\.\s*(.+)", blk)
            if not sm or not cm:
                fail(f"Q{n}: cannot parse conclusion-item statements/conclusions")
            stmts = [parse_stmt(s) for s in split_sentences(sm.group(1).strip())]
            c1 = parse_stmt(cm.group(1).strip())
            c2 = parse_stmt(cm.group(2).strip())
            rec["stmts"] = stmts
            rec["concs"] = [c1, c2]
        questions[n] = rec

    nq = len(questions)
    print(f"Parsed {nq} questions.")
    if nq != 500:
        fail(f"expected 500 questions, got {nq}")

    # ---- parse answers ----
    a_re = re.compile(r"\*\*Q(\d+)\.\s*\(([a-e])\)\s*(.+?)\*\*\s*\*\[(M|H|VH)\]\*")
    answers, diffs = {}, {}
    for m in a_re.finditer(a_section):
        n = int(m.group(1))
        answers[n] = (m.group(2), m.group(3).strip())
        diffs[n] = m.group(4)
    na = len(answers)
    print(f"Parsed {na} answers.")
    if na != 500:
        fail(f"expected 500 answers, got {na}")

    # ---- sidecar ----
    with open(SIDECAR, encoding="utf-8") as f:
        sidecar = json.load(f)
    print(f"Sidecar entries: {len(sidecar)}")

    # ---- per-question structural + key checks ----
    errors = 0
    conc_nums = []
    for n in range(1, 501):
        if n not in questions:
            fail(f"missing question {n}")
        if n not in answers:
            fail(f"missing answer {n}")
        q = questions[n]
        letter, atext = answers[n]
        opts = q["opts"]
        vals = list(opts.values())
        if len(set(vals)) != len(vals):
            print(f"Q{n}: duplicate option text {vals}"); errors += 1
        if letter not in opts:
            print(f"Q{n}: answer letter {letter} not among options {list(opts)}"); errors += 1
            continue
        if opts[letter] != atext:
            print(f"Q{n}: keyed text {opts[letter]!r} != answer text {atext!r}"); errors += 1
        if atext not in ALL_LEGAL:
            print(f"Q{n}: answer text not a standard option: {atext!r}"); errors += 1
            continue
        # EXACTLY ONE keyed option present: the answer text must appear once in opts
        if vals.count(atext) != 1:
            print(f"Q{n}: keyed option not uniquely present"); errors += 1
        # sub-type consistency: all options belong to the same legal set
        if q["is_conc"]:
            conc_nums.append(n)
            if not all(v in CONC_TEXT_TO_VERDICT for v in vals):
                print(f"Q{n}: conclusion item has non-conclusion options"); errors += 1
            if atext not in CONC_TEXT_TO_VERDICT:
                print(f"Q{n}: conclusion item keyed to non-conclusion text"); errors += 1
        else:
            # curated: options must all fall in exactly one curated set
            sets_hit = [s for s in (ASSUM_SET, INFER_SET, COA_SET, CE_SET)
                        if all(v in s for v in vals)]
            if len(sets_hit) != 1:
                print(f"Q{n}: curated item options not from one clean set: {vals}"); errors += 1

    if errors:
        fail(f"{errors} structural/key errors")
    print("Structural + key checks: PASS")

    # ---- sidecar must cover exactly the conclusion (Family A) subset ----
    sidecar_keys = set(int(k) for k in sidecar)
    if sidecar_keys != set(conc_nums):
        missing = set(conc_nums) - sidecar_keys
        extra = sidecar_keys - set(conc_nums)
        fail(f"sidecar coverage mismatch; missing={sorted(missing)[:5]} extra={sorted(extra)[:5]}")
    print(f"Sidecar covers exactly the {len(conc_nums)} computable items: PASS")

    # ---- INDEPENDENT re-solve of every Family A item ----
    mism = 0
    for n in conc_nums:
        q = questions[n]
        cats = sorted({c for (_, a, b) in q["stmts"] for c in (a, b)}
                      | {q["concs"][0][1], q["concs"][0][2],
                         q["concs"][1][1], q["concs"][1][2]})
        v = compute_verdict(q["stmts"], q["concs"][0], q["concs"][1], cats)
        key_v = CONC_TEXT_TO_VERDICT[answers[n][1]]
        side_v = sidecar.get(str(n))
        if v != key_v:
            print(f"Q{n}: independent verdict {v} != key {key_v}")
            print(f"     stmts={q['stmts']} concs={q['concs']}")
            mism += 1
        if side_v != key_v:
            print(f"Q{n}: sidecar {side_v} != key {key_v}"); mism += 1
    print(f"Independently re-solved {len(conc_nums)} computable items; {mism} mismatches.")
    if mism:
        fail(f"{mism} verdict mismatches")

    # ---- difficulty distribution ----
    dist = Counter(diffs.values())
    total = sum(dist.values())
    print("Difficulty distribution:", dict(dist),
          f"(M={dist['M']/total:.0%} H={dist['H']/total:.0%} VH={dist['VH']/total:.0%})")
    curated_count = 500 - len(conc_nums)
    print(f"Computable (Family A): {len(conc_nums)}  |  Curated (Family B): {curated_count}")

    print("ALL CHECKS PASS")
    print("PASS")

if __name__ == "__main__":
    main()
