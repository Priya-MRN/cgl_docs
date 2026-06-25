# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Non-Verbal Reasoning set.

Re-parses the WRITTEN markdown (does NOT import the generator), confirms
500 Q + 500 A, that each keyed option value == the stated answer string, that
every question has 4 DISTINCT options, and cross-checks every key against the
JSON sidecar. Then it INDEPENDENTLY re-computes the answer for several
recognizable computable types directly from the stem text:

   * mirror_string  : reverse the quoted string -> expected answer.
   * dice (pair)    : two opposite pairs stated -> the third pair is forced.
   * paper folding  : f folds, p punches -> p * 2^f holes.
   * counting       : squares-in-grid (sum k^2), rectangles (C*C),
                      base-split-into-s fan (s(s+1)/2), triangle subdivision.
   * water_string   : water image of horizontally-symmetric glyphs = same string.
   * series_shift   : detect constant shift, extend the series.
   * embedded_count : count contiguous (overlapping) occurrences.

NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
import json
from math import comb

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_10_NonVerbal_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_10_NonVerbal_500.key.json"

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

# Questions: stems may span multiple lines (we wrote "  \n" line breaks inside
# stems). Capture everything from "**Qn.**" up to the "(a) ... (d) ..." line.
qs = {}
qpat = re.compile(
    r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s\s+\(b\)\s*(.*?)\s\s+\(c\)\s*(.*?)\s\s+\(d\)\s*(.*?)\n",
    re.S,
)
for m in qpat.finditer(qpart):
    n = int(m.group(1))
    stem = re.sub(r"\s+", " ", m.group(2)).strip()
    opts = [m.group(3).strip(), m.group(4).strip(),
            m.group(5).strip(), m.group(6).strip()]
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

def tick(name):
    type_counts[name] = type_counts.get(name, 0) + 1

for n in range(1, 501):
    stem, opts = qs[n]
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]

    # 1) keyed option string == stated answer string
    if keyed_opt != aval:
        print(f"Q{n}: keyed option[{letter}]='{keyed_opt}' != stated answer '{aval}'")
        mismatch += 1
        continue
    # 2) 4 distinct options
    if len(set(opts)) != 4:
        print(f"Q{n}: options not distinct: {opts}")
        mismatch += 1
    # 3) cross-check sidecar
    if sidecar[str(n)] != keyed_opt:
        print(f"Q{n}: sidecar '{sidecar[str(n)]}' != keyed '{keyed_opt}'")
        mismatch += 1

    # ----- independent re-derivation -----
    try:
        # MIRROR STRING: "...MIRROR IMAGE ... of the string 'XXXX'?"
        mm = re.search(r"MIRROR IMAGE.*?of the string '([A-Z0-9]+)'", stem)
        if mm:
            s = mm.group(1)
            exp = s[::-1]
            if aval != exp:
                print(f"Q{n} MIRROR: got '{aval}', expected '{exp}'"); mismatch += 1
            checked += 1; tick("mirror_string"); continue

        # DICE PAIR: "the face A is opposite the face B, and the face C is
        #             opposite the face D. ... OPPOSITE to the face numbered Q?"
        md = re.search(
            r"the face (\d+) is opposite the face (\d+), and the face (\d+) is "
            r"opposite the face (\d+).*?OPPOSITE to the face numbered (\d+)", stem)
        if md:
            a, b, c, d, q = (int(md.group(i)) for i in range(1, 6))
            used = {a, b, c, d}
            rest = [x for x in range(1, 7) if x not in used]  # the third pair
            # q is one of the remaining two; its opposite is the other
            if q in rest and len(rest) == 2:
                exp = str(rest[1] if rest[0] == q else rest[0])
                if aval != exp:
                    print(f"Q{n} DICE-PAIR: got '{aval}', expected '{exp}'"); mismatch += 1
                checked += 1; tick("dice_pair"); continue

        # DICE TWO-VIEW: deduce opposite of q as the unique face never shown
        #   sharing a corner with q across the two views.
        mdv = re.search(
            r"faces with numbers (\d+) \(top\), (\d+) \(front\) and (\d+) "
            r"\(right\) meet at a corner\. In the second position the faces "
            r"(\d+) \(top\), (\d+) \(front\) and (\d+) \(right\).*?"
            r"OPPOSITE to the face numbered (\d+)", stem)
        if mdv:
            v1 = set(map(int, mdv.group(1, 2, 3)))
            v2 = set(map(int, mdv.group(4, 5, 6)))
            q = int(mdv.group(7))
            shown = set()
            for v in (v1, v2):
                if q in v:
                    shown |= (v - {q})
            remaining = set(range(1, 7)) - {q} - shown
            if len(remaining) == 1:       # must be uniquely deducible
                exp = str(next(iter(remaining)))
                if aval != exp:
                    print(f"Q{n} DICE-VIEW: got '{aval}', expected '{exp}'"); mismatch += 1
                checked += 1; tick("dice_opposite"); continue
            else:
                print(f"Q{n} DICE-VIEW: not uniquely deducible {remaining}"); mismatch += 1

        # PAPER PUNCH (general): "folded in half F time(s) ... P hole(s) through
        #   ALL the layers ... how many holes"
        mp = re.search(
            r"folded in half (\d+) time\(s\).*?makes (\d+) hole\(s\) through ALL",
            stem)
        if mp:
            f, p = int(mp.group(1)), int(mp.group(2))
            exp = str(p * (2 ** f))
            if aval != exp:
                print(f"Q{n} PAPER-PUNCH: got '{aval}', expected '{exp}'"); mismatch += 1
            checked += 1; tick("paper_punch"); continue

        # PAPER SIMPLE: "folded straight in half F time(s) ... One hole ...
        #   how many holes"
        mps = re.search(
            r"folded straight in half (\d+) time\(s\).*?One hole is punched", stem)
        if mps:
            f = int(mps.group(1))
            exp = str(2 ** f)
            if aval != exp:
                print(f"Q{n} PAPER-SIMPLE: got '{aval}', expected '{exp}'"); mismatch += 1
            checked += 1; tick("paper_simple"); continue

        # COUNT SQUARES: "N x N grid ... squares of ALL sizes ... how many squares"
        msq = re.search(
            r"into a (\d+) x (\d+) grid.*?squares of ALL sizes.*?how many squares",
            stem)
        if msq:
            a, b = int(msq.group(1)), int(msq.group(2))
            if a == b:
                exp = str(sum(k * k for k in range(1, a + 1)))
                if aval != exp:
                    print(f"Q{n} COUNT-SQ: got '{aval}', expected '{exp}'"); mismatch += 1
                checked += 1; tick("count_squares"); continue

        # COUNT RECTANGLES: "M x N grid ... how many rectangles"
        mrc = re.search(
            r"into an (\d+) x (\d+) grid.*?how many rectangles", stem, re.I)
        if mrc:
            a, b = int(mrc.group(1)), int(mrc.group(2))
            exp = str(comb(a + 1, 2) * comb(b + 1, 2))
            if aval != exp:
                print(f"Q{n} COUNT-RECT: got '{aval}', expected '{exp}'"); mismatch += 1
            checked += 1; tick("count_rectangles"); continue

        # COUNT FAN: "base BC is divided into S equal parts ... how many triangles"
        mfan = re.search(
            r"base BC is divided into (\d+) equal parts.*?how many triangles", stem, re.I)
        if mfan:
            s = int(mfan.group(1))
            exp = str(s * (s + 1) // 2)
            if aval != exp:
                print(f"Q{n} COUNT-FAN: got '{aval}', expected '{exp}'"); mismatch += 1
            checked += 1; tick("count_fan"); continue

        # COUNT TRIANGLES (subdivision): "divided ... into N rows of small ...
        #   how many triangles"
        mtr = re.search(
            r"parallel to its three sides into (\d+) rows of small.*?how many triangles",
            stem)
        if mtr:
            nn = int(mtr.group(1))
            base = nn * (nn + 2) * (2 * nn + 1)
            exp = str(base // 8 if nn % 2 == 0 else (base - 1) // 8)
            if aval != exp:
                print(f"Q{n} COUNT-TRI: got '{aval}', expected '{exp}'"); mismatch += 1
            checked += 1; tick("count_triangles"); continue

        # WATER STRING: "WATER IMAGE ... of 'XXXX'?" -> unchanged
        mw = re.search(r"WATER IMAGE.*?of '([A-Z0-9]+)'", stem)
        if mw:
            s = mw.group(1)
            WATER = set("BCDEHIKOX0138")
            if all(ch in WATER for ch in s):
                exp = s
                if aval != exp:
                    print(f"Q{n} WATER: got '{aval}', expected '{exp}'"); mismatch += 1
                checked += 1; tick("water_string"); continue

        # SERIES SHIFT: "Series: T1, T2, T3, T4, ?" with constant alphabet shift
        mss = re.search(r"shifting every letter the SAME fixed number.*?"
                        r"Series:\s*([A-Z, ]+?),\s*\?", stem)
        if mss:
            terms = [t.strip() for t in mss.group(1).split(",") if t.strip()]
            if len(terms) >= 2 and len({len(t) for t in terms}) == 1:
                # detect shift between consecutive terms
                def delta(a, b):
                    ds = {(pos(y) - pos(x)) % 26 for x, y in zip(a, b)}
                    return ds.pop() if len(ds) == 1 else None
                deltas = [delta(terms[i], terms[i + 1]) for i in range(len(terms) - 1)]
                if deltas and all(d is not None for d in deltas) and len(set(deltas)) == 1:
                    k = deltas[0]
                    exp = shift_word(terms[-1], k)
                    if aval != exp:
                        print(f"Q{n} SERIES-SHIFT: got '{aval}', expected '{exp}'"); mismatch += 1
                    checked += 1; tick("series_shift"); continue

        # EMBEDDED COUNT: "string of symbols 'BODY', how many times does ...
        #   'PAT' appear ... as a CONTIGUOUS block"
        mec = re.search(
            r"linear string of symbols '([A-Z]+)', how many times does the "
            r"smaller pattern '([A-Z]+)' appear", stem)
        if mec:
            body, pat = mec.group(1), mec.group(2)
            cnt = sum(1 for i in range(len(body) - len(pat) + 1)
                      if body[i:i + len(pat)] == pat)
            exp = str(cnt)
            if aval != exp:
                print(f"Q{n} EMBED-COUNT: got '{aval}', expected '{exp}'"); mismatch += 1
            checked += 1; tick("embedded_count"); continue

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")

print(f"Independently re-derived {checked} questions by parsing the stem.")
print("Re-derived type breakdown:", type_counts)
print(f"Distinct computable types independently verified: {len(type_counts)}")
assert checked >= 100, f"only {checked} re-derived (<100 required)"
assert len(type_counts) >= 3, "fewer than 3 types independently re-derived!"
print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
assert mismatch == 0, "verification FAILED"
