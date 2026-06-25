# Daily Editorial Vocabulary — Setup & Usage

Automatically generates **50 vocabulary words every day** (word, part of speech,
simple meaning, easy synonym, newspaper-style example) and saves them as a dated
Markdown file in [Daily-Words/](Daily-Words/).

## How it works

Each run pulls words from up to three sources, with automatic fallback:

1. **Editorials (online)** — mines "difficult" words from today's national +
   international newspaper editorial RSS feeds (The Hindu, Indian Express, BBC,
   The Guardian, NYT, Reuters). *Headlines/summaries only — full articles are
   never copied.*
2. **AI (Claude)** — if you set an `ANTHROPIC_API_KEY`, today's mined words are
   defined with meanings + examples by Claude. Without a key, this step is
   skipped.
3. **Curated word bank (offline)** — `word_bank.json`, a hand-built SSC/UPSC
   editorial word list, fills the rest. **Always works, even with no internet.**

Every word produced is recorded in `used_words.json`, so each day's 50 words are
**new** until the bank is exhausted, then it recycles oldest-first.

## It's already set up

A Windows Scheduled Task named **`DailyEditorialVocabulary`** runs the script
**every day at 07:00** whenever the PC is on. Missed runs (PC was off) catch up
automatically at next startup.

Today's file has already been generated:
[Daily-Words/](Daily-Words/).

## Common commands (PowerShell)

```powershell
# Run it right now
Start-ScheduledTask -TaskName "DailyEditorialVocabulary"

# Check when it last ran / next runs (LastTaskResult 0 = success)
Get-ScheduledTaskInfo -TaskName "DailyEditorialVocabulary"

# Change the time (e.g. 6:30 AM)
powershell -ExecutionPolicy Bypass -File .\setup_task_scheduler.ps1 -Time "06:30"

# Remove the schedule
Unregister-ScheduledTask -TaskName "DailyEditorialVocabulary" -Confirm:$false
```

## Run manually any time

```powershell
py daily_vocab.py            # generate today (skips if already done)
py daily_vocab.py --force    # regenerate today's file
```

## Optional: enable AI-defined editorial words

Set an environment variable (one-time) and install the SDK:

```powershell
py -m pip install anthropic
setx ANTHROPIC_API_KEY "sk-ant-..."
```

After that, each day's words will be drawn from the *actual* editorials
published that day and defined automatically.

## Add your own words

Edit `word_bank.json` — append objects to the `words` array with keys
`word`, `pos`, `meaning`, `easy`, `example`. They'll be picked up on the next run.

## Files

| File | Purpose |
| --- | --- |
| `daily_vocab.py` | Main generator |
| `word_bank.json` | Curated offline word bank |
| `used_words.json` | Tracks words already produced (dedupe) |
| `run_daily_vocab.bat` | Launcher used by Task Scheduler |
| `setup_task_scheduler.ps1` | Registers / updates the daily task |
| `run.log` | Run history |
| `Daily-Words/` | Generated dated `.md` files + index |
