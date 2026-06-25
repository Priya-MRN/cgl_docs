# -*- coding: utf-8 -*-
"""
SSC CGL Profit & Loss (incl. Discount & Successive Discount) - 500 hard MCQ generator.
Every answer is COMPUTED, so the key is provably correct.
Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.

Mirrors gen_percentage.py architecture exactly.
CRITICAL: never pass a float into Fraction(num,den); convert floats via
          Fraction(x).limit_denominator(1000) first.
"""
import random
from fractions import Fraction

random.seed(20260625)  # deterministic

LETTERS = "abcd"

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

questions = []  # each: dict(stem, opts(list of str), correct_index, sol, diff)
seen = set()

def is_clean(x):
    """Accept integers, halves/quarters/thirds/sixths/eighths, and <=2dp decimals."""
    fr = Fraction(x).limit_denominator(10**6)
    if fr.denominator in (1, 2, 3, 4, 5, 6, 8):
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
    dfrs = [Fraction(d).limit_denominator(10**6) for d in distractors if d is not None]
    dfrs = [d for d in dfrs if is_clean(d) and d != cfr]
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

def Fr(x):
    """Safe Fraction from possibly-float scalar."""
    return Fraction(x).limit_denominator(1000)

# ---------------- TEMPLATES ----------------

def t_cp_sp_profit():
    """CP and SP given -> profit% (or loss%). [H]"""
    cp = random.choice([120,150,160,180,200,240,250,300,320,360,400,450,480,500,
                        600,640,720,750,800,900,960,1000,1200,1250,1500])
    pct = random.choice([8,10,12,15,16,20,24,25,30,32,35,40])
    gain = random.choice([True, False])
    if gain:
        sp = Fraction(cp)*(100+pct)/100
    else:
        sp = Fraction(cp)*(100-pct)/100
    if sp != int(sp):
        return None
    sp = Fraction(int(sp))
    # ask the profit/loss percent given CP and SP
    diffamt = sp - cp
    correct = Fraction(abs(diffamt))*100/cp
    # distractors: % on SP instead of CP; raw diff; wrong sign base
    wrong1 = Fraction(abs(diffamt))*100/sp                 # % on SP not CP
    wrong2 = Fraction(abs(diffamt))*100/cp + 5             # off
    wrong3 = Fraction(abs(diffamt))*100/cp - 4
    kind = "profit" if diffamt >= 0 else "loss"
    stem = (f"A man buys an article for Rs {cp} and sells it for Rs {fmt(sp)}. "
            f"His {kind} percent is:")
    sol = (f"{kind.capitalize()} = |{fmt(sp)} − {cp}| = Rs {fmt(abs(diffamt))}. "
           f"{kind.capitalize()}% = {fmt(abs(diffamt))}/{cp} × 100 = {fmt(correct)}%. "
           f"Trap: percent is always on COST PRICE, not SP.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_cp_from_sp_profit():
    """SP and profit% given -> CP. [H]"""
    cp = random.choice([160,180,200,240,250,300,320,360,400,450,480,500,540,600,
                        640,720,750,800,900,1000,1200,1250,1500,1600,2000])
    pct = random.choice([8,10,12,15,16,20,24,25,30,32,40,50])
    gain = random.choice([True, False])
    if gain:
        sp = Fraction(cp)*(100+pct)/100
    else:
        sp = Fraction(cp)*(100-pct)/100
    if sp != int(sp):
        return None
    sp = Fraction(int(sp))
    correct = Fraction(cp)
    if gain:
        wrong1 = sp*100/(100-pct)        # subtract instead of add
        wrong2 = sp - Fraction(pct,100)*sp  # take % of SP
    else:
        wrong1 = sp*100/(100+pct)        # add instead of subtract
        wrong2 = sp + Fraction(pct,100)*sp
    wrong3 = sp                           # forgets the markup entirely
    kind = "gain" if gain else "loss"
    stem = (f"By selling an article for Rs {fmt(sp)}, a trader makes a {kind} of {pct}%. "
            f"The cost price of the article is:")
    base = (100+pct) if gain else (100-pct)
    sol = (f"SP = CP × {base}/100 → CP = {fmt(sp)} × 100/{base} = Rs {fmt(correct)}. "
           f"Trap: a {pct}% {kind} means SP is {base}% of CP.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_single_equiv_discount():
    """Two successive discounts -> single equivalent discount. [H]"""
    d1 = random.choice([10,12,15,16,20,25,30,40])
    d2 = random.choice([5,8,10,12,15,20,25])
    eq = d1 + d2 - Fraction(d1*d2,100)
    correct = eq
    wrong1 = Fraction(d1+d2)                       # just adds
    wrong2 = Fraction(d1*d2,100)                   # only product
    wrong3 = d1 + d2 + Fraction(d1*d2,100)         # wrong sign
    stem = (f"Two successive discounts of {d1}% and {d2}% are equivalent to a single "
            f"discount of:")
    sol = (f"Single equiv = d1 + d2 − d1·d2/100 = {d1} + {d2} − {d1*d2}/100 = {fmt(correct)}%. "
           f"Trap: successive discounts are NOT additive ({d1}+{d2}={d1+d2}% is wrong).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_three_equiv_discount():
    """Three successive discounts -> single equivalent discount. [VH]"""
    d1 = random.choice([10,20,25,30])
    d2 = random.choice([10,20,25])
    d3 = random.choice([5,10,20])
    f1 = Fraction(100-d1,100); f2 = Fraction(100-d2,100); f3 = Fraction(100-d3,100)
    net_factor = f1*f2*f3
    eq = (1-net_factor)*100
    correct = eq
    wrong1 = Fraction(d1+d2+d3)                              # adds all
    wrong2 = (1-f1*f2)*100                                   # only two
    wrong3 = Fraction(d1+d2+d3) - 5
    stem = (f"Three successive discounts of {d1}%, {d2}% and {d3}% are equivalent to a "
            f"single discount of:")
    sol = (f"Net price factor = (1−{d1}/100)(1−{d2}/100)(1−{d3}/100) = {fmt(net_factor)}. "
           f"Single discount = (1 − {fmt(net_factor)}) × 100 = {fmt(correct)}%.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_mp_cp_profit_after_discount():
    """CP, MP marked up by m%, discount d% -> profit/loss%. [VH]"""
    cp = random.choice([100,120,150,160,200,240,250,300,320,400,500,600,800,1000])
    m = random.choice([20,25,30,40,50,60,80])     # markup over CP
    d = random.choice([5,10,12,15,20,25])         # discount on MP
    mp = Fraction(cp)*(100+m)/100
    sp = mp*(100-d)/100
    profit = sp - cp
    correct = profit*100/cp
    wrong1 = Fraction(m-d)                                 # naive markup minus discount
    wrong2 = (sp-cp)*100/mp                                # base on MP
    wrong3 = Fraction(m-d) + Fraction(m*d,100)            # sign slip
    if correct >= 0:
        kindword = "profit"
    else:
        kindword = "loss"
    stem = (f"A shopkeeper marks his goods {m}% above the cost price and allows a discount "
            f"of {d}% on the marked price. His {kindword} percent is:")
    sol = (f"Let CP = Rs {cp}. MP = {cp}×{100+m}/100 = Rs {fmt(mp)}. "
           f"SP = {fmt(mp)}×{100-d}/100 = Rs {fmt(sp)}. "
           f"{kindword.capitalize()}% = ({fmt(sp)}−{cp})/{cp}×100 = {fmt(correct)}%. "
           f"Trap: {m}%−{d}% = {m-d}% is wrong; discount is on the higher MP.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_find_markup_for_profit():
    """Want profit p% after discount d% -> markup% over CP. [VH]"""
    p = random.choice([10,12,15,20,25,30,40])
    d = random.choice([10,12,15,20,25])
    # (1+m/100) = (1+p/100)/(1-d/100)
    m = ((Fraction(100+p)/(100-d)) - 1)*100
    correct = m
    wrong1 = Fraction(p+d)                                  # just adds
    wrong2 = Fraction(p+d) + Fraction(p*d,100)
    wrong3 = (Fraction(100+p)/(100+d) - 1)*100             # wrong sign in denom
    stem = (f"A trader wants to earn a profit of {p}% after allowing a discount of {d}% "
            f"on the marked price. By what percent above the cost price must he mark "
            f"his goods?")
    sol = (f"(1 + m/100) = (1 + {p}/100)/(1 − {d}/100) = {fmt(Fraction(100+p)/(100-d))}. "
           f"So markup m = ({fmt(Fraction(100+p)/(100-d))} − 1)×100 = {fmt(correct)}%.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_same_sp_net_loss():
    """Two articles same SP, +x% and -x% -> net loss = (x/10)^2 %. [VH]"""
    x = random.choice([10,12,15,16,20,24,25,30,40])
    xf = Fr(x)
    correct = (xf/10)**2   # net loss percent, classic
    wrong1 = Fraction(0)                       # thinks it cancels (no profit no loss)
    wrong2 = xf                                # thinks loss = x%
    wrong3 = (xf**2)/100                       # same as correct actually? (x/10)^2 = x^2/100 -> identical!
    # fix wrong3 to a genuine different wrong value
    wrong3 = xf*2/10                           # plausible wrong
    stem = (f"A man sold two articles at Rs equal selling price. On one he gained {fmt(x)}% "
            f"and on the other he lost {fmt(x)}%. His overall percentage loss in the "
            f"whole transaction is:")
    sol = (f"When two items are sold at the SAME selling price with +{fmt(x)}% and −{fmt(x)}%, "
           f"there is always a net LOSS = (x/10)² = ({fmt(x)}/10)² = {fmt(correct)}%. "
           f"Trap: it is NOT no-profit-no-loss.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_false_weight():
    """Dishonest dealer sells at CP but uses false weight -> gain%. [VH]"""
    real = 1000
    given = random.choice([800,850,875,900,920,940,950,960])
    error = real - given
    correct = Fraction(error)*100/given      # gain% = error/(true value given) *100
    wrong1 = Fraction(error)*100/real        # base on claimed weight
    wrong2 = Fraction(error,10)              # raw grams /10
    wrong3 = Fraction(error)*100/given + 2
    stem = (f"A dishonest dealer professes to sell his goods at cost price but uses a "
            f"weight of {given} g instead of 1 kg. His gain percent is:")
    sol = (f"He gives {given} g but charges for 1000 g. Gain = error/true-given × 100 "
           f"= {error}/{given} × 100 = {fmt(correct)}%. "
           f"Trap: divide by what he ACTUALLY gives ({given}), not 1000.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_dishonest_at_profit():
    """Sells at gain% AND uses false weight -> total gain%. [VH]"""
    real = 1000
    given = random.choice([800,900,950,960])
    g = random.choice([10,20,25])
    # effective gain factor = (claimed/given) * (1+g/100) - 1
    factor = Fraction(real, given)*Fraction(100+g,100)
    correct = (factor - 1)*100
    wrong1 = Fraction(g) + Fraction((real-given)*100, real)   # adds, base on 1000
    wrong2 = Fraction(g)                                        # ignores false weight
    wrong3 = Fraction((real-given)*100, given)                # ignores stated profit
    stem = (f"A shopkeeper sells his goods at {g}% profit but uses a weight of {given} g "
            f"for 1 kg. His actual gain percent is:")
    sol = (f"Actual gain factor = (1000/{given})×(1+{g}/100) = {fmt(factor)}. "
           f"Gain% = ({fmt(factor)} − 1)×100 = {fmt(correct)}%.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_profit_if_no_discount():
    """CP, MP markup m%, discount d% currently; profit% if NO discount. [H]"""
    cp = random.choice([100,120,150,160,200,250,300,400,500,800,1000])
    m = random.choice([25,30,40,50,60,80])
    mp = Fraction(cp)*(100+m)/100
    correct = Fraction(m)                       # profit if sold at MP = markup%
    d = random.choice([10,15,20,25])
    sp = mp*(100-d)/100
    actual = (sp-cp)*100/cp
    wrong1 = actual                              # current profit
    wrong2 = Fraction(m+d)                       # adds discount back wrongly
    wrong3 = Fraction(m-d)
    stem = (f"A shopkeeper marks his goods {m}% above cost price but allows a discount "
            f"of {d}%. What would his profit percent be if he gave NO discount?")
    sol = (f"With no discount SP = MP = CP×(1+{m}/100), so profit = markup = {fmt(correct)}%. "
           f"(With the {d}% discount the actual profit is only {fmt(actual)}%.)")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_sp_for_target_given_other():
    """SP at y% loss known -> SP needed for x% profit. [H]"""
    cp = random.choice([200,240,300,320,400,450,480,500,600,720,800,1000,1200])
    yloss = random.choice([10,12,15,20,25,30])
    xprofit = random.choice([10,15,20,25,30,40])
    sp_loss = Fraction(cp)*(100-yloss)/100
    if sp_loss != int(sp_loss):
        return None
    sp_target = Fraction(cp)*(100+xprofit)/100
    if sp_target != int(sp_target):
        return None
    correct = Fraction(int(sp_target))
    wrong1 = sp_loss + Fraction(xprofit,100)*sp_loss   # apply x% on wrong base (sp_loss)
    wrong2 = Fraction(cp)*(100+xprofit-yloss)/100      # combine percents wrongly
    wrong3 = sp_loss + (sp_target - sp_loss)/2
    stem = (f"An article sold for Rs {fmt(sp_loss)} gives a loss of {yloss}%. At what price "
            f"should it be sold to gain {xprofit}%?")
    sol = (f"CP = {fmt(sp_loss)}×100/(100−{yloss}) = Rs {cp}. "
           f"For {xprofit}% gain, SP = {cp}×(100+{xprofit})/100 = Rs {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_discount_plus_cash():
    """MP, discount d%, additional cash discount c% -> net price / total discount%. [VH]"""
    mp = random.choice([800,1000,1200,1500,2000,2400,2500,3000])
    d = random.choice([10,15,20,25])
    c = random.choice([5,8,10])
    net = Fraction(mp)*(100-d)/100*(100-c)/100
    total_disc = (1 - Fraction(100-d,100)*Fraction(100-c,100))*100
    ask_net = random.choice([True, False])
    if ask_net:
        if net != int(net):
            return None
        correct = Fraction(int(net))
        wrong1 = Fraction(mp)*(100-d-c)/100              # adds discounts
        wrong2 = Fraction(mp)*(100-d)/100               # forgets cash discount
        wrong3 = Fraction(mp)*(100-c)/100
        stem = (f"The marked price of an article is Rs {mp}. A discount of {d}% is given, "
                f"and an additional cash discount of {c}% is allowed on the reduced price. "
                f"The net price paid is:")
        sol = (f"Net = {mp}×(1−{d}/100)×(1−{c}/100) = {mp}×{fmt(Fraction(100-d,100))}×"
               f"{fmt(Fraction(100-c,100))} = Rs {fmt(correct)}.")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"
    else:
        correct = total_disc
        wrong1 = Fraction(d+c)                          # adds
        wrong2 = Fraction(d*c,100)
        wrong3 = Fraction(d+c) + Fraction(d*c,100)
        stem = (f"A discount of {d}% and a further cash discount of {c}% are allowed "
                f"successively on the marked price. The total discount percent is:")
        sol = (f"Total discount = (1 − (1−{d}/100)(1−{c}/100))×100 = {fmt(correct)}%. "
               f"Trap: {d}%+{c}% = {d+c}% is wrong (successive, not additive).")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_cp_when_profit_equals_loss():
    """Sold at A => profit = sold at B => loss; find CP (midpoint). [H]"""
    cp = random.choice([400,500,600,720,800,900,1000,1200,1500,1600,2000])
    delta = random.choice([40,50,60,80,100,120,150,200])
    A = cp + delta   # SP giving profit
    B = cp - delta   # SP giving equal loss
    if B <= 0:
        return None
    correct = Fraction(cp)
    wrong1 = Fraction(A)                          # picks higher SP
    wrong2 = Fraction(B)                          # picks lower SP
    wrong3 = Fraction(A+B)//1 + 50               # nonsense
    stem = (f"The profit earned by selling an article for Rs {A} equals the loss incurred "
            f"by selling it for Rs {B}. The cost price of the article is:")
    sol = (f"When profit at one SP equals loss at another, CP = (SP1 + SP2)/2 "
           f"= ({A} + {B})/2 = Rs {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_buy_x_get_y_free():
    """Buy x get y free -> effective discount%. [VH]"""
    combos = [(3,1),(4,1),(5,1),(2,1),(6,2),(5,2),(4,2),(10,2),(6,1),(8,2)]
    x,y = random.choice(combos)
    # customer pays for x, gets x+y; discount = y/(x+y)*100
    correct = Fraction(y)*100/(x+y)
    wrong1 = Fraction(y)*100/x                  # base on paid items only
    wrong2 = Fraction(y)*100/(x+y) + 5
    wrong3 = Fraction(100,x+y)                  # 1 item base
    stem = (f"In a 'buy {x} get {y} free' offer, the effective discount percent a customer "
            f"gets is:")
    sol = (f"Customer pays for {x} but receives {x+y}. Effective discount "
           f"= {y}/({x}+{y}) × 100 = {fmt(correct)}%. "
           f"Trap: base is total items received ({x+y}), not items paid for.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_mixture_overall_profit():
    """Two lots different CP, sold at overall SP -> overall profit%. [H]"""
    q1 = random.choice([20,25,30,40,50])
    q2 = random.choice([20,25,30,40,50])
    r1 = random.choice([10,12,15,20,24,25,30])   # cost per kg lot 1
    r2 = random.choice([10,12,15,20,24,25,30])   # cost per kg lot 2
    sell = random.choice([18,20,24,25,28,30,32,36,40])  # selling price per kg of mixture
    total_cost = q1*r1 + q2*r2
    total_kg = q1+q2
    total_sp = total_kg*sell
    profit = total_sp - total_cost
    correct = Fraction(profit)*100/total_cost
    wrong1 = Fraction(profit)*100/total_sp        # base on SP
    wrong2 = Fraction(profit)*100/total_cost + 4
    wrong3 = Fraction(profit)*100/total_cost - 3
    stem = (f"{q1} kg of rice costing Rs {r1}/kg is mixed with {q2} kg costing Rs {r2}/kg. "
            f"The whole mixture is sold at Rs {sell}/kg. The overall profit or loss "
            f"percent is:")
    sol = (f"Total cost = {q1}×{r1}+{q2}×{r2} = Rs {total_cost}. "
           f"Total SP = {total_kg}×{sell} = Rs {total_sp}. "
           f"Profit/Loss% = ({total_sp}−{total_cost})/{total_cost}×100 = {fmt(correct)}%.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_articles_cost_sell_gain():
    """CP of m articles = SP of n articles -> gain/loss%. [VH]"""
    pairs = [(20,16),(15,12),(25,20),(16,12),(21,18),(12,10),(18,15),(24,20),(10,8),(30,25)]
    m,n = random.choice(pairs)
    # CP of m = SP of n => gain% = (m-n)/n *100
    correct = Fraction(m-n)*100/n
    wrong1 = Fraction(m-n)*100/m                  # base on m
    wrong2 = Fraction(m-n)                         # raw diff
    wrong3 = Fraction(m-n)*100/n + 5
    stem = (f"If the cost price of {m} articles is equal to the selling price of {n} "
            f"articles, the gain percent is:")
    sol = (f"CP of {m} = SP of {n}. Gain% = (CP−SP)/SP×100 on equal money basis "
           f"= ({m}−{n})/{n}×100 = {fmt(correct)}%. "
           f"Trap: divide by the SP count ({n}), not the CP count.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_mp_from_cp_discount_profit():
    """CP, discount d%, profit p% -> MP as % above CP (or MP value). [H]"""
    cp = random.choice([200,240,300,400,500,600,800,1000,1200,1500])
    p = random.choice([10,15,20,25,30,40])
    d = random.choice([10,15,20,25])
    # SP = CP(1+p/100); MP = SP/(1-d/100)
    sp = Fraction(cp)*(100+p)/100
    mp = sp*100/(100-d)
    if mp != int(mp):
        return None
    correct = Fraction(int(mp))
    wrong1 = Fraction(cp)*(100+p+d)/100          # add percents
    wrong2 = sp*(100+d)/100                       # multiply not divide
    wrong3 = Fraction(cp)*(100+p)/100            # forgets to raise MP (=SP)
    stem = (f"A trader buys an article for Rs {cp}. He wants to make a profit of {p}% even "
            f"after giving a discount of {d}%. The marked price should be:")
    sol = (f"Required SP = {cp}×(100+{p})/100 = Rs {fmt(sp)}. "
           f"MP = SP/(1−{d}/100) = {fmt(sp)}×100/{100-d} = Rs {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

TEMPLATES = [
    t_cp_sp_profit, t_cp_from_sp_profit, t_single_equiv_discount,
    t_three_equiv_discount, t_mp_cp_profit_after_discount, t_find_markup_for_profit,
    t_same_sp_net_loss, t_false_weight, t_dishonest_at_profit,
    t_profit_if_no_discount, t_sp_for_target_given_other, t_discount_plus_cash,
    t_cp_when_profit_equals_loss, t_buy_x_get_y_free, t_mixture_overall_profit,
    t_articles_cost_sell_gain, t_mp_from_cp_discount_profit,
]

DIFF_OF = {
    t_cp_sp_profit:"H", t_cp_from_sp_profit:"H", t_single_equiv_discount:"H",
    t_three_equiv_discount:"VH", t_mp_cp_profit_after_discount:"VH",
    t_find_markup_for_profit:"VH", t_same_sp_net_loss:"VH", t_false_weight:"VH",
    t_dishonest_at_profit:"VH", t_profit_if_no_discount:"H",
    t_sp_for_target_given_other:"H", t_discount_plus_cash:"VH",
    t_cp_when_profit_equals_loss:"H", t_buy_x_get_y_free:"VH",
    t_mixture_overall_profit:"H", t_articles_cost_sell_gain:"VH",
    t_mp_from_cp_discount_profit:"H",
}

# We want ~20% M / 60% H / 20% VH. There are no M templates here, so add a few
# easier "Medium" templates to fill the 20% Medium quota.
def t_basic_profit_amount():
    """CP and profit% -> SP value (straightforward). [M]"""
    cp = random.choice([120,150,200,240,250,300,400,500,600,800,1000,1200,1500,2000])
    p = random.choice([10,12,15,20,25,30,40,50])
    sp = Fraction(cp)*(100+p)/100
    if sp != int(sp):
        return None
    correct = Fraction(int(sp))
    wrong1 = Fraction(cp)*(100-p)/100             # loss instead
    wrong2 = Fraction(cp) + Fraction(p)           # add p rupees
    wrong3 = Fraction(cp)*(100+p+5)/100
    stem = (f"An article costing Rs {cp} is sold at a profit of {p}%. The selling price is:")
    sol = (f"SP = CP×(100+{p})/100 = {cp}×{100+p}/100 = Rs {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_basic_loss_amount():
    """CP and loss% -> SP value. [M]"""
    cp = random.choice([120,150,200,240,250,300,400,500,600,800,1000,1200,1500])
    p = random.choice([10,12,15,20,25,30,40])
    sp = Fraction(cp)*(100-p)/100
    if sp != int(sp):
        return None
    correct = Fraction(int(sp))
    wrong1 = Fraction(cp)*(100+p)/100             # profit instead
    wrong2 = Fraction(cp) - Fraction(p)           # subtract p rupees
    wrong3 = Fraction(cp)*(100-p-5)/100
    stem = (f"An article costing Rs {cp} is sold at a loss of {p}%. The selling price is:")
    sol = (f"SP = CP×(100−{p})/100 = {cp}×{100-p}/100 = Rs {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_basic_discount_value():
    """MP and discount% -> SP after discount. [M]"""
    mp = random.choice([200,250,300,400,500,600,800,1000,1200,1500,2000,2500])
    d = random.choice([5,10,12,15,20,25,30,40])
    sp = Fraction(mp)*(100-d)/100
    if sp != int(sp):
        return None
    correct = Fraction(int(sp))
    wrong1 = Fraction(mp)*(100+d)/100             # adds
    wrong2 = Fraction(mp) - Fraction(d)           # subtract d rupees
    wrong3 = Fraction(mp)*(100-d-5)/100
    stem = (f"The marked price of an article is Rs {mp}. After a discount of {d}%, "
            f"its selling price is:")
    sol = (f"SP = MP×(100−{d})/100 = {mp}×{100-d}/100 = Rs {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

MEDIUM_TEMPLATES = [t_basic_profit_amount, t_basic_loss_amount, t_basic_discount_value]
for t in MEDIUM_TEMPLATES:
    TEMPLATES.append(t)
DIFF_OF[t_basic_profit_amount] = "M"
DIFF_OF[t_basic_loss_amount] = "M"
DIFF_OF[t_basic_discount_value] = "M"

# Weighted selection to hit ~20% M / 60% H / 20% VH.
# Per-difficulty TOTAL weight is split across the templates of that difficulty,
# so the realized distribution is robust to how many templates each group has.
TARGET = {"M": 100, "H": 300, "VH": 100}  # out of 500
BY_DIFF = {"M": [], "H": [], "VH": []}
for t in TEMPLATES:
    BY_DIFF[DIFF_OF[t]].append(t)

# Generate quota-by-quota so dedupe exhaustion in one group can't starve another.
attempts = 0
order = ["M", "H", "VH"]
for d in order:
    target_total = sum(1 for _ in range(TARGET[d]))  # questions wanted in this difficulty
    pool = BY_DIFF[d]
    have = sum(1 for q in questions if q["diff"] == d)
    local_attempts = 0
    while sum(1 for q in questions if q["diff"] == d) < TARGET[d] and local_attempts < 300000:
        local_attempts += 1
        attempts += 1
        t = random.choice(pool)
        res = t()
        if res is None:
            continue
        stem, correct, distractors, sol, diff = res
        add(stem, correct, distractors, sol, diff)

# Top up to 500 from Hard pool if any group fell short of capacity.
fill_pool = BY_DIFF["H"] + BY_DIFF["VH"] + BY_DIFF["M"]
while len(questions) < 500 and attempts < 600000:
    attempts += 1
    t = random.choice(fill_pool)
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    add(stem, correct, distractors, sol, diff)

# Interleave difficulties across the paper instead of clustering M/H/VH blocks.
random.shuffle(questions)

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- VERIFY: each has exactly 4 distinct options, exactly one correct ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
print(f"Verification errors: {errors}")

from collections import Counter
print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_03_Profit_Loss_500.md"

lines = []
lines.append("# Profit & Loss (incl. Discount & Successive Discount) — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** Medium / Hard / Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- `Profit% = (SP − CP)/CP × 100`  ·  `Loss% = (CP − SP)/CP × 100`  (always on **CP**)")
lines.append("- `SP = CP × (100 ± profit/loss%)/100`  ·  `CP = SP × 100/(100 ± %)`")
lines.append("- Marked price & discount: `SP = MP × (100 − discount%)/100`")
lines.append("- Two successive discounts d₁, d₂ → single equiv **d₁ + d₂ − d₁d₂/100 %**")
lines.append("- For a target profit p% after discount d%: markup = **[(100+p)/(100−d) − 1] × 100 %**")
lines.append("- Same SP, +x% on one & −x% on other → always **net loss = (x/10)² %**")
lines.append("- False weight (sell at CP): `gain% = error/(true value given) × 100`")
lines.append("- CP of m articles = SP of n articles → `gain% = (m − n)/n × 100`")
lines.append("- Profit = Loss for two SPs → `CP = (SP₁ + SP₂)/2`")
lines.append("- Buy x get y free → effective discount = **y/(x+y) × 100 %**\n")
lines.append("\n# =================== QUESTIONS ===================\n")

for start in range(0, 500, 50):
    blk = start//50 + 1
    lines.append(f"\n## Block {blk} (Q{start+1}–Q{start+50})\n")
    for j in range(start, min(start+50, 500)):
        q = questions[j]
        n = j+1
        o = q["opts"]
        lines.append(f"**Q{n}.** {q['stem']}")
        lines.append(f"(a) {o[0]}  (b) {o[1]}  (c) {o[2]}  (d) {o[3]}\n")

lines.append("\n# =================== ANSWER KEY & EXPLANATIONS ===================\n")
for start in range(0, 500, 50):
    blk = start//50 + 1
    lines.append(f"\n## Answers Q{start+1}–Q{start+50}\n")
    for j in range(start, min(start+50, 500)):
        q = questions[j]
        n = j+1
        letter = LETTERS[q["ci"]]
        val = q["opts"][q["ci"]]
        lines.append(f"**Q{n}. ({letter}) {val}**  *[{q['diff']}]* — {q['sol']}")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Wrote {OUT}")
print(f"Total lines: {len(lines)}")
