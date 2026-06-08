# Number System, HCF & LCM — Solved Question Bank

> Part of the **SSC CGL AIR-10 Master Repository** · Back to [README.md](README.md) · See also the [Quant Formula Sheet](../Formula-Sheets/Quant_Formula_Sheet.md)

---

## Key Formulas

- Sum of first n natural numbers: `1 + 2 + … + n = n(n+1)/2`
- Sum of squares: `1² + 2² + … + n² = n(n+1)(2n+1)/6`
- Sum of cubes: `1³ + 2³ + … + n³ = [n(n+1)/2]²`
- **Number of factors:** if `N = aᵖ · bˣ · cʳ …` (where x is the power of b), then number of factors `= (p+1)(x+1)(r+1)…`
- **Sum of factors:** `= (aᵖ⁺¹−1)/(a−1) · (b^(q+1)−1)/(b−1) · …`
- **Divisibility rules:**
  - By `3`: digit-sum divisible by 3
  - By `8`: last 3 digits divisible by 8
  - By `7`: drop last digit, subtract twice it from the rest; repeat → multiple of 7
  - By `11`: (sum of odd-place digits − sum of even-place digits) is `0` or a multiple of 11
- **Units-digit cyclicity:** unit digits repeat with cycle length `4` → reduce the power mod 4 (treat remainder 0 as 4)
- **HCF × LCM = product of the two numbers:** `HCF(a,b) × LCM(a,b) = a × b`
- **HCF / LCM of fractions:**
  - `HCF of fractions = HCF(numerators) / LCM(denominators)`
  - `LCM of fractions = LCM(numerators) / HCF(denominators)`
- **Remainder theorems:**
  - Greatest number dividing `a, b, c` leaving the **same** remainder `= HCF(a−b, b−c, c−a)`
  - Greatest number dividing `a, b, c` leaving remainders `r₁, r₂, r₃` `= HCF(a−r₁, b−r₂, c−r₃)`
  - Least number leaving remainder `r` with each of `a, b, c` `= LCM(a,b,c) + r`
- **aⁿ − bⁿ divisibility:** `aⁿ − bⁿ` is always divisible by `(a − b)`; it is divisible by `(a + b)` when `n` is even.

---

## EASY

**Q1.** What is the unit digit of `7¹⁰⁵`?
(a) 1  (b) 3  (c) 7  (d) 9
**Answer: (c) 7**
*Solution:* Unit digits of 7 cycle as 7, 9, 3, 1 (length 4). 105 ÷ 4 leaves remainder 1, so the unit digit equals that of `7¹` = **7**.
🔑 *Trick:* Reduce the exponent mod 4; remainder 1 → first term of the cycle.

**Q2.** Find the HCF of 36 and 84.
(a) 6  (b) 12  (c) 18  (d) 24
**Answer: (b) 12**
*Solution:* `36 = 2²·3²`, `84 = 2²·3·7`. Common factors `= 2²·3 = 12`.

**Q3.** Find the LCM of 12, 15 and 20.
(a) 30  (b) 45  (c) 60  (d) 120
**Answer: (c) 60**
*Solution:* `12 = 2²·3`, `15 = 3·5`, `20 = 2²·5`. LCM `= 2²·3·5 = 60`.

**Q4.** How many factors does 72 have?
(a) 8  (b) 10  (c) 12  (d) 14
**Answer: (c) 12**
*Solution:* `72 = 2³·3²`. Number of factors `= (3+1)(2+1) = 4·3 = 12`.

**Q5.** Is 3,42,112 divisible by 8?
(a) Yes  (b) No  (c) Only by 4  (d) Cannot say
**Answer: (a) Yes**
*Solution:* Divisibility by 8 depends only on the last 3 digits, `112`. As `112 ÷ 8 = 14` exactly, 3,42,112 is divisible by 8.
🔑 *Trick:* For 8, test only the last 3 digits; for 4, only the last 2 digits.

**Q6.** What is the sum of the first 20 natural numbers?
(a) 190  (b) 200  (c) 210  (d) 220
**Answer: (c) 210**
*Solution:* `n(n+1)/2 = 20·21/2 = 210`.

---

## MEDIUM

**Q7.** Find the unit digit of `2⁵⁴ × 3⁴¹`.
(a) 2  (b) 4  (c) 6  (d) 8
**Answer: (a) 2**
*Solution:* For 2: cycle 2,4,8,6; `54 mod 4 = 2` → unit digit 4. For 3: cycle 3,9,7,1; `41 mod 4 = 1` → unit digit 3. Product unit digit `= 4 × 3 = 12` → **2**.

**Q8.** The HCF and LCM of two numbers are 12 and 240 respectively. If one number is 48, find the other.
(a) 50  (b) 60  (c) 72  (d) 96
**Answer: (b) 60**
*Solution:* `HCF × LCM = product` → `12 × 240 = 48 × x` → `x = 2880 / 48 = 60`.

**Q9.** What is the greatest number that divides 43, 91 and 183 leaving the same remainder in each case?
(a) 4  (b) 7  (c) 9  (d) 13
**Answer: (a) 4**
*Solution:* Required number `= HCF(91−43, 183−91, 183−43) = HCF(48, 92, 140)`. `48 = 2⁴·3`, `92 = 2²·23`, `140 = 2²·5·7`. Common `= 2² = 4`.
🔑 *Trick:* "Same remainder" → take pairwise differences, then HCF.

**Q10.** Find the least number which when divided by 6, 7 and 8 leaves a remainder 3 in each case.
(a) 165  (b) 168  (c) 171  (d) 174
**Answer: (c) 171**
*Solution:* `LCM(6,7,8) = 168`. Least such number `= 168 + 3 = 171`.

**Q11.** Find the HCF of the fractions 2/3, 8/9 and 16/81.
(a) 2/81  (b) 2/9  (c) 16/3  (d) 4/27
**Answer: (a) 2/81**
*Solution:* `HCF of fractions = HCF(2,8,16) / LCM(3,9,81) = 2 / 81`.

**Q12.** What is the remainder when `17²⁰⁰` is divided by 18?
(a) 0  (b) 1  (c) 16  (d) 17
**Answer: (b) 1**
*Solution:* `17 ≡ −1 (mod 18)`, so `17²⁰⁰ ≡ (−1)²⁰⁰ = 1 (mod 18)`. Remainder **1**.
🔑 *Trick:* Write the base as (divisor − 1); an even power gives remainder 1.

**Q13.** Find the sum of all factors of 60.
(a) 144  (b) 156  (c) 168  (d) 180
**Answer: (c) 168**
*Solution:* `60 = 2²·3·5`. Sum of factors `= (2³−1)/(2−1) · (3²−1)/(3−1) · (5²−1)/(5−1) = 7 · 4 · 6 = 168`.

---

## HARD

**Q14.** Find the smallest number which leaves remainders 1, 2 and 3 when divided by 2, 3 and 4 respectively.
(a) 9  (b) 11  (c) 13  (d) 15
**Answer: (b) 11**
*Solution:* Note each remainder is exactly 1 less than its divisor (2−1, 3−1, 4−1). So the number is `LCM(2,3,4) − 1 = 12 − 1 = 11`. Check: `11 = 2·5+1`, `11 = 3·3+2`, `11 = 4·2+3`. ✔
🔑 *Trick:* When (divisor − remainder) is constant `k`, answer `= LCM − k`.

**Q15.** What is the unit digit of `(7¹³ + 8¹⁵)`?
(a) 0  (b) 5  (c) 9  (d) 1
**Answer: (c) 9**
*Solution:* 7 cycle 7,9,3,1; `13 mod 4 = 1` → 7. 8 cycle 8,4,2,6; `15 mod 4 = 3` → 2. Sum of unit digits `= 7 + 2 = 9`. So unit digit is **9**.
🔑 *Trick:* Find each term's unit digit separately, then add and take the unit digit of the sum.

**Q16.** A number when divided by 296 leaves a remainder 75. What is the remainder when the same number is divided by 37?
(a) 1  (b) 2  (c) 8  (d) 11
**Answer: (a) 1**
*Solution:* Number `= 296k + 75`. Since `296 = 37·8`, the term `296k` is divisible by 37. Remainder from 75: `75 = 37·2 + 1`. So remainder **1**.
🔑 *Trick:* If the new divisor is a factor of the old one, just take the old remainder mod the new divisor.

**Q17.** Find the largest 4-digit number exactly divisible by 12, 15, 18 and 27.
(a) 9720  (b) 9728  (c) 9800  (d) 9990
**Answer: (a) 9720**
*Solution:* `LCM(12,15,18,27)`: `12=2²·3`, `15=3·5`, `18=2·3²`, `27=3³` → LCM `= 2²·3³·5 = 540`. Largest 4-digit multiple of 540: `9999 ÷ 540 = 18.5…` → `18 × 540 = 9720`.

**Q18.** Simplify: `√(6 + √(6 + √(6 + …)))` (infinite nested radical).
(a) 2  (b) 3  (c) 4  (d) 6
**Answer: (b) 3**
*Solution:* Let `x = √(6 + x)` → `x² = 6 + x` → `x² − x − 6 = 0` → `(x−3)(x+2) = 0`. Taking the positive root, `x = 3`.
🔑 *Trick:* For `√(a + √(a + …))`, answer is the positive root of `x² − x − a = 0`; for `a = n(n−1)` the answer is simply `n`.

---

## SSC PYQ PATTERN

**Q19.** (SSC CGL pattern) Four bells toll at intervals of 6, 8, 12 and 18 seconds respectively. If they toll together at 12:00:00, after how many seconds will they next toll together?
(a) 48  (b) 60  (c) 72  (d) 96
**Answer: (c) 72**
*Solution:* They toll together after `LCM(6,8,12,18)` seconds. `6=2·3`, `8=2³`, `12=2²·3`, `18=2·3²` → LCM `= 2³·3² = 72`. So after **72 seconds**.

**Q20.** (SSC CGL pattern) Three pieces of cloth are 24 m, 36 m and 48 m long. What is the greatest length of tape that can measure each exactly?
(a) 6 m  (b) 8 m  (c) 12 m  (d) 16 m
**Answer: (c) 12 m**
*Solution:* Greatest measuring length `= HCF(24, 36, 48)`. `24=2³·3`, `36=2²·3²`, `48=2⁴·3` → HCF `= 2²·3 = 12 m`.
🔑 *Trick:* "Greatest length / largest container that measures all" → HCF.

**Q21.** (SSC CGL pattern) Find the unit digit of `(123)¹⁴⁷ × (456)⁹⁹`.
(a) 2  (b) 4  (c) 6  (d) 8
**Answer: (a) 2**
*Solution:* Use only unit digits. 3 cycle 3,9,7,1; `147 mod 4 = 3` → 7. 6 always ends in 6. Product unit digit `= 7 × 6 = 42` → **2**.
🔑 *Trick:* Any power of a number ending in 6 also ends in 6.

**Q22.** (SSC CGL pattern) The product of two co-prime numbers is 117. Their LCM is:
(a) 9  (b) 13  (c) 39  (d) 117
**Answer: (d) 117**
*Solution:* For co-prime numbers `HCF = 1`, so `LCM = product / HCF = 117 / 1 = 117`.
🔑 *Trick:* Co-prime ⇒ HCF = 1 ⇒ LCM equals the product.

**Q23.** (SSC CGL pattern) When a number is divided by 5 the remainder is 3, and when divided by 7 the remainder is 4. Find the smallest such positive number.
(a) 11  (b) 18  (c) 25  (d) 32
**Answer: (b) 18**
*Solution:* Numbers ≡ 3 (mod 5): 3, 8, 13, 18, 23… Test each for ≡ 4 (mod 7): `18 = 7·2 + 4` ✔. So smallest is **18**.
🔑 *Trick:* List multiples of the larger condition or smaller set and test the other — fast CRT for small numbers.

---

### 🔑 Exam Tricks Box

- **Unit digits:** reduce the exponent mod 4 (remainder 0 → take 4); digits 0,1,5,6 always repeat themselves.
- **HCF vs LCM keywords:** "greatest length / largest / measure exactly / maximum students" → **HCF**; "least number / ring together / together again / minimum" → **LCM**.
- **Same remainder problems:** take pairwise differences then HCF; **remainder = (divisor − constant)** problems → `LCM − constant`.
- **HCF × LCM = product** works only for **two** numbers — never extend it to three.
- **Base = (divisor ± 1):** `(d−1)ⁿ` gives remainder 1 for even n and `d−1` for odd n — collapses huge-power remainder questions instantly.

---

> Next: continue with [Percentage & Profit-Loss](README.md) in this repository, and keep the [Quant Formula Sheet](../Formula-Sheets/Quant_Formula_Sheet.md) open while practising. Consistency beats intensity — solve 10 questions daily.
