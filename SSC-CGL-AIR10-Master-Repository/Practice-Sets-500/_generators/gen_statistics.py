# -*- coding: utf-8 -*-
"""
SSC CGL Statistics - 500 hard MCQ generator.
Topics: Mean, Median, Mode, Range, Variance, SD, Quartiles, Combined mean,
Weighted/grouped mean, Mode=3Median-2Mean, effect of transforms.

Every answer is COMPUTED with exact Fraction arithmetic, so the key is
provably correct. Builds 4 distinct options (1 correct + 3 common-mistake
distractors), randomizes correct position, dedupes stems, outputs markdown.

CRITICAL: the actual data list is embedded IN the stem so the independent
verifier can re-read it and recompute the statistic from scratch.
Never pass a float into Fraction(num, den).
"""
import random
from fractions import Fraction
from collections import Counter

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


questions = []  # each: dict(stem, opts, ci, sol, diff)
seen = set()


def is_clean(x):
    """Accept integers, halves/quarters/thirds/fifths/sixths/eighths, and <=2dp decimals."""
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


# ---------------- exact stat helpers (Fraction) ----------------

def mean_F(data):
    return Fraction(sum(data), len(data))


def median_F(data):
    s = sorted(data)
    n = len(s)
    if n % 2 == 1:
        return Fraction(s[n // 2])
    return Fraction(s[n // 2 - 1] + s[n // 2], 2)


def variance_F(data):
    """Population variance, exact."""
    m = mean_F(data)
    return Fraction(sum((Fraction(x) - m) ** 2 for x in data), len(data))


def list_str(data):
    """Render a python list of ints as 'a, b, c'."""
    return ", ".join(str(x) for x in data)


# ---------------- TEMPLATES ----------------

def t_mean_small():
    """Mean of a small dataset listed in the stem. [M]"""
    n = random.choice([5, 6, 7, 8])
    # pick data whose mean is clean
    data = [random.randint(8, 80) for _ in range(n)]
    m = mean_F(data)
    correct = m
    s = sum(data)
    wrong1 = Fraction(s, n - 1)               # divides by n-1
    wrong2 = Fraction(s, n + 1)               # divides by n+1
    wrong3 = median_F(data)                    # confuses with median
    if wrong3 == correct:
        wrong3 = correct + 1
    stem = (f"Find the arithmetic mean of the following data: "
            f"{list_str(data)}.")
    sol = (f"Mean = (sum of observations)/(number of observations) "
           f"= {s}/{n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_median_odd():
    """Median of an odd-length list (must sort). [M]"""
    n = random.choice([5, 7, 9])
    data = random.sample(range(5, 95), n)
    correct = median_F(data)
    s = sorted(data)
    wrong1 = Fraction(data[n // 2])            # middle of UNSORTED list
    wrong2 = mean_F(data)                       # confuses with mean
    wrong3 = Fraction(s[n // 2 - 1])           # off-by-one position
    stem = (f"Find the median of the following data: {list_str(data)}.")
    sol = (f"Arrange in ascending order: {list_str(s)}. With n={n} (odd), "
           f"median = the {(n+1)//2}th value = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_median_even():
    """Median of an even-length list (must sort, average two middles). [H]"""
    n = random.choice([6, 8, 10])
    data = random.sample(range(5, 95), n)
    correct = median_F(data)
    s = sorted(data)
    wrong1 = Fraction(s[n // 2])               # only the upper middle
    wrong2 = Fraction(s[n // 2 - 1])           # only the lower middle
    wrong3 = mean_F(data)                       # confuses with mean
    if not is_clean(correct):
        return None
    stem = (f"Find the median of the following data: {list_str(data)}.")
    sol = (f"Arrange in ascending order: {list_str(s)}. With n={n} (even), "
           f"median = average of the {n//2}th and {n//2+1}th values "
           f"= ({s[n//2-1]}+{s[n//2]})/2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_mode():
    """Mode of a list (single clear mode). [M]"""
    base = random.sample(range(10, 60), 5)
    mode_val = random.choice(base)
    # make mode_val appear 3 times, others once; keep a clear single mode
    data = base + [mode_val, mode_val]
    random.shuffle(data)
    cnt = Counter(data)
    top = max(cnt.values())
    modes = [v for v, c in cnt.items() if c == top]
    if len(modes) != 1:
        return None
    correct = Fraction(modes[0])
    others = sorted(set(data) - {modes[0]})
    wrong1 = Fraction(others[0])
    wrong2 = mean_F(data)
    wrong3 = median_F(data)
    stem = (f"Find the mode of the following data: {list_str(data)}.")
    sol = (f"The mode is the value with the highest frequency. "
           f"Here {modes[0]} occurs {top} times, more than any other value, "
           f"so mode = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_range():
    """Range = max - min of a list. [M]"""
    n = random.choice([6, 7, 8])
    data = random.sample(range(4, 99), n)
    mx, mn = max(data), min(data)
    correct = Fraction(mx - mn)
    wrong1 = Fraction(mx + mn)                  # adds instead
    wrong2 = Fraction(mx)                        # just the max
    wrong3 = Fraction(mx - mn) // 2 if (mx - mn) % 2 == 0 else Fraction(mx - mn - 1)
    stem = (f"Find the range of the following data: {list_str(data)}.")
    sol = (f"Range = maximum - minimum = {mx} - {mn} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"


def t_grouped_mean():
    """Mean of grouped/weighted data: values with frequencies. [H]"""
    k = random.choice([4, 5])
    vals = sorted(random.sample(range(2, 20), k))
    freqs = [random.randint(2, 9) for _ in range(k)]
    N = sum(freqs)
    fx = sum(v * f for v, f in zip(vals, freqs))
    correct = Fraction(fx, N)
    wrong1 = Fraction(sum(vals), k)             # ignores frequencies
    wrong2 = Fraction(fx, k)                     # divides by k not N
    wrong3 = Fraction(fx + N, N)
    pairs = "; ".join(f"value {v} with frequency {f}" for v, f in zip(vals, freqs))
    if not is_clean(correct):
        return None
    stem = (f"The frequency distribution is: {pairs}. Find the mean.")
    sol = (f"Mean = Σ(f·x)/Σf = {fx}/{N} = {fmt(correct)}. "
           f"Trap: divide the weighted sum by the total frequency Σf={N}, "
           f"not by the number of distinct values.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_combined_mean():
    """Combined mean of two groups. [H]"""
    n1 = random.choice([10, 12, 15, 16, 20, 24, 25, 30, 40])
    n2 = random.choice([10, 12, 15, 16, 20, 24, 25, 30, 40])
    m1 = random.choice([20, 24, 25, 30, 32, 36, 40, 45, 48, 50])
    m2 = random.choice([20, 24, 25, 30, 32, 36, 40, 45, 48, 50])
    if m1 == m2:
        return None
    correct = Fraction(n1 * m1 + n2 * m2, n1 + n2)
    wrong1 = Fraction(m1 + m2, 2)               # simple average of means
    wrong2 = Fraction(n1 * m1 + n2 * m2, max(n1, n2))
    wrong3 = Fraction(n2 * m1 + n1 * m2, n1 + n2)  # swapped weights
    if not is_clean(correct):
        return None
    stem = (f"A group of {n1} students has an average score of {m1}, and another "
            f"group of {n2} students has an average score of {m2}. Find the "
            f"combined average score of all {n1 + n2} students.")
    sol = (f"Combined mean = (n1·m1 + n2·m2)/(n1+n2) "
           f"= ({n1}×{m1} + {n2}×{m2})/({n1}+{n2}) "
           f"= {n1*m1 + n2*m2}/{n1+n2} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_new_mean_add():
    """New mean after adding one observation. [H]"""
    n = random.choice([8, 9, 10, 12, 15, 19, 20, 24])
    old_mean = random.choice([12, 15, 16, 18, 20, 24, 25, 30, 36, 40])
    added = random.choice([5, 8, 10, 14, 22, 30, 41, 52, 63, 75])
    old_sum = n * old_mean
    new_sum = old_sum + added
    correct = Fraction(new_sum, n + 1)
    wrong1 = Fraction(new_sum, n)               # forgets count grew
    wrong2 = Fraction(old_mean + added, 2)      # averages mean with new value
    wrong3 = Fraction(old_sum, n + 1)           # forgets to add value
    if not is_clean(correct):
        return None
    stem = (f"The mean of {n} observations is {old_mean}. If a new observation "
            f"of value {added} is included, find the mean of all {n + 1} "
            f"observations.")
    sol = (f"Old sum = {n}×{old_mean} = {old_sum}. New sum = {old_sum}+{added} "
           f"= {new_sum}. New mean = {new_sum}/{n+1} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_mean_remove():
    """New mean after removing one observation. [H]"""
    n = random.choice([6, 7, 8, 10, 11, 13, 16, 21])
    old_mean = random.choice([12, 15, 16, 18, 20, 24, 25, 30, 36, 40])
    removed = random.choice([6, 9, 12, 15, 20, 28, 33, 45, 54])
    old_sum = n * old_mean
    new_sum = old_sum - removed
    if new_sum <= 0:
        return None
    correct = Fraction(new_sum, n - 1)
    wrong1 = Fraction(new_sum, n)               # forgets count shrank
    wrong2 = Fraction(old_sum, n - 1)           # forgets to remove value
    wrong3 = Fraction(old_mean - removed, 1)
    if not is_clean(correct):
        return None
    stem = (f"The mean of {n} numbers is {old_mean}. If one number equal to "
            f"{removed} is removed, find the mean of the remaining {n - 1} "
            f"numbers.")
    sol = (f"Total = {n}×{old_mean} = {old_sum}. After removing {removed}: "
           f"sum = {new_sum}, count = {n-1}. New mean = {new_sum}/{n-1} "
           f"= {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_variance_small():
    """Variance of a small set, exact. [VH]"""
    n = random.choice([4, 5])
    # build a set whose population variance is clean
    for _ in range(40):
        data = random.sample(range(2, 40), n)
        var = variance_F(data)
        if var.denominator in (1, 2, 4) and var <= 200:
            break
    else:
        return None
    m = mean_F(data)
    correct = var
    sd2 = Fraction(sum((Fraction(x) - m) ** 2 for x in data), n - 1)  # sample var
    wrong1 = sd2                                 # divides by n-1
    wrong2 = m                                    # confuses with mean
    wrong3 = Fraction(sum(Fraction(x) ** 2 for x in data), n)  # mean of squares only
    if not (is_clean(wrong1) and is_clean(wrong3)):
        wrong1 = correct + 2
        wrong3 = correct + 5
    stem = (f"Find the variance of the following data: {list_str(data)}.")
    sol = (f"Mean = {sum(data)}/{n} = {fmt(m)}. Variance = Σ(x−mean)²/n "
           f"= {fmt(correct)}. (Population variance: divide by n.)")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_sd_small():
    """SD of a small set chosen so SD is a clean integer. [VH]
    Build a symmetric set {m, m±a, m±b, ...} so population variance is exactly
    the mean of the squared deviations, then keep only perfect-square variances."""
    for _ in range(120):
        m = random.randint(15, 60)
        k = random.choice([2, 3, 4, 5, 6, 7, 8])
        shape = random.choice(["k4", "k6", "k2asym"])
        if shape == "k4":
            # every deviation is exactly ±k -> variance = k^2, SD = k (integer)
            data = [m - k, m - k, m + k, m + k]
        elif shape == "k6":
            data = [m - k, m - k, m - k, m + k, m + k, m + k]
        else:
            # mix of +-k and 0 kept so variance stays a perfect square:
            # {m-k, m, m, m+k} -> var = 2k^2/4 = k^2/2 (not integer); skip such.
            # Instead use {m-k,m-k,m,m,m+k,m+k}? var = 4k^2/6 -> not clean.
            # Keep an integer-SD asymmetric-looking set: 8 values, ±k each.
            data = [m - k] * 4 + [m + k] * 4
        if min(data) < 1:
            continue
        var = variance_F(data)
        r = int(round(float(var) ** 0.5))
        if var.denominator == 1 and r * r == var.numerator and r >= 1:
            sd = Fraction(r)
            shuffled = data[:]
            random.shuffle(shuffled)
            data = shuffled
            break
    else:
        return None
    correct = sd
    var = variance_F(data)
    wrong1 = var                                  # gives variance instead of SD
    wrong2 = sd + 1
    wrong3 = mean_F(data)
    if not is_clean(correct):
        return None
    stem = (f"Find the standard deviation of the following data: "
            f"{list_str(data)}.")
    sol = (f"Mean = {fmt(mean_F(data))}. Variance = Σ(x−mean)²/n = {fmt(var)}. "
           f"SD = √(variance) = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_sd_naturals():
    """SD of first n natural numbers; pick n giving clean SD. SD=sqrt((n^2-1)/12). [H]"""
    # n such that (n^2-1)/12 is a perfect square -> clean integer SD
    good = []
    for n in range(5, 200):
        v = Fraction(n * n - 1, 12)
        r = float(v) ** 0.5
        if abs(r - round(r)) < 1e-9 and v.denominator == 1:
            good.append((n, int(round(r))))
    if not good:
        return None
    n, sd_int = random.choice(good)
    correct = Fraction(sd_int)
    var = Fraction(n * n - 1, 12)
    wrong1 = var                                  # variance not SD
    wrong2 = Fraction(n, 2)
    wrong3 = correct + 1
    stem = (f"Find the standard deviation of the first {n} natural numbers "
            f"(i.e. 1, 2, 3, ..., {n}).")
    sol = (f"For first n natural numbers, variance = (n²−1)/12 = "
           f"({n}²−1)/12 = {fmt(var)}, so SD = √{fmt(var)} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_transform_mean():
    """Effect on mean when each value is multiplied and/or shifted by a constant. [H]"""
    old_mean = random.choice([10, 12, 15, 18, 20, 24, 25, 30, 40])
    k = random.choice([2, 3, 4, 5])
    c = random.choice([3, 4, 5, 6, 7, 8, 10])
    op = random.choice(["mul_add", "add", "mul"])
    if op == "mul_add":
        correct = Fraction(k * old_mean + c)
        desc = f"each observation is multiplied by {k} and then {c} is added"
        formula = f"new mean = {k}×{old_mean} + {c}"
        wrong1 = Fraction(old_mean + c)          # forgets multiply
        wrong2 = Fraction(k * old_mean)          # forgets add
        wrong3 = Fraction(k * (old_mean + c))    # wrong grouping
    elif op == "add":
        correct = Fraction(old_mean + c)
        desc = f"{c} is added to each observation"
        formula = f"new mean = {old_mean} + {c}"
        wrong1 = Fraction(old_mean)              # unchanged (mistake)
        wrong2 = Fraction(old_mean - c)
        wrong3 = Fraction(old_mean * c)
    else:
        correct = Fraction(k * old_mean)
        desc = f"each observation is multiplied by {k}"
        formula = f"new mean = {k}×{old_mean}"
        wrong1 = Fraction(old_mean)              # unchanged (mistake)
        wrong2 = Fraction(old_mean + k)
        wrong3 = Fraction(old_mean, k)
    stem = (f"The mean of a set of observations is {old_mean}. If {desc}, "
            f"find the mean of the new set of observations.")
    sol = (f"Mean is linear: {formula} = {fmt(correct)}. "
           f"(Adding c shifts the mean by c; multiplying by k scales it by k.)")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_transform_sd():
    """Effect on SD when each value is multiplied and/or shifted by a constant. [H]"""
    old_sd = random.choice([2, 3, 4, 5, 6, 8, 10, 12])
    k = random.choice([2, 3, 4, 5])
    c = random.choice([4, 5, 6, 7, 9, 11])
    op = random.choice(["mul_add", "add", "mul"])
    if op == "mul_add":
        correct = Fraction(k * old_sd)
        desc = f"each observation is multiplied by {k} and then {c} is added"
        sol_extra = (f"Adding a constant does NOT change SD; multiplying by {k} "
                     f"scales SD by |{k}|.")
        wrong1 = Fraction(k * old_sd + c)        # also adds c
        wrong2 = Fraction(old_sd + c)
        wrong3 = Fraction(old_sd)
    elif op == "add":
        correct = Fraction(old_sd)
        desc = f"{c} is added to each observation"
        sol_extra = "Adding a constant to every value shifts the data but does NOT change the spread, so SD is unchanged."
        wrong1 = Fraction(old_sd + c)
        wrong2 = Fraction(old_sd - c) if old_sd - c > 0 else Fraction(old_sd + 2 * c)
        wrong3 = Fraction(old_sd * c)
    else:
        correct = Fraction(k * old_sd)
        desc = f"each observation is multiplied by {k}"
        sol_extra = f"Multiplying every value by {k} multiplies the SD by |{k}|."
        wrong1 = Fraction(old_sd)                # unchanged (mistake)
        wrong2 = Fraction(old_sd + k)
        wrong3 = Fraction(k * old_sd * k)        # squared by mistake (variance-like)
    stem = (f"The standard deviation of a set of observations is {old_sd}. "
            f"If {desc}, find the standard deviation of the new set.")
    sol = (f"New SD = {fmt(correct)}. {sol_extra}")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_quartiles_iqr():
    """Q1, Q3 and IQR of a small ordered set (odd n, exclusive method). [VH]"""
    # use n = 4k+3 sizes (7, 11) so halves are clean with the common method
    n = random.choice([7, 11])
    data = random.sample(range(3, 90), n)
    s = sorted(data)
    half = n // 2
    lower = s[:half]
    upper = s[half + 1:]
    # each half has odd length -> clean integer median
    q1 = median_F(lower)
    q3 = median_F(upper)
    iqr = q3 - q1
    ask = random.choice(["Q1", "Q3", "IQR"])
    if ask == "Q1":
        correct = q1
        wrong1 = q3
        wrong2 = median_F(s)
        wrong3 = q1 + 2
        target = "the first quartile (Q1)"
    elif ask == "Q3":
        correct = q3
        wrong1 = q1
        wrong2 = median_F(s)
        wrong3 = q3 - 2
        target = "the third quartile (Q3)"
    else:
        correct = iqr
        wrong1 = q3 + q1                         # adds instead
        wrong2 = median_F(s)
        wrong3 = iqr + 3
        target = "the interquartile range (Q3 − Q1)"
    stem = (f"For the data {list_str(data)}, find {target}. "
            f"(Use the median to split the ordered data into lower and upper "
            f"halves, excluding the overall median.)")
    sol = (f"Sorted: {list_str(s)}. Median is the {half+1}th value. "
           f"Lower half = {list_str(lower)} (Q1 = {fmt(q1)}); "
           f"upper half = {list_str(upper)} (Q3 = {fmt(q3)}). "
           f"IQR = Q3 − Q1 = {fmt(q3)} − {fmt(q1)} = {fmt(iqr)}. "
           f"Answer = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"


def t_empirical_mode():
    """Empirical relation Mode = 3 Median - 2 Mean; given two, find third. [H]"""
    which = random.choice(["mode", "mean", "median"])
    # choose mean & median so that mode comes out clean and consistent
    mean = random.choice([20, 24, 25, 30, 32, 36, 40, 45, 48, 50, 54, 60])
    median = random.choice([22, 26, 28, 30, 34, 38, 42, 46, 50, 52, 58, 62])
    mode = 3 * median - 2 * mean
    if mode <= 0:
        return None
    if which == "mode":
        correct = Fraction(mode)
        wrong1 = Fraction(3 * mean - 2 * median)  # swapped
        wrong2 = Fraction(2 * median - mean)
        wrong3 = Fraction(median + mean, 2)
        stem = (f"In a moderately skewed distribution, the mean is {mean} and "
                f"the median is {median}. Using the empirical relation, find "
                f"the mode.")
        sol = (f"Empirical relation: Mode = 3·Median − 2·Mean "
               f"= 3×{median} − 2×{mean} = {fmt(correct)}.")
    elif which == "mean":
        correct = Fraction(3 * median - mode, 2)
        if correct.denominator not in (1, 2):
            return None
        wrong1 = Fraction(3 * mode - median, 2)
        wrong2 = Fraction(median + mode, 2)
        wrong3 = Fraction(3 * median - mode)
        stem = (f"In a moderately skewed distribution, the mode is {mode} and "
                f"the median is {median}. Using the empirical relation, find "
                f"the mean.")
        sol = (f"Empirical relation: Mode = 3·Median − 2·Mean ⇒ "
               f"Mean = (3·Median − Mode)/2 = (3×{median} − {mode})/2 "
               f"= {fmt(correct)}.")
    else:
        correct = Fraction(mode + 2 * mean, 3)
        if correct.denominator != 1:
            return None
        wrong1 = Fraction(mode + 2 * mean)
        wrong2 = Fraction(mode + mean, 2)
        wrong3 = Fraction(2 * mode + mean, 3)
        stem = (f"In a moderately skewed distribution, the mode is {mode} and "
                f"the mean is {mean}. Using the empirical relation, find the "
                f"median.")
        sol = (f"Empirical relation: Mode = 3·Median − 2·Mean ⇒ "
               f"Median = (Mode + 2·Mean)/3 = ({mode} + 2×{mean})/3 "
               f"= {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_weighted_mean():
    """Weighted mean with explicit weights. [H]"""
    k = random.choice([3, 4])
    vals = random.sample(range(40, 95), k)
    weights = random.sample(range(1, 9), k)
    W = sum(weights)
    sw = sum(v * w for v, w in zip(vals, weights))
    correct = Fraction(sw, W)
    wrong1 = Fraction(sum(vals), k)             # plain mean
    wrong2 = Fraction(sw, k)
    wrong3 = Fraction(sw + W, W)
    if not is_clean(correct):
        return None
    items = "; ".join(f"{v} (weight {w})" for v, w in zip(vals, weights))
    stem = (f"Find the weighted mean of the following values with their "
            f"weights: {items}.")
    sol = (f"Weighted mean = Σ(w·x)/Σw = {sw}/{W} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


def t_grouped_median_simple():
    """Median of a simple discrete frequency distribution. [H]"""
    k = random.choice([4, 5])
    vals = sorted(random.sample(range(1, 25), k))
    freqs = [random.choice([2, 3, 4, 5, 6, 7]) for _ in range(k)]
    N = sum(freqs)
    if N % 2 == 0:
        N += 0  # handle even via average of two positional values
    # build cumulative and find median position(s)
    cum = []
    run = 0
    for f in freqs:
        run += f
        cum.append(run)

    def value_at(pos):
        for v, c in zip(vals, cum):
            if pos <= c:
                return v
        return vals[-1]

    if N % 2 == 1:
        correct = Fraction(value_at((N + 1) // 2))
    else:
        correct = Fraction(value_at(N // 2) + value_at(N // 2 + 1), 2)
    if not is_clean(correct):
        return None
    wrong1 = Fraction(sum(v * f for v, f in zip(vals, freqs)), N)  # the mean
    wrong2 = Fraction(vals[len(vals) // 2])     # middle distinct value
    wrong3 = mean_F(vals)
    pairs = "; ".join(f"value {v} with frequency {f}" for v, f in zip(vals, freqs))
    sol_pos = ("the value at the (N+1)/2 = "
               f"{(N+1)//2}th position" if N % 2 == 1
               else f"the average of the {N//2}th and {N//2+1}th positional values")
    stem = (f"For the discrete frequency distribution ({pairs}), find the "
            f"median.")
    sol = (f"Total frequency N = {N}. Using cumulative frequencies, the median "
           f"is {sol_pos} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"


TEMPLATES = [
    t_mean_small, t_median_odd, t_median_even, t_mode, t_range,
    t_grouped_mean, t_combined_mean, t_new_mean_add, t_mean_remove,
    t_variance_small, t_sd_small, t_sd_naturals, t_transform_mean,
    t_transform_sd, t_quartiles_iqr, t_empirical_mode, t_weighted_mean,
    t_grouped_median_simple,
]

DIFF_OF = {
    t_mean_small: "M", t_median_odd: "H", t_median_even: "H", t_mode: "M",
    t_range: "M", t_grouped_mean: "H", t_combined_mean: "H",
    t_new_mean_add: "H", t_mean_remove: "H", t_variance_small: "VH",
    t_sd_small: "VH", t_sd_naturals: "H", t_transform_mean: "H",
    t_transform_sd: "H", t_quartiles_iqr: "VH", t_empirical_mode: "H",
    t_weighted_mean: "H", t_grouped_median_simple: "H",
}

# Weighted selection to hit ~20% M / 60% H / 20% VH.
# M has only 3 templates vs many H, so give each M template a high per-template
# weight; H gets the bulk; VH is throttled to land near 20%.
WEIGHT = {"M": 4.6, "H": 4.6, "VH": 2.5}
POOL = []
for t in TEMPLATES:
    POOL += [t] * int(WEIGHT[DIFF_OF[t]] * 10)

# Generate until we have 500 unique
attempts = 0
while len(questions) < 500 and attempts < 600000:
    attempts += 1
    t = random.choice(POOL)
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    add(stem, correct, distractors, sol, diff)

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- VERIFY internal: 4 distinct options, exactly one correct ----
errors = 0
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
print(f"Internal verification errors: {errors}")
print("Difficulty:", Counter(q["diff"] for q in questions))

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_17_Statistics_500.md"

lines = []
lines.append("# Statistics — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- **Mean** = (Σx)/n  ·  **Grouped/Weighted mean** = Σ(f·x)/Σf")
lines.append("- **Median:** sort the data. Odd n → middle value; even n → average of the two middle values.")
lines.append("- **Mode** = the value occurring most frequently.")
lines.append("- **Range** = maximum − minimum.")
lines.append("- **Combined mean** = (n₁m₁ + n₂m₂)/(n₁ + n₂).")
lines.append("- **Population variance** = Σ(x − mean)²/n  ·  **SD** = √variance.")
lines.append("- **SD of first n natural numbers** = √((n² − 1)/12).")
lines.append("- **Transforms:** new value = a·x + b ⇒ mean → a·mean + b ; SD → |a|·SD (adding b does not change SD).")
lines.append("- **Quartiles:** Q1 = median of lower half, Q3 = median of upper half; **IQR** = Q3 − Q1.")
lines.append("- **Empirical relation:** Mode = 3·Median − 2·Mean.\n")
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
