# Series — Solved Question Bank

> Quick links: [Reasoning Index](README.md) · [Reasoning Cheat Sheet](../Cheat-Sheets/Reasoning_Cheat_Sheet.md)

## Key Concepts
- **Number series**: look for +k, ×k, squares, cubes, primes, or alternating patterns.
- **Letter series**: convert to positions (A=1…Z=26) and track the step.
- **Alphanumeric series**: letters and numbers alternate — handle each stream separately.
- **Missing term**: find the rule from known terms, then fill the blank.
- Differences of differences often reveal a hidden quadratic pattern.

## EASY

**Q1.** 2, 4, 6, 8, ?
(a) 9  (b) 10  (c) 11  (d) 12
**Answer: (b) 10**
*Solution:* Each term increases by 2: 2, 4, 6, 8, 10.

**Q2.** 5, 10, 20, 40, ?
(a) 60  (b) 70  (c) 80  (d) 50
**Answer: (c) 80**
*Solution:* Each term is doubled: 40 × 2 = 80.

**Q3.** A, C, E, G, ?
(a) H  (b) I  (c) J  (d) K
**Answer: (b) I**
*Solution:* Skip one letter each time (+2): A, C, E, G, I.

**Q4.** 1, 4, 9, 16, ?
(a) 20  (b) 24  (c) 25  (d) 36
**Answer: (c) 25**
*Solution:* Perfect squares: 1², 2², 3², 4², 5² = 25.

**Q5.** Z, X, V, T, ?
(a) S  (b) R  (c) Q  (d) U
**Answer: (b) R**
*Solution:* Letters decrease by 2: Z(26), X(24), V(22), T(20), R(18).

## MEDIUM

**Q1.** 3, 6, 11, 18, 27, ?
(a) 36  (b) 38  (c) 40  (d) 42
**Answer: (b) 38**
*Solution:* Differences are 3, 5, 7, 9, 11 (odd numbers). 27 + 11 = 38.

**Q2.** 2, 6, 12, 20, 30, ?
(a) 40  (b) 42  (c) 44  (d) 36
**Answer: (b) 42**
*Solution:* Terms are n(n+1): 1·2, 2·3, 3·4, 4·5, 5·6, 6·7 = 42. Differences 4,6,8,10,12.

**Q3.** B, D, G, K, ?
(a) N  (b) O  (c) P  (d) M
**Answer: (c) P**
*Solution:* Steps increase: B(+2)D(+3)G(+4)K(+5)P. K=11, +5=16=P.

**Q4.** A1, C3, E5, G7, ?
(a) H8  (b) I9  (c) I8  (d) H9
**Answer: (b) I9**
*Solution:* Letters skip one (A,C,E,G,I) and numbers are odd (1,3,5,7,9). Next is I9.

**Q5.** 4, 9, 16, 25, 36, ?
(a) 45  (b) 48  (c) 49  (d) 50
**Answer: (c) 49**
*Solution:* Squares of 2,3,4,5,6,7 → 7² = 49.

**Q6.** 1, 1, 2, 3, 5, 8, ?
(a) 11  (b) 12  (c) 13  (d) 10
**Answer: (c) 13**
*Solution:* Fibonacci — each term is the sum of the previous two: 5 + 8 = 13.

## HARD

**Q1.** 2, 5, 10, 17, 26, ?
(a) 35  (b) 37  (c) 36  (d) 38
**Answer: (b) 37**
*Solution:* n²+1: 1+1, 4+1, 9+1, 16+1, 25+1, 36+1 = 37. Differences 3,5,7,9,11.

**Q2.** 7, 26, 63, 124, ?
(a) 215  (b) 216  (c) 217  (d) 218
**Answer: (a) 215**
*Solution:* n³−1: 2³−1=7, 3³−1=26, 4³−1=63, 5³−1=124, 6³−1=215.

**Q3.** AZ, CX, EV, GT, ?
(a) IR  (b) IS  (c) HR  (d) IQ
**Answer: (a) IR**
*Solution:* First letters +2 (A,C,E,G,I); second letters −2 (Z,X,V,T,R). Next pair = IR.

**Q4.** 3, 7, 16, 35, 74, ?
(a) 150  (b) 151  (c) 152  (d) 153
**Answer: (d) 153**
*Solution:* Rule: ×2 + (1,2,3,4,5). 3·2+1=7, 7·2+2=16, 16·2+3=35, 35·2+4=74, 74·2+5=153.

## SSC PYQ PATTERN (SSC CGL pattern)

**Q1.** Select the number that will come in place of the question mark: 6, 11, 21, 36, 56, ?
(a) 81  (b) 80  (c) 79  (d) 82
**Answer: (a) 81**
*Solution:* Differences 5, 10, 15, 20, 25 (multiples of 5). 56 + 25 = 81.

**Q2.** Find the missing term: 5, 11, 23, 47, ?
(a) 93  (b) 94  (c) 95  (d) 96
**Answer: (c) 95**
*Solution:* Rule: ×2 + 1. 5·2+1=11, 11·2+1=23, 23·2+1=47, 47·2+1=95.

**Q3.** Find the next term: C, F, I, L, ?
(a) N  (b) O  (c) P  (d) M
**Answer: (b) O**
*Solution:* Letters increase by 3: C(3), F(6), I(9), L(12), O(15).

**Q4.** Find the missing number: 8, 27, 64, 125, ?
(a) 196  (b) 216  (c) 225  (d) 250
**Answer: (b) 216**
*Solution:* Cubes of 2,3,4,5,6 → 6³ = 216.

### 🔑 Trick Box
- Always compute the **differences** first; if they form a pattern, you have the rule.
- If differences also grow, take the **second difference** — likely a square/cube pattern.
- For letter series, convert to numbers immediately; never eyeball alphabet jumps.
- Watch for two interleaved series (odd and even positions) hiding in one row.

> When stuck, check ×2±k and n²/n³ patterns — SSC loves these.
