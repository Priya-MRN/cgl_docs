# 🕐 Clocks & Calendars — Deep Dive (SSC CGL Reasoning)

> Detailed companion to the Clocks & Calendars row in
> [SSC-CGL-ASO-Formulas-Tricks-Master.md](SSC-CGL-ASO-Formulas-Tricks-Master.md#24-clocks--calendars-).
> Syllabus: Reasoning (Para 13.10.1 / 13.11.2). Read each idea, cover the box, redo the worked example.

**Contents**
1. [Clock basics — the geometry](#1-clock-basics--the-geometry)
2. [Angle between the hands](#2-angle-between-the-hands-)
3. [When do the hands coincide / oppose / make 90°?](#3-when-do-the-hands-coincide-oppose-or-make-90)
4. [Fast / slow / faulty clocks](#4-fast-slow--faulty-clocks)
5. [Calendars — odd days](#5-calendars--the-odd-days-method-)
6. [Leap years](#6-leap-years)
7. [Finding the day of any date](#7-finding-the-day-of-any-date-)
8. [Repeating calendars](#8-which-year-has-the-same-calendar)
9. [Practice set + answers](#9-practice-set)

---

# PART A — CLOCKS

## 1. Clock basics — the geometry

```
   A clock face = 360°, divided into 12 hours and 60 minutes.
   ┌───────────────────────────────────────────────┐
   │  Full circle ............... 360°              │
   │  1 hour space (12 → 1) ...... 360/12 = 30°      │
   │  1 minute space ............ 360/60 = 6°        │
   │  Each hour = 5 minute-spaces (30° = 5 × 6°)     │
   └───────────────────────────────────────────────┘
```

| Hand | Speed | Per minute |
| :-- | :-- | :-- |
| **Minute hand** | 360° in 60 min | **6° per minute** |
| **Hour hand** | 360° in 12 h = 720 min | **0.5° per minute** |
| **Relative gain** | minute over hour | **6 − 0.5 = 5.5° per minute** ⭐ |

🔑 **The single most useful number:** the minute hand gains **5.5° every minute** on the hour hand.
Almost every clock question reduces to *"how long to gain X degrees?"* → time = X ÷ 5.5 min.

```
            12
        11      1
     10            2     • Minute hand moves 6°/min  (fast)
    9       •       3    • Hour hand moves 0.5°/min  (slow)
     8             4     • Gap changes by 5.5°/min
        7       5
            6
```

## 2. Angle between the hands  ⭐

```
   ┌──────────────────────────────────────────────┐
   │   θ = | 30·H − 5.5·M |                         │
   │   H = hour, M = minutes                        │
   │   If θ > 180°, the (smaller) angle = 360 − θ   │
   └──────────────────────────────────────────────┘
   Why: hour hand is at (30H + 0.5M)°; minute hand at (6M)°.
        Difference = |30H + 0.5M − 6M| = |30H − 5.5M|.
```

**Worked example 1 — angle at 3:40**
- θ = |30×3 − 5.5×40| = |90 − 220| = |−130| = **130°**.

**Worked example 2 — angle at 4:20**
- θ = |30×4 − 5.5×20| = |120 − 110| = **10°**.

**Worked example 3 — reflex check at 9:15**
- θ = |30×9 − 5.5×15| = |270 − 82.5| = 187.5° → greater than 180°
- smaller angle = 360 − 187.5 = **172.5°**.

🪄 **Speed tip:** at H o'clock exactly (M=0), angle = 30H (take the smaller side). E.g. 5:00 → 150°.

## 3. When do the hands coincide, oppose, or make 90°?

The hands start a "race"; the minute hand catches up at **5.5°/min**.

| Event | Angle to cover | Times in 12 hours | Gap between events |
| :-- | :-- | :-- | :-- |
| **Coincide** (0° apart) | 0° / 360° | **11 times** | every 720/11 = **65 5⁄11 min** |
| **Opposite** (180° apart) | 180° | **11 times** | every 65 5⁄11 min |
| **Right angle** (90°) | 90° (twice/cycle) | **22 times** | — |

```
   WHY 11 (not 12) overlaps in 12 hours:
   In 12 h the minute hand laps the hour hand only 11 times
   (the 12 o'clock overlap is shared by start & end).
   → overlaps at 12:00, 1:05⁵⁄₁₁, 2:10¹⁰⁄₁₁, … about every 65.45 min.
```

**Worked example 4 — after 4 o'clock, when do hands coincide?**
- At 4:00 the hour hand leads by 4×30 = 120°.
- Minute hand must gain 120° at 5.5°/min → time = 120 ÷ 5.5 = **21 9⁄11 min past 4** (≈ 4:21:49).

**Worked example 5 — between 4 and 5, when are hands at right angles (90°)?**
- Need gap = 90°. Start gap (at 4:00) = 120°.
- **First 90°:** reduce 120 → 90, gain (120−90)=30° → 30÷5.5 = 5 5⁄11 min → **4:05 5⁄11**.
- **Second 90°:** go past coincidence to 90° on other side: gain (120+90)=210° → 210÷5.5 = 38 2⁄11 → **4:38 2⁄11**.

## 4. Fast, slow & faulty clocks

| Situation | How to handle | 🪄 Trick |
| :-- | :-- | :-- |
| Clock **gains** x min/day | runs fast; shows later time | add error over elapsed days |
| Clock **loses** x min/day | runs slow; shows earlier time | subtract error |
| Hands coincide every X min | if X ≠ 65 5⁄11, clock is **faulty** | compare to 65.4545… |
| Total gain/loss | rate × (number of days/hours) | proportion |

**Worked example 6 — fast clock**
> A clock gains 5 minutes every hour. If set correct at 8:00 a.m., what does it show at the real 8:00 p.m. (same day)?
- Real time elapsed = 12 hours → gain = 5 × 12 = 60 min = 1 hour.
- Clock shows **9:00 p.m.**

**Worked example 7 — "faulty" detection**
> The hands of a clock coincide every 64 minutes of correct time. Is it fast or slow?
- Correct clocks coincide every 65 5⁄11 ≈ 65.45 min. This one does it in 64 min (sooner) → it is running **fast**.
- Gain per coincidence = 65 5⁄11 − 64 = 16⁄11 min, so over a day it can be scaled up.

---

# PART B — CALENDARS

## 5. Calendars — the "odd days" method  ⭐

```
   ┌──────────────────────────────────────────────┐
   │  ODD DAYS = days left over after counting     │
   │  complete weeks (remainder when ÷ 7).         │
   │  The day of the week shifts by the odd days.  │
   └──────────────────────────────────────────────┘
   1 ordinary year = 365 days = 52 weeks + 1 → 1 odd day
   1 leap year     = 366 days = 52 weeks + 2 → 2 odd days
```

| Period | Odd days | 🪄 Trick |
| :-- | :-- | :-- |
| Ordinary year | **1** | "next year same date = next weekday" |
| Leap year | **2** | jumps two weekdays |
| 100 years | **5** | (76 ordinary + 24 leap → 76+48 = 124 ; 124 mod 7 = 5) |
| 200 years | **3** | (5×2 = 10 → 3) |
| 300 years | **1** | (5×3 = 15 → 1) |
| 400 years | **0** | (and every multiple of 400) ⭐ |

```
   ODD-DAY COUNT PER MONTH (memorise the remainders, value mod 7)
   ┌───────┬────┬───────┬────┬───────┬────┐
   │ Jan 31│ 3  │ May 31│ 3  │ Sep 30│ 2  │
   │ Feb 28│ 0  │ Jun 30│ 2  │ Oct 31│ 3  │   (Feb 29 in a leap yr → 1)
   │ Mar 31│ 3  │ Jul 31│ 3  │ Nov 30│ 2  │
   │ Apr 30│ 2  │ Aug 31│ 3  │ Dec 31│ 3  │
   └───────┴────┴───────┴────┴───────┴────┘
   🪄 30-day months give 2 odd days; 31-day months give 3; Feb gives 0 (or 1 if leap).
```

## 6. Leap years

```
   ┌──────────────────────────────────────────────┐
   │  Leap year rule:                              │
   │  • divisible by 4              → leap          │
   │  • BUT century years (÷100)    → NOT leap …    │
   │  • … UNLESS also ÷ 400         → leap          │
   └──────────────────────────────────────────────┘
   ✅ Leap:  2008, 2012, 2024, 2000, 2400
   ❌ Not :  2009, 1900, 2100, 2200, 2300
```

🪄 **Trick:** 1900 is **not** a leap year (÷100 but not ÷400); 2000 **is** (÷400). This single fact is a very common trap.

## 7. Finding the day of any date  ⭐

**Method (odd-days from a reference):** add odd days for completed centuries + years + months + date, take mod 7, map to a weekday.

```
   WEEKDAY CODE (from total odd days, mod 7)
   0 → Sunday   1 → Monday   2 → Tuesday   3 → Wednesday
   4 → Thursday 5 → Friday   6 → Saturday
```

**Worked example 8 — what day was 15 August 1947?**
Step 1: 1600 yrs → 0 odd days. (use nearest 400-multiple before the year)
Step 2: 300 yrs (1601–1900) → 1 odd day.
Step 3: 46 complete years (1901–1946): leap years among them = 46÷4 = 11 leaps, 35 ordinary.
  odd days = 35×1 + 11×2 = 35 + 22 = 57 → 57 mod 7 = **1**.
Step 4: year 1947, months Jan–Jul + 15 days of Aug:
  Jan31 Feb28 Mar31 Apr30 May31 Jun30 Jul31 = 212 days; + 15 = 227 days → 227 mod 7 = **3**.
Step 5: total odd days = 0 + 1 + 1 + 3 = 5 → **Friday**.
✅ **15 August 1947 was a Friday.**

```
   COUNT-UP DIAGRAM
   [centuries: 0+1] + [years 1901-46: 1] + [this year's months+date: 3]
            = 5  →  Friday
```

**Worked example 9 — same date, next year**
> If 1 Jan 2025 is Wednesday, what is 1 Jan 2026?
- 2025 is an ordinary year → 1 odd day → shift by 1 → **Thursday**.
> And 1 Jan 2027? (2026 ordinary → +1) → **Friday**.

## 8. Which year has the same calendar?

| Case | Calendar repeats after | 🪄 Trick |
| :-- | :-- | :-- |
| Ordinary year after ordinary | +6 or +11 years (commonly **+11**) | sum of odd days = 7 |
| Leap year | repeats after **28 years** | full cycle |
| Quick rule | add years until cumulative odd days = 0 (mod 7) | — |

**Worked example 10**
> Which year will have the same calendar as 2024 (a leap year)?
- Leap-year calendars repeat every 28 years → **2052**.

---

# 9. Practice set

> Cover the answers. Aim: < 40 seconds each.

| # | Question | Answer |
| :-: | :-- | :-- |
| 1 | Angle between hands at **2:30**? | \|30·2 − 5.5·30\| = \|60−165\| = **105°** |
| 2 | Angle at **6:00**? | 180° (straight line) |
| 3 | How many times do the hands coincide in **a day (24 h)**? | **22 times** (11 per 12 h) |
| 4 | Hands coincide every 65 5⁄11 min — true gap in a **correct** clock? | yes, ≈ **65.45 min** |
| 5 | A clock loses 10 min/day. After 6 days it shows? | **1 hour slow** (10×6=60 min) |
| 6 | Odd days in a **leap year**? | **2** |
| 7 | Is **2100** a leap year? | **No** (÷100, not ÷400) |
| 8 | If 1 Jan 2024 is Monday, 1 Jan 2025 is? | 2024 leap → +2 → **Wednesday** |
| 9 | Odd days in **400 years**? | **0** |
| 10 | Day on **26 January 1950** (Republic Day)? | **Thursday** |
| 11 | Between 3 and 4 o'clock, hands coincide at? | 3:00 gap 90° → 90÷5.5 = **3:16 4⁄11** |
| 12 | A leap year's calendar repeats after? | **28 years** |

```
   Q11 working:  at 3:00 hour hand leads by 90°.
   Minute hand gains 90° at 5.5°/min → 90 ÷ 5.5 = 16 4⁄11 min past 3.
```

---

> ✅ **Two numbers carry this whole topic:** **5.5°/min** (clocks) and **odd days mod 7** (calendars).
> Master those and every question becomes a one-line calculation. Back to the
> [main formula sheet »](SSC-CGL-ASO-Formulas-Tricks-Master.md).
