# 📐 Geometry & Mensuration — Dimension Change Relations

### *(Height, Radius, Length, Breadth, Side Changes)* — SSC CGL · CHSL · CPO · Banking · Railways · CAT

> **The single most predictable scoring topic in the paper.** Once you know *which power* a dimension carries, you never re-derive a formula — you just scale it. This chapter makes every "if side doubles / radius halves / height tripled" question a **5-second mental sum**.
>
> **Colour legend** (used throughout): 🔵 **Original formula** · 🟢 **New formula** · 🔴 **Shortcut** · 🟠 **Common mistake**
>
> Companion to [Geometry-Handbook-Formulas-and-Figures.md](Geometry-Handbook-Formulas-and-Figures.md). View the **PDF** so diagrams stay aligned.

---

## 0. The One Idea That Runs the Whole Chapter

Every measurement in geometry is built from powers of length. **Count the powers, and you know the scaling.**

```
   ┌────────────────────────────────────────────────────────────┐
   │   QUANTITY          POWER of length      Scale by k means   │
   │   ───────────────   ───────────────────  ─────────────────  │
   │   Length / Perimeter / Circumference /                      │
   │   Diagonal / Radius / Arc / Slant     →   ¹    →   × k       │
   │                                                             │
   │   AREA / CSA / LSA / TSA / Surface     →   ²    →   × k²     │
   │                                                             │
   │   VOLUME                               →   ³    →   × k³     │
   └────────────────────────────────────────────────────────────┘
```

🔴 **Master shortcut:** If **every** linear dimension is multiplied by *k*:

| Quantity | Multiplies by |
| :-- | :--: |
| Length-type (perimeter, diagonal, circumference, arc, slant) | **k** |
| Area-type (any area, CSA, LSA, TSA) | **k²** |
| Volume | **k³** |

**Percentage form:** if a dimension changes by *x*%, put `k = (1 ± x/100)`, then apply the power.
- Increase 20% → k = 1.2 · Decrease 25% → k = 0.75 · Increase 50% → k = 1.5 · Decrease 20% → k = 0.8

🟠 **The #1 mistake in the whole topic:** applying the linear percentage to area/volume directly. "Side up 20% → area up 20%" is **WRONG**. Area up = (1.2)² − 1 = **44%**. Always raise to the power *first*, subtract 1 *after*.

---

## 0.1 Percentage-Change Ready Reckoner

Keep these `k` and `k²`, `k³` values on your fingertips — most SSC questions use them.

| Change | k | k² (area) | k³ (volume) |
| :-- | :--: | :--: | :--: |
| ×2 (double, +100%) | 2 | 4 | 8 |
| ×3 (triple) | 3 | 9 | 27 |
| ÷2 (half, −50%) | 0.5 | 0.25 | 0.125 |
| +10% | 1.1 | 1.21 (+21%) | 1.331 (+33.1%) |
| +20% | 1.2 | 1.44 (+44%) | 1.728 (+72.8%) |
| +25% | 1.25 | 1.5625 (+56.25%) | 1.953 (+95.3%) |
| +50% | 1.5 | 2.25 (+125%) | 3.375 (+237.5%) |
| −10% | 0.9 | 0.81 (−19%) | 0.729 (−27.1%) |
| −20% | 0.8 | 0.64 (−36%) | 0.512 (−48.8%) |
| −25% | 0.75 | 0.5625 (−43.75%) | 0.4219 (−57.8%) |

🔴 **Two-factor percentage shortcut (for area / two dimensions):** if one dimension changes by *a*% and another by *b*%, net change =
`a + b + (a·b)/100` percent.
Example: length +20%, breadth −20% → `20 − 20 + (20·−20)/100 = −4%` (area **falls 4%**, never 0%).

---
---

# PART A — 2D FIGURES

*In 2D: perimeter/diagonal/circumference/arc scale as **k**; area scales as **k²**.*

---

## A1. Square

<!-- FIG:square -->

1. **Original formulas** — 🔵 Area `A = a²` · Perimeter `P = 4a` · Diagonal `d = a√2`
2. **One dimension changes** (a square has only one dimension, the side *a*):
   - Side ×2 → 🟢 `A = (2a)² = 4a²` → **Area ×4**; `P = 4(2a) = 8a` → **Perimeter ×2**; diagonal ×2.
   - Side ÷2 → Area ×¼, Perimeter ×½, Diagonal ×½.
3. **Multiple dimensions** — n/a (single dimension), but *area given* works backwards: if **area** doubles, side ×√2, perimeter ×√2.
4. 🔴 **SSC shortcut:** Square scales purely by side. Area = side², so `Area factor = (side factor)²`. Perimeter & diagonal = (side factor)¹.
5. **Memory trick:** *"Square = the name says it — everything about area is squared."* Side ×k ⇒ Area ×k².
6. **Exam pattern:** "Side of a square is increased by 20%, find % increase in area." (Answer 44%.) Or the reverse: "Area increased by 44%, find side increase" → √1.44 = 1.2 → **20%**.
7. 🟠 **Common mistakes:** (i) saying area ×2 when side ×2 (it's ×4). (ii) forgetting diagonal scales linearly (×k), not ×k².
8. **Numericals:**
   - *Q.* Side doubles. Area? → **×4** (4a²).
   - *Q.* Side +20%, area increase? → 1.2² − 1 = **44%**.
   - *Q.* Perimeter increases 30%, area increases by? → side ×1.3 → area ×1.69 → **69%**.
9. **Revision:** Side ×k → **A ×k², P ×k, d ×k.**

---

## A2. Rectangle

<!-- FIG:rectangle -->

1. **Original formulas** — 🔵 Area `A = l·b` · Perimeter `P = 2(l + b)` · Diagonal `d = √(l² + b²)`
2. **One dimension changes:**
   - Length ×2 (b fixed) → 🟢 `A = 2l·b` → **Area ×2**. Perimeter changes *non-uniformly* (only l part), so **no single factor** — must compute.
   - Breadth ÷2 (l fixed) → Area ×½.
3. **Multiple dimensions:** Area factor = **(l-factor) × (b-factor)**.
   - Length ×2 **and** breadth ×½ → Area ×(2 × ½) = **×1 (unchanged)**. 🔴 classic trap answer.
   - Length +20%, breadth +20% → 1.2×1.2 = **+44%**.
   - Length +20%, breadth −20% → 1.2×0.8 = 0.96 → **−4%** (use `a+b+ab/100`).
4. 🔴 **SSC shortcut:** For rectangle **area only multiply the two factors**; perimeter does *not* follow a clean factor unless both change by the same k.
5. **Memory trick:** *"Two sides, two factors — multiply them for area."*
6. **Exam pattern:** "Length doubled, breadth halved — effect on area?" (Unchanged). "L +10%, B +20%, area change?" (`10+20+2 = 32%`).
7. 🟠 **Mistakes:** (i) applying a single factor to perimeter when only one side changes. (ii) adding the two % for area instead of using `a+b+ab/100`. (iii) forgetting the cross-term (the `ab/100`).
8. **Numericals:**
   - *Q.* L ×3, B ×2 → Area **×6**.
   - *Q.* L −10%, B −20% → `−10 −20 + 2 = −28%` (area falls 28%).
   - *Q.* L +50%, B unchanged → Area **+50%** (only one factor).
9. **Revision:** Area ×(k_l·k_b). If both ×k → A ×k², P ×k, d ×k.

---

## A3. Triangle (general)

<!-- FIG:triangle -->

1. **Original formula** — 🔵 Area `A = ½ · b · h` · Perimeter = sum of sides.
2. **One dimension changes:**
   - Base ×2 (h fixed) → 🟢 `A = ½(2b)h = b·h` → **Area ×2**.
   - Height ÷2 → Area ×½.
3. **Multiple dimensions:** Area factor = **(base-factor) × (height-factor)**.
   - Base +20%, height −25% → 1.2 × 0.75 = 0.9 → **−10%**.
   - Base ×2, height ×3 → **×6**.
4. 🔴 **SSC shortcut:** Triangle area behaves exactly like rectangle — it's just ½ of one. Only base × height matter.
5. **Memory trick:** *"½ is a constant — it never changes the factor. Watch base and height only."*
6. **Exam pattern:** "Base increased 20%, height decreased 20%, area change?" (`20 −20 −4 = −4%`).
7. 🟠 **Mistakes:** (i) thinking the ½ affects scaling (it cancels). (ii) using a *side* instead of the base⟂height pair.
8. **Numericals:**
   - *Q.* Base ×4, height ÷2 → Area **×2**.
   - *Q.* Base +30%, height +30% → `30+30+9 = 69%`.
9. **Revision:** A ×(k_b·k_h). All-sides ×k (similar triangle) → A ×k², P ×k.

---

## A4. Equilateral Triangle

<!-- FIG:equilateral -->

1. **Original formulas** — 🔵 Area `A = (√3/4)a²` · Perimeter `P = 3a` · Height `h = (√3/2)a`
2. **One dimension (side a):** it's the *only* dimension → behaves like a square.
   - Side ×2 → 🟢 `A = (√3/4)(2a)² = 4·(√3/4)a²` → **Area ×4**; P ×2; h ×2.
   - Side ÷2 → Area ×¼.
3. **Multiple dimensions:** n/a — single dimension.
4. 🔴 **SSC shortcut:** Everything with a²-form (equilateral triangle, square, circle) scales ×k² in area for side ×k.
5. **Memory trick:** *"Equal sides → treat like a square: area is a squared quantity."*
6. **Exam pattern:** "Side of equilateral triangle tripled, area becomes?" (×9).
7. 🟠 **Mistakes:** (i) scaling height by k² (it's k). (ii) forgetting the √3/4 is a constant and cancels in ratios.
8. **Numericals:**
   - *Q.* Side +100% (doubles) → Area **+300%** (×4).
   - *Q.* Side +50% → Area 1.5² = 2.25 → **+125%**.
9. **Revision:** Side ×k → A ×k², P ×k, h ×k.

---

## A5. Circle

<!-- FIG:circle -->

1. **Original formulas** — 🔵 Area `A = πr²` · Circumference `C = 2πr = πd` · Diameter `d = 2r`
2. **One dimension (radius r):**
   - Radius ×2 → 🟢 `A = π(2r)² = 4πr²` → **Area ×4**; `C = 2π(2r)` → **Circumference ×2**.
   - Radius ÷2 → Area ×¼, Circumference ×½.
   - **Diameter ×2 = Radius ×2** (same factor) → Area ×4, C ×2.
3. **Multiple dimensions:** n/a — a circle has one dimension.
4. 🔴 **SSC shortcut:** Circle = pure r² for area, r¹ for circumference. Diameter and radius scale identically.
5. **Memory trick:** *"Area is π-r-squared → the '-squared' tells you the power."*
6. **Exam pattern:** "Radius increased 50%, area increases by?" (2.25 → **125%**). "Circumference doubles, area becomes?" (r ×2 → **×4**).
7. 🟠 **Mistakes:** (i) circumference ×4 when radius ×2 (it's ×2). (ii) treating a *diameter* change as different from radius — it's the same factor.
8. **Numericals:**
   - *Q.* Radius halves → Area **¼**, Circumference **½**.
   - *Q.* Diameter tripled → Area **×9**, Circumference **×3**.
   - *Q.* Area increased 44% → radius √1.44 = ×1.2 → **+20%**.
9. **Revision:** r (or d) ×k → **A ×k², C ×k.**

---

## A6. Semicircle

<!-- FIG:semicircle -->

1. **Original formulas** — 🔵 Area `A = ½πr²` · Perimeter `P = πr + 2r = (π + 2)r` (curved arc **+** diameter).
2. **One dimension (r):**
   - Radius ×2 → 🟢 `A = ½π(2r)² = 4·½πr²` → **Area ×4**; `P = (π+2)(2r)` → **Perimeter ×2**.
   - Radius ÷2 → Area ×¼, Perimeter ×½.
3. **Multiple dimensions:** n/a.
4. 🔴 **SSC shortcut:** Same powers as a full circle — the ½ and (π+2) are constants that cancel in any ratio.
5. **Memory trick:** *"Half a circle scales exactly like a whole circle."*
6. **Exam pattern:** "Radius of a semicircular field doubled — perimeter change?" (**×2**).
7. 🟠 **Mistakes:** (i) **forgetting the diameter** in perimeter — using only πr. Perimeter is `πr + 2r`, not `πr`. (ii) scaling perimeter by k².
8. **Numericals:**
   - *Q.* r = 7, perimeter? → (π+2)·7 = (22/7 + 2)·7 = 22 + 14 = **36 cm**.
   - *Q.* r ×3 → Area **×9**, Perimeter **×3**.
9. **Revision:** r ×k → A ×k², P ×k. *Perimeter = curved arc + diameter.*

---

## A7. Sector of a Circle

<!-- FIG:sector -->

1. **Original formulas** (angle θ) — 🔵 Area `A = (θ/360)πr²` · Arc `ℓ = (θ/360)·2πr = (θ/180)πr` · Perimeter `P = ℓ + 2r`.
2. **One dimension changes:**
   - **Radius ×2** (θ fixed) → 🟢 Area `= (θ/360)π(2r)²` → **×4**; Arc `= (θ/360)2π(2r)` → **×2**.
   - **Angle ×2** (r fixed) → Area ×2, Arc ×2 (θ is *linear* in both, since area's r is unchanged).
3. **Multiple dimensions:**
   - Radius ×2 **and** angle ×2 → Area ×(4·2) = **×8**; Arc ×(2·2) = **×4**.
   - Radius ÷2, angle ×2 → Area ×(¼·2) = **×½**; Arc ×(½·2) = **×1**.
4. 🔴 **SSC shortcut:** Treat **radius** with its normal powers (Area r², Arc r¹) and **angle θ as a plain linear multiplier** on both area and arc.
5. **Memory trick:** *"θ is a fraction of the circle → it scales area and arc equally and linearly. r keeps its square/linear powers."*
6. **Exam pattern:** "Radius doubled, angle same — arc length change?" (**×2**). "Angle doubled, radius same — area change?" (**×2**).
7. 🟠 **Mistakes:** (i) scaling area by θ² (θ is linear, not squared). (ii) forgetting the two radii `2r` in perimeter.
8. **Numericals:**
   - *Q.* r ×3, θ same → Area **×9**, Arc **×3**.
   - *Q.* θ from 60° to 120° (×2), r same → Area & Arc both **×2**.
9. **Revision:** Area ×(k_r²·k_θ), Arc ×(k_r·k_θ).

---

## A8. Rhombus

<!-- FIG:rhombus -->

1. **Original formulas** — 🔵 Area `A = ½·d₁·d₂` (diagonals) · Perimeter `P = 4a` · Side `a = ½√(d₁²+d₂²)`.
2. **One dimension:**
   - Diagonal d₁ ×2 (d₂ fixed) → 🟢 `A = ½(2d₁)d₂` → **Area ×2**.
   - Side ×2 (a *similar* rhombus, both diagonals ×2) → Area ×4, Perimeter ×2.
3. **Multiple dimensions:** Area factor = **(d₁-factor)(d₂-factor)**.
   - Both diagonals ×2 → Area **×4**.
   - d₁ +20%, d₂ +20% → **+44%**.
4. 🔴 **SSC shortcut:** Rhombus area works on **diagonals like a rectangle works on sides** — multiply the two factors.
5. **Memory trick:** *"Half-d-one-d-two — treat the two diagonals as the two 'sides' of area."*
6. **Exam pattern:** "Both diagonals doubled, area?" (**×4**). "One diagonal +50%, other same?" (**+50%**).
7. 🟠 **Mistakes:** (i) using side for area (must use diagonals or side×height). (ii) forgetting the ½.
8. **Numericals:**
   - *Q.* d₁ ×3, d₂ ÷2 → Area **×1.5**.
   - *Q.* Side ×2 (similar) → Area **×4**, Perimeter **×2**.
9. **Revision:** Area ×(k_{d1}·k_{d2}); similar-scale side ×k → A ×k², P ×k.

---

## A9. Parallelogram

<!-- FIG:parallelogram -->

1. **Original formula** — 🔵 Area `A = b · h` (base × ⟂ height) · Perimeter `P = 2(a + b)`.
2. **One dimension:**
   - Base ×2 (h fixed) → 🟢 **Area ×2**.
   - Height ÷2 → Area ×½.
3. **Multiple dimensions:** Area factor = **(base-factor)(height-factor)** (identical to rectangle/triangle logic).
   - Base ×2, height ×3 → **×6**. Base +25%, height −20% → 1.25×0.8 = **×1 (no change)**.
4. 🔴 **SSC shortcut:** Parallelogram = rectangle for scaling purposes — base × height only.
5. **Memory trick:** *"A slanted rectangle scales like a rectangle."*
6. **Exam pattern:** "Base up 20%, height down 20%, area?" (`−4%`).
7. 🟠 **Mistakes:** (i) using the slant side instead of ⟂ height. (ii) same `a+b+ab/100` cross-term slip as rectangle.
8. **Numericals:**
   - *Q.* Base ×4, height ÷2 → **×2**.
   - *Q.* Base +10%, height +10% → **+21%**.
9. **Revision:** A ×(k_b·k_h).

---

## A10. Trapezium

<!-- FIG:trapezium -->

1. **Original formula** — 🔵 Area `A = ½(a + b)·h` (mean of parallel sides × height).
2. **One dimension:**
   - Height ×2 (a, b fixed) → 🟢 `A = ½(a+b)(2h)` → **Area ×2**.
   - A parallel side changing alone does **not** give a clean factor (it's `a+b`, a sum) — must compute.
3. **Multiple dimensions:**
   - **Both** parallel sides ×2 and height ×2 (similar figure) → Area **×4**.
   - Height ×3, sides fixed → **×3**.
4. 🔴 **SSC shortcut:** Height is a clean linear factor. The `(a+b)` sum is **not** a factor unless both parallel sides scale by the *same* k.
5. **Memory trick:** *"Height is the honest factor; the two parallel sides add — you can't factor a sum."*
6. **Exam pattern:** "Height of a trapezium doubled, parallel sides same — area?" (**×2**). Similar-scaled (all ×k) → area ×k².
7. 🟠 **Mistakes:** (i) treating `(a+b)` as multiplying when only one parallel side changes. (ii) forgetting the ½.
8. **Numericals:**
   - *Q.* a = 6, b = 10, h = 4 → A = ½(16)(4) = **32 cm²**. Now h ×2 → **64 cm²** (×2). ✓
   - *Q.* All linear dims ×3 (similar) → Area **×9**.
9. **Revision:** Height ×k → A ×k. All-linear ×k → A ×k².

---

## A11. Quadrilateral (general, via a diagonal)

```
        B_______C
        |\      |
        | \  d  |     Split by diagonal AC = d.
        |  \    |     Area = ½·d·(h₁ + h₂)
        |   \   |     h₁, h₂ = ⟂ offsets from B and D
        A____\__D
```

1. **Original formula** — 🔵 Area `A = ½·d·(h₁ + h₂)` (diagonal × sum of the two offsets).
2. **One dimension:**
   - Diagonal d ×2 (offsets fixed) → 🟢 **Area ×2**.
   - An offset alone → sum `(h₁+h₂)`, no clean factor.
3. **Multiple dimensions:** Fully similar (all lengths ×k) → **Area ×k²**, perimeter ×k.
4. 🔴 **SSC shortcut:** Any planar figure, when *uniformly* scaled by k, has **area ×k², perimeter ×k** — no need for its specific formula.
5. **Memory trick:** *"Whatever the shape, uniform scale → area squares, boundary just scales."*
6. **Exam pattern:** "A field's map is scaled up 3×; actual area is how many times the model?" (**×9**).
7. 🟠 **Mistakes:** scaling a *sum* term as if it were a single factor.
8. **Numericals:**
   - *Q.* All sides & diagonals ×2 → Area **×4**.
   - *Q.* Diagonal ×3, offsets same → Area **×3**.
9. **Revision:** Uniform ×k → A ×k², P ×k.

---

## ★ 2D Master Recap

| Figure | Area formula | Uniform side/radius ×k ⇒ Area | ⇒ Perimeter/Circ |
| :-- | :-- | :--: | :--: |
| Square | a² | ×k² | ×k |
| Rectangle | l·b | ×k² (both), or k_l·k_b | ×k (both) |
| Triangle | ½bh | ×k² (similar) | ×k |
| Equilateral △ | (√3/4)a² | ×k² | ×k |
| Circle | πr² | ×k² | C ×k |
| Semicircle | ½πr² | ×k² | ×k |
| Sector | (θ/360)πr² | ×k² (r), ×linear (θ) | arc ×k |
| Rhombus | ½d₁d₂ | ×k² (both diag) | ×k |
| Parallelogram | b·h | ×k² (similar) | ×k |
| Trapezium | ½(a+b)h | ×k² (similar) | ×k |
| Quadrilateral | ½d(h₁+h₂) | ×k² (similar) | ×k |

---
---

# PART B — 3D SOLIDS

*In 3D: slant/diagonal/edge scale as **k**; every surface area (CSA/LSA/TSA) scales as **k²**; volume scales as **k³**.*

---

## B1. Cube

<!-- FIG:cube -->

1. **Original formulas** — 🔵 Volume `V = a³` · TSA `= 6a²` · LSA `= 4a²` · Space diagonal `= a√3` · Edge total `= 12a`.
2. **One dimension (edge a — the only one):**
   - Edge ×2 → 🟢 `V = (2a)³ = 8a³` → **Volume ×8**; TSA `= 6(2a)² = 24a²` → **×4**; diagonal ×2.
   - Edge ÷2 → V ×⅛, SA ×¼, diagonal ×½.
3. **Multiple dimensions:** n/a — one dimension.
4. 🔴 **SSC shortcut:** Cube is the purest case: edge ×k → **V ×k³, SA ×k², diagonal ×k.**
5. **Memory trick:** *"Cube → cubes it: 1-2-3 powers. Length k, Surface k², Volume k³."*
6. **Exam pattern:** "Edge of a cube increased 50%, volume increases by?" (1.5³ = 3.375 → **237.5%**). "Volume increased 8×, edge?" (**×2**).
7. 🟠 **Mistakes:** (i) SA ×8 when edge ×2 (SA is ×4). (ii) diagonal ×k² (it's ×k).
8. **Numericals:**
   - *Q.* Edge tripled → V **×27**, SA **×9**.
   - *Q.* Edge +20% → V 1.728 → **+72.8%**, SA 1.44 → **+44%**.
9. **Revision:** Edge ×k → **V ×k³, TSA/LSA ×k², diagonal ×k.**

---

## B2. Cuboid

<!-- FIG:cuboid -->

1. **Original formulas** — 🔵 `V = lbh` · `TSA = 2(lb + bh + hl)` · `LSA = 2h(l + b)` · diagonal `= √(l²+b²+h²)`.
2. **One dimension:**
   - Height ×2 (l, b fixed) → 🟢 `V = lb(2h)` → **Volume ×2**. TSA/diagonal have no clean single factor (mixed sums).
3. **Multiple dimensions:** Volume factor = **k_l · k_b · k_h**.
   - **Length doubled, breadth tripled, height halved** → `2 × 3 × ½` = **Volume ×3**.
   - All three ×2 (similar) → V ×8, TSA ×4, diagonal ×2.
   - l +10%, b +20%, h −20% → 1.1×1.2×0.8 = 1.056 → **+5.6%**.
4. 🔴 **SSC shortcut:** **Volume = multiply the three factors.** TSA/diagonal only get a clean factor when *all* dimensions scale by the same k.
5. **Memory trick:** *"Three sides → three factors, multiplied, for volume."*
6. **Exam pattern:** "L ×2, B ×3, H ÷2 — volume becomes?" (**×3**). "All edges +10% — volume up?" (1.331 → **33.1%**).
7. 🟠 **Mistakes:** (i) adding the three factors instead of multiplying. (ii) applying one factor to TSA when only one edge changes.
8. **Numericals:**
   - *Q.* L ×2, B ×2, H ×2 → V **×8**.
   - *Q.* L −20%, B −20%, H unchanged → V ×0.64 → **−36%** (an *area-type* change since one dim fixed).
9. **Revision:** V ×(k_l·k_b·k_h); uniform ×k → V ×k³, TSA ×k², diagonal ×k.

---

## B3. Cylinder

<!-- FIG:cylinder -->

1. **Original formulas** — 🔵 `V = πr²h` · `CSA = 2πrh` · `TSA = 2πr(r + h)`.
2. **One dimension:**
   - **Radius ×2** (h fixed) → 🟢 `V = π(2r)²h = 4πr²h` → **Volume ×4**; `CSA = 2π(2r)h` → **×2**.
   - **Radius ÷2** → `V = π(r/2)²h = ¼πr²h` → **Volume ×¼**; CSA ×½.
   - **Height ×2** (r fixed) → `V = πr²(2h)` → **Volume ×2**; `CSA = 2πr(2h)` → **×2**.
   - **Height ÷2** → V ×½, CSA ×½.
   - **Diameter ×2 = Radius ×2** → V ×4, CSA ×2.
3. **Multiple dimensions:** V factor = **(r-factor)² × (h-factor)**; CSA factor = **(r-factor) × (h-factor)**.
   - **Radius ×2 & height ÷2** → V `= 4 × ½` = **×2**; CSA `= 2 × ½` = **×1 (unchanged)**.
   - **Radius ÷2 & height ×2** → V `= ¼ × 2` = **×½**; CSA `= ½ × 2` = **×1**.
   - **Radius ×2 & height ×2** (similar) → V ×8, CSA ×4, TSA ×4.
4. 🔴 **SSC shortcut:** Volume: **square the radius factor, times the height factor.** CSA: radius factor × height factor. TSA gets a single factor **only** if r and h scale together.
5. **Memory trick:** *"r is squared in volume, once in CSA; h is once in both."*
6. **Exam pattern:** "Radius doubled, height halved — volume?" (**×2**). "Radius +50%, height same — CSA?" (**×1.5**).
7. 🟠 **Mistakes:** (i) squaring the height (h is linear). (ii) TSA — don't apply a single factor unless r and h scale equally; the r² and r·h terms scale differently otherwise.
8. **Numericals:**
   - *Q.* r ×3, h same → V **×9**, CSA **×3**.
   - *Q.* r same, h ×3 → V **×3**, CSA **×3**.
   - *Q.* r +20%, h +50% → V = 1.44 × 1.5 = 2.16 → **+116%**.
9. **Revision:** V ×(k_r²·k_h), CSA ×(k_r·k_h); uniform ×k → V ×k³, CSA/TSA ×k².

---

## B4. Cone

<!-- FIG:cone -->

1. **Original formulas** — 🔵 `V = ⅓πr²h` · `CSA = πrl` · `TSA = πr(l + r)` · Slant `l = √(r² + h²)`.
2. **One dimension:**
   - **Radius ×2** (h fixed) → 🟢 `V = ⅓π(2r)²h = 4·⅓πr²h` → **Volume ×4**. (CSA changes non-trivially because *l* depends on r.)
   - **Height ×2** (r fixed) → `V = ⅓πr²(2h)` → **Volume ×2**.
   - **Radius ÷2** → Volume ×¼.
   - **Slant height ×2** with r same → `CSA = πr(2l)` → **CSA ×2** (treating l as independent).
3. **Multiple dimensions:** V factor = **(r-factor)² × (h-factor)**.
   - **Radius ×2 & height halved** → V `= 4 × ½` = **×2**.
   - **Radius ÷2 & height ×2** → V `= ¼ × 2` = **×½**.
   - All linear (r, h, l) ×2 → V ×8, CSA ×4, TSA ×4.
4. 🔴 **SSC shortcut:** Cone volume scales **exactly like a cylinder** (r² · h) — the ⅓ is a constant. For CSA/TSA, if the whole cone is scaled by k, they go ×k².
5. **Memory trick:** *"⅓ is a decoration — cone volume = cylinder volume rules (r² h)."*
6. **Exam pattern:** "Radius doubled, height halved — cone volume?" (**×2**). "Radius same, height tripled — volume?" (**×3**).
7. 🟠 **Mistakes:** (i) forgetting **l depends on r and h** — you can't hold CSA's factor clean when only r or only h changes. (ii) scaling CSA by r² (it's r·l).
8. **Numericals:**
   - *Q.* r ×3, h same → V **×9**.
   - *Q.* r same, h ×2 → V **×2**.
   - *Q.* Whole cone scaled ×2 → V ×8, CSA ×4, slant ×2.
9. **Revision:** V ×(k_r²·k_h); uniform ×k → V ×k³, CSA/TSA ×k², slant ×k.

---

## B5. Sphere

<!-- FIG:sphere -->

1. **Original formulas** — 🔵 `V = (4/3)πr³` · Surface `S = 4πr²` · Diameter `d = 2r`.
2. **One dimension (r):**
   - **Radius ×2** → 🟢 `V = (4/3)π(2r)³ = 8·(4/3)πr³` → **Volume ×8**; `S = 4π(2r)²` → **Surface ×4**.
   - **Radius ×3** → **Volume ×27**, **Surface ×9**.
   - **Radius ÷2** → Volume ×⅛, Surface ×¼.
   - **Diameter ×2 = Radius ×2** → V ×8, S ×4.
3. **Multiple dimensions:** n/a — one dimension.
4. 🔴 **SSC shortcut:** Sphere is the cleanest 3D case: **r ×k → V ×k³, S ×k².** No height, no slant.
5. **Memory trick:** *"Sphere = radius only. Volume cubes it, surface squares it."*
6. **Exam pattern:** "Radius of a sphere increased 50%, volume increases by?" (1.5³ = 3.375 → **237.5%**). "Surface ×9 → radius?" (**×3**).
7. 🟠 **Mistakes:** (i) V ×4 when r ×2 (it's ×8 — cube it). (ii) confusing diameter change as different from radius.
8. **Numericals:**
   - *Q.* r ÷2 → V **×⅛**, S **×¼**.
   - *Q.* r +20% → V 1.728 → **+72.8%**, S 1.44 → **+44%**.
9. **Revision:** r ×k → **V ×k³, S ×k².**

---

## B6. Hemisphere

<!-- FIG:hemisphere -->

1. **Original formulas** — 🔵 `V = (2/3)πr³` · `CSA = 2πr²` · `TSA = 3πr²`.
2. **One dimension (r):**
   - Radius ×2 → 🟢 `V = (2/3)π(2r)³` → **×8**; CSA & TSA `= …(2r)²` → **×4**.
   - Radius ÷2 → V ×⅛, SA ×¼.
3. **Multiple dimensions:** n/a.
4. 🔴 **SSC shortcut:** Same powers as a sphere — r ×k → V ×k³, SA ×k². Constants (2/3, 2π, 3π) all cancel in ratios.
5. **Memory trick:** *"Half a ball, same power law: V cubes, SA squares."*
6. **Exam pattern:** "Radius of a hemispherical bowl doubled — volume?" (**×8**).
7. 🟠 **Mistakes:** (i) forgetting TSA = 3πr² includes the **flat circular face** (CSA is only 2πr²). (ii) scaling SA by k³.
8. **Numericals:**
   - *Q.* r ×3 → V **×27**, SA **×9**.
   - *Q.* r +50% → V **+237.5%**, SA **+125%**.
9. **Revision:** r ×k → V ×k³, CSA/TSA ×k².

---

## B7. Frustum of a Cone

<!-- FIG:frustum -->

1. **Original formulas** — 🔵 `V = ⅓πh(R² + Rr + r²)` · `CSA = π(R + r)l` · `TSA = CSA + πR² + πr²` · Slant `l = √(h² + (R−r)²)`.
2. **One dimension:** because R, r, h are interlinked through sums, a *single* dimension change has **no clean factor** — compute directly.
3. **Multiple dimensions — the exam-usable case:** scale **all** linear dimensions (R, r, h, l) by the same k → 🟢 **V ×k³, CSA ×k², TSA ×k², slant ×k.**
   - Whole frustum ×2 → V ×8, CSA ×4.
4. 🔴 **SSC shortcut:** Don't try to factor a single dimension of a frustum. If it's *uniformly* scaled, apply k³/k²/k. Otherwise, plug numbers into the formula.
5. **Memory trick:** *"Frustum = a truncated cone; only whole-figure scaling gives clean k³/k² powers."*
6. **Exam pattern:** "A bucket (frustum) enlarged uniformly 3× — capacity becomes?" (**×27**).
7. 🟠 **Mistakes:** (i) treating (R² + Rr + r²) as scalable by one radius. (ii) slant `l` uses `(R − r)`, **not** `(R + r)`.
8. **Numericals:**
   - *Q.* Whole frustum ×2 → V **×8**, CSA **×4**.
   - *Q.* R = 6, r = 3, h = 4 → l = √(16 + 9) = **5**; CSA = π(9)(5) = **45π**.
9. **Revision:** Uniform ×k → V ×k³, CSA/TSA ×k², slant ×k.

---

## B8. Prism (uniform cross-section)

<!-- FIG:prism -->

1. **Original formulas** — 🔵 `V = (Base area B) × (length h)` · `LSA = (Base perimeter P) × h` · `TSA = 2B + Ph`.
2. **One dimension:**
   - **Length h ×2** (base fixed) → 🟢 `V = B(2h)` → **Volume ×2**; `LSA = P(2h)` → **×2**.
   - **Base scaled ×m** (all base lengths ×m, h fixed) → B ×m², P ×m → V ×m², LSA ×m².
3. **Multiple dimensions:** V factor = **(base-area factor) × (length factor)** = **m² · k** (base linear ×m, length ×k).
   - Base doubled linearly (m=2) & length ×3 → V ×(4·3) = **×12**.
   - Whole prism ×k → V ×k³, all SA ×k².
4. 🔴 **SSC shortcut:** Prism volume = base-area factor × length factor. Base area scales ×(base-linear)².
5. **Memory trick:** *"A prism is an extruded 2D shape — the base carries the 2D power law, the length adds one more."*
6. **Exam pattern:** "Cross-section sides doubled, length same — volume?" (base area ×4 → **V ×4**).
7. 🟠 **Mistakes:** (i) scaling base area linearly (it's squared in base sides). (ii) forgetting `2B` in TSA.
8. **Numericals:**
   - *Q.* Length ×5, base fixed → V **×5**.
   - *Q.* Base linear ×2, length ×2 (similar) → V **×8**.
9. **Revision:** V ×(m²·k); uniform ×k → V ×k³, SA ×k².

---

## B9. Pyramid

<!-- FIG:pyramid -->

1. **Original formulas** — 🔵 `V = ⅓ · B · h` · `LSA = ½ · P · l` · `TSA = B + ½Pl` · slant `l` (from h and base).
2. **One dimension:**
   - **Height h ×2** (base fixed) → 🟢 `V = ⅓B(2h)` → **Volume ×2**.
   - **Base scaled linearly ×m** (h fixed) → B ×m² → **Volume ×m²**.
3. **Multiple dimensions:** V factor = **(base-area factor) × (height factor)** = **m² · k**.
   - Base sides ×2 & height ×3 → V ×(4·3) = **×12**.
   - Whole pyramid ×k → V ×k³, LSA/TSA ×k², slant ×k.
4. 🔴 **SSC shortcut:** Pyramid volume = ⅓ · base-area factor · height factor; base area scales as (base-linear)². (Same law as prism, with the ⅓.)
5. **Memory trick:** *"⅓ · base · height — base is a 2D area (squares), height is linear."*
6. **Exam pattern:** "Base edge doubled, height same — volume of a square pyramid?" (base area ×4 → **×4**).
7. 🟠 **Mistakes:** (i) scaling base area linearly. (ii) confusing slant height *l* with vertical height *h* in the volume formula (volume uses **h**, LSA uses **l**).
8. **Numericals:**
   - *Q.* Height tripled, base same → V **×3**.
   - *Q.* Whole pyramid ×2 → V **×8**, LSA **×4**, slant **×2**.
9. **Revision:** V ×(m²·k); uniform ×k → V ×k³, SA ×k², slant ×k.

---
---

# PART C — ★ DIMENSION CHANGE SHORTCUT TABLE (Master)

🔴 *The exam's whole point in one board. "×k" reads "multiplied by k".*

### 2D figures  *(4th column = perimeter / circumference / arc / diagonal)*

| Figure | Change | Area | Boundary / other length |
| :-- | :-- | :--: | :-- |
| Square | Side ×2 | ×4 | Perimeter ×2, diagonal ×2 |
| Square | Side ×3 | ×9 | Perimeter ×3, diagonal ×3 |
| Rectangle | L ×2, B ×½ | ×1 (same) | compute (mixed) |
| Rectangle | L ×2, B ×3 | ×6 | compute (mixed) |
| Triangle | Base ×2, Height ×3 | ×6 | compute (mixed) |
| Equilateral △ | Side ×2 | ×4 | Perimeter ×2, height ×2 |
| Circle | Radius ×2 | ×4 | Circumference ×2 |
| Circle | Radius ×3 | ×9 | Circumference ×3 |
| Circle | Radius ×½ | ×¼ | Circumference ×½ |
| Semicircle | Radius ×2 | ×4 | Perimeter ×2 |
| Sector | Radius ×2 (θ same) | ×4 | Arc ×2 |
| Sector | Angle ×2 (r same) | ×2 | Arc ×2 |
| Rhombus | Both diagonals ×2 | ×4 | Perimeter ×2 |
| Parallelogram | Base ×2, Height ×½ | ×1 (same) | compute (mixed) |
| Trapezium | Height ×2 (sides same) | ×2 | — |

### 3D solids  *(surface column = CSA/LSA; TSA scales as k² only under uniform scaling)*

| Solid | Change | Volume | Surface (CSA/LSA/TSA) |
| :-- | :-- | :--: | :-- |
| Cube | Side ×2 | ×8 | ×4 (diagonal ×2) |
| Cube | Side ×3 | ×27 | ×9 (diagonal ×3) |
| Cuboid | L×2, B×3, H×½ | ×3 | compute (mixed) |
| Cuboid | all ×2 | ×8 | TSA ×4 (diagonal ×2) |
| Cylinder | Radius ×2 (h same) | ×4 | CSA ×2, TSA changes* |
| Cylinder | Height ×2 (r same) | ×2 | CSA ×2, TSA changes* |
| Cylinder | R ×2 & H ×½ | ×2 | CSA ×1 (same), TSA changes* |
| Cylinder | all ×2 | ×8 | CSA ×4, TSA ×4 |
| Cone | Radius ×2 (h same) | ×4 | l changes — compute |
| Cone | Height ×2 (r same) | ×2 | l changes — compute |
| Cone | R ×2 & H ×½ | ×2 | l changes — compute |
| Cone | all ×2 | ×8 | CSA ×4, TSA ×4 (slant ×2) |
| Sphere | Radius ×2 | ×8 | Surface ×4 |
| Sphere | Radius ×3 | ×27 | Surface ×9 |
| Sphere | Radius ×½ | ×⅛ | Surface ×¼ |
| Hemisphere | Radius ×2 | ×8 | CSA/TSA ×4 |
| Frustum | all ×2 | ×8 | CSA ×4 (slant ×2) |
| Prism | Length ×2 (base same) | ×2 | LSA ×2 |
| Prism | Base linear ×2, len same | ×4 | compute |
| Pyramid | Height ×2 (base same) | ×2 | — |
| Pyramid | all ×2 | ×8 | LSA ×4 (slant ×2) |

*\*Cylinder/cone TSA gets a single clean factor **only** when r and h scale by the same k (then ×k²); otherwise compute term-by-term.*

---

# PART D — SSC SHORTCUTS (the reasoning behind every row)

🔴 **Shortcut 1 — Power counting.** Volume depends on **cubic** dimensions (k³), all areas/surfaces on **square** dimensions (k²), all length quantities (perimeter, circumference, arc, slant, diagonal, radius) change **linearly** (k¹).

🔴 **Shortcut 2 — Multiply the factors.** When several dimensions change together, multiply their individual factors, **each raised to the power it carries** in the formula.
`V_cylinder = πr²h` → radius ×a, height ×b → volume × **a²b**.

🔴 **Shortcut 3 — Constants vanish.** π, ½, ⅓, √3/4, 4/3, (π+2) etc. are constants — they **cancel** in every "how many times / what %" question. Ignore them; only variable dimensions scale.

🔴 **Shortcut 4 — Percentages.** Convert to a factor `k = 1 ± x/100` first, apply the power, then subtract 1 for the % change. For two area-factors use `a + b + ab/100`.

🔴 **Shortcut 5 — Reverse questions.** "Volume became 8×, find edge change" → take the cube root of 8 = 2 → edge ×2 (+100%). Area ×k² given → side = √k². Volume ×k³ given → side = ∛k³.

🔴 **Shortcut 6 — Diameter = Radius factor.** For circle/sphere/cylinder/cone, a diameter change is the **same factor** as the radius change — never double-count.

---

# PART E — MEMORY TRICKS

```
   ┌──────────────────────────────────────────────┐
   │   POWER LADDER  (the heart of the chapter)    │
   │                                               │
   │     LENGTH   →  1 power   →  ×k                │
   │     AREA     →  2 power   →  ×k²               │
   │     VOLUME   →  3 power   →  ×k³               │
   │                                               │
   │   Dimension ×2  →  L×2 · A×4 · V×8   (1-2-3 → 2-4-8)
   │   Dimension ×3  →  L×3 · A×9 · V×27  (1-2-3 → 3-9-27)
   │   Dimension ×½  →  L×½ · A×¼ · V×⅛              │
   └──────────────────────────────────────────────┘
```

- **"L-A-V = 1-2-3."** Length, Area, Volume carry powers 1, 2, 3. Say it before every question.
- **"Double → 2-4-8, Triple → 3-9-27."** Memorise these two rows cold; most SSC scaling questions are one of them.
- **"Halve → ¼ area, ⅛ volume."** The tank/bucket favourite.
- **"+x% → (1 + x/100), then power."** Never apply % to area/volume directly.
- **"Two things change? Multiply — don't add."** (Except the `a + b + ab/100` % form, which *is* the multiplied factor expanded.)
- **"Constants cancel."** π, ½, ⅓ never affect a ratio.
- **Cylinder/Cone chant:** *"r-squared, h-once."* Volume = r²h-behaviour; CSA = r·(h or l).
- **Sphere chant:** *"radius only — cube for volume, square for skin."*

---

# PART F — TOP COMMON MISTAKES (🟠 avoid to score full marks)

| # | Mistake 🟠 | Correct thinking 🟢 |
| :-- | :-- | :-- |
| 1 | Side +20% ⇒ area +20% | Area +44% ( raise 1.2 to power 2 first ) |
| 2 | Radius ×2 ⇒ sphere volume ×4 | Volume **×8** (cube it) |
| 3 | Adding two % changes for area | Use `a + b + ab/100` |
| 4 | Applying one factor to cuboid TSA when only one edge changes | TSA is a sum — compute term-by-term |
| 5 | Cylinder TSA ×k when only r changes | Only clean if r **and** h scale equally |
| 6 | Scaling diagonal / slant by k² | They're **length** → ×k |
| 7 | Counting diameter and radius as separate changes | Same factor — once |
| 8 | Forgetting the diameter in a semicircle's perimeter | P = πr **+ 2r** |
| 9 | Using slant `l` in cone/pyramid **volume** | Volume uses vertical height **h**; l is for CSA |
| 10 | Treating a *sum* term (a+b, R²+Rr+r²) as a single scalable factor | Only whole-figure uniform scaling gives clean powers |

---
---

# PART G — 🧾 SSC LAST-MINUTE REVISION SHEET (2 pages)

> 🔵 Original · 🟢 New/Result · 🔴 Shortcut · 🟠 Mistake. Read this the night before.

## PAGE 1 — The Law + 2D

```
   THE ONE LAW:  scale every linear dim by k  →  Length ×k · Area ×k² · Volume ×k³
   Percentage:   k = 1 ± x/100 ,  then raise to the power ,  then −1 for the %.
   Two dims:     area % = a + b + (ab)/100  ·  volume factor = multiply each (to its power)
```

| 🔵 2D Formula | 🔴 Uniform side/radius ×k | Key single-dim case |
| :-- | :-- | :-- |
| Square `a²`, `4a`, `a√2` | A ×k², P ×k, d ×k | side ×2 → A ×4 |
| Rectangle `lb`, `2(l+b)` | A ×k², P ×k | L×2,B×½ → A same |
| Triangle `½bh` | A ×k² | base×2,h×3 → A ×6 |
| Equilateral `(√3/4)a²` | A ×k², P ×k | side ×3 → A ×9 |
| Circle `πr²`, `2πr` | A ×k², C ×k | r ×2 → A ×4, C ×2 |
| Semicircle `½πr²`, `(π+2)r` | A ×k², P ×k | 🟠 P = πr **+2r** |
| Sector `(θ/360)πr²` | A ×k_r²·k_θ | arc ×k_r·k_θ |
| Rhombus `½d₁d₂` | A ×k² | both diag ×2 → A ×4 |
| Parallelogram `bh` | A ×k² | b×2,h×½ → A same |
| Trapezium `½(a+b)h` | A ×k² | h ×2 → A ×2 |

**2D quick numbers:** ×2 → area ×4 · ×3 → area ×9 · ×½ → area ×¼ · +20% → area +44% · +50% → area +125%.

## PAGE 2 — 3D Solids

```
   SURFACE (CSA/LSA/TSA) ×k²   ·   VOLUME ×k³   ·   SLANT & DIAGONAL ×k
   Cylinder/Cone volume:  r²·h behaviour  →  radius×a, height×b  ⇒  V ×a²b
```

| 🔵 3D Formula | 🔴 Uniform ×k | Signature exam case 🟢 |
| :-- | :-- | :-- |
| Cube `a³`, `6a²`, `a√3` | V ×k³, SA ×k², d ×k | edge ×2 → V ×8, SA ×4 |
| Cuboid `lbh`, `2(lb+bh+hl)` | V ×k³, SA ×k² | L×2,B×3,H×½ → V ×3 |
| Cylinder `πr²h`, CSA `2πrh` | V ×k³, CSA ×k² | r×2,h×½ → V ×2, CSA same |
| Cone `⅓πr²h`, CSA `πrl` | V ×k³, CSA ×k² | r×2,h×½ → V ×2 |
| Sphere `(4/3)πr³`, `4πr²` | V ×k³, S ×k² | r ×2 → V ×8, S ×4 |
| Hemisphere `(2/3)πr³`, `3πr²` | V ×k³, SA ×k² | r ×2 → V ×8 |
| Frustum `⅓πh(R²+Rr+r²)` | V ×k³, CSA ×k² | whole ×2 → V ×8 |
| Prism `B·h`, LSA `P·h` | V ×k³, SA ×k² | length ×2 → V ×2 |
| Pyramid `⅓Bh`, LSA `½Pl` | V ×k³, SA ×k² | height ×2 → V ×2 |

**3D quick numbers:** dim ×2 → V ×8, SA ×4 · ×3 → V ×27, SA ×9 · ×½ → V ×⅛, SA ×¼ · +50% → V +237.5% · −20% → V −48.8%.

```
   FINAL 10-SECOND CHECK before you tick an answer:
   1. Is the quantity length (¹), area (²), or volume (³)?
   2. Did I raise EACH factor to its own power?
   3. Did I MULTIPLY (not add) the factors?
   4. For %: did I convert to a factor and subtract 1 at the end?
   5. Diameter = radius factor (count once). Constants cancelled.
```

> ✅ **Master this one page and every "if the dimension changes…" question in Geometry & Mensuration is a guaranteed mark.**
