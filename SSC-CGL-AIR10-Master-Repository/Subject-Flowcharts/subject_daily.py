#!/usr/bin/env python3
"""
Subject Flowchart — Daily Updater
=================================
Keeps the 5 Subject-Flowchart study pages "alive" every day:

  1. Stamps TODAY'S DATE into every page's <!-- DAILY-AUTO --> block.
  2. Rotates a "focus of the day" (a topic anchor) so you always open the
     page on something new to revise — deterministic by day-of-year, so the
     same day always shows the same focus (good for spaced revision).
  3. For the Current-Affairs page ONLY, mines TODAY'S headlines from GKToday
     that fall into the 5 buckets (Awards / Schemes / Sports / Days / Orgs),
     storing HEADLINES + source link only (copyright-safe), newest highlighted.

Pages touched (in this same folder):
  01_History-Flowchart.html
  02_Geography-Flowchart.html
  03_Polity-Flowchart.html
  04_Science-Flowchart.html
  05_Current-Affairs-Flowchart.html

Run:  py subject_daily.py            (stamp dates + rotate focus + mine CA news)
      py subject_daily.py --no-news  (skip the network scrape; just stamp/rotate)
      py subject_daily.py --rebuild  (rebuild CA feed from the stored JSON only)
"""
import re
import sys
import json
import html as _html
import datetime
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))  # repo root, for html_to_pdf
from html_to_pdf import html_to_pdf  # noqa: E402

STORE = BASE / "ca_news_store.json"
LOG = BASE / "run.log"

GK_HOME = "https://www.gktoday.in/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# ---- per-page rotating "focus of the day" (anchor + label) --------------
# Each entry: (filename, [(anchor, label), ...]).  Rotated by day-of-year.
PAGES = {
    "01_History-Flowchart.html": ("Topic of the day", [
        ("#buddhism", "Buddhism & Jainism — councils + 8-fold path"),
        ("#mauryan",  "Mauryan Empire — Chandragupta→Ashoka, Kalinga"),
        ("#gupta",    "Gupta 'Golden Age' — Samudragupta, Aryabhata"),
        ("#bhakti",   "Bhakti & Sufi saints — Nirguna vs Saguna"),
        ("#mughal",   "Mughal admin — Mansabdari, Todar Mal, Navaratnas"),
        ("#modern",   "Freedom Movement timeline — 1857 → 1947"),
        ("#acts",     "Important Acts — 1773 → 1935"),
    ]),
    "02_Geography-Flowchart.html": ("Topic of the day", [
        ("#rivers",  "River systems — Himalayan vs Peninsular split"),
        ("#tribs",   "Tributaries — Ganga & Yamuna trees"),
        ("#parks",   "National Parks & animals — the Big 4"),
        ("#ports",   "Ports — West vs East coast superlatives"),
        ("#mount",   "Mountains & passes — Himadri/Himachal/Shiwalik"),
        ("#soil",    "Soils — Black=cotton, Alluvial=fertile"),
        ("#climate", "Climate — SW vs NE monsoon"),
    ]),
    "03_Polity-Flowchart.html": ("Article of the day", [
        ("#fr",         "Fundamental Rights — 6 rights + 5 writs"),
        ("#dpsp",       "DPSP — Part IV, Gandhian/Socialist/Liberal"),
        ("#parliament", "Parliament — LS vs RS, bill flow"),
        ("#executive",  "President/PM/Judiciary powers"),
        ("#amend",      "Amendments — 42,44,73,74,86"),
        ("#borrowed",   "Borrowed features — UK/USA/Ireland"),
        ("#fd",         "Fundamental Duties — Art 51A"),
    ]),
    "04_Science-Flowchart.html": ("Concept of the day", [
        ("#motion",      "Motion & Force — Newton's laws, SI units"),
        ("#light",       "Light — VIBGYOR, eye defects"),
        ("#electricity", "Electricity — Ohm's law, series/parallel"),
        ("#acids",       "Acids & Bases — pH scale, indicators"),
        ("#metals",      "Metals — reactivity series, alloys"),
        ("#vitamins",    "Vitamins — deficiency diseases table"),
        ("#diseases",    "Diseases — bacterial/viral/vector-borne"),
    ]),
    # Current Affairs handled specially (news feed), but still gets a focus line.
    "05_Current-Affairs-Flowchart.html": ("Bucket of the day", [
        ("#awards",  "Awards — civilian order R-V-B-S"),
        ("#schemes", "Schemes — aim + tagline + ministry"),
        ("#sports",  "Sports — cup ↔ sport, player counts"),
        ("#days",    "Important Days — date → day → org"),
        ("#orgs",    "Intl Orgs — HQ + head + year"),
    ]),
}

CA_PAGE = "05_Current-Affairs-Flowchart.html"

# Bucket classifier for Current-Affairs headline mining.
BUCKETS = [
    ("Awards",  re.compile(r"\b(award|honou?r|padma|bharat ratna|nobel|prize|"
                           r"jnanpith|gyanpith|dadasaheb|khel ratna|arjuna|felicitat)\b", re.I)),
    ("Schemes", re.compile(r"\b(scheme|yojana|mission|abhiyan|programme|program|"
                           r"initiative|launch(?:es|ed)? .*?(?:scheme|yojana|mission))\b", re.I)),
    ("Sports",  re.compile(r"\b(cup|trophy|olympic|world championship|medal|tournament|"
                           r"final|champion|athlet|cricket|football|hockey|badminton|"
                           r"chess|wins? (?:gold|silver|bronze))\b", re.I)),
    ("Days",    re.compile(r"\b(day observed|international day|world .* day|national .* day|"
                           r"celebrat(?:es|ed)|observ(?:es|ed) .* day|theme for)\b", re.I)),
    ("Orgs",    re.compile(r"\b(summit|un |united nations|who|imf|world bank|wto|unesco|"
                           r"g20|g-20|brics|saarc|asean|opec|assembly|organi[sz]ation)\b", re.I)),
]


def log(msg):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    try:
        print(line)
    except UnicodeEncodeError:
        # Windows consoles default to cp1252; fall back to ASCII-safe output.
        print(line.encode("ascii", "replace").decode("ascii"))
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


# ---------- 1 & 2 : date stamp + rotating focus (all pages) --------------
def stamp_focus(fname, label, choices, today, doy):
    path = BASE / fname
    if not path.exists():
        log(f"skip (missing): {fname}")
        return
    anchor, focus = choices[doy % len(choices)]
    doc = path.read_text(encoding="utf-8")

    focus_html = (
        f'<div class="daily">📅 <b>{today}</b> &nbsp;·&nbsp; '
        f'<b>{label}:</b> <a href="{anchor}">{_esc(focus)}</a> '
        f'&nbsp;<span class="pill">rotates daily</span></div>'
    )

    if fname == CA_PAGE:
        # For Current Affairs, keep the news feed block; only refresh the top
        # focus line (the first <div class="daily">...</div> inside the block).
        def repl_ca(m):
            body = m.group(1)
            # replace only the leading focus div, keep the rest (feed) intact
            body2 = re.sub(r'<div class="daily">.*?</div>', focus_html, body,
                           count=1, flags=re.S)
            return f"<!-- DAILY-AUTO-START -->{body2}<!-- DAILY-AUTO-END -->"
        doc = re.sub(r"<!-- DAILY-AUTO-START -->(.*?)<!-- DAILY-AUTO-END -->",
                     repl_ca, doc, flags=re.S)
    else:
        block = ("<!-- DAILY-AUTO-START -->\n" + focus_html +
                 "\n<!-- DAILY-AUTO-END -->")
        doc = re.sub(r"<!-- DAILY-AUTO-START -->.*?<!-- DAILY-AUTO-END -->",
                     lambda m: block, doc, flags=re.S)

    path.write_text(doc, encoding="utf-8")
    log(f"stamped {fname}: {today} → {focus}")


# ---------- 3 : Current-Affairs headline mining --------------------------
def fetch_ca_headlines():
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
        bucket = next((name for name, rx in BUCKETS if rx.search(title)), None)
        if bucket:
            seen.add(url)
            out.append({"title": title, "url": url, "bucket": bucket})
    log(f"GKToday: {len(out)} bucket-matched headline(s).")
    return out


def render_ca_feed(items, focus_html, today):
    rows = []
    today_n = sum(1 for e in items if e.get("date") == today)
    badge = (f" <span class='newtag'>{today_n} new today</span>" if today_n else "")
    for e in sorted(items, key=lambda x: x.get("date", ""), reverse=True)[:40]:
        hl = " style='background:#fff3cd'" if e.get("date") == today else ""
        nb = " 🆕" if e.get("date") == today else ""
        link = (f"<a href='{_esc(e['url'])}' target='_blank' rel='noopener'>{_esc(e['title'])}</a>"
                if e.get("url") else _esc(e["title"]))
        rows.append(f"<tr{hl}><td>{link}{nb}</td>"
                    f"<td><span class='pill'>{_esc(e.get('bucket','—'))}</span></td>"
                    f"<td>{_esc(e.get('date',''))}</td></tr>")
    if not rows:
        rows.append("<tr><td colspan='3'><em>No headlines captured yet — "
                    "run the daily script when GKToday has fresh news.</em></td></tr>")
    return (
        "<!-- DAILY-AUTO-START -->\n" + focus_html + "\n"
        f"<div class='daily' style='margin-top:0'>🗞️ <b>Today's mined headlines</b>{badge} "
        "— Awards · Schemes · Sports · Days · Orgs (source: GKToday; headlines only).</div>\n"
        "<div class='tablewrap' style='margin-top:8px'>\n"
        "<table><thead><tr><th>Headline</th><th>Bucket</th><th>Date</th></tr></thead><tbody>\n"
        + "\n".join(rows) +
        "\n</tbody></table></div>\n"
        "<!-- DAILY-AUTO-END -->")


def update_ca(today, doy, do_news):
    path = BASE / CA_PAGE
    if not path.exists():
        log(f"skip (missing): {CA_PAGE}")
        return
    label, choices = PAGES[CA_PAGE]
    anchor, focus = choices[doy % len(choices)]
    focus_html = (
        f'<div class="daily">📅 <b>{today}</b> &nbsp;·&nbsp; '
        f'<b>{label}:</b> <a href="{anchor}">{_esc(focus)}</a> '
        f'&nbsp;<span class="pill">rotates daily</span></div>'
    )

    store = load_json(STORE, {"items": []})
    items = store.get("items", [])
    have = {e.get("url") for e in items if e.get("url")}

    added = 0
    if do_news and "--rebuild" not in sys.argv:
        for e in fetch_ca_headlines():
            if e["url"] in have:
                continue
            have.add(e["url"])
            items.append({**e, "date": today})
            added += 1
        store["items"] = items
        STORE.write_text(json.dumps(store, ensure_ascii=False, indent=2), encoding="utf-8")

    doc = path.read_text(encoding="utf-8")
    feed = render_ca_feed(items, focus_html, today)
    doc = re.sub(r"<!-- DAILY-AUTO-START -->.*?<!-- DAILY-AUTO-END -->",
                 lambda m: feed, doc, flags=re.S)
    path.write_text(doc, encoding="utf-8")
    log(f"CA page: +{added} new headline(s), {len(items)} total; focus → {focus}")


def main():
    log("=== Subject-daily build started ===")
    now = datetime.date.today()
    today = now.strftime("%Y-%m-%d")
    doy = now.timetuple().tm_yday
    do_news = "--no-news" not in sys.argv

    for fname, (label, choices) in PAGES.items():
        if fname == CA_PAGE:
            continue
        stamp_focus(fname, label, choices, today, doy)

    update_ca(today, doy, do_news)

    # HTML pages are the script's local working files (patched in place each run)
    # and are .gitignored; publish a mobile-friendly PDF of each for GitHub.
    for fname in PAGES:
        html_to_pdf(BASE / fname, delete_html=False, log=log)

    log("=== Subject-daily build finished ===")


if __name__ == "__main__":
    main()
