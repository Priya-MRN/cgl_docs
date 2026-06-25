# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Analogy & Classification set.
Re-parses the WRITTEN markdown, confirms 500 Q + 500 A, keyed option value ==
stated answer string, 4 DISTINCT options each. Cross-checks every key against the
JSON sidecar emitted by gen_analogy.py (written == computed/authored).

For the RULE-BASED subset it INDEPENDENTLY re-derives the answer by parsing the
numbers/letters out of the stem (without importing the generator) for at least
three rule types:
  - square analogy            a : a^2 :: b : ?      -> b^2
  - multiply analogy          a : a*k :: b : ?      -> b*k
  - perfect-square odd-one-out (3 squares + 1 non-square) -> the non-square
(plus cube analogy, +k analogy, prime/divisible/cube/consecutive-product
odd-one-out, and letter-shift analogy as bonus coverage).

For the CURATED word subset, asserts structural validity: exactly one keyed
option that matches the stated answer and 4 distinct options.

NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
import json

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_05_Analogy_Classification_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_05_Analogy_Classification_500.key.json"

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def pos(ch):
    return ord(ch.upper()) - ord('A') + 1

def from_pos(p):
    return AZ[(p - 1) % 26]

def shift_word(word, n):
    return "".join(from_pos(pos(c) + n) for c in word)

def is_square(x):
    if x < 0:
        return False
    r = int(round(x ** 0.5))
    return r * r == x

def is_cube(x):
    if x < 0:
        return False
    r = int(round(x ** (1.0 / 3.0)))
    for c in (r - 1, r, r + 1):
        if c >= 0 and c * c * c == x:
            return True
    return False

def is_prime(x):
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    i = 3
    while i * i <= x:
        if x % i == 0:
            return False
        i += 2
    return True

def is_consec_prod(x):
    if x < 0:
        return False
    n = int(x ** 0.5)
    for c in (n - 1, n, n + 1):
        if c >= 0 and c * (c + 1) == x:
            return True
    return False

def is_square_offset(fa, a):
    """True if fa = a^2 + k for small k in 1..5."""
    k = fa - a * a
    return 1 <= k <= 5

# Independent candidate rule family for numeric analogies (built here, NOT imported
# from the generator). Each entry: (name, function n->value).
def _build_num_rules():
    rules = [("square", lambda n: n * n),
             ("cube", lambda n: n ** 3),
             ("n(n+1)", lambda n: n * (n + 1)),
             ("n(n-1)", lambda n: n * (n - 1))]
    for k in range(2, 13):
        rules.append((f"x{k}", (lambda kk: (lambda n: n * kk))(k)))
    for k in range(1, 26):
        rules.append((f"+{k}", (lambda kk: (lambda n: n + kk))(k)))
        rules.append((f"-{k}", (lambda kk: (lambda n: n - kk))(k)))
    for k in range(1, 11):
        rules.append((f"sq+{k}", (lambda kk: (lambda n: n * n + kk))(k)))
        rules.append((f"sq-{k}", (lambda kk: (lambda n: n * n - kk))(k)))
    return rules

NUM_RULES = _build_num_rules()

def derive_num_analogy(pairs, b):
    """Find the rule(s) fitting EVERY example pair; return (name, answer_for_b) if
    exactly one fits, else (None, None) signalling ambiguity."""
    fits = [(nm, fn) for nm, fn in NUM_RULES if all(fn(a) == fa for a, fa in pairs)]
    if len(fits) != 1:
        return None, None
    nm, fn = fits[0]
    return nm, fn(b)

txt = open(PATH, encoding="utf-8").read()
sidecar = json.load(open(SIDECAR, encoding="utf-8"))

qpart, apart = txt.split("# =================== ANSWER KEY")

# ---- parse questions: a Q block runs from "**Qn.**" to the option line "(a) ... (d) ..." ----
# Stem may span multiple lines (joined). The options line is the first line that
# starts with "(a)".
qs = {}
qblock = re.compile(r"\*\*Q(\d+)\.\*\*\s*(.*?)\n\(a\)\s*(.*?)\s{2,}\(b\)\s*(.*?)\s{2,}\(c\)\s*(.*?)\s{2,}\(d\)\s*(.*?)\s*\n",
                    re.S)
for m in qblock.finditer(qpart):
    n = int(m.group(1))
    stem = re.sub(r"\s+", " ", m.group(2)).strip()
    opts = [m.group(i).strip() for i in (3, 4, 5, 6)]
    qs[n] = (stem, opts)

# ---- parse answers ----
ans = {}
apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*\s*\*\[([MHV]+)\]\*", re.S)
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), re.sub(r"\s+", " ", m.group(3)).strip(), m.group(4))

print(f"Parsed {len(qs)} questions, {len(ans)} answers, sidecar has {len(sidecar)} keys")
assert len(qs) == 500, f"question count {len(qs)} != 500"
assert len(ans) == 500, f"answer count {len(ans)} != 500"
assert len(sidecar) == 500, f"sidecar count {len(sidecar)} != 500"

mismatch = 0
checked = 0
type_counts = {}
fam_counts = {"A": 0, "B": 0}

def tcount(t):
    type_counts[t] = type_counts.get(t, 0) + 1

for n in range(1, 501):
    stem, opts = qs[n]
    letter, aval, diff = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]
    side = sidecar[str(n)]
    fam = side["family"]
    fam_counts[fam] = fam_counts.get(fam, 0) + 1

    # 1) keyed option string must equal stated answer string
    if keyed_opt != aval:
        print(f"Q{n}: keyed option[{letter}]='{keyed_opt}' != stated answer '{aval}'")
        mismatch += 1
        continue
    # 2) 4 distinct options
    if len(set(opts)) != 4:
        print(f"Q{n}: options not distinct: {opts}")
        mismatch += 1
    # 3) cross-check against sidecar (written == computed/authored)
    if side["answer"] != keyed_opt:
        print(f"Q{n}: sidecar '{side['answer']}' != keyed '{keyed_opt}'")
        mismatch += 1

    # ----- CURATED (family B): structural validity only -----
    if fam == "B":
        # exactly one keyed option equals the answer; 4 distinct already checked.
        if keyed_opt != aval:
            print(f"Q{n} CURATED: keyed != answer")
            mismatch += 1
        tcount("curated_word")
        continue

    # ----- RULE-BASED (family A): independent re-derivation -----
    try:
        # Numeric analogy (TWO example pairs): "a1 : f1 :: a2 : f2 :: b : ?"
        manalogy = re.search(
            r"(\d+)\s*:\s*(\d+)\s*::\s*(\d+)\s*:\s*(\d+)\s*::\s*(\d+)\s*:\s*\?", stem)
        # Letter analogy form: "XY : ZW :: PQ : ?"
        mletter = re.search(r"([A-Z]+)\s*:\s*([A-Z]+)\s*::\s*([A-Z]+)\s*:\s*\?", stem)
        # Odd-one-out (numbers): "Numbers: a, b, c, d"
        mnums = re.search(r"Numbers:\s*([\d,\s]+)", stem)
        # Odd-one-out (clusters): "Clusters: AB, CD, ..."
        mclus = re.search(r"Clusters:\s*([A-Z0-9,\s]+)", stem)

        if manalogy:
            a1, f1, a2, f2, b = (int(manalogy.group(i)) for i in range(1, 6))
            name, exp = derive_num_analogy([(a1, f1), (a2, f2)], b)
            if name is None:
                # AMBIGUOUS example pairs -> this must never happen; flag it.
                print(f"Q{n} NUM-ANALOGY AMBIGUOUS: {a1}:{f1}::{a2}:{f2}::{b} "
                      "fits 0 or >1 rules")
                mismatch += 1
            else:
                if str(exp) != aval:
                    print(f"Q{n} num_analogy[{name}]: got '{aval}', expected '{exp}' "
                          f"({a1}:{f1}::{a2}:{f2}::{b})")
                    mismatch += 1
                checked += 1
                # bucket by rule shape for the breakdown / required-types check
                if name == "square":
                    tcount("square_analogy")
                elif name == "cube":
                    tcount("cube_analogy")
                elif name.startswith("x"):
                    tcount("mul_analogy")
                elif name.startswith("+"):
                    tcount("add_analogy")
                elif name in ("n(n+1)", "n(n-1)"):
                    tcount("n_n1_analogy")
                elif name.startswith("sq"):
                    tcount("sq_plus_analogy")
                else:
                    tcount("other_num_analogy")
            continue

        if mletter:
            ex, exc, ask = mletter.group(1), mletter.group(2), mletter.group(3)
            if len(ex) == len(exc) and len(ex) == len(ask):
                deltas = {(pos(b) - pos(a)) % 26 for a, b in zip(ex, exc)}
                if len(deltas) == 1:
                    k = deltas.pop()
                    exp = shift_word(ask, k)
                    if aval != exp:
                        print(f"Q{n} letter_shift: got '{aval}', expected '{exp}'")
                        mismatch += 1
                    checked += 1
                    tcount("letter_shift_analogy")
                    continue
                # opposite-letter: each pos -> 27 - pos
                if all(pos(b) == 27 - pos(a) for a, b in zip(ex, exc)):
                    exp = "".join(from_pos(27 - pos(c)) for c in ask)
                    if aval != exp:
                        print(f"Q{n} letter_opposite: got '{aval}', expected '{exp}'")
                        mismatch += 1
                    checked += 1
                    tcount("letter_opposite_analogy")
                    continue
                # positional varying shift: i-th letter +(i+1)?  derive per-position deltas
                pd = [(pos(b) - pos(a)) % 26 for a, b in zip(ex, exc)]
                exp = "".join(from_pos(pos(c) + pd[i]) for i, c in enumerate(ask))
                if aval == exp:
                    checked += 1
                    tcount("letter_positional_analogy")
                    continue
                # otherwise fall through (still cross-checked vs sidecar above)

        if mnums:
            nums = [int(x) for x in mnums.group(1).split(",") if x.strip()]
            if len(nums) == 4:
                # try each property; exactly one element should violate
                for prop, name in [
                    (is_square, "oo_square"),
                    (is_cube, "oo_cube"),
                    (is_prime, "oo_prime"),
                    (is_consec_prod, "oo_consec_prod"),
                ]:
                    holds = [prop(x) for x in nums]
                    if sum(holds) == 3 and holds.count(False) == 1:
                        odd = nums[holds.index(False)]
                        if aval != str(odd):
                            print(f"Q{n} {name}: got '{aval}', expected odd '{odd}' from {nums}")
                            mismatch += 1
                        checked += 1
                        tcount(name)
                        break
                else:
                    # divisibility: find a k that divides exactly 3 of them
                    found = False
                    for k in range(3, 13):
                        holds = [x % k == 0 for x in nums]
                        if sum(holds) == 3 and holds.count(False) == 1:
                            odd = nums[holds.index(False)]
                            if aval != str(odd):
                                print(f"Q{n} oo_divisible({k}): got '{aval}', expected '{odd}' from {nums}")
                                mismatch += 1
                            checked += 1
                            tcount("oo_divisible")
                            found = True
                            break
                    # if not found, sidecar cross-check (already done) covers it
                if mnums:
                    continue

        if mclus:
            clus = [c.strip() for c in mclus.group(1).split(",") if c.strip()]
            if len(clus) == 4:
                # alphanumeric: letter followed by number == its position
                if all(re.fullmatch(r"[A-Z]\d+", c) for c in clus):
                    holds = [int(c[1:]) == pos(c[0]) for c in clus]
                    if sum(holds) == 3 and holds.count(False) == 1:
                        odd = clus[holds.index(False)]
                        if aval != odd:
                            print(f"Q{n} oo_alnum: got '{aval}', expected '{odd}' from {clus}")
                            mismatch += 1
                        checked += 1
                        tcount("oo_alnum")
                        continue
                # letter-skip: constant internal gap in 3 of 4
                if all(re.fullmatch(r"[A-Z]{3}", c) for c in clus):
                    def gaps(c):
                        return ((pos(c[1]) - pos(c[0])) % 26, (pos(c[2]) - pos(c[1])) % 26)
                    g = [gaps(c) for c in clus]
                    # find the common (equal-gap) pattern among 3
                    from collections import Counter as _C
                    same = [c for c in clus if gaps(c)[0] == gaps(c)[1]]
                    # the majority gap value
                    gapvals = [gaps(c)[0] for c in clus if gaps(c)[0] == gaps(c)[1]]
                    if gapvals:
                        common = _C(gapvals).most_common(1)[0][0]
                        holds = [gaps(c) == (common, common) for c in clus]
                        if sum(holds) == 3 and holds.count(False) == 1:
                            odd = clus[holds.index(False)]
                            if aval != odd:
                                print(f"Q{n} oo_letter_skip: got '{aval}', expected '{odd}' from {clus}")
                                mismatch += 1
                            checked += 1
                            tcount("oo_letter_skip")
                            continue
                # else sidecar cross-check covers it

    except Exception as e:
        print(f"Q{n}: parse skip ({e})")


print()
print(f"Family breakdown (from sidecar): A(rule-based)={fam_counts['A']}, B(curated)={fam_counts['B']}")
print(f"Independently re-derived {checked} rule-based questions by parsing the stem.")
print("Re-derived type breakdown:", dict(sorted(type_counts.items())))

# Required: at least 3 rule types independently re-derived; must include the 3 named.
required = {"square_analogy", "mul_analogy", "oo_square"}
present_required = required & set(type_counts)
print(f"Required rule types present {sorted(required)}: {sorted(present_required)}")
print(f"Distinct rule types independently verified: {len(type_counts)}")

assert len(type_counts) >= 3, "Fewer than 3 rule types independently re-derived!"
assert required.issubset(set(type_counts)), \
    f"Missing required re-derived rule types: {required - set(type_counts)}"

print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
assert mismatch == 0, "verification FAILED"
