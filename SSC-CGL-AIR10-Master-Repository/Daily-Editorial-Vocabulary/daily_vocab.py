#!/usr/bin/env python3
"""
Daily Editorial Vocabulary Generator
====================================

Generates 50 vocabulary words a day (word + part of speech + simple meaning +
easy synonym + newspaper-style example), saved as a dated Markdown file under
Daily-Words/.

Word sources (in priority order, with graceful fallback when offline):
  1. EDITORIALS  -> scrape today's national + international newspaper editorial
                    headlines/op-eds via RSS, pull out the "tough" words.
  2. AI (Claude) -> if ANTHROPIC_API_KEY is set, generate fresh editorial-style
                    words with meanings + examples.
  3. WORD BANK   -> a large curated offline SSC/UPSC word bank (word_bank.json).
                    Always works, even with no internet.

The script DEDUPES against every word it has produced before (tracked in
used_words.json), so each day's 50 words are new until the bank is exhausted,
then it recycles oldest-first.

Run it once a day. Designed to be registered with Windows Task Scheduler
(see setup_task_scheduler.ps1).

Author: built for the SSC-CGL master repository.
"""

import os
import re
import sys
import json
import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
WORDS_PER_DAY = 50

BASE_DIR = Path(__file__).resolve().parent
WORD_BANK_FILE = BASE_DIR / "word_bank.json"
USED_WORDS_FILE = BASE_DIR / "used_words.json"
OUTPUT_DIR = BASE_DIR / "Daily-Words"
LOG_FILE = BASE_DIR / "run.log"

# National (Indian) + international editorial RSS feeds.
# Only headlines/summaries are read to MINE difficult words; full articles are
# never reproduced (copyright-safe).
EDITORIAL_FEEDS = [
    # National (India)
    "https://www.thehindu.com/opinion/editorial/feeder/default.rss",
    "https://www.thehindu.com/opinion/op-ed/feeder/default.rss",
    "https://indianexpress.com/section/opinion/editorials/feed/",
    "https://indianexpress.com/section/opinion/feed/",
    # International
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.theguardian.com/uk/commentisfree/rss",
    "https://rss.nytimes.com/services/xml/rss/nyt/Opinion.xml",
    "http://feeds.reuters.com/reuters/topNews",
]

# A small fallback meaning lookup is NOT attempted online for scraped words
# unless the AI source is available; scraped words without a known meaning are
# only used if Claude can define them. Otherwise we rely on the curated bank.

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
def log(msg: str) -> None:
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Persistence helpers
# ---------------------------------------------------------------------------
def load_json(path: Path, default):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def save_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Source 3: curated word bank (always available)
# ---------------------------------------------------------------------------
def load_word_bank():
    data = load_json(WORD_BANK_FILE, {"words": []})
    words = data.get("words", [])
    # Normalise display word (strip helper suffixes like "Quell2")
    cleaned = []
    seen = set()
    for w in words:
        word = re.sub(r"\d+$", "", w.get("word", "")).strip()
        if not word:
            continue
        key = word.lower()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append({
            "word": word,
            "pos": w.get("pos", ""),
            "meaning": w.get("meaning", ""),
            "easy": w.get("easy", ""),
            "example": w.get("example", ""),
            "source": "Curated word bank",
        })
    return cleaned


# ---------------------------------------------------------------------------
# Source 1: editorial scraping (mines difficult words from today's feeds)
# ---------------------------------------------------------------------------
COMMON_WORDS = set("""
the a an and or but if then else for to of in on at by with from into over under
is are was were be been being have has had do does did will would shall should can
could may might must this that these those it its their his her your our my you he
she they we who whom which what when where why how not no yes as so than too very
more most some any all both each few many much other another such only own same up
down out off again further once here there about against between through during after
before above below new news say said says world year years day days time people
government india indian us said new said will say also said may amid set get got make
made one two three first second new
""".split())


def fetch_editorial_words(limit=120):
    """Return candidate 'difficult' words mined from editorial feeds."""
    try:
        import feedparser  # noqa
    except ImportError:
        log("feedparser not installed; skipping editorial source.")
        return []

    candidates = {}
    for url in EDITORIAL_FEEDS:
        try:
            feed = feedparser.parse(url)
            if getattr(feed, "bozo", 0) and not feed.entries:
                continue
            for entry in feed.entries[:25]:
                text = " ".join(filter(None, [
                    entry.get("title", ""),
                    entry.get("summary", ""),
                ]))
                for raw in re.findall(r"[A-Za-z][A-Za-z'-]{6,}", text):
                    w = raw.lower().strip("'-")
                    if len(w) < 7 or w in COMMON_WORDS:
                        continue
                    candidates[w] = candidates.get(w, 0) + 1
        except Exception as exc:  # network / parse issues -> skip feed
            log(f"Feed failed ({url.split('/')[2]}): {exc}")
            continue

    # Prefer words that appear across multiple editorials (more "editorial-y")
    ranked = sorted(candidates.items(), key=lambda kv: (-kv[1], kv[0]))
    words = [w.capitalize() for w, _ in ranked[:limit]]
    if words:
        log(f"Editorial source mined {len(words)} candidate words.")
    return words


# ---------------------------------------------------------------------------
# Source 2: Claude API (defines scraped words OR generates fresh ones)
# ---------------------------------------------------------------------------
def claude_define(words):
    """Given a list of words, ask Claude for meaning/pos/easy/example.
    Returns list of entry dicts. Empty list if API unavailable."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or not words:
        return []
    try:
        import anthropic
    except ImportError:
        log("anthropic SDK not installed; skipping AI source. "
            "(pip install anthropic to enable)")
        return []

    client = anthropic.Anthropic(api_key=api_key)
    word_list = ", ".join(words[:WORDS_PER_DAY])
    prompt = (
        "You are building SSC-CGL / UPSC editorial vocabulary flashcards for a "
        "beginner. For each word below, give a JSON object with keys: "
        "word, pos (part of speech), meaning (very simple, <12 words), "
        "easy (1-3 easy synonyms), example (one newspaper-style sentence). "
        "Skip proper nouns, names, and non-English words. "
        "Return ONLY a JSON array, no prose.\n\nWords: " + word_list
    )
    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = msg.content[0].text.strip()
        text = re.sub(r"^```(json)?|```$", "", text, flags=re.MULTILINE).strip()
        arr = json.loads(text)
        entries = []
        for e in arr:
            if all(k in e for k in ("word", "meaning", "example")):
                e["source"] = "Today's editorials (AI-defined)"
                e.setdefault("pos", "")
                e.setdefault("easy", "")
                entries.append(e)
        if entries:
            log(f"AI source defined {len(entries)} editorial words.")
        return entries
    except Exception as exc:
        log(f"Claude API call failed: {exc}")
        return []


# ---------------------------------------------------------------------------
# Selection logic: combine sources, dedupe, pick 50
# ---------------------------------------------------------------------------
def pick_words():
    used = set(w.lower() for w in load_json(USED_WORDS_FILE, []))
    selected = []
    chosen_keys = set()

    def add(entry):
        key = entry["word"].lower()
        if key in chosen_keys or key in used:
            return
        if not entry.get("meaning") or not entry.get("example"):
            return
        chosen_keys.add(key)
        selected.append(entry)

    # 1 + 2) Editorials (mined) defined by AI, if available
    mined = fetch_editorial_words()
    fresh_mined = [w for w in mined if w.lower() not in used]
    for entry in claude_define(fresh_mined):
        if len(selected) >= WORDS_PER_DAY:
            break
        add(entry)

    # 3) Curated word bank fills the rest
    bank = load_word_bank()
    for entry in bank:
        if len(selected) >= WORDS_PER_DAY:
            break
        add(entry)

    # If we've exhausted everything new, recycle oldest-used bank words
    if len(selected) < WORDS_PER_DAY:
        log("New words exhausted; recycling from word bank (oldest first).")
        for entry in bank:
            if len(selected) >= WORDS_PER_DAY:
                break
            if entry["word"].lower() not in chosen_keys:
                chosen_keys.add(entry["word"].lower())
                selected.append(entry)

    return selected[:WORDS_PER_DAY]


# ---------------------------------------------------------------------------
# Output: write the dated Markdown file
# ---------------------------------------------------------------------------
def write_markdown(entries, day):
    nice_date = day.strftime("%d %B %Y (%A)")
    fname = OUTPUT_DIR / f"{day.strftime('%Y-%m-%d')}_Editorial_Vocabulary.md"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Daily Editorial Vocabulary — {nice_date}",
        "",
        f"> **{len(entries)} words today.** Each: **Word** *(part of speech)* — "
        "simple meaning · **easy word:** synonym, followed by a newspaper-style "
        "sentence.",
        "",
        "**How to use:** read each meaning and sentence out loud, cover the "
        "meaning, and try to recall it. Revise yesterday's file before starting.",
        "",
        "---",
        "",
    ]
    for i, e in enumerate(entries, 1):
        pos = f" *({e['pos']})*" if e.get("pos") else ""
        easy = f" · **easy word:** {e['easy']}" if e.get("easy") else ""
        lines.append(f"**{i}. {e['word']}**{pos} — {e['meaning']}{easy}")
        lines.append(f"> *{e['example']}*")
        lines.append("")

    # Sources footer
    srcs = sorted({e.get("source", "Curated word bank") for e in entries})
    lines += ["---", "", "**Sources:** " + "; ".join(srcs) + ".", ""]

    with open(fname, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    return fname


def update_index():
    """Rebuild a README index of all daily files, newest first."""
    files = sorted(OUTPUT_DIR.glob("*_Editorial_Vocabulary.md"), reverse=True)
    lines = [
        "# Daily Editorial Vocabulary — Index",
        "",
        "Auto-generated 50 words a day, mined from national + international "
        "newspaper editorials with a curated SSC/UPSC fallback bank.",
        "",
        f"**Total days generated:** {len(files)}",
        "",
        "| Date | File |",
        "| --- | --- |",
    ]
    for f in files:
        date = f.name.split("_")[0]
        lines.append(f"| {date} | [{f.name}](Daily-Words/{f.name}) |")
    with open(BASE_DIR / "README.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    log("=== Daily vocab run started ===")
    today = datetime.date.today()

    out_file = OUTPUT_DIR / f"{today.strftime('%Y-%m-%d')}_Editorial_Vocabulary.md"
    if out_file.exists() and "--force" not in sys.argv:
        log(f"Already generated for {today}: {out_file.name}. Use --force to redo.")
        return

    entries = pick_words()
    if not entries:
        log("ERROR: no words could be selected. Check word_bank.json.")
        sys.exit(1)

    fname = write_markdown(entries, today)
    log(f"Wrote {len(entries)} words -> {fname.name}")

    # Mark words used (append, keep order = oldest first)
    used = load_json(USED_WORDS_FILE, [])
    used.extend(e["word"] for e in entries)
    save_json(USED_WORDS_FILE, used)

    update_index()
    log("=== Daily vocab run finished ===")


if __name__ == "__main__":
    main()
