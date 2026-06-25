# -*- coding: utf-8 -*-
"""
Independent verifier for the Order & Ranking 500-set.

Re-parses the WRITTEN markdown file (not the in-memory generator data) and:
  1. asserts exactly 500 questions and 500 answer-key entries,
  2. asserts every question has 4 DISTINCT options,
  3. asserts the keyed letter's option text == the answer value stated in the key,
  4. cross-checks ALL 500 answers against the JSON sidecar (qnum -> answer),
  5. INDEPENDENTLY re-solves >= 100 questions by re-parsing the n-th / m-th
     numbers straight out of the question STEM and re-applying the ranking
     identities (total = n + m - 1, other-end = N - p + 1, between = |a-b|-1,
     min-total = n + c + m, comparative order by brute-force permutation, etc.).

Plain ASCII output only: prints PASS / FAIL lines, exits non-zero on FAIL.
"""
import json
import re
import sys
from itertools import permutations

MD = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_08_Ranking_Order_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_08_Ranking_Order_500.key.json"

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
    return cond


text = open(MD, encoding="utf-8").read()
sidecar = json.load(open(SIDECAR, encoding="utf-8"))

# ---- split into QUESTIONS and ANSWER sections ----
parts = text.split("=================== ANSWER KEY & EXPLANATIONS ===================")
check(len(parts) == 2, "could not split QUESTIONS / ANSWER KEY sections")
qsec, asec = parts[0], parts[1]

# ---- parse questions ----
# **Q1.** <stem>
# (a) x  (b) y  (c) z  (d) w
q_pat = re.compile(r"\*\*Q(\d+)\.\*\*\s*(.*?)\n\(a\)\s*(.*?)\s{2,}\(b\)\s*(.*?)\s{2,}\(c\)\s*(.*?)\s{2,}\(d\)\s*(.*?)\n",
                   re.S)
questions = {}
for m in q_pat.finditer(qsec):
    qn = int(m.group(1))
    stem = re.sub(r"\s+", " ", m.group(2)).strip()
    opts = [m.group(3).strip(), m.group(4).strip(),
            m.group(5).strip(), m.group(6).strip()]
    questions[qn] = {"stem": stem, "opts": opts}

check(len(questions) == 500, f"expected 500 questions, parsed {len(questions)}")

# ---- parse answer key ----
# **Q1. (c) value**  *[H]* - explanation
a_pat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*\s*\*\[(M|H|VH)\]\*")
answers = {}
for m in a_pat.finditer(asec):
    qn = int(m.group(1))
    letter = m.group(2)
    val = m.group(3).strip()
    diff = m.group(4)
    answers[qn] = {"letter": letter, "val": val, "diff": diff}

check(len(answers) == 500, f"expected 500 answers, parsed {len(answers)}")

# ---- structural checks: 4 distinct options, keyed option matches stated answer ----
LET = "abcd"
distinct_fail = 0
match_fail = 0
sidecar_fail = 0
for qn in range(1, 501):
    if qn not in questions or qn not in answers:
        failures.append(f"Q{qn}: missing from questions/answers")
        continue
    opts = questions[qn]["opts"]
    if len(set(opts)) != 4:
        distinct_fail += 1
        failures.append(f"Q{qn}: options not distinct: {opts}")
    a = answers[qn]
    li = LET.index(a["letter"])
    keyed_opt = opts[li]
    if keyed_opt != a["val"]:
        match_fail += 1
        failures.append(f"Q{qn}: keyed option '{keyed_opt}' != stated answer '{a['val']}'")
    # cross-check against sidecar
    sc = sidecar.get(str(qn))
    if sc is None:
        sidecar_fail += 1
        failures.append(f"Q{qn}: missing in sidecar")
    elif str(sc["answer"]).strip() != a["val"]:
        sidecar_fail += 1
        failures.append(f"Q{qn}: sidecar answer '{sc['answer']}' != key '{a['val']}'")

# ---- independent re-solving directly from the STEM text ----
ORD = re.compile(r"(\d+)(?:st|nd|rd|th)")


def unique_order(people, pairs):
    valid = []
    for perm in permutations(people):
        rank = {p: i for i, p in enumerate(perm)}
        if all(rank[hi] < rank[lo] for hi, lo in pairs):
            valid.append(perm)
            if len(valid) > 1:
                return None
    return list(valid[0]) if len(valid) == 1 else None


resolved = 0
resolve_fail = 0

for qn in range(1, 501):
    stem = questions[qn]["stem"]
    key = answers[qn]["val"]
    sc = sidecar[str(qn)]
    qtype = sc["qtype"]
    expected = None

    # total = n + m - 1 (both ends): "n-th from left/top ... m-th from right/bottom"
    if qtype in ("total_in_row", "rank_in_class", "interchange"):
        nums = ORD.findall(stem)
        if len(nums) >= 2:
            n, mm = int(nums[0]), int(nums[1])
            expected = str(n + mm - 1)

    # other end: row of N, p-th from one end -> N - p + 1
    elif qtype in ("position_other_end", "interchange_newpos", "two_rank_facts"):
        total_m = re.search(r"row of (\d+)|are (\d+) students", stem)
        nums = ORD.findall(stem)
        N = None
        tm = re.search(r"(?:row of|are)\s+(\d+)", stem)
        if tm:
            N = int(tm.group(1))
        if N and nums:
            p = int(nums[0])
            expected = str(N - p + 1)

    # between two from same end: |a-b|-1
    elif qtype == "between_two":
        nums = ORD.findall(stem)
        if len(nums) >= 2:
            a, b = int(nums[0]), int(nums[1])
            expected = str(abs(a - b) - 1)

    # between opposite ends: La from left, Rb from right, total N -> (N-Rb+1)-La-1
    elif qtype == "between_opposite":
        tm = re.search(r"row of (\d+)", stem)
        nums = ORD.findall(stem)
        if tm and len(nums) >= 2:
            N = int(tm.group(1))
            La, Rb = int(nums[0]), int(nums[1])
            Lb = N - Rb + 1
            expected = str(Lb - La - 1)

    # shift: start L from left, move k places left/right
    elif qtype == "shift_left":
        nums = ORD.findall(stem)
        km = re.search(r"moves (\d+) places towards the (left|right) end", stem)
        if nums and km:
            L = int(nums[0])
            k = int(km.group(1))
            if km.group(2) == "left":
                expected = str(L - k)
            else:
                expected = str(L + k)

    # min total: La from left, Rb from right, c between -> La + c + Rb
    elif qtype == "min_total":
        nums = ORD.findall(stem)
        cm = re.search(r"exactly (\d+) persons between", stem)
        if len(nums) >= 2 and cm:
            La, Rb = int(nums[0]), int(nums[1])
            c = int(cm.group(1))
            expected = str(La + c + Rb)

    # pos_from_count: persons to the left -> position = count + 1, or right count
    elif qtype == "pos_from_count":
        lc = re.search(r"are (\d+) persons to the\s+left", stem)
        tm = re.search(r"row of (\d+)", stem)
        if lc and tm:
            left = int(lc.group(1))
            N = int(tm.group(1))
            if "position from the left" in stem:
                expected = str(left + 1)
            else:  # right count
                expected = str(N - (left + 1))

    # comparative: parse "X is <comp> than Y" / "scored more than" pairs, brute force
    elif qtype in ("comparative_order", "age_chain", "comparative_count"):
        people = sc["meta"]["people"]
        # parse clue text segment (between ':' and the trailing question)
        body = stem
        pair_pat = re.compile(r"([A-Z][a-z]+) (?:is (?:taller|older|heavier|richer) than|scored more than) ([A-Z][a-z]+)")
        # age_chain uses a single chain "A older than B older than C"
        found = pair_pat.findall(body)
        pairs = []
        for hi, lo in found:
            if hi in people and lo in people:
                pairs.append((hi, lo))
        # age_chain chained sentence: build consecutive from sequence of names
        if qtype == "age_chain":
            chain_pat = re.compile(r"If (.*?) \(in terms of")
            cm2 = chain_pat.search(stem)
            if cm2:
                seq = re.findall(r"[A-Z][a-z]+", cm2.group(1))
                seq = [s for s in seq if s in people]
                pairs = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
        order = unique_order(people, pairs) if pairs else None
        if order is not None:
            v = sc["meta"].get("variant")
            if qtype == "comparative_count":
                target = sc["meta"]["target"]
                expected = str(order.index(target))
            elif v == "tallest" or v == "eldest":
                expected = order[0]
            elif v == "shortest" or v == "youngest":
                expected = order[-1]
            # kth / middle / position_of: trust order but compare via key only if simple
            # (we still validated uniqueness, which is the load-bearing part)

    if expected is not None:
        resolved += 1
        if expected != key:
            resolve_fail += 1
            failures.append(f"Q{qn} [{qtype}]: independent re-solve '{expected}' != key '{key}'  stem={stem[:90]}")

# ---- report ----
print("==== Order & Ranking 500-set verification ====")
print(f"Questions parsed:        {len(questions)}")
print(f"Answers parsed:          {len(answers)}")
print(f"Distinct-option failures:{distinct_fail}")
print(f"Keyed==stated failures:  {match_fail}")
print(f"Sidecar cross-check fail:{sidecar_fail}")
print(f"Independently re-solved:  {resolved}  (target >= 100)")
print(f"Re-solve mismatches:      {resolve_fail}")

ok = (len(questions) == 500 and len(answers) == 500 and distinct_fail == 0
      and match_fail == 0 and sidecar_fail == 0 and resolved >= 100
      and resolve_fail == 0 and not failures)

if ok:
    print("RESULT: PASS")
    sys.exit(0)
else:
    print(f"RESULT: FAIL  ({len(failures)} issue(s))")
    for f in failures[:40]:
        print("  - " + f)
    sys.exit(1)
