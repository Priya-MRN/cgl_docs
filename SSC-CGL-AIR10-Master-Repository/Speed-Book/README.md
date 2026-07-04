# ⚡ SSC CGL Speed Book

Your own growing book of **200–300 high-value SSC tricks**, each in a fixed
**7-part anatomy** so revision is consistent. Output is one self-contained PDF book,
grouped by topic (mobile-friendly on GitHub; rebuilt each time you run the builder).

👉 **[Open Speed-Book.pdf »](Speed-Book.pdf)**
Current count: **20 tricks** — growing toward 200–300.

## The 7-part anatomy (every trick has these)

| Field | Meaning |
| --- | --- |
| `shortcut` | ✅ The SSC shortcut / rule |
| `mental` | 🧮 How to do it in your head |
| `whenUse` | 🔎 When to use it (trigger) |
| `whenNotUse` | 🚫 When NOT to use it |
| `traps` | ⚠️ Common traps examiners exploit |
| `pyq` | 📝 A worked PYQ example (with answer) |
| `fails` | ❌ The case where the shortcut breaks |

## Files

| File | Purpose |
| --- | --- |
| `Speed-Book.pdf` | **The revision book** (open this) — auto-generated from the JSON |
| `speedbook.json` | The trick data (one object per trick) |
| `new_tricks.json` | Drop-box: add new tricks here, then run the builder |
| `speedbook.py` | Generator |
| `run.log` | Run history |

## How to add tricks

Append objects to `speedbook.json` → `tricks` (or drop them in `new_tricks.json`), then:

```bash
py speedbook.py
```

New tricks merge in (duplicate `id`s are skipped), the drop-box is cleared, and the
HTML rebuilds. **Template for one trick:**

```json
{
  "id": "PCT-04",
  "topic": "Percentage",
  "priority": "high",
  "name": "Short descriptive title",
  "shortcut": "The rule in one or two sentences.",
  "mental": "How to compute it mentally, with a tiny example.",
  "whenUse": "The exact trigger conditions.",
  "whenNotUse": "Contexts where it gives the wrong answer.",
  "traps": "What students get wrong.",
  "pyq": "Q: ... → working → Answer: ...",
  "fails": "The edge case that breaks the shortcut."
}
```

- **`id`** = topic prefix + number (PCT, PL, AVG, SICI, TW, TSD, ALG, GEO, TRIG, DI,
  REAS, ENG, GA). Keep it stable.
- **`priority`** `"high"` shows a ★ on the card. Omit for normal.
- **`topic`** controls the section. Section order is set in `TOPIC_ORDER` in `speedbook.py`.

## Topics & target spread (≈200–300 total)

Arithmetic (Percentage, Profit-Loss, Ratio, Average/Mixtures, SI-CI, Time-Work, TSD,
Number System) · Algebra · Geometry & Mensuration · Trigonometry · Data Interpretation ·
Reasoning · English · General Awareness.

Source bank to mine from: [15_Arithmetic_Tricks_Handbook.md](../Quantitative-Aptitude/15_Arithmetic_Tricks_Handbook.md)
and the [ASO Formula sheet](../Formula-Sheets/SSC-CGL-ASO-Formulas-Tricks-Master.md) — upgrade each
to the full 7-part format here. Scope: [official syllabus](../SSC-CGL-2026-Official-Syllabus.md).
