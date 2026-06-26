# Statistics — Solved Question Bank

> Scoring topic — direct formula application. Mean, median, mode and SD show up almost every shift.
> [Quant Index](README.md) · [Formula Sheet](../Formula-Sheets/Quant_Formula_Sheet.md)

## Key Formulas
- Mean = `Σx / n`
- Weighted mean = `Σwx / Σw`
- Median (data sorted): odd n → `middle value`; even n → `average of the two middle values`
- Mode = `most frequently occurring value`
- Empirical relation: `Mean − Mode = 3(Mean − Median)` → `Mode = 3·Median − 2·Mean`
- Variance `σ² = Σ(x − x̄)² / n`
- Standard Deviation `σ = √Variance`
- Range = `max − min`
- Combined mean of two groups = `(n₁x̄₁ + n₂x̄₂) / (n₁ + n₂)`
- Quartiles: Q₁ = lower-half median, Q₂ = median, Q₃ = upper-half median; IQR = `Q₃ − Q₁`

---

## EASY

**Q1.** Find the mean of 12, 15, 18, 21, 24.
(a) 17  (b) 18  (c) 19  (d) 20
**Answer: (b) 18**
*Solution:* Σx = 12+15+18+21+24 = 90; n = 5 → Mean = 90/5 = 18.
🔑 *Trick:* Evenly spaced data → mean = average of first and last = (12+24)/2 = 18.

**Q2.** Find the median of 7, 3, 9, 5, 11.
(a) 5  (b) 7  (c) 9  (d) 8
**Answer: (b) 7**
*Solution:* Sort: 3, 5, **7**, 9, 11. n = 5 (odd) → middle value = 7.

**Q3.** Find the mode of 4, 6, 6, 8, 6, 10, 8.
(a) 6  (b) 8  (c) 4  (d) 10
**Answer: (a) 6**
*Solution:* 6 appears 3 times, more than any other value → Mode = 6.

**Q4.** Find the range of 14, 22, 9, 30, 17.
(a) 16  (b) 21  (c) 30  (d) 9
**Answer: (b) 21**
*Solution:* Range = max − min = 30 − 9 = 21.

**Q5.** Find the median of 10, 20, 30, 40.
(a) 20  (b) 25  (c) 30  (d) 35
**Answer: (b) 25**
*Solution:* Already sorted, n = 4 (even) → median = average of two middle values = (20+30)/2 = 25.

---

## MEDIUM

**Q6.** The marks of 5 students are 60, 70, 80, 90 and one unknown. If the mean is 76, find the missing mark.
(a) 78  (b) 80  (c) 82  (d) 84
**Answer: (b) 80**
*Solution:* Σx = mean × n = 76 × 5 = 380. Known sum = 60+70+80+90 = 300 → missing = 380 − 300 = 80.

**Q7.** Find the mean of the following frequency data.
| Value (x) | 2 | 4 | 6 | 8 |
|---|---|---|---|---|
| Frequency (f) | 3 | 5 | 2 | 4 |
(a) 4.8  (b) 5.0  (c) 5.2  (d) 5.6
**Answer: (b) 5.0**
*Solution:* Σfx = 2·3 + 4·5 + 6·2 + 8·4 = 6+20+12+32 = 70; Σf = 3+5+2+4 = 14 → Mean = Σfx/Σf = 70/14 = 5.0.

**Q8.** A student scores 80 in a test of weight 2 and 50 in a test of weight 3. Find the weighted mean.
(a) 60  (b) 62  (c) 65  (d) 58
**Answer: (b) 62**
*Solution:* Weighted mean = Σwx/Σw = (2·80 + 3·50)/(2+3) = (160+150)/5 = 310/5 = 62.

**Q9.** Find the median of 8, 12, 15, 20, 22, 25 (even count).
(a) 17  (b) 17.5  (c) 18  (d) 20
**Answer: (b) 17.5**
*Solution:* Sorted, n = 6 (even). Two middle values are the 3rd and 4th: 15 and 20 → median = (15+20)/2 = 17.5.

**Q10.** Group A has 20 students with mean 15; Group B has 30 students with mean 20. Find the combined mean.
(a) 17  (b) 17.5  (c) 18  (d) 18.5
**Answer: (c) 18**
*Solution:* Combined mean = (n₁x̄₁ + n₂x̄₂)/(n₁+n₂) = (20·15 + 30·20)/(20+30) = (300+600)/50 = 900/50 = 18.
🔑 *Trick:* Answer is weighted toward the larger group (30), so it sits closer to 20 than to 15.

**Q11.** The mean of 10 observations is 25. If each observation is increased by 4, the new mean is:
(a) 25  (b) 29  (c) 100  (d) 21
**Answer: (b) 29**
*Solution:* Adding a constant c to every value raises the mean by c → new mean = 25 + 4 = 29.
🔑 *Trick:* Add/subtract a constant → mean shifts by that constant; SD and range are unchanged.

---

## HARD

**Q12.** The mean of 8 numbers is 21. When one number is removed, the mean of the remaining 7 becomes 20. Find the removed number.
(a) 26  (b) 27  (c) 28  (d) 30
**Answer: (c) 28**
*Solution:* Total of 8 = 21×8 = 168. Total of 7 = 20×7 = 140 → removed = 168 − 140 = 28.

**Q13.** Find the standard deviation of 2, 4, 4, 4, 5, 5, 7, 9.
(a) 1  (b) 2  (c) 3  (d) 4
**Answer: (b) 2**
*Solution:* Mean = (2+4+4+4+5+5+7+9)/8 = 40/8 = 5. Deviations: −3,−1,−1,−1,0,0,2,4. Squares: 9,1,1,1,0,0,4,16 → Σ = 32. Variance = 32/8 = 4 → SD = √4 = 2.

**Q14.** Find the variance of 2, 4, 6, 8, 10.
(a) 6  (b) 8  (c) 10  (d) 4
**Answer: (b) 8**
*Solution:* Mean = 30/5 = 6. Deviations: −4,−2,0,2,4 → squares 16,4,0,4,16 → Σ = 40. Variance = 40/5 = 8. (SD = √8 = 2√2 ≈ 2.83.)

**Q15.** For a moderately skewed distribution, Mean = 35 and Median = 33. Using the empirical relation, find the Mode.
(a) 28  (b) 29  (c) 31  (d) 37
**Answer: (b) 29**
*Solution:* Mode = 3·Median − 2·Mean = 3(33) − 2(35) = 99 − 70 = 29.
🔑 *Trick:* `Mean − Mode = 3(Mean − Median)` → 35 − Mode = 3(35−33) = 6 → Mode = 29.

---

## SSC PYQ PATTERN

**Q16.** (SSC CGL pattern) The average of 5 consecutive odd numbers is 27. Find the largest number.
(a) 29  (b) 31  (c) 33  (d) 35
**Answer: (b) 31**
*Solution:* For consecutive numbers, the mean is the middle term → middle = 27. The numbers are 23, 25, **27**, 29, 31 → largest = 31.

**Q17.** (SSC CGL pattern) The mean of 11 observations is 30. If the mean of the first 6 is 28 and of the last 6 is 32, find the 6th observation.
(a) 28  (b) 30  (c) 32  (d) 34
**Answer: (b) 30**
*Solution:* Sum of all 11 = 30×11 = 330. First 6 = 28×6 = 168; last 6 = 32×6 = 192. The 6th is counted in both → 168 + 192 − 330 = 30.

**Q18.** (SSC CGL pattern) Find the median of the data: 12, 15, 18, 18, 20, 22, 25, 30.
(a) 18  (b) 19  (c) 20  (d) 18.5
**Answer: (b) 19**
*Solution:* Sorted, n = 8 (even). Middle two are the 4th and 5th: 18 and 20 → median = (18+20)/2 = 19.

**Q19.** (SSC CGL pattern) The mean of 20 numbers is 18. It was later found that a number 30 was wrongly read as 3. Find the correct mean.
(a) 18.35  (b) 19.35  (c) 19.0  (d) 18.5
**Answer: (b) 19.35**
*Solution:* Wrong sum = 18×20 = 360. Correction = +(30 − 3) = +27 → correct sum = 387 → correct mean = 387/20 = 19.35.
🔑 *Trick:* Error in a single reading shifts the mean by (correction)/n = 27/20 = 1.35 → 18 + 1.35 = 19.35.

---

### 🔑 Exam Tricks Box
- For consecutive / evenly-spaced data, **mean = median = middle term = (first + last)/2** — no full addition needed.
- Adding a constant to every value shifts the **mean** by that constant but leaves **SD and range unchanged**; multiplying scales both mean and SD.
- "Wrong value corrected" problems: new mean = old mean + (correct − wrong)/n. Never re-add the whole set.
- Empirical relation `Mode = 3·Median − 2·Mean` lets you get any one of mean/median/mode from the other two.

### 🔑 Mode of Grouped Data — Quick Rules
> Modal class = the class with the highest frequency. When the mode lands on a class boundary, the adjacent frequencies are forced:
- **Mode = lower boundary of modal class** → modal frequency = **previous** class frequency.
- **Mode = upper boundary of modal class** → modal frequency = **next** class frequency.
- **Mode at the exact junction of two classes** → the two adjacent frequencies are **equal**.

> Re-attempt every ✗ after 3 days. Aim: 19/19 untimed, then under 12 min.
