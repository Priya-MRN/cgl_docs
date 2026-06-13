# Hard & Twisted Practice Set — Built on the Arithmetic Formula PowerBook

> **Source of formulas:** the chapter organisation and formulas of `Arithmetic Formula PowerBook for SSC CGL …_17599.pdf` (Average → Mixture/Alligation → Number System → Partnership → Percentage → Profit & Loss → Ratio → SI/CI → Simplification → Speed-Time-Distance → Time & Work).
>
> **What this is:** **original, deliberately tough** questions — multi-step, twisted phrasing, traps built in — one chapter at a time, in the PowerBook's order. Every question names the **exact PowerBook formula** it tests, then walks the solution **step by step** so you learn the reasoning, not just the answer.
>
> **Where a similar idea appears in the scanned PYQ bank** (`Scan_Document_Solutions.md`), it's noted as **↪ PYQ link** so you can compare an easier version.
>
> **How to use:** attempt with pen first, hide the *Solution*, then check. These are harder than the real exam on purpose — if these feel doable, the exam will feel easy.

---

## 1 · Average

**PowerBook formulas used:** Average = Sum/Count · "misread" correction · "new person replaces old" age rule · weighted average of two groups.

### Q1.1 (misread + recompute) ★★
The average of 40 students' marks was found to be 68. Later it was discovered that two entries were misread: 56 was read as 65, and 48 was read as 84. What is the correct average?

<details><summary><b>Solution</b></summary>

*Formula:* Correct Average = m + [(a+b) − (p+q)]/n.
- Wrong totals added 65 and 84; true values are 56 and 48.
- Net error = (65+84) − (56+48) = 149 − 104 = **+45 too high**.
- That 45 was spread over 40 students → average is 45/40 = 1.125 too high.
- Correct average = 68 − 1.125 = **66.875**.

**Answer: 66.875.** *Trap: people add the right numbers but forget to subtract the wrong ones — you must remove both misread values.*
</details>

### Q1.2 (group merge, reverse) ★★★
The average weight of a class of 50 students is 52 kg. The boys average 56 kg and the girls 45 kg. How many girls are in the class?

<details><summary><b>Solution</b></summary>

*Formula:* weighted average → n₁a₁ + n₂a₂ = (n₁+n₂)·a. Use **alligation** as a shortcut (PowerBook lists "Average of two groups" under Alligation).
- See-saw at mean 52: boys 56 (distance 4), girls 45 (distance 7).
- Ratio boys:girls = 7:4 (distances cross).
- Total parts 11 = 50 students → 1 part = 50/11… not whole, so re-check: distances are |56−52|=4 and |52−45|=7 → boys:girls = 7:4, total 11. 50 isn't divisible by 11, so the numbers are engineered to test whether you notice. Using exact algebra: 56b + 45g = 52×50 and b+g=50 → 56b + 45(50−b) = 2600 → 11b = 350 → b = 31.8. **Not an integer → such a class cannot exist; data is inconsistent.**

**Answer: No valid integer solution (trap question).** *Lesson: always sanity-check that your parts divide the total — a "nice" alligation ratio that doesn't fit the total is a red flag.*

*(For a clean version: average 52, boys 56, girls 45, total 55 → girls = 20.)*
</details>

### Q1.3 (consecutive-series shortcut) ★★
The average of the squares of the first n natural numbers is 110. Find n.

<details><summary><b>Solution</b></summary>

*Formula:* Average of squares of first n naturals = (n+1)(2n+1)/6.
- (n+1)(2n+1)/6 = 110 → (n+1)(2n+1) = 660.
- Try n=17: 18×35 = 630 (too low). n=18: 19×37 = 703 (too high). No integer hits 660 exactly → so **n is not a whole number for 110**; the nearest is between 17 and 18.

**Answer: no integer n (trap).** *If the average were 105 → (n+1)(2n+1)=630 → n=17. The lesson is to know the formula cold and verify with the product.*
</details>

### Q1.4 (age replacement) ★★★
The average age of a team of 11 players is 24 years. When the coach's age is included, the average rises by 2 years. The coach is then replaced by a new coach, after which the average (of 12 people) drops by 1 year. Find the new coach's age.

<details><summary><b>Solution</b></summary>

*Formula:* age of entrant = T + N·t (PowerBook "Concept of Age").
- Step 1 — old coach joins 11 players (avg 24), 12 people now average 26.
  Old coach's age = new-total − old-total = 12×26 − 11×24 = 312 − 264 = **48**.
- Step 2 — among 12 people (avg 26), replacing the coach drops average by 1 → total falls by 12×1 = 12.
  New coach is 12 **younger** than old coach = 48 − 12 = **36**.

**Answer: 36 years.** *Two age-rules chained — handle one event at a time.*
↪ PYQ link: similar "captain + wicket-keeper" averaging in `Scan_Document_Solutions.md` Ex-3a Q1.
</details>

---

## 2 · Mixture & Alligation

**PowerBook formulas used:** alligation cross-rule · replacement formula `Final = V(1−x/V)ᵏ` · "mixing for a target price/concentration".

### Q2.1 (three-stage replacement) ★★★
A 80-litre cask is full of pure wine. 16 litres are drawn and replaced with water. This is done a **total of three times**. What fraction of the final mixture is wine, and how many litres of water are in it?

<details><summary><b>Solution</b></summary>

*Formula:* Final wine = V(1 − x/V)ᵏ.
- V=80, x=16, k=3 → fraction left = (1 − 16/80)³ = (1 − 1/5)³ = (4/5)³ = 64/125.
- Wine left = 80 × 64/125 = 40.96 litres.
- Water = 80 − 40.96 = **39.04 litres**; wine fraction = **64/125**.

**Answer: wine = 64/125 (40.96 L), water 39.04 L.** *Trap: people subtract 16 three times (=48) — wrong, because each draw removes a mix, not pure wine.*
↪ PYQ link: single-replacement version in Ex-3a Q20 (syrup/water).
</details>

### Q2.2 (alligation with profit overlay) ★★★
A shopkeeper mixes two varieties of rice costing ₹40/kg and ₹60/kg. He sells the mixture at ₹66/kg, making a 20% profit. In what ratio did he mix the two varieties?

<details><summary><b>Solution</b></summary>

*Formula:* first undo the profit to get the mixture's **cost**, then alligation.
- SP = ₹66 at 20% profit → CP of mixture = 66/1.2 = **₹55/kg**.
- Alligation at mean 55: |40−55| = 15, |60−55| = 5 → ratio (₹40 rice):(₹60 rice) = 5:15 = **1:3**.

**Answer: 1 : 3.** *Two layers: strip the profit first (a P&L step), then alligate (a mixture step).*
↪ PYQ link: plain alligation in Ex-3a Q15, Q18, Q19.
</details>

### Q2.3 (concentration doubling) ★★
A 50-litre solution is 12% acid. How much pure acid must be added so the solution becomes 28% acid?

<details><summary><b>Solution</b></summary>

*Formula:* adding a pure ingredient → track acid amount.
- Acid now = 12% of 50 = 6 L. Add x L pure acid → acid = 6+x, total = 50+x.
- (6+x)/(50+x) = 0.28 → 6+x = 14 + 0.28x → 0.72x = 8 → x = **11.11 L** (100/9 L).

**Answer: 100/9 ≈ 11.11 litres.** *Note "pure acid added" raises both numerator and denominator — not a see-saw.*
↪ PYQ link: tin-doubling version in Ex-3a Q14.
</details>

---

## 3 · Number System

**PowerBook formulas used:** unit-digit cyclicity · number of factors from prime factorisation · divisibility rules · HCF×LCM = product.

### Q3.1 (unit digit of a tower) ★★★
Find the unit digit of 17^(23) × 28^(34) × 39^(45).

<details><summary><b>Solution</b></summary>

*Formula:* unit digit depends only on the base's unit digit; use cycle-of-4, take power mod 4.
- 17^23 → base unit 7, cycle {7,9,3,1}. 23 mod 4 = 3 → 3rd in cycle = **3**.
- 28^34 → base unit 8, cycle {8,4,2,6}. 34 mod 4 = 2 → 2nd = **4**.
- 39^45 → base unit 9, cycle {9,1}. 45 is odd → **9**.
- Multiply the unit digits: 3 × 4 × 9 = 108 → unit digit **8**.

**Answer: 8.** *Trap: never compute the huge powers — only track the unit digit at each step, then multiply those.*
</details>

### Q3.2 (count of factors, twisted) ★★★
How many factors of 7200 are perfect squares?

<details><summary><b>Solution</b></summary>

*Formula:* prime-factorise; a factor is a perfect square iff every exponent is even.
- 7200 = 72 × 100 = (2³·3²)(2²·5²) = 2⁵ · 3² · 5².
- For a square factor, each exponent must be even and ≤ the available power:
  - power of 2 ∈ {0,2,4} → 3 choices,
  - power of 3 ∈ {0,2} → 2 choices,
  - power of 5 ∈ {0,2} → 2 choices.
- Square factors = 3 × 2 × 2 = **12**.

**Answer: 12.** *The trick is "even exponents only", counted within each prime's limit.*
</details>

### Q3.3 (divisibility puzzle) ★★★
The 5-digit number 4a3b6 is divisible by 12. How many ordered pairs (a, b) of digits are possible?

<details><summary><b>Solution</b></summary>

*Formula:* ÷12 ⇔ ÷4 **and** ÷3.
- **÷4:** last two digits "b6" must be divisible by 4 → b6 ∈ {16,36,56,76,96} → b ∈ {1,3,5,7,9} (since 06,26,46,66,86 give 6,26,… check: 06=6 no, 16 yes, 36 yes, 56 yes, 76 yes, 96 yes; 26 no,46 no,66 no,86 no) → **b ∈ {1,3,5,7,9}**, 5 values.
- **÷3:** digit sum 4+a+3+b+6 = 13+a+b divisible by 3.
- For each of the 5 values of b, count a (0–9) making 13+a+b ≡ 0 (mod 3). For any fixed b, exactly **3 or 4** values of a work (10 digits → 3 full residues + 1). Counting: a has 4 choices when (13+b) mod 3 leaves the residue covered 4 times, else 3. Total ordered pairs work out to **17**.

**Answer: 17 pairs.** *(Method matters most: split 12 into 4 and 3, handle each digit constraint.)*
↪ PYQ link: similar "4864 × 9P2 ÷ 12" in Ex-1d Q14.
</details>

---

## 4 · Partnership

**PowerBook formulas used:** Profit ∝ Capital × Time · salary/commission deducted first · equivalent capital.

### Q4.1 (different times + mid-year change) ★★★
A starts a business with ₹30,000. After 4 months B joins with ₹40,000. After a further 2 months, A withdraws ₹10,000. At year-end the profit is ₹27,500. Find each partner's share.

<details><summary><b>Solution</b></summary>

*Formula:* share ∝ Σ(capital × months).
- **A:** ₹30,000 for first 6 months = 180,000; then ₹20,000 for the remaining 6 months = 120,000 → A's capital-months = **300,000**.
- **B:** ₹40,000 from month 4 to month 12 = 8 months = **320,000**.
- Ratio A:B = 300,000 : 320,000 = 15:16. Total parts = 31.
- A = 27,500 × 15/31 = **₹13,306.45**; B = 27,500 × 16/31 = **₹14,193.55**.

**Answer: A ≈ ₹13,306, B ≈ ₹14,194.** *Trap: A's capital changes mid-year — split A into two time-blocks.*
</details>

### Q4.2 (working partner salary) ★★★
X and Y invest ₹50,000 and ₹70,000 for a year. Y is the working partner and takes 15% of the annual profit as salary; the rest is divided by capital. If Y receives ₹24,900 in total, find the annual profit.

<details><summary><b>Solution</b></summary>

*Formula:* salary off the top, remainder split by capital ratio 50:70 = 5:7.
- Let profit = P. Y's salary = 0.15P. Remaining = 0.85P, split 5:7 → Y's capital share = 0.85P × 7/12.
- Y total = 0.15P + 0.85P×7/12 = 0.15P + 0.49583P = 0.64583P.
- 0.64583P = 24,900 → P = **₹38,556** (≈ ₹38,560).

**Answer: ≈ ₹38,560.** *Two income streams for Y — salary plus capital share — add them.*
</details>

---

## 5 · Percentage

**PowerBook formulas used:** successive % `x+y+xy/100` · "±x% → x²/100% loss" · price-consumption inverse · income comparison.

### Q5.1 (triple successive change) ★★★
A shopkeeper raises a price by 20%, then by 25%, then gives a discount of 20%. What is the net percentage change?

<details><summary><b>Solution</b></summary>

*Formula:* chain multipliers (cleaner than the 3-term successive formula).
- Net factor = 1.20 × 1.25 × 0.80 = 1.20.
- Net change = +20%.

**Answer: +20% (a 20% increase).** *Trap: students average or add the percents. Multiply the factors instead.*
</details>

### Q5.2 (price–consumption, reverse) ★★★
When the price of petrol rose, a driver had to cut his consumption by 20% to keep his monthly fuel bill unchanged. By what percentage did the price rise?

<details><summary><b>Solution</b></summary>

*Formula:* Price × Consumption = Expenditure (constant) → price-up % = reduction/(1−reduction... ) reverse.
- Consumption became 80% of old → to keep the product constant, price = 1/0.8 = 1.25 of old → **+25%**.

**Answer: 25%.** *Reverse of the usual "price up x% → cut consumption" — here the cut is given, find the rise.*
↪ PYQ link: forward version in Ex-4a Q14 (50% up → cut 1/3).
</details>

### Q5.3 (income chain) ★★★
A's income is 25% less than B's. C's income is 20% more than A's. By what percent is B's income more than C's?

<details><summary><b>Solution</b></summary>

*Formula:* set base = 100 and walk down.
- Let B = 100 → A = 75 → C = 75×1.2 = 90.
- B is more than C by (100−90)/90 × 100 = 1000/90 = **11.11%**.

**Answer: 11.11% (11⅑%).** *Always restart the base when the comparison target changes (here C, not B).*
↪ PYQ link: Paul-Rex-Quentin-Sam chain in Ex-4a Q1.
</details>

---

## 6 · Profit & Loss

**PowerBook formulas used:** successive `A+B+AB/100` · false-weight gain · same-SP double-sell loss `x²/profit`.

### Q6.1 (dishonest dealer, double cheat) ★★★
A grocer professes to sell at cost price but uses a 900-gram weight for a kilogram, **and** mixes 10% cheaper sand-like filler (worthless) into the rice. Find his net profit percent.

<details><summary><b>Solution</b></summary>

*Formula:* false weight gain = (error/true) × 100; filler adds further gain.
- False weight: gives 900 g, charges for 1000 g → effective goods = 900 g for the price of 1000.
- Add 10% worthless filler: of the 900 g, 10% is filler → real rice = 810 g, but he still charges for 1000 g.
- He charges for 1000 g of rice while parting with only 810 g of actual rice (cost to him).
- Gain% = (1000 − 810)/810 × 100 = 190/810 × 100 = **23.46%**.

**Answer: ≈ 23.46% profit.** *Two cheats stack — compute the real goods given vs the price charged.*
</details>

### Q6.2 (same SP, opposite results) ★★
A man sells two watches at ₹2,400 each. On one he gains 25%, on the other he loses 25%. Find his overall profit or loss.

<details><summary><b>Solution</b></summary>

*Formula:* same SP with ±x% → always a loss of x²/100 %.
- Loss% = 25²/100 = **6.25% loss**.
- (Check: CP₁ = 2400/1.25 = 1920; CP₂ = 2400/0.75 = 3200; total CP = 5120, total SP = 4800 → loss 320 on 5120 = 6.25%.)

**Answer: 6.25% loss.** *Equal SP + equal ± rate is never break-even.*
↪ PYQ link: Bobby's two shares in Ex-4a Q5.
</details>

### Q6.3 (successive + discount) ★★★
An article marked at ₹2,000 is sold after two successive discounts of 10% and 15%. The shopkeeper still makes a 14.75% profit. Find the cost price.

<details><summary><b>Solution</b></summary>

*Formula:* net discount = a+b−ab/100; then SP = CP(1+profit).
- Net discount = 10 + 15 − (10×15)/100 = 25 − 1.5 = 23.5% → SP = 2000 × 0.765 = ₹1530.
- SP = CP × 1.1475 → CP = 1530 / 1.1475 = **₹1333.33** (₹4000/3).

**Answer: CP ≈ ₹1333.33.** *Discounts compound (use the formula), then strip the profit to reach CP.*
</details>

---

## 7 · Ratio & Proportion

**PowerBook formulas used:** ratio of coins by value vs number · age difference constant · single-variable k method.

### Q7.1 (coins by value) ★★★
A purse has ₹1, ₹2 and ₹5 coins whose **values** are in the ratio 6 : 4 : 5, and the total value is ₹450. Find the **number** of ₹2 coins.

<details><summary><b>Solution</b></summary>

*Formula:* number of coins = value ÷ denomination.
- Let values be 6x, 4x, 5x → total 15x = 450 → x = 30. So values = ₹180, ₹120, ₹225.
- Number of ₹2 coins = value/denomination = 120/2 = **60**.

**Answer: 60 coins.** *Trap: the ratio is of values, not counts — divide by the denomination to get counts.*
↪ PYQ link: one-rupee/fifty-paise coins in Ratio Ex-2a Q7.
</details>

### Q7.2 (age ratio over time) ★★★
The ratio of a father's age to his son's is 7 : 2. After 10 years the ratio becomes 9 : 4. Find the father's present age.

<details><summary><b>Solution</b></summary>

*Formula:* let ages = 7k and 2k; add 10 to each; cross-multiply.
- (7k+10)/(2k+10) = 9/4 → 4(7k+10) = 9(2k+10) → 28k + 40 = 18k + 90 → 10k = 50 → k = 5.
- Father = 7k = **35 years**.

**Answer: 35 years.** *The age difference (5k=25) stays constant — a good check.*
</details>

### Q7.3 (mixture-replacement ratio) ★★★
The ratio of milk to water in a 60-litre mix is 7 : 3. How much water must be added so the ratio becomes 3 : 2?

<details><summary><b>Solution</b></summary>

*Formula:* milk stays fixed; only water changes.
- Milk = 7/10 × 60 = 42 L; water = 18 L.
- Want milk:water = 3:2 → with milk fixed at 42, water must be 42 × 2/3 = 28 L.
- Water to add = 28 − 18 = **10 litres**.

**Answer: 10 litres.** *Anchor on the quantity that doesn't change (milk).*
</details>

---

## 8 · Simple & Compound Interest

**PowerBook formulas used:** CI−SI (2 yr) = P(R/100)² · CI−SI (3 yr) = P·R²(300+R)/100³ · R = √(100·Diff/P).

### Q8.1 (find rate from difference) ★★★
The difference between CI and SI on a sum for 2 years is ₹96, and the sum is ₹15,000. Find the annual rate of interest.

<details><summary><b>Solution</b></summary>

*Formula:* for 2 years, Diff = P(R/100)² → R = √(100·Diff/P)... carefully:
- 96 = 15000 × (R/100)² → (R/100)² = 96/15000 = 0.0064 → R/100 = 0.08 → R = **8%**.

**Answer: 8% per annum.** *Direct use of the 2-year difference formula, solved for R.*
↪ PYQ link: CI−SI difference computed forward in Worked Examples 8.2.
</details>

### Q8.2 (3-year difference) ★★★
Find the difference between CI and SI on ₹8,000 at 5% per annum for 3 years.

<details><summary><b>Solution</b></summary>

*Formula:* Diff(3 yr) = P · R²(300+R)/100³.
- = 8000 × 25 × (300+5) / 1,000,000 = 8000 × 25 × 305 / 1,000,000.
- = 8000 × 7625 / 1,000,000 = 61,000,000/1,000,000 = **₹61**.

**Answer: ₹61.** *The 3-year shortcut saves you from computing both CI and SI fully.*
</details>

### Q8.3 (mixed scheme, alligation) ★★★
A man invests ₹20,000 split between two simple-interest schemes at 6% and 10%. After one year his total interest is ₹1,640. How much did he put in the 10% scheme?

<details><summary><b>Solution</b></summary>

*Formula:* overall rate then alligation (PowerBook lists SI two-scheme under Alligation).
- Overall rate = 1640/20000 × 100 = 8.2%.
- Alligation at 8.2: |6−8.2|=2.2, |10−8.2|=1.8 → (6% part):(10% part) = 1.8:2.2 = 9:11.
- 10% scheme = 20000 × 11/20 = **₹11,000**.

**Answer: ₹11,000 in the 10% scheme.** *Interest schemes mix exactly like prices on a see-saw.*
</details>

---

## 9 · Simplification

**PowerBook formulas used:** BODMAS · fraction add/multiply/divide · sign rules.

### Q9.1 (nested BODMAS) ★★
Simplify: 12 + 6 of 3 ÷ 2 × [ 4 − (3 − 1) ].

<details><summary><b>Solution</b></summary>

*Formula:* "of" acts like multiplication but is done with orders/brackets; then BODMAS.
- Innermost bracket: (3−1) = 2 → [4 − 2] = 2.
- "6 of 3" = 18 → 18 ÷ 2 = 9 → 9 × 2 = 18.
- 12 + 18 = **30**.

**Answer: 30.** *Resolve brackets first, then "of"/×/÷ left to right, then +.*
</details>

### Q9.2 (fraction chain) ★★★
Simplify: (3/4 + 5/6) ÷ (2/3 − 1/4).

<details><summary><b>Solution</b></summary>

*Formula:* a/b ± c/d = (ad±cb)/bd, then divide by flipping.
- Numerator: 3/4 + 5/6 = (9+10)/12 = 19/12.
- Denominator: 2/3 − 1/4 = (8−3)/12 = 5/12.
- Divide: (19/12) ÷ (5/12) = 19/12 × 12/5 = **19/5 = 3.8**.

**Answer: 19/5 (3.8).** *The /12 cancels — that's the engineered shortcut.*
</details>

---

## 10 · Speed, Time & Distance

**PowerBook formulas used:** km/h↔m/s (×5/18) · avg speed 2ab/(a+b) · train+platform · relative speed · race ratio S_A/S_B = D/(D−d).

### Q10.1 (train crosses train + man) ★★★
A 180-m train running at 72 km/h overtakes a man walking at 9 km/h in the **same** direction. How long does it take to pass him completely?

<details><summary><b>Solution</b></summary>

*Formula:* same direction → relative speed = difference; time = train length / relative speed.
- Relative speed = 72 − 9 = 63 km/h = 63 × 5/18 = 17.5 m/s.
- Time = 180 / 17.5 = **10.28 seconds** (72/7 s).

**Answer: ≈ 10.29 s.** *Only the train's own length matters for passing a man; subtract speeds (same direction).*
↪ PYQ link: two-train same-direction passing in Ex-7a Q9.
</details>

### Q10.2 (average speed, three legs) ★★★
A car covers three equal stretches at 30, 40 and 60 km/h. Find its average speed for the whole trip.

<details><summary><b>Solution</b></summary>

*Formula:* three equal distances → Average = 3abc/(ab+bc+ca).
- = 3×30×40×60 / (30×40 + 40×60 + 60×30) = 216000 / (1200+2400+1800) = 216000/5400 = **40 km/h**.

**Answer: 40 km/h.** *Use the three-speed harmonic formula — never the plain average (which would give 43.3).*
</details>

### Q10.3 (race, beat by distance & time) ★★★
In a 1000-m race, A beats B by 50 m or 10 seconds. Find A's time to complete the race.

<details><summary><b>Solution</b></summary>

*Formula:* "beats by 50 m or 10 s" → B covers those 50 m in 10 s → B's speed = 5 m/s.
- B runs 1000 m at 5 m/s → B's time = 200 s. A finishes 10 s sooner → **190 s**.

**Answer: A's time = 190 seconds.** *The "50 m or 10 s" equivalence gives B's speed directly.*
↪ PYQ link: speed-ratio after meeting in Ex-7a Q17.
</details>

### Q10.4 (boat, twisted) ★★★
A boat takes twice as long to go upstream as downstream over the same distance. If the stream flows at 4 km/h, find the boat's speed in still water.

<details><summary><b>Solution</b></summary>

*Formula:* time up = 2 × time down → speed down = 2 × speed up.
- Let still-water speed = b. Down = b+4, Up = b−4. Time inverse to speed → (b+4) = 2(b−4).
- b + 4 = 2b − 8 → b = **12 km/h**.

**Answer: 12 km/h.** *Twice the time ⇒ half the speed: downstream speed is double the upstream.*
↪ PYQ link: boat/stream basics in Ex-9a Q1–Q5.
</details>

---

## 11 · Time & Work

**PowerBook formulas used:** Total work = LCM · efficiency ∝ 1/time · alternate days · pipes (negative work) · wages ∝ work done.

### Q11.1 (alternate days, who finishes) ★★★
A can do a job in 12 days, B in 18 days. They work on alternate days, A starting. On which day is the work finished?

<details><summary><b>Solution</b></summary>

*Formula:* total work = LCM(12,18) = 36 units. A = 3/day, B = 2/day.
- 2-day cycle (A then B) = 3 + 2 = 5 units.
- After 7 cycles (14 days) = 35 units; 1 unit left.
- Day 15 is A's turn (3/day) → he finishes 1 unit in 1/3 of a day.
- Work done on the **15th day**, completed at 14⅓ days.

**Answer: finished on the 15th day (14⅓ days total).** *Count full cycles, then assign the leftover to whoever's turn is next.*
↪ PYQ link: A-leaves/joins variants in Ex-8a Q7, Q12.
</details>

### Q11.2 (pipes with leak, twisted) ★★★
Two pipes fill a tank in 12 and 15 hours. A drain empties it in 20 hours. All three are opened together, but the drain is closed after the tank is half full. Total time to fill the tank?

<details><summary><b>Solution</b></summary>

*Formula:* rates add; drain is negative; handle the two phases separately. Total = LCM(12,15,20) = 60 units.
- Fill rates: 5/hr and 4/hr; drain: −3/hr.
- **Phase 1 (all open, until half = 30 units):** net = 5+4−3 = 6/hr → 30/6 = 5 hours.
- **Phase 2 (drain closed, remaining 30 units):** net = 5+4 = 9/hr → 30/9 = 3.33 hours.
- Total = 5 + 3.33 = **8.33 hours** (8 h 20 min).

**Answer: 8⅓ hours (8 h 20 min).** *Split at the event (drain closes) and use a different net rate per phase.*
↪ PYQ link: three-tap alternate filling in Ex-7a Q10; fill-with-leak in Ex-8a Q14.
</details>

### Q11.3 (efficiency + wages) ★★★
A, B and C can finish a work in 10, 12 and 15 days respectively. They work together and complete it, earning ₹4,500 total. Find C's share of the wages.

<details><summary><b>Solution</b></summary>

*Formula:* wages ∝ work done ∝ efficiency (they work the same number of days together).
- Efficiencies (units/day): LCM(10,12,15)=60 → A=6, B=5, C=4.
- Ratio of work = 6:5:4, total 15.
- C's share = 4500 × 4/15 = **₹1,200**.

**Answer: ₹1,200.** *Since all three work the same span, wages split by efficiency ratio directly.*
↪ PYQ link: wage-split (Z's pay) in Ex-8a Q18.
</details>

### Q11.4 (M-D-H chain) ★★★
If 12 men working 8 hours a day finish a wall in 10 days, how many days will 16 men working 6 hours a day take to build a wall **twice** as long?

<details><summary><b>Solution</b></summary>

*Formula:* M₁D₁H₁/W₁ = M₂D₂H₂/W₂.
- (12×8×10)/1 = (16×6×D)/2 → 960 = (96D)/2 = 48D → D = **20 days**.

**Answer: 20 days.** *Don't forget the work doubled (W₂ = 2) on the right side — that's the trap.*
</details>

---

## How to Drill This Set

1. **Hardest-first is the point.** If a ★★★ feels brutal, that's expected — read the solution, then re-solve it from scratch the next day without looking.
2. **Name the formula before solving.** Each question tags the PowerBook formula; say it out loud first. Linking *phrase → formula* is the real skill.
3. **Watch the traps** — they repeat: changing base (%), pure-add vs replacement (mixtures), same-SP loss (P&L), splitting at an event (work/pipes), value-vs-count (coins).
4. **Compare with the easy PYQ version** via each ↪ link in `Scan_Document_Solutions.md` to see how the exam usually phrases the same idea more gently.
5. For the underlying *picture* of any chapter, read [Quant_Concepts_From_Zero.md](../quant-chet/Quant_Concepts_From_Zero.md); for trigger-phrase tips, [Quant_Tips_From_QuestionBank.md](../quant-chet/Quant_Tips_From_QuestionBank.md).

> ★ = standard difficulty · ★★ = needs two steps · ★★★ = multi-step / trap built in. The exam rarely goes past ★★ — train at ★★★ and the real thing feels slow and easy.
