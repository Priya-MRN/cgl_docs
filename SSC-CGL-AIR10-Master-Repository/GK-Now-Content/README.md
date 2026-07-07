# GK Now — Content Directory

Study content compiled and improvised from the category structure of **[gknow.in](https://gknow.in)**, organised for SSC CGL / competitive-exam preparation. Each file contains **revision notes + sample MCQs** for its category.

> ⚠️ Content is improvised/summarised for study use. Current-affairs items reflect the source as of mid-2026 — verify dates and figures against primary sources before relying on them in an exam.

## Structure

```
GK-Now-Content/
├── README.md                       ← this index
├── Current-Affairs/                ← Daily/monthly CA, sub-category wise
│   ├── 01_Appointments.md
│   ├── 02_Awards_and_Honours.md
│   ├── 03_Government_Schemes.md
│   ├── 04_Science_and_Technology.md
│   ├── 05_Economy.md
│   ├── 08_National.md
│   ├── 09_Polity.md
│   ├── 11_States.md
│   └── 13_Books_and_Authors.md
├── GK-Topics/                      ← Static GK MCQ topics
│   ├── 01_History.md
│   ├── 02_Geography.md
│   ├── 03_Polity_Constitution.md
│   ├── 04_Economy.md
│   └── 05_General_Science.md
└── State-GK/                       ← State-wise GK
    ├── Uttarakhand.md
    └── Bihar.md
```

## Category Map (from gknow.in)

| Group | Categories Covered |
|-------|-------------------|
| **Current Affairs** | Appointments · Awards & Honours · Art & Culture · Books & Authors · Economy · Environment · Government Schemes · Important Days · International · National · Polity · Science & Technology · Sports · States |
| **GK MCQ (Topic-wise)** | History (Ancient/Medieval/Modern/World) · Geography (Indian/World) · Polity & Constitution · Economy · Science (Bio/Chem/Physics) · Art & Culture · Sports · Environment · Awards · Books & Authors · Important Days |
| **State-wise GK** | Uttarakhand · Bihar · Haryana · UP |

## 📖 Daily Combined Digest (auto-updated)

The eight Current-Affairs categories are merged into **one** mobile-friendly PDF —
curated revision notes + MCQs on top, then the **latest headlines & descriptions
scraped daily from [gknow.in](https://gknow.in)** underneath each category, with a
by-date coverage index at the end.

👉 **[Open the combined GK digest (PDF) »](GK-Current-Affairs-Digest.pdf)** — rebuilt & auto-pushed every day.

- Builder: `daily_gk_digest.py` (scrape + merge + render + git push).
- Schedule it: run `setup_gk_digest_task.ps1` once (Windows Task Scheduler, daily 07:15).
- Manual run: `py daily_gk_digest.py` · rebuild-only: `--rebuild` · skip push: `--no-push`.

## How to Use

1. **Current Affairs** — skim daily; revise sub-category files weekly.
2. **GK Topics** — attempt the MCQs first, then read the notes to fill gaps.
3. **State GK** — relevant for state-level exams and a few SSC GA questions.

_Important Days, Organizations & Books/Authors now live in [Static-GK/Current-Affairs-Special-Master.pdf](../Static-GK/Current-Affairs-Special-Master.pdf); Art & Culture in [Static-GK/Art-Culture-Master.pdf](../Static-GK/Art-Culture-Master.pdf)._
