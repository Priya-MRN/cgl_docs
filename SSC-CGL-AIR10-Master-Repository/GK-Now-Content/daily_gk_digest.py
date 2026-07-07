"""
Daily GK Current-Affairs Digest (gknow.in) — 8-category notes, auto-pushed.

Scrapes the per-category RSS feeds of gknow.in for the eight Current-Affairs
categories the user tracks (Appointments, Awards & Honours, Government Schemes,
Economy, National, Polity, States, Books & Authors), pulling each item's
HEADLINE + a short DESCRIPTION + source link (copyright-safe — only the feed's
own summary snippet is stored, never the full article), then:
  1. merges deduped items into gk_digest_store.json (grouped by category, each
     item stamped with the date it was first seen),
  2. renders ONE combined, mobile-friendly PDF (GK-Current-Affairs-Digest.pdf)
     with today's additions highlighted and a "Coverage by date" index at the end,
  3. commits AND pushes the PDF to git automatically.

This is the gknow.in companion to daily_ca_digest.py (which mines gktoday.in
headlines). The two are independent: separate stores, separate PDFs, separate
scheduled tasks.

Run:  py daily_gk_digest.py            (scrape + merge + render + push)
      py daily_gk_digest.py --rebuild  (re-render from the store, no fetch)
      py daily_gk_digest.py --no-push  (skip the git commit/push step)
      py daily_gk_digest.py --force    (merge again even if run already today)
"""
from __future__ import annotations

import re
import sys
import json
import html as _html
import datetime
import subprocess
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REPO_SUBDIR = BASE_DIR.parent                 # SSC-CGL-AIR10-Master-Repository
GIT_ROOT = REPO_SUBDIR.parent                 # D:/Documents/cgl_docs (actual git root)
sys.path.insert(0, str(REPO_SUBDIR))
from md_to_pdf import render as md_render, CSS as MD_CSS   # reuse the MD->HTML renderer
from html_to_pdf import html_to_pdf

STORE = BASE_DIR / "gk_digest_store.json"
MD_OUT = BASE_DIR / "GK-Current-Affairs-Digest.md"    # local working source (gitignored)
PDF_OUT = BASE_DIR / "GK-Current-Affairs-Digest.pdf"  # the committed artifact
LOG = BASE_DIR / "run.log"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# The eight tracked categories, in display order. Each maps to its gknow.in
# category RSS feed and to the curated source-notes file that is merged in at
# the top of that category's section. (Emoji is just for the PDF headings.)
SRC_DIR = BASE_DIR / "Current-Affairs"
CATEGORIES = [
    ("👤 Appointments",
     "https://gknow.in/category/current-affairs/appointments/feed/",
     "01_Appointments.md"),
    ("🏅 Awards & Honours",
     "https://gknow.in/category/current-affairs/awards-and-honors/feed/",
     "02_Awards_and_Honours.md"),
    ("🏛️ Government Schemes",
     "https://gknow.in/category/current-affairs/government-schemes-current-affairs/feed/",
     "03_Government_Schemes.md"),
    ("💰 Economy",
     "https://gknow.in/category/current-affairs/economy-current-affairs/feed/",
     "05_Economy.md"),
    ("📰 National",
     "https://gknow.in/category/current-affairs/national-current-affairs/feed/",
     "08_National.md"),
    ("⚖️ Polity",
     "https://gknow.in/category/current-affairs/polity-current-affairs/feed/",
     "09_Polity.md"),
    ("🗺️ States",
     "https://gknow.in/category/current-affairs/states-current-affairs/feed/",
     "11_States.md"),
    ("📚 Books & Authors",
     "https://gknow.in/category/current-affairs/books-and-authors/feed/",
     "13_Books_and_Authors.md"),
]
CAT_ORDER = [name for name, _, _ in CATEGORIES]
CAT_SRCFILE = {name: src for name, _, src in CATEGORIES}


def curated_notes(src_file):
    """Read a curated Current-Affairs/NN_*.md and return its body demoted for
    embedding: the top-level '# Current Affairs — X' title and the immediate
    '> Source:' line are dropped (the combined doc supplies its own heading),
    and every heading is pushed down two levels so it nests under the category's
    ## section. Returns '' if the file is missing."""
    path = SRC_DIR / src_file
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError:
        return ""
    out = []
    for ln in raw.split("\n"):
        s = ln.strip()
        if s.startswith("# "):                 # drop the file's own H1 title
            continue
        if s.startswith("> Source:"):          # drop the per-file source note
            continue
        m = re.match(r"^(#{1,4})\s+(.*)$", ln)
        if m:                                   # demote headings by two levels
            out.append("#" * min(len(m.group(1)) + 2, 6) + " " + m.group(2))
        else:
            out.append(ln)
    return "\n".join(out).strip()

# Cap items shown per category per day-group so the PDF stays revision-sized.
MAX_PER_CATEGORY = 40
# Description snippet length (chars) — enough to be a useful note, not the article.
DESC_LEN = 240


def log(msg):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] GK-Digest: {msg}"
    try:
        print(line)
    except UnicodeEncodeError:      # console (cp1252) can't render emoji category names
        enc = sys.stdout.encoding or "ascii"
        print(line.encode(enc, "replace").decode(enc, "replace"))
    try:
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


# ---------------------------------------------------------------------------
# Scrape: pull items (title + link + description) from one category feed.
# ---------------------------------------------------------------------------
def _clean(text):
    text = _html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)          # strip any HTML tags
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _decode(raw):
    """Decode a feed body using its declared charset (gknow.in is UTF-8, but the
    header sometimes mis-parses, mangling apostrophes/dashes)."""
    m = re.search(rb'encoding=["\']([\w-]+)["\']', raw[:200])
    enc = (m.group(1).decode("ascii", "ignore") if m else "utf-8") or "utf-8"
    try:
        return raw.decode(enc, "replace")
    except LookupError:
        return raw.decode("utf-8", "replace")


def fetch_category(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=25) as resp:
            page = _decode(resp.read())
    except Exception as exc:
        log(f"feed fetch failed ({url.split('/')[-3]}): {exc}")
        return []
    items = []
    for block in re.findall(r"<item>(.*?)</item>", page, re.S):
        t = re.search(r"<title>(.*?)</title>", block, re.S)
        l = re.search(r"<link>(.*?)</link>", block, re.S)
        d = re.search(r"<description>(.*?)</description>", block, re.S)
        title = _clean(t.group(1)) if t else ""
        link = (l.group(1).strip() if l else "")
        desc = _clean(d.group(1)) if d else ""
        if len(title) < 12 or not link.startswith("http"):
            continue
        # trim the description to a clean sentence-ish snippet
        if len(desc) > DESC_LEN:
            cut = desc[:DESC_LEN].rsplit(" ", 1)[0]
            desc = cut.rstrip(".,;:") + "…"
        items.append({"title": title, "url": link, "desc": desc})
    return items


# ---------------------------------------------------------------------------
# Markdown: today first, earlier dates, then a by-date index (like the CA digest)
# ---------------------------------------------------------------------------
def build_markdown(store, today):
    cats = store.get("categories", {})     # {cat_name: [items]}  (items carry "added")
    days_index = store.get("days", {})     # {date: count}  for the tail index

    md = []
    md.append("# 📖 Daily GK Current-Affairs Digest — SSC CGL")
    md.append("")
    md.append(f"> Auto-generated exam digest from **gknow.in**. "
              f"**Latest update: {today}.** Eight categories: Appointments · "
              "Awards & Honours · Government Schemes · Economy · National · "
              "Polity · States · Books & Authors.")
    md.append("")
    md.append("> ⚠️ Headlines + short descriptions + source links only "
              "(copyright-safe). Click a headline to read the full article at the "
              "source. Verify facts before the exam. 🆕 marks items added today.")
    md.append("")
    md.append("---")

    total = sum(len(v) for v in cats.values())
    today_total = sum(1 for v in cats.values() for it in v if it.get("added") == today)
    md.append(f"> **{total} items** across {len(CAT_ORDER)} categories — "
              f"**{today_total} new today.**")
    md.append("")

    for cat in CAT_ORDER:
        items = cats.get(cat, [])
        curated = curated_notes(CAT_SRCFILE[cat])
        if not items and not curated:
            continue
        md.append(f"## {cat}")
        md.append("")

        # (a) Curated revision notes + MCQs merged from the source file (if any).
        if curated:
            md.append("### 📌 Curated Revision Notes")
            md.append("")
            md.append(curated)
            md.append("")

        # (b) Latest scraped feed items (headline + description + link).
        if items:
            md.append("### 🗞️ Latest from gknow.in")
            md.append("")
            # newest first: today's additions on top, then by descending add-date
            ordered = sorted(items, key=lambda x: x.get("added", ""), reverse=True)
            shown = ordered[:MAX_PER_CATEGORY]
            if len(ordered) > MAX_PER_CATEGORY:
                md.append(f"_Showing latest {MAX_PER_CATEGORY} of {len(ordered)}._")
                md.append("")
            for it in shown:
                new = " 🆕" if it.get("added") == today else ""
                title = it["title"].replace("|", "\\|")
                md.append(f"- **[{title}]({it['url']})**{new}")
                if it.get("desc"):
                    md.append(f"  {it['desc']}")
            md.append("")

    # ---- Running index BY DATE at the very end ----
    md.append("---")
    md.append("## 🗓️ Coverage by Date (index)")
    md.append("")
    md.append("| Date | New items added |")
    md.append("|---|---|")
    for d in sorted(days_index, reverse=True):
        md.append(f"| {d} | {days_index[d]} |")
    md.append("")
    md.append(f"> **Total:** {total} items across {len(days_index)} day(s).")
    md.append("")
    md.append("---")
    md.append("> Source: [gknow.in](https://gknow.in/) current-affairs categories "
              "(RSS, scraped daily). For SSC CGL General Awareness. Back to "
              "[GK-Now index](README.md).")
    return "\n".join(md)


def render_pdf():
    body = md_render(MD_OUT.read_text(encoding="utf-8"))
    doc = (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
           f"<title>Daily GK Current-Affairs Digest</title>{MD_CSS}</head>"
           f"<body>{body}</body></html>")
    html_out = MD_OUT.with_suffix(".html")
    html_out.write_text(doc, encoding="utf-8")
    return html_to_pdf(html_out, delete_html=True, log=lambda m: log(m))


# ---------------------------------------------------------------------------
# Git: commit + push the PDF automatically (from the real git root).
# ---------------------------------------------------------------------------
def git_push(today):
    rel = PDF_OUT.relative_to(GIT_ROOT).as_posix()
    try:
        subprocess.run(["git", "add", rel], cwd=GIT_ROOT, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=GIT_ROOT)
        if diff.returncode == 0:
            log("no PDF changes to commit")
            return
        msg = (f"Daily GK current-affairs digest — {today}\n\n"
               "Auto-generated gknow.in digest (headlines + descriptions + links) "
               "across 8 categories.\n\n"
               "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
        subprocess.run(["git", "commit", "-m", msg], cwd=GIT_ROOT, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "push", "origin", "main"], cwd=GIT_ROOT, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("committed and pushed the digest PDF")
    except subprocess.CalledProcessError as exc:
        log(f"git step failed ({exc}); PDF generated but not pushed")


def main():
    log("=== run started ===")
    today = datetime.date.today().strftime("%Y-%m-%d")
    store = load_json(STORE, {"categories": {}, "days": {}, "seen_urls": []})
    cats = store.setdefault("categories", {})
    days_index = store.setdefault("days", {})
    seen = set(store.setdefault("seen_urls", []))

    added = 0
    if "--rebuild" not in sys.argv:
        if today in days_index and "--force" not in sys.argv:
            log(f"already merged today ({today}); use --force to re-scrape. "
                "Re-rendering from store.")
        else:
            for cat_name, feed in CATEGORIES:
                bucket = cats.setdefault(cat_name, [])
                new_here = 0
                for it in fetch_category(feed):
                    if it["url"] in seen:
                        continue
                    seen.add(it["url"])
                    it["added"] = today
                    bucket.append(it)
                    added += 1
                    new_here += 1
                log(f"{cat_name}: +{new_here}")
            if added:
                days_index[today] = days_index.get(today, 0) + added
            store["seen_urls"] = sorted(seen)
            STORE.write_text(json.dumps(store, ensure_ascii=False, indent=2),
                             encoding="utf-8")

    MD_OUT.write_text(build_markdown(store, today), encoding="utf-8")
    pdf = render_pdf()
    total = sum(len(v) for v in cats.values())
    log(f"merged {added} new; {total} total -> "
        f"{PDF_OUT.name if pdf else 'PDF FAILED'}")

    if "--no-push" not in sys.argv and pdf:
        git_push(today)
    log("=== run finished ===")


if __name__ == "__main__":
    main()
