# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Coding-Decoding set.
Re-parse the WRITTEN markdown, confirm 500 Q + 500 A, keyed option value ==
stated answer string, 4 DISTINCT options each. Cross-check every key against
the JSON sidecar emitted by gen_coding.py (written == computed). Then, for
several recognizable rule types, INDEPENDENTLY re-derive the answer by parsing
the rule from the stem (detect shift from the example pair, apply to the asked
word, etc.) and compare. Does NOT import the generator.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
import json

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_01_Coding_Decoding_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_01_Coding_Decoding_500.key.json"

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def pos(ch):
    return ord(ch) - ord('A') + 1

def from_pos(p):
    return AZ[(p - 1) % 26]

def shift_word(word, n):
    return "".join(from_pos(pos(c) + n) for c in word)

txt = open(PATH, encoding="utf-8").read()
sidecar = json.load(open(SIDECAR, encoding="utf-8"))

qpart, apart = txt.split("# =================== ANSWER KEY")

qs = {}
qpat = re.compile(
    r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s\s+\(b\)\s*(.*?)\s\s+\(c\)\s*(.*?)\s\s+\(d\)\s*(.*?)\n",
    re.S,
)
for m in qpat.finditer(qpart):
    n = int(m.group(1))
    stem = m.group(2).replace("\n", " ").strip()
    opts = [m.group(3).strip(), m.group(4).strip(), m.group(5).strip(), m.group(6).strip()]
    qs[n] = (stem, opts)

ans = {}
apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*\s*\*\[")
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), m.group(3).strip())

print(f"Parsed {len(qs)} questions, {len(ans)} answers, sidecar has {len(sidecar)} keys")
assert len(qs) == 500, f"question count {len(qs)} != 500"
assert len(ans) == 500, f"answer count {len(ans)} != 500"
assert len(sidecar) == 500, f"sidecar count {len(sidecar)} != 500"

mismatch = 0
checked = 0
type_counts = {}

for n in range(1, 501):
    stem, opts = qs[n]
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]

    # 1) keyed option string must equal stated answer string
    if keyed_opt != aval:
        print(f"Q{n}: keyed option[{letter}]='{keyed_opt}' != stated answer '{aval}'")
        mismatch += 1
        continue
    # 2) 4 distinct options
    if len(set(opts)) != 4:
        print(f"Q{n}: options not distinct: {opts}")
        mismatch += 1
    # 3) cross-check against sidecar (written == computed)
    if sidecar[str(n)] != keyed_opt:
        print(f"Q{n}: sidecar '{sidecar[str(n)]}' != keyed '{keyed_opt}'")
        mismatch += 1

    # ----- independent re-derivation for recognizable rule types -----
    try:
        # TYPE A: simple letter-shift coding.
        # "'EX' is written as 'EXCODE'. How will 'ASK' be written ..."
        mshift = re.search(
            r"'([A-Z]+)' is written as '([A-Z]+)'.*?'([A-Z]+)' be written", stem)
        if mshift and "reverse" not in stem.lower() and "PRODUCT" not in stem \
                and "SUM" not in stem and "position" not in stem.lower() \
                and "symbol" not in stem.lower():
            ex, ex_code, ask = mshift.group(1), mshift.group(2), mshift.group(3)
            if len(ex) == len(ex_code):
                # detect a single constant shift from the example
                deltas = {(pos(b) - pos(a)) % 26 for a, b in zip(ex, ex_code)}
                if len(deltas) == 1:
                    n_shift = deltas.pop()
                    exp = shift_word(ask, n_shift)
                    if aval != exp:
                        print(f"Q{n} LETTER-SHIFT: got '{aval}', expected '{exp}'")
                        mismatch += 1
                    checked += 1
                    type_counts["letter_shift"] = type_counts.get("letter_shift", 0) + 1
                    continue

        # TYPE B: opposite-letter coding (detected via solution-independent re-derive
        # from the example: each pos -> 27-pos).
        mopp = re.search(
            r"'([A-Z]+)' is coded as '([A-Z]+)'.*?'([A-Z]+)' coded", stem)
        if mopp:
            ex, ex_code, ask = mopp.group(1), mopp.group(2), mopp.group(3)
            if len(ex) == len(ex_code) and \
               all(pos(b) == 27 - pos(a) for a, b in zip(ex, ex_code)):
                exp = "".join(from_pos(27 - pos(c)) for c in ask)
                if aval != exp:
                    print(f"Q{n} OPPOSITE: got '{aval}', expected '{exp}'")
                    mismatch += 1
                checked += 1
                type_counts["opposite"] = type_counts.get("opposite", 0) + 1
                continue

        # TYPE C: word -> SUM of alphabet positions.
        msum = re.search(r"SUM of these values.*?'([A-Z]+)' is coded as (\d+).*?"
                         r"code for '([A-Z]+)'", stem)
        if msum:
            ex, ex_val, ask = msum.group(1), int(msum.group(2)), msum.group(3)
            # confirm example is consistent, then derive
            if sum(pos(c) for c in ex) == ex_val:
                exp = str(sum(pos(c) for c in ask))
                if aval != exp:
                    print(f"Q{n} WORD-SUM: got '{aval}', expected '{exp}'")
                    mismatch += 1
                checked += 1
                type_counts["word_sum"] = type_counts.get("word_sum", 0) + 1
                continue

        # TYPE D: number coding - reverse the digits.
        mrev = re.search(r"number (\d+) is written as (\d+).*?How is (\d+) written", stem)
        if mrev:
            ex, ex_code, ask = mrev.group(1), mrev.group(2), int(mrev.group(3))
            if int(ex[::-1]) == int(ex_code):
                exp = str(int(str(ask)[::-1]))
                if aval != exp:
                    print(f"Q{n} NUM-REVERSE: got '{aval}', expected '{exp}'")
                    mismatch += 1
                checked += 1
                type_counts["num_reverse"] = type_counts.get("num_reverse", 0) + 1
                continue

        # TYPE E: number coding - fixed arithmetic, given TWO example pairs that
        # uniquely determine whether the rule is additive (+k) or multiplicative (*k).
        marith = re.search(
            r"If (\d+) is coded as (\d+) and (\d+) is coded as (\d+).*?"
            r"then (\d+) will be coded", stem)
        if marith:
            e1a, e1b, e2a, e2b, ask = (int(marith.group(i)) for i in range(1, 6))
            exp = None
            # additive: same difference in both examples
            if (e1b - e1a) == (e2b - e2a):
                exp = str(ask + (e1b - e1a))
            # multiplicative: same ratio in both examples (takes precedence only
            # if additive doesn't also hold; with distinct numbers exactly one holds)
            elif e1a != 0 and e2a != 0 and e1b % e1a == 0 and e2b % e2a == 0 \
                    and (e1b // e1a) == (e2b // e2a):
                exp = str(ask * (e1b // e1a))
            if exp is not None:
                if aval != exp:
                    print(f"Q{n} NUM-ARITH: got '{aval}', expected '{exp}'")
                    mismatch += 1
                checked += 1
                type_counts["num_arith"] = type_counts.get("num_arith", 0) + 1
                continue

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-derived {checked} questions by parsing the rule from the stem.")
print("Re-derived type breakdown:", type_counts)
print(f"Distinct rule types independently verified: {len(type_counts)}")
assert len(type_counts) >= 3, "Fewer than 3 rule types independently re-derived!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
assert mismatch == 0, "verification FAILED"
