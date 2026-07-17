"""
Political Reforms & Reformers — curated base + daily auto-update.

A STATIC-GK / POLITY study document pairing a frozen, hand-verified base
(Chief Ministers, Union Ministers and historic reformers — with person /
designation / state of working / state of birth / age / years in office /
reform / motto / theme / beneficiaries) with a DAILY-updated feed of fresh
political & reform headlines mined from GKToday.

Each run:
  1. mines GKToday homepage headlines, keeps only the ones relevant to this
     document's scope (CM/minister appointments & oaths, state schemes,
     reforms & bills, cabinet decisions, party/legislature news), tags each
     with the state it concerns where detectable,
  2. merges the deduped new items into political_reforms_store.json (grouped
     by the date first seen),
  3. renders ONE combined, mobile-friendly PDF:
        [ frozen curated base ]  +  [ Daily Updates, newest date first ]
        +  a running "Coverage by date" index at the very end,
  4. commits AND pushes the PDF to git automatically.

COPYRIGHT-SAFE: only headlines + source links are stored — never article bodies.
The frozen base (Political-Reforms-Leaders-2Y-Base.md) is the curated,
hand-verified source; it is gitignored (PDF-only policy) and edited directly.

⚠️ ACCURACY NOTE: the daily feed is UNVERIFIED headline text. Officeholders
change (six states changed CM in 2026 alone) — when a headline signals a new
CM/minister, the BASE FILE must be hand-updated. The rendered PDF says so.

Run:  py daily_political_reforms.py            (mine + merge + render + push)
      py daily_political_reforms.py --rebuild  (re-render from the store, no fetch)
      py daily_political_reforms.py --no-push  (skip the git commit/push step)
      py daily_political_reforms.py --force    (merge again even if run already today)
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

STORE = BASE_DIR / "political_reforms_store.json"
BASE_MD = BASE_DIR / "Political-Reforms-Leaders-2Y-Base.md"   # frozen curated source (gitignored)
MD_OUT = BASE_DIR / "Political-Reforms-Leaders.md"            # working full source (gitignored)
PDF_OUT = BASE_DIR / "Political-Reforms-Leaders.pdf"          # the committed artifact
LOG = BASE_DIR / "run.log"

GK_HOME = "https://www.gktoday.in/"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def log(msg):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] Political-Reforms: {msg}"
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
# Buckets — tuned to THIS document's scope (who holds office, what reforms they
# drive). The first pattern that matches wins. Headlines matching none are
# dropped — general CA lives in the other daily digests.
# ---------------------------------------------------------------------------
BUCKETS = [
    ("👤 Appointments, Oaths & Office",
     r"\b(sworn[- ]in|swearing|takes? oath|took oath|oath of office|appointed|"
     r"resign|resignation|steps? down|new chief minister|becomes chief minister|"
     r"cabinet reshuffle|inducted|portfolio|deputy chief minister|"
     r"governor|chief minister|cm |minister of|union minister|"
     r"elected leader|floor test|vote of confidence|no.confidence)\b"),
    ("🏛️ Reforms, Bills & Laws",
     r"\b(bill|act |amendment|ordinance|law|legislation|reform|repeal|"
     r"passed by|assembly passe|tabled|enacted|notified|rules? framed|"
     r"uniform civil code|ucc|reservation|quota|policy|code)\b"),
    ("💰 Schemes & Welfare Programmes",
     r"\b(yojana|scheme|programme|program|mission|abhiyan|bharosa|thogai|"
     r"pension|subsidy|free |cash transfer|dbt|allowance|stipend|"
     r"launch(es|ed)?|rolled out|beneficiar|welfare|outlay|crore)\b"),
    ("🗳️ Elections, Assemblies & Parties",
     r"\b(election|poll|assembly|vidhan sabha|constituency|mla|mlc|mp |"
     r"lok sabha|rajya sabha|by[- ]election|bypoll|seat|majority|alliance|"
     r"coalition|party|manifesto|ballot|ecs?i|election commission|verdict)\b"),
    ("📋 Cabinet & Governance Decisions",
     r"\b(cabinet (approve|clear|decid|meeting)|council of ministers|"
     r"state government|budget|announce|nod to|clears?|sanction|"
     r"secretariat|administration|governance|task force|commission|"
     r"committee|panel)\b"),
]

# Detect which state a headline concerns, so items can be tagged.
STATES = {
    "Andhra Pradesh": r"\b(andhra|amaravati|vijayawada|naidu|tdp|ysrcp?)\b",
    "Arunachal Pradesh": r"\b(arunachal|itanagar|khandu)\b",
    "Assam": r"\b(assam|guwahati|dispur|himanta|sonowal)\b",
    "Bihar": r"\b(bihar|patna|nitish|samrat choudhary|jd\(u\)|rjd|tejashwi)\b",
    "Chhattisgarh": r"\b(chhattisgarh|raipur|vishnu deo)\b",
    "Delhi": r"\b(delhi|new delhi|rekha gupta|kejriwal|aap\b)\b",
    "Goa": r"\b(goa|panaji|sawant)\b",
    "Gujarat": r"\b(gujarat|gandhinagar|ahmedabad|bhupendra patel)\b",
    "Haryana": r"\b(haryana|chandigarh|nayab|saini)\b",
    "Himachal Pradesh": r"\b(himachal|shimla|sukhu)\b",
    "Jammu & Kashmir": r"\b(jammu|kashmir|srinagar|omar abdullah|jknc)\b",
    "Jharkhand": r"\b(jharkhand|ranchi|hemant soren|jmm)\b",
    "Karnataka": r"\b(karnataka|bengaluru|bangalore|shivakumar|siddaramaiah)\b",
    "Kerala": r"\b(kerala|thiruvananthapuram|kochi|satheesan|pinarayi|udf|ldf)\b",
    "Madhya Pradesh": r"\b(madhya pradesh|bhopal|indore|mohan yadav|chouhan)\b",
    "Maharashtra": r"\b(maharashtra|mumbai|nagpur|fadnavis|shinde|ncp|shiv sena)\b",
    "Manipur": r"\b(manipur|imphal|khemchand|biren)\b",
    "Meghalaya": r"\b(meghalaya|shillong|conrad sangma)\b",
    "Mizoram": r"\b(mizoram|aizawl|lalduhoma|zpm)\b",
    "Nagaland": r"\b(nagaland|kohima|neiphiu rio|npf|ndpp)\b",
    "Odisha": r"\b(odisha|bhubaneswar|majhi|subhadra|patnaik|bjd)\b",
    "Puducherry": r"\b(puducherry|pondicherry|rangaswamy|ainrc)\b",
    "Punjab": r"\b(punjab|amritsar|ludhiana|bhagwant mann)\b",
    "Rajasthan": r"\b(rajasthan|jaipur|bhajan lal|gehlot)\b",
    "Sikkim": r"\b(sikkim|gangtok|prem singh tamang|skm)\b",
    "Tamil Nadu": r"\b(tamil ?nadu|chennai|madras|vijay|tvk|stalin|dmk|aiadmk|"
                  r"singappen|edappadi|annamalai)\b",
    "Telangana": r"\b(telangana|hyderabad|revanth|brs|kcr)\b",
    "Tripura": r"\b(tripura|agartala|manik saha)\b",
    "Uttar Pradesh": r"\b(uttar pradesh|\bup\b|lucknow|yogi|adityanath|varanasi|noida)\b",
    "Uttarakhand": r"\b(uttarakhand|dehradun|dhami)\b",
    "West Bengal": r"\b(west bengal|bengal|kolkata|calcutta|suvendu|mamata|tmc|"
                   r"annapurna|nandigram)\b",
    "Centre": r"\b(union (govt|government|cabinet|minister)|centre|central government|"
              r"parliament|prime minister|modi|amit shah|nirmala|jaishankar|"
              r"rajnath|nadda|vaishnaw|lok sabha|rajya sabha|niti aayog)\b",
}
_STATE_RE = {name: re.compile(pat, re.I) for name, pat in STATES.items()}

# Headlines that signal an officeholder CHANGE — these need a base-file edit,
# so they get flagged loudly in the PDF rather than just listed.
ACTION_RE = re.compile(
    r"\b(sworn[- ]in|swearing|takes? oath|took oath|new chief minister|"
    r"becomes chief minister|resign|steps? down|appointed (as )?(chief minister|"
    r"governor)|cabinet reshuffle|president'?s rule)\b", re.I)

ORDER = [b for b, _ in BUCKETS]


def bucket_of(title):
    """Return the matching bucket, or None if the headline is out of scope."""
    t = title.lower()
    for name, pat in BUCKETS:
        if re.search(pat, t):
            return name
    return None


def state_of(title):
    """Best-effort: which state/UT (or the Centre) does this headline concern?"""
    hits = [name for name, rx in _STATE_RE.items() if rx.search(title)]
    if not hits:
        return None
    # A specific state beats the generic "Centre" catch-all.
    specific = [h for h in hits if h != "Centre"]
    return specific[0] if specific else "Centre"


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
        state = state_of(title)
        if state is None:           # no Indian state/Centre angle -> drop
            continue
        seen.add(url)
        out.append({"title": title, "url": url, "bucket": bucket,
                    "state": state, "action": bool(ACTION_RE.search(title))})
    log(f"scraped {len(out)} in-scope headlines")
    return out


# ---------------------------------------------------------------------------
# Markdown rendering: frozen base first, then dated daily updates, then index.
# ---------------------------------------------------------------------------
def build_markdown(store, today):
    days = store.get("days", {})   # {date: [items]}
    md = []

    # ---- 1) the frozen, curated base (verbatim) ----
    if BASE_MD.exists():
        md.append(BASE_MD.read_text(encoding="utf-8").rstrip())
    else:
        md.append("# Political Reforms & Reformers")
        md.append("")
        md.append("> _Base capsule file missing; showing daily updates only._")
    md.append("")
    md.append("---")

    # ---- 2) Daily Updates section (newest date first) ----
    md.append("# 🔄 Daily Updates — Fresh Political & Reform News")
    md.append("")
    md.append(f"> Auto-mined daily from GKToday and filtered to this document's scope "
              f"(Appointments & Oaths · Reforms, Bills & Laws · Schemes & Welfare · "
              f"Elections & Assemblies · Cabinet Decisions). "
              f"**Latest update: {today}.** Each item tagged with the **state** it concerns.")
    md.append("")
    md.append("> ⚠️ **Headlines are UNVERIFIED and copyright-safe (headline + link only).** "
              "The tables in the base capsule above are hand-verified; these daily items "
              "are not. Click through to the source before trusting any fact.")
    md.append("")
    md.append("> 🔴 **Items marked ⚡ signal an officeholder or power change** (oath, "
              "resignation, reshuffle). When one appears, **hand-update the base capsule** "
              "(`Political-Reforms-Leaders-2Y-Base.md`) — six states changed CM in 2026 "
              "alone, and a stale base is worse than no base.")
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

    # ---- 3) Running indexes at the very end ----
    md.append("---")
    md.append("## 🗓️ Daily-Update Coverage by Date (index)")
    md.append("")
    md.append("| Date | Items | ⚡ Power changes | Buckets covered |")
    md.append("|---|---|---|---|")
    for d in sorted(days, reverse=True):
        items = days[d]
        buckets = sorted({i["bucket"].split(" ", 1)[-1] for i in items})
        flags = sum(1 for i in items if i.get("action"))
        md.append(f"| {d} | {len(items)} | {flags or '—'} | {', '.join(buckets)} |")
    md.append("")

    # Coverage by state — useful for spotting which states are moving.
    by_state = {}
    for items in days.values():
        for i in items:
            by_state.setdefault(i.get("state", "—"), 0)
            by_state[i["state"]] += 1
    if by_state:
        md.append("## 🗺️ Daily-Update Coverage by State (index)")
        md.append("")
        md.append("| State / UT | Items mined |")
        md.append("|---|---|")
        for st, n in sorted(by_state.items(), key=lambda kv: (-kv[1], kv[0])):
            md.append(f"| {st} | {n} |")
        md.append("")

    total = sum(len(v) for v in days.values())
    md.append(f"> **Daily-update total:** {total} items across {len(days)} day(s), "
              f"on top of the hand-verified base capsule above.")
    md.append("")
    md.append("---")
    md.append("> Base: hand-verified against live sources (July 2026). "
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
        # Power-change items first — they're the ones needing a base edit.
        for it in sorted(group, key=lambda x: (not x.get("action"),
                                               x.get("state") or "")):
            flag = "⚡ " if it.get("action") else ""
            state = it.get("state")
            tag = f"**[{state}]** " if state else ""
            title = it["title"].replace("|", "\\|")
            md.append(f"- {flag}{tag}[{title}]({it['url']})")
        md.append("")


# ---------------------------------------------------------------------------
# Render MD -> PDF (reuse md_to_pdf's renderer + styling), delete the HTML.
# ---------------------------------------------------------------------------
def render_pdf():
    body = md_render(MD_OUT.read_text(encoding="utf-8"))
    doc = (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
           f"<title>Political Reforms &amp; Reformers</title>"
           f"{MD_CSS}</head><body>{body}</body></html>")
    html_out = MD_OUT.with_suffix(".html")
    html_out.write_text(doc, encoding="utf-8")
    return html_to_pdf(html_out, delete_html=True, log=lambda m: log(m))


# ---------------------------------------------------------------------------
# Git: commit + push the PDF automatically (from the real git root).
# ---------------------------------------------------------------------------
def git_push(today):
    rel = PDF_OUT.relative_to(GIT_ROOT).as_posix()
    store_rel = STORE.relative_to(GIT_ROOT).as_posix()
    try:
        subprocess.run(["git", "add", rel, store_rel], cwd=GIT_ROOT, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=GIT_ROOT)
        if diff.returncode == 0:
            log("no PDF changes to commit")
            return
        msg = (f"Daily Political Reforms & Reformers update — {today}\n\n"
               "Auto-generated: curated leaders/reforms capsule + daily headlines "
               "(source links).\n\n"
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

    added = flagged = 0
    already_ran_today = today in days and "--force" not in sys.argv
    if "--rebuild" not in sys.argv and not already_ran_today:
        todays = days.setdefault(today, [])
        for it in fetch_headlines():
            if it["url"] in seen:
                continue
            seen.add(it["url"])
            todays.append(it)
            added += 1
            if it.get("action"):
                flagged += 1
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
    if flagged:
        log(f"⚡ {flagged} POWER-CHANGE headline(s) today — review and hand-update "
            f"{BASE_MD.name}")

    if "--no-push" not in sys.argv and pdf:
        git_push(today)
    log("=== run finished ===")


if __name__ == "__main__":
    main()
