"""
Daily Current Affairs Digest — exam-oriented, auto-generated, auto-pushed.

Mines public GK/news headlines (GKToday homepage), buckets them into the
CA categories SSC actually tests — Sports · Important Days/Events · Summits ·
Agreements · Awards & Honours — each tagged India / International, then:
  1. merges deduped into ca_digest_store.json (grouped by date),
  2. renders a dated, mobile-friendly PDF (Current-Affairs-Daily-Digest.pdf),
     with a running "Coverage by date" index at the very end,
  3. commits AND pushes the PDF to git automatically.

COPYRIGHT-SAFE: only headlines + source links are stored — never article bodies.

Run:  py daily_ca_digest.py            (mine + merge + render + push)
      py daily_ca_digest.py --rebuild  (re-render from the store, no fetch)
      py daily_ca_digest.py --no-push  (skip the git commit/push step)
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

STORE = BASE_DIR / "ca_digest_store.json"
MD_OUT = BASE_DIR / "Current-Affairs-Daily-Digest.md"   # local working source (gitignored)
PDF_OUT = BASE_DIR / "Current-Affairs-Daily-Digest.pdf"  # the committed artifact
LOG = BASE_DIR / "run.log"

GK_HOME = "https://www.gktoday.in/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def log(msg):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] CA-Digest: {msg}"
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
# Buckets — the exam-focused CA categories the user asked for.
# Order matters: the first pattern that matches wins.
# ---------------------------------------------------------------------------
OTHER = "🗂️ Other Notable"
BUCKETS = [
    ("🏅 Awards & Honours",
     r"\b(award|honour|honor|prize|medal|padma|bharat ratna|gallantry|laureate|"
     r"nobel|booker|magsaysay|khel ratna|arjuna|dronacharya|conferred|felicitat)\b"),
    ("🤝 Agreements, MoUs & Recognitions",
     r"\b(mou|agreement|pact|deal|fta|cepa|ecta|treaty|signs?|signed|"
     r"partnership|accord|cooperation|collaborat|gi tag|recognition|"
     r"designat|approve[sd]?|launch(es|ed)?|inaugurat)\b"),
    ("🌐 Summits & Meetings",
     r"\b(summit|conference|meet(ing)?|g20|g7|brics|sco|asean|saarc|quad|"
     r"bilateral|dialogue|forum|session|convention)\b"),
    ("📅 Important Days & Events",
     r"\b(day|diwas|week|anniversary|jayanti|observ|celebrat|theme of|"
     r"world .* day|international .* day|national .* day)\b"),
    ("🏆 Sports",
     r"\b(cup|gold|silver|bronze|championship|olympic|paralympic|world cup|"
     r"tournament|cricket|hockey|football|badminton|tennis|chess|medal|won|"
     r"final|match|trophy|league|grand slam|title|series)\b"),
]
INDIA_HINT = re.compile(
    r"\b(india|indian|delhi|bharat|modi|isro|rbi|drdo|uidai|aadhaar|niti|"
    r"supreme court|parliament|union|centre|ministry|lok sabha|rajya sabha|"
    r"andhra|arunachal|assam|bihar|chhattisgarh|goa|gujarat|haryana|himachal|"
    r"jharkhand|karnataka|kerala|madhya pradesh|maharashtra|manipur|meghalaya|"
    r"mizoram|nagaland|odisha|punjab|rajasthan|sikkim|tamil nadu|telangana|"
    r"tripura|uttar pradesh|uttarakhand|west bengal|ladakh|kashmir|"
    r"gi tag|udan|scheme|yojana)\b", re.I)
ORDER = [b for b, _ in BUCKETS] + [OTHER]


def bucket_of(title):
    t = title.lower()
    for name, pat in BUCKETS:
        if re.search(pat, t):
            return name
    return OTHER


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
        seen.add(url)
        out.append({"title": title, "url": url,
                    "bucket": bucket_of(title), "scope": scope_of(title)})
    log(f"scraped {len(out)} headlines")
    return out


# ---------------------------------------------------------------------------
# Markdown rendering: today's digest + full history + a dated index at the end
# ---------------------------------------------------------------------------
def build_markdown(store, today):
    days = store.get("days", {})   # {date: [items]}
    md = []
    md.append("# 📰 Daily Current Affairs Digest — SSC CGL")
    md.append("")
    md.append(f"> Auto-generated exam digest. **Latest update: {today}.** "
              "Buckets: Awards & Honours · Agreements & MoUs · Summits & Meetings · "
              "Important Days & Events · Sports. Each item tagged **India / International**.")
    md.append("")
    md.append("> ⚠️ Headlines + source links only (copyright-safe). Click a headline "
              "to read the full article at the source. Verify facts before the exam.")
    md.append("")
    md.append("---")

    # ---- Today's section first ----
    today_items = days.get(today, [])
    md.append(f"## 🆕 Today — {today}")
    md.append("")
    if not today_items:
        md.append("_No new items mined today. See earlier dates below._")
        md.append("")
    else:
        _render_buckets(md, today_items)

    # ---- Recent days (most recent first, excluding today) ----
    other_dates = sorted((d for d in days if d != today), reverse=True)
    if other_dates:
        md.append("---")
        md.append("## 📚 Earlier Dates")
        md.append("")
        for d in other_dates:
            md.append(f"### {d}")
            md.append("")
            _render_buckets(md, days[d])

    # ---- Running index BY DATE at the very end (as requested) ----
    md.append("---")
    md.append("## 🗓️ Coverage by Date (index)")
    md.append("")
    md.append("| Date | Items | Buckets covered |")
    md.append("|---|---|---|")
    for d in sorted(days, reverse=True):
        items = days[d]
        buckets = sorted({i["bucket"].split(" ", 1)[-1] for i in items})
        md.append(f"| {d} | {len(items)} | {', '.join(buckets)} |")
    md.append("")
    total = sum(len(v) for v in days.values())
    md.append(f"> **Total:** {total} items across {len(days)} day(s).")
    md.append("")
    md.append("---")
    md.append("> Source: [GKToday](https://www.gktoday.in/) (headlines mined daily). "
              "For SSC CGL General Awareness. Back to "
              "[GK-Now index](README.md).")
    return "\n".join(md)


OTHER_CAP = 6   # keep the digest focused on the 5 exam buckets; cap the tail


def _render_buckets(md, items):
    for bucket in ORDER:
        group = [i for i in items if i["bucket"] == bucket]
        if not group:
            continue
        capped = bucket == OTHER and len(group) > OTHER_CAP
        shown = group[:OTHER_CAP] if capped else group
        label = f"**{bucket}**" + (f" _(top {OTHER_CAP} of {len(group)})_" if capped else "")
        md.append(label)
        md.append("")
        # India items first within each bucket, then International
        for it in sorted(shown, key=lambda x: x["scope"] != "India"):
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
           f"<title>Daily CA Digest</title>{MD_CSS}</head><body>{body}</body></html>")
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
        # nothing staged? then skip commit
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=GIT_ROOT)
        if diff.returncode == 0:
            log("no PDF changes to commit")
            return
        msg = (f"Daily CA digest — {today}\n\n"
               "Auto-generated current-affairs digest (headlines + source links).\n\n"
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
    store = load_json(STORE, {"days": {}, "seen_urls": []})
    days = store.setdefault("days", {})
    seen = set(store.setdefault("seen_urls", []))

    added = 0
    if "--rebuild" not in sys.argv:
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

    MD_OUT.write_text(build_markdown(store, today), encoding="utf-8")
    pdf = render_pdf()
    log(f"merged {added} new; {sum(len(v) for v in days.values())} total -> "
        f"{PDF_OUT.name if pdf else 'PDF FAILED'}")

    if "--no-push" not in sys.argv and pdf:
        git_push(today)
    log("=== run finished ===")


if __name__ == "__main__":
    main()
