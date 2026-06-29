# 📐 SSC CGL — Formulas, Identities & Tricks (ASO Target Post)

> Companion to the [Official Syllabus](../SSC-CGL-2026-Official-Syllabus.md). Scope for **Assistant
> Section Officer (ASO)** = **Tier-I + Tier-II Paper-I only**. Paper-II (Statistics) and Paper-III
> (Finance & Economics) are **out of scope** for ASO. Every section maps to the official syllabus para.
>
> **Each table has a “🪄 Trick / Shortcut” column.** Diagrams use fixed-width boxes — view in a
> monospace font (or the generated PDF) for correct alignment.

**Legend:** `S`=Speed `D`=Distance `T`=Time `P`=Principal `R`=Rate `CP`=Cost Price `SP`=Selling Price · ⭐ = very high-yield.

---

# PART 1 — QUANTITATIVE APTITUDE  *(Para 13.10.3 / 13.11.1)*

## 1.1 Number System & Divisibility  ⭐

| Concept | Formula | 🪄 Trick / Shortcut |
| :-- | :-- | :-- |
| Sum 1→n | n(n+1)/2 | last × next ÷ 2 |
| Sum of squares 1→n | n(n+1)(2n+1)/6 | — |
| Sum of cubes 1→n | [n(n+1)/2]² | = (sum)² |
| Sum of first n odd | n² | "1,4,9,16…" |
| Sum of first n even | n(n+1) | — |
| No. of factors of N=aᵖ·bᵠ | (p+1)(q+1) | add 1 to each power, multiply |
| Sum of factors | (aᵖ⁺¹−1)/(a−1) × … | — |
| HCF × LCM | = product of the two numbers | find one, divide to get other |
| Divisible by 3 / 9 | digit-sum ÷ 3 / 9 | add digits |
| Divisible by 11 | (odd-pos sum − even-pos sum) ÷ 11 | alternating ± |
| Divisible by 8 | last 3 digits ÷ 8 | — |
| Unit digit of aⁿ | cycle of 4 (e.g. 2,4,8,6) | take n mod 4 |

```
 Divisibility by 11 :  7  9  2  4   →   (7+2) − (9+4) = 9 − 13 = −4  ✗ not ÷11
                       ↑  ↓  ↑  ↓        (odd places)  (even places)
```

## 1.2 Percentage  ⭐

| Concept | Formula | 🪄 Trick / Shortcut |
| :-- | :-- | :-- |
| x% of y | (x/100)·y | x% of y = y% of x |
| % change | (new−old)/old × 100 | — |
| Successive a%, b% | a + b + ab/100 | both +ve add term; one −ve → subtract |
| If A is x% more than B | B is x/(100+x)×100 % less than A | — |
| If A is x% less than B | B is x/(100−x)×100 % more than A | — |
| Value ↑ x% then ↓ x% | net **decrease** = x²/100 % | always a loss |
| Fraction ⇄ % | 1/8=12.5%, 1/6=16.67%, 1/3=33.33% | memorise 1/n table |

🪄 **Successive sign rule:** `a + b + (ab/100)` — plug b as negative for a decrease.
Example: 20% up then 20% down → 20 − 20 − 400/100 = **−4%** (net 4% loss).

## 1.3 Ratio, Proportion & Partnership  *(13.11.1.2)*

| Concept | Formula | 🪄 Trick / Shortcut |
| :-- | :-- | :-- |
| Proportion a:b=c:d | a·d = b·c | product of means = extremes |
| Mean proportional of a,b | √(ab) | — |
| Third proportional of a,b | b²/a | — |
| Partnership profit share | ∝ (capital × time) | "months-money" product |
| Componendo-Dividendo | (a+b)/(a−b) = (c+d)/(c−d) | speeds up ratio sums |

## 1.4 Average, Mixture & Alligation  ⭐ *(13.11.1.2)*

| Concept | Formula | 🪄 Trick / Shortcut |
| :-- | :-- | :-- |
| Average | sum ÷ count | — |
| New avg on adding 1 item | shifts by (item−avg)/(n+1) | — |
| Avg speed (equal distance) | 2·S₁·S₂/(S₁+S₂) | **harmonic mean** |
| Alligation ratio | (Cheaper⇄Mean) : (Dear⇄Mean) | cross-difference |
| Replacement: remaining | Original·(1 − x/V)ⁿ | x removed each of n times, vol V |

```
   ALLIGATION (cross method):
        Cheaper(C)            Dearer(D)
             \                 /
              \               /
               Mean price (M)
              /               \
   (D − M)  ────────         ──────── (M − C)
   Ratio  Cheaper : Dearer  =  (D−M) : (M−C)
```

## 1.5 Profit, Loss & Discount  ⭐ *(13.11.1.2)*

| Concept | Formula | 🪄 Trick / Shortcut |
| :-- | :-- | :-- |
| Profit % | (SP−CP)/CP × 100 | always on **CP** |
| SP from CP & profit% | CP·(100+P)/100 | — |
| Discount % | (MP−SP)/MP × 100 | always on **MP** (marked price) |
| MP, discount d%, profit p% | CP·(100+p) = MP·(100−d) | links MP↔CP |
| Two successive discounts | d₁+d₂ − d₁d₂/100 | same as % successive rule |
| Dishonest dealer gain% | error/(true−error) × 100 | uses false weight |
| Profit% if SP fixed, CP±x% | use multiplying factors | — |

## 1.6 Simple & Compound Interest  ⭐ *(13.11.1.2)*

| Concept | Formula | 🪄 Trick / Shortcut |
| :-- | :-- | :-- |
| Simple Interest | P·R·T/100 | linear in time |
| Amount (CI) | P(1 + R/100)ᵀ | — |
| CI − SI (2 years) | P(R/100)² | quick! |
| CI − SI (3 years) | P(R/100)²·(3 + R/100) | — |
| Doubles in (SI) | T = 100/R years | — |
| Doubles in (CI) | Rule of 72 → 72/R years | approx |
| Half-yearly CI | rate R/2, time 2T | n compoundings |

```
  SI vs CI growth (same P,R):
  Amount
    |                         •  CI  (curves up — interest on interest)
    |                  •  •
    |           •  •          ____ SI (straight line)
    |      • •      _____
    |   ••   ______
    |•___________________________  time
  CI − SI gap widens each year;  for 2 yrs it is exactly  P(R/100)².
```

## 1.7 Time, Speed, Distance · Trains · Boats  ⭐ *(13.10.3)*

| Concept | Formula | 🪄 Trick / Shortcut |
| :-- | :-- | :-- |
| Basic | D = S × T | cover triangle below |
| km/h → m/s | × 5/18 | m/s → km/h: × 18/5 |
| Train crossing pole | length ÷ speed | pole = point object |
| Train crossing platform | (L_train+L_plat) ÷ speed | add both lengths |
| Two trains opposite | relative S = S₁+S₂ | sum |
| Two trains same dir | relative S = S₁−S₂ | difference |
| Boat downstream | (b + s) | b=boat, s=stream |
| Boat upstream | (b − s) | — |
| Boat speed / stream speed | (down+up)/2 / (down−up)/2 | half sum / half diff |

```
        D            (cover the unknown to read its formula)
      ┌───┐          cover D → S×T
      │ D │          cover S → D/T
      ├─┬─┤          cover T → D/S
      │S│T│
      └─┴─┘
```

## 1.8 Time & Work · Pipes  ⭐ *(13.11.1.2)*

| Concept | Formula | 🪄 Trick / Shortcut |
| :-- | :-- | :-- |
| Work rate | 1/days | A does 1/a per day |
| A+B together | 1/a + 1/b = (a+b)/ab | "product ÷ sum" days |
| **LCM method** | Total work = LCM(days); rate = LCM/day | avoids fractions ⭐ |
| Efficiency ∝ | 1/time | more efficient = fewer days |
| M₁D₁H₁/W₁ = M₂D₂H₂/W₂ | chain rule | men-days-hours-work |
| Pipe fill − empty | 1/fill − 1/empty | leak subtracts |

🪄 **LCM trick:** A=10d, B=15d → Total = LCM 30 units. A=3/day, B=2/day → together 5/day → **6 days**.

## 1.9 Algebra Identities  ⭐ *(13.11.1.3)*

| Identity | Expansion |
| :-- | :-- |
| (a+b)² | a² + 2ab + b² |
| (a−b)² | a² − 2ab + b² |
| a² − b² | (a+b)(a−b) |
| (a+b)³ | a³ + b³ + 3ab(a+b) |
| (a−b)³ | a³ − b³ − 3ab(a−b) |
| a³ + b³ | (a+b)(a²−ab+b²) |
| a³ − b³ | (a−b)(a²+ab+b²) |
| a³+b³+c³−3abc | (a+b+c)(a²+b²+c²−ab−bc−ca) |
| If a+b+c=0 | then a³+b³+c³ = 3abc ⭐ |

| Conditional (very high-yield) | Result |
| :-- | :-- |
| x + 1/x = k | x² + 1/x² = k² − 2 |
| x + 1/x = k | x³ + 1/x³ = k³ − 3k |
| x − 1/x = k | x² + 1/x² = k² + 2 |

## 1.10 Geometry — Triangles & Circles  ⭐ *(13.11.1.4)*

| Concept | Formula / Fact | 🪄 Trick |
| :-- | :-- | :-- |
| Pythagoras | a² + b² = c² | triples: 3-4-5, 5-12-13, 8-15-17, 7-24-25 |
| Triangle area | ½ · base · height | — |
| Area (Heron) | √[s(s−a)(s−b)(s−c)], s=perimeter/2 | when 3 sides known |
| Equilateral area | (√3/4)·a² | height = (√3/2)a |
| Centroid divides median | 2 : 1 | from vertex |
| Angle sum | 180° (triangle), 360° (quad) | — |
| Exterior angle | = sum of 2 opposite interiors | — |
| Inradius r | Area / s | — |
| Circumradius R | (a·b·c) / (4·Area) | — |
| Angle in semicircle | 90° | diameter subtends right angle |
| Angle at centre | = 2 × angle at circumference | same arc |
| Tangent ⟂ radius | 90° at point of contact | — |

```
   FOUR CENTRES OF A TRIANGLE (don't mix up!)
   ┌──────────────┬───────────────────────┬───────────────┐
   │ Centroid (G) │ medians meet           │ ratio 2:1     │
   │ Incentre (I) │ angle bisectors meet   │ centre of in-○ │
   │ Circumcentre │ perpendicular bisectors│ centre of out-○│
   │ Orthocentre  │ altitudes meet         │ —             │
   └──────────────┴───────────────────────┴───────────────┘
   Line through G, Circumcentre & Orthocentre = "Euler Line".
```

## 1.11 Mensuration 2D / 3D  ⭐ *(13.11.1.5)*

| Shape | Area / Volume | Surface / Perimeter |
| :-- | :-- | :-- |
| Rectangle | l·b | perimeter 2(l+b), diagonal √(l²+b²) |
| Square | a² | perimeter 4a, diagonal a√2 |
| Circle | πr² | circumference 2πr |
| Triangle | ½·b·h | — |
| Trapezium | ½(a+b)·h | a,b parallel sides |
| Cube | V = a³ | TSA 6a², diagonal a√3 |
| Cuboid | V = l·b·h | TSA 2(lb+bh+hl), diag √(l²+b²+h²) |
| Cylinder | V = πr²h | CSA 2πrh, TSA 2πr(r+h) |
| Cone | V = ⅓πr²h | CSA πrl, slant l=√(r²+h²) |
| Sphere | V = 4/3·πr³ | SA 4πr² |
| Hemisphere | V = 2/3·πr³ | CSA 2πr², TSA 3πr² |

```
   CONE relationship:   slant height  l² = r² + h²
            /|              l (slant)
           / |  h           ┌───────────┐
          /  |              │ l = √(r²+h²)│
         /___|              └───────────┘
           r
```

## 1.12 Trigonometry  ⭐ *(13.11.1.6)*

| Identity | Value |
| :-- | :-- |
| sin²θ + cos²θ | 1 |
| 1 + tan²θ | sec²θ |
| 1 + cot²θ | cosec²θ |
| sin(90−θ) | cosθ (co-functions) |
| tanθ | sinθ/cosθ |

```
   STANDARD ANGLES TABLE (memorise the sin row, rest follows)
   θ        0°     30°     45°     60°     90°
   sinθ    √0/2   √1/2    √2/2    √3/2    √4/2
        =   0     1/2    1/√2    √3/2     1
   cosθ  = reverse the sin row (1 → 0)
   tanθ  = sinθ / cosθ  →  0, 1/√3, 1, √3, ∞

   🪄 Trick: write 0,1,2,3,4 under the angles → take √ → divide by 2 = sinθ.
```

| Heights & Distances | Quick fact |
| :-- | :-- |
| Angle of elevation 45° | height = distance (tan45=1) |
| 30° | height = distance/√3 |
| 60° | height = distance·√3 |

---

# PART 2 — REASONING & GENERAL INTELLIGENCE  *(Para 13.10.1 / 13.11.2)*

## 2.1 Coding–Decoding

| Type | Method | 🪄 Trick |
| :-- | :-- | :-- |
| Letter↔Number | A=1 … Z=26 | "EJOTY": E=5,J=10,O=15,T=20,Y=25 |
| Reverse position | A=26 … Z=1 | sum with normal = 27 |
| Shift cipher | +n or −n on each letter | watch wrap-around Z→A |
| Opposite letter | letter + its pair sums to 27 | A↔Z, B↔Y (mirror) |

```
   EJOTY anchor (count from nearest):  A B C D E ... J ... O ... T ... Y Z
                                        1 2 3 4 5     10    15    20   25 26
```

## 2.2 Number / Letter Series

| Pattern | Clue |
| :-- | :-- |
| Constant difference | arithmetic (e.g. +5) |
| Multiply/divide | geometric (×2, ÷3) |
| Squares / cubes | 1,4,9,16 or 1,8,27,64 |
| Prime sequence | 2,3,5,7,11,13 |
| Alternating | two interleaved series |
| ±increasing diff | +2,+4,+6 … (2nd difference constant) |

## 2.3 Blood Relations

```
        Grandfather ── Grandmother
                 │
        ┌────────┴────────┐
      Father ── Mother   Uncle/Aunt
        │
   ┌────┴────┐
  Self      Sibling
```
| 🪄 Trick | How |
| :-- | :-- |
| Use symbols | + male, − female, → married, ⊥ child |
| Maternal vs Paternal | maternal = mother's side |
| **Self-reference phrases** | collapse "the X of Y" to one known person — see below |

### 🔑 Cracking "only son/daughter of his/her ___" (self-reference trick)

The exam hides the answer behind a chain like *"the only daughter of his mother."*
**Rule:** replace the phrase from the **inside out**, and use the **pronoun** (his/her) to lock who is speaking.

```
  GOLDEN SUBSTITUTIONS (memorise these collapses)
  ┌────────────────────────────────────────────────┬─────────────────────────┐
  │ Phrase (pointing to a picture/person)           │ Collapses to            │
  ├────────────────────────────────────────────────┼─────────────────────────┤
  │ "only son of HIS mother"                        │ = the man HIMSELF        │
  │ "only daughter of HIS mother"                   │ = his SISTER             │
  │ "only daughter of HER mother"                   │ = the woman HERSELF      │
  │ "only son of HER father"                        │ = her BROTHER            │
  │ "his father's only son"                         │ = he HIMSELF (no brother)│
  │ "my mother's only son's wife"                   │ = MY wife (I am that son)│
  └────────────────────────────────────────────────┴─────────────────────────┘
  Why: "only" means no siblings of that type → the description can point to just ONE person.
```

**Example 1 — classic photo puzzle**
> *Pointing to a photograph, a man said, "She is the **only daughter of my mother**." Who is in the photo?*
- "only daughter of my mother" + pronoun **my** (the man speaks) → his mother's only daughter = **his sister**.
✅ **Answer: his SISTER.**

**Example 2 — the two-step chain**
> *A woman said, "He is the **only son of the mother of my brother**." How is he related to her?*
- "mother of my brother" = **my mother** (same mother).
- "only son of my mother" = **my brother** (if speaker is female) — but he's already called her brother → confirms it.
✅ **Answer: her BROTHER.**

**Example 3 — wife hidden inside**
> *Pointing to a lady, Raman said, "Her mother is the **only daughter of my mother**." How is the lady related to Raman?*
- "only daughter of my mother" = Raman's **sister**.
- So the lady's mother is Raman's sister → the lady is the **daughter of Raman's sister** = his **niece**.
✅ **Answer: his NIECE.**

**Example 4 — "father's only son" = himself**
> *"That boy is the son of my **father's only son**." (spoken by a man) How is the boy related to him?*
- "my father's only son" = the speaker **himself**.
- son of himself = **his son**.
✅ **Answer: his SON.**

```
  STEP METHOD (use on every self-reference question)
  1) Find the innermost phrase ("X of my/his/her Y").
  2) Apply a GOLDEN substitution → replace with ONE person.
  3) Re-read the sentence with that person plugged in.
  4) Repeat outward until only "speaker → target" remains.
  5) Decide gender from his/her/she/he, then name the relation.
```

🪄 **Quickest tells:** *"only daughter of HIS mother"* is almost always **sister**;
*"only son of HER father"* is almost always **brother**; whenever the **pronoun matches the gender
of the person described** (his…son, her…daughter), it usually collapses to the **speaker himself/herself**.

## 2.4 Clocks & Calendars  ⭐

> 📖 **Full topic with derivations, 12 worked examples, diagrams & a practice set:**
> [Clocks & Calendars — Deep Dive »](Clocks-and-Calendars-Deep-Dive.md)

| Concept | Formula | 🪄 Trick |
| :-- | :-- | :-- |
| Angle between hands | \|30H − 5.5M\| degrees | H=hour, M=minutes |
| Hands overlap | every 65·5/11 min (~65.45) | 11 times in 12 h |
| Minute hand gains | 5.5° per minute | — |
| Odd days in 100 yrs | 5 | 200→3, 300→1, 400→0 |
| Leap year | ÷4 (century ÷400) | 2000 leap, 1900 not |
| Day code (week) | count odd days from a known date | — |

```
   CLOCK ANGLE :  θ = |30·H − 5.5·M|
   e.g. 3:40  →  |30·3 − 5.5·40| = |90 − 220| = 130°
   (if >180°, subtract from 360° for the smaller angle)
```

## 2.5 Direction Sense & Dice

```
   DIRECTIONS                      DICE (standard):
        N                          opposite faces sum to 7
        │                          1↔6, 2↔5, 3↔4
   W────┼────E                     If two dice show same 4 faces,
        │                          the two odd faces are opposite.
        S
   Right turn = clockwise (N→E→S→W). Shadow at morning falls West, evening East.
```

| Topic | 🪄 Trick |
| :-- | :-- |
| Net displacement | use Pythagoras on net N-S & E-W legs |
| Syllogism | draw Venn circles; "possibility" cases for "some/all" |
| Venn diagram | smallest region logic; least/most overlap |

---

# PART 3 — COMPUTER KNOWLEDGE / PROFICIENCY (Paper-I, Section-III)  ✅ ASO *(Para 13.11.5)*

> In scope for ASO (it sits inside the compulsory Paper-I). Mostly factual — these tables are the high-yield recall points.

## 3.1 Computer Basics & Memory

| Concept | Key fact | 🪄 Trick |
| :-- | :-- | :-- |
| CPU parts | ALU + Control Unit + Registers | "brain" of computer |
| ALU | does arithmetic & logic | A = Arithmetic, L = Logic |
| Memory units (small→big) | bit < Byte < KB < MB < GB < TB | 1 Byte = 8 bits; ×1024 each step |
| RAM | volatile, temporary, fast | lost on power-off |
| ROM | non-volatile, permanent | BIOS lives here |
| Cache | fastest memory, near CPU | speeds up repeat access |
| Primary vs Secondary | RAM/ROM vs HDD/SSD/pen-drive | secondary = storage |
| Input devices | keyboard, mouse, scanner, mic | data IN |
| Output devices | monitor, printer, speaker | data OUT |

```
   DATA-SIZE LADDER (each ×1024)
   bit → Byte → KB → MB → GB → TB → PB
    1     8b   1024B ...
   🪄 "Big Kids May Get Trophies" → Byte, KB, MB, GB, TB.
```

## 3.2 Software, MS Office & Shortcuts

| Item | Fact | 🪄 Trick |
| :-- | :-- | :-- |
| System software | OS (Windows, Linux) | runs the machine |
| Application software | MS Word, Excel, browser | user tasks |
| MS Word file ext | .docx | word DOC |
| MS Excel file ext | .xlsx | X = eXcel |
| PowerPoint ext | .pptx | PPT |
| Excel: cell ref | column-letter + row-number (e.g. B5) | — |
| Excel: formula starts with | = sign | =SUM(A1:A5) |

| Shortcut | Action | Shortcut | Action |
| :-- | :-- | :-- | :-- |
| Ctrl+C / X / V | Copy / Cut / Paste | Ctrl+Z / Y | Undo / Redo |
| Ctrl+A | Select all | Ctrl+S | Save |
| Ctrl+B / I / U | Bold / Italic / Underline | Ctrl+F | Find |
| Ctrl+P | Print | Ctrl+Home | Go to start |
| F5 | Refresh / Slideshow (PPT) | Alt+F4 | Close window |

## 3.3 Internet, E-mail & Cyber Security

| Term | Meaning | 🪄 Trick |
| :-- | :-- | :-- |
| HTTP / HTTPS | web protocol / **S = Secure** | padlock = HTTPS |
| URL | web address | http://… |
| ISP | Internet Service Provider | gives you internet |
| CC / BCC (e-mail) | Carbon Copy / **Blind** CC | BCC = hidden recipients |
| Virus / Worm / Trojan | malware types | Trojan = disguised as safe |
| Phishing | fake mail steals data | "fishing" for passwords |
| Firewall | blocks unauthorised access | network gatekeeper |
| Cookie | small file storing browse data | — |

---

## ⚡ 60-Second Recall (cover the right column) — ASO scope

| Prompt | Answer |
| :-- | :-- |
| km/h → m/s | × 5/18 |
| Avg speed (equal distance) | 2S₁S₂/(S₁+S₂) |
| CI − SI for 2 years | P(R/100)² |
| a+b+c=0 ⇒ a³+b³+c³ | 3abc |
| x+1/x=k ⇒ x³+1/x³ | k³−3k |
| Successive % a, b | a+b+ab/100 |
| Clock angle | \|30H − 5.5M\| |
| Sphere volume | 4/3·πr³ |
| Cone slant l | √(r²+h²) |
| sin²θ+cos²θ | 1 |
| "only daughter of HIS mother" | his sister |
| Memory ladder | bit < Byte < KB < MB < GB < TB |
| HTTPS | secure web protocol |
| Save / Find shortcut | Ctrl+S / Ctrl+F |

---

> ✅ **Study flow for ASO:** the whole exam is **Tier-I + Tier-II Paper-I** — so master
> **Part 1 (Quant)**, **Part 2 (Reasoning)**, and **Part 3 (Computer)** here, plus English &
> General Awareness. **Finance/Economics (Paper-III) and Statistics (Paper-II) are NOT in your
> syllabus.** Redraw the diagrams from memory — the boxed relationships are built to "snap" back in the exam.
