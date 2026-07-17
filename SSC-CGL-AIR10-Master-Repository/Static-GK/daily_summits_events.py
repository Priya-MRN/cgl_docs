"""
Summits, Events, Sports, IR & Inventions — 2-year capsule + daily auto-update.

A STATIC-GK study document that pairs a frozen, richly-tabulated 2-year base
(major national & international summits, sports events, political/national days,
international relations, and inventions/discoveries — with host / theme / motto /
occasion / date / day / winners / main speakers & speech content) with a
DAILY-updated feed of fresh current-affairs headlines mined from GKToday.

Each run:
  1. mines GKToday homepage headlines, keeps only the ones relevant to this
     document's scope (Summits · Sports · Days & Events · Int'l Relations ·
     Inventions/Discoveries · Awards), tags each India / International,
  2. merges the deduped new items into summits_events_store.json (grouped by
     the date first seen),
  3. renders ONE combined, mobile-friendly PDF:
        [ frozen 2-year base ]  +  [ Daily Updates, newest date first ]
        +  a running "Coverage by date" index at the very end,
  4. commits AND pushes the PDF to git automatically.

COPYRIGHT-SAFE: only headlines + source links are stored — never article bodies.
The frozen base (Summits-Events-Sports-IR-Inventions-2Y-Base.md) is the curated,
hand-verified source; it is gitignored (PDF-only policy) and edited directly.

Run:  py daily_summits_events.py            (mine + merge + render + push)
      py daily_summits_events.py --rebuild  (re-render from the store, no fetch)
      py daily_summits_events.py --no-push  (skip the git commit/push step)
      py daily_summits_events.py --force    (merge again even if run already today)
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
from md_to_pdf import render as md_render, CSS as MD_CSS  # reuse the MD->HTML renderer
from html_to_pdf import html_to_pdf

STORE = BASE_DIR / "summits_events_store.json"
BASE_MD = BASE_DIR / "Summits-Events-Sports-IR-Inventions-2Y-Base.md"  # frozen curated source (gitignored)
MD_OUT = BASE_DIR / "Summits-Events-Sports-IR-Inventions.md"           # working full source (gitignored)
PDF_OUT = BASE_DIR / "Summits-Events-Sports-IR-Inventions.pdf"         # the committed artifact
LOG = BASE_DIR / "run.log"

GK_HOME = "https://www.gktoday.in/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def log(msg):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] Summits-Events: {msg}"
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
# Buckets — tuned to THIS document's scope (summits / sports / events /
# international relations / inventions & discoveries / awards). The first
# pattern that matches wins. Headlines that match none are dropped (this doc is
# focused — general CA lives in the other daily digests).
# ---------------------------------------------------------------------------
BUCKETS = [
    ("🌐 Summits, Meetings & International Relations",
     r"\b(summit|conference|g20|g7|brics|sco|asean|saarc|quad|bimstec|"
     r"bilateral|dialogue|forum|convention|un general assembly|unga|davos|"
     r"cop\d+|voice of global south|multilateral|diplomatic|state visit|"
     r"treaty|pact|accord|mou|foreign minister|external affairs)\b"),
    ("🔬 Inventions, Discoveries & Science",
     r"\b(invent|discover|breakthrough|isro|nasa|mission|launch(es|ed)?|"
     r"satellite|rover|spacecraft|chandrayaan|gaganyaan|aditya|spadex|nisar|"
     r"vaccine|gene|crispr|quantum|semiconductor|ai model|research|"
     r"scientists?|patent|telescope|space station|rocket|probe)\b"),
    ("🏆 Sports",
     r"\b(cup|gold|silver|bronze|championship|olympic|paralympic|world cup|"
     r"tournament|cricket|hockey|football|badminton|tennis|chess|medal|won|"
     r"final|trophy|league|grand slam|title|series|athlet|khelo india|"
     r"national games|ipl|fifa|wrestl|boxing|shoot)\b"),
    ("🏅 Awards & Honours",
     r"\b(award|honour|honor|prize|medal|padma|bharat ratna|gallantry|laureate|"
     r"nobel|booker|jnanpith|magsaysay|khel ratna|arjuna|dronacharya|conferred|"
     r"felicitat|oscar|grammy)\b"),
    ("📅 Important Days, Events & Celebrations",
     r"\b(day|diwas|week|anniversary|jayanti|observ|celebrat|theme of|festival|"
     r"republic day|independence day|world .* day|international .* day|"
     r"national .* day|inaugurat)\b"),
]
INDIA_HINT = re.compile(
    r"\b(india|indian|delhi|bharat|modi|isro|rbi|drdo|uidai|aadhaar|niti|"
    r"supreme court|parliament|union|centre|ministry|lok sabha|rajya sabha|"
    r"andhra|arunachal|assam|bihar|chhattisgarh|goa|gujarat|haryana|himachal|"
    r"jharkhand|karnataka|kerala|madhya pradesh|maharashtra|manipur|meghalaya|"
    r"mizoram|nagaland|odisha|punjab|rajasthan|sikkim|tamil nadu|telangana|"
    r"tripura|uttar pradesh|uttarakhand|west bengal|ladakh|kashmir|"
    r"gi tag|udan|scheme|yojana)\b", re.I)
ORDER = [b for b, _ in BUCKETS]


def bucket_of(title):
    """Return the matching bucket, or None if the headline is out of scope."""
    t = title.lower()
    for name, pat in BUCKETS:
        if re.search(pat, t):
            return name
    return None


def scope_of(title):
    return "India" if INDIA_HINT.search(title) else "International"


def fetch_headlines():
    try:
        req = urllib.request.Request(GK_HOME, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            page = resp.read().decode("utf-8", "ignore")
    except Exception as exc:
        log(f"GKToday fetch failed: {exc}")
        return []
    blocks = re.findall(r"home-post-item.*?(?=home-post-item|side_menu_title|\Z)",
                        page, re.S)
    out, seen = [], set()
    for blk in blocks:
        m = re.search(
            r'<a[^>]+href="(https://www\.gktoday\.in/[a-z0-9-]{8,}/)"[^>]*>(.*?)</a>',
            blk, re.S)
        if not m:
            continue
        url = m.group(1)
        title = _html.unescape(re.sub(r"<[^>]+>", "", m.group(2))).strip()
        title = re.sub(r"\s+", " ", title)
        if len(title) < 12 or url in seen:
            continue
        # skip non-news noise (quizzes, MCQ round-ups, generic listicles)
        if re.search(r"\b(quiz|mcq|current affairs (of|for|:)|test series)\b",
                     title, re.I):
            continue
        bucket = bucket_of(title)
        if bucket is None:          # out of this document's scope -> drop
            continue
        seen.add(url)
        out.append({"title": title, "url": url,
                    "bucket": bucket, "scope": scope_of(title)})
    log(f"scraped {len(out)} in-scope headlines")
    return out


# ---------------------------------------------------------------------------
# Markdown rendering: frozen base first, then dated daily updates, then index.
# ---------------------------------------------------------------------------
def build_markdown(store, today):
    days = store.get("days", {})   # {date: [items]}
    md = []

    # ---- 1) the frozen, curated 2-year base (verbatim) ----
    if BASE_MD.exists():
        md.append(BASE_MD.read_text(encoding="utf-8").rstrip())
    else:
        md.append("# Summits, Events, Sports, International Relations & Inventions "
                  "— 2-Year Capsule")
        md.append("")
        md.append("> _Base capsule file missing; showing daily updates only._")
    md.append("")
    md.append("---")

    # ---- 2) Daily Updates section (newest date first) ----
    md.append("# 🔄 Daily Updates — Fresh Current Affairs")
    md.append("")
    md.append(f"> Auto-mined daily from GKToday and filtered to this document's "
              f"scope (Summits · Sports · Days & Events · International Relations · "
              f"Inventions & Discoveries · Awards). **Latest update: {today}.** "
              f"Each item tagged **India / International**.")
    md.append("")
    md.append("> ⚠️ Headlines + source links only (copyright-safe). Click a headline "
              "to read the full story at the source. Verify facts before the exam.")
    md.append("")

    today_items = days.get(today, [])
    md.append(f"## 🆕 Today — {today}")
    md.append("")
    if not today_items:
        md.append("_No new in-scope items mined today. See earlier dates below._")
        md.append("")
    else:
        _render_buckets(md, today_items)

    other_dates = sorted((d for d in days if d != today), reverse=True)
    if other_dates:
        md.append("---")
        md.append("## 📚 Earlier Updates")
        md.append("")
        for d in other_dates:
            md.append(f"### {d}")
            md.append("")
            _render_buckets(md, days[d])

    # ---- 3) Running index BY DATE at the very end ----
    md.append("---")
    md.append("## 🗓️ Daily-Update Coverage by Date (index)")
    md.append("")
    md.append("| Date | Items | Buckets covered |")
    md.append("|---|---|---|")
    for d in sorted(days, reverse=True):
        items = days[d]
        buckets = sorted({i["bucket"].split(" ", 1)[-1] for i in items})
        md.append(f"| {d} | {len(items)} | {', '.join(buckets)} |")
    md.append("")
    total = sum(len(v) for v in days.values())
    md.append(f"> **Daily-update total:** {total} items across {len(days)} day(s), "
              f"on top of the frozen 2-year base above.")
    md.append("")
    md.append("---")
    md.append("> Base: hand-curated from news/journals (last 2 years). "
              "Daily feed source: [GKToday](https://www.gktoday.in/). "
              "For SSC CGL General Awareness. Back to "
              "[Static-GK index](README.md).")
    return "\n".join(md)


def _render_buckets(md, items):
    for bucket in ORDER:
        group = [i for i in items if i["bucket"] == bucket]
        if not group:
            continue
        md.append(f"**{bucket}**")
        md.append("")
        # India items first within each bucket, then International
        for it in sorted(group, key=lambda x: x["scope"] != "India"):
            tag = "🇮🇳" if it["scope"] == "India" else "🌍"
            title = it["title"].replace("|", "\\|")
            md.append(f"- {tag} [{title}]({it['url']})")
        md.append("")


# ---------------------------------------------------------------------------
# Render MD -> PDF (reuse md_to_pdf's renderer + styling), delete the HTML.
# ---------------------------------------------------------------------------
def render_pdf():
    body = md_render(MD_OUT.read_text(encoding="utf-8"))
    doc = (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
           f"<title>Summits, Events, Sports, IR &amp; Inventions</title>"
           f"{MD_CSS}</head><body>{body}</body></html>")
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
        msg = (f"Daily Summits/Events/Sports/IR/Inventions update — {today}\n\n"
               "Auto-generated: 2-year capsule + daily headlines (source links).\n\n"
               "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>")
        subprocess.run(["git", "commit", "-m", msg], cwd=GIT_ROOT, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "push", "origin", "main"], cwd=GIT_ROOT, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log("committed and pushed the PDF")
    except subprocess.CalledProcessError as exc:
        log(f"git step failed ({exc}); PDF generated but not pushed")


def main():
    log("=== run started ===")
    today = datetime.date.today().strftime("%Y-%m-%d")
    store = load_json(STORE, {"days": {}, "seen_urls": []})
    days = store.setdefault("days", {})
    seen = set(store.setdefault("seen_urls", []))

    added = 0
    already_ran_today = today in days and "--force" not in sys.argv
    if "--rebuild" not in sys.argv and not already_ran_today:
        todays = days.setdefault(today, [])
        for it in fetch_headlines():
            if it["url"] in seen:
                continue
            seen.add(it["url"])
            todays.append(it)
            added += 1
        if not todays:            # keep store tidy — drop an empty today key
            days.pop(today, None)
        store["seen_urls"] = sorted(seen)
        STORE.write_text(json.dumps(store, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    elif already_ran_today:
        log("already ran today; re-rendering only (use --force to re-mine)")

    MD_OUT.write_text(build_markdown(store, today), encoding="utf-8")
    pdf = render_pdf()
    log(f"merged {added} new; {sum(len(v) for v in days.values())} daily-update "
        f"items total -> {PDF_OUT.name if pdf else 'PDF FAILED'}")

    if "--no-push" not in sys.argv and pdf:
        git_push(today)
    log("=== run finished ===")


if __name__ == "__main__":
    main()
