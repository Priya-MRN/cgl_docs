# 🧠 Subject Flowchart Memory Maps — SSC CGL 2026

Five self-contained, print-ready PDF study pages that turn each GS subject into
**flowcharts, trees, comparison tables and mnemonics** — designed so a topic
*registers in one glance* instead of being read as a wall of text.
(PDFs render reliably on GitHub mobile; they're rebuilt automatically each day
by `subject_daily.py`.)

Every topic carries a **colour-tier priority badge** so you always know what to
do first:

| Badge | Meaning |
|-------|---------|
| 🔴 **P1** | High-yield — learn first (repeats almost every year) |
| 🟠 **P2** | Medium priority |
| 🟢 **P3** | Low / rare — polish at the end |

> Priority reflects SSC repeat-frequency, **not** official marks weightage.

---

## 📚 The five pages

| # | Page | Covers | Open |
|---|------|--------|------|
| 01 | **History** | Timeline · Buddhism/Jainism · Mauryan · Gupta · Bhakti/Sufi · Mughal admin · Freedom Movement · Acts | [01_History-Flowchart.pdf](01_History-Flowchart.pdf) |
| 02 | **Geography** | Rivers & tributaries · Ports · National Parks & animals · Mountains · Soils · Climate | [02_Geography-Flowchart.pdf](02_Geography-Flowchart.pdf) |
| 03 | **Polity** | Fundamental Rights/Duties · DPSP · Parliament · President/PM · Amendments (42,44,73,74,86) · Borrowed features | [03_Polity-Flowchart.pdf](03_Polity-Flowchart.pdf) |
| 04 | **Science** | Physics (motion, sound, light, electricity) · Chemistry (acids/bases, metals) · Biology (human body, vitamins, diseases) | [04_Science-Flowchart.pdf](04_Science-Flowchart.pdf) |
| 05 | **Current Affairs** | Awards · Schemes · Sports · Important Days · Intl Orgs **+ daily auto-fed headlines** | [05_Current-Affairs-Flowchart.pdf](05_Current-Affairs-Flowchart.pdf) |

Each page ends with a **⚡ Rapid Revision** table (30+ one-line Q→A) — your
last-5-minutes-before-exam sheet.

---

## 📅 Daily update — keep the pages alive

Run once a day (or via Task Scheduler). It:

1. **Stamps today's date** into every page's top banner.
2. **Rotates a "focus of the day"** — a different anchor each day (deterministic
   by day-of-year, so spaced revision is even). Open any page and it points you
   at what to revise today.
3. **Mines today's Current-Affairs headlines** from GKToday, sorts them into the
   5 buckets (Awards / Schemes / Sports / Days / Orgs) and lists them at the top
   of the CA page — **headlines + source link only** (copyright-safe), today's
   highlighted 🆕.

```bat
:: full run (stamp date + rotate focus + mine CA news)
run_daily.bat

:: offline — just stamp the date & rotate the focus, no network
run_daily.bat --no-news

:: rebuild the CA feed from the stored JSON without re-scraping
py subject_daily.py --rebuild
```

Files created/used by the updater:
- `subject_daily.py` — the updater
- `run_daily.bat` — launcher (edit the Python path if yours differs)
- `ca_news_store.json` — the growing store of mined CA headlines
- `run.log` — run history

### Schedule it (optional)
Add to Windows Task Scheduler (daily, e.g. 7 AM):
```
Program:   d:\Documents\cgl_docs\SSC-CGL-AIR10-Master-Repository\Subject-Flowcharts\run_daily.bat
Start in:  d:\Documents\cgl_docs\SSC-CGL-AIR10-Master-Repository\Subject-Flowcharts
```
(Your existing `setup_daily_tasks.ps1` in the repo root is the pattern to follow.)

---

## 🎯 How to study these

1. **Open on the P1 blocks first** — the flowcharts and mnemonics are the anchors.
2. **Trace the trees with your finger** (Ganga → tributaries, Babur → Aurangzeb).
   The spatial layout is the memory hook.
3. **Say the mnemonic aloud** (🧠 boxes) — that's what sticks under exam pressure.
4. **End every session on the ⚡ Rapid Revision table.**
5. Let the **daily focus** decide your warm-up topic so nothing goes stale.

All pages work **offline** and **print cleanly** (nav & buttons hidden in print).
