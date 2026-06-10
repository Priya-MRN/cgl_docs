# Quant Worked Examples — *See It → Set It Up → Solve It*

> **Companion to** `Quant_Concepts_From_Zero.md`. That sheet taught you the **picture**. This sheet shows the picture *in action* on real questions, step by step, the same way you should think on paper.
>
> **Read every example like this:** cover the solution, try the **🎯 Picture** and **✍️ Setup** yourself first, *then* check. The thinking matters more than the answer.
>
> **Every solution follows 4 steps:**
> **🎯 Picture** (what's happening) → **✍️ Setup** (given vs asked) → **🧮 Solve** (the formula) → **✅ Answer** + the lesson.

---

## 1 · Percentages

### Example 1.1
**Q:** A student scored 45 marks and failed by 5 marks. Passing is 25% of total. Find total marks.

🎯 **Picture:** He needed the pass mark. He got 45 but was 5 short → pass mark = 45+5 = 50. And 50 is 25% of the total.
✍️ **Setup:** 25% of Total = 50. *Asked:* Total.
🧮 **Solve:** `25/100 × Total = 50` → `Total = 50 × 100/25 = 200`.
✅ **Answer: 200.** *Lesson: "failed by 5" means he was 5 below the pass line — add it.*

### Example 1.2 (the changing-base trap)
**Q:** A's salary is 20% more than B's. By what % is B's salary less than A's?

🎯 **Picture:** The base flips. "A is 20% more than B" → base is **B**. The second question's base is **A** — a different, bigger number, so the answer is NOT 20%.
✍️ **Setup:** Let B = 100 → A = 120.
🧮 **Solve:** B is less than A by `(120−100)/120 × 100 = 1000/120 = 16⅔%`.
✅ **Answer: 16⅔%.** *Lesson: always restart from the new base. "Less than A" means divide by A.*

---

## 2 · Profit & Loss

### Example 2.1
**Q:** A man buys a watch for ₹800 and sells it for ₹920. Find profit %.

🎯 **Picture:** Shopkeeper's diary. CP=800 (spent), SP=920 (got back). He gained 120. Profit % is on CP.
✍️ **Setup:** CP=800, SP=920. *Asked:* profit%.
🧮 **Solve:** Profit = 920−800 = 120. `Profit% = 120/800 × 100 = 15%`.
✅ **Answer: 15%.** *Lesson: divide gain by CP (the base), never by SP.*

### Example 2.2 (MP → discount → SP)
**Q:** Marked price ₹1500, discount 20%, and he still makes 20% profit. Find the cost price.

🎯 **Picture:** Flow is CP → MP(1500) → 20% off → SP. First find SP from MP, then work back to CP.
✍️ **Setup:** MP=1500, discount 20%, profit 20%.
🧮 **Solve:**
- SP = MP × (1 − 20/100) = 1500 × 0.8 = **1200**.
- SP = CP × (1 + 20/100) → 1200 = CP × 1.2 → CP = 1200/1.2 = **1000**.
✅ **Answer: CP = ₹1000.** *Lesson: discount works on MP; profit works on CP — handle them in separate steps.*

---

## 3 · Ratio & Proportion

### Example 3.1 (let one part = x)
**Q:** ₹720 is divided among A, B, C in ratio 2:3:4. Find B's share.

🎯 **Picture:** Boxes. 2 boxes + 3 boxes + 4 boxes = 9 boxes total. Each box has equal value x.
✍️ **Setup:** 2x + 3x + 4x = 720.
🧮 **Solve:** 9x = 720 → x = 80. B = 3x = 3×80 = **240**.
✅ **Answer: ₹240.** *Lesson: add the ratio numbers to get total parts, find one part, then scale.*

### Example 3.2 (combining ratios)
**Q:** A:B = 2:3 and B:C = 4:5. Find A:B:C.

🎯 **Picture:** B appears in both but as different numbers (3 and 4). Make B match using LCM.
✍️ **Setup:** B = 3 and B = 4 → LCM(3,4) = 12.
🧮 **Solve:** Scale first ratio ×4: A:B = 8:12. Scale second ×3: B:C = 12:15. Now B matches → **A:B:C = 8:12:15**.
✅ **Answer: 8:12:15.** *Lesson: the bridge value (B) must be made equal before you can chain ratios.*

---

## 4 · Averages & Mixtures (the See-Saw)

### Example 4.1 (average direction check)
**Q:** Average of 10 numbers is 25. If one number 25 is replaced by 35, find the new average.

🎯 **Picture:** One number went up by 10, spread over 10 numbers → average rises by 10/10 = 1.
✍️ **Setup:** Old total = 10×25 = 250. New total = 250 − 25 + 35 = 260.
🧮 **Solve:** New average = 260/10 = **26**.
✅ **Answer: 26.** *Lesson: change in total ÷ count = change in average. Sanity check: it went up, as expected.*

### Example 4.2 (alligation see-saw)
**Q:** In what ratio must rice at ₹30/kg be mixed with rice at ₹40/kg to get a mixture worth ₹34/kg?

🎯 **Picture:** See-saw with pivot at 34. Distances: from 30 it's 4; from 40 it's 6. The mixture is closer to 30, so we used **more** ₹30 rice.
✍️ **Setup:**
```
   30 ●———————●————● 40
       (4)  34  (6)
```
🧮 **Solve:** Cross the distances → cheap : dear = 6 : 4 = **3 : 2**.
✅ **Answer: 3:2.** *Lesson: distances cross over; the side closer to the mean gets the larger quantity.*

---

## 5 · Time, Speed & Distance

### Example 5.1 (unit conversion + triangle)
**Q:** A car travels 90 km in 1.5 hours. Find speed in m/s.

🎯 **Picture:** Speed triangle — cover Speed → Distance/Time. Then convert km/h to m/s with ×5/18.
✍️ **Setup:** D=90 km, T=1.5 h.
🧮 **Solve:** Speed = 90/1.5 = 60 km/h. In m/s = 60 × 5/18 = **16⅔ m/s** (≈16.67).
✅ **Answer: 16⅔ m/s.** *Lesson: km/h → m/s always ×5/18.*

### Example 5.2 (train + platform)
**Q:** A 120 m long train at 54 km/h crosses a 180 m platform. How long does it take?

🎯 **Picture:** The front enters, the back must clear the far end → train covers **its own length + the platform** = 120+180 = 300 m.
✍️ **Setup:** Distance = 300 m. Speed = 54 km/h = 54×5/18 = 15 m/s.
🧮 **Solve:** Time = Distance/Speed = 300/15 = **20 seconds**.
✅ **Answer: 20 s.** *Lesson: platform problems → add both lengths. Convert speed to m/s to match metres.*

### Example 5.3 (average speed — NOT simple average)
**Q:** A man goes to a town at 40 km/h and returns at 60 km/h. Find average speed.

🎯 **Picture:** Same distance each way, but more *time* spent at 40 → it drags the average below 50.
✍️ **Setup:** Equal distances → use harmonic mean `2xy/(x+y)`.
🧮 **Solve:** `2×40×60 / (40+60) = 4800/100 = **48 km/h**`.
✅ **Answer: 48 km/h** (not 50!). *Lesson: equal distance → 2xy/(x+y). It's always less than the simple average.*

---

## 6 · Boats & Streams

### Example 6.1
**Q:** A boat goes 30 km downstream in 2 hours and 30 km upstream in 3 hours. Find boat speed and stream speed.

🎯 **Picture:** Travelator. Downstream the river helps (fast), upstream it fights (slow). First find each speed, then split.
✍️ **Setup:** Downstream speed = 30/2 = 15 km/h. Upstream = 30/3 = 10 km/h.
🧮 **Solve:**
- Boat `b = (down + up)/2 = (15+10)/2 = **12.5 km/h**`.
- Stream `s = (down − up)/2 = (15−10)/2 = **2.5 km/h**`.
✅ **Answer: boat 12.5, stream 2.5.** *Lesson: boat = average of the two; stream = half their difference.*

---

## 7 · Time & Work

### Example 7.1 (LCM method — no fractions)
**Q:** A can do a job in 12 days, B in 18 days. Working together, how long?

🎯 **Picture:** Let total work = LCM(12,18) = 36 units. Each does so many units/day; together add the rates.
✍️ **Setup:** Total = 36 units. A's rate = 36/12 = 3/day. B's rate = 36/18 = 2/day.
🧮 **Solve:** Together = 3+2 = 5 units/day → time = 36/5 = **7.2 days** (7⅕ days).
✅ **Answer: 7⅕ days.** *Lesson: LCM as total work kills all the messy fractions.*

### Example 7.2 (pipes — one drains)
**Q:** Pipe A fills a tank in 6 h, pipe B empties it in 8 h. Both open — time to fill?

🎯 **Picture:** A is positive (+), B is a leak (−). Net rate is the difference. Use LCM(6,8)=24 units.
✍️ **Setup:** A = 24/6 = +4/h. B = 24/8 = −3/h.
🧮 **Solve:** Net = 4 − 3 = 1 unit/h → fills 24 units in **24 hours**.
✅ **Answer: 24 hours.** *Lesson: draining pipe = negative rate; subtract it.*

---

## 8 · Simple & Compound Interest

### Example 8.1 (SI)
**Q:** Find SI on ₹5000 at 8% per year for 3 years.

🎯 **Picture:** Flat rent every year on the original ₹5000.
✍️ **Setup:** P=5000, R=8, T=3.
🧮 **Solve:** `SI = P×R×T/100 = 5000×8×3/100 = **1200**`.
✅ **Answer: ₹1200.** *Lesson: SI is linear — same interest each year.*

### Example 8.2 (CI vs SI difference)
**Q:** Find the difference between CI and SI on ₹8000 at 10% for 2 years.

🎯 **Picture:** CI earns interest on the interest, so it's slightly more. For exactly 2 years there's a shortcut.
✍️ **Setup:** P=8000, R=10, T=2.
🧮 **Solve:** `Difference = P×(R/100)² = 8000×(10/100)² = 8000×0.01 = **80**`.
✅ **Answer: ₹80.** *Lesson: 2-year CI−SI difference = P(R/100)². Memorise this — it's a frequent shortcut.*

---

## 9 · Mensuration

### Example 9.1 (area — "carpet the floor")
**Q:** A rectangular room is 8 m by 5 m. Cost of carpeting at ₹50/m². Find total cost.

🎯 **Picture:** Carpet covers the **floor** → area (two lengths multiplied → units²).
✍️ **Setup:** Area = 8×5 = 40 m². Rate = ₹50/m².
🧮 **Solve:** Cost = 40 × 50 = **₹2000**.
✅ **Answer: ₹2000.** *Lesson: "carpet/floor/tile" = area.*

### Example 9.2 (volume — "water it holds")
**Q:** A cylindrical tank has radius 7 m and height 10 m. How much water can it hold? (π = 22/7)

🎯 **Picture:** Water *fills* it → volume (three dimensions → units³). Cylinder volume = πr²h.
✍️ **Setup:** r=7, h=10, π=22/7.
🧮 **Solve:** `V = πr²h = 22/7 × 7 × 7 × 10 = 22 × 7 × 10 = **1540 m³**`.
✅ **Answer: 1540 m³.** *Lesson: "holds water" = volume; use π=22/7 when radius is a multiple of 7.*

---

## 10 · Trigonometry

### Example 10.1 (use the angle table)
**Q:** Find the value of `sin 30° + cos 60°`.

🎯 **Picture:** Read straight off the memorised table.
✍️ **Setup:** sin 30° = 1/2, cos 60° = 1/2.
🧮 **Solve:** 1/2 + 1/2 = **1**.
✅ **Answer: 1.** *Lesson: the 5-angle table answers most direct trig questions instantly.*

### Example 10.2 (height & distance — DRAW IT)
**Q:** From a point 30 m from the base of a tower, the angle of elevation of the top is 60°. Find the tower's height.

🎯 **Picture:** Draw the right triangle. You stand 30 m away (that's the **adjacent** side, on the ground). Tower height is the **opposite** side (going up). Angle 60° at your feet. Which ratio uses opposite & adjacent? → **tan**.
```
        |\
        | \
height  |  \   60°
        |___\_______
          30 m
```
✍️ **Setup:** tan 60° = opposite/adjacent = height/30. And tan 60° = √3.
🧮 **Solve:** √3 = height/30 → height = 30√3 ≈ **51.96 m**.
✅ **Answer: 30√3 m.** *Lesson: "elevation" = look up. Label opposite/adjacent, pick tan (it uses both ground distance and height).*

---

## 11 · Probability & Statistics

### Example 11.1 (count the universe)
**Q:** Two dice are rolled. Find the probability that the sum is 7.

🎯 **Picture:** Total universe = 6×6 = 36 outcomes. Now count the ways to make 7.
✍️ **Setup:** Sum 7 from: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) → **6 ways**.
🧮 **Solve:** P = favourable/total = 6/36 = **1/6**.
✅ **Answer: 1/6.** *Lesson: always count the full universe first (36 for two dice), then count what you want.*

### Example 11.2 (mean vs median vs mode)
**Q:** Find mean, median, and mode of: 4, 7, 7, 9, 13.

🎯 **Picture:** Mean = pour-and-spread average. Median = middle when sorted. Mode = most repeated.
✍️ **Setup:** Already sorted, 5 numbers (odd count → median is the 3rd).
🧮 **Solve:**
- Mean = (4+7+7+9+13)/5 = 40/5 = **8**.
- Median = middle (3rd value) = **7**.
- Mode = appears most = **7** (appears twice).
✅ **Answer: mean 8, median 7, mode 7.** *Lesson: sort first; median is the middle for odd count, average of two middles for even count.*

---

## How to Drill These

1. **Cover the solution.** Try **🎯 Picture** and **✍️ Setup** on your own — that's where the real skill is.
2. If your *setup* matched mine, you've already won — the formula is the easy part.
3. After all 11, open `PYQ-Collection/` and do 5 fresh questions per topic **using the same 4-step layout on paper** (Picture → Setup → Solve → Answer).
4. Keep a "mistake sentence" log: one line per wrong answer saying *which step* you slipped on. Almost always it's a rushed **Setup**.

> **The whole secret:** slow down on **🎯 Picture** and **✍️ Setup**. Students who fail quant rush to a formula before they understand the scene. You won't — you'll draw the picture first, every time.
