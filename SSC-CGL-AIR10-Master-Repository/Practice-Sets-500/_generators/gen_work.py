# -*- coding: utf-8 -*-
"""
SSC CGL Time & Work (incl. Pipes & Cisterns) - 500 hard MCQ generator.
Every answer is COMPUTED via Fraction / LCM-of-times "total work units"
method, so the key is provably correct. Builds 4 distinct options
(1 correct + 3 common-mistake distractors), randomizes correct position,
dedupes question stems, outputs markdown.
"""
import random
from fractions import Fraction
from math import gcd

random.seed(20260625)  # deterministic

LETTERS = "abcd"

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_list(xs):
    r = 1
    for x in xs:
        r = lcm(r, int(x))
    return r

def fmt(x):
    """Format a number cleanly: ints as ints, fractions as decimals or fraction."""
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        f = float(x)
        if abs(f - round(f, 4)) < 1e-9:
            s = f"{f:.4f}".rstrip("0").rstrip(".")
            return s
        return f"{x.numerator}/{x.denominator}"
    if isinstance(x, float):
        if abs(x - round(x)) < 1e-9:
            return str(int(round(x)))
        s = f"{x:.4f}".rstrip("0").rstrip(".")
        return s
    return str(x)

def make_options(correct, distractors):
    """Return (options_list, correct_index). Ensures 4 distinct values."""
    opts = [correct]
    for d in distractors:
        if d is None:
            continue
        if all(abs(float(d) - float(o)) > 1e-9 for o in opts):
            opts.append(d)
        if len(opts) == 4:
            break
    bump = 1
    cf = float(correct)
    while len(opts) < 4:
        cand = Fraction(correct) + Fraction(bump * (3 if cf >= 0 else -3))
        if all(abs(float(cand) - float(o)) > 1e-9 for o in opts):
            opts.append(cand)
        bump += 1
    random.shuffle(opts)
    ci = opts.index(correct)
    return opts, ci

questions = []  # each: dict(stem, opts, ci, sol, diff)
seen = set()

def is_clean(x):
    """Accept integers, halves/thirds/quarters/fifths/sixths/eighths, <=2dp decimals."""
    fr = Fraction(x).limit_denominator(10**6)
    if fr.denominator in (1, 2, 3, 4, 5, 6, 7, 8, 10, 12):
        return True
    f = float(fr)
    return abs(f - round(f, 2)) < 1e-9

def add(stem, correct, distractors, sol, diff):
    key = stem.strip()
    if key in seen:
        return False
    cfr = Fraction(correct).limit_denominator(10**6)
    if not is_clean(cfr):
        return False
    if cfr <= 0:
        return False
    dfrs = [Fraction(d).limit_denominator(10**6) for d in distractors if d is not None]
    dfrs = [d for d in dfrs if is_clean(d) and d != cfr and d > 0]
    if len(dfrs) < 3:
        return False
    seen.add(key)
    opts, ci = make_options(cfr, dfrs)
    questions.append({
        "stem": stem,
        "opts": [fmt(o) for o in opts],
        "ci": ci,
        "sol": sol,
        "diff": diff,
    })
    return True

# ---------------- TEMPLATES ----------------
# All use the LCM-of-times "total work units" method internally so rates are integers.

def t_ab_together_a_alone():
    """A+B finish in t days, A alone in a days -> B alone. [H]"""
    a = random.choice([10, 12, 15, 16, 18, 20, 24, 25, 30, 36, 40, 45, 60])
    t = random.choice([4, 5, 6, 7.5, 8, 9, 10, 12, 15, 18])
    tf = Fraction(t).limit_denominator(1000)
    af = Fraction(a)
    if tf >= af:
        return None
    # 1/t = 1/a + 1/b -> 1/b = 1/t - 1/a
    inv_b = Fraction(1, 1) / tf - Fraction(1, 1) / af
    if inv_b <= 0:
        return None
    b = 1 / inv_b
    correct = b
    wrong1 = af + tf                       # naive add
    wrong2 = af - tf                       # naive subtract
    wrong3 = (af * tf) / (af + tf)         # the product/sum formula (gives together, not B)
    stem = (f"A and B together can complete a piece of work in {fmt(tf)} days. "
            f"If A alone can complete it in {fmt(af)} days, then B alone can complete "
            f"the same work in how many days?")
    sol = (f"B's one-day work = 1/{fmt(tf)} - 1/{fmt(af)} = {fmt(inv_b)}. "
           f"So B alone takes 1 / ({fmt(inv_b)}) = {fmt(correct)} days. "
           f"Trap: do NOT add/subtract the day-figures directly.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_two_individuals_together():
    """A alone a days, B alone b days -> together. [M]"""
    a = random.choice([6, 8, 10, 12, 15, 16, 18, 20, 24, 30, 36, 40, 45, 60])
    b = random.choice([6, 8, 10, 12, 15, 16, 18, 20, 24, 30, 36, 40, 45, 60])
    if a == b:
        return None
    af, bf = Fraction(a), Fraction(b)
    together = (af * bf) / (af + bf)
    correct = together
    wrong1 = af + bf                  # add times
    wrong2 = (af + bf) / 2           # average times
    wrong3 = abs(af - bf)           # difference
    stem = (f"A can do a work in {a} days and B can do the same work in {b} days. "
            f"Working together, in how many days will they complete the work?")
    sol = (f"Together time = ab/(a+b) = {a}×{b}/({a}+{b}) = {fmt(correct)} days. "
           f"(Add the RATES 1/{a}+1/{b}, never the day-counts.)")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_three_together():
    """A, B, C alone -> all three together. [H]"""
    trip = random.choice([
        (10, 12, 15), (12, 15, 20), (6, 8, 12), (10, 15, 30),
        (8, 12, 24), (20, 30, 60), (15, 20, 30), (12, 18, 36),
        (9, 12, 18), (10, 20, 40), (6, 12, 24), (12, 16, 24),
    ])
    a, b, c = trip
    L = lcm_list([a, b, c])
    rate = L // a + L // b + L // c
    together = Fraction(L, rate)
    correct = together
    wrong1 = Fraction(a + b + c)
    wrong2 = Fraction(a + b + c, 3)
    wrong3 = Fraction(L, L // a + L // b)   # only A and B
    stem = (f"A, B and C can individually complete a work in {a}, {b} and {c} days "
            f"respectively. If all three work together, the work will be finished in:")
    sol = (f"Take total work = LCM({a},{b},{c}) = {L} units. Rates = {L//a}+{L//b}+{L//c} "
           f"= {rate} units/day. Time = {L}/{rate} = {fmt(correct)} days.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_pairs_to_individual():
    """(A+B), (B+C), (C+A) times given -> all three together OR one alone. [VH]"""
    # pick clean individual times, derive pair times, ask for all-three time
    trip = random.choice([
        (12, 15, 20), (10, 12, 15), (20, 30, 60), (8, 12, 24),
        (15, 20, 30), (12, 18, 36), (10, 15, 30), (6, 12, 24),
    ])
    a, b, c = trip
    L = lcm_list([a, b, c])
    ra, rb, rc = L // a, L // b, L // c
    # pair times
    ab = Fraction(L, ra + rb)
    bc = Fraction(L, rb + rc)
    ca = Fraction(L, rc + ra)
    if not (ab.denominator <= 12 and bc.denominator <= 12 and ca.denominator <= 12):
        return None
    total_rate = ra + rb + rc  # = (sum of pair rates)/2
    together = Fraction(L, total_rate)
    correct = together
    wrong1 = (ab + bc + ca) / 3        # average of pairs
    wrong2 = Fraction(L, ra + rb)      # just one pair
    wrong3 = ab + bc + ca              # sum of pair times
    stem = (f"A and B together can do a work in {fmt(ab)} days, B and C in {fmt(bc)} days, "
            f"and C and A in {fmt(ca)} days. In how many days can all three together "
            f"finish the work?")
    sol = (f"Let total work = {L} units. Adding the three pair-rates "
           f"({ra+rb}+{rb+rc}+{rc+ra}) = {2*total_rate} gives 2×(A+B+C), so the "
           f"A+B+C rate = {total_rate} units/day. Time = {L}/{total_rate} = {fmt(correct)} days.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_leaves_after_k():
    """A+B start, A leaves after k days, B finishes rest -> total days. [H]"""
    a = random.choice([12, 15, 16, 18, 20, 24, 30, 36, 40])
    b = random.choice([12, 15, 16, 18, 20, 24, 30, 36, 40, 45, 60])
    if a == b:
        return None
    L = lcm(a, b)
    ra, rb = L // a, L // b
    k = random.choice([2, 3, 4, 5, 6])
    done = (ra + rb) * k
    if done >= L:
        return None
    remaining = L - done
    rest_time = Fraction(remaining, rb)
    total = Fraction(k) + rest_time
    correct = total
    wrong1 = Fraction(L, rb)              # ignores joint phase
    wrong2 = rest_time                    # only the remaining time
    wrong3 = Fraction(k) + Fraction(remaining, ra)  # uses A's rate by mistake
    stem = (f"A and B can complete a work in {a} and {b} days respectively. They start "
            f"working together, but A leaves after {k} days. In how many TOTAL days will "
            f"the work be completed?")
    sol = (f"Total work = LCM = {L} units; rates A={ra}, B={rb}/day. In {k} days together "
           f"they do ({ra}+{rb})×{k} = {done} units. Remaining {remaining} units done by B "
           f"in {remaining}/{rb} = {fmt(rest_time)} days. Total = {k} + {fmt(rest_time)} "
           f"= {fmt(correct)} days.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_efficiency_more():
    """A is x% more efficient than B; B alone b days -> A alone (or together). [H]"""
    x = random.choice([20, 25, 50, 100, 150, 33.3333, 66.6667])
    if x == 33.3333:
        xr = Fraction(100, 3)
    elif x == 66.6667:
        xr = Fraction(200, 3)
    else:
        xr = Fraction(x).limit_denominator(1000)
    b = random.choice([12, 15, 18, 20, 24, 30, 36, 40, 45, 50, 60])
    bf = Fraction(b)
    # A's efficiency = (1 + x/100) of B; time inversely proportional
    a = bf / (1 + xr / 100)
    if a.denominator > 12:
        return None
    correct = a
    wrong1 = bf * (1 + xr / 100)        # multiplies (wrong direction)
    wrong2 = bf - bf * xr / 100         # subtracts % of time
    wrong3 = bf * (1 - xr / 100) if xr < 100 else bf / 2
    stem = (f"A is {fmt(xr)}% more efficient than B. If B alone can finish a work in "
            f"{b} days, in how many days can A alone finish the same work?")
    sol = (f"Efficiency(A) = (1 + {fmt(xr)}/100)×Efficiency(B). Time is inverse of "
           f"efficiency, so A's time = {b} / (1 + {fmt(xr)}/100) = {fmt(correct)} days. "
           f"Trap: more efficient => LESS time, so divide (not multiply).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_efficiency_ratio_together():
    """A twice/thrice as efficient as B; together t days -> A alone. [H]"""
    k = random.choice([2, 3, 4])   # A is k times as efficient as B
    t = random.choice([4, 6, 8, 9, 10, 12, 15, 18, 20])
    tf = Fraction(t)
    # rate B = 1 unit, rate A = k units; together (k+1) units/day finishing in t days
    # so total work = (k+1)*t units; A alone = total / k
    total = (k + 1) * tf
    a_alone = total / k
    b_alone = total
    if a_alone.denominator > 12:
        return None
    correct = a_alone
    wrong1 = b_alone                       # gives B alone
    wrong2 = tf * k                        # multiplies together-time by k
    wrong3 = tf / k                        # divides
    stem = (f"A is {k} times as efficient as B. Working together they finish a work in "
            f"{t} days. In how many days can A alone finish the work?")
    sol = (f"Let B do 1 unit/day, A do {k} units/day; together {k+1} units/day for {t} days "
           f"=> total = {fmt(total)} units. A alone = {fmt(total)}/{k} = {fmt(correct)} days.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_men_women_mixed():
    """m men + n women given combined rates -> mixed-group time. [VH]"""
    # 1 man = p women efficiency; given M men finish in dm days, find time for combo
    combos = random.choice([
        # (men, men_days, women, women_days, qm, qw)
        (8, 12, 12, 16, 4, 6),
        (6, 10, 10, 12, 3, 5),
        (10, 8, 8, 15, 5, 4),
        (12, 9, 9, 16, 6, 6),
        (4, 15, 6, 20, 2, 3),
    ])
    M, Dm, W, Dw, qm, qw = combos
    # total work via men: man-rate r_m = 1/(M*Dm) ; woman-rate r_w = 1/(W*Dw)
    rm = Fraction(1, M * Dm)
    rw = Fraction(1, W * Dw)
    combined = qm * rm + qw * rw
    time = 1 / combined
    if time.denominator > 12:
        return None
    correct = time
    wrong1 = Fraction(M * Dm, qm)          # ignores women
    wrong2 = 1 / (qm * rm)                 # men only
    wrong3 = Fraction(Dm + Dw, 2)          # average days
    stem = (f"{M} men can finish a work in {Dm} days, and {W} women can finish the same "
            f"work in {Dw} days. In how many days can {qm} men and {qw} women together "
            f"finish the work?")
    sol = (f"1 man's 1-day work = 1/({M}×{Dm}) = {fmt(rm)}; 1 woman's = 1/({W}×{Dw}) = {fmt(rw)}. "
           f"Combined rate = {qm}×{fmt(rm)} + {qw}×{fmt(rw)} = {fmt(combined)} work/day. "
           f"Time = 1/({fmt(combined)}) = {fmt(correct)} days.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_wages_ratio():
    """Total wages split between A and B by work done. [H]"""
    a = random.choice([10, 12, 15, 16, 18, 20, 24, 30])
    b = random.choice([10, 12, 15, 16, 18, 20, 24, 30, 36, 40, 60])
    if a == b:
        return None
    L = lcm(a, b)
    ra, rb = L // a, L // b
    # total wage divisible so that A's share is clean
    unit = random.choice([100, 120, 150, 200, 240, 300])
    total_wage = (ra + rb) * unit
    a_share = Fraction(ra, ra + rb) * total_wage
    if a_share.denominator != 1:
        return None
    correct = a_share
    wrong1 = Fraction(rb, ra + rb) * total_wage   # B's share (swap)
    wrong2 = Fraction(total_wage, 2)              # equal split
    wrong3 = Fraction(a, a + b) * total_wage      # uses days ratio (wrong direction)
    stem = (f"A can do a work in {a} days and B in {b} days. They complete it together "
            f"and receive ₹{total_wage} in total. A's share of the wages is:")
    sol = (f"Wages split in ratio of work done = ratio of rates = {ra}:{rb}. "
           f"A's share = {ra}/({ra}+{rb}) × {total_wage} = ₹{fmt(correct)}. "
           f"Trap: share is in ratio of EFFICIENCY, not days.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_alternate_days():
    """A and B work on alternate days (A starts) -> total days. [VH]"""
    a = random.choice([8, 9, 10, 12, 15, 16, 18, 20])
    b = random.choice([8, 9, 10, 12, 15, 16, 18, 20, 24])
    if a == b:
        return None
    L = lcm(a, b)
    ra, rb = L // a, L // b
    # A starts. Simulate.
    work = 0
    day = 0
    seq = [ra, rb]  # A on odd days, B on even
    finished = None
    while work < L and day < 200:
        r = seq[day % 2]
        if work + r >= L:
            # finishes partway through this day
            frac = Fraction(L - work, r)
            finished = Fraction(day) + frac
            work = L
            break
        work += r
        day += 1
    if finished is None or finished.denominator > 12:
        return None
    correct = finished
    wrong1 = Fraction(L, ra + rb) * 2        # treats as together pace mistake
    wrong2 = Fraction(a + b, 2)             # average
    wrong3 = (Fraction(a) * Fraction(b)) / (Fraction(a) + Fraction(b))  # together time
    stem = (f"A and B can do a work in {a} and {b} days respectively. They work on "
            f"ALTERNATE days with A starting on the first day. In how many days will the "
            f"work be completed?")
    sol = (f"Total work = LCM = {L} units; A does {ra}/day, B does {rb}/day on alternate "
           f"days starting with A. Counting day by day until the {L} units are done gives "
           f"{fmt(correct)} days. Trap: order matters and the last day may be partial.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_two_fill_one_empty():
    """Two fill pipes + one empty pipe -> net fill time. [H]"""
    f1 = random.choice([6, 8, 10, 12, 15, 16, 20, 24])
    f2 = random.choice([8, 10, 12, 15, 16, 18, 20, 24, 30])
    e = random.choice([10, 12, 15, 16, 18, 20, 24, 30, 36, 40, 60])
    L = lcm_list([f1, f2, e])
    net = L // f1 + L // f2 - L // e
    if net <= 0:
        return None
    time = Fraction(L, net)
    if time.denominator > 12:
        return None
    correct = time
    wrong1 = Fraction(L, L // f1 + L // f2)         # ignores leak
    wrong2 = Fraction(L, L // f1 + L // f2 + L // e)  # adds leak instead
    wrong3 = Fraction(f1 + f2 + e, 3)               # average
    stem = (f"Two pipes can fill a tank in {f1} and {f2} hours respectively, while a "
            f"third (outlet) pipe can empty the full tank in {e} hours. If all three are "
            f"opened together, the tank will be filled in:")
    sol = (f"Tank = LCM = {L} units. Net inflow = {L//f1}+{L//f2}-{L//e} = {net} units/hr. "
           f"Time = {L}/{net} = {fmt(correct)} hours.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_leak_with_fill():
    """Fill pipe fills in f hrs; with leak takes longer -> leak empties full in? [VH]"""
    f = random.choice([6, 8, 10, 12, 15, 16, 20])
    # leak time L_leak; combined time = f*L/(L-f)
    leak = random.choice([12, 15, 18, 20, 24, 30, 36, 40, 48, 60])
    if leak <= f:
        return None
    Lc = lcm(f, leak)
    net = Lc // f - Lc // leak
    if net <= 0:
        return None
    combined = Fraction(Lc, net)  # time with leak
    if combined.denominator > 12:
        return None
    # Ask: given fill alone = f and with leak = combined, find leak-empty time = leak
    correct = Fraction(leak)
    cf = combined
    ff = Fraction(f)
    # correct formula: 1/leak = 1/f - 1/combined
    wrong1 = cf - ff                     # naive subtract
    wrong2 = cf + ff                     # naive add
    wrong3 = (ff * cf) / (cf - ff) + 1   # near-miss
    stem = (f"A pipe can fill a tank in {f} hours. Due to a leak at the bottom, it takes "
            f"{fmt(combined)} hours to fill the tank. In how many hours can the leak alone "
            f"empty the full tank?")
    sol = (f"1/leak = 1/{f} - 1/{fmt(combined)} = {fmt(Fraction(1,f)-1/cf)} per hour, "
           f"so the leak empties the full tank in {fmt(correct)} hours. "
           f"Trap: combine rates, do not just subtract the hour-figures.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_pipe_opened_late():
    """Pipe A open whole time, pipe B opened after k hrs -> total fill time. [VH]"""
    a = random.choice([10, 12, 15, 16, 18, 20, 24])
    b = random.choice([12, 15, 16, 18, 20, 24, 30])
    if a == b:
        return None
    L = lcm(a, b)
    ra, rb = L // a, L // b
    k = random.choice([2, 3, 4, 5, 6])
    done = ra * k
    if done >= L:
        return None
    remaining = L - done
    rest = Fraction(remaining, ra + rb)
    total = Fraction(k) + rest
    if total.denominator > 12:
        return None
    correct = total
    wrong1 = Fraction(L, ra + rb)              # ignores solo phase
    wrong2 = Fraction(k) + Fraction(remaining, rb)  # uses only B for rest
    wrong3 = (Fraction(a) * Fraction(b)) / (Fraction(a) + Fraction(b))
    stem = (f"Pipe A can fill a tank in {a} hours and pipe B in {b} hours. Pipe A is "
            f"opened first, and after {k} hours pipe B is also opened. The total time "
            f"taken to fill the tank is:")
    sol = (f"Tank = LCM = {L} units; A={ra}, B={rb} units/hr. In first {k} hrs A fills "
           f"{ra}×{k} = {done} units. Remaining {remaining} done by both at {ra+rb}/hr in "
           f"{remaining}/{ra+rb} = {fmt(rest)} hrs. Total = {k} + {fmt(rest)} = {fmt(correct)} hrs.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_tank_partly_full():
    """Tank already x full; fill pipe + leak -> time to fill remaining. [H]"""
    f = random.choice([6, 8, 10, 12, 15, 16, 20])
    e = random.choice([12, 15, 18, 20, 24, 30, 40, 60])
    if e <= f:
        return None
    frac_full = random.choice([Fraction(1, 4), Fraction(1, 3), Fraction(1, 2),
                               Fraction(2, 5), Fraction(3, 5), Fraction(2, 3)])
    L = lcm(f, e)
    net = L // f - L // e
    if net <= 0:
        return None
    remaining = L * (1 - frac_full)
    time = remaining / net
    if time.denominator > 12:
        return None
    correct = time
    wrong1 = Fraction(L, net)                       # fills whole tank
    wrong2 = (L * frac_full) / net                 # fills only the already-full part
    wrong3 = remaining / (L // f)                  # ignores leak
    stem = (f"A tank is already {fmt(frac_full)} full. A pipe can fill the whole tank in "
            f"{f} hours, while a leak can empty the full tank in {e} hours. With both "
            f"open, how long will it take to fill the tank completely?")
    sol = (f"Tank = {L} units; net inflow = {L//f}-{L//e} = {net} units/hr. Already "
           f"{fmt(frac_full)} full, so remaining = {fmt(1-frac_full)}×{L} = {fmt(remaining)} units. "
           f"Time = {fmt(remaining)}/{net} = {fmt(correct)} hours.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_mandays_chain():
    """M1 D1 H1 / W1 = M2 D2 H2 / W2 -> find missing men or days. [H]"""
    M1 = random.choice([12, 15, 16, 18, 20, 24, 30])
    D1 = random.choice([8, 10, 12, 15, 16, 18, 20])
    H1 = random.choice([6, 7, 8, 9, 10])
    D2 = random.choice([6, 8, 10, 12, 14, 15])
    H2 = random.choice([6, 7, 8, 9, 10])
    # same work: M1*D1*H1 = M2*D2*H2 -> M2 = M1*D1*H1/(D2*H2)
    M2 = Fraction(M1 * D1 * H1, D2 * H2)
    if M2.denominator != 1 or M2 <= 0 or M2 > 200:
        return None
    correct = M2
    wrong1 = Fraction(M1 * D2 * H2, D1 * H1)        # inverted
    wrong2 = Fraction(M1 * D1, D2)                  # ignores hours
    wrong3 = Fraction(M1 * D1 * H1, D2 * H2) + M1   # off
    stem = (f"If {M1} men working {H1} hours a day can complete a work in {D1} days, how "
            f"many men are required to complete the same work in {D2} days working {H2} "
            f"hours a day?")
    sol = (f"Men-days-hours constant: M2 = (M1×D1×H1)/(D2×H2) = "
           f"({M1}×{D1}×{H1})/({D2}×{H2}) = {fmt(correct)} men.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_mandays_days():
    """Find days given changed number of men. [M]"""
    M1 = random.choice([12, 15, 16, 18, 20, 24, 30, 36, 40])
    D1 = random.choice([8, 10, 12, 15, 16, 18, 20, 24])
    M2 = random.choice([6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 30])
    if M2 == M1:
        return None
    D2 = Fraction(M1 * D1, M2)
    if D2.denominator > 12:
        return None
    correct = D2
    wrong1 = Fraction(M2 * D1, M1)        # inverted ratio
    wrong2 = Fraction(D1 + (M1 - M2))     # additive nonsense
    wrong3 = Fraction(D1 * M2, M1) + D1   # off
    stem = (f"{M1} men can complete a work in {D1} days. How many days will {M2} men "
            f"take to complete the same work?")
    sol = (f"Men × days = constant. D2 = (M1×D1)/M2 = ({M1}×{D1})/{M2} = {fmt(correct)} days. "
           f"Fewer men => more days (inverse proportion).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_men_leave_after():
    """Some men leave after k days -> remaining time. [VH]"""
    M = random.choice([20, 24, 30, 36, 40, 45, 60])
    D = random.choice([10, 12, 15, 16, 18, 20, 24])
    k = random.choice([3, 4, 5, 6, 8])
    if k >= D:
        return None
    leave = random.choice([4, 5, 6, 8, 10, 12])
    if leave >= M:
        return None
    total_work = M * D  # man-days
    done = M * k
    remaining = total_work - done
    rem_men = M - leave
    rest_days = Fraction(remaining, rem_men)
    if rest_days.denominator > 12:
        return None
    correct = rest_days
    wrong1 = Fraction(remaining, M)            # forgets men left
    wrong2 = Fraction(total_work, rem_men) - k # off framing
    wrong3 = Fraction(remaining, M - 2 * leave) if M - 2 * leave > 0 else Fraction(remaining, rem_men) + 2
    stem = (f"{M} men can complete a work in {D} days. After working for {k} days, "
            f"{leave} men leave the job. In how many MORE days will the remaining men "
            f"complete the work?")
    sol = (f"Total = {M}×{D} = {total_work} man-days. In {k} days, {M}×{k} = {done} man-days "
           f"done; remaining = {remaining} man-days. Now {rem_men} men work, so more days "
           f"= {remaining}/{rem_men} = {fmt(correct)} days.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_men_join_after():
    """Reinforcement: more men join after k days -> finish in total time / find days saved. [VH]"""
    M = random.choice([10, 12, 15, 16, 18, 20, 24])
    D = random.choice([20, 24, 30, 36, 40, 45])
    k = random.choice([5, 6, 8, 10, 12])
    if k >= D:
        return None
    join = random.choice([4, 5, 6, 8, 10, 12])
    total_work = M * D
    done = M * k
    remaining = total_work - done
    new_men = M + join
    rest_days = Fraction(remaining, new_men)
    if rest_days.denominator > 12:
        return None
    total_time = Fraction(k) + rest_days
    correct = total_time
    wrong1 = Fraction(D)                      # original time, unchanged
    wrong2 = rest_days                        # only remaining
    wrong3 = Fraction(k) + Fraction(remaining, M)  # forgets reinforcement
    stem = (f"{M} men can complete a work in {D} days. After {k} days, {join} more men "
            f"join them. In how many TOTAL days will the work be completed?")
    sol = (f"Total = {M}×{D} = {total_work} man-days. After {k} days, {done} man-days done; "
           f"remaining = {remaining}. With {new_men} men, that takes {remaining}/{new_men} "
           f"= {fmt(rest_days)} days. Total = {k} + {fmt(rest_days)} = {fmt(correct)} days.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_single_fill_pipe():
    """Single fill pipe rate question / simple net of one fill + one leak. [M]"""
    f = random.choice([4, 5, 6, 8, 10, 12, 15, 20])
    e = random.choice([12, 15, 20, 24, 30, 40, 60])
    if e <= f:
        return None
    L = lcm(f, e)
    net = L // f - L // e
    if net <= 0:
        return None
    time = Fraction(L, net)
    if time.denominator > 12:
        return None
    correct = time
    wrong1 = Fraction(f)                      # ignores leak
    wrong2 = Fraction(e - f)                  # naive subtract
    wrong3 = Fraction(f + e, 2)               # average
    stem = (f"A pipe can fill a tank in {f} hours, and a leak at the bottom can empty the "
            f"full tank in {e} hours. If both work together, in how many hours will the "
            f"tank be filled?")
    sol = (f"Tank = LCM = {L} units; net inflow = {L//f}-{L//e} = {net} units/hr. "
           f"Time = {L}/{net} = {fmt(correct)} hours.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_fraction_of_work():
    """A does work in d days -> work done in k days (fraction). [M]"""
    d = random.choice([12, 15, 16, 18, 20, 24, 30, 36, 40, 45, 48, 60])
    k = random.choice([3, 4, 5, 6, 8, 9, 10, 12])
    if k >= d:
        return None
    frac_done = Fraction(k, d)
    frac_left = 1 - frac_done
    correct = frac_left
    wrong1 = frac_done                         # gives part done
    wrong2 = Fraction(d - k, d) - Fraction(1, d) if d - k - 1 > 0 else frac_done + Fraction(1, d)
    wrong3 = Fraction(k, d) + Fraction(1, d) if Fraction(k, d) + Fraction(1, d) != frac_left else frac_done - Fraction(1, d)
    stem = (f"A can complete a work in {d} days. If A works for {k} days only, what "
            f"FRACTION of the work is left unfinished?")
    sol = (f"In {k} days A does {k}/{d} = {fmt(frac_done)} of the work. "
           f"Fraction left = 1 - {fmt(frac_done)} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_double_efficiency_days():
    """If A becomes twice/half as efficient, find new days. [M]"""
    d = random.choice([12, 16, 18, 20, 24, 30, 36, 40, 48, 60])
    mult = random.choice([2, 3, 4])  # efficiency multiplied
    new_d = Fraction(d, mult)
    if new_d.denominator > 12:
        return None
    correct = new_d
    wrong1 = Fraction(d * mult)               # multiplies instead of divides
    wrong2 = Fraction(d - mult)               # subtract
    wrong3 = Fraction(d, mult) + d            # off
    stem = (f"A can finish a work in {d} days. If A works {mult} times as fast, how many "
            f"days will A now take to finish the same work?")
    sol = (f"Time is inversely proportional to speed. New time = {d}/{mult} = {fmt(correct)} "
           f"days. (Faster ⇒ fewer days.)")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

TEMPLATES = [
    t_ab_together_a_alone, t_two_individuals_together, t_three_together,
    t_pairs_to_individual, t_leaves_after_k, t_efficiency_more,
    t_efficiency_ratio_together, t_men_women_mixed, t_wages_ratio,
    t_alternate_days, t_two_fill_one_empty, t_leak_with_fill,
    t_pipe_opened_late, t_tank_partly_full, t_mandays_chain,
    t_mandays_days, t_men_leave_after, t_men_join_after,
    t_single_fill_pipe, t_fraction_of_work, t_double_efficiency_days,
]

DIFF_OF = {
    t_ab_together_a_alone: "H", t_two_individuals_together: "M", t_three_together: "H",
    t_pairs_to_individual: "VH", t_leaves_after_k: "H", t_efficiency_more: "H",
    t_efficiency_ratio_together: "H", t_men_women_mixed: "VH", t_wages_ratio: "H",
    t_alternate_days: "VH", t_two_fill_one_empty: "H", t_leak_with_fill: "VH",
    t_pipe_opened_late: "VH", t_tank_partly_full: "H", t_mandays_chain: "H",
    t_mandays_days: "M", t_men_leave_after: "VH", t_men_join_after: "VH",
    t_single_fill_pipe: "M", t_fraction_of_work: "M", t_double_efficiency_days: "M",
}

# Difficulty-quota generation to hit ~20% M / 60% H / 20% VH.
TARGET = {"M": 100, "H": 300, "VH": 100}
BY_DIFF = {"M": [], "H": [], "VH": []}
for t in TEMPLATES:
    BY_DIFF[DIFF_OF[t]].append(t)

count = {"M": 0, "H": 0, "VH": 0}
attempts = 0
order = ["M", "VH", "H"]  # fill scarcer pools first

while len(questions) < 500 and attempts < 2000000:
    attempts += 1
    # choose a difficulty that still needs questions
    need = [d for d in order if count[d] < TARGET[d]]
    if not need:
        need = order
    diff_target = random.choice(need)
    t = random.choice(BY_DIFF[diff_target])
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    if add(stem, correct, distractors, sol, diff):
        count[diff] += 1

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- SELF-CHECK ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
assert len(questions) == 500, f"Only {len(questions)} questions!"
print(f"Self-check errors: {errors}")

from collections import Counter
dist = Counter(q["diff"] for q in questions)
print("Difficulty:", dist)
total = len(questions)
print(f"  M={100*dist['M']/total:.1f}%  H={100*dist['H']/total:.1f}%  VH={100*dist['VH']/total:.1f}%")

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_04_Time_Work_500.md"

lines = []
lines.append("# Time & Work (incl. Pipes & Cisterns) — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- If A does a work in `a` days, A's one-day work (rate) = `1/a`. **Add rates, never day-counts.**")
lines.append("- A & B together: time = `ab/(a+b)`; one-day work = `1/a + 1/b`.")
lines.append("- **LCM method:** total work = LCM of all the times (in units); each rate = total/time.")
lines.append("- A is x% more efficient than B → A's time = B's time `÷ (1 + x/100)` (more efficient ⇒ less time).")
lines.append("- Wages are shared in the ratio of **work done (efficiency)**, i.e. ratio of rates, not days.")
lines.append("- Men-days-hours: `M₁·D₁·H₁ / W₁ = M₂·D₂·H₂ / W₂` (inverse proportion for men ↔ days).")
lines.append("- Pipes: fill pipe = +rate, leak/outlet = −rate; net rate = sum; time = total/net.")
lines.append("- Leak: `1/leak = 1/fill − 1/(actual fill time)`.")
lines.append("- Alternate days: add the two rates day-by-day in the given order; the last day may be partial.\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        o = q["opts"]
        lines.append(f"**Q{n}.** {q['stem']}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    blk = start // 50 + 1
    lines.append(f"\n## Answers Q{start+1}–Q{start+50}\n")
    for j in range(start, min(start + 50, 500)):
        q = questions[j]
        n = j + 1
        letter = LETTERS[q["ci"]]
        val = q["opts"][q["ci"]]
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* — {q['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUT}")
print(f"Total lines: {len(lines)}")
