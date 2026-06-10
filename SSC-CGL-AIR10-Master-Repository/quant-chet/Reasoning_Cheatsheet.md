# SSC CGL — Logical Reasoning Cheat Sheet

> **Source:** Table-of-contents pages (`quant-chet/`). The images list the Logical Reasoning syllabus; this sheet expands each listed chapter into its tricks and shortcut techniques.
>
> **Chapters covered:** Cubes & Cuboids · Days Sequence · Blood Relation · Coding–Decoding · Clocks & Calendars · Puzzles · Directions · Series.

---

## Cubes & Cuboids

A cube of side n painted on all faces, cut into n³ small cubes:

| Painted faces | Count | Location |
|---|---|---|
| 3 faces | `8` | corners (always 8) |
| 2 faces | `12(n−2)` | edges |
| 1 face | `6(n−2)²` | face centres |
| 0 faces | `(n−2)³` | inner core |

- Total small cubes = `n³`. Check: 8 + 12(n−2) + 6(n−2)² + (n−2)³ = n³.
- If only some faces painted, redo per exposed face.

---

## Days / Days Sequence

- **Odd days method:** map remainder of total days ÷ 7.
- Ordinary year = 365 days → **1 odd day**; Leap year = **2 odd days**.
- Leap year: divisible by 4 (century years must be ÷ 400).
- Day after `d` days = (today + d) mod 7.

---

## Blood Relation

- Solve from the **speaker outward**; draw a family tree.
- Symbols: `+` male, `−` female, `→` "is parent of".
- "My father's only son" = the speaker himself.
- For coded relations (A × B, A + B), decode operator-by-operator.
- Generations: grandparent → parent → self → child → grandchild.

---

## Coding–Decoding

- **Letter values:** A=1 … Z=26; reverse A=26 … Z=1 (EJOTY: E=5,J=10,O=15,T=20,Y=25).
- Letter-shift coding: find constant +/− shift between positions.
- Opposite-pair (mirror): A↔Z, B↔Y… sum of positions = 27.
- Number coding: check sum of letter values, or position pattern.
- Symbol/condition coding: apply rules in stated priority order.

---

## Clocks & Calendars

**Clocks**
- Minute hand = 6°/min ; Hour hand = 0.5°/min ; gain of minute over hour = 5.5°/min.
- Angle between hands = `|30H − 5.5M|` degrees.
- Hands coincide every `65 + 5/11` min → 22 times/day.
- Hands at right angle 44 times/day; opposite 22 times/day.

**Calendars**
- Same calendar repeats: after 28 yrs (general), or 6/11 yr gaps depending on leaps.
- Use odd-days table to find day of any date.

---

## Puzzles (seating / scheduling)

- Build a **grid/table**; lock in definite clues first, then conditional ones.
- Circular seating: facing centre → left/right reversed vs facing out.
- Eliminate possibilities; track "not" clues separately.
- For linear arrangements note both possible directions until fixed.

---

## Directions

- Mental compass: N-top, E-right, S-bottom, W-left.
- Right turn = clockwise 90°; Left turn = anticlockwise 90°.
- **Shortest distance** = Pythagoras on net E–W and N–S displacement: `√(x²+y²)`.
- Shadows: sunrise (E) → shadow West; sunset (W) → shadow East; noon → no shadow.

---

## Series

**Number series — check in order:**
1. Constant difference (AP) → `+d`
2. Constant ratio (GP) → `×r`
3. Difference of differences (2nd-order)
4. Squares / cubes (±k)
5. Prime numbers, alternating series, two interleaved series

**Letter series:** convert to position numbers (A=1…Z=26), find the numeric pattern, convert back.

**Alphanumeric:** treat letters and numbers as separate series running together.

---

### Universal reasoning tips
1. **Diagram everything** — tree (blood relation), grid (puzzles), compass (directions).
2. Read **negative clues** ("not adjacent", "neither") — they eliminate fast.
3. For series, always test difference **and** ratio before exotic patterns.
4. Memorize **A=1…Z=26** and the **mirror pairs (sum 27)** cold — saves time in coding.
5. In cubes, the **8-corner / 12-edge** facts are fixed regardless of n.
