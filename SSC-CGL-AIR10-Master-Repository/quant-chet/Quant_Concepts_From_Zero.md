# Quant From Zero — How to *See* the Question Before You Solve It

> **Who this is for:** You, right now, who feels lost staring at a quant question.
> **The goal:** Not to memorise formulas (you already have those in `Quant_Cheatsheet.md`). The goal is to teach you to **read a word problem and instantly picture what's happening** — because once you can picture it, the formula becomes obvious.
>
> **How to use this sheet:** Read one chapter. Do the "Picture it" exercise in your head. Then do 5 questions from your PYQ folder on that topic. Don't move on until the *picture* comes automatically.

---

## The One Mental Habit That Fixes Everything

Before any question, ask yourself **3 questions in order**:

1. **What is moving / changing / being compared?** (a person, money, water, an angle, a shape)
2. **What do they GIVE me, and what do they ASK for?** (Write both down. Underline the question.)
3. **What is the ONE relationship connecting them?** (speed=dist/time, profit=SP−CP, etc.)

90% of "I don't know how to start" disappears when you force yourself to write down *given* vs *asked*. Do it on paper every single time until it's a reflex.

---

## 1 · Percentages — *"out of 100"*

**The picture:** Percent literally means "per 100". Imagine a pizza cut into 100 slices. 25% = 25 slices. That's it.

**The only idea you need:** A percentage is a **fraction in disguise**. `25% = 25/100 = 1/4`. Convert percent → fraction and the problem shrinks.

**How to read these questions:**
- "20% of 150" → *of* means multiply → `(20/100)×150 = 30`.
- "A is 25% more than B" → start from B (the thing after "than" is the base = 100). A = 125.
- "Price rose 10% then fell 10%" → it does **NOT** come back to the same value, because the second 10% is taken from a bigger number. Net = `+10 −10 −(10×10)/100 = −1%` (a loss).

**Picture it:** Salary ₹100 → +10% → ₹110 → −10% of 110 = −11 → ₹99. You lost ₹1. *The base changed.* This single idea (the base changing) is the root of percentage, profit, interest, and population questions.

**Memorise this table — it makes you fast:**
| Fraction | % | | Fraction | % |
|---|---|---|---|---|
| 1/2 | 50% | | 1/6 | 16⅔% |
| 1/3 | 33⅓% | | 1/7 | 14²⁄₇% |
| 1/4 | 25% | | 1/8 | 12½% |
| 1/5 | 20% | | 1/9 | 11⅑% |

---

## 2 · Profit & Loss — *"a shopkeeper's diary"*

**The picture:** A shopkeeper **buys** at Cost Price (CP) and **sells** at Selling Price (SP).
- SP > CP → **profit** (he made money).
- SP < CP → **loss**.

**Profit/Loss is ALWAYS calculated on CP** (what he spent). That's the base — like percentage, the base matters.

**Read the words like this:**
| Word in question | What it means |
|---|---|
| Cost Price / "bought for" | CP — the base |
| Selling Price / "sold for" | SP |
| Marked Price / "tag price" / "listed" | MP (the inflated sticker price) |
| Discount | reduction **from MP** |
| Profit% | `(SP−CP)/CP × 100` |

**The flow of a sale:** `CP → (mark up) → MP → (discount) → SP`. Discount comes off MP, profit is measured against CP. Keep these two separate and you'll never confuse them.

**Picture it:** Bag costs ₹100 (CP). Shopkeeper tags it ₹150 (MP). Gives 20% discount → sells at ₹120 (SP). Profit = 120−100 = ₹20 = 20% profit. *Notice the discount was on 150, the profit was on 100.*

**Classic trap:** Two items sold at the same price, one at +10% one at −10% → you **always lose** `(10²/100)% = 1%`. (Same "changing base" idea again.)

---

## 3 · Ratio & Proportion — *"sharing in parts"*

**The picture:** A ratio 2:3 means "for every 2 of mine, you get 3." Think of it as **boxes**: ▢▢ : ▢▢▢. The total has 5 boxes. Each box is worth the same amount.

**The magic word "x":** If two people share money in ratio 2:3, call the amounts **2x and 3x**. The "x" is the value of one box. Total = 5x. If total is ₹500, then 5x=500, so one box x=₹100. First person = 2x = ₹200.

**This "let one part = x" trick solves almost every ratio question.**

**Read it like this:**
- "divide ₹600 in ratio 1:2:3" → parts = 1x+2x+3x = 6x = 600 → x=100 → shares ₹100, ₹200, ₹300.
- "A:B = 2:3, B:C = 4:5, find A:B:C" → make B match. B is 3 and 4 → LCM 12. Scale: A:B = 8:12, B:C = 12:15 → **A:B:C = 8:12:15**.

**Proportion** is just two equal ratios: `a:b = c:d` means `a×d = b×c` (cross-multiply). If "x is to 4 as 6 is to 8" → `x/4 = 6/8` → x=3.

---

## 4 · Averages & Mixtures (Alligation) — *"the balancing point"*

**Average picture:** Average is the **flat level** if you poured everything into one pile and spread it evenly. 3 people with ₹10, ₹20, ₹30 → pour together = ₹60, spread over 3 = ₹20 each. `Average = Total ÷ Count`.

**The key insight:** If the average of a class is 40 and a new student of marks 50 joins, the average goes **up** (because 50 > 40 pulls it up). If marks 30 joins, it pulls **down**. Always sanity-check direction.

**Mixtures / Alligation picture — a see-saw:** You mix cheap tea (₹40/kg) and costly tea (₹60/kg) to get a blend at ₹45/kg. Picture a see-saw with the **mean (45) as the pivot**:

```
   Cheap 40 ●————————●———● Costly 60
                  pivot=45
   distance from 45:  (45−40)=5      (60−45)=15
   ratio of quantities = 15 : 5  =  3 : 1   ← CROSSED over
```

**Rule:** distances cross over. The blend is closer to 40, so you used **more** cheap tea (3 parts cheap : 1 part costly). Closer = more.

This see-saw replaces hard two-variable equations in: mixtures, average speed, profit blending, and even alligation of money.

---

## 5 · Time, Speed & Distance — *"the triangle"*

**The picture:** Three quantities locked together: **Speed = Distance ÷ Time.** Memorise the triangle:

```
        Distance
        ─────────
        Speed │ Time
```
Cover the one you want; the other two show the formula. Want Distance? Cover it → Speed × Time. Want Time? → Distance ÷ Speed.

**The unit trick you'll use constantly:** km/h → m/s, multiply by **5/18**. m/s → km/h, multiply by **18/5**. (A car at 72 km/h = 72×5/18 = 20 m/s.)

**Trains — picture the front of the train:**
- Crossing a **pole** (a dot): the train must travel its **own length**. Distance = length of train.
- Crossing a **platform/bridge**: distance = **train length + platform length** (the front enters and the back must clear the far end).

**Relative speed — picture two cars:**
- Coming **toward** each other → speeds **add** (they close the gap fast). Relative speed = a + b.
- Same direction (one chasing) → speeds **subtract**. Relative speed = a − b.

**Average speed (equal distances, e.g. go-and-return):** It is **NOT** the simple average! Use `2xy/(x+y)`. Why? You spend more *time* at the slower speed, so it drags the average down.

---

## 6 · Boats & Streams — *"swimming in a river"*

**The picture (this one is easy once you see it):** A boat has its own engine speed `b`. The river current (stream) has speed `s`.

- **Downstream** (going *with* the current — the river helps you): speeds add → `b + s`. Fast.
- **Upstream** (going *against* the current — the river fights you): speeds subtract → `b − s`. Slow.

**Picture it:** Walking on a moving airport travelator. Walk with it → you zoom (b+s). Walk against it → you crawl (b−s). Same idea exactly.

**To find the two hidden speeds:**
- Boat speed `b = (downstream + upstream) / 2` (the average).
- Stream speed `s = (downstream − upstream) / 2` (the half-difference).

That's the *whole* chapter. Read "downstream", add. Read "upstream", subtract.

---

## 7 · Time & Work — *"how much per day"*

**The picture:** If A finishes a job in 5 days, then in **1 day** he does **1/5** of the job. That fraction is his **rate**. This "1-day work" idea unlocks everything.

**Working together = add the rates:**
- A alone: 1/5 per day. B alone: 1/10 per day.
- Together in 1 day: 1/5 + 1/10 = 3/10 of the job.
- So together they finish in 10/3 days. (Flip the combined rate.)

**The smarter way — LCM method (avoids fractions):** Let total work = LCM of the days.
- A:5 days, B:10 days → total work = LCM(5,10) = **10 units**.
- A's rate = 10/5 = 2 units/day. B's rate = 10/10 = 1 unit/day.
- Together = 3 units/day → 10 units ÷ 3 = 10/3 days. *Same answer, no fractions.*

**Pipes & cisterns = the same chapter.** A filling pipe is positive work (+), a leak/drain is negative (−). A tank filled by pipe (1/6) with a leak (1/8) → net rate = 1/6 − 1/8.

**Efficiency is inverse to time:** "A is twice as efficient as B" → A takes **half** the time.

---

## 8 · Simple & Compound Interest — *"rent on money"*

**The picture:** When you lend money, the borrower pays you **rent** for using it = interest.

- **Simple Interest (SI):** rent is on the **original amount only**, every year the same. ₹100 at 10% → ₹10 every year, forever flat. `SI = P×R×T/100`.
- **Compound Interest (CI):** rent gets **added to the pile**, then next year's rent is on the *bigger* pile. (The "changing base" idea returns!) `Amount = P(1 + R/100)ᵀ`.

**Picture it (₹100 at 10%):**
| Year | SI | CI |
|---|---|---|
| 1 | +10 → 110 | +10 → 110 |
| 2 | +10 → 120 | +11 (10% of 110) → 121 |
| 3 | +10 → 130 | +12.1 → 133.1 |

CI grows faster because it earns interest *on the interest*. The gap (CI − SI) for 2 years = `P(R/100)²`.

---

## 9 · Mensuration — *"area is floor tiles, volume is water"*

**The picture that makes it click:**
- **Area** = how many 1×1 tiles cover a flat floor. Measured in **square** units. (2D — length × breadth-ish.)
- **Volume** = how much **water** fills a solid container. Measured in **cubic** units. (3D — has depth.)
- **Surface area** = how much **wrapping paper** to cover the outside of a solid.

If a formula has **two** lengths multiplied → it's an **area** (units²). **Three** lengths → **volume** (units³). Use this to catch mistakes instantly.

**The shapes you must know cold:**
| Shape | Area | |
|---|---|---|
| Rectangle | length × breadth | |
| Square | side² | |
| Triangle | ½ × base × height | |
| Circle | πr² | circumference = 2πr |

| Solid | Volume | Surface |
|---|---|---|
| Cube | a³ | 6a² |
| Cuboid (box) | l×b×h | 2(lb+bh+hl) |
| Cylinder (can) | πr²h | curved 2πrh |
| Cone | ⅓πr²h | curved πrl |
| Sphere (ball) | ⁴⁄₃πr³ | 4πr² |

**Read the question:** "paint the walls" → surface area. "water it holds" → volume. "carpet the floor" → area. The verb tells you which formula.

---

## 10 · Trigonometry — *"a right triangle and its angles"*

**The picture:** Stand a ladder against a wall. It makes a right-angled triangle. Pick one angle θ (not the 90° one). The three sides get names *relative to θ*:
- **Opposite** — the side across from θ.
- **Adjacent** — the side next to θ (touching it, not the hypotenuse).
- **Hypotenuse** — the longest, always opposite the 90°.

**The 3 ratios (just labels for side÷side):**
```
sin θ = Opposite / Hypotenuse      ("SOH")
cos θ = Adjacent / Hypotenuse      ("CAH")
tan θ = Opposite / Adjacent        ("TOA")
```
Say **"SOH-CAH-TOA"** out loud. That's the whole foundation.

**The table you MUST memorise (these 5 angles cover ~all SSC questions):**
| θ | 0° | 30° | 45° | 60° | 90° |
|---|---|---|---|---|---|
| sin | 0 | 1/2 | 1/√2 | √3/2 | 1 |
| cos | 1 | √3/2 | 1/√2 | 1/2 | 0 |
| tan | 0 | 1/√3 | 1 | √3 | ∞ |

**Memory trick for sin:** write 0,1,2,3,4 → divide each by 4 → take √ → `0, 1/2, 1/√2, √3/2, 1`. cos is the **same list reversed**. tan = sin÷cos.

**Height & distance (the word problems):** "angle of elevation" = look **up** (top of a tower). "angle of depression" = look **down**. Draw the triangle, mark the angle, label opposite/adjacent, pick sin/cos/tan that uses your known + unknown side. **Always draw the picture** — never solve these in your head.

**Key identity:** `sin²θ + cos²θ = 1` (always true, any angle).

---

## 11 · Probability & Statistics — *"chance and the typical value"*

**Probability picture:** Probability = `(ways you WANT) / (ALL possible ways)`. It's always between 0 (impossible) and 1 (certain).

**Count the universe first:**
- One die → 6 outcomes. Two dice → 6×6 = 36 outcomes.
- A coin → 2. Two coins → 4 (HH, HT, TH, TT).
- A deck → 52 cards (26 red, 26 black; 4 suits of 13; 12 face cards).

**Picture it:** "Probability of rolling a 4 on a die" → 1 way you want (the 4) ÷ 6 total = 1/6. "Rolling an even number" → 3 ways (2,4,6) ÷ 6 = 1/2.

**The two connecting words:**
- **"OR"** (A or B happens) → usually **add** probabilities.
- **"AND"** (both happen) → usually **multiply** probabilities.

**Statistics (the "typical value" trio):**
- **Mean** = average = total ÷ count. (Sensitive to extreme values.)
- **Median** = the **middle** value when sorted. (For even count, average the two middle ones.)
- **Mode** = the value that appears **most often**.

**Picture it:** Salaries [10, 12, 12, 14, 200]. Mean = 49.6 (dragged up by the 200!). Median = 12 (middle, ignores the outlier). Mode = 12 (most frequent). This shows *why* median is "fairer" for skewed data — a classic exam concept.

---

## How to Practise (the part that actually makes you pass)

1. **Pick ONE chapter.** Read its section above until the picture is automatic.
2. **Do 10 PYQs** from your `PYQ-Collection/` on that single topic. Not mixed.
3. For every wrong answer, write **one sentence**: "I missed it because ___." Patterns will emerge (usually "didn't write given vs asked" or "used wrong base").
4. **Speed comes last.** First get it right slowly. Speed is just right-method repeated.
5. **Re-derive the see-saw (alligation) and the speed triangle from memory** weekly. These two pictures alone cover a huge slice of the paper.

---

### The 5 pictures to burn into memory
1. **Changing base** (percent/profit/CI — the base moves, that's why ±x% ≠ 0).
2. **Boxes = x** (ratio — let one part be x).
3. **See-saw** (alligation — distances cross, closer side = more quantity).
4. **Speed triangle** (D / S·T — cover what you want).
5. **SOH-CAH-TOA + the angle table** (all of trig).

> Master these five pictures and the "I don't know how to start" feeling is gone. Formulas are in `Quant_Cheatsheet.md` for the exact numbers — but *seeing* the question is what you build here.
