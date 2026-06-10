# SSC CGL — Quantitative Aptitude Cheat Sheet

> **Source:** Table-of-contents pages (`quant-chet/`). The images list the chapter syllabus; this sheet expands every listed topic into its key formulas, tricks, and shortcut techniques.
>
> **Chapters covered (Quant Ch-1 to Ch-15):** Number System · Ratio, Proportion & Variation · Averages, Mixtures & Alligations · Percentages · Profit & Loss · Simple & Compound Interest · Time & Distance · Time & Work · Boats & Streams · Permutation & Combination · Probability · Geometry & Mensuration · Simplification · Logarithms · Set Theory.

---

## Ch-1 · Number System

**Divisibility shortcuts**

| Div by | Rule |
|---|---|
| 2 / 5 / 10 | last digit 0/2/4/6/8 ; 0/5 ; 0 |
| 3 / 9 | digit sum divisible by 3 / 9 |
| 4 / 8 | last 2 / last 3 digits divisible |
| 6 | divisible by 2 **and** 3 |
| 7 | double last digit, subtract from rest; repeat |
| 11 | (sum of odd-place digits − sum of even-place digits) divisible by 11 |

**Key results**
- Sum of first *n* natural numbers = `n(n+1)/2`
- Sum of squares = `n(n+1)(2n+1)/6` ; Sum of cubes = `[n(n+1)/2]²`
- Sum of first *n* odd numbers = `n²` ; even = `n(n+1)`
- Number of divisors: if `N = aᵖ·b�q·cʳ` → divisors `= (p+1)(q+1)(r+1)`
- Sum of divisors `= (aᵖ⁺¹−1)/(a−1) × …`
- HCF × LCM = product of two numbers
- **Unit digit cyclicity:** 2→(2,4,8,6), 3→(3,9,7,1), 7→(7,9,3,1), 8→(8,4,2,6) — cycle of 4. Divide power by 4, use remainder.
- **Remainder (Fermat):** if p is prime, `aᵖ⁻¹ ≡ 1 (mod p)`.

---

## Ch-2 · Ratio, Proportion & Variation

- `a:b = c:d` → `ad = bc` (product of means = product of extremes)
- **Mean proportional** of a & b = `√(ab)`; **third proportional** to a,b = `b²/a`
- Compounded ratio of a:b and c:d = `ac:bd`
- If `a:b = m:n` and `b:c = p:q` → `a:b:c = mp : np : nq`
- **Direct variation:** `a ∝ b → a/b = k`; **Inverse:** `a ∝ 1/b → ab = k`
- Trick: to combine A:B and B:C, make B common (LCM of the two B-values).

---

## Ch-3 · Averages, Mixtures & Alligations

**Averages**
- Average = `Sum / Count`
- New avg after adding/removing: `New Sum / New Count`
- Average of first n natural numbers = `(n+1)/2`
- Average speed (equal distances) = `2xy/(x+y)` (harmonic mean)

**Alligation rule** (mixing two ingredients at prices/concentrations C₁, C₂ to get mean M):

```
        Cheaper(C₁)        Dearer(C₂)
                  \        /
                   Mean(M)
                  /        \
   (C₂ − M)  :  (M − C₁)   →  Qty₁ : Qty₂
```

- **Replacement formula:** vessel of V litres, x removed & replaced k times →
  `Final = V·(1 − x/V)ᵏ`

---

## Ch-4 · Percentages

- `x% of y = (x/100)·y` ; `x% = x/100`
- **% change** = `(New − Old)/Old × 100`
- **Successive % change** (a then b): net = `a + b + ab/100`
- If A is x% more than B → B is `x/(100+x)×100 %` less than A
- If price ↑ x%, reduce consumption by `x/(100+x)×100 %` to keep expense same
- Population/CI growth: `P(1 ± r/100)ⁿ`

**Fraction ↔ % quick table:** 1/2=50, 1/3=33⅓, 1/4=25, 1/5=20, 1/6=16⅔, 1/7=14²⁄₇, 1/8=12½, 1/9=11⅑, 1/11=9¹⁄₁₁, 1/12=8⅓.

---

## Ch-5 · Profit & Loss

- `Profit% = (SP − CP)/CP × 100` ; `Loss% = (CP − SP)/CP × 100`
- `SP = CP·(100 ± P%/L%)/100`
- **Discount** on Marked Price: `SP = MP·(1 − D/100)`
- Two articles sold at same SP, one at +x% and one at −x% → **always a loss** of `(x/10)%`= `x²/100 %`
- **False weight:** gain% = `(Error / (True − Error)) × 100`
- Successive discounts a%, b% → net = `a + b − ab/100`

---

## Ch-6 · Simple & Compound Interest

- **SI** = `P·R·T/100`
- **CI** Amount = `P(1 + R/100)ᵀ` ; CI = Amount − P
- Half-yearly: rate `R/2`, time `2T`. Quarterly: `R/4`, `4T`.
- Difference (CI − SI) for 2 yrs = `P(R/100)²`
- Difference for 3 yrs = `P(R/100)²·(3 + R/100)`
- Money doubles in SI: `T = 100/R` years.

---

## Ch-7 · Time & Distance

- `Speed = Distance/Time` ; 1 km/h = `5/18` m/s ; 1 m/s = `18/5` km/h
- Average speed for equal distance = `2xy/(x+y)`
- **Trains:** crossing a pole → length/speed; crossing a platform → (len+platform)/speed
- Relative speed: opposite → `a+b`; same direction → `a−b`
- Two bodies start toward each other, meet then reach in t₁,t₂: speed ratio = `√t₂:√t₁`

---

## Ch-8 · Time & Work

- Work = `Rate × Time` ; if A does job in `a` days → rate `1/a`/day
- A & B together: `1/a + 1/b = 1/T → T = ab/(a+b)`
- **Efficiency–time inverse:** if A is twice as efficient, takes half time
- M₁D₁H₁/W₁ = M₂D₂H₂/W₂ (men–days–hours–work chain rule)
- Pipes & cisterns: inlet `+`, leak/outlet `−`; same algebra as work.

---

## Ch-9 · Boats & Streams

- Downstream speed = `b + s` ; Upstream = `b − s`
- Boat speed `b = (down + up)/2` ; Stream `s = (down − up)/2`
- Same distance up & down, total time t → distance = `t·(b²−s²)/(2b)`

---

## Ch-10 · Permutation & Combination

- `n! = n(n−1)…1`, `0! = 1`
- Permutation: `ⁿPᵣ = n!/(n−r)!` (order matters)
- Combination: `ⁿCᵣ = n!/(r!(n−r)!)` (order doesn't)
- `ⁿCᵣ = ⁿCₙ₋ᵣ` ; `ⁿC₀ = ⁿCₙ = 1`
- Arrangements of n items with repeats `p,q,…`: `n!/(p!·q!…)`
- Circular permutations of n = `(n−1)!`

---

## Ch-11 · Probability

- `P(E) = favorable/total` , `0 ≤ P ≤ 1`
- `P(not E) = 1 − P(E)`
- Mutually exclusive: `P(A∪B) = P(A) + P(B)`
- General: `P(A∪B) = P(A) + P(B) − P(A∩B)`
- Independent: `P(A∩B) = P(A)·P(B)`
- Dice (2): total outcomes 36 ; Cards: 52 (13×4, 26 red/black, 12 face).

---

## Ch-12 · Geometry & Mensuration

**Areas / Perimeters**
- Triangle = `½·b·h` ; Equilateral = `(√3/4)a²` ; Heron = `√(s(s−a)(s−b)(s−c))`, `s=(a+b+c)/2`
- Rectangle `l·b` ; Square `a²` ; Parallelogram `b·h` ; Rhombus `½d₁d₂` ; Trapezium `½(a+b)h`
- Circle area `πr²`, circumference `2πr` ; Sector `θ/360·πr²`

**Solids (Volume / Surface)**
- Cube V=`a³`, TSA=`6a²` ; Cuboid V=`lbh`, TSA=`2(lb+bh+hl)`
- Cylinder V=`πr²h`, CSA=`2πrh`, TSA=`2πr(r+h)`
- Cone V=`⅓πr²h`, CSA=`πrl` (l=`√(r²+h²)`), TSA=`πr(r+l)`
- Sphere V=`⁴⁄₃πr³`, SA=`4πr²` ; Hemisphere V=`⅔πr³`, TSA=`3πr²`

**Triangle facts:** angle sum 180°; Pythagoras `a²+b²=c²`; common triples 3-4-5, 5-12-13, 8-15-17, 7-24-25.

---

## Ch-13 · Simplification (BODMAS)

- Order: **B**rackets → **O**rders(powers) → **D**ivision → **M**ultiplication → **A**ddition → **S**ubtraction
- `(a+b)² = a²+2ab+b²` , `(a−b)² = a²−2ab+b²`
- `a²−b² = (a+b)(a−b)` , `a³±b³ = (a±b)(a²∓ab+b²)`
- `(a+b+c)² = a²+b²+c²+2(ab+bc+ca)`
- Surds: `√a·√b=√(ab)` ; rationalize by conjugate.

---

## Ch-14 · Logarithms

- `logₐ(xy)=logₐx+logₐy` ; `logₐ(x/y)=logₐx−logₐy`
- `logₐ(xⁿ)=n·logₐx` ; `logₐa=1`, `logₐ1=0`
- **Base change:** `logₐx = log x / log a`
- `log_b a = 1/log_a b` ; `a^{logₐx}=x`
- `log 2≈0.3010`, `log 3≈0.4771`.

---

## Ch-15 · Set Theory

- `n(A∪B) = n(A)+n(B) − n(A∩B)`
- Three sets: `n(A∪B∪C) = Σn(A) − Σn(A∩B) + n(A∩B∩C)`
- Subsets of a set with n elements = `2ⁿ` ; proper subsets = `2ⁿ−1`
- De Morgan: `(A∪B)' = A'∩B'` , `(A∩B)' = A'∪B'`
- Use Venn diagrams for "exactly one / at least two" type questions.

---

### Universal exam tricks
1. **Plug the options** in for algebra-heavy questions — back-solving beats deriving.
2. **Fraction-to-percent table** memorized = instant percentage/profit sums.
3. **Approximate first**, eliminate far-off options, then compute precisely.
4. **Unit-digit method** for "find the unit digit" / large-power questions.
5. **Alligation** replaces two-variable equations in mixtures, average-speed, profit-mix.
