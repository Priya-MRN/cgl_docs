# Chapter 2 — Electronic Devices and Circuits

**Syllabus coverage (Unit 2, CEN 05/2025 Annexure-VII C):** PN Junction diodes, thyristor; Diode and triode circuits; Junction Transistors; Amplifiers; Oscillator; Multivibrator, counters; Rectifiers; Inverter and UPS.

---

## 📊 Weightage & Trend Box

| Parameter | Detail |
|---|---|
| Observed weight (CBT-2, 22-04-2025 shift) | **8 out of 50 technical questions ≈ 16%** — the single highest-weight unit |
| Expected marks contribution | 14–18 out of 100 technical marks |
| Difficulty band | Easy–Moderate; mostly formula-recall, statement-verification and one-step numericals |

**Topics actually asked in the 22-04-2025 CBT-2 paper (recreated in the PYQ Corner of this chapter):**

1. Rectifier comparison — statement question involving **TUF** (Transformer Utilisation Factor)
2. **BJT current relation** IE = IC + IB and α–β conversions
3. **Half-wave rectifier fed through a transformer** — turns-ratio / output-voltage numerical
4. **Bridge vs centre-tapped** full-wave rectifier — comparative statement question
5. **Colpitts oscillator** — pick-the-incorrect-statement
6. **n-type semiconductor** — majority carriers
7. **Ideal diode circuit** with input V(t) = sin²t + cos²t (a disguised 1 V DC source!)
8. **Oscillator / Barkhausen criterion** — pick-the-false-statement

**Preparation strategy:** Master the rectifier comparison table (ripple factor, efficiency, PIV, TUF, form factor) until you can reproduce it from memory; memorise every oscillator frequency formula and its identification trick; drill α/β/γ conversions; and never forget the trigonometric identity sin²θ + cos²θ = 1 — RRB literally tested it.

---

## 2.1 Semiconductor Physics — The Foundation

### 2.1.1 Energy bands and classification of materials

Electrons in an isolated atom occupy discrete energy levels. When atoms come close in a crystal, these levels split into closely spaced **energy bands**. The two bands that decide electrical behaviour are:

- **Valence band (VB):** highest band filled with electrons at 0 K.
- **Conduction band (CB):** the next higher band; electrons here are free to conduct.
- **Forbidden energy gap (Eg):** separation between the top of VB and bottom of CB.

| Material | Energy gap Eg | Behaviour |
|---|---|---|
| Conductor (Cu, Al) | Bands overlap, Eg ≈ 0 | Abundant free electrons |
| Semiconductor (Ge, Si, GaAs) | Ge ≈ 0.72 eV, Si ≈ 1.1 eV, GaAs ≈ 1.43 eV | Conduction possible with thermal/optical energy |
| Insulator (diamond, mica) | Eg > 3 eV (diamond ≈ 6 eV) | Practically no conduction |

**Key facts repeatedly asked:**
- Silicon (Z = 14) and Germanium (Z = 32) are **tetravalent** (4 valence electrons), Group-14 (IV-A) elements forming a diamond-cubic covalent lattice.
- Resistivity order: conductor (10⁻⁸ Ω·m) < semiconductor (10⁻⁵–10⁶ Ω·m) < insulator (10¹¹–10¹⁹ Ω·m).
- Semiconductors have a **negative temperature coefficient of resistance** — resistance *decreases* as temperature rises because carrier concentration increases exponentially.

### 2.1.2 Intrinsic semiconductors

A chemically pure semiconductor is **intrinsic**. At 0 K it behaves as a perfect insulator. At room temperature, thermal energy breaks some covalent bonds, generating **electron–hole pairs (EHP)**:

- Free electron → jumps to conduction band.
- **Hole** → the vacancy left in the valence band; behaves as a mobile positive charge carrier.

In an intrinsic semiconductor:

**n = p = nᵢ**

where nᵢ is the intrinsic carrier concentration (Si: nᵢ ≈ 1.5 × 10¹⁶ /m³; Ge: nᵢ ≈ 2.5 × 10¹⁹ /m³ at 300 K).

Intrinsic concentration rises steeply with temperature:

**nᵢ² = A₀ T³ e^(−Eg/kT)**

Total current = electron current + hole current. Conductivity of an intrinsic sample:

**σᵢ = nᵢ e (µₙ + µₚ)**

where µₙ, µₚ are electron and hole mobilities (for Si: µₙ ≈ 0.135 m²/V·s, µₚ ≈ 0.048 m²/V·s — electrons are roughly 2–3 times more mobile than holes).

### 2.1.3 Extrinsic semiconductors — doping

Adding a controlled impurity (≈ 1 part in 10⁶) enormously increases conductivity. Two types:

**n-type (donor doping)**
- Dopant: **pentavalent** atom — P, As, Sb, Bi (Group 15/V-A).
- Four electrons bond covalently; the fifth is loosely bound (~0.01–0.05 eV below CB) and is easily donated → **donor level just below the conduction band**.
- **Majority carriers: electrons. Minority carriers: holes.** ← *asked verbatim in the 2025 paper*
- n ≈ N_D (donor concentration); the crystal remains **electrically neutral** overall.

**p-type (acceptor doping)**
- Dopant: **trivalent** atom — B, Al, Ga, In (Group 13/III-A).
- Only three bonds complete; the vacancy accepts an electron → **acceptor level just above the valence band**.
- **Majority carriers: holes. Minority carriers: electrons.**
- p ≈ N_A.

**Mass-action law** (holds for both intrinsic and extrinsic material at thermal equilibrium):

**n · p = nᵢ²**

So doping that raises one carrier type suppresses the other proportionally.

**Charge neutrality:** p + N_D = n + N_A.

### 2.1.4 Drift and diffusion currents

Two transport mechanisms exist in semiconductors:

**Drift current** — carriers move under an applied electric field E:

- Drift velocity: v_d = µE
- Drift current density: **J_drift = (n e µₙ + p e µₚ) E = σE** (Ohm's law in point form)

**Diffusion current** — carriers move from high to low concentration (no field needed); unique to semiconductors:

- **Jₙ(diff) = +e Dₙ (dn/dx)**  **Jₚ(diff) = −e Dₚ (dp/dx)**

Dₙ, Dₚ are diffusion coefficients linked to mobility by the **Einstein relation**:

**D/µ = kT/e = V_T** (thermal voltage; **V_T ≈ 26 mV at 300 K**, ≈ T/11600 volts)

Total current density: J = J_drift + J_diffusion for each carrier type.

**Hall effect (quick recall):** when a current-carrying semiconductor is placed in a transverse magnetic field, a voltage develops perpendicular to both — used to find carrier type and concentration. Hall voltage V_H = BI/(n e t). The polarity of V_H tells whether the sample is n-type or p-type.

---

## 2.2 The PN Junction Diode

### 2.2.1 Junction formation and the depletion region

When p-type and n-type regions are formed in a single crystal:

1. Electrons diffuse from n → p; holes diffuse from p → n (concentration gradients).
2. Near the junction, they recombine, leaving **immobile ions**: negative acceptor ions on the p-side, positive donor ions on the n-side.
3. This carrier-free zone is the **depletion (space-charge) region**, width ≈ 0.1–0.5 µm.
4. The ionic charges create an internal electric field (n → p) and a **barrier potential V_B**:
   - **Si: ≈ 0.7 V, Ge: ≈ 0.3 V** (at 25 °C); GaAs ≈ 1.2 V.
   - V_B decreases by about **2 mV per °C rise** in temperature.
5. Equilibrium: diffusion current is exactly balanced by drift of minority carriers — net current zero.

Built-in potential (Boylestad/Millman level):

**V₀ = V_T ln(N_A N_D / nᵢ²)**

Depletion width W ∝ √(V₀ ± V) — widens under reverse bias, narrows under forward bias. The region penetrates deeper into the **lightly doped side** (W ∝ 1/N).

### 2.2.2 Biasing

**Forward bias** (p to +, n to −):
- Applied field opposes barrier; depletion narrows.
- Significant current flows once V > cut-in (knee) voltage **V_γ ≈ 0.7 V (Si) / 0.3 V (Ge)**.
- Current is due to **majority carriers**; grows exponentially.

**Reverse bias** (p to −, n to +):
- Barrier increases; depletion widens.
- Only a tiny **reverse saturation current I₀ (Iₛ)** flows, due to **minority carriers**; nearly independent of voltage.
- I₀ **doubles for every 10 °C rise** in temperature (both Si and Ge). I₀ is of order nA for Si, µA for Ge.

### 2.2.3 Diode equation and V-I characteristics

**Shockley diode equation:**

**I = I₀ (e^(V/ηV_T) − 1)**

- η (ideality factor) = 1 for Ge, ≈ 2 for Si at low currents (often taken as 1 in problems unless stated).
- V_T = kT/e ≈ 26 mV at 300 K.

The forward characteristic is exponential after the knee; the reverse characteristic is a flat −I₀ line until breakdown.

**Diode resistances:**

- **Static (DC) resistance:** R_D = V/I at the operating point.
- **Dynamic (AC) resistance:** r_d = ΔV/ΔI = **ηV_T / I** → the famous **r_d ≈ 26 mV / I(mA) ohms** (for η = 1).
- Bulk/body resistance of semiconductor material adds in series at high currents.

### 2.2.4 Diode equivalent models

| Model | Description | Use |
|---|---|---|
| **Ideal diode** | Short when forward, open when reverse; V_γ = 0, r_f = 0 | Quick circuit analysis, exam "ideal diode" questions |
| **Constant-voltage / practical (2nd approx.)** | Battery V_γ (0.7 V Si) in series with ideal diode | Most numericals |
| **Piecewise-linear (3rd approx.)** | V_γ + forward resistance r_f in series | Accurate rectifier calculations |

### 2.2.5 Breakdown — Zener vs Avalanche

Under sufficient reverse voltage, the diode conducts heavily — **breakdown**. Not destructive if current is limited.

| Feature | **Zener breakdown** | **Avalanche breakdown** |
|---|---|---|
| Mechanism | High field (~10⁷ V/m) directly ruptures covalent bonds — quantum-mechanical tunnelling of electrons | Minority carriers accelerated by field cause impact ionisation → carrier multiplication (chain reaction) |
| Doping | **Heavily doped**, thin depletion layer | Lightly doped, wide depletion layer |
| Breakdown voltage | Low: **V_Z < ~5–6 V** | Higher: **V_Z > ~6–8 V** |
| Temperature coefficient | **Negative** (V_Z falls as T rises) | **Positive** (V_Z rises as T rises) |
| V-I knee | Sharp | Softer |

Around 5–6 V both mechanisms coexist and the temperature coefficient is nearly zero — hence 5.6 V Zeners are the most temperature-stable.

### 2.2.6 Zener diode as voltage regulator

A Zener operated in reverse breakdown maintains nearly constant voltage V_Z across itself. Standard shunt-regulator circuit: unregulated V_in → series resistor R_S → Zener (in reverse) in parallel with load R_L.

Analysis (Zener ON when the open-circuit voltage across it ≥ V_Z):

- Voltage across load: **V_L = V_Z**
- Series-resistor current: **I_S = (V_in − V_Z)/R_S**
- Load current: **I_L = V_Z/R_L**
- Zener current: **I_Z = I_S − I_L** (must satisfy I_Z(min) ≤ I_Z ≤ I_Z(max) = P_Z/V_Z)

Regulation works against both **line variations** (changing V_in) and **load variations** (changing R_L). Worst cases: I_Z is maximum when V_in is max and I_L is min; I_Z is minimum when V_in is min and I_L is max.

### 2.2.7 Special-purpose diodes

| Diode | Bias used | Principle | Applications / key point |
|---|---|---|---|
| **LED** | Forward | Electroluminescence — radiative recombination of injected carriers | Made from **GaAs (IR), GaAsP (red/yellow), GaP (green)** — never plain Si/Ge (indirect band gap). λ = 1240/Eg(eV) nm. Cut-in ≈ 1.8–2.4 V |
| **Photodiode** | **Reverse** | Light generates EHPs in depletion region → photocurrent ∝ illumination | Light detectors, optocouplers; faster than LDR |
| **Solar cell** | No external bias | Photovoltaic effect at unbiased junction | Large area junction; open-circuit voltage ≈ 0.5–0.6 V per Si cell |
| **Varactor (varicap)** | **Reverse** | Depletion width (hence junction/transition capacitance C_T ∝ 1/√V_R) varies with reverse voltage | Electronic tuning, VCOs, AFC |
| **Schottky (hot-carrier)** | Forward | **Metal–semiconductor** junction; conduction by majority carriers only — no minority-carrier storage | Very fast switching, low forward drop ≈ 0.2–0.3 V; used in SMPS, clamping in TTL (Schottky TTL) |
| **Tunnel (Esaki) diode** | Forward | Very heavy doping (1:10³) → extremely thin junction → quantum tunnelling | Exhibits **negative resistance region** between peak (V_P ≈ 65 mV) and valley (V_V ≈ 350 mV Ge); microwave oscillators, high-speed switching |
| **PIN diode** | Reverse/RF | Intrinsic layer between p and n | RF switch/attenuator |

**Diode capacitances:** transition (depletion) capacitance C_T dominates in **reverse** bias (varactor); diffusion (storage) capacitance C_D dominates in **forward** bias and limits switching speed (reverse recovery time t_rr).

---

## 2.3 Diode Circuits — Rectifiers

Rectification = conversion of AC into unidirectional (pulsating) DC. Input: v = V_m sin ωt from the transformer secondary.

### 2.3.1 Half-wave rectifier (HWR)

One diode conducts only in the positive half-cycle; output is zero for the negative half.

**Derivations (ideal diode, resistive load R_L):**

- DC (average) load current: I_dc = (1/2π)∫₀^π I_m sin θ dθ = **I_m/π**
- DC output voltage: **V_dc = V_m/π ≈ 0.318 V_m**
- RMS load current: I_rms = √[(1/2π)∫₀^π I_m² sin²θ dθ] = **I_m/2**
- **Form factor** = I_rms/I_dc = (I_m/2)/(I_m/π) = **π/2 = 1.57**
- **Ripple factor** γ = √(FF² − 1) = √(1.57² − 1) = **1.21**
- **Rectification efficiency** η = P_dc/P_ac = (I_dc²R_L)/(I_rms²(r_f+R_L)) → max **η = 4/π² = 40.6 %** (ideal diode)
- **PIV = V_m**
- **TUF = 0.287** (secondary); because DC flows through the secondary, the transformer core suffers **DC saturation** — a major drawback.
- Ripple (lowest/fundamental) frequency = **f** (same as supply, e.g. 50 Hz).

### 2.3.2 Full-wave centre-tapped rectifier (FWR-CT)

Two diodes + centre-tapped secondary; each half of the secondary drives one diode alternately, so **both half-cycles** appear across the load in the same direction.

- **I_dc = 2I_m/π**, **V_dc = 2V_m/π ≈ 0.636 V_m** (V_m = peak of *half* secondary)
- **I_rms = I_m/√2**
- **Form factor = (I_m/√2)/(2I_m/π) = π/(2√2) = 1.11**
- **Ripple factor γ = √(1.11² − 1) = 0.482 ≈ 0.48**
- **η(max) = 8/π² = 81.2 %**
- **PIV = 2V_m** ← the big penalty of the centre-tap topology
- **TUF = 0.693** (average of primary 0.812 and secondary 0.574)
- Ripple frequency = **2f** (100 Hz on 50 Hz mains).

### 2.3.3 Bridge rectifier

Four diodes in a bridge; no centre tap required. In each half-cycle two diagonal diodes conduct in series.

- Same waveform maths as FWR-CT: V_dc = 2V_m/π, FF = 1.11, γ = 0.48, η(max) = 81.2 %
- **PIV per diode = V_m only** (half that of centre-tap for the same output)
- **TUF = 0.812** — best transformer utilisation
- Two diode drops (≈ 1.4 V for Si) in series each half-cycle — slight disadvantage at low voltages
- Ripple frequency = **2f**.

### 2.3.4 Master comparison table (memorise completely)

| Parameter | Half-wave | Full-wave centre-tap | Bridge |
|---|---|---|---|
| No. of diodes | 1 | 2 | 4 |
| V_dc (ideal) | V_m/π = 0.318 V_m | 2V_m/π = 0.636 V_m | 2V_m/π = 0.636 V_m |
| I_rms | I_m/2 | I_m/√2 | I_m/√2 |
| Form factor | **1.57** | **1.11** | **1.11** |
| Ripple factor | **1.21** | **0.482** | **0.482** |
| Max efficiency | **40.6 %** | **81.2 %** | **81.2 %** |
| PIV per diode | V_m | **2V_m** | **V_m** |
| TUF | 0.287 | 0.693 | **0.812** |
| Ripple frequency | f | 2f | 2f |
| Centre-tapped transformer? | No | **Yes** | No |
| Diode drops in path | 1 | 1 | 2 |
| DC core saturation | Yes | No | No |

**Bridge vs centre-tap (statement questions love these):**
1. Bridge needs no centre-tapped transformer (cheaper, smaller transformer).
2. PIV rating of bridge diodes is half → suits **high-voltage** applications.
3. Bridge has the **highest TUF (0.812)**.
4. Centre-tap wins only where the two extra diode drops matter (very low output voltages) since it has one diode drop per path.

### 2.3.5 Transformer Utilisation Factor (TUF) — asked in 2025

**TUF = P_dc delivered to load / AC (VA) rating of the transformer**

It measures how effectively transformer VA capacity is converted into DC power. TUF is always < 1. Ranking: **Bridge (0.812) > FW centre-tap (0.693) > Half-wave (0.287)**. Low TUF of HWR means a much bigger transformer is needed for the same DC output.

### 2.3.6 Filters

The pulsating rectifier output = DC + ripple harmonics. Filters pass DC and block ripple.

| Filter | Connection | Behaviour | Ripple factor (FWR) | Best at |
|---|---|---|---|---|
| **Shunt capacitor (C)** | C across load | C charges to V_m, feeds load during diode-off time | γ = 1/(4√3 f C R_L) | Light loads (small I_dc). Surge current on diodes is high |
| **Series inductor (L)** | L in series | L opposes changes in current | γ = R_L/(3√2 ωL) | Heavy loads (large I_dc) |
| **LC (L-section)** | L series + C shunt | Combines both; ripple independent of load | γ = √2/(12 ω²LC) | Good regulation; needs bleeder resistor & critical inductance L_C = R_L/3ω |
| **π (CLC)** | C–L–C | Highest DC output (≈ V_m), best smoothing | Higher than LC at same L,C values? No — lowest ripple, but **poor regulation** | Low-current, low-ripple loads |

Capacitor-filter DC output ≈ V_m − I_dc/(4fC) for full-wave. Peak-to-peak ripple V_r(pp) = I_dc/(2fC) (full-wave), I_dc/(fC) (half-wave).

### 2.3.7 Clippers and clampers

**Clipper (limiter):** removes part of the waveform above/below a reference level using a diode ± bias battery. Series clipper (diode in series with load) or shunt clipper (diode across load). Output amplitude is *changed*; DC level essentially unchanged. Applications: wave shaping, protection, TV sync separation.

- Positive clipper: removes positive peaks. Biased clipper: clips beyond V_γ + V_bias.
- Two-level (slicer/zener) clipper: clips both peaks — makes an approximate square wave from a sine.

**Clamper (DC restorer):** shifts the entire waveform up or down **without changing its shape or peak-to-peak value**, using a capacitor + diode (+ optional bias). RC ≫ T (typically ≥ 10T).

- Positive clamper: pushes waveform up (diode conducts on negative peak, charging C to V_m).
- Negative clamper: pushes it down.
- Total swing after clamping = same 2V_m; new peak = 2V_m (voltage doubler principle builds on this).

**Rule of thumb:** clipper *cuts*, clamper *shifts*.

---

## 2.4 Junction Transistor (BJT)

### 2.4.1 Construction

A Bipolar Junction Transistor = two PN junctions back-to-back sharing a common middle region: **NPN** or **PNP**.

| Region | Doping | Width | Role |
|---|---|---|---|
| **Emitter (E)** | Heaviest | Moderate | Injects (emits) majority carriers |
| **Base (B)** | Lightest | **Thinnest** (~µm) | Passes carriers through; small recombination |
| **Collector (C)** | Moderate | **Largest area** | Collects carriers; large area to dissipate heat |

"Bipolar" = both electrons **and** holes take part in conduction. NPN is preferred: electron mobility > hole mobility → faster, higher gain.

### 2.4.2 Operation (active region, NPN)

Bias for amplifier action: **emitter–base junction forward biased, collector–base junction reverse biased.**

1. Forward-biased EB junction injects electrons from emitter into the base.
2. Base is thin and lightly doped → only ~1–5 % recombine (forming I_B).
3. ~95–99 % diffuse across and are swept into the collector by the reverse-biased CB field → I_C.

**Fundamental current relation (KCL on the device):**

**I_E = I_C + I_B**  ← asked directly in 2025

Including leakage: I_C = αI_E + I_CBO, and in CE form I_C = βI_B + I_CEO where **I_CEO = (1+β) I_CBO**.

### 2.4.3 Current gains α, β, γ

- **α (CB current gain)** = I_C/I_E (0.95–0.998, always < 1)
- **β = h_FE (CE current gain)** = I_C/I_B (20–500)
- **γ (CC current gain)** = I_E/I_B = **1 + β**

Conversions (drill these):

**β = α/(1−α)  α = β/(1+β)  γ = 1 + β = 1/(1−α)**

### 2.4.4 Configurations — comparison table

| Property | Common Base (CB) | Common Emitter (CE) | Common Collector (CC) |
|---|---|---|---|
| Input between | E–B | B–E | B–C |
| Current gain | α < 1 | **β (high)** | γ = 1+β (highest) |
| Voltage gain | High | **High** | < 1 (≈ 0.95–0.99) |
| Power gain | Moderate | **Highest** | Lowest |
| Input impedance | Very low (20–100 Ω) | Moderate (~1 kΩ) | **Very high (~100s of kΩ)** |
| Output impedance | Very high (~MΩ) | Moderate (~50 kΩ) | **Very low (~50 Ω)** |
| Phase shift (in–out) | 0° | **180°** | 0° |
| Applications | HF amplifier, impedance step-up | **General amplifier** (most used) | Buffer / emitter follower, impedance matching |

### 2.4.5 CE output characteristics and regions of operation

Plot of I_C vs V_CE for steps of I_B shows three regions:

| Region | EB junction | CB junction | Behaviour | Use |
|---|---|---|---|---|
| **Cut-off** | Reverse | Reverse | I_C ≈ 0 (only leakage) | Switch OFF |
| **Active** | Forward | Reverse | I_C = βI_B, nearly flat curves | **Amplifier** |
| **Saturation** | Forward | Forward | V_CE ≈ 0.2 V (Si), I_C limited by external circuit | Switch ON |

Early effect (base-width modulation): increasing V_CE slightly narrows the base → curves have small upward slope in active region.

### 2.4.6 DC load line and Q-point

For a CE stage with collector supply V_CC and collector resistor R_C (plus R_E if present), KVL gives:

**V_CE = V_CC − I_C (R_C + R_E)**

This straight line on the output characteristics is the **DC load line**:
- V_CE-axis intercept (cut-off point): V_CE = V_CC (I_C = 0)
- I_C-axis intercept (saturation point): I_C(sat) = V_CC/(R_C + R_E)

The **quiescent (Q) point** is the intersection of the load line with the I_B = I_BQ characteristic. For maximum symmetrical swing in class-A: place Q at the **middle** of the load line (V_CEQ ≈ V_CC/2).

AC load line has slope −1/(R_C ∥ R_L) and passes through Q; it is steeper than the DC load line.

### 2.4.7 Biasing methods and stability factor

Bias circuits must hold Q fixed against temperature (I_CBO doubles/10 °C, V_BE −2 mV/°C, β spread).

**Stability factor S = ∂I_C/∂I_CBO** (smaller is better; ideal = 1).

| Method | Circuit essence | S | Comment |
|---|---|---|---|
| **Fixed bias (base bias)** | Single R_B from V_CC to base | **S = 1 + β** (worst) | Simplest; thermally unstable; risk of thermal runaway |
| **Collector-to-base bias** | R_B from collector to base | S = (1+β)/(1 + β·R_C/(R_C+R_B)) | Negative feedback improves stability; reduces gain |
| **Emitter bias (fixed + R_E)** | R_B + emitter resistor R_E | Between fixed and voltage-divider | R_E gives current-series feedback |
| **Voltage-divider (self) bias** | R₁–R₂ divider + R_E | **S = (1+β)·(1 + R_B/R_E)/(1 + β + R_B/R_E) ≈ 1 + R_B/R_E** (best practical) | Industry standard; Q nearly independent of β |

Voltage-divider analysis: V_B = V_CC·R₂/(R₁+R₂) (if divider stiff, i.e. I_divider ≫ I_B); V_E = V_B − 0.7; I_C ≈ I_E = V_E/R_E; V_CE = V_CC − I_C(R_C + R_E).

**Thermal runaway:** rise in T → I_CBO↑ → I_C↑ → junction power ↑ → T↑ … cumulative destruction. Prevented by R_E (self-bias), heat sinks, and ensuring V_CE < V_CC/2 condition for thermal stability.

### 2.4.8 BJT as a switch

- **OFF:** base open/reverse biased → cut-off → V_out ≈ V_CC.
- **ON:** enough base drive to saturate (I_B > I_C(sat)/β) → V_CE(sat) ≈ 0.2 V.
Used in logic gates, relay/LED drivers, choppers. Switching speed is limited by storage time (charge stored in base during saturation).

---

## 2.5 Field-Effect Transistors — JFET and MOSFET (basics)

FETs are **unipolar** (conduction by one carrier type only), **voltage-controlled** devices with very high input impedance.

### 2.5.1 JFET

- Structure: n-channel (or p-channel) bar with two p⁺ (or n⁺) gate regions; terminals **Source, Gate, Drain**.
- Gate–channel junction always **reverse biased**; input impedance ~10⁸ Ω.
- Increasing |V_GS| widens depletion, narrows channel; at **pinch-off voltage V_P**, channel closes and I_D saturates.
- Transfer (Shockley) equation: **I_D = I_DSS (1 − V_GS/V_P)²** — square-law device (low intermodulation distortion).
- Transconductance: **g_m = ∂I_D/∂V_GS = g_m0 (1 − V_GS/V_P)**, where g_m0 = 2I_DSS/|V_P|.
- Amplification factor: **µ = g_m × r_d**.
- JFET is a **depletion-mode-only** device; normally ON at V_GS = 0.

### 2.5.2 MOSFET

Metal-Oxide-Semiconductor FET: gate insulated from channel by SiO₂ → input impedance 10¹⁰–10¹⁵ Ω; handle with anti-static care (gate oxide punctures easily).

| Type | State at V_GS = 0 | Control |
|---|---|---|
| **Depletion MOSFET (D-MOSFET)** | ON (channel built in) | Can be operated in both depletion and enhancement modes |
| **Enhancement MOSFET (E-MOSFET)** | **OFF** (no channel) | Conducts only when V_GS > threshold V_T; I_D = k(V_GS − V_T)² |

E-MOSFETs (NMOS/PMOS) are the basis of **CMOS** digital ICs — negligible static power. Power MOSFETs (VDMOS) dominate SMPS and motor drives.

**BJT vs FET quick contrast:** BJT — bipolar, current-controlled, low input Z, higher gain, cheaper; FET — unipolar, voltage-controlled, very high input Z, better thermal stability (negative temperature coefficient of I_D prevents thermal runaway), lower noise.

---

## 2.6 Transistor Amplifiers

### 2.6.1 Small-signal CE amplifier

The workhorse voltage amplifier: voltage-divider-biased CE stage with coupling capacitors (block DC) and emitter bypass capacitor (restores AC gain).

- AC emitter resistance: **r_e′ = 26 mV / I_E(mA)**
- Voltage gain (bypassed R_E): **A_v ≈ −(R_C ∥ R_L)/r_e′** (minus = 180° phase inversion)
- Input impedance: Z_in = R₁ ∥ R₂ ∥ β r_e′
- Removing the bypass capacitor: A_v ≈ −R_C/(r_e′ + R_E) — lower but stabler gain (swamping).

### 2.6.2 h-parameters (hybrid model) — basics

For any two-port: v₁ = h_i i₁ + h_r v₂; i₂ = h_f i₁ + h_o v₂.

| Symbol (CE) | Name | Typical value | Unit |
|---|---|---|---|
| h_ie | Input impedance (output shorted) | 1–2 kΩ | Ω |
| h_re | Reverse voltage ratio | 2.5 × 10⁻⁴ | — |
| h_fe (= β_ac) | Forward current gain | 50–300 | — |
| h_oe | Output admittance (input open) | 25 µS | siemens (℧) |

Note the mixed units → "hybrid". Approximate CE results: A_i = −h_fe/(1 + h_oe R_L) ≈ −h_fe; Z_in ≈ h_ie; A_v = −h_fe R_L/h_ie.

### 2.6.3 Multistage & RC-coupled amplifier frequency response

Cascading raises gain: overall A = A₁ × A₂ × … ; in dB, gains add. Coupling methods: RC (cheapest, audio), transformer (impedance matching, power), direct (DC amplifiers, drift problem).

**RC-coupled amplifier response** (the classic curve):
- **Low-frequency roll-off:** coupling & bypass capacitors' reactance rises → gain falls.
- **Mid-band:** capacitors ≈ shorts, strays ≈ open → flat maximum gain.
- **High-frequency roll-off:** shunt/stray/junction capacitances (and Miller capacitance C_M = C_bc(1+|A_v|)) short the signal.
- **Cut-off frequencies f₁ (lower), f₂ (upper):** gain = A_mid/√2 = **−3 dB points** (half-power points).
- **Bandwidth BW = f₂ − f₁**; **Gain × Bandwidth = constant** (figure of merit f_T).

### 2.6.4 Amplifier classes (power amplifiers)

| Class | Conduction angle | Q-point location | Max theoretical efficiency | Distortion | Use |
|---|---|---|---|---|---|
| **A** | 360° | Centre of load line | **25 %** (series-fed), **50 %** (transformer-coupled) | Lowest | Small-signal, hi-fi |
| **B** | 180° | At cut-off | **78.5 % (π/4)** | Crossover distortion in push-pull | Push-pull output stages |
| **AB** | 180°–360° | Slightly above cut-off | 50–78.5 % | Removes crossover distortion | Audio power amps |
| **C** | < 180° | Below cut-off | > 90 % (up to ~99 %) | Very high — needs tuned tank | RF tuned amplifiers, oscillators |

Push-pull class-B: two transistors handle alternate half-cycles; even harmonics cancel. Complementary-symmetry version (NPN + PNP) eliminates transformers. Crossover distortion (dead zone ±0.7 V) removed by class-AB pre-bias (diode biasing).

### 2.6.5 Distortion & noise (one-liners)
- Amplitude (harmonic) distortion — nonlinearity of characteristics; measured by THD.
- Frequency distortion — unequal gain at different frequencies.
- Phase distortion — unequal phase shift vs frequency.
- Noise figure NF = (S/N)_in / (S/N)_out in dB; ideal amplifier NF = 0 dB.

---

## 2.7 Feedback in Amplifiers

Feedback returns a fraction β_f (feedback factor) of the output to the input.

**Closed-loop gain: A_f = A / (1 + Aβ_f)** (negative feedback; loop gain = Aβ_f)

If |1 + Aβ_f| > 1 → **negative (degenerative)**; if < 1 → positive (regenerative); if 1 + Aβ_f = 0 → oscillation.

**Effects of negative feedback (all by the factor D = 1 + Aβ_f):**

| Quantity | Effect |
|---|---|
| Gain | Decreases: A_f = A/D |
| Gain stability | Improves: dA_f/A_f = (1/D)(dA/A) |
| Bandwidth | **Increases**: BW_f = D × BW (gain × BW constant) |
| Distortion & noise (in loop) | Decreases by D |
| Input impedance | ↑ for **series** mixing; ↓ for shunt mixing |
| Output impedance | ↓ for **voltage** (shunt) sampling; ↑ for current (series) sampling |

**Four topologies:**

| Topology (sampling–mixing) | Alt name | Z_in | Z_out | Stabilised gain | Example |
|---|---|---|---|---|---|
| Voltage-series | Series-shunt | ↑ | ↓ | Voltage gain | Emitter follower, non-inverting op-amp |
| Voltage-shunt | Shunt-shunt | ↓ | ↓ | Transresistance | Collector-to-base bias, inverting op-amp |
| Current-series | Series-series | ↑ | ↑ | Transconductance | Unbypassed R_E stage |
| Current-shunt | Shunt-series | ↓ | ↑ | Current gain | Two-stage feedback pair |

When Aβ_f ≫ 1: **A_f ≈ 1/β_f** — gain set only by (passive, stable) feedback network.

---

## 2.8 Oscillators

An oscillator converts DC into AC of desired frequency **without any external input signal** — it is an amplifier with **positive feedback** satisfying:

### 2.8.1 Barkhausen criterion — asked in 2025

For sustained oscillations:

1. **Loop gain magnitude |Aβ_f| = 1** (in practice slightly > 1 to start; amplitude then self-limits), and
2. **Total loop phase shift = 0° or 360°** (i.e. 2nπ).

The starting "input" is internal noise/switching transient — no external signal is required. If |Aβ| < 1 oscillations die out; if held ≫ 1 the output distorts/clips.

### 2.8.2 RC oscillators (audio frequency)

**RC phase-shift oscillator**
- CE amplifier (180°) + three-section RC ladder giving another 180° (60° per section).
- **f = 1/(2πRC√6)** (FET/ideal version); with BJT loading: f = 1/[2πRC√(6 + 4R_C/R)].
- Requires amplifier gain **|A| ≥ 29** (β_f = 1/29).

**Wien bridge oscillator**
- Series RC + parallel RC (lead–lag) network in a bridge; two-stage/non-inverting amplifier (0° amplifier phase, 0° network phase at f₀).
- **f = 1/(2πRC)** (equal R, C).
- Network attenuation = 1/3 → requires **gain ≥ 3** (so in op-amp form R_f = 2R₁).
- Amplitude stabilised by a thermistor/sensistor or lamp. Excellent low-distortion sine source; standard in audio signal generators.

### 2.8.3 LC oscillators (radio frequency)

General form: tank circuit of reactances X₁, X₂ (across the two amplifier input/output nodes) and X₃ (feedback). Oscillation needs X₁, X₂ same type and X₃ opposite type.

**Hartley oscillator** — **tapped inductor** (two inductors L₁, L₂, may be mutually coupled M) + one capacitor:

**f = 1/(2π√(L_eq C)), L_eq = L₁ + L₂ + 2M**; feedback fraction β_f = L₂/L₁ (gain needed ≈ L₁/L₂).

**Colpitts oscillator** — **tapped capacitor** (C₁, C₂ in series) + one inductor:

**f = 1/(2π√(L C_eq)), C_eq = C₁C₂/(C₁ + C₂)**; feedback fraction = C₁/C₂ (voltage divider across capacitors); gain condition ≈ C₂/C₁ (using amplifier input side C₂). Better frequency stability than Hartley at high f; capacitors are cheaper/purer than tapped coils.

**Clapp oscillator** — Colpitts + small capacitor **C₃ in series with L**; C₃ ≪ C₁, C₂ dominates the frequency:

**f = (1/2π)√[(1/L)(1/C₁ + 1/C₂ + 1/C₃)] ≈ 1/(2π√(LC₃))**

Frequency almost independent of transistor junction capacitances → improved stability.

**Identification trick:** **C**olpitts → **C**apacitive divider; **H**artley → tapped **H**enries (inductor); Clapp → Colpitts + extra series C.

### 2.8.4 Crystal oscillator

Quartz crystal = electromechanical resonator (piezoelectric effect). Equivalent circuit: series R-L-C (motional arm) in parallel with mount capacitance C_M.

- **Series resonance f_s = 1/(2π√(LC))**; parallel (antiresonance) f_p slightly above f_s; crystal is **inductive between f_s and f_p** — the region used in oscillator circuits (e.g. Pierce = crystal Colpitts).
- Extraordinary **Q (10⁴–10⁶)** → frequency stability ~1 ppm or better.
- Used wherever accuracy matters: clocks, microprocessors, transmitters, watches.

**Frequency-stability ranking: Crystal ≫ Clapp > Colpitts ≈ Hartley > RC types.**

### 2.8.5 Negative-resistance & relaxation oscillators
- Tunnel-diode and UJT oscillators exploit negative-resistance/relaxation action (UJT covered in §2.10.6).
- Relaxation oscillators produce **non-sinusoidal** (sawtooth/square) outputs via RC charge–discharge.

---

## 2.9 Multivibrators and Counters

Multivibrators are two-stage regenerative (positive-feedback) switching circuits producing square/rectangular waves. Each stage drives the other; the transistors act as switches, alternately cut-off and saturated.

### 2.9.1 The three types

| Type | Stable states | Coupling (classic BJT circuit) | Output | Also called | Applications |
|---|---|---|---|---|---|
| **Astable** | **0** (free-running) | Both stages **capacitor (AC)** coupled | Continuous square wave | Free-running MV | Clock generation, flashers |
| **Monostable** | **1** | One capacitive + one resistive (DC) coupling | Single pulse of fixed width per trigger | One-shot | Pulse-width generation, timing/delay |
| **Bistable** | **2** | Both stages **resistive (DC)** coupled | Toggles state on each trigger, holds indefinitely | Flip-flop, Eccles–Jordan, binary | Memory, **counters**, frequency division |

### 2.9.2 Timing formulas (BJT collector-coupled circuits)

- Half-period of astable per side: T₁ = **0.693 R₁C₁** (time for the capacitor to bring the off transistor's base up through V_BE); total **T = 0.693(R₁C₁ + R₂C₂)**; symmetric case **T = 1.386 RC**, f = 1/T ≈ **0.72/RC**.
- Monostable pulse width: **T = 0.693 RC**.
- (IC 555 versions: astable T = 0.693(R_A + 2R_B)C; monostable T = 1.1 RC — useful cross-checks.)

### 2.9.3 Schmitt trigger

An emitter-coupled bistable with **hysteresis**: two different threshold voltages, Upper Trip Point (UTP) and Lower Trip Point (LTP). Converts any slowly varying/noisy waveform into a clean square wave — a "squaring circuit"/level detector. Hysteresis width = UTP − LTP gives noise immunity.

### 2.9.4 Counters (as required by the syllabus keyword)

A **counter** is a chain of bistable multivibrators (flip-flops). Each flip-flop **divides frequency by 2** (one output pulse for every two input triggers).

- **n flip-flops → modulus up to 2ⁿ** (counts 0 to 2ⁿ − 1). For MOD-m: n = ⌈log₂m⌉ flip-flops; unwanted states skipped by reset logic (e.g. decade counter MOD-10 uses 4 FFs, resets at 1010).
- **Asynchronous (ripple) counter:** clock ripples through FFs; simple but slow (delays add: t_total = n·t_pd).
- **Synchronous counter:** common clock to all FFs; faster, glitch-free.
- **Ring counter:** n FFs → MOD-n; **Johnson (twisted-ring):** n FFs → MOD-2n.
- Applications: digital clocks, frequency division/measurement, event counting. (Full digital treatment appears in the Digital Electronics chapter; here remember the multivibrator–counter link: **bistable = 1-bit memory = divide-by-2**.)

---

## 2.10 Thyristor Family

### 2.10.1 SCR — construction

The Silicon Controlled Rectifier is a **four-layer (P-N-P-N), three-junction (J₁, J₂, J₃), three-terminal** device: **Anode (A), Cathode (K), Gate (G — attached to the inner p-layer near the cathode)**. It is a unidirectional, latching power switch (ratings to several kA / kV).

### 2.10.2 V-I characteristic

- **Reverse blocking (A negative):** J₁, J₃ reverse biased → tiny leakage until reverse breakdown V_BR. SCR must never be gated here.
- **Forward blocking (A positive, no gate):** J₂ reverse biased → only leakage flows (OFF state) until the **forward break-over voltage V_BO**.
- **Forward conduction (ON):** once triggered (gate pulse or V > V_BO), J₂ collapses; device latches like a closed switch, drop ≈ 1–2 V. **Increasing gate current lowers the break-over voltage.**
- **Latching current I_L:** minimum anode current to latch ON just after triggering (gate may then be removed).
- **Holding current I_H:** minimum anode current below which the SCR turns OFF. **I_L > I_H** (typically I_L ≈ 2–3 × I_H).

### 2.10.3 Two-transistor analogy

Split the PNPN structure into a PNP (Q₁) and an NPN (Q₂) transistor: collector of each feeds the base of the other. Anode current:

**I_A = (α₁ + α₂) I_A + I_leak → I_A = I_leak / [1 − (α₁ + α₂)]**

When gate/leakage current raises α₁ + α₂ → 1, I_A → ∞ (limited only by external circuit) — **regenerative latching**. This explains: (i) why the gate loses control after turn-on, and (ii) dv/dt false triggering (junction capacitance current mimics gate current).

### 2.10.4 Triggering (turn-on) and commutation (turn-off)

**Turn-on methods:**
1. **Gate triggering** (normal method — small gate pulse while forward biased)
2. Forward-voltage triggering (exceeding V_BO — avoided in practice)
3. **dv/dt triggering** (fast anode voltage rise — unwanted; suppressed by RC **snubber**)
4. Temperature triggering (leakage rise — unwanted)
5. Light triggering (**LASCR** — used in HVDC valves)

**Turn-off (commutation)** — anode current must fall below I_H and reverse bias/zero bias held for the turn-off time t_q:
- **Natural (line) commutation:** AC supply reverses every half-cycle — free of cost; used in phase-controlled rectifiers, AC regulators.
- **Forced commutation:** in DC circuits an auxiliary L-C circuit forces current to zero (classes A–F) — used in choppers and (older) inverters.

**Gate protection & firing:** series resistor limits gate current, R-C across gate for noise, pulse-transformer/optocoupler isolation; R-firing, RC-firing and UJT-firing circuits give 0–90°, 0–180°, and precise wide-range control respectively.

### 2.10.5 TRIAC and DIAC

**TRIAC** = two SCRs in inverse parallel integrated in one 5-layer chip; terminals **MT₁, MT₂, Gate**. Conducts in **both directions**; can be triggered by positive or negative gate pulses (four triggering modes; quadrants I+ and III− are most sensitive). Used in AC phase control: fan regulators, lamp dimmers, temperature control. Drawback vs two SCRs: lower dv/dt rating, less sensitive in some quadrants.

**DIAC** = gateless bidirectional trigger diode (3-layer/5-layer symmetric). Blocks until break-over (≈ 30–35 V) in either polarity, then exhibits negative resistance. Almost always used in the gate circuit of a TRIAC (dimmers) to deliver sharp symmetric trigger pulses.

**Other members (one-liners):** GTO — gate turn-off thyristor (negative gate pulse turns it OFF; no forced-commutation circuit needed); SCS — silicon controlled switch (two gates); PUT — programmable UJT; MCT/IGBT covered in Power Electronics.

### 2.10.6 UJT and the relaxation oscillator

**UJT (Uni-Junction Transistor):** lightly doped n-type silicon bar with base contacts B₁, B₂ and a single p-emitter part-way along — one PN junction, hence the name; also called *double-base diode*.

- **Intrinsic stand-off ratio: η = R_B1/(R_B1 + R_B2)**, typically **0.5–0.8**.
- Emitter peak (firing) voltage: **V_P = ηV_BB + V_D** (V_D ≈ 0.7 V).
- Once V_E ≥ V_P, the E–B₁ region floods with carriers → R_B1 collapses → **negative-resistance region** between peak and valley points — the key to oscillation.

**UJT relaxation oscillator:** R_T charges C_T toward V_BB; at V_P the UJT fires and rapidly discharges C_T through B₁ (sharp pulse across R₁); C_T recharges and the cycle repeats.

**T ≈ R_T C_T ln[1/(1−η)], f = 1/T**

(For η = 0.63, T ≈ R_T C_T.) Output: sawtooth at the emitter, sharp spikes at B₁ — ideal, well-synchronised **trigger pulses for SCR/TRIAC firing**.

---

## 2.11 Triode and Vacuum-Tube Basics (brief — syllabus item)

Before semiconductors, thermionic vacuum tubes did every electronic job.

- **Diode valve (Fleming, 1904):** heated cathode (thermionic emission — Richardson's law) + anode (plate). Conducts only when plate is positive → rectifier. Space-charge-limited current follows **Child–Langmuir 3/2-power law: I_P ∝ V_P^(3/2)**.
- **Triode (De Forest, 1906):** adds a **control grid** between cathode and plate. A small negative grid voltage strongly throttles plate current → **amplification**.

**Triode constants** (defined at constant third variable):

| Constant | Definition | Typical |
|---|---|---|
| Amplification factor **µ** | −∂V_P/∂V_G at constant I_P | 10–100 |
| Plate (dynamic) resistance **r_p** | ∂V_P/∂I_P at constant V_G | 5–50 kΩ |
| Transconductance (mutual conductance) **g_m** | ∂I_P/∂V_G at constant V_P | 1–10 mA/V |

**Master relation: µ = g_m × r_p**

Triode amplifier gain: **A = µR_L/(r_p + R_L)** (approaches µ as R_L → ∞).

Later tubes: **tetrode** (screen grid — but has negative-resistance kink from secondary emission), **pentode** (adds suppressor grid — removes the kink; higher gain). Tubes survive today in high-power RF transmitters, magnetrons (microwave ovens), CRTs and boutique audio. Triode ↔ semiconductor analogy: cathode↔emitter/source, grid↔base/gate, plate↔collector/drain.

---

## 2.12 Inverters and UPS

### 2.12.1 Inverter

An **inverter converts DC into AC** of desired voltage and frequency (the inverse of a rectifier). Power devices used: MOSFET/IGBT (modern), thyristors with forced commutation (legacy).

**Classification:**

| Basis | Types |
|---|---|
| Source | **VSI** (Voltage Source Inverter — stiff DC voltage, capacitor at input) / **CSI** (Current Source Inverter — stiff DC current, large series inductor) |
| Phases | Single-phase (half-bridge: 2 switches, output ±V_dc/2; full-bridge/H-bridge: 4 switches, output ±V_dc) / Three-phase (6 switches; 120°- or 180°-conduction modes) |
| Output waveform | **Square wave** (simple, high harmonic content), **modified/quasi sine** (stepped), **pure sine** (PWM + LC filter — best for motors and sensitive loads) |
| Control | PWM — **sinusoidal PWM (SPWM)** compares a sine reference with a high-frequency triangular carrier; modulation index m_a = V_ref/V_carrier controls the fundamental output; harmonics pushed to high frequency, easily filtered |

Square-wave full-bridge output: RMS = V_dc; fundamental RMS = (4V_dc/π)/√2 = **0.9 V_dc**; only odd harmonics present (3rd = 1/3 amplitude, 5th = 1/5 …). Harmonic quality measured by **THD** (square wave THD ≈ 48.3 %).

Applications: solar/battery power systems, UPS, variable-frequency drives (VFD), induction heating, HVDC receiving stations, electric traction auxiliaries.

### 2.12.2 UPS — Uninterruptible Power Supply

A UPS delivers continuous, conditioned AC power to critical loads (computers, servers, medical, railway signalling) during mains failure or disturbances.

**Core blocks:** Rectifier/charger (AC→DC), **Battery bank** (energy storage), **Inverter** (DC→AC), **Static transfer switch/bypass**.

**Three standard topologies:**

| Type | Normal-path operation | Transfer time | Protection quality | Typical use |
|---|---|---|---|---|
| **Offline (standby)** | Load fed **directly from mains**; inverter idle, battery on float charge. On failure, static switch transfers load to inverter | ~4–10 ms (brief break) | Basic — voltage sags/noise pass through in normal mode | PCs, home use; cheapest, most efficient in standby |
| **Line-interactive** | Mains feeds load through an **AVR (buck–boost autotransformer)**; the bidirectional inverter/charger sits across the line and corrects sags/swells without draining the battery | ~2–4 ms | Good — regulates voltage without battery use | Small servers, network gear |
| **Online (double-conversion)** | Load is fed **always from the inverter**: mains → rectifier → DC bus (battery floats here) → inverter → load. Mains failure causes **zero transfer time** — battery is already in the path | **0 ms (no break)** | Best — total isolation from all mains disturbances; output frequency/voltage fully regenerated | Data centres, hospitals, railway signalling & telecom |

*Block-diagram memory aid (online UPS):* Mains → [Rectifier/Charger] → DC bus ← [Battery] → [Inverter] → [Static bypass switch] → Load. The bypass carries the load if the inverter itself fails or during overload/maintenance.

### 2.12.3 Battery sizing basics

- **Battery Ah capacity required ≈ (Load power in W × backup time in h) / (Battery voltage × inverter efficiency × depth-of-discharge)**
- Example: 600 W load, 1 h backup, 24 V bank, η_inv = 0.85, DoD = 0.8:
  Ah = 600 × 1 / (24 × 0.85 × 0.8) ≈ **36.8 Ah → choose 40–42 Ah bank (e.g. two 12 V, 42 Ah in series)**.
- **VA vs W:** UPS rating in VA; usable watts = VA × power factor (typically 0.6–0.8 for small UPS; unity for premium online units).
- Battery types: flooded/tubular lead-acid (long life, needs topping-up), **SMF/VRLA** (sealed maintenance-free — standard in UPS), Li-ion (modern, light, costly). Float charge ≈ 2.25 V/cell, boost ≈ 2.4 V/cell (lead-acid, 2 V nominal per cell → 6 cells = 12 V battery).
- Backup time ∝ Ah / load current; runtime doubles (roughly) when load halves.

---

## 2.13 Worked Numerical Examples (12)

**Example 1 — Diode dynamic resistance.**
A Si diode carries a forward DC current of 2 mA at 300 K. Find its dynamic resistance (η = 1).

*Solution:* r_d = ηV_T/I = 26 mV / 2 mA = **13 Ω**.

---

**Example 2 — Zener regulator.**
V_in = 20 V, R_S = 1 kΩ, V_Z = 10 V, R_L = 5 kΩ. Find I_S, I_L, I_Z and power dissipated in the Zener.

*Solution:*
I_S = (20 − 10)/1k = 10 mA; I_L = 10/5k = 2 mA; I_Z = 10 − 2 = **8 mA**.
P_Z = V_Z × I_Z = 10 × 8 mA = **80 mW**.

---

**Example 3 — Half-wave rectifier with transformer.**
A HWR is fed from 230 V, 50 Hz mains through a 10:1 step-down transformer. Diode ideal, R_L = 100 Ω. Find V_dc, I_dc, PIV and ripple frequency.

*Solution:*
Secondary RMS = 230/10 = 23 V → V_m = 23√2 ≈ 32.5 V.
V_dc = V_m/π = 32.5/3.1416 ≈ **10.35 V**; I_dc = 10.35/100 ≈ **103.5 mA**.
PIV = V_m ≈ **32.5 V**; ripple frequency = **50 Hz**.

---

**Example 4 — Full-wave centre-tap numbers.**
A centre-tapped FWR has 30-0-30 V (RMS) secondary, ideal diodes, R_L = 1 kΩ. Find V_dc, I_dc, PIV, and ripple factor.

*Solution:*
V_m (per half) = 30√2 ≈ 42.43 V.
V_dc = 2V_m/π = 2 × 42.43/π ≈ **27 V**; I_dc = 27 mA.
PIV = 2V_m ≈ **84.85 V**; γ = **0.482**.

---

**Example 5 — Rectifier efficiency with diode resistance.**
A half-wave rectifier uses a diode of forward resistance r_f = 20 Ω with R_L = 480 Ω. Find the rectification efficiency.

*Solution:*
η = 0.406/(1 + r_f/R_L) = 0.406/(1 + 20/480) = 0.406/1.04167 ≈ **0.39 → 39 %**.

---

**Example 6 — Capacitor filter ripple.**
A bridge rectifier (50 Hz mains) delivers 20 mA DC to a load with a 1000 µF filter capacitor. Find peak-to-peak ripple voltage.

*Solution:*
Full-wave: V_r(pp) = I_dc/(2fC) = 0.02/(2 × 50 × 1000×10⁻⁶) = 0.02/0.1 = **0.2 V**.

---

**Example 7 — α to β conversion.**
A transistor has α = 0.98 and I_E = 5 mA. Find β, I_C and I_B.

*Solution:*
β = α/(1−α) = 0.98/0.02 = **49**.
I_C = αI_E = 0.98 × 5 = **4.9 mA**; I_B = I_E − I_C = **0.1 mA** (check: I_C/I_B = 49 ✓).

---

**Example 8 — Voltage-divider bias Q-point.**
V_CC = 12 V, R₁ = 40 kΩ, R₂ = 8 kΩ, R_C = 2 kΩ, R_E = 1 kΩ, Si transistor (V_BE = 0.7 V), β large. Find I_C and V_CE.

*Solution:*
V_B = 12 × 8/(40+8) = 2 V; V_E = 2 − 0.7 = 1.3 V.
I_C ≈ I_E = 1.3/1k = **1.3 mA**.
V_CE = 12 − 1.3 mA × (2k + 1k) = 12 − 3.9 = **8.1 V**. Q-point = (8.1 V, 1.3 mA).

---

**Example 9 — Load line end-points.**
For V_CC = 10 V, R_C = 2 kΩ (no R_E), state the DC load-line intercepts and the mid-point Q for maximum swing.

*Solution:*
Cut-off point: (V_CE, I_C) = (**10 V, 0**). Saturation point: I_C = 10/2k = **5 mA** at V_CE = 0.
Mid-point Q: V_CEQ = 5 V, I_CQ = **2.5 mA**.

---

**Example 10 — CE amplifier gain.**
A CE amplifier has I_E = 1.3 mA, R_C = 3 kΩ, R_L = 6 kΩ (capacitively coupled), emitter fully bypassed. Estimate the voltage gain.

*Solution:*
r_e′ = 26/1.3 = 20 Ω. R_ac = R_C ∥ R_L = 3k×6k/9k = 2 kΩ.
A_v = −R_ac/r_e′ = −2000/20 = **−100** (gain 100 with 180° inversion).

---

**Example 11 — Colpitts frequency.**
A Colpitts oscillator uses C₁ = 100 pF, C₂ = 400 pF and L = 50 µH. Find the oscillation frequency.

*Solution:*
C_eq = C₁C₂/(C₁+C₂) = 100×400/500 = 80 pF.
f = 1/(2π√(LC_eq)) = 1/(2π√(50×10⁻⁶ × 80×10⁻¹²))
= 1/(2π√(4×10⁻¹⁵)) = 1/(2π × 6.325×10⁻⁸) ≈ **2.52 MHz**.

---

**Example 12 — UJT relaxation oscillator.**
A UJT with η = 0.63 is used with R_T = 10 kΩ, C_T = 0.1 µF, V_BB = 12 V. Find the firing voltage and oscillation frequency (V_D = 0.7 V).

*Solution:*
V_P = ηV_BB + V_D = 0.63 × 12 + 0.7 = **8.26 V**.
T = R_T C_T ln[1/(1−η)] = 10⁴ × 10⁻⁷ × ln(1/0.37) = 10⁻³ × 0.994 ≈ 1 ms.
f = 1/T ≈ **1 kHz**.

---

**Bonus Example 13 — Wien bridge.**
R = 10 kΩ, C = 0.01 µF in a Wien bridge oscillator. f = 1/(2πRC) = 1/(2π × 10⁴ × 10⁻⁸) = 1/(2π × 10⁻⁴) ≈ **1.59 kHz**; minimum amplifier gain required = **3**.

---

**Bonus Example 14 — Class-B efficiency check.**
A class-B push-pull amplifier with V_CC = 20 V drives a load to a peak output of 20 V (full swing). Maximum efficiency = π/4 = **78.5 %**. If the swing is only 10 V peak, η = (π/4)(V_peak/V_CC) = 0.785 × 0.5 ≈ **39.3 %**.

---

## 2.14 PYQ Corner — 22-04-2025 CBT-2 (recreated & fully solved)

**PYQ 1 (TUF statement).** *Which statement about Transformer Utilisation Factor is correct?*
(a) TUF of a half-wave rectifier is 0.812
(b) TUF = DC power delivered to load ÷ AC rating of transformer secondary
(c) TUF of a bridge rectifier is less than that of a half-wave rectifier
(d) TUF is always greater than 1

**Solution:** TUF is defined as P_dc/(transformer VA rating) — option **(b)**. Values: HWR 0.287, FW-CT 0.693, bridge 0.812 (highest); TUF < 1 always. Hence (a), (c), (d) are all wrong. **Answer: (b)**

---

**PYQ 2 (BJT current relation).** *For a junction transistor, which of the following is always true?*
(a) I_C = I_E + I_B (b) I_B = I_C + I_E (c) **I_E = I_C + I_B** (d) I_E = I_C − I_B

**Solution:** KCL at the device: the emitter current splits into collector and base components: **I_E = I_C + I_B**. Numerically I_E is the largest, I_B the smallest (I_B ≈ 1–5 % of I_E). **Answer: (c)**

---

**PYQ 3 (HWR with transformer — numerical).** *A half-wave rectifier is supplied from 220 V, 50 Hz mains through a step-down transformer of turns ratio 10:1. Assuming an ideal diode, the DC output voltage is approximately:*
(a) 22 V (b) 9.9 V (c) 31.1 V (d) 14 V

**Solution:** Secondary RMS = 220/10 = 22 V → V_m = 22√2 = 31.11 V.
V_dc = V_m/π = 31.11/3.1416 ≈ **9.9 V**. **Answer: (b)**
(Trap options: 22 V is the RMS, 31.1 V is the peak, 14 V ≈ 0.636×22 is the *full-wave* value.)

---

**PYQ 4 (Bridge vs centre-tap).** *Which of the following is NOT an advantage of the bridge rectifier over the centre-tapped full-wave rectifier?*
(a) No centre-tapped transformer is required
(b) PIV rating required per diode is half
(c) Higher transformer utilisation factor
(d) Only one diode drop occurs in the conduction path

**Solution:** In a bridge, **two** diodes conduct in series each half-cycle (≈ 1.4 V total drop); the centre-tap circuit has only one. So (d) is false — it is actually a *disadvantage*. (a), (b), (c) are genuine advantages. **Answer: (d)**

---

**PYQ 5 (Colpitts — incorrect statement).** *Which statement about the Colpitts oscillator is INCORRECT?*
(a) It uses a capacitive voltage divider for feedback
(b) Its frequency is f = 1/(2π√(LC_eq)) with C_eq = C₁C₂/(C₁+C₂)
(c) It uses a tapped inductor for feedback
(d) It is an LC (tuned) oscillator suitable for RF generation

**Solution:** The tapped-**inductor** feedback belongs to the **Hartley** oscillator; Colpitts uses the tapped-**capacitor** pair C₁–C₂. Mnemonic: **C**olpitts–**C**apacitor, **H**artley–**H**enry. **Answer: (c)**

---

**PYQ 6 (n-type majority carriers).** *In an n-type semiconductor, the majority charge carriers are:*
(a) Holes (b) **Electrons** (c) Protons (d) Negative ions

**Solution:** Pentavalent donor atoms (P, As, Sb) contribute one free electron each → electrons are majority carriers, holes minority. The crystal remains electrically neutral. **Answer: (b)**

---

**PYQ 7 (Ideal diode, V(t) = sin²t + cos²t).** *An ideal diode is connected in series with a 1 kΩ load across a source V(t) = sin²t + cos²t volts. The current through the load is:*
(a) Zero (b) 1 mA DC (c) 1 mA AC at 1 rad/s (d) 0.5 mA pulsating

**Solution:** Trigonometric identity: sin²t + cos²t = **1** for all t → the source is a pure **1 V DC** supply. The ideal diode (zero drop) is forward biased permanently, so I = 1 V / 1 kΩ = **1 mA steady DC**; output voltage across the load = 1 V DC. **Answer: (b)**
*Lesson: RRB hides a mathematics identity inside an electronics question — always simplify the source expression first.*

---

**PYQ 8 (Oscillator — false statement).** *Which statement about oscillators is FALSE?*
(a) The Barkhausen criterion requires |Aβ| = 1 and total loop phase shift of 0° or 360°
(b) An oscillator needs an external AC input signal to sustain its output
(c) Oscillations start from internal noise or the switching transient
(d) If |Aβ| < 1, the oscillations die out

**Solution:** An oscillator is precisely a circuit that generates AC **without** any external input — positive feedback recycles a fraction of the output as its own input, with internal noise providing the seed. Statement (b) is false; (a), (c), (d) are correct. **Answer: (b)**

---

## 2.15 Practice MCQs (30)

**Q1.** The forbidden energy gap of silicon at room temperature is about:
(a) 0.3 eV (b) 0.72 eV (c) 1.1 eV (d) 6 eV

**Q2.** The barrier potential of a germanium PN junction at 25 °C is approximately:
(a) 0.7 V (b) 0.3 V (c) 1.1 V (d) 0.1 V

**Q3.** With every 10 °C rise in temperature, the reverse saturation current of a diode:
(a) halves (b) doubles (c) stays constant (d) becomes zero

**Q4.** In a p-type semiconductor, the Fermi level lies:
(a) closer to the conduction band (b) closer to the valence band (c) exactly at mid-gap (d) inside the conduction band

**Q5.** Zener breakdown (as distinct from avalanche) occurs in diodes that are:
(a) lightly doped (b) heavily doped with thin depletion layers (c) undoped (d) metal–semiconductor junctions

**Q6.** A varactor diode is operated in:
(a) forward bias (b) reverse bias (c) breakdown (d) zero bias only

**Q7.** The negative-resistance region in a tunnel diode lies between:
(a) zero and peak point (b) peak and valley points (c) valley point and infinity (d) it has no such region

**Q8.** The ripple factor of an ideal full-wave rectifier is:
(a) 1.21 (b) 0.482 (c) 0.812 (d) 1.11

**Q9.** For a half-wave rectifier with peak input V_m, the PIV rating of the diode must be at least:
(a) V_m/2 (b) V_m (c) 2V_m (d) πV_m

**Q10.** The lowest ripple frequency at the output of a bridge rectifier on 50 Hz mains is:
(a) 25 Hz (b) 50 Hz (c) 100 Hz (d) 150 Hz

**Q11.** A shunt-capacitor filter gives the best performance when:
(a) load current is large (b) load current is small (c) frequency is very low (d) capacitor is very small

**Q12.** A clamper circuit changes the:
(a) peak-to-peak value (b) waveshape (c) DC level of the waveform (d) frequency

**Q13.** In a BJT, the emitter region compared to base and collector is:
(a) most lightly doped (b) most heavily doped (c) largest in area (d) thinnest

**Q14.** If α = 0.99, β equals:
(a) 9 (b) 49 (c) 99 (d) 100

**Q15.** The configuration with voltage gain less than unity but highest input impedance is:
(a) CB (b) CE (c) CC (d) all equal

**Q16.** For a transistor used as an amplifier, the junction bias condition is:
(a) both junctions forward (b) both reverse (c) EB forward, CB reverse (d) EB reverse, CB forward

**Q17.** The stability factor of a fixed-bias circuit is:
(a) 1 (b) 1 + β (c) 1/(1+β) (d) β

**Q18.** In a voltage-divider-biased amplifier, the emitter bypass capacitor is used to:
(a) increase DC stability (b) prevent AC degeneration and restore gain (c) block collector DC (d) reduce input impedance

**Q19.** The device with the highest input impedance among these is:
(a) BJT-CE (b) JFET (c) MOSFET (d) BJT-CB

**Q20.** Shockley's equation I_D = I_DSS(1 − V_GS/V_P)² applies to:
(a) BJT (b) JFET (c) SCR (d) UJT

**Q21.** Maximum theoretical efficiency of a class-B push-pull amplifier is:
(a) 25 % (b) 50 % (c) 78.5 % (d) 100 %

**Q22.** Crossover distortion is associated with class:
(a) A (b) B (c) C (d) AB

**Q23.** Negative feedback in an amplifier:
(a) increases gain and decreases bandwidth (b) decreases gain and increases bandwidth (c) increases both (d) decreases both

**Q24.** An RC phase-shift oscillator using three identical RC sections needs each section to provide a phase shift of:
(a) 30° (b) 45° (c) 60° (d) 90°

**Q25.** The minimum amplifier gain required for a Wien bridge oscillator is:
(a) 1 (b) 3 (c) 29 (d) 10

**Q26.** The oscillator with the best frequency stability is:
(a) Hartley (b) Colpitts (c) RC phase-shift (d) crystal

**Q27.** A monostable multivibrator has:
(a) no stable state (b) one stable state (c) two stable states (d) three stable states

**Q28.** An SCR is a:
(a) 2-layer, 1-junction device (b) 3-layer, 2-junction device (c) 4-layer, 3-junction device (d) 5-layer, 4-junction device

**Q29.** The relation between latching current I_L and holding current I_H of an SCR is:
(a) I_L = I_H (b) I_L < I_H (c) I_L > I_H (d) unrelated

**Q30.** In an online (double-conversion) UPS, the transfer time on mains failure is:
(a) 10 ms (b) 4 ms (c) 25 ms (d) zero

### Answer Key with one-line explanations

| Q | Ans | One-line reason |
|---|---|---|
| 1 | c | Si Eg ≈ 1.1 eV (Ge 0.72 eV, diamond ≈ 6 eV) |
| 2 | b | Ge barrier ≈ 0.3 V; Si ≈ 0.7 V |
| 3 | b | I₀ doubles per 10 °C rise (minority-carrier generation) |
| 4 | b | Acceptor level/holes pull the Fermi level toward the valence band |
| 5 | b | Heavy doping → thin depletion → field tunnelling (Zener), V_Z < ~5–6 V |
| 6 | b | Reverse bias varies depletion width → voltage-variable capacitance |
| 7 | b | Current falls from peak (~65 mV) to valley → negative resistance |
| 8 | b | γ(FW) = √(1.11² − 1) = 0.482; 1.21 is half-wave |
| 9 | b | HWR diode blocks only the peak V_m; 2V_m applies to centre-tap FWR |
| 10 | c | Full-wave ripple frequency = 2f = 100 Hz |
| 11 | b | γ = 1/(4√3 fCR_L): small I_dc (large R_L) → low ripple |
| 12 | c | Clamper shifts the DC level; shape and p-p value unchanged |
| 13 | b | Emitter is doped heaviest to inject carriers efficiently |
| 14 | c | β = α/(1−α) = 0.99/0.01 = 99 |
| 15 | c | CC (emitter follower): A_v < 1, very high Z_in — buffer |
| 16 | c | Active region: EB forward, CB reverse |
| 17 | b | Fixed bias: S = 1 + β — the worst stability |
| 18 | b | Bypassing R_E removes AC negative feedback → full gain, DC stability kept |
| 19 | c | MOSFET's insulated gate: 10¹⁰–10¹⁵ Ω |
| 20 | b | JFET square-law transfer characteristic |
| 21 | c | η_max(class B) = π/4 = 78.5 % |
| 22 | b | Class B dead zone near ±0.7 V; class AB cures it |
| 23 | b | A_f = A/(1+Aβ); BW multiplies by (1+Aβ) — G×BW constant |
| 24 | c | 3 × 60° = 180° from network + 180° from CE amplifier = 360° |
| 25 | b | Lead–lag network attenuates by 3 → gain ≥ 3 |
| 26 | d | Quartz Q ~10⁴–10⁶ → ppm-level stability |
| 27 | b | Monostable = one-shot: one stable + one quasi-stable state |
| 28 | c | SCR = PNPN: 4 layers, 3 junctions, 3 terminals |
| 29 | c | I_L (to latch ON) ≈ 2–3 × I_H (to stay ON) |
| 30 | d | Inverter is always in the load path → zero-break transfer |

---

## 2.16 Rapid-Revision Formula Sheet

### Semiconductors & diode
- Mass action: n·p = nᵢ²  σ = e(nµₙ + pµₚ)  Einstein: D/µ = V_T = kT/e ≈ **26 mV @ 300 K**
- Diode: I = I₀(e^(V/ηV_T) − 1); r_d = ηV_T/I ≈ 26 mV/I(mA)
- Barrier: Si 0.7 V, Ge 0.3 V; falls ≈ 2 mV/°C; I₀ doubles per 10 °C
- Zener breakdown: heavy doping, V_Z < 5–6 V, −ve temp-coeff; Avalanche: light doping, V_Z > 6 V, +ve temp-coeff
- LED wavelength: λ(nm) = 1240/Eg(eV)

### Rectifiers (V_m = peak input)
| | HW | FW-CT | Bridge |
|---|---|---|---|
| V_dc | V_m/π (0.318V_m) | 2V_m/π (0.636V_m) | 2V_m/π |
| I_rms | I_m/2 | I_m/√2 | I_m/√2 |
| FF | 1.57 | 1.11 | 1.11 |
| γ | 1.21 | 0.482 | 0.482 |
| η_max | 40.6 % | 81.2 % | 81.2 % |
| PIV | V_m | 2V_m | V_m |
| TUF | 0.287 | 0.693 | 0.812 |
| f_ripple | f | 2f | 2f |

- η(HW) = 0.406/(1 + r_f/R_L); η(FW) = 0.812/(1 + r_f/R_L)
- γ = √(FF² − 1); C-filter: γ = 1/(4√3 fCR_L) (FW); V_r(pp) = I_dc/(2fC) (FW)

### BJT
- **I_E = I_C + I_B**; α = I_C/I_E; β = I_C/I_B; γ = 1 + β
- **β = α/(1−α); α = β/(1+β)**; I_CEO = (1+β)I_CBO
- Load line: V_CE = V_CC − I_C(R_C + R_E); I_C(sat) = V_CC/(R_C+R_E)
- r_e′ = 26 mV/I_E(mA); CE gain A_v = −(R_C ∥ R_L)/r_e′
- Stability: fixed bias S = 1+β (worst); voltage-divider S ≈ 1 + R_B/R_E (best)

### FET
- I_D = I_DSS(1 − V_GS/V_P)²; g_m = g_m0(1 − V_GS/V_P); g_m0 = 2I_DSS/|V_P|; µ = g_m r_d

### Amplifier classes
- A: 25 % (50 % transformer) — 360°; B: **78.5 %** — 180°; AB: between; C: > 90 % — < 180°
- Feedback: A_f = A/(1+Aβ); BW_f = (1+Aβ)BW; distortion ÷ (1+Aβ)

### Oscillators
- Barkhausen: |Aβ| = 1, phase = 0°/360°
- RC phase-shift: f = 1/(2πRC√6), gain ≥ 29
- Wien: f = 1/(2πRC), gain ≥ 3
- Hartley: f = 1/(2π√((L₁+L₂+2M)C)) — tapped inductor
- Colpitts: f = 1/(2π√(L·C₁C₂/(C₁+C₂))) — tapped capacitor
- Clapp: f ≈ 1/(2π√(LC₃)), C₃ smallest
- Crystal: f_s = 1/(2π√(LC)); inductive between f_s and f_p; Q ~ 10⁴–10⁶

### Multivibrators / UJT / SCR
- Astable (BJT): T = 0.693(R₁C₁ + R₂C₂); symmetric T = 1.386RC
- Monostable: T = 0.693RC; n flip-flops → MOD 2ⁿ counter (÷2 per FF)
- UJT: V_P = ηV_BB + 0.7; T = RC ln[1/(1−η)]; η = R_B1/(R_B1+R_B2) ≈ 0.5–0.8
- SCR: I_A = I_leak/[1 − (α₁+α₂)]; latches when α₁+α₂ → 1; I_L > I_H

### Triode
- **µ = g_m × r_p**; gain A = µR_L/(r_p + R_L); Child's law I_P ∝ V_P^(3/2)

### Inverter / UPS
- Square-wave fundamental (full-bridge): V₁(rms) = 0.9 V_dc; odd harmonics only
- UPS transfer times: offline 4–10 ms > line-interactive 2–4 ms > **online 0 ms**
- Battery Ah = (W × hours)/(V_batt × η_inv × DoD); Watts = VA × pf

---

*End of Chapter 2. Next: Chapter 3 — Digital Electronics.*
