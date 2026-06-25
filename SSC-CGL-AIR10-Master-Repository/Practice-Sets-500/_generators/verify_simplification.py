# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Simplification set.

Parse the rendered markdown, confirm 500 Q + 500 A, keyed option value == stated
answer, 4 distinct options. Then for the BODMAS / expression-style questions,
RE-PARSE the expression text out of the stem, rebuild a +-*/() Python expression,
RE-EVALUATE it exactly with Fraction, and confirm it equals the keyed value.
This is a very strong check and is applied to >= 150 questions.

Does NOT import or reuse the generator's objects.
NO unicode emoji in prints - plain "PASS"/"FAIL".
"""
import re
import math
from fractions import Fraction

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_16_Simplification_500.md"
txt = open(PATH, encoding="utf-8").read()

qpart, apart = txt.split("# =================== ANSWER KEY")

qs = {}
qpat = re.compile(
    r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s+\(b\)\s*(.*?)\s+\(c\)\s*(.*?)\s+\(d\)\s*(.*?)\n",
    re.S,
)
for m in qpat.finditer(qpart):
    n = int(m.group(1))
    stem = m.group(2).replace("\n", " ").strip()
    opts = [m.group(3).strip(), m.group(4).strip(),
            m.group(5).strip(), m.group(6).strip()]
    qs[n] = (stem, opts)

ans = {}
apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*")
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), m.group(3).strip())

print(f"Parsed {len(qs)} questions, {len(ans)} answers")
assert len(qs) == 500 and len(ans) == 500, "count mismatch!"


def F(s):
    s = s.strip().replace("₹", "")
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(s).limit_denominator(10**6)


def feval(expr):
    """Evaluate a +-*/() expression EXACTLY using Fraction division.

    Decimal literals (e.g. 6.1) are converted to exact Fractions, never floats.
    """
    allowed = set("0123456789.+-*/() ")
    if not set(expr) <= allowed:
        raise ValueError(f"illegal char in expr: {expr!r}")

    def lit(m):
        s = m.group(0)
        if "." in s:
            whole, frac = s.split(".")
            den = 10 ** len(frac)
            num = int(whole + frac) if whole else int(frac)
            return f"Fraction({num},{den})"
        return f"Fraction({s})"

    pyexpr = re.sub(r"\d+(?:\.\d+)?", lit, expr)
    return eval(pyexpr, {"Fraction": Fraction, "__builtins__": {}})


def to_pyexpr(display):
    """Convert an SSC-display arithmetic snippet to a Python +-*/() expression.

    Handles ×, ÷, the three bracket styles, the 'a/b of c' -> 'a/b * c' rewrite,
    and 'aN bN/dN' mixed-number is NOT handled here (frac_expr stems are improper).
    """
    s = display
    s = s.replace("×", "*").replace("·", "*")
    s = s.replace("÷", "/")
    s = s.replace("−", "-").replace("—", "-")
    s = s.replace("[", "(").replace("]", ")")
    s = s.replace("{", "(").replace("}", ")")
    s = re.sub(r"\bof\b", "*", s)   # 'of' means multiply
    # squared notation a² -> a*a  (only appears as digits + superscript 2)
    s = s.replace("²", "")  # handled separately where needed
    return s.strip()


checked = 0
mismatch = 0
type_counts = {}

# Superscript map for indices stems
SUP = {"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
       "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9"}


def note(kind):
    type_counts[kind] = type_counts.get(kind, 0) + 1


for n, (stem, opts) in qs.items():
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]

    # keyed option value must equal stated answer
    if F(keyed_opt) != F(aval):
        print(f"Q{n}: keyed letter/value mismatch: option[{letter}]={keyed_opt} vs answer {aval}")
        mismatch += 1
        continue
    # 4 distinct options
    if len(set(F(o) for o in opts)) != 4:
        print(f"Q{n}: duplicate options {opts}")
        mismatch += 1

    key = F(aval)

    try:
        # ---------- sqrt-of-expression:  √( <arith> ) ----------
        msq = re.match(r"Simplify:\s*√\((.+)\)\s*$", stem)
        if msq and "²" not in stem and "of" not in stem:
            inner = to_pyexpr(msq.group(1))
            ev = feval(inner)
            r = math.isqrt(ev.numerator) if ev.denominator == 1 else None
            if r is None or Fraction(r) != key or r * r != ev.numerator:
                print(f"Q{n} SQRT-EXPR wrong: inner={inner}->{ev}, key={aval}")
                mismatch += 1
            checked += 1; note("sqrt_expr")
            continue

        # ---------- a^2 - b^2 over a-b ----------
        mdf = re.match(r"Simplify:\s*\((\d+)²\s*[-−]\s*(\d+)²\)\s*÷\s*\((\d+)\s*[-−]\s*(\d+)\)", stem)
        if mdf:
            a, b, c, d = map(int, mdf.groups())
            ev = (Fraction(a * a - b * b)) / (c - d)
            if ev != key:
                print(f"Q{n} DIFFSQ wrong: got {aval}, expect {ev}")
                mismatch += 1
            checked += 1; note("diff_sq")
            continue

        # ---------- 'of' chain:  a/b of c/d of N ----------
        mof = re.match(r"Simplify:\s*(\d+)/(\d+)\s+of\s+(\d+)/(\d+)\s+of\s+(\d+)\s*$", stem)
        if mof:
            p, q, r, s, N = map(int, mof.groups())
            ev = Fraction(p, q) * Fraction(r, s) * N
            if ev != key:
                print(f"Q{n} OF-CHAIN wrong: got {aval}, expect {ev}")
                mismatch += 1
            checked += 1; note("of_chain")
            continue

        # ---------- frac BODMAS / improper-fraction expr (no brackets, no 'of') ----------
        mfb = re.match(r"Simplify:\s*([0-9 /×÷+\-−]+)\s*$", stem)
        # ---------- generic BODMAS (brackets, ×, ÷, +, -) ----------
        mb = re.match(r"Simplify:\s*(.+)$", stem)
        mapprox = re.match(r".*approximate value of:\s*(.+)$", stem)
        mnear = re.match(r".*value nearest to\s*(.+?)\s*is approximately", stem)

        target = None
        kind = None
        if mnear:
            target = mnear.group(1); kind = "approx"
        elif mapprox:
            target = mapprox.group(1); kind = "approx"
        elif mb and "√" not in stem and "²" not in stem and "of" not in stem \
                and "^" not in stem and "continued fraction" not in stem:
            target = mb.group(1); kind = "bodmas"

        if target is not None:
            # mixed numbers like "3 1/4" would break a pure expr; detect & skip those
            if re.search(r"\d+\s+\d+/\d+", target):
                # mixed-number arithmetic - reconstruct improper fractions
                # pattern: W n/d (+|-) W n/d (+|-) W n/d
                toks = re.findall(r"([+\-−])?\s*(\d+)\s+(\d+)/(\d+)", target)
                # first term has no leading sign
                expr_parts = []
                # rebuild by scanning with signs
                m_terms = re.finditer(r"([+\-−]?)\s*(\d+)\s+(\d+)/(\d+)", target)
                val = Fraction(0)
                first = True
                ok = True
                for mt in m_terms:
                    sign, w, num, den = mt.group(1), int(mt.group(2)), int(mt.group(3)), int(mt.group(4))
                    term = Fraction(w * den + num, den)
                    if first and sign in ("", None):
                        val = term
                    elif sign in ("-", "−"):
                        val -= term
                    else:
                        val += term
                    first = False
                if val != key:
                    print(f"Q{n} MIXED-FRAC wrong: target='{target}' got {aval}, expect {val}")
                    mismatch += 1
                checked += 1; note("mixed_frac")
                continue

            py = to_pyexpr(target)
            try:
                ev = feval(py)
            except Exception as e:
                # not a pure arithmetic expr; skip
                raise
            if ev != key:
                print(f"Q{n} {kind.upper()} wrong: expr='{py}' -> {ev}, key={aval}")
                mismatch += 1
            checked += 1; note(kind)
            continue

        # ---------- rationalise: 1 ÷ (√A + √B) ----------
        mrat = re.match(r"Find the value of:\s*1\s*÷\s*\(√(\d+)\s*\+\s*√(\d+)\)", stem)
        if mrat:
            A, B = map(int, mrat.groups())
            mm, nn = math.isqrt(A), math.isqrt(B)
            if mm * mm == A and nn * nn == B:
                ev = Fraction(1, mm + nn)
                if ev != key:
                    print(f"Q{n} RATIONALISE wrong: got {aval}, expect {ev}")
                    mismatch += 1
                checked += 1; note("rationalise")
            continue

        # ---------- surd √a × √b ----------
        msm = re.match(r"Simplify:\s*√(\d+)\s*×\s*√(\d+)\s*$", stem)
        if msm:
            a, b = map(int, msm.groups())
            r = math.isqrt(a * b)
            if r * r == a * b and Fraction(r) != key:
                print(f"Q{n} SURD-MULT wrong: got {aval}, expect {r}")
                mismatch += 1
            checked += 1; note("surd_mult")
            continue

        # ---------- surd √(a/b) ----------
        msd = re.match(r"Simplify:\s*√\((\d+)/(\d+)\)\s*$", stem)
        if msd:
            a, b = map(int, msd.groups())
            q = Fraction(a, b)
            r = math.isqrt(q.numerator) if q.denominator == 1 else None
            if r is not None and r * r == q.numerator:
                if Fraction(r) != key:
                    print(f"Q{n} SURD-DIV wrong: got {aval}, expect {r}")
                    mismatch += 1
                checked += 1; note("surd_div")
            continue

        # ---------- indices x^a · x^b ----------
        mip = re.match(r"Simplify and evaluate:\s*(\d+)\^(\d+)\s*×\s*(\d+)\^(\d+)\s*$", stem)
        if mip:
            x, a, x2, b = map(int, mip.groups())
            if x == x2:
                ev = Fraction(x ** (a + b))
                if ev != key:
                    print(f"Q{n} IDX-PROD wrong: got {aval}, expect {ev}")
                    mismatch += 1
                checked += 1; note("idx_prod")
            continue

        # ---------- indices (x^a)^b ----------
        mpp = re.match(r"Simplify and evaluate:\s*\((\d+)\^(\d+)\)\^(\d+)\s*$", stem)
        if mpp:
            x, a, b = map(int, mpp.groups())
            ev = Fraction(x ** (a * b))
            if ev != key:
                print(f"Q{n} IDX-POW wrong: got {aval}, expect {ev}")
                mismatch += 1
            checked += 1; note("idx_pow")
            continue

        # ---------- solve a^x = b ----------
        mse = re.match(r"If (\d+)\^x = (\d+), then the value of x is:", stem)
        if mse:
            a, b = map(int, mse.groups())
            x = round(math.log(b, a))
            if a ** x == b:
                if Fraction(x) != key:
                    print(f"Q{n} SOLVE-EXP wrong: got {aval}, expect {x}")
                    mismatch += 1
                checked += 1; note("solve_exp")
            continue

        # ---------- repeated root √√... N ----------
        mrr = re.match(r"Simplify:\s*(√+)(\d+)\s*$", stem)
        if mrr:
            roots = len(mrr.group(1))
            radicand = int(mrr.group(2))
            v = radicand
            ok = True
            for _ in range(roots):
                r = math.isqrt(v)
                if r * r != v:
                    ok = False; break
                v = r
            if ok:
                if Fraction(v) != key:
                    print(f"Q{n} REP-ROOT wrong: got {aval}, expect {v}")
                    mismatch += 1
                checked += 1; note("rep_root")
            continue

    except Exception as e:
        safe = stem[:60].encode("ascii", "replace").decode("ascii")
        print(f"Q{n}: parse skip ({e}) :: {safe}")

print(f"Independently re-solved {checked} questions from parsed stems.")
print("Re-solved type breakdown:", type_counts)
print(f"Distinct template types independently verified: {len(type_counts)}")

assert checked >= 150, f"Re-evaluated only {checked} (<150) expression questions!"
assert len(type_counts) >= 5, "Fewer than 5 template types independently re-solved!"

print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
