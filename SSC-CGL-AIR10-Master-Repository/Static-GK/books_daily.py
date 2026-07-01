#!/usr/bin/env python3
"""
Daily Book-Releases Updater (source: GKToday)
=============================================
Scrapes the GKToday homepage for BOOK / AUTHOR related headlines (new releases,
launches, "penned by", memoirs, biographies) and maintains an auto-updated
"Recently in the News — Book Releases" block inside Books-and-Authors.html.

Only HEADLINES + the source link are stored (copyright-safe). Today's new items
are highlighted 🆕. The hand-written static reference sections in the HTML are
left untouched — this script only replaces the marked auto-block.

Markers in Books-and-Authors.html (added automatically on first run):
   <!-- BOOKS-AUTO-START -->  ... auto block ...  <!-- BOOKS-AUTO-END -->

Run:  py books_daily.py            (scrape + merge + refresh block)
      py books_daily.py --rebuild  (just refresh the block from the store)
"""
import re
import sys
import json
import html as _html
import datetime
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORE = BASE_DIR / "books_news_store.json"
HTML = BASE_DIR / "Books-and-Authors.html"
LOG = BASE_DIR / "run.log"

GK_HOME = "https://www.gktoday.in/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# STRONG book signals — a headline must contain at least one of these to count.
# (Generic "launches/releases" alone is NOT enough — too many false positives.)
BOOK_RE = re.compile(
    r"\b(book|books|author|authored|co-?author|novel|memoir|autobiograph(?:y|ies)|"
    r"biograph(?:y|ies)|penned|titled|writes? a book|releases? (?:his|her|the) book|"
    r"launch(?:es|ed)? (?:his|her|the|a|book)|book titled|new book)\b", re.I)
# Hard exclusions — defence/tech/scheme "launches" that are never books.
NOT_BOOK_RE = re.compile(
    r"\b(missile|satellite|rocket|app|portal|scheme|vaccine|fund|index|drdo|"
    r"operation|mission|bridge|train|highway|chatbot|service|programme|program|"
    r"dfp|defence|defense|aircraft|drone|exercise|campaign|website|platform)\b", re.I)


def log(msg):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    print(line)
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


def _esc(s):
    return _html.escape(s or "", quote=False)


def fetch_book_headlines():
    try:
        req = urllib.request.Request(GK_HOME, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            page = resp.read().decode("utf-8", "ignore")
    except Exception as exc:
        log(f"GKToday fetch failed: {exc}")
        return []
    items = re.findall(r"home-post-item.*?(?=home-post-item|side_menu_title|\Z)",
                       page, re.S)
    out, seen = [], set()
    for it in items:
        m = re.search(r'<a[^>]+href="(https://www\.gktoday\.in/[a-z0-9-]{8,}/)"[^>]*>(.*?)</a>',
                      it, re.S)
        if not m:
            continue
        url = m.group(1)
        title = re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", "", m.group(2)))).strip()
        if len(title) < 12 or url in seen:
            continue
        if BOOK_RE.search(title) and not NOT_BOOK_RE.search(title):
            seen.add(url)
            out.append({"title": title, "url": url})
    if out:
        log(f"GKToday: {len(out)} book-related headline(s) found.")
    return out


def render_block(items, today):
    rows = []
    today_n = sum(1 for e in items if e.get("date") == today)
    badge = (f" <span style='background:#e67e22;color:#fff;border-radius:6px;"
             f"padding:1px 8px;font-size:.8em'>{today_n} new today</span>"
             if today_n else "")
    for e in sorted(items, key=lambda x: x.get("date", ""), reverse=True):
        hl = " style='background:#fff3cd'" if e.get("date") == today else ""
        nb = " 🆕" if e.get("date") == today else ""
        link = (f"<a href='{_esc(e['url'])}' target='_blank' rel='noopener'>{_esc(e['title'])}</a>"
                if e.get("url") else _esc(e["title"]))
        rows.append(f"<tr{hl}><td>{link}{nb}</td><td class='date'>{_esc(e.get('date',''))}</td></tr>")
    if not rows:
        rows.append("<tr><td colspan='2'><em>No book headlines captured yet — "
                    "run after GKToday posts book news.</em></td></tr>")
    return (
        "<!-- BOOKS-AUTO-START -->\n"
        "<h2 id='recent-releases'>🆕 Recently in the News — Book Releases"
        f"{badge} <a class='backtop' href='#contents'>↑ top</a></h2>\n"
        "<p class='meta'>Auto-mined daily from "
        "<a href='https://www.gktoday.in/' target='_blank' rel='noopener'>GKToday</a> "
        "(headlines only; click to read). Today's are highlighted.</p>\n"
        "<table><thead><tr><th>Headline</th><th>Date</th></tr></thead><tbody>\n"
        + "\n".join(rows) +
        "\n</tbody></table>\n"
        "<!-- BOOKS-AUTO-END -->")


def refresh_html(items, today):
    if not HTML.exists():
        log(f"ERROR: {HTML.name} not found.")
        return
    doc = HTML.read_text(encoding="utf-8")
    block = render_block(items, today)
    if "<!-- BOOKS-AUTO-START -->" in doc:
        doc = re.sub(r"<!-- BOOKS-AUTO-START -->.*?<!-- BOOKS-AUTO-END -->",
                     lambda m: block, doc, flags=re.S)
    else:
        # insert just after the Contents table (before the first content section)
        marker = "</tbody></table>"
        idx = doc.find(marker)  # end of the Contents table
        if idx != -1:
            cut = idx + len(marker)
            doc = doc[:cut] + "\n\n" + block + "\n" + doc[cut:]
        else:
            doc = doc.replace("</body>", block + "\n</body>")
    HTML.write_text(doc, encoding="utf-8")


def main():
    log("=== Books-news build started ===")
    today = datetime.date.today().strftime("%Y-%m-%d")
    store = load_json(STORE, {"items": []})
    items = store.get("items", [])
    have = {e.get("url") for e in items if e.get("url")}
    have_t = {e["title"].lower() for e in items}

    added = 0
    if "--rebuild" not in sys.argv:
        for e in fetch_book_headlines():
            if e["url"] in have or e["title"].lower() in have_t:
                continue
            have.add(e["url"]); have_t.add(e["title"].lower())
            items.append({"title": e["title"], "url": e["url"], "date": today})
            added += 1
        store["items"] = items
        STORE.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")

    refresh_html(items, today)
    log(f"Merged {added} new book headline(s); {len(items)} total -> {HTML.name}")
    log("=== Books-news build finished ===")


if __name__ == "__main__":
    main()
