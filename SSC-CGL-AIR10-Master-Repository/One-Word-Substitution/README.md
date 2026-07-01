# One-Word Substitution — Daily Builder

A single, self-contained HTML file of **One-Word Substitutions** (phrase → one word),
seeded from the **SSC-CGL PYQ papers** and curated word banks, grouped by theme,
deduped, and **updated daily** from newspapers, articles, speeches & books.
**Today's newly-added words are highlighted** 🆕.

👉 **[Open One_Word_Substitution.html »](One_Word_Substitution.html)** in a browser —
the Contents links jump to each theme; new rows are shaded yellow with a 🆕 badge.

## Files

| File | Purpose |
| --- | --- |
| `One_Word_Substitution.html` | **The single master file** (open this) |
| `ows_store.json` | Canonical deduped entries (the data) |
| `new_today.json` | Drop-box for today's new additions (see below) |
| `ows_daily.py` | Builder / daily merger |
| `run.log` | Run history |

## How to add today's words (from newspapers, articles, speeches, books)

1. Edit **`new_today.json`** — a list of objects:

   ```json
   [
     {"word": "Quixotic", "phrase": "Exceedingly idealistic and impractical",
      "meaning": "from Don Quixote; unrealistic", "source": "Editorial (The Hindu)"},
     {"word": "Sycophant", "phrase": "One who flatters the powerful for gain",
      "meaning": "a flatterer", "source": "Speech"}
   ]
   ```

2. Run:

   ```bash
   py ows_daily.py
   ```

   New, non-duplicate words are merged, **stamped with today's date, highlighted**
   in the HTML, and the drop-box is cleared. Duplicates are skipped automatically.

3. Just rebuild the HTML (no new words):

   ```bash
   py ows_daily.py --rebuild
   ```

## Source of the seed

Extracted from (deduped, in priority order):
- `English/03_One_Word_Substitution.md`
- `Practice-Sets-500/English_03_OneWord_Idioms_500.md` (PYQ-style 250 OWS)
- `Cheat-Sheets/SSC-CGL-Vocabulary-Master-Handbook.md` (Chapter 6)

Scope per the [official syllabus](../SSC-CGL-2026-Official-Syllabus.md): One-word
substitution is an explicit English topic (Tier-I English & Tier-II Paper-I, Para 13.11.3).
