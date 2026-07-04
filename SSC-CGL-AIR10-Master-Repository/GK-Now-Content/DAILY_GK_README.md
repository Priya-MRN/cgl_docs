# Daily GK / Current Affairs — Auto-updated from GKToday

A single, self-contained PDF of **current-affairs headlines mined daily from
[GKToday](https://www.gktoday.in/)**, grouped by topic, deduped, with **today's new
items highlighted** 🆕. (Rebuilt as a mobile-friendly PDF each run — GitHub shows it
correctly on phones.)

👉 **[Open Daily_GK_Current_Affairs.pdf »](Daily_GK_Current_Affairs.pdf)** —
grouped by topic; click any headline to read the full article on GKToday.

> ⚠️ **Copyright-safe:** only **headlines + the source link** are stored — never article
> bodies. Every item links back to GKToday.

## Files

| File | Purpose |
| --- | --- |
| `Daily_GK_Current_Affairs.pdf` | **The single master file** (open this) — rebuilt each run |
| `gk_store.json` | Deduped headline store (title, url, category, date) |
| `gk_new_today.json` | Optional drop-box for manual additions (newspapers/notes) |
| `gk_daily.py` | Scraper / daily builder |
| `run.log` | Run history |

## Daily use

```bash
py gk_daily.py            # scrape GKToday + merge + rebuild PDF
py gk_daily.py --rebuild  # just rebuild PDF from the store (no fetch)
```

New, non-duplicate headlines are merged, **stamped with today's date, highlighted**,
and the page is rewritten. Run it once a day (or schedule it like the vocab task).

### Add items from other sources (optional)

Drop extra items into `gk_new_today.json` before running:

```json
[
  {"title": "RBI keeps repo rate unchanged at 6.0%", "url": "", "category": "💰 Economy & Banking"}
]
```

`category` is optional — if omitted, it's auto-detected from the title.

## Topics

Headlines are auto-bucketed into: Awards & Honours · Appointments · Defence & Security ·
Economy & Banking · Science & Technology · International · Environment & Ecology ·
Polity & Schemes · Sports · Art, Culture & Days · Other / National.

Scope: SSC CGL **General Awareness** (Tier-I Sec-B / Tier-II Paper-I Sec-II Part-B) —
see the [official syllabus](../SSC-CGL-2026-Official-Syllabus.md).

## Scheduling (optional, like the vocab task)

Register a Windows Scheduled Task to run `py gk_daily.py` once a day — mirror the
setup used in `Daily-Editorial-Vocabulary/setup_task_scheduler.ps1`.
