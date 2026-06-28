# Trigonometry — Solved Question Bank

> 📚 Navigation: [Back to README](README.md) | [Quant Formula Sheet](../Formula-Sheets/Quant_Formula_Sheet.md)

## Key Formulas

- `sin²θ + cos²θ = 1`
- `1 + tan²θ = sec²θ`
- `1 + cot²θ = cosec²θ`
- `tanθ = sinθ/cosθ`, `cotθ = cosθ/sinθ`
- Complementary angles: `sin(90° − θ) = cosθ`, `cos(90° − θ) = sinθ`, `tan(90° − θ) = cotθ`
- Standard values:
  - `sin: 0, ½, 1/√2, √3/2, 1` for `0°, 30°, 45°, 60°, 90°`
  - `cos: 1, √3/2, 1/√2, ½, 0` for `0°, 30°, 45°, 60°, 90°`
  - `tan: 0, 1/√3, 1, √3, ∞` for `0°, 30°, 45°, 60°, 90°`
- Height & distance: `tanθ = height / horizontal distance`

---

## 📐 Standard Trigonometric Values (Chart)

| θ      | **0°** | **30°** | **45°** | **60°** | **90°** |
|--------|:------:|:-------:|:-------:|:-------:|:-------:|
| **sin θ** | 0 | 1/2 | 1/√2 | √3/2 | 1 |
| **cos θ** | 1 | √3/2 | 1/√2 | 1/2 | 0 |
| **tan θ** | 0 | 1/√3 | 1 | √3 | ∞ |
| **cot θ** | ∞ | √3 | 1 | 1/√3 | 0 |
| **sec θ** | 1 | 2/√3 | √2 | 2 | ∞ |
| **cosec θ** | ∞ | 2 | √2 | 2/√3 | 1 |

> **Decimal quick-reference:** `1/√2 ≈ 0.707`, `√3/2 ≈ 0.866`, `1/√3 ≈ 0.577`, `√3 ≈ 1.732`.

---

## 🧾 Trigonometric Identities (Master List)

### 1. Reciprocal Identities
```
cosec θ = 1 / sin θ        sin θ = 1 / cosec θ
sec θ   = 1 / cos θ        cos θ = 1 / sec θ
cot θ   = 1 / tan θ        tan θ = 1 / cot θ
```

### 2. Quotient Identities
```
tan θ = sin θ / cos θ        cot θ = cos θ / sin θ
```

### 3. Pythagorean Identities ⭐ (most used in SSC)
| Identity | Useful rearrangements |
|---|---|
| `sin²θ + cos²θ = 1` | `sin²θ = 1 − cos²θ` &nbsp;•&nbsp; `cos²θ = 1 − sin²θ` |
| `1 + tan²θ = sec²θ` | `sec²θ − tan²θ = 1` &nbsp;•&nbsp; `tan²θ = sec²θ − 1` |
| `1 + cot²θ = cosec²θ` | `cosec²θ − cot²θ = 1` &nbsp;•&nbsp; `cot²θ = cosec²θ − 1` |

> 🔑 The last two come free from the first: divide `sin²θ + cos²θ = 1` by `cos²θ` → second; by `sin²θ` → third.

### 4. Complementary Angles (90° − θ)
```
sin(90° − θ) = cos θ        cos(90° − θ) = sin θ
tan(90° − θ) = cot θ        cot(90° − θ) = tan θ
sec(90° − θ) = cosec θ      cosec(90° − θ) = sec θ
```
> 🔑 **Co-function rule:** add the prefix **"co"** and the value is unchanged — `sin↔cos`, `tan↔cot`, `sec↔cosec`. Spot it when two angles **add to 90°** (e.g. `sin 70° = cos 20°`).

### 5. Even / Odd (Negative Angles)
```
sin(−θ) = −sin θ        cos(−θ) =  cos θ        tan(−θ) = −tan θ
cot(−θ) = −cot θ        sec(−θ) =  sec θ        cosec(−θ) = −cosec θ
```
> Only **cos** and **sec** keep their sign — see the [Negative Angles](#-negative-angles--sin−θ-cos−θ-) section below.

### 6. Sum & Difference Formulas
```
sin(A ± B) = sin A cos B ± cos A sin B
cos(A ± B) = cos A cos B ∓ sin A sin B
tan(A ± B) = (tan A ± tan B) / (1 ∓ tan A tan B)
```

### 7. Double-Angle Formulas
```
sin 2θ = 2 sin θ cos θ = 2 tan θ / (1 + tan²θ)
cos 2θ = cos²θ − sin²θ = 1 − 2 sin²θ = 2 cos²θ − 1 = (1 − tan²θ)/(1 + tan²θ)
tan 2θ = 2 tan θ / (1 − tan²θ)
```

### 8. Half-Angle / Power-Reduction (handy for `cos²`, `sin²`)
```
sin²θ = (1 − cos 2θ) / 2          cos²θ = (1 + cos 2θ) / 2
```

> 💡 **SSC priority:** sections **3 (Pythagorean)** and **4 (Complementary)** appear in nearly every Tier-1 paper. Sections 6–8 show up mainly in Tier-2 / harder identity-simplification questions.

---

### ✋ The √ Trick — build the whole sin row from memory

Write `0 1 2 3 4` under the five angles, then apply `sin θ = √(n) / 2`:

```
 θ        0°      30°     45°     60°     90°
 n         0       1       2       3       4
 √n/2   √0/2    √1/2    √2/2    √3/2    √4/2
 sin    = 0     = 1/2   = 1/√2  = √3/2  = 1
```

**Then:**
- **cos** = the same row **reversed** (read sin right-to-left): `1, √3/2, 1/√2, 1/2, 0`
- **tan** = `sin ÷ cos` for each column
- **cosec, sec, cot** = reciprocals of **sin, cos, tan** respectively

---

### 🤚 Hand (Finger) Trick for sin & cos

Hold your **left palm** facing you. Number the fingers **0 → 4** starting from the thumb:

```
  thumb   index   middle   ring   little
   0°      30°      45°      60°     90°
   0        1        2        3       4   ← count
```

To find **sin θ**: fold the finger for that angle. Count the fingers **below** it = `n`, then `sin θ = √n / 2`.
To find **cos θ**: count the fingers **above** the folded one instead (same `√(above)/2`).

> Example — **sin 60°**: fold the ring finger (60°). Fingers below = 3 → `sin 60° = √3 / 2`. ✅
> For **cos 60°**: fingers above the ring finger = 1 → `cos 60° = √1 / 2 = 1/2`. ✅

---

## ➖ Negative Angles — sin(−θ), cos(−θ), …

A negative angle is handled by the **even / odd** property of each function. You never need new values — just decide whether the minus sign **stays** or **vanishes**, then read the normal positive value off the chart above.

| Function | Type | Rule | Sign of the minus |
|---|---|---|---|
| **sin θ** | odd | `sin(−θ) = −sin θ` | **comes out front** |
| **cos θ** | even | `cos(−θ) = cos θ` | **disappears** |
| **tan θ** | odd | `tan(−θ) = −tan θ` | **comes out front** |
| **cot θ** | odd | `cot(−θ) = −cot θ` | **comes out front** |
| **sec θ** | even | `sec(−θ) = sec θ` | **disappears** |
| **cosec θ** | odd | `cosec(−θ) = −cosec θ` | **comes out front** |

> 🔑 **Memory hook:** *Only **cos** and its reciprocal **sec** survive unchanged — every other function flips sign.* (On the unit circle, flipping the angle below the x-axis keeps the x-coordinate = cos the same, but reverses the y-coordinate = sin.)

**Worked examples**

| Expression | Step | Value |
|---|---|---|
| `sin(−30°)` | odd → `−sin 30°` | **−1/2** |
| `cos(−60°)` | even → `cos 60°` | **1/2** |
| `tan(−45°)` | odd → `−tan 45°` | **−1** |
| `cos(−30°) + sin(−30°)` | `cos 30° − sin 30°` | `√3/2 − 1/2 = (√3 − 1)/2` |

⚠️ **Common trap:** students wrongly write `cos(−θ) = −cos θ`. It does **not** — cos is even, so `cos(−θ) = +cos θ`. Only the *odd* functions take the minus out.

---

## 📐 Pythagorean Triples — Recognise, Don't Calculate

When a question gives one ratio like `sin θ = 3/5`, `cos θ = 4/5`, or `tan θ = 3/4`, **don't** plug into `sin²θ + cos²θ = 1` to find the rest. Instantly recognise it as a **3–4–5 right triangle** and read off every other ratio.

> 🔑 **Memory hook:** the two smaller numbers are the legs (perpendicular & base), the largest is the hypotenuse. `sin = opp/hyp`, `cos = adj/hyp`, `tan = opp/adj`.

**Common triples to memorise:**

| Triple (P, B, H) | Recognise it when you see a ratio with… |
|---|---|
| **3 – 4 – 5** | 3, 4, or 5 in the denominator/numerator |
| **5 – 12 – 13** | 12 or 13 |
| **8 – 15 – 17** | 15 or 17 |
| **7 – 24 – 25** | 24 or 25 |

**Worked example**

> Given `sin θ = 3/5`, find `tan θ`.

```
sin θ = 3/5  →  opposite = 3, hypotenuse = 5  →  3–4–5 triangle  →  adjacent = 4
tan θ = opposite / adjacent = 3/4
```

✅ **tan θ = 3/4** — no identity, no square roots, ~3 seconds.

> 💡 **Bonus:** any multiple of a triple also works — `6–8–10`, `9–12–15`, `10–24–26` are all just scaled 3–4–5 / 5–12–13. If the numbers look "off", try dividing by a common factor to spot the base triple.

---

## 🪜 Ladder / Height & Distance — Stop Guessing sin vs cos

**Don't** memorise rules like *"ladder = sin"* or *"ladder = cos"* — they break the moment the angle is measured from a different side. Instead, run this 3-step routine every time:

**Step 1 — Where is the angle?** Read the question carefully:

| The angle is measured with the… | → Angle sits at the… |
|---|---|
| **Ground / Horizontal** | **bottom** of the ladder |
| **Wall / Vertical** | **top** of the ladder |

**Step 2 — Label the three sides relative to *that* angle:**
- **Opposite** — the side facing the angle
- **Adjacent** — the side touching the angle (other than the hypotenuse)
- **Hypotenuse** — always the ladder itself (the slanted side)

**Step 3 — Apply SOH-CAH-TOA:**

```
SOH → sin = Opposite / Hypotenuse
CAH → cos = Adjacent / Hypotenuse
TOA → tan = Opposite / Adjacent
```

> 🎯 **SSC reality check:** ~90% of ladder problems say *"the ladder makes an angle with the **ground**"* or use an **angle of elevation from the ground**. So when you spot the words **ground** or **horizontal**, the angle is at the **bottom** → the **wall (height) is Opposite** and the **floor distance is Adjacent**. Pick your ratio from there.

**Worked example**

> A ladder leans against a wall making **60° with the ground**; its foot is **5 m** from the wall. Find the ladder's length.

```
"with the ground" → angle at the bottom
Foot-to-wall distance (5 m) = Adjacent   |   Ladder = Hypotenuse
Adjacent + Hypotenuse → use CAH (cos)
cos 60° = Adjacent / Hypotenuse = 5 / L
½ = 5 / L  →  L = 10 m
```

✅ **Ladder = 10 m**

---

## EASY

**Q1.** Find the value of `sin 30° + cos 60°`.
(a) 1  (b) ½  (c) √3/2  (d) 0
**Answer: (a) 1**
*Solution:* `sin 30° = ½` and `cos 60° = ½`, so sum `= ½ + ½ = 1`.

**Q2.** Find `sin²45° + cos²45°`.
(a) 1  (b) ½  (c) √2  (d) 2
**Answer: (a) 1**
*Solution:* By the identity `sin²θ + cos²θ = 1` for any θ, the value is 1.

🔑 *Trick:* `sin²θ + cos²θ` is ALWAYS 1 — don't compute, just write 1.

**Q3.** Find the value of `tan 45°`.
(a) 1  (b) 0  (c) √3  (d) 1/√3
**Answer: (a) 1**
*Solution:* `tan 45° = sin 45°/cos 45° = (1/√2)/(1/√2) = 1`.

**Q4.** Simplify `sin(90° − θ)`.
(a) cos θ  (b) sin θ  (c) tan θ  (d) cot θ
**Answer: (a) cos θ**
*Solution:* Complementary-angle rule: `sin(90° − θ) = cos θ`.

**Q5.** Find `cos 0° + sin 90°`.
(a) 2  (b) 1  (c) 0  (d) ½
**Answer: (a) 2**
*Solution:* `cos 0° = 1` and `sin 90° = 1`, so sum `= 1 + 1 = 2`.

---

## MEDIUM

**Q6.** If `sin θ = 3/5`, find `cos θ` (θ acute).
(a) 4/5  (b) 5/4  (c) 3/4  (d) 5/3
**Answer: (a) 4/5**
*Solution:* `cos θ = √(1 − sin²θ) = √(1 − 9/25) = √(16/25) = 4/5`.

**Q7.** If `tan θ = 1`, find `θ` (acute).
(a) 45°  (b) 30°  (c) 60°  (d) 90°
**Answer: (a) 45°**
*Solution:* `tan 45° = 1`, so θ = 45°.

**Q8.** Evaluate `sin 60° · cos 30° + cos 60° · sin 30°`.
(a) 1  (b) √3/2  (c) ½  (d) √3/4
**Answer: (a) 1**
*Solution:* `= (√3/2)(√3/2) + (½)(½) = 3/4 + 1/4 = 1`. (This is `sin(60° + 30°) = sin 90° = 1`.)

**Q9.** If `sec θ = 13/5`, find `tan θ` (θ acute).
(a) 12/5  (b) 5/12  (c) 13/12  (d) 12/13
**Answer: (a) 12/5**
*Solution:* `tan²θ = sec²θ − 1 = 169/25 − 1 = 144/25`, so `tan θ = 12/5`.

**Q10.** Evaluate `(sin 30°)/(cos 60°) + (tan 45°)`.
(a) 2  (b) 1  (c) 3  (d) 0
**Answer: (a) 2**
*Solution:* `(½)/(½) = 1`, and `tan 45° = 1`, so total `= 1 + 1 = 2`.

**Q11.** Simplify `tan θ · cot θ`.
(a) 1  (b) 0  (c) tan²θ  (d) sec θ
**Answer: (a) 1**
*Solution:* `cot θ = 1/tan θ`, so `tan θ · cot θ = tan θ × (1/tan θ) = 1`.

🔑 *Trick:* Reciprocal pairs (tan·cot, sin·cosec, cos·sec) always multiply to 1.

---

## HARD

**Q12.** If `sin θ + cos θ = √2`, find θ (acute).
(a) 45°  (b) 30°  (c) 60°  (d) 90°
**Answer: (a) 45°**
*Solution:* Square: `1 + 2 sinθ cosθ = 2`, so `2 sinθ cosθ = 1`, meaning `sin 2θ = 1`, giving `2θ = 90°`, θ = 45°.

**Q13.** Simplify `(1 − cos²θ)/(sin θ)` for acute θ.
(a) sin θ  (b) cos θ  (c) tan θ  (d) 1
**Answer: (a) sin θ**
*Solution:* `1 − cos²θ = sin²θ`, so `sin²θ / sin θ = sin θ`.

**Q14.** A tower casts a shadow of length equal to its height. Find the angle of elevation of the sun.
(a) 45°  (b) 30°  (c) 60°  (d) 90°
**Answer: (a) 45°**
*Solution:* `tan θ = height/shadow = h/h = 1`, so θ = 45°.

**Q15.** From a point 30 m from the base of a tower, the angle of elevation of the top is 60°. Find the tower's height.
(a) `30√3 m`  (b) `30 m`  (c) `10√3 m`  (d) `60 m`
**Answer: (a) 30√3 m**
*Solution:* `tan 60° = height/30`, so `height = 30 × tan 60° = 30 × √3 = 30√3 m`.

🔑 *Trick:* In height-distance problems, set up `tanθ = opposite/adjacent` first, then plug the standard value.

---

## SSC PYQ PATTERN

**Q16.** (SSC CGL pattern) Evaluate `sin²30° + cos²30°`.
(a) 1  (b) ½  (c) √3/2  (d) 2
**Answer: (a) 1**
*Solution:* By identity `sin²θ + cos²θ = 1`, value is 1 (no calculation needed).

**Q17.** (SSC CGL pattern) If `cos θ = 4/5`, find `sin θ · tan θ` (θ acute).
(a) 9/20  (b) 3/5  (c) 3/4  (d) 12/25
**Answer: (a) 9/20**
*Solution:* `sin θ = 3/5`, `tan θ = (3/5)/(4/5) = 3/4`. Product `= (3/5)(3/4) = 9/20`.

**Q18.** (SSC CGL pattern) Simplify `sec²θ − tan²θ`.
(a) 1  (b) 0  (c) sec θ  (d) tan θ
**Answer: (a) 1**
*Solution:* From `1 + tan²θ = sec²θ`, we get `sec²θ − tan²θ = 1`.

**Q19.** (SSC CGL pattern) A ladder leans against a wall making 60° with the ground; its foot is 5 m from the wall. Find the ladder's length.
(a) 10 m  (b) `5√3 m`  (c) `10√3 m`  (d) 15 m
**Answer: (a) 10 m**
*Solution:* `cos 60° = base/ladder = 5/L`, so `½ = 5/L`, giving `L = 10 m`.

🔑 *Trick:* Identify which side is given (base/height/hypotenuse) to pick sin, cos, or tan correctly.

---

### 🔑 Exam Tricks Box

- `sin²θ + cos²θ = 1`, `sec²θ − tan²θ = 1`, `cosec²θ − cot²θ = 1` — recognise these and skip all working.
- Memorise the standard-angle table (0°, 30°, 45°, 60°, 90°) cold; it underlies nearly every question.
- Reciprocal/complementary identities turn long expressions into 1 — look for `sin(90°−θ) = cosθ` patterns.
- For height & distance, always write `tanθ = opposite/adjacent` first, then substitute the standard value.

> ✅ Trigonometry in SSC CGL is about identity recognition and the standard-angle table — master both and the section is fast and high-scoring.
