# 📐 Geometry Handbook — Formulas & Figures (SSC CGL)

> Every shape & theorem with a **labelled figure** + its formulas. Companion to
> [SSC-CGL-ASO-Formulas-Tricks-Master.md](SSC-CGL-ASO-Formulas-Tricks-Master.md).
> Syllabus: Quant — Geometry & Mensuration (Para 13.10.3 / 13.11.1.4–13.11.1.5).
> View in a monospace font (or the HTML/PDF) so the figures stay aligned.

**Contents**
1. [Lines & Angles](#1-lines--angles)
2. [Triangle — basics & types](#2-triangle--basics--types)
3. [Triangle — centres](#3-the-four-centres-of-a-triangle)
4. [Triangle — area formulas](#4-triangle-area-formulas)
5. [Pythagoras & triples](#5-pythagoras-theorem--triples)
6. [Similarity & congruence](#6-similarity--congruence)
7. [Quadrilaterals](#7-quadrilaterals)
8. [Polygons](#8-polygons)
9. [Circle — parts & theorems](#9-circle--parts--theorems)
   · [9A Chord theorems](#9a-circle--chord-theorems)
   · [9B Intersecting chords / secants (Power of a Point)](#9b-intersecting-chords-secants--tangentsecant-power-of-a-point-)
   · [9C Tangent theorems](#9c-tangent-theorems)
   · [9D Proportionality & angle theorems](#9d-proportionality--angle-theorems-circle)
10. [Mensuration 2D (areas)](#10-mensuration-2d--areas--perimeters)
11. [Mensuration 3D (solids)](#11-mensuration-3d--solids)
12. [Coordinate geometry](#12-coordinate-geometry)
13. [Quick recall table](#13-quick-recall-table)

---

## 1. Lines & Angles

```
   Types of angles:                 Angle pairs on a transversal:
   • Acute    < 90°                       a\ b
   • Right    = 90°   ┐                     \
   • Obtuse   90–180°                    ────\──────  line 1
   • Straight = 180°  ──                  c   \ d
   • Reflex   180–360°                         \
                                          e\ f  \
                                       ─────\────\───  line 2
                                            g\ h
```

| Concept | Rule |
| :-- | :-- |
| Complementary angles | sum = **90°** |
| Supplementary angles | sum = **180°** |
| Angles on a straight line | sum = **180°** (linear pair) |
| Angles around a point | sum = **360°** |
| Vertically opposite angles | **equal** (a = d, b = c) |
| Parallel lines: corresponding | **equal** |
| Parallel lines: alternate (interior/exterior) | **equal** |
| Parallel lines: co-interior (allied) | sum = **180°** |

---

## 2. Triangle — basics & types

```
            A
            /\                 • Angle sum  ∠A + ∠B + ∠C = 180°
           /  \                • Exterior angle = sum of 2 remote interiors
          /    \                  ∠ACD = ∠A + ∠B
         /      \              • Sum of any two sides > third side
        /________\___ D        • Side opposite the bigger angle is longer
       B          C
```

| By sides | By angles |
| :-- | :-- |
| **Equilateral** — all sides equal (each angle 60°) | **Acute** — all angles < 90° |
| **Isosceles** — two sides equal (base angles equal) | **Right** — one angle = 90° |
| **Scalene** — all sides different | **Obtuse** — one angle > 90° |

---

## 3. The Four Centres of a Triangle

```
   ┌──────────────┬──────────────────────────┬─────────────────────────────┐
   │ Centre       │ Where lines meet          │ Note                        │
   ├──────────────┼──────────────────────────┼─────────────────────────────┤
   │ Centroid  G  │ the 3 MEDIANS             │ divides each median 2:1     │
   │              │ (vertex → midpoint)       │ (from vertex)               │
   │ Incentre  I  │ the 3 ANGLE BISECTORS     │ centre of inscribed circle  │
   │ Circumcentre │ the 3 PERP. BISECTORS     │ centre of circumscribed ○;  │
   │   O          │ of the sides              │ equidistant from vertices   │
   │ Orthocentre  │ the 3 ALTITUDES           │ —                           │
   │   H          │ (vertex ⟂ opposite side)  │                             │
   └──────────────┴──────────────────────────┴─────────────────────────────┘
   • G, O, H are collinear → the EULER LINE; and OG : GH = 1 : 2.
   • In an equilateral triangle all four centres COINCIDE.
```

```
        A                      Median: A → midpoint of BC.
        /|\                    Centroid G lies on all three, 2:1 from vertex.
       / | \                   r (inradius)  = Area / s
      /  G  \                   R (circumradius) = (a·b·c) / (4·Area)
     /  /|\  \                  In a right triangle: R = hypotenuse / 2
    B__/_|_\__C                 and the circumcentre is the midpoint of hypotenuse.
```

---

## 4. Triangle Area Formulas

| Given | Area |
| :-- | :-- |
| base & height | **½ × base × height** |
| 3 sides a,b,c (Heron) | **√[s(s−a)(s−b)(s−c)]**,  s = (a+b+c)/2 |
| two sides & included angle | **½ · a · b · sin C** |
| equilateral side a | **(√3 / 4) · a²** |
| with inradius r | **r × s** |
| with circumradius R | **(a·b·c) / (4R)** |

```
   Equilateral triangle (side a):
        /\         height  h = (√3/2)·a
       /  \        area      = (√3/4)·a²
      / h  \       inradius  r = a / (2√3)
     /______\      circumradius R = a / √3   (R = 2r)
        a
```

---

## 5. Pythagoras Theorem & Triples

```
        |\                   c² = a² + b²
        | \                  (hypotenuse² = sum of squares of legs)
      b |  \ c               Common Pythagorean triples:
        |   \                  3, 4, 5      5, 12, 13
        |____\                 8, 15, 17    7, 24, 25
          a                    9, 40, 41    20, 21, 29
                             (and any multiple: 6-8-10, 9-12-15 …)
```

| Result | Formula |
| :-- | :-- |
| Hypotenuse | √(a² + b²) |
| A leg | √(c² − other leg²) |
| Altitude to hypotenuse | (a·b)/c |
| Right-triangle inradius | r = (a + b − c)/2 |

---

## 6. Similarity & Congruence

```
   SIMILAR (same shape, sizes scaled)        CONGRUENT (identical)
        A              P                      Tests: SSS, SAS, ASA, AAS, RHS
        /\            /\                       (RHS only for right triangles)
       /  \          /  \                     Similar tests: AA, SSS~, SAS~
      /____\        /______\
      ratio of sides equal: AB/PQ = BC/QR = CA/RP = k
```

| In similar triangles (ratio k) | Relationship |
| :-- | :-- |
| Corresponding sides | in ratio **k** |
| Perimeters | in ratio **k** |
| **Areas** | in ratio **k²** |
| (for solids) Volumes | in ratio **k³** |
| Basic Proportionality (Thales) | a line ∥ one side divides the other two **proportionally** |

---

## 7. Quadrilaterals

```
   Square            Rectangle          Parallelogram        Rhombus
   ┌──────┐          ┌────────┐          ____                  /\
   │      │          │        │         /   /                 /  \
   │      │          │        │        /   /                  \  /
   └──────┘          └────────┘       /___/                    \/
```

| Shape | Area | Perimeter / notes |
| :-- | :-- | :-- |
| Square (side a) | a² | 4a; diagonal = a√2 |
| Rectangle (l, b) | l·b | 2(l+b); diagonal = √(l²+b²) |
| Parallelogram | base × height | opposite sides ∥ & equal; diagonals bisect |
| Rhombus (diagonals d₁,d₂) | **½ · d₁ · d₂** | all sides equal; diagonals ⟂ bisect |
| Trapezium (∥ sides a,b; height h) | **½ (a + b) · h** | one pair of sides parallel |
| Kite (diagonals d₁,d₂) | ½ · d₁ · d₂ | diagonals ⟂ |
| Cyclic quad (Brahmagupta) | √[(s−a)(s−b)(s−c)(s−d)] | opposite angles sum 180° |

---

## 8. Polygons

```
   Regular hexagon (n = 6):
        ____            • Sum of interior angles = (n − 2) × 180°
       /    \           • Each interior angle (regular) = (n−2)·180° / n
      /      \          • Each exterior angle (regular)  = 360° / n
      \      /          • Number of diagonals = n(n − 3) / 2
       \____/
```

| n | Name | Interior-angle sum | Each interior (regular) |
| :-: | :-- | :-- | :-- |
| 3 | Triangle | 180° | 60° |
| 4 | Quadrilateral | 360° | 90° |
| 5 | Pentagon | 540° | 108° |
| 6 | Hexagon | 720° | 120° |
| 8 | Octagon | 1080° | 135° |

---

## 9. Circle — parts & theorems

```
                ___________
              /     arc     \
            /        ___      \      • Radius r; Diameter d = 2r
           |       /   \  ●────|──── radius     • Circumference = 2πr = πd
           |      |  C  |chord |      • Area = πr²
           |       \___/      |       • Chord: a line joining two points on ○
            \    tangent      /        • Tangent: touches ○ at one point ⟂ radius
             \ ___|__________/         • Secant: cuts ○ at two points
                  |
               tangent line
```

| Theorem | Statement |
| :-- | :-- |
| Angle at centre | = **2 ×** angle at circumference (same arc) |
| Angles in same segment | **equal** |
| Angle in a semicircle | **90°** (diameter subtends right angle) |
| Cyclic quadrilateral | opposite angles sum **180°** |
| Tangent ⟂ radius | at the point of contact (90°) |
| Two tangents from a point | are **equal** in length |
| Alternate segment | tangent-chord angle = angle in alternate segment |
| Intersecting chords | PA · PB = PC · PD |
| Equal chords | equidistant from the centre |

| Circle measure | Formula |
| :-- | :-- |
| Area | π r² |
| Circumference | 2 π r |
| Arc length (angle θ°) | (θ/360) × 2πr |
| Sector area (angle θ°) | (θ/360) × πr² |
| Segment area | sector area − triangle area |

---

## 9A. Circle — Chord Theorems

```
   PERPENDICULAR FROM CENTRE BISECTS A CHORD
            ●  O (centre)
           /|\
          / | \  r           • OM ⟂ AB  ⇒  AM = MB
         /  |  \              • Distance of chord from centre:
        /   |M  \                 OM = √(r² − (AB/2)²)
     A •────┴────• B          • Conversely, the line from O to the
          chord AB              midpoint of a chord is ⟂ to it.
```

| Chord theorem | Statement |
| :-- | :-- |
| Perpendicular from centre | **bisects** the chord (AM = MB) |
| Line from centre to chord-midpoint | is **perpendicular** to the chord |
| Equal chords | are **equidistant** from the centre (and vice-versa) |
| Longer chord | is **nearer** the centre; the diameter is the longest chord |
| Equal chords subtend | **equal angles** at the centre |

---

## 9B. Intersecting Chords, Secants & Tangent–Secant (Power of a Point) ⭐

```
   (1) CHORDS meet INSIDE        (2) SECANTS meet OUTSIDE      (3) TANGENT + SECANT
        A                              P                             P
         \   D                          \                             \
          \ /                            \● A                          ● T (tangent)
       P ● X                          P ●─\───● B  (secant PAB)     P ●─\──● A ── ● B
          / \                            \  \                            (secant PAB)
         /   \                            \● C
        C     B                            \● D (secant PCD)
   PA·PB = PC·PD                  PA·PB = PC·PD                 PT² = PA·PB
   (two chords AB, CD             (two secants from P)          (tangent² = secant product)
    crossing at X: AX·XB = CX·XD)
```

| Theorem (Power of a Point) | Relation |
| :-- | :-- |
| Two chords intersect **inside** at X | AX · XB = CX · XD |
| Two secants from an **external** point P | PA · PB = PC · PD |
| **Tangent–Secant** from external point P | PT² = PA · PB |
| Two **tangents** from external point P | PT₁ = PT₂ (equal lengths) |

🪄 **One idea:** for any point P and a line through it cutting the circle at two points,
the **product of the two distances is constant** (the "power" of P). Inside → chord·chord;
outside → secant·secant; tangent is the limiting case where the two points merge → PT².

---

## 9C. Tangent Theorems

```
   TANGENT ⟂ RADIUS                 TWO TANGENTS FROM A POINT
          ___                              ___
        /     \                          /     \
       |   ●O  |                         |   ●O  |
        \   |  /                          \ /|\ /
         \  | /                       ─────● P (external)
          \ |/  90°                    PT₁ = PT₂ ; OP bisects ∠T₁PT₂
       ────●──── tangent               ; OT₁ ⟂ PT₁ , OT₂ ⟂ PT₂
           T
```

| Tangent theorem | Statement |
| :-- | :-- |
| Tangent ⟂ radius | at the point of contact (90°) |
| Two tangents from external point | are **equal** (PT₁ = PT₂) |
| Line from centre to external point | **bisects** the angle between the two tangents |
| Tangent length | PT = √(OP² − r²) |
| Alternate Segment Theorem | angle between tangent & chord = angle in the **alternate segment** |

```
   DIRECT & TRANSVERSE COMMON TANGENTS (two circles, centres d apart, radii R, r)
   • Length of DIRECT common tangent     = √(d² − (R − r)²)
   • Length of TRANSVERSE common tangent = √(d² − (R + r)²)
```

**Number of common tangents by position of two circles** (centres `d` apart, radii `R ≥ r`):

| Condition | Position of Circles | Common Tangents |
| :-- | :-- | :--: |
| `d > R + r` | Separate (do not touch) | 4 |
| `d = R + r` | Externally touching | 3 ⭐ |
| `R − r < d < R + r` | Intersecting | 2 |
| `d = R − r` | Internally touching | 1 ⭐ |
| `d < R − r` | One circle inside another | 0 |
| `d = 0, R = r` | Coincident (same circle) | Infinite |

🔑 *Trick:* Tangent count drops as the circles get closer — the two **touching** cases (⭐) are the exam favourites: externally touching → **3**, internally touching → **1**.

---

## 9D. Proportionality & Angle Theorems (Circle)

```
   ANGLE AT CENTRE = 2 × ANGLE AT CIRCUMFERENCE     ANGLE IN SAME SEGMENT
            O                                              C   D
           /|\  ∠AOB = 2·∠ACB                              \   /     ∠ACB = ∠ADB
          / | \                                             \ /      (subtend the
       A ●  |  ● B   (same arc AB)                       A ●──X──● B   same arc AB)
            ● C
```

| Angle / proportion theorem | Statement |
| :-- | :-- |
| Angle at centre | = **2 ×** angle at the circumference on the same arc |
| Angles in the same segment | are **equal** |
| Angle in a semicircle | = **90°** |
| Cyclic quadrilateral | opposite angles are **supplementary** (sum 180°) |
| Exterior angle of cyclic quad | = interior **opposite** angle |
| Ptolemy's theorem (cyclic quad) | AC · BD = AB · CD + AD · BC (product of diagonals) |
| Equal arcs | subtend equal angles at the centre & equal chords |

---

## 10. Mensuration 2D — areas & perimeters

| Shape | Area | Perimeter |
| :-- | :-- | :-- |
| Square (a) | a² | 4a |
| Rectangle (l,b) | l·b | 2(l+b) |
| Triangle (b,h) | ½·b·h | a+b+c |
| Equilateral (a) | (√3/4)a² | 3a |
| Parallelogram | b·h | 2(a+b) |
| Rhombus (d₁,d₂) | ½·d₁·d₂ | 4·side |
| Trapezium (a,b,h) | ½(a+b)h | sum of sides |
| Circle (r) | πr² | 2πr |
| Semicircle (r) | ½πr² | πr + 2r |
| Ring (R,r) | π(R²−r²) | — |

---

## 11. Mensuration 3D — solids

```
   Cube           Cuboid              Cylinder         Cone            Sphere
   ┌──┐          ┌────┐               ___              /\               ___
   │  │╱         │    │╱             |   |            /  \             /   \
   └──┘          └────┘              |   |           /____\           |  ●  |
                                     |___|                             \___/
```

| Solid | Volume | Curved/Lateral SA | Total SA |
| :-- | :-- | :-- | :-- |
| Cube (a) | a³ | 4a² | 6a²; diagonal a√3 |
| Cuboid (l,b,h) | l·b·h | 2h(l+b) | 2(lb+bh+hl); diag √(l²+b²+h²) |
| Cylinder (r,h) | πr²h | 2πrh | 2πr(r+h) |
| Cone (r,h) | ⅓πr²h | πrl | πr(r+l); slant l=√(r²+h²) |
| Sphere (r) | 4/3·πr³ | — | 4πr² |
| Hemisphere (r) | 2/3·πr³ | 2πr² | 3πr² |
| Frustum (R,r,h) | ⅓πh(R²+r²+Rr) | π(R+r)l | + π(R²+r²) |

```
   Cone slant height:          Sphere:                Hemisphere:
       /|                       4               2          ___
      / | h        l² = r²+h²   V = ─ πr³       V = ─ πr³  /   \
   l /  |                       3               3         |_____|
    /___|                       SA = 4πr²       TSA = 3πr² (flat + curved)
      r
```

---

## 12. Coordinate Geometry

```
        y
        |        • P(x₁,y₁) , Q(x₂,y₂)
     Q •|                  __________________
        |  •P    Distance = √[(x₂−x₁)² + (y₂−y₁)²]
   ─────┼───── x  Midpoint = ((x₁+x₂)/2 , (y₁+y₂)/2)
        |        Slope m   = (y₂−y₁)/(x₂−x₁)
        |        Section (m:n) = ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n))
```

| Concept | Formula |
| :-- | :-- |
| Distance | √[(x₂−x₁)² + (y₂−y₁)²] |
| Midpoint | ((x₁+x₂)/2, (y₁+y₂)/2) |
| Slope m | (y₂−y₁)/(x₂−x₁) |
| Line (slope-intercept) | y = mx + c |
| Parallel lines | equal slopes (m₁ = m₂) |
| Perpendicular lines | m₁ · m₂ = −1 |
| Area of triangle (vertices) | ½ \|x₁(y₂−y₃)+x₂(y₃−y₁)+x₃(y₁−y₂)\| |

---

## 13. Quick recall table

| Prompt | Answer |
| :-- | :-- |
| Triangle angle sum | 180° |
| Equilateral area | (√3/4)·a² |
| Heron's area | √[s(s−a)(s−b)(s−c)] |
| Centroid divides median | 2 : 1 |
| Circumradius R | abc/(4·Area) |
| Inradius r | Area/s |
| Angle in semicircle | 90° |
| Angle at centre vs circumference | 2 : 1 |
| Rhombus area | ½·d₁·d₂ |
| Trapezium area | ½(a+b)·h |
| Interior-angle sum (n-gon) | (n−2)·180° |
| Diagonals of n-gon | n(n−3)/2 |
| Cube diagonal | a√3 |
| Cuboid diagonal | √(l²+b²+h²) |
| Cone slant l | √(r²+h²) |
| Sphere volume / SA | 4/3·πr³ / 4πr² |
| Hemisphere TSA | 3πr² |
| Areas of similar figures | ratio of sides² |
| Perpendicular slopes | m₁·m₂ = −1 |

---

> ✅ **Strategy:** learn the **figure first**, then attach its formulas — recall is far
> stronger when you can *picture* the shape. Redraw 2–3 figures from memory daily.
> Back to the [main formula sheet »](SSC-CGL-ASO-Formulas-Tricks-Master.md).
