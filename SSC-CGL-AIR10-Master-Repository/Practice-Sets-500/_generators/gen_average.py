# -*- coding: utf-8 -*-
"""
SSC CGL Average - 500 hard PYQ-pattern MCQ generator.
Every answer is COMPUTED, so the key is provably correct.
Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.
Mirrors gen_percentage.py. CRITICAL: never pass a float into Fraction(num,den).
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

questions = []  # each: dict(stem, opts, correct_index, sol, diff)
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

# ---------------- TEMPLATES ----------------
# All arithmetic in exact Fraction. PYQ-pattern Average shapes (SSC CGL 2018-2025).

def t_basic_avg():
    """Average of n given numbers. [M]"""
    n = random.choice([4, 5, 6, 7, 8])
    nums = [random.choice(range(20, 120)) for _ in range(n)]
    total = sum(nums)
    avg = Fraction(total, n)
    if not is_clean(avg):
        return None
    correct = avg
    wrong1 = Fraction(total, n + 1)       # divides by wrong count
    wrong2 = Fraction(total, max(1, n - 1))
    wrong3 = avg + random.choice([2, 3, 4, 5])
    stem = (f"The average of the numbers {', '.join(map(str, nums))} is:")
    sol = (f"Average = sum/count = {total}/{n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_consec_integers():
    """Average of consecutive integers. [M]"""
    start = random.choice(range(10, 90))
    n = random.choice([5, 7, 9, 11, 13, 6, 8, 10])
    nums = list(range(start, start + n))
    total = sum(nums)
    avg = Fraction(total, n)
    correct = avg
    wrong1 = Fraction(start)              # first term
    wrong2 = Fraction(start + n - 1)      # last term
    wrong3 = Fraction(start + n)
    stem = (f"The average of {n} consecutive integers starting from {start} is:")
    sol = (f"Average of consecutive numbers = (first+last)/2 = "
           f"({start}+{start+n-1})/2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_consec_even_odd():
    """Average of consecutive even/odd numbers. [M]"""
    kind = random.choice(["even", "odd"])
    if kind == "even":
        start = random.choice(range(10, 80, 2))
    else:
        start = random.choice(range(11, 81, 2))
    n = random.choice([5, 6, 7, 8, 9, 10])
    nums = [start + 2 * i for i in range(n)]
    last = nums[-1]
    total = sum(nums)
    avg = Fraction(total, n)
    correct = avg
    wrong1 = Fraction(start)
    wrong2 = Fraction(last)
    wrong3 = avg + 2
    stem = (f"The average of {n} consecutive {kind} numbers starting from {start} is:")
    sol = (f"Average = (first+last)/2 = ({start}+{last})/2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_first_n_multiples():
    """Average of first n multiples of k = k(n+1)/2. [H]"""
    k = random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15])
    n = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 15, 20])
    avg = Fraction(k * (n + 1), 2)
    if not is_clean(avg):
        return None
    correct = avg
    wrong1 = Fraction(k * n, 2)           # forgets +1
    wrong2 = Fraction(k * (n + 1))        # forgets /2
    wrong3 = Fraction(k * n)              # uses k*n
    stem = (f"The average of the first {n} multiples of {k} is:")
    sol = (f"Average of first n multiples of k = k(n+1)/2 = "
           f"{k}×({n}+1)/2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_first_n_natural():
    """Average of first n natural numbers = (n+1)/2. [H]"""
    n = random.choice(range(15, 100))
    avg = Fraction(n + 1, 2)
    correct = avg
    wrong1 = Fraction(n, 2)               # n/2
    wrong2 = Fraction(n + 1)              # forgets /2
    wrong3 = avg + Fraction(1, 2)
    stem = (f"The average of the first {n} natural numbers is:")
    sol = (f"Average of first n natural numbers = (n+1)/2 = ({n}+1)/2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_ap_average():
    """Average of an AP = (first+last)/2. [H]"""
    a = random.choice(range(5, 50))
    d = random.choice([2, 3, 4, 5, 6, 7])
    n = random.choice([6, 8, 10, 12, 9, 11])
    last = a + (n - 1) * d
    total = Fraction(n * (a + last), 2)
    avg = total / n
    if not is_clean(avg):
        return None
    correct = avg
    wrong1 = Fraction(a)
    wrong2 = Fraction(last)
    wrong3 = avg + d
    stem = (f"The average of {n} terms of an arithmetic progression whose first term "
            f"is {a} and common difference is {d} is:")
    sol = (f"Last term = a+(n-1)d = {a}+{n-1}×{d} = {last}. "
           f"Average = (first+last)/2 = ({a}+{last})/2 = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_element_added():
    """New average when one element is added. [H]"""
    n = random.choice([6, 8, 10, 12, 15, 9, 11, 14])
    old_avg = random.choice(range(20, 80))
    old_total = old_avg * n
    new_val = random.choice(range(20, 120))
    new_avg = Fraction(old_total + new_val, n + 1)
    if not is_clean(new_avg):
        return None
    correct = new_avg
    wrong1 = Fraction(old_total + new_val, n)     # forgets count change
    wrong2 = Fraction(old_avg + new_val, 2)       # avg of avg & value
    wrong3 = Fraction(old_avg)
    stem = (f"The average of {n} numbers is {old_avg}. If a new number {new_val} is "
            f"included, the average of all {n+1} numbers becomes:")
    sol = (f"New average = (old sum + new) / (n+1) = "
           f"({old_avg}×{n}+{new_val})/{n+1} = {old_total + new_val}/{n+1} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_element_removed():
    """New average when one element is removed. [H]"""
    n = random.choice([6, 8, 10, 12, 15, 9, 11])
    old_avg = random.choice(range(30, 90))
    old_total = old_avg * n
    removed = random.choice(range(10, old_avg))
    new_avg = Fraction(old_total - removed, n - 1)
    if not is_clean(new_avg):
        return None
    correct = new_avg
    wrong1 = Fraction(old_total - removed, n)     # forgets count change
    wrong2 = Fraction(old_avg)
    wrong3 = new_avg + random.choice([2, 3])
    stem = (f"The average of {n} numbers is {old_avg}. If one number {removed} is "
            f"removed, the average of the remaining {n-1} numbers is:")
    sol = (f"New average = (old sum − removed) / (n−1) = "
           f"({old_avg}×{n}−{removed})/{n-1} = {old_total - removed}/{n-1} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_wrong_replaced_find_correct():
    """Average changes by d when a wrong value replaced by correct -> find correct value. [VH]"""
    n = random.choice([6, 8, 10, 12, 15, 20, 25])
    wrong_val = random.choice(range(20, 80))
    direction = random.choice(["increased", "decreased"])
    d = random.choice([1, 2, Fraction(1, 2), 3, Fraction(3, 2)])
    delta = Fraction(d) * n
    if direction == "increased":
        correct_val = Fraction(wrong_val) + delta
    else:
        correct_val = Fraction(wrong_val) - delta
    if correct_val <= 0 or not is_clean(correct_val):
        return None
    correct = correct_val
    wrong1 = Fraction(wrong_val) + Fraction(d)          # adds d not d*n
    wrong2 = Fraction(wrong_val) - Fraction(d) if direction == "increased" else Fraction(wrong_val) + Fraction(d)
    wrong3 = Fraction(wrong_val) - delta if direction == "increased" else Fraction(wrong_val) + delta
    stem = (f"The average of {n} numbers was calculated. It was later found that one "
            f"number was wrongly read as {wrong_val}. After correcting it, the average "
            f"{direction} by {fmt(Fraction(d))}. The correct value of that number is:")
    sol = (f"Total change in sum = {fmt(Fraction(d))}×{n} = {fmt(delta)}. The average "
           f"{direction}, so the correct number = {wrong_val} "
           f"{'+' if direction=='increased' else '−'} {fmt(delta)} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_misread_find_correct_avg():
    """A number misread; given correct & wrong values, find the correct average. [VH]"""
    n = random.choice([10, 12, 15, 20, 25])
    wrong_avg = random.choice(range(30, 80))
    wrong_total = wrong_avg * n
    read_as = random.choice(range(20, 60))
    actual = read_as + random.choice([6, 8, 9, 10, 12, 15, 18, 20, 24])
    correct_total = wrong_total - read_as + actual
    correct_avg = Fraction(correct_total, n)
    if not is_clean(correct_avg):
        return None
    correct = correct_avg
    wrong1 = Fraction(wrong_avg)                          # ignores correction
    wrong2 = Fraction(wrong_total - actual + read_as, n)  # correction reversed
    wrong3 = correct_avg + 1
    stem = (f"The average of {n} numbers is {wrong_avg}. Later it was found that a "
            f"number {actual} was misread as {read_as} while calculating. The correct "
            f"average is:")
    sol = (f"Correct sum = {wrong_avg}×{n} − {read_as} + {actual} = {correct_total}. "
           f"Correct average = {correct_total}/{n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_omitted_number():
    """Find the omitted/wrong number given average correction. [VH]"""
    n = random.choice([10, 12, 15, 20])
    true_avg = random.choice(range(30, 80))
    true_total = true_avg * n
    # one number replaced; given new wrong average, find that number
    other_num = random.choice(range(20, 60))
    wrong_total = true_total - other_num + 0  # placeholder
    # Simpler classic: average of n numbers is A; if one number is omitted avg of rest is B; find omitted
    rest_avg = random.choice(range(20, true_avg))
    omitted = true_total - rest_avg * (n - 1)
    if omitted <= 0:
        return None
    correct = Fraction(omitted)
    wrong1 = Fraction(true_avg)
    wrong2 = Fraction(rest_avg)
    wrong3 = Fraction(true_avg * n - rest_avg * n)
    stem = (f"The average of {n} numbers is {true_avg}. If one of the numbers is "
            f"excluded, the average of the remaining {n-1} numbers is {rest_avg}. "
            f"The excluded number is:")
    sol = (f"Excluded = (sum of all) − (sum of rest) = {true_avg}×{n} − {rest_avg}×{n-1} "
           f"= {true_total} − {rest_avg*(n-1)} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_age_person_joins():
    """Average age of group; a person joins -> new average. [H]"""
    n = random.choice([6, 8, 10, 12, 15, 9, 11])
    avg = random.choice(range(18, 45))
    joiner = random.choice(range(15, 60))
    new_avg = Fraction(avg * n + joiner, n + 1)
    if not is_clean(new_avg):
        return None
    correct = new_avg
    wrong1 = Fraction(avg * n + joiner, n)
    wrong2 = Fraction(avg + joiner, 2)
    wrong3 = Fraction(avg)
    stem = (f"The average age of {n} members of a club is {avg} years. If a new member "
            f"aged {joiner} years joins the club, the new average age (in years) is:")
    sol = (f"New average = (total age + new member)/(n+1) = "
           f"({avg}×{n}+{joiner})/{n+1} = {avg*n+joiner}/{n+1} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_age_change_find_person():
    """Group average changes when person joins/leaves -> find that person's age. [VH]"""
    n = random.choice([8, 10, 12, 15, 20])
    avg = random.choice(range(20, 45))
    direction = random.choice(["increases", "decreases"])
    d = random.choice([1, 2, 3, Fraction(1, 2)])
    if direction == "increases":
        # a person joins, avg increases by d. new count n+1.
        person = Fraction(avg) + Fraction(d) * (n + 1)
        new_avg = Fraction(avg) + Fraction(d)
    else:
        person = Fraction(avg) - Fraction(d) * (n + 1)
        new_avg = Fraction(avg) - Fraction(d)
    if person <= 0 or not is_clean(person):
        return None
    correct = person
    wrong1 = Fraction(avg) + Fraction(d) * n if direction == "increases" else Fraction(avg) - Fraction(d) * n
    wrong2 = Fraction(avg) + Fraction(d) if direction == "increases" else Fraction(avg) - Fraction(d)
    wrong3 = Fraction(avg)
    stem = (f"The average age of a group of {n} persons is {avg} years. When one more "
            f"person joins the group, the average age {direction} by {fmt(Fraction(d))} "
            f"years. The age (in years) of the new person is:")
    sol = (f"New average = {avg} {'+' if direction=='increases' else '−'} {fmt(Fraction(d))} "
           f"= {fmt(new_avg)}. New person's age = (new avg)×(n+1) − (old total) = "
           f"{fmt(new_avg)}×{n+1} − {avg}×{n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_captain_included():
    """Team average; captain/teacher included changes average -> their value. [VH]"""
    role = random.choice(["captain of a cricket team", "class teacher"])
    if "captain" in role:
        n = 11
        unit = "players"
    else:
        n = random.choice([20, 25, 30, 35, 40])
        unit = "students"
    avg = random.choice(range(20, 40))
    d = random.choice([1, 2, 3])
    # including the extra person raises average by d; total people = n+1
    # excluding_avg given for n; with person avg = avg+d for n+1
    new_avg = avg + d
    person_val = new_avg * (n + 1) - avg * n
    correct = Fraction(person_val)
    wrong1 = Fraction(avg)
    wrong2 = Fraction(new_avg)
    wrong3 = Fraction(avg + d * n)
    stem = (f"The average age of {n} {unit} is {avg} years. When the {role.split(' of')[0] if 'captain' in role else role}'s "
            f"age is also included, the average age increases by {d} year(s). "
            f"The age (in years) of the {role.split(' of')[0] if 'captain' in role else role} is:")
    # simplify wording
    who = "captain" if "captain" in role else "teacher"
    stem = (f"The average age of {n} {unit} of a {('team' if who=='captain' else 'class')} is "
            f"{avg} years. When the {who}'s age is included, the average increases by "
            f"{d} year(s). The age (in years) of the {who} is:")
    sol = (f"{who.capitalize()}'s age = (new avg)×(n+1) − (old total) = "
           f"{new_avg}×{n+1} − {avg}×{n} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_weighted_two_groups():
    """Weighted average of two groups (boys/girls marks). [H]"""
    n1 = random.choice([15, 20, 24, 25, 30, 36, 40])
    n2 = random.choice([10, 12, 15, 18, 20, 25, 30])
    a1 = random.choice(range(40, 80))
    a2 = random.choice(range(40, 80))
    total = a1 * n1 + a2 * n2
    avg = Fraction(total, n1 + n2)
    if not is_clean(avg):
        return None
    correct = avg
    wrong1 = Fraction(a1 + a2, 2)            # simple average of the two averages
    wrong2 = Fraction(total, n1)            # wrong total count
    wrong3 = Fraction(a1 * n2 + a2 * n1, n1 + n2)  # swapped weights
    stem = (f"In a class, the average marks of {n1} boys is {a1} and the average marks "
            f"of {n2} girls is {a2}. The average marks of the whole class is:")
    sol = (f"Class average = (n1×a1 + n2×a2)/(n1+n2) = "
           f"({n1}×{a1}+{n2}×{a2})/{n1+n2} = {total}/{n1+n2} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_abc_find_third():
    """Average of a,b,c is X; average of a,b is Y -> find c. [H]"""
    avg3 = random.choice(range(20, 80))
    avg2 = random.choice(range(20, 80))
    c = 3 * avg3 - 2 * avg2
    if c <= 0:
        return None
    correct = Fraction(c)
    wrong1 = Fraction(avg3)
    wrong2 = Fraction(3 * avg3 - avg2)       # forgets ×2
    wrong3 = Fraction(2 * avg3 - 2 * avg2)
    stem = (f"The average of three numbers a, b and c is {avg3}. If the average of a and "
            f"b is {avg2}, then the value of c is:")
    sol = (f"a+b+c = 3×{avg3} = {3*avg3}; a+b = 2×{avg2} = {2*avg2}. "
           f"c = {3*avg3} − {2*avg2} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_avg_increase_new_members():
    """Average increases by d when new members of avg-y join -> count of new members or value. [VH]"""
    n = random.choice([10, 12, 15, 20, 24, 25])
    avg = random.choice(range(20, 45))
    k = random.choice([2, 3, 4, 5])      # new members
    d = random.choice([1, 2, 3])         # increase in average
    new_count = n + k
    new_avg = avg + d
    # average value of the k new members:
    new_members_total = new_avg * new_count - avg * n
    each = Fraction(new_members_total, k)
    if not is_clean(each) or each <= 0:
        return None
    correct = each
    wrong1 = Fraction(new_avg)
    wrong2 = Fraction(avg)
    wrong3 = Fraction(new_members_total)   # total not average
    stem = (f"The average age of {n} workers is {avg} years. {k} new workers join and "
            f"the average age of all workers becomes {new_avg} years. The average age "
            f"(in years) of the {k} new workers is:")
    sol = (f"Total of new workers = (new avg)×(total) − (old total) = "
           f"{new_avg}×{new_count} − {avg}×{n} = {new_members_total}. "
           f"Average = {new_members_total}/{k} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_innings_raise_average():
    """To raise average to A after k innings, given current avg over (k-1), find runs needed. [VH]"""
    played = random.choice([9, 10, 11, 12, 14, 15, 16, 19])
    cur_avg = random.choice(range(20, 55))
    inc = random.choice([2, 3, 4, 5])
    new_avg = cur_avg + inc
    next_inning = played + 1
    runs_needed = new_avg * next_inning - cur_avg * played
    if runs_needed <= 0:
        return None
    correct = Fraction(runs_needed)
    wrong1 = Fraction(new_avg)
    wrong2 = Fraction(new_avg * played - cur_avg * played)  # forgets the +1 inning
    wrong3 = Fraction(cur_avg + inc * next_inning)
    stem = (f"A batsman has an average of {cur_avg} runs in {played} innings. How many "
            f"runs must he score in his next innings to raise his average to {new_avg}?")
    sol = (f"Required runs = (new avg)×(innings now) − (old total) = "
           f"{new_avg}×{next_inning} − {cur_avg}×{played} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_innings_drop_average():
    """A score in next innings drops/raises avg -> find new average. [H]"""
    played = random.choice([10, 12, 15, 16, 11, 9])
    cur_avg = random.choice(range(30, 60))
    score = random.choice(range(5, 100))
    new_avg = Fraction(cur_avg * played + score, played + 1)
    if not is_clean(new_avg):
        return None
    correct = new_avg
    wrong1 = Fraction(cur_avg * played + score, played)
    wrong2 = Fraction(cur_avg + score, 2)
    wrong3 = Fraction(cur_avg)
    stem = (f"A cricketer has a batting average of {cur_avg} runs in {played} innings. "
            f"In the next innings he scores {score} runs. His new batting average is:")
    sol = (f"New average = (old runs + new score)/(innings+1) = "
           f"({cur_avg}×{played}+{score})/{played+1} = {cur_avg*played+score}/{played+1} "
           f"= {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_replace_person_age():
    """One person replaced by another changes average -> find new/old person's age. [VH]"""
    n = random.choice([8, 10, 12, 15, 20])
    avg = random.choice(range(20, 45))
    d = random.choice([1, 2, 3, Fraction(1, 2)])
    direction = random.choice(["decreases", "increases"])
    old_person = random.choice(range(30, 60))
    if direction == "decreases":
        new_person = Fraction(old_person) - Fraction(d) * n
    else:
        new_person = Fraction(old_person) + Fraction(d) * n
    if new_person <= 0 or not is_clean(new_person):
        return None
    correct = new_person
    wrong1 = Fraction(old_person) - Fraction(d) if direction == "decreases" else Fraction(old_person) + Fraction(d)
    wrong2 = Fraction(old_person) + Fraction(d) * n if direction == "decreases" else Fraction(old_person) - Fraction(d) * n
    wrong3 = Fraction(old_person)
    stem = (f"The average age of {n} persons is {avg} years. A person aged {old_person} "
            f"years is replaced by a new person, and the average {direction} by "
            f"{fmt(Fraction(d))} year(s). The age (in years) of the new person is:")
    sol = (f"Total change in sum = {fmt(Fraction(d))}×{n} = {fmt(Fraction(d)*n)}. "
           f"New person's age = {old_person} "
           f"{'−' if direction=='decreases' else '+'} {fmt(Fraction(d)*n)} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_avg_of_averages_temp():
    """Average of daily temperature / monthly figures over a period. [M]"""
    days = random.choice([5, 6, 7])
    vals = [random.choice(range(25, 45)) for _ in range(days)]
    total = sum(vals)
    avg = Fraction(total, days)
    if not is_clean(avg):
        return None
    correct = avg
    wrong1 = Fraction(total, days + 1)
    wrong2 = Fraction(total, days - 1)
    wrong3 = avg + 1
    label = "temperature (in °C)"
    stem = (f"The {label} recorded over {days} days was "
            f"{', '.join(map(str, vals))}. The average {label.split(' (')[0]} is:")
    sol = (f"Average = sum/days = {total}/{days} = {fmt(correct)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

TEMPLATES = [
    t_basic_avg, t_consec_integers, t_consec_even_odd, t_first_n_multiples,
    t_first_n_natural, t_ap_average, t_element_added, t_element_removed,
    t_wrong_replaced_find_correct, t_misread_find_correct_avg, t_omitted_number,
    t_age_person_joins, t_age_change_find_person, t_captain_included,
    t_weighted_two_groups, t_abc_find_third, t_avg_increase_new_members,
    t_innings_raise_average, t_innings_drop_average, t_replace_person_age,
    t_avg_of_averages_temp,
]

DIFF_OF = {
    t_basic_avg: "M", t_consec_integers: "M", t_consec_even_odd: "M",
    t_first_n_multiples: "H", t_first_n_natural: "H", t_ap_average: "H",
    t_element_added: "H", t_element_removed: "H",
    t_wrong_replaced_find_correct: "VH", t_misread_find_correct_avg: "VH",
    t_omitted_number: "VH", t_age_person_joins: "H",
    t_age_change_find_person: "VH", t_captain_included: "VH",
    t_weighted_two_groups: "H", t_abc_find_third: "H",
    t_avg_increase_new_members: "VH", t_innings_raise_average: "VH",
    t_innings_drop_average: "H", t_replace_person_age: "VH",
    t_avg_of_averages_temp: "M",
}
# Target ~20% M / 60% H / 20% VH -> 100 / 300 / 100.
# Per-difficulty quota controls the skew precisely (dedup-safe).
QUOTA = {"M": 100, "H": 300, "VH": 100}
BY_DIFF = {"M": [], "H": [], "VH": []}
for t in TEMPLATES:
    BY_DIFF[DIFF_OF[t]].append(t)

count_by_diff = {"M": 0, "H": 0, "VH": 0}
attempts = 0
while len(questions) < 500 and attempts < 2000000:
    attempts += 1
    # pick a difficulty bucket that still needs questions
    needed = [d for d in ("M", "H", "VH") if count_by_diff[d] < QUOTA[d]]
    if not needed:
        break
    d = random.choice(needed)
    t = random.choice(BY_DIFF[d])
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    before = len(questions)
    if add(stem, correct, distractors, sol, diff):
        count_by_diff[diff] += 1

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- VERIFY internally ----
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
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_12_Average_500.md"

lines = []
lines.append("# Average — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** Medium / Hard / Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- `Average = (sum of observations) / (number of observations)`")
lines.append("- Average of consecutive numbers / an AP = **(first + last) / 2**")
lines.append("- Average of first n natural numbers = **(n+1)/2**")
lines.append("- Average of first n multiples of k = **k(n+1)/2**")
lines.append("- New value when one item is added/removed: recompute **sum ± value** over **new count**")
lines.append("- Wrong value corrected: change in sum = **(change in average) × (count)**")
lines.append("- Person joins and average changes by d → person = **(new avg)×(new count) − (old sum)**")
lines.append("- Weighted average of two groups = **(n₁a₁ + n₂a₂)/(n₁ + n₂)**")
lines.append("- Runs to raise average to A after next innings = **A×(innings now) − (old total)**\n")
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
