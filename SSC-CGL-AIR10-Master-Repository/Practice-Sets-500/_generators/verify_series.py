# -*- coding: utf-8 -*-
"""
Independent verifier for Reasoning_03_Series_500.md.
Re-parses the WRITTEN markdown (no shared state with the generator) and asserts:
  - exactly 500 questions and 500 answer-key entries
  - each question has 4 DISTINCT options
  - the answer-key letter (a/b/c/d) points to an option whose value matches
    the bolded answer value stated in the key
  - the keyed value matches the JSON sidecar (written == computed) for ALL 500
  - independently RE-DERIVES the rule for >=3 simple types (arithmetic,
    geometric, square-based) by fitting the VISIBLE terms and predicting the
    hidden '?' term, then checks that prediction equals the keyed answer.
Plain output: PASS / FAIL. No unicode emoji.
"""
import re
import json
import sys

MD = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_03_Series_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_03_Series_500.key.json"

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
failures = []

def fail(msg):
    failures.append(msg)

with open(MD, "r", encoding="utf-8") as f:
    text = f.read()

# Split into QUESTIONS and ANSWER sections
qmark = "# =================== QUESTIONS ==================="
amark = "# =================== ANSWER KEY & EXPLANATIONS ==================="
assert qmark in text and amark in text, "section markers missing"
q_section = text.split(qmark, 1)[1].split(amark, 1)[0]
a_section = text.split(amark, 1)[1]

# ---- parse questions ----
# **Qn.** stem  \n (a) X  (b) Y  (c) Z  (d) W
q_re = re.compile(r"\*\*Q(\d+)\.\*\*\s*(.*?)\n\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\s*\n",
                  re.DOTALL)
questions = {}
for m in q_re.finditer(q_section):
    n = int(m.group(1))
    stem = m.group(2).strip()
    opts = [m.group(3).strip(), m.group(4).strip(), m.group(5).strip(), m.group(6).strip()]
    questions[n] = {"stem": stem, "opts": opts}

# ---- parse answers ----
# **Qn. (x) VALUE**  *[DIFF]* — explanation
a_re = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*\s*\*\[(M|H|VH)\]\*\s*[-—]\s*(.*?)(?=\n\*\*Q\d+\.|\Z)",
                  re.DOTALL)
answers = {}
for m in a_re.finditer(a_section):
    n = int(m.group(1))
    letter = m.group(2)
    val = m.group(3).strip()
    diff = m.group(4)
    expl = m.group(5).strip()
    answers[n] = {"letter": letter, "val": val, "diff": diff, "expl": expl}

# ---- counts ----
if len(questions) != 500:
    fail(f"expected 500 questions, parsed {len(questions)}")
if len(answers) != 500:
    fail(f"expected 500 answers, parsed {len(answers)}")

# ---- sidecar ----
with open(SIDECAR, "r", encoding="utf-8") as f:
    sidecar = json.load(f)
if len(sidecar) != 500:
    fail(f"sidecar has {len(sidecar)} entries, expected 500")

L2I = {"a": 0, "b": 1, "c": 2, "d": 3}

# ---- per-question checks ----
diffcount = {"M": 0, "H": 0, "VH": 0}
rederive_checked = 0
rederive_ok = 0

def parse_int(s):
    try:
        return int(s)
    except ValueError:
        return None

def fit_arithmetic(vals_idx, hide_pos):
    """vals_idx: list of (position, int_value) for visible terms. Predict hidden."""
    # need at least two consecutive-known diffs; use first two visible
    pos_vals = dict(vals_idx)
    knowns = sorted(pos_vals)
    if len(knowns) < 2:
        return None
    # common difference from consecutive known terms
    diffs = []
    for i in range(len(knowns) - 1):
        gap = knowns[i+1] - knowns[i]
        diffs.append((pos_vals[knowns[i+1]] - pos_vals[knowns[i]]) / gap)
    d = diffs[0]
    if not all(abs(x - d) < 1e-9 for x in diffs):
        return None
    base_p = knowns[0]
    return pos_vals[base_p] + d * (hide_pos - base_p)

def fit_geometric(vals_idx, hide_pos):
    pos_vals = dict(vals_idx)
    knowns = sorted(pos_vals)
    if len(knowns) < 2:
        return None
    # only support consecutive positions for ratio
    ratios = []
    for i in range(len(knowns) - 1):
        if knowns[i+1] - knowns[i] != 1:
            return None
        if pos_vals[knowns[i]] == 0:
            return None
        ratios.append(pos_vals[knowns[i+1]] / pos_vals[knowns[i]])
    r = ratios[0]
    if not all(abs(x - r) < 1e-9 for x in ratios):
        return None
    base_p = knowns[0]
    return pos_vals[base_p] * (r ** (hide_pos - base_p))

def fit_square(vals_idx, hide_pos):
    """Fit terms == (n)^2 + k for consecutive n. Return predicted hidden value."""
    pos_vals = dict(vals_idx)
    knowns = sorted(pos_vals)
    if len(knowns) < 3:
        return None
    # try to find integer base n0 at position knowns[0] s.t. value = (n0+offset)^2 + k
    import math
    # guess sqrt of first value
    v0 = pos_vals[knowns[0]]
    for kk in range(-3, 4):
        base = v0 - kk
        if base < 0:
            continue
        root = round(math.isqrt(base)) if base >= 0 else -1
        for rr in (root - 1, root, root + 1):
            if rr < 1:
                continue
            # n at position knowns[0] is rr; n increments by 1 per position
            ok = True
            for p in knowns:
                n_here = rr + (p - knowns[0])
                if n_here * n_here + kk != pos_vals[p]:
                    ok = False
                    break
            if ok:
                n_hidden = rr + (hide_pos - knowns[0])
                return n_hidden * n_hidden + kk
    return None

for n in range(1, 501):
    if n not in questions:
        fail(f"Q{n} missing in questions"); continue
    if n not in answers:
        fail(f"Q{n} missing in answers"); continue
    q = questions[n]
    a = answers[n]
    # 4 distinct options
    if len(q["opts"]) != 4:
        fail(f"Q{n}: not 4 options: {q['opts']}")
    if len(set(q["opts"])) != 4:
        fail(f"Q{n}: duplicate options: {q['opts']}")
    # keyed letter points to option == stated answer value
    idx = L2I[a["letter"]]
    if idx >= len(q["opts"]):
        fail(f"Q{n}: bad letter index"); continue
    if q["opts"][idx] != a["val"]:
        fail(f"Q{n}: keyed option '{q['opts'][idx]}' != stated answer '{a['val']}'")
    # sidecar cross-check
    if sidecar.get(str(n)) != a["val"]:
        fail(f"Q{n}: sidecar '{sidecar.get(str(n))}' != written answer '{a['val']}'")
    diffcount[a["diff"]] += 1

    # ---- independent re-derivation for simple numeric types ----
    expl = a["expl"]
    stem = q["stem"]
    # extract the series terms from the stem (the part after the colon)
    if ":" in stem:
        body = stem.split(":", 1)[1]
    else:
        body = stem
    toks = [t.strip() for t in body.split(",")]
    # find hidden position
    if "?" not in toks:
        continue
    hide_pos = toks.index("?")
    # numeric series only
    parsed = []
    numeric = True
    for i, t in enumerate(toks):
        if t == "?":
            continue
        v = parse_int(t)
        if v is None:
            numeric = False
            break
        parsed.append((i, v))
    if not numeric or len(parsed) < 2:
        continue

    keyed = parse_int(a["val"])
    if keyed is None:
        continue

    pred = None
    kind = None
    if "arithmetic progression" in expl and "common difference" in expl:
        pred = fit_arithmetic(parsed, hide_pos); kind = "arith"
    elif "geometric" in expl and "Find the wrong" not in stem:
        pred = fit_geometric(parsed, hide_pos); kind = "geo"
    elif ("perfect squares" in expl) or ("n^2" in expl and "cube" not in expl):
        pred = fit_square(parsed, hide_pos); kind = "square"

    if pred is not None and kind is not None:
        rederive_checked += 1
        if abs(pred - keyed) < 1e-9:
            rederive_ok += 1
        else:
            fail(f"Q{n} [{kind}]: re-derived {pred} != keyed {keyed} (terms {toks})")

# ---- difficulty skew sanity ----
total = sum(diffcount.values())
print(f"Parsed {len(questions)} questions, {len(answers)} answers.")
print(f"Difficulty: {diffcount}  (total {total})")
if total:
    print(f"Skew: M={diffcount['M']/total*100:.0f}% H={diffcount['H']/total*100:.0f}% VH={diffcount['VH']/total*100:.0f}%")
print(f"Independent rule re-derivation: checked {rederive_checked}, matched {rederive_ok}")

if rederive_checked < 3:
    fail(f"re-derivation coverage too low ({rederive_checked}); need >=3")
if rederive_ok != rederive_checked:
    fail(f"re-derivation mismatches: {rederive_checked - rederive_ok}")

if failures:
    print(f"\n{len(failures)} FAILURE(S):")
    for f_ in failures[:40]:
        print("  -", f_)
    print("\nFAIL")
    sys.exit(1)
else:
    print("\nAll checks passed: 500 Q + 500 A, options distinct, keyed==stated==sidecar==computed, rules re-derived.")
    print("PASS")
