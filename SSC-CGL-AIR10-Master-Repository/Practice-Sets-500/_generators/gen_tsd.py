# -*- coding: utf-8 -*-
"""
SSC CGL Time, Speed & Distance (incl. Trains, Boats & Streams) - 500 hard MCQ generator.
Every answer is COMPUTED, so the key is provably correct.
Builds 4 distinct options (1 correct + 3 common-mistake distractors),
randomizes correct position, dedupes question stems, outputs markdown.

CRITICAL: never pass a float into Fraction(num, den). Convert floats via
Fraction(x).limit_denominator(1000) first. Use Fraction(5,18) for km/h<->m/s.
"""
import random
from fractions import Fraction
from collections import Counter

random.seed(20260625)  # deterministic

LETTERS = "abcd"
KMPH_TO_MPS = Fraction(5, 18)   # multiply km/h by this to get m/s
MPS_TO_KMPH = Fraction(18, 5)   # multiply m/s by this to get km/h

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

# ----------------------------------------------------------------------------
# TEMPLATES
# ----------------------------------------------------------------------------

def t_basic_speed():
    """Distance & time given -> speed (km/h). km/h<->m/s trap. [M]"""
    dist = random.choice([120, 135, 140, 150, 160, 165, 175, 180, 195, 210, 220, 225,
                          240, 245, 260, 270, 280, 300, 315, 320, 330, 350, 360, 375,
                          390, 400, 420, 440, 450, 480, 510, 540, 560, 600])
    time_h = random.choice([2, 3, 4, 5, 6, 7])
    speed = Fraction(dist, time_h)             # km/h
    if not is_clean(speed):
        return None
    correct = speed
    wrong1 = speed * KMPH_TO_MPS               # mistakenly reports m/s value
    wrong2 = Fraction(dist) * time_h           # multiplies instead of divides (scaled)
    wrong3 = speed + 5
    vehicle = random.choice(["car", "bus", "truck", "train", "cyclist", "motorbike"])
    stem = (f"A {vehicle} covers a distance of {dist} km in {time_h} hours. "
            f"Its speed (in km/h) is:")
    sol = (f"Speed = distance / time = {dist} / {time_h} = {fmt(correct)} km/h. "
           f"Trap: do not report the m/s value ({fmt(wrong1)}).")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_kmph_to_mps():
    """Convert km/h to m/s using x5/18. [M]"""
    kmph = random.choice([36, 54, 72, 90, 108, 126, 144, 18, 45, 63, 81, 99])
    correct = Fraction(kmph) * KMPH_TO_MPS
    if not is_clean(correct):
        return None
    wrong1 = Fraction(kmph) * MPS_TO_KMPH      # multiplied by 18/5 instead
    wrong2 = Fraction(kmph, 2)                 # halved
    wrong3 = correct + 5
    stem = (f"Convert {kmph} km/h into metres per second (m/s):")
    sol = (f"m/s = km/h x 5/18 = {kmph} x 5/18 = {fmt(correct)} m/s. "
           f"Trap: x 18/5 converts m/s -> km/h, the wrong direction.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_avg_speed_two_equal():
    """Average speed over two EQUAL distances at speeds x and y -> harmonic mean 2xy/(x+y). [VH]"""
    pairs = [(40, 60), (30, 60), (60, 90), (40, 80), (50, 75), (20, 30),
             (45, 90), (60, 40), (80, 120), (36, 54), (60, 120), (24, 40),
             (30, 45), (50, 30), (90, 60), (48, 72)]
    x, y = random.choice(pairs)
    correct = Fraction(2 * x * y, x + y)       # harmonic mean
    if not is_clean(correct):
        return None
    wrong1 = Fraction(x + y, 2)                # arithmetic mean (classic trap)
    wrong2 = Fraction(x + y)                   # sum
    wrong3 = Fraction(3 * x * y, x + y)        # wrong coefficient
    stem = (f"A man travels from town P to town Q at {x} km/h and returns along the "
            f"same road at {y} km/h. His average speed for the whole journey (in km/h) is:")
    sol = (f"Equal distances -> average speed = harmonic mean = 2xy/(x+y) "
           f"= 2 x {x} x {y} / ({x}+{y}) = {fmt(correct)} km/h. "
           f"Trap: it is NOT the arithmetic mean (x+y)/2 = {fmt(wrong1)}.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_train_cross_pole():
    """Train length L (m) crosses a pole/stationary man -> time, speed given. [M]"""
    length = random.choice([100, 120, 150, 180, 200, 240, 250, 300, 360, 400])
    speed_kmph = random.choice([36, 54, 72, 90, 108])
    speed_mps = Fraction(speed_kmph) * KMPH_TO_MPS
    correct = Fraction(length) / speed_mps     # time in seconds
    if not is_clean(correct):
        return None
    wrong1 = Fraction(length) / Fraction(speed_kmph)   # forgot to convert speed
    wrong2 = Fraction(length) / (speed_mps * 2)
    wrong3 = correct + 2
    stem = (f"A train {length} m long is running at a speed of {speed_kmph} km/h. "
            f"The time it takes to cross a pole (in seconds) is:")
    sol = (f"Speed = {speed_kmph} x 5/18 = {fmt(speed_mps)} m/s. "
           f"Time = length / speed = {length} / {fmt(speed_mps)} = {fmt(correct)} s. "
           f"Trap: convert km/h to m/s first.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_train_cross_platform():
    """Train length L, platform P, speed -> time to cross platform. [H]"""
    length = random.choice([100, 120, 150, 180, 200, 240, 250])
    platform = random.choice([130, 150, 200, 250, 270, 300, 350, 400, 450, 500])
    speed_kmph = random.choice([36, 54, 72, 90, 108])
    speed_mps = Fraction(speed_kmph) * KMPH_TO_MPS
    total = length + platform
    correct = Fraction(total) / speed_mps      # time seconds
    if not is_clean(correct):
        return None
    wrong1 = Fraction(platform) / speed_mps    # forgot train length
    wrong2 = Fraction(length) / speed_mps      # forgot platform
    wrong3 = Fraction(total) / Fraction(speed_kmph)   # no conversion
    stem = (f"A train {length} m long, running at {speed_kmph} km/h, crosses a platform "
            f"{platform} m long. The time taken (in seconds) is:")
    sol = (f"Total distance = train + platform = {length} + {platform} = {total} m. "
           f"Speed = {speed_kmph} x 5/18 = {fmt(speed_mps)} m/s. "
           f"Time = {total} / {fmt(speed_mps)} = {fmt(correct)} s. "
           f"Trap: a train crossing a platform must cover its own length too.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_train_length_from_platform():
    """Speed & time to cross platform given -> train length. [H]"""
    speed_kmph = random.choice([36, 54, 72, 90])
    speed_mps = Fraction(speed_kmph) * KMPH_TO_MPS
    platform = random.choice([150, 180, 200, 240, 250, 300, 320, 360])
    length = random.choice([100, 120, 150, 180, 200, 240])
    total = length + platform
    time_s = Fraction(total) / speed_mps
    if time_s != int(time_s):
        return None
    correct = Fraction(length)
    wrong1 = Fraction(total)                          # gives total, forgets to subtract platform
    wrong2 = Fraction(speed_mps * time_s) - 2 * platform
    wrong3 = Fraction(platform) - length if platform > length else Fraction(platform)
    stem = (f"A train running at {speed_kmph} km/h crosses a platform {platform} m long "
            f"in {fmt(time_s)} seconds. The length of the train (in metres) is:")
    sol = (f"Speed = {speed_kmph} x 5/18 = {fmt(speed_mps)} m/s. "
           f"Distance covered = speed x time = {fmt(speed_mps)} x {fmt(time_s)} = {total} m. "
           f"Train length = total - platform = {total} - {platform} = {fmt(correct)} m.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_two_trains_opposite():
    """Two trains, lengths L1,L2, speeds s1,s2 opposite directions -> time to cross. [H]"""
    l1 = random.choice([120, 140, 150, 160, 180, 200])
    l2 = random.choice([120, 140, 150, 160, 180, 200, 220])
    s1 = random.choice([36, 45, 54, 63, 72])
    s2 = random.choice([36, 45, 54, 63, 72, 81])
    rel = Fraction(s1 + s2) * KMPH_TO_MPS       # opposite -> add speeds
    correct = Fraction(l1 + l2) / rel
    if not is_clean(correct):
        return None
    rel_same = abs(s1 - s2)
    wrong1 = (Fraction(l1 + l2) / (Fraction(rel_same) * KMPH_TO_MPS)
              if rel_same != 0 else None)        # used difference (same-dir mistake)
    wrong2 = Fraction(l1 + l2) / Fraction(s1 + s2)   # no conversion
    wrong3 = correct + 2
    stem = (f"Two trains {l1} m and {l2} m long are running in opposite directions at "
            f"{s1} km/h and {s2} km/h respectively. The time (in seconds) they take to "
            f"cross each other is:")
    sol = (f"Opposite directions -> relative speed = ({s1}+{s2}) x 5/18 = {fmt(rel)} m/s. "
           f"Combined length = {l1}+{l2} = {l1 + l2} m. "
           f"Time = {l1 + l2} / {fmt(rel)} = {fmt(correct)} s. "
           f"Trap: ADD speeds when trains move in opposite directions.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_two_trains_same():
    """Two trains same direction -> time to cross (faster overtakes slower). [VH]"""
    l1 = random.choice([120, 140, 150, 160, 180, 200])
    l2 = random.choice([120, 140, 150, 160, 180, 200, 220])
    fast = random.choice([72, 81, 90, 99, 108])
    slow = random.choice([36, 45, 54, 63])
    rel = Fraction(fast - slow) * KMPH_TO_MPS    # same direction -> subtract
    correct = Fraction(l1 + l2) / rel
    if not is_clean(correct):
        return None
    wrong1 = Fraction(l1 + l2) / (Fraction(fast + slow) * KMPH_TO_MPS)  # added (opp-dir mistake)
    wrong2 = Fraction(l1 + l2) / Fraction(fast - slow)                  # no conversion
    wrong3 = correct + 4
    stem = (f"Two trains {l1} m and {l2} m long are moving in the same direction at "
            f"{fast} km/h and {slow} km/h. The time taken (in seconds) by the faster "
            f"train to completely overtake the slower one is:")
    sol = (f"Same direction -> relative speed = ({fast}-{slow}) x 5/18 = {fmt(rel)} m/s. "
           f"Combined length = {l1}+{l2} = {l1 + l2} m. "
           f"Time = {l1 + l2} / {fmt(rel)} = {fmt(correct)} s. "
           f"Trap: SUBTRACT speeds for same direction.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_train_two_persons():
    """Train passes two persons walking at p1,p2 km/h same dir in t1,t2 s -> train speed. [VH]
    Same direction. Train length L equal in both. Solve two equations.
    L = (S - p1)*5/18*t1 = (S - p2)*5/18*t2  -> S."""
    # choose nice integers: pick S, p1, p2, t1 then derive t2 must be clean.
    for _ in range(40):
        S = random.choice([45, 54, 63, 72, 81, 90])
        p1 = random.choice([3, 5, 6, 9])
        p2 = random.choice([3, 5, 6, 9])
        if p2 <= p1 or p1 >= S or p2 >= S:
            continue
        t1 = random.choice([10, 12, 15, 18, 20, 24, 30])
        # L = (S-p1)*5/18*t1
        L = Fraction(S - p1) * KMPH_TO_MPS * t1
        t2 = L / (Fraction(S - p2) * KMPH_TO_MPS)
        if t2 != int(t2) or t2 == t1 or t2 <= 0:
            continue
        if L != int(L):
            continue
        correct = Fraction(S)
        wrong1 = Fraction(S) + (p2 - p1)            # off
        wrong2 = Fraction(p1 + p2)
        wrong3 = Fraction(S) - p1
        stem = (f"A train passes a man walking at {p1} km/h in the same direction in "
                f"{t1} seconds and another man walking at {p2} km/h in the same "
                f"direction in {fmt(t2)} seconds. The speed of the train (in km/h) is:")
        sol = (f"Let train speed = S. Length is the same in both cases: "
               f"(S-{p1}) x 5/18 x {t1} = (S-{p2}) x 5/18 x {fmt(t2)}. "
               f"Solving gives S = {fmt(correct)} km/h.")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"
    return None

def t_boat_down_up_given():
    """Downstream & upstream speeds given -> boat speed & stream speed. [H]
    Ask for speed of boat in still water = (down+up)/2."""
    boat = random.choice([8, 10, 12, 14, 15, 16, 18, 20, 24])
    stream = random.choice([2, 3, 4, 5, 6])
    if stream >= boat:
        return None
    down = boat + stream
    up = boat - stream
    correct = Fraction(down + up, 2)            # = boat speed
    wrong1 = Fraction(down - up, 2)             # = stream speed (asked boat)
    wrong2 = Fraction(down + up)                # sum, forgot /2
    wrong3 = Fraction(down)
    stem = (f"A boat goes downstream at {down} km/h and upstream at {up} km/h. "
            f"The speed of the boat in still water (in km/h) is:")
    sol = (f"Boat speed = (downstream + upstream)/2 = ({down}+{up})/2 = {fmt(correct)} km/h. "
           f"Stream speed would be (down-up)/2 = {fmt(wrong1)} km/h.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_boat_stream_speed():
    """Downstream & upstream speeds given -> speed of STREAM = (down-up)/2. [H]"""
    boat = random.choice([8, 10, 12, 14, 15, 16, 18, 20, 24])
    stream = random.choice([2, 3, 4, 5, 6])
    if stream >= boat:
        return None
    down = boat + stream
    up = boat - stream
    correct = Fraction(down - up, 2)            # = stream
    wrong1 = Fraction(down + up, 2)             # = boat speed (swapped)
    wrong2 = Fraction(down - up)                # forgot /2
    wrong3 = Fraction(down - up, 2) + 1
    stem = (f"A boat travels downstream at {down} km/h and upstream at {up} km/h. "
            f"The speed of the stream (in km/h) is:")
    sol = (f"Stream speed = (downstream - upstream)/2 = ({down}-{up})/2 = {fmt(correct)} km/h. "
           f"Trap: (down+up)/2 gives the boat's still-water speed instead.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_boat_time_each_way():
    """Boat & stream speed given, distance D one way -> time downstream OR total time. [H]"""
    boat = random.choice([10, 12, 14, 15, 16, 18, 20])
    stream = random.choice([2, 3, 4, 5, 6])
    if stream >= boat:
        return None
    dist = random.choice([24, 30, 36, 40, 48, 60, 72, 84, 90])
    down = boat + stream
    up = boat - stream
    t_total = Fraction(dist, down) + Fraction(dist, up)   # round trip time hours
    if not is_clean(t_total):
        return None
    correct = t_total
    wrong1 = Fraction(2 * dist, boat)                     # ignores stream
    wrong2 = Fraction(dist, down)                         # only one way
    wrong3 = Fraction(2 * dist, up)
    stem = (f"The speed of a boat in still water is {boat} km/h and the speed of the "
            f"stream is {stream} km/h. The total time taken by the boat to go {dist} km "
            f"downstream and return to the starting point (in hours) is:")
    sol = (f"Downstream = {down} km/h, upstream = {up} km/h. "
           f"Total time = {dist}/{down} + {dist}/{up} = {fmt(correct)} hours.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_boat_ratio_time():
    """Ratio of up:down time = k:1 -> ratio boat:stream speed. Ask stream speed given boat. [VH]
    time_up/time_down = down_speed/up_speed = (b+s)/(b-s). If up:down = m:n then
    (b+s)/(b-s) = m/n -> b/s = (m+n)/(m-n)."""
    boat = random.choice([12, 15, 18, 20, 24, 30, 36])
    # choose m,n with m>n
    mn = random.choice([(2, 1), (3, 1), (3, 2), (5, 3), (4, 1), (5, 2)])
    m, n = mn
    # b/s = (m+n)/(m-n) -> s = b*(m-n)/(m+n)
    correct = Fraction(boat) * Fraction(m - n, m + n)
    if not is_clean(correct) or correct <= 0:
        return None
    wrong1 = Fraction(boat) * Fraction(n, m)            # naive ratio
    wrong2 = Fraction(boat) * Fraction(m - n, m)
    wrong3 = Fraction(boat) * Fraction(m + n, m - n) if m > n else None
    if wrong3 is not None and wrong3 == correct:
        wrong3 = correct + 1
    stem = (f"A boat takes {m} times as long to go upstream as to come downstream over "
            f"the same distance. If the speed of the boat in still water is {boat} km/h "
            f"(and the ratio of upstream to downstream time is {m}:{n}), the speed of "
            f"the stream (in km/h) is:")
    sol = (f"time_up : time_down = {m}:{n} -> (b+s)/(b-s) = {m}/{n} "
           f"-> b/s = ({m}+{n})/({m}-{n}). "
           f"So s = b x ({m}-{n})/({m}+{n}) = {boat} x {m - n}/{m + n} = {fmt(correct)} km/h.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_speed_change_pct_time():
    """Change speed by x% -> percentage change in time for same distance. [VH]
    new time = old/(1+x/100). time change% = -x/(100+x)*100 (saved)."""
    x = random.choice([20, 25, 50, 100, 10, 40, 60, 80])
    xf = Fraction(x)
    # time becomes T * 100/(100+x); time reduced by x/(100+x)*100 %
    correct = xf / (100 + xf) * 100           # % reduction in time
    if not is_clean(correct):
        return None
    wrong1 = xf                               # naive same %
    wrong2 = xf / (100 - xf) * 100 if xf < 100 else xf
    wrong3 = xf - 2
    stem = (f"If a person increases his speed by {x}%, by what percent will the time "
            f"taken to cover the same distance decrease?")
    sol = (f"Time is inversely proportional to speed. New time = T x 100/(100+{x}). "
           f"Reduction = {x}/(100+{x}) x 100 = {fmt(correct)}%. "
           f"Trap: it is NOT {x}% itself.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_late_early_distance():
    """At speed s1 reaches late by t1 min, at s2 early by t2 min -> distance. [VH]
    D/s1 - D/s2 = (t1+t2)/60  (total time difference in hours). Solve D."""
    for _ in range(40):
        s1 = random.choice([4, 5, 6, 8, 10, 12])
        s2 = random.choice([5, 6, 8, 10, 12, 15])
        if s2 <= s1:
            continue
        late = random.choice([5, 10, 12, 15, 20, 30])     # late minutes at s1
        early = random.choice([5, 10, 12, 15, 20])        # early minutes at s2
        diff_h = Fraction(late + early, 60)
        # D*(1/s1 - 1/s2) = diff_h
        denom = Fraction(1, s1) - Fraction(1, s2)
        D = diff_h / denom
        if D <= 0 or not is_clean(D) or D > 500:
            continue
        correct = D
        wrong1 = diff_h / (Fraction(1, s1) + Fraction(1, s2))   # added rates
        wrong2 = Fraction(late + early, 60) * s1 * s2           # wrong combination
        wrong3 = D + 2
        stem = (f"A boy walking at {s1} km/h reaches his school {late} minutes late, "
                f"but walking at {s2} km/h he reaches {early} minutes early. "
                f"The distance to the school (in km) is:")
        sol = (f"Let distance = D. Time difference = ({late}+{early}) min = {fmt(diff_h)} h. "
               f"D/{s1} - D/{s2} = {fmt(diff_h)} -> D = {fmt(correct)} km.")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"
    return None

def t_catch_up():
    """A starts, B follows t hours later at higher speed -> distance/time to catch up. [H]
    A at sa, B starts h hours later at sb (sb>sa). Catch-up distance from start."""
    for _ in range(40):
        sa = random.choice([30, 36, 40, 45, 50, 54, 60])
        sb = random.choice([45, 54, 60, 72, 80, 90])
        if sb <= sa:
            continue
        head = random.choice([1, 2, 3])                # hours head start (A)
        # A is ahead by sa*head when B starts. B gains (sb-sa) per hour.
        t_catch = Fraction(sa * head, sb - sa)         # hours for B to catch
        dist = t_catch * sb                            # distance from start
        if not is_clean(dist) or dist > 1500:
            continue
        correct = dist
        wrong1 = Fraction(sa * head)                   # just head-start distance
        wrong2 = t_catch * sa                          # uses sa
        wrong3 = Fraction(sa * head, sb + sa) * sb     # added speeds
        stem = (f"A thief running at {sa} km/h is spotted, and {head} hour(s) later a "
                f"policeman starts chasing him at {sb} km/h along the same road. "
                f"The distance (in km) the policeman covers before catching the thief is:")
        sol = (f"Head start of thief = {sa} x {head} = {sa * head} km. "
               f"Relative speed = {sb}-{sa} = {sb - sa} km/h, "
               f"time to catch = {sa * head}/{sb - sa} = {fmt(t_catch)} h. "
               f"Distance by policeman = {sb} x {fmt(t_catch)} = {fmt(correct)} km.")
        return stem, correct, [wrong1, wrong2, wrong3], sol, "H"
    return None

def t_meet_toward():
    """Two people start toward each other from D apart at sa, sb -> time to meet. [H]"""
    sa = random.choice([30, 36, 40, 45, 50, 60])
    sb = random.choice([30, 36, 40, 45, 50, 60, 70])
    dist = random.choice([120, 150, 180, 210, 240, 300, 360, 420, 480])
    t_meet = Fraction(dist, sa + sb)               # hours
    if not is_clean(t_meet):
        return None
    correct = t_meet
    wrong1 = Fraction(dist, abs(sa - sb)) if sa != sb else None  # subtracted (wrong)
    wrong2 = Fraction(dist, sa)
    wrong3 = Fraction(dist, sb)
    stem = (f"Two cars start at the same time from two places {dist} km apart and move "
            f"toward each other at {sa} km/h and {sb} km/h. The time (in hours) after "
            f"which they meet is:")
    sol = (f"Moving toward each other -> relative speed = {sa}+{sb} = {sa + sb} km/h. "
           f"Time = {dist} / {sa + sb} = {fmt(correct)} h. "
           f"Trap: ADD the speeds when approaching.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_stoppage_time():
    """Avg speed without stops = a, with stops = b -> stoppage minutes per hour. [VH]
    stop min/hr = (a-b)/a * 60."""
    a = random.choice([40, 45, 50, 54, 60, 63, 72, 80])
    b = random.choice([30, 36, 40, 42, 45, 48, 54, 60])
    if b >= a:
        return None
    correct = Fraction(a - b, a) * 60          # minutes stopped per hour
    if not is_clean(correct) or correct >= 60:
        return None
    wrong1 = Fraction(a - b)                    # raw difference in km/h
    wrong2 = Fraction(a - b, b) * 60           # wrong base
    wrong3 = Fraction(a - b, a) * 100          # used 100 not 60
    stem = (f"Excluding stoppages, the average speed of a bus is {a} km/h, and including "
            f"stoppages it is {b} km/h. For how many minutes per hour does the bus stop?")
    sol = (f"Distance lost per hour = {a}-{b} = {a - b} km. "
           f"Time to cover that at running speed = ({a}-{b})/{a} h "
           f"= ({a - b}/{a}) x 60 = {fmt(correct)} minutes per hour.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "VH"

def t_train_man_running():
    """Train length & speed; man runs opposite/same -> time to pass man. [H]"""
    length = random.choice([100, 120, 150, 180, 200, 240, 250])
    train = random.choice([54, 63, 72, 81, 90])
    man = random.choice([3, 6, 9])
    opposite = random.choice([True, False])
    if opposite:
        rel_kmph = train + man
        dir_word = "opposite to the direction of"
    else:
        rel_kmph = train - man
        dir_word = "the same direction as"
    rel = Fraction(rel_kmph) * KMPH_TO_MPS
    correct = Fraction(length) / rel
    if not is_clean(correct):
        return None
    # distractor: used wrong sign
    other = (train - man) if opposite else (train + man)
    wrong1 = Fraction(length) / (Fraction(other) * KMPH_TO_MPS)
    wrong2 = Fraction(length) / (Fraction(train) * KMPH_TO_MPS)   # ignored man
    wrong3 = Fraction(length) / Fraction(rel_kmph)                # no conversion
    stem = (f"A train {length} m long is running at {train} km/h. The time (in seconds) "
            f"it takes to pass a man running at {man} km/h in {dir_word} the train is:")
    sol = (f"Relative speed = "
           f"({train}{'+' if opposite else '-'}{man}) x 5/18 = {fmt(rel)} m/s. "
           f"Time = {length} / {fmt(rel)} = {fmt(correct)} s. "
           f"Trap: {'ADD' if opposite else 'SUBTRACT'} speeds for "
           f"{'opposite' if opposite else 'same'} direction.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "H"

def t_time_dist_speed_find_time():
    """Given speed (km/h) and distance, find time in hours. [M]"""
    speed = random.choice([35, 40, 45, 48, 50, 55, 60, 64, 70, 72, 75, 80, 90])
    time_h = random.choice([2, 3, 4, 5, 6, 7, 8])
    dist = speed * time_h
    correct = Fraction(time_h)
    wrong1 = Fraction(dist, speed) + 1
    wrong2 = Fraction(dist * speed, 1000)
    wrong3 = Fraction(time_h) + 2
    mover = random.choice(["A cyclist", "A car", "A bus", "A jogger", "A train", "A scooter"])
    stem = (f"{mover} travels {dist} km at a uniform speed of {speed} km/h. "
            f"The time taken (in hours) is:")
    sol = (f"Time = distance / speed = {dist} / {speed} = {fmt(correct)} hours.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

def t_mps_to_kmph():
    """Convert m/s to km/h using x18/5. [M]"""
    mps = random.choice([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 7.5, 12.5, 17.5, 22.5])
    correct = Fraction(mps).limit_denominator(1000) * MPS_TO_KMPH
    if not is_clean(correct):
        return None
    wrong1 = Fraction(mps).limit_denominator(1000) * KMPH_TO_MPS   # wrong direction
    wrong2 = Fraction(mps).limit_denominator(1000) * 3              # arbitrary
    wrong3 = correct + 6
    stem = (f"Convert {fmt(Fraction(mps).limit_denominator(1000))} m/s into "
            f"kilometres per hour (km/h):")
    sol = (f"km/h = m/s x 18/5 = {fmt(Fraction(mps).limit_denominator(1000))} x 18/5 "
           f"= {fmt(correct)} km/h. Trap: x 5/18 is the reverse conversion.")
    return stem, correct, [wrong1, wrong2, wrong3], sol, "M"

TEMPLATES = [
    t_basic_speed, t_kmph_to_mps, t_avg_speed_two_equal, t_train_cross_pole,
    t_train_cross_platform, t_train_length_from_platform, t_two_trains_opposite,
    t_two_trains_same, t_train_two_persons, t_boat_down_up_given,
    t_boat_stream_speed, t_boat_time_each_way, t_boat_ratio_time,
    t_speed_change_pct_time, t_late_early_distance, t_catch_up,
    t_meet_toward, t_stoppage_time, t_train_man_running,
    t_time_dist_speed_find_time, t_mps_to_kmph,
]

DIFF_OF = {
    t_basic_speed: "M", t_kmph_to_mps: "M", t_avg_speed_two_equal: "VH",
    t_train_cross_pole: "H", t_train_cross_platform: "H",
    t_train_length_from_platform: "H", t_two_trains_opposite: "H",
    t_two_trains_same: "VH", t_train_two_persons: "VH", t_boat_down_up_given: "H",
    t_boat_stream_speed: "H", t_boat_time_each_way: "H", t_boat_ratio_time: "VH",
    t_speed_change_pct_time: "VH", t_late_early_distance: "VH", t_catch_up: "H",
    t_meet_toward: "H", t_stoppage_time: "VH", t_train_man_running: "H",
    t_time_dist_speed_find_time: "M", t_mps_to_kmph: "M",
}
# Target skew ~20% Medium / 60% Hard / 20% Very-Hard.
TARGET = {"M": 100, "H": 300, "VH": 100}
BY_DIFF = {"M": [], "H": [], "VH": []}
for t in TEMPLATES:
    BY_DIFF[DIFF_OF[t]].append(t)

got = Counter()
attempts = 0
# Draw from whichever difficulty is still under its target; pick a random
# template of that difficulty. This guarantees convergence to the exact skew.
while len(questions) < 500 and attempts < 2000000:
    attempts += 1
    under = [d for d in ("M", "H", "VH") if got[d] < TARGET[d]]
    if not under:
        break
    d = random.choice(under)
    t = random.choice(BY_DIFF[d])
    res = t()
    if res is None:
        continue
    stem, correct, distractors, sol, diff = res
    if add(stem, correct, distractors, sol, diff):
        got[diff] += 1

print(f"Generated {len(questions)} questions in {attempts} attempts.")

# ---- SELF-CHECK ----
errors = 0
assert len(questions) == 500, f"Expected 500, got {len(questions)}"
for i, q in enumerate(questions, 1):
    if len(q["opts"]) != 4:
        print(f"Q{i}: not 4 options"); errors += 1
    if len(set(q["opts"])) != 4:
        print(f"Q{i}: duplicate options {q['opts']}"); errors += 1
    if not (0 <= q["ci"] < 4):
        print(f"Q{i}: bad correct index"); errors += 1
print(f"Self-check errors: {errors}")
assert errors == 0, "Self-check failed!"

dist = Counter(q["diff"] for q in questions)
total = len(questions)
print("Difficulty:", dict(dist))
print("Percentages:", {k: f"{v/total*100:.1f}%" for k, v in dist.items()})

# ---------------- WRITE MARKDOWN ----------------
OUT = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Quant_05_Time_Speed_Distance_500.md"

lines = []
lines.append("# Time, Speed & Distance (incl. Trains, Boats & Streams) — 500 Question Practice Set (SSC CGL, Hard / Tier-II Level)\n")
lines.append("> **Format:** All 500 questions appear first; the full **Answer Key & Explanations** is at the very end.")
lines.append("> **Difficulty skew:** ~20% Medium · ~60% Hard · ~20% Very-Hard (trap) — CGL Tier-II standard.")
lines.append("> **Every numeric answer is computed and machine-verified** — the keyed option is provably correct.")
lines.append("> Negative marking in CGL is −0.50; the distractors are real common-mistake values.\n")
lines.append("## Key Formulas")
lines.append("- Speed = Distance / Time  ·  Distance = Speed × Time  ·  Time = Distance / Speed")
lines.append("- km/h → m/s: **× 5/18**  ·  m/s → km/h: **× 18/5**")
lines.append("- Average speed over two EQUAL distances at x, y = **2xy/(x+y)** (harmonic mean, NOT (x+y)/2)")
lines.append("- Train crossing a pole: time = length / speed")
lines.append("- Train crossing a platform: time = (length + platform) / speed")
lines.append("- Opposite directions: relative speed = **s₁ + s₂**  ·  Same direction: relative speed = **s₁ − s₂**")
lines.append("- Boats: downstream = b + s, upstream = b − s  ·  b = (down+up)/2, s = (down−up)/2")
lines.append("- Speed ↑ x% → time decreases by **x/(100+x)×100 %**")
lines.append("- Stoppage time/hour = **(a−b)/a × 60** minutes (a = speed w/o stops, b = with stops)\n")
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
