# Average & Mixtures — Solved Question Bank

> Navigation: [README.md](README.md) | [Quant Formula Sheet](../Formula-Sheets/Quant_Formula_Sheet.md)

## Key Formulas

- Average: `Average = Sum of observations / n`
- Average of first n natural numbers: `(n + 1) / 2`
- Average of consecutive numbers: `(first + last) / 2`
- Replacement (one in, one out): `Δavg = (new − old) / n`
- Alligation rule: `(cheaper qty) / (dearer qty) = (dearer − mean) / (mean − cheaper)`
- Repeated replacement: `Final = Initial × (1 − r/V)^n`

---

## EASY

**Q1.** The average of 5 numbers is 27. If one number 33 is included, what is the new average?
(a) 28  (b) 29  (c) 30  (d) 26
**Answer: (a) 28**
*Solution:* Sum of 5 numbers = 27 × 5 = 135. New sum = 135 + 33 = 168. New average = 168 / 6 = 28.
🔑 *Trick:* Total changes by (added value − old average) spread over new count.

**Q2.** Find the average of the first 10 natural numbers.
(a) 5  (b) 5.5  (c) 6  (d) 4.5
**Answer: (b) 5.5**
*Solution:* Average of first n natural numbers = (n + 1) / 2 = (10 + 1) / 2 = 11 / 2 = 5.5.

**Q3.** The average of 5 consecutive numbers starting from 12 is:
(a) 13  (b) 14  (c) 15  (d) 16
**Answer: (b) 14**
*Solution:* Numbers are 12, 13, 14, 15, 16. Average of consecutive = (first + last) / 2 = (12 + 16) / 2 = 28 / 2 = 14.

**Q4.** The average age of 4 boys is 15 years. If a 5th boy aged 20 joins, the new average age is:
(a) 15  (b) 16  (c) 17  (d) 18
**Answer: (b) 16**
*Solution:* Sum of 4 boys = 15 × 4 = 60. New sum = 60 + 20 = 80. New average = 80 / 5 = 16.

**Q5.** The average of three numbers is 20. Two of them are 15 and 25. Find the third.
(a) 18  (b) 20  (c) 22  (d) 24
**Answer: (b) 20**
*Solution:* Sum = 20 × 3 = 60. Third = 60 − (15 + 25) = 60 − 40 = 20.

**Q6.** In what ratio must rice at ₹30/kg be mixed with rice at ₹40/kg to get a mixture worth ₹34/kg?
(a) 2 : 3  (b) 3 : 2  (c) 4 : 1  (d) 1 : 4
**Answer: (b) 3 : 2**
*Solution:* By alligation, cheaper : dearer = (dearer − mean) : (mean − cheaper) = (40 − 34) : (34 − 30) = 6 : 4 = 3 : 2.
🔑 *Trick:* Differences taken across the mean give the inverse-ratio of quantities.

---

## MEDIUM

**Q7.** The average of 11 results is 50. The average of the first 6 is 49 and of the last 6 is 52. Find the 6th result.
(a) 56  (b) 55  (c) 54  (d) 52
**Answer: (a) 56**
*Solution:* Sum of all 11 = 50 × 11 = 550. First 6 sum = 49 × 6 = 294. Last 6 sum = 52 × 6 = 312. The 6th result is counted in both, so 294 + 312 = 606 = 550 + 6th. 6th = 606 − 550 = 56.
🔑 *Trick:* Overlapping element = (sum of two groups) − (total sum).

**Q8.** The average age of a class of 30 students is 14 years. If the teacher's age is included, the average rises to 15. Find the teacher's age.
(a) 42  (b) 44  (c) 45  (d) 48
**Answer: (c) 45**
*Solution:* Students' sum = 14 × 30 = 420. With teacher (31 people) sum = 15 × 31 = 465. Teacher's age = 465 − 420 = 45.

**Q9.** The average weight of 8 men increases by 1.5 kg when a new man replaces one weighing 65 kg. The weight of the new man is:
(a) 76  (b) 77  (c) 78  (d) 75
**Answer: (b) 77**
*Solution:* Total increase = 8 × 1.5 = 12 kg. Using Δavg = (new − old)/n, new − old = 12. New man = 65 + 12 = 77.
🔑 *Trick:* Replacement raises total by n × (rise); new value = old value + that total.

**Q10.** A student's marks were wrongly entered as 83 instead of 63. Due to this the average marks of the class of 40 increased by how much?
(a) 0.5  (b) 0.4  (c) 0.6  (d) 1
**Answer: (a) 0.5**
*Solution:* Excess added = 83 − 63 = 20. Average increase = 20 / 40 = 0.5.

**Q11.** 40 litres of a mixture contains milk and water in ratio 3 : 1. How much water must be added to make the ratio 3 : 2?
(a) 8 L  (b) 10 L  (c) 12 L  (d) 6 L
**Answer: (b) 10 L**
*Solution:* Milk = 40 × 3/4 = 30 L, water = 10 L. For ratio 3 : 2, with milk fixed at 30, water = 30 × 2/3 = 20 L. Water to add = 20 − 10 = 10 L.

**Q12.** A milkman buys milk at ₹12/L and adds water (free) so that selling the mixture at ₹12/L gives him a 25% profit. In what ratio is water mixed with milk?
(a) 1 : 4  (b) 1 : 5  (c) 1 : 3  (d) 2 : 5
**Answer: (a) 1 : 4**
*Solution:* Selling at cost-of-milk (₹12) with 25% profit means the mixture's cost price = 12 / 1.25 = ₹9.60/L. By alligation between water (₹0) and milk (₹12) about mean ₹9.60: water : milk = (12 − 9.6) : (9.6 − 0) = 2.4 : 9.6 = 1 : 4.
🔑 *Trick:* Water is the "free" cheaper ingredient (price 0); its profit comes purely from dilution.

**Q13.** The average of 6 numbers is 8. If each number is multiplied by 3, the new average is:
(a) 11  (b) 21  (c) 24  (d) 18
**Answer: (c) 24**
*Solution:* Multiplying every observation by a constant multiplies the average by the same constant. New average = 8 × 3 = 24.

---

## HARD

**Q14.** A vessel contains 40 L of pure milk. 4 L is drawn out and replaced with water; this is done 3 times. Find the milk remaining.
(a) 29.16 L  (b) 30 L  (c) 28.8 L  (d) 32 L
**Answer: (a) 29.16 L**
*Solution:* Final = Initial × (1 − r/V)^n = 40 × (1 − 4/40)^3 = 40 × (9/10)^3 = 40 × 729/1000 = 29.16 L.
🔑 *Trick:* Each replacement keeps fraction (1 − r/V) of milk; raise it to the power n.

**Q15.** The average of 50 numbers is 38. Two numbers 45 and 55 are discarded. The average of the remaining 48 is:
(a) 36.5  (b) 37.5  (c) 37.9  (d) 38.5
**Answer: (b) 37.5**
*Solution:* Sum of 50 = 38 × 50 = 1900. Remove 45 + 55 = 100. Remaining sum = 1800 over 48 = 37.5.

**Q16.** Two vessels contain milk and water in ratios 4 : 1 and 2 : 3. Equal quantities are taken from each and mixed. Find milk : water in the final mixture.
(a) 3 : 2  (b) 2 : 3  (c) 1 : 1  (d) 5 : 4
**Answer: (a) 3 : 2**
*Solution:* Take 5 L from each (LCM of parts). Vessel 1: milk = 5 × 4/5 = 4 L, water = 1 L. Vessel 2: milk = 5 × 2/5 = 2 L, water = 3 L. Total milk = 4 + 2 = 6 L, total water = 1 + 3 = 4 L. Ratio = 6 : 4 = 3 : 2.
🔑 *Trick:* Take equal volumes (use the part-LCM) so each fraction converts cleanly to litres before adding.

**Q17.** The average salary of all workers in a workshop is ₹8000. The average of 7 technicians is ₹12000 and of the rest is ₹6000. Find the total number of workers.
(a) 18  (b) 21  (c) 20  (d) 24
**Answer: (b) 21**
*Solution:* Let total = n, non-technicians = n − 7. Then 12000 × 7 + 6000 × (n − 7) = 8000n. 84000 + 6000n − 42000 = 8000n. 42000 = 2000n. n = 21.
🔑 *Trick:* Use alligation: 12000 vs 6000 about mean 8000 gives ratio 2000 : 4000 = 1 : 2, so 7 : 14, total 21.

**Q18.** A container has 60 L mixture of milk and water in ratio 2 : 1. If 15 L mixture is removed and replaced with milk, the new ratio of milk to water is:
(a) 13 : 5  (b) 3 : 1  (c) 5 : 2  (d) 7 : 3
**Answer: (b) 3 : 1**
*Solution:* Milk = 40 L, water = 20 L. Remove 15 L (in ratio 2 : 1): milk removed = 10, water removed = 5. Now milk = 30, water = 15. Add 15 L pure milk: milk = 45, water = 15. Ratio = 45 : 15 = 3 : 1.
🔑 *Trick:* The removed portion carries the same ratio as the current mixture.

---

## SSC PYQ PATTERN

**Q19.** (SSC CGL pattern) The average of 7 consecutive even numbers is 24. The largest of these numbers is:
(a) 28  (b) 30  (c) 26  (d) 32
**Answer: (b) 30**
*Solution:* For an odd count of consecutive even numbers, the middle term equals the average = 24. The 7 numbers are 18, 20, 22, 24, 26, 28, 30. Largest = 30.

**Q20.** (SSC CGL pattern) In what ratio should tea at ₹250/kg be mixed with tea at ₹350/kg to obtain a blend worth ₹280/kg?
(a) 7 : 3  (b) 3 : 7  (c) 5 : 2  (d) 2 : 5
**Answer: (a) 7 : 3**
*Solution:* By alligation, cheaper : dearer = (350 − 280) : (280 − 250) = 70 : 30 = 7 : 3.

**Q21.** (SSC CGL pattern) The average of 6 observations is 12. A 7th observation is added and the average becomes 13. The 7th observation is:
(a) 18  (b) 19  (c) 20  (d) 21
**Answer: (b) 19**
*Solution:* Sum of 6 = 72. New sum (7 obs) = 13 × 7 = 91. 7th = 91 − 72 = 19.
🔑 *Trick:* New value = new total − old total.

**Q22.** (SSC CGL pattern) From a 100 L vessel of pure spirit, 20 L is removed and replaced with water twice. The spirit left is:
(a) 64 L  (b) 60 L  (c) 80 L  (d) 72 L
**Answer: (a) 64 L**
*Solution:* Final = 100 × (1 − 20/100)^2 = 100 × (4/5)^2 = 100 × 16/25 = 64 L.

**Q23.** (SSC CGL pattern) The average age of a husband and wife was 23 years at marriage. After 5 years they have a one-year-old child. The average age of the family now is:
(a) 19 years  (b) 20 years  (c) 18.5 years  (d) 21 years
**Answer: (a) 19 years**
*Solution:* At marriage husband + wife sum = 46. After 5 years each ages 5: sum = 46 + 10 = 56. Add child age 1: total = 57 over 3 members = 19 years.
🔑 *Trick:* Add the elapsed years to every existing member before averaging in the new one.

---

### 🔑 Exam Tricks Box

- The average always lies between the smallest and largest values; use this to eliminate impossible options instantly.
- For replacement problems, remember Total change = n × (change in average); solve for the unknown value directly.
- In alligation, the differences are taken across the mean and the resulting ratio is the inverse-quantity ratio (cheaper : dearer).
- Treat water as a free (₹0) ingredient in milk-water alligation questions.
- For repeated replacement, never recompute step by step under time pressure — apply `Initial × (1 − r/V)^n`.

> Practice these patterns until alligation and replacement become reflex; they appear in nearly every SSC CGL Tier-1 paper.
