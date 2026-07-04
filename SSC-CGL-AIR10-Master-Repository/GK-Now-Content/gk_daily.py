#!/usr/bin/env python3
"""
Daily GK / Current-Affairs Builder (source: GKToday)
====================================================
Scrapes the day's current-affairs HEADLINES from GKToday (gktoday.in homepage),
categorises them, merges into one deduped store, and rewrites a single
self-contained HTML page with TODAY's new items highlighted.

⚠️ Copyright-safe: only HEADLINES + the source link are stored (never article
bodies). Each item links back to GKToday to read in full.

Each item: { title, url, category, date (YYYY-MM-DD) }.

Run:  py gk_daily.py            (scrape + merge + rebuild)
      py gk_daily.py --rebuild  (rebuild HTML from the store only, no fetch)

Optional manual additions: drop items into  gk_new_today.json  as a list of
  {"title": "...", "url": "...", "category": "National"}   (e.g. from newspapers)
they are merged alongside the scraped ones.
"""
import re
import sys
import json
import html as _html
import datetime
import urllib.request
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))  # repo root, for html_to_pdf
from html_to_pdf import html_to_pdf  # noqa: E402

STORE = BASE_DIR / "gk_store.json"
NEW_TODAY = BASE_DIR / "gk_new_today.json"
OUTPUT = BASE_DIR / "Daily_GK_Current_Affairs.html"
LOG = BASE_DIR / "run.log"

GK_HOME = "https://www.gktoday.in/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


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


# ---------------------------------------------------------------------------
# Scrape today's headlines from GKToday homepage (titles + links only)
# ---------------------------------------------------------------------------
def fetch_gktoday():
    try:
        req = urllib.request.Request(GK_HOME, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            html_text = resp.read().decode("utf-8", "ignore")
    except Exception as exc:
        log(f"GKToday fetch failed: {exc}")
        return []

    items = re.findall(r"home-post-item.*?(?=home-post-item|side_menu_title|\Z)",
                       html_text, re.S)
    out = []
    seen = set()
    for it in items:
        m = re.search(r'<a[^>]+href="(https://www\.gktoday\.in/[a-z0-9-]{8,}/)"[^>]*>(.*?)</a>',
                      it, re.S)
        if not m:
            continue
        url = m.group(1)
        title = _html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        title = re.sub(r"\s+", " ", title)
        if len(title) < 12 or url in seen:
            continue
        seen.add(url)
        out.append({"title": title, "url": url, "category": categorise(title)})
    if out:
        log(f"GKToday: scraped {len(out)} headlines.")
    return out


# ---------------------------------------------------------------------------
# Categorise a headline by keywords (SSC GA buckets)
# ---------------------------------------------------------------------------
OTHER = "🗂️ Other / National"
CATEGORIES = [
    ("🏅 Awards & Honours",
     r"\b(award|honour|honor|prize|medal|padma|bharat ratna|gallantry|laureate)\b"),
    ("👤 Appointments",
     r"\b(appoint|takes charge|new chief|sworn in|named|elected as|chairman|ceo|"
     r"governor|ambassador|chief justice)\b"),
    ("🛡️ Defence & Security",
     r"\b(army|navy|air force|iaf|defence|defense|drdo|missile|warfare|military|"
     r"brahmos|exercise|border|naval|soldier)\b"),
    ("💰 Economy & Banking",
     r"\b(rbi|gdp|economy|bank|inflation|rupee|budget|tax|gst|fiscal|trade|"
     r"investment|repo|sensex|nifty)\b"),
    ("🔬 Science & Technology",
     r"\b(isro|satellite|space|launch|rocket|technology|ai |research|vaccine|"
     r"scientist|dna|mission|chandrayaan)\b"),
    ("🌍 International",
     r"\b(india and|pact|summit|bilateral|united nations|un |g20|brics|"
     r"foreign|treaty|agreement with|saudi|china|usa|russia)\b"),
    ("🌱 Environment & Ecology",
     r"\b(climate|environment|wildlife|tiger|forest|pollution|biodiversity|"
     r"emission|renewable|solar|species|ramsar)\b"),
    ("🏛️ Polity & Schemes",
     r"\b(scheme|yojana|mission|bill|act|policy|cabinet|parliament|supreme court|"
     r"gram sabha|government launches|ministry)\b"),
    ("🏆 Sports",
     r"\b(cup|gold|championship|olympic|world cup|tournament|cricket|rowing|"
     r"medal|won|final|match|trophy)\b"),
    ("🎭 Art, Culture & Days",
     r"\b(festival|heritage|culture|day|anniversary|dance|temple|unesco|"
     r"celebrat|tradition)\b"),
]
CAT_ORDER = [c for c, _ in CATEGORIES] + [OTHER]


def categorise(title):
    t = title.lower()
    for name, pat in CATEGORIES:
        if re.search(pat, t):
            return name
    return OTHER


def _anchor(heading):
    t = heading.strip().lower()
    t = re.sub(r"[^\w \-]", "", t, flags=re.UNICODE)
    t = re.sub(r"[^\x00-\x7f]", "", t)
    return t.strip().replace(" ", "-")


def _esc(s):
    return _html.escape(s or "", quote=False)


PAGE_CSS = """
  :root{ --ink:#102a16; --accent:#1e7a3c; }
  body{ font-family:"Segoe UI",Arial,sans-serif; color:var(--ink); max-width:1000px;
        margin:0 auto; padding:28px; line-height:1.5; }
  h1{ color:#fff; background:linear-gradient(135deg,#14532d,#1e7a3c); padding:18px 22px;
      border-radius:12px; font-size:1.6em; }
  h2{ color:#14532d; border-left:7px solid var(--accent); padding:6px 12px;
      background:#eef8f1; border-radius:0 8px 8px 0; margin-top:30px; scroll-margin-top:14px; }
  blockquote{ background:#fff8e1; border-left:5px solid #f1c40f; margin:12px 0;
      padding:10px 16px; border-radius:0 8px 8px 0; }
  table{ border-collapse:collapse; width:100%; margin:12px 0; font-size:.95em; }
  th{ background:#14532d; color:#fff; text-align:left; padding:8px 11px; }
  td{ border:1px solid #d3e8da; padding:7px 11px; vertical-align:top; }
  tr:nth-child(even){ background:#f4faf6; }
  a{ color:#14532d; text-decoration:none; } a:hover{ text-decoration:underline; }
  .count{ text-align:center; font-weight:600; }
  .backtop{ font-size:.8em; }
  .date{ color:#666; font-size:.85em; white-space:nowrap; }
  tr.today{ background:#fff3cd !important; }
  tr.today td:first-child::after{ content:" 🆕"; }
  .newbadge{ background:#e67e22; color:#fff; border-radius:6px; padding:1px 8px;
      font-size:.8em; margin-left:8px; }
  hr{ border:0; border-top:2px dashed #d3e8da; margin:22px 0; }
"""


def write_html(items, today_str):
    buckets = defaultdict(list)
    for e in items:
        buckets[e.get("category", OTHER)].append(e)
    used = [c for c in CAT_ORDER if buckets[c]]
    today_count = sum(1 for e in items if e.get("date") == today_str)

    p = ["<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width, initial-scale=1'>",
         "<title>Daily GK & Current Affairs — GKToday</title>",
         f"<style>{PAGE_CSS}</style></head><body>",
         "<h1>🗞️ Daily GK &amp; Current Affairs</h1>"]
    badge = f"<span class='newbadge'>{today_count} new today</span>" if today_count else ""
    p.append(
        f"<blockquote><strong>{len(items)} headlines</strong>{badge}, grouped by "
        "topic, mined daily from <strong>GKToday</strong>. Items added "
        "<strong>today are highlighted</strong> 🆕. Headlines only — click a title "
        "to read the full article on GKToday.<br><br><strong>How to use:</strong> "
        "skim a topic daily, click through for detail, and note names/dates/places "
        "for the SSC General Awareness section.</blockquote>")

    p.append("<h2 id='contents'>🧭 Contents</h2>")
    p.append("<table><thead><tr><th>#</th><th>Topic</th><th>Items</th>"
             "<th>New</th></tr></thead><tbody>")
    for i, c in enumerate(used, 1):
        n_new = sum(1 for e in buckets[c] if e.get("date") == today_str)
        p.append(f"<tr><td class='count'>{i}</td>"
                 f"<td><a href='#{_anchor(c)}'>{_esc(c)}</a></td>"
                 f"<td class='count'>{len(buckets[c])}</td>"
                 f"<td class='count'>{n_new or ''}</td></tr>")
    p.append("</tbody></table>")

    for c in used:
        p.append(f"<h2 id='{_anchor(c)}'>{_esc(c)} "
                 "<a class='backtop' href='#contents'>↑ top</a></h2>")
        p.append("<table><thead><tr><th>Headline</th><th>Date</th>"
                 "</tr></thead><tbody>")
        # newest first within a topic
        for e in sorted(buckets[c], key=lambda x: x.get("date", ""), reverse=True):
            cls = " class='today'" if e.get("date") == today_str else ""
            link = (f"<a href='{_esc(e['url'])}' target='_blank' rel='noopener'>"
                    f"{_esc(e['title'])}</a>") if e.get("url") else _esc(e["title"])
            p.append(f"<tr{cls}><td>{link}</td>"
                     f"<td class='date'>{_esc(e.get('date',''))}</td></tr>")
        p.append("</tbody></table>")

    p.append("<hr><p><strong>Source:</strong> "
             "<a href='https://www.gktoday.in/' target='_blank' rel='noopener'>GKToday</a> "
             "(headlines mined daily; full articles on their site). For SSC CGL "
             "General Awareness practice.</p>")
    p.append("</body></html>")
    OUTPUT.write_text("\n".join(p), encoding="utf-8")
    return today_count


def main():
    log("=== GK daily build started ===")
    today = datetime.date.today().strftime("%Y-%m-%d")
    store = load_json(STORE, {"items": []})
    items = store.get("items", [])
    have = {e["url"] for e in items if e.get("url")}
    have_titles = {e["title"].lower() for e in items}

    added = 0
    if "--rebuild" not in sys.argv:
        scraped = fetch_gktoday()
        scraped += [{"title": x.get("title", ""), "url": x.get("url", ""),
                     "category": x.get("category") or categorise(x.get("title", ""))}
                    for x in load_json(NEW_TODAY, [])]
        for e in scraped:
            url, title = e.get("url", ""), (e.get("title") or "").strip()
            if not title:
                continue
            if (url and url in have) or title.lower() in have_titles:
                continue
            have.add(url); have_titles.add(title.lower())
            items.append({"title": title, "url": url,
                          "category": e.get("category") or categorise(title),
                          "date": today})
            added += 1
        store["items"] = items
        STORE.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")
        NEW_TODAY.write_text("[]", encoding="utf-8")

    n_today = write_html(items, today)
    log(f"Merged {added} new; {len(items)} total; {n_today} highlighted today "
        f"-> {OUTPUT.name}")
    html_to_pdf(OUTPUT, delete_html=True, log=log)  # mobile-friendly PDF; drop HTML
    log("=== GK daily build finished ===")


if __name__ == "__main__":
    main()
