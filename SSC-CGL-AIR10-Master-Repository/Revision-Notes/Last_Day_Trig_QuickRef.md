# Last-Day Quick Reference — Trigonometry & High-Yield Tricks

> Back to: [Last 1 Day Revision](Last_1_Day_Revision.md) · [README](README.md)
> See also: [Trigonometry Question Bank](../Quantitative-Aptitude/12_Trigonometry.md) · [Quant Formula Sheet](../Formula-Sheets/Quant_Formula_Sheet.md)

**Visual, glance-and-go sheet.** Tables for recall, diagrams that render as images on GitHub and in the IDE. No solving today — just look, recognise, move on.

---

## 1. Degree ↔ Radian Equivalents

| Degrees | 0° | 30° | 45° | 60° | 90° | 120° | 135° | 150° | 180° | 270° | 360° |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Radians** | 0 | π/6 | π/4 | π/3 | π/2 | 2π/3 | 3π/4 | 5π/6 | π | 3π/2 | 2π |

> **Convert:** degrees → radians: `× π/180`  ·  radians → degrees: `× 180/π`.

---

## 2. Standard-Angle Table (memorise cold)

| θ | 0° | 30° | 45° | 60° | 90° |
|---|---|---|---|---|---|
| **sin θ** | 0 | ½ | 1/√2 | √3/2 | 1 |
| **cos θ** | 1 | √3/2 | 1/√2 | ½ | 0 |
| **tan θ** | 0 | 1/√3 | 1 | √3 | ∞ |
| **cosec θ** | ∞ | 2 | √2 | 2/√3 | 1 |
| **sec θ** | 1 | 2/√3 | √2 | 2 | ∞ |
| **cot θ** | ∞ | √3 | 1 | 1/√3 | 0 |

🔑 **Finger / "0-1-2-3-4" trick:** for sin, write `0,1,2,3,4` → divide each by 4 → take √ → `0, ½, 1/√2, √3/2, 1`. Reverse the row for cos.

<!-- Standard-ratio visual -->
<svg xmlns="http://www.w3.org/2000/svg" width="520" height="190" viewBox="0 0 520 190" font-family="Segoe UI, Arial, sans-serif">
  <rect x="0" y="0" width="520" height="190" fill="#ffffff" stroke="#cfd8dc"/>
  <text x="260" y="26" font-size="16" font-weight="bold" text-anchor="middle" fill="#0d47a1">sin — divide 0,1,2,3,4 by 4, then √</text>
  <g font-size="14" text-anchor="middle">
    <rect x="20"  y="50" width="92" height="40" fill="#e3f2fd" stroke="#90caf9"/>
    <rect x="116" y="50" width="92" height="40" fill="#e3f2fd" stroke="#90caf9"/>
    <rect x="212" y="50" width="92" height="40" fill="#e3f2fd" stroke="#90caf9"/>
    <rect x="308" y="50" width="92" height="40" fill="#e3f2fd" stroke="#90caf9"/>
    <rect x="404" y="50" width="92" height="40" fill="#e3f2fd" stroke="#90caf9"/>
    <text x="66"  y="68" fill="#37474f">0°</text><text x="66"  y="84" font-weight="bold">0</text>
    <text x="162" y="68" fill="#37474f">30°</text><text x="162" y="84" font-weight="bold">½</text>
    <text x="258" y="68" fill="#37474f">45°</text><text x="258" y="84" font-weight="bold">1/√2</text>
    <text x="354" y="68" fill="#37474f">60°</text><text x="354" y="84" font-weight="bold">√3/2</text>
    <text x="450" y="68" fill="#37474f">90°</text><text x="450" y="84" font-weight="bold">1</text>
  </g>
  <text x="260" y="120" font-size="14" text-anchor="middle" fill="#37474f">cos = same row reversed  ·  tan = sin ÷ cos</text>
  <text x="260" y="150" font-size="13" text-anchor="middle" fill="#b71c1c">cosec = 1/sin   sec = 1/cos   cot = 1/tan</text>
  <text x="260" y="172" font-size="12" text-anchor="middle" fill="#607d8b">90° column: tan, sec, cosec→∞ ; cot, cos, sin handled above</text>
</svg>

---

## 3. Core Identities

- `sin²θ + cos²θ = 1`
- `1 + tan²θ = sec²θ`  →  `sec²θ − tan²θ = 1`
- `1 + cot²θ = cosec²θ`  →  `cosec²θ − cot²θ = 1`
- `tanθ = sinθ/cosθ`, `cotθ = cosθ/sinθ`
- Reciprocals: `sinθ·cosecθ = cosθ·secθ = tanθ·cotθ = 1`
- Complementary: `sin(90°−θ)=cosθ`, `tan(90°−θ)=cotθ`, `sec(90°−θ)=cosecθ`

🔑 The three Pythagorean identities each rearrange to **= 1** — spot them and skip all working.

---

## 4. Unit Circle & Sign of Ratios (ASTC)

<!-- Unit circle with quadrant signs -->
<svg xmlns="http://www.w3.org/2000/svg" width="360" height="360" viewBox="0 0 360 360" font-family="Segoe UI, Arial, sans-serif">
  <rect x="0" y="0" width="360" height="360" fill="#ffffff" stroke="#cfd8dc"/>
  <!-- axes -->
  <line x1="180" y1="20" x2="180" y2="340" stroke="#90a4ae" stroke-width="1.5"/>
  <line x1="20" y1="180" x2="340" y2="180" stroke="#90a4ae" stroke-width="1.5"/>
  <!-- circle -->
  <circle cx="180" cy="180" r="130" fill="none" stroke="#1565c0" stroke-width="2"/>
  <!-- 45-degree radius -->
  <line x1="180" y1="180" x2="272" y2="88" stroke="#e53935" stroke-width="2"/>
  <circle cx="272" cy="88" r="4" fill="#e53935"/>
  <text x="278" y="84" font-size="12" fill="#e53935">(cosθ, sinθ)</text>
  <!-- quadrant ASTC labels -->
  <text x="250" y="120" font-size="18" font-weight="bold" fill="#2e7d32" text-anchor="middle">A</text>
  <text x="250" y="138" font-size="11" fill="#2e7d32" text-anchor="middle">all +</text>
  <text x="110" y="120" font-size="18" font-weight="bold" fill="#6a1b9a" text-anchor="middle">S</text>
  <text x="110" y="138" font-size="11" fill="#6a1b9a" text-anchor="middle">sin +</text>
  <text x="110" y="250" font-size="18" font-weight="bold" fill="#ef6c00" text-anchor="middle">T</text>
  <text x="110" y="268" font-size="11" fill="#ef6c00" text-anchor="middle">tan +</text>
  <text x="250" y="250" font-size="18" font-weight="bold" fill="#00838f" text-anchor="middle">C</text>
  <text x="250" y="268" font-size="11" fill="#00838f" text-anchor="middle">cos +</text>
  <!-- angle marks -->
  <text x="330" y="174" font-size="12" fill="#607d8b">0°/360°</text>
  <text x="186" y="32" font-size="12" fill="#607d8b">90°</text>
  <text x="148" y="174" font-size="12" fill="#607d8b" text-anchor="end">180°</text>
  <text x="186" y="352" font-size="12" fill="#607d8b">270°</text>
  <text x="180" y="18" font-size="13" font-weight="bold" fill="#0d47a1" text-anchor="middle">Unit Circle · ASTC</text>
</svg>

🔑 **"Add Sugar To Coffee"** (Q1→Q4): **A**ll +, **S**in +, **T**an +, **C**os + — tells you the sign of each ratio per quadrant.

---

## 5. Height & Distance — Set-Up at a Glance

<!-- Right triangle for elevation -->
<svg xmlns="http://www.w3.org/2000/svg" width="420" height="220" viewBox="0 0 420 220" font-family="Segoe UI, Arial, sans-serif">
  <rect x="0" y="0" width="420" height="220" fill="#ffffff" stroke="#cfd8dc"/>
  <!-- triangle -->
  <polygon points="60,180 360,180 360,40" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <!-- right angle box -->
  <rect x="344" y="164" width="16" height="16" fill="none" stroke="#2e7d32"/>
  <!-- angle arc at left -->
  <path d="M 60 180 A 40 40 0 0 0 99 168" fill="none" stroke="#e53935" stroke-width="2"/>
  <text x="104" y="172" font-size="14" fill="#e53935">θ</text>
  <!-- labels -->
  <text x="210" y="200" font-size="14" text-anchor="middle" fill="#37474f">base = horizontal distance (adjacent)</text>
  <text x="372" y="115" font-size="14" fill="#37474f">height</text>
  <text x="372" y="131" font-size="14" fill="#37474f">(opposite)</text>
  <text x="195" y="100" font-size="14" fill="#1565c0" transform="rotate(-25 195 100)">hypotenuse</text>
  <text x="210" y="28" font-size="15" font-weight="bold" text-anchor="middle" fill="#0d47a1">tan θ = opposite / adjacent = height / distance</text>
</svg>

🔑 Write `tanθ = opposite/adjacent` **first**, then plug the standard value. Shadow = height → θ = 45°.

---

## 6. Bonus — SSC "Doubling at CI" Trick (Compound Interest)

When a sum **doubles every T years**, don't run the CI formula — just **count the periods and double**.

- **Formula:** `Amount = P × 2ⁿ`, where `n = (total time) ÷ (doubling time)`.
- **"Becomes x times"** → the multiplier is `2^(number of periods)`.
- **Count periods first, then double** — fastest and error-proof.

**Worked example:** ₹15,000 doubles every period; over 4 periods →
`Amount = 15000 × 2⁴ = 15000 × 16 = ₹240,000`.

<!-- Doubling chain visual -->
<svg xmlns="http://www.w3.org/2000/svg" width="520" height="120" viewBox="0 0 520 120" font-family="Segoe UI, Arial, sans-serif">
  <rect x="0" y="0" width="520" height="120" fill="#ffffff" stroke="#cfd8dc"/>
  <text x="260" y="26" font-size="15" font-weight="bold" text-anchor="middle" fill="#0d47a1">Doubling chain: ×2 each period</text>
  <g font-size="13" text-anchor="middle">
    <rect x="14"  y="48" width="88" height="38" rx="6" fill="#fff3e0" stroke="#fb8c00"/><text x="58"  y="72" font-weight="bold">15,000</text>
    <rect x="124" y="48" width="88" height="38" rx="6" fill="#fff3e0" stroke="#fb8c00"/><text x="168" y="72" font-weight="bold">30,000</text>
    <rect x="234" y="48" width="88" height="38" rx="6" fill="#fff3e0" stroke="#fb8c00"/><text x="278" y="72" font-weight="bold">60,000</text>
    <rect x="344" y="48" width="88" height="38" rx="6" fill="#fff3e0" stroke="#fb8c00"/><text x="388" y="72" font-weight="bold">120,000</text>
    <rect x="436" y="48" width="74" height="38" rx="6" fill="#e8f5e9" stroke="#2e7d32"/><text x="473" y="72" font-weight="bold">240,000</text>
    <text x="113" y="44" fill="#e53935">×2</text>
    <text x="223" y="44" fill="#e53935">×2</text>
    <text x="333" y="44" fill="#e53935">×2</text>
    <text x="434" y="44" fill="#e53935">×2</text>
  </g>
  <text x="260" y="108" font-size="12" text-anchor="middle" fill="#607d8b">4 periods → ×2⁴ = ×16</text>
</svg>

---

> ✅ **Last-day mindset:** glance, recognise, breathe. The tables and the unit circle above cover nearly every Tier-1 trig question — and the doubling trick saves a full CI calculation. Trust your prep.
