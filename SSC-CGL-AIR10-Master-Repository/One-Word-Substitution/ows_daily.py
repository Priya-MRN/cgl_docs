#!/usr/bin/env python3
"""
One-Word Substitution (OWS) — Daily Builder
===========================================
Maintains ONE self-contained HTML file of One-Word-Substitution entries
(phrase -> single word), seeded from the SSC-CGL PYQ papers and related word
banks, grouped by theme, deduped, with TODAY's new words highlighted.

Each entry: { word, phrase, meaning, source, added (YYYY-MM-DD) }.

Daily update: drop new phrase/word pairs (e.g. mined from newspapers, articles,
speeches, books) into  new_today.json  as a list of
  {"word": "...", "phrase": "...", "meaning": "...", "source": "..."}
then run:  py ows_daily.py
New, non-duplicate entries are merged, stamped with today's date, highlighted in
the HTML, and the file is rewritten.

Run:  py ows_daily.py            (merge new_today.json + rebuild)
      py ows_daily.py --rebuild  (just rebuild HTML from the store)
"""
import re
import sys
import json
import html as _html
import datetime
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent))  # repo root, for html_to_pdf
from html_to_pdf import html_to_pdf  # noqa: E402

STORE = BASE_DIR / "ows_store.json"          # canonical deduped entries
NEW_TODAY = BASE_DIR / "new_today.json"      # drop-box for today's additions
OUTPUT = BASE_DIR / "One_Word_Substitution.html"
LOG = BASE_DIR / "run.log"


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
# Grouping by theme — first matching rule wins; phrase + word + meaning matched
# ---------------------------------------------------------------------------
OTHER = "🗂️ Other & Mixed"
GROUPS = [
    ("🔬 Study of / Science of (-logy, -ist)",
     r"\b(one who studies|study of|science of|expert in|-logy|specialist)\b"),
    ("👤 People, Professions & Roles",
     r"\b(one who|a person who|someone who|people who|one that)\b"),
    ("😱 Fears & Phobias",
     r"\b(fear of|dread of|phobia|hatred of|hater of)\b"),
    ("🏛️ Government & Rule (-cracy, -archy)",
     r"\b(government by|rule by|rule of|-cracy|-archy|state )\b"),
    ("🏠 Places & Buildings",
     r"\b(a place where|place for|building where|room where|home for)\b"),
    ("🐾 Animals, Groups & Sounds",
     r"\b(group of|collection of|young of|sound of|cry of|animal|home of)\b"),
    ("🩺 Medicine, Body & Death",
     r"\b(medicine|disease|cure|kills|death|killing|murder|body|study of life)\b"),
    ("📜 Words, Speech & Writing",
     r"\b(speech|words|writing|written|book|language|talk|study of words)\b"),
    ("⏳ Time, Age & Period",
     r"\b(time|period|years|age|lasting|happening every|once in)\b"),
    ("⚖️ Belief, Religion & Morals",
     r"\b(belief|believe|god|religion|faith|moral|sin|worship)\b"),
    ("💍 Marriage & Relationships",
     r"\b(marriage|married|wife|husband|widow|unmarried|spouse)\b"),
    ("🍽️ Food & Eating",
     r"\b(eats|eating|feeds on|food|diet|flesh)\b"),
]
# Gen-Z / internet slang is NOT exam OWS — kept in its own section at the end so
# it never mixes into SSC prep. Entries opt in via "category" == GENZ.
GENZ = "🔥 Gen-Z / Internet Slang (not exam OWS)"
GROUP_ORDER = [g for g, _ in GROUPS] + [OTHER, GENZ]


def group_for(e):
    # An explicit category (e.g. Gen-Z) always wins over keyword detection.
    if e.get("category"):
        return e["category"]
    text = (e.get("phrase", "") + " " + e.get("word", "") + " " +
            e.get("meaning", "")).lower()
    for name, pat in GROUPS:
        if re.search(pat, text):
            return name
    return OTHER


def _anchor(heading):
    """GitHub/VS Code slug: lowercase, drop emoji/punct in place, spaces->'-'."""
    t = heading.strip().lower()
    t = re.sub(r"[^\w \-]", "", t, flags=re.UNICODE)
    t = re.sub(r"[^\x00-\x7f]", "", t)
    return t.strip().replace(" ", "-")


def _esc(s):
    return _html.escape(s or "", quote=False)


PAGE_CSS = """
  :root{ --ink:#1a1a2e; --accent:#7b2d8e; }
  body{ font-family:"Segoe UI",Arial,sans-serif; color:var(--ink); max-width:1000px;
        margin:0 auto; padding:28px; line-height:1.5; }
  h1{ color:#fff; background:linear-gradient(135deg,#4a148c,#7b2d8e); padding:18px 22px;
      border-radius:12px; font-size:1.6em; }
  h2{ color:#4a148c; border-left:7px solid var(--accent); padding:6px 12px;
      background:#f7f1fb; border-radius:0 8px 8px 0; margin-top:30px; scroll-margin-top:14px; }
  blockquote{ background:#fff8e1; border-left:5px solid #f1c40f; margin:12px 0;
      padding:10px 16px; border-radius:0 8px 8px 0; }
  table{ border-collapse:collapse; width:100%; margin:12px 0; font-size:.95em; }
  th{ background:#4a148c; color:#fff; text-align:left; padding:8px 11px; }
  td{ border:1px solid #e0d4ea; padding:7px 11px; vertical-align:top; }
  tr:nth-child(even){ background:#faf6fd; }
  a{ color:#4a148c; text-decoration:none; } a:hover{ text-decoration:underline; }
  .count{ text-align:center; font-weight:600; }
  .backtop{ font-size:.8em; }
  /* TODAY's new words highlighted */
  tr.today{ background:#fff3cd !important; }
  tr.today td:first-child::after{ content:" 🆕"; }
  .newbadge{ background:#e67e22; color:#fff; border-radius:6px; padding:1px 8px;
      font-size:.8em; margin-left:8px; }
  hr{ border:0; border-top:2px dashed #e0d4ea; margin:22px 0; }
"""


def write_html(entries, today_str):
    buckets = defaultdict(list)
    for e in entries:
        buckets[group_for(e)].append(e)
    used = [g for g in GROUP_ORDER if buckets[g]]
    today_count = sum(1 for e in entries if e.get("added") == today_str)

    p = ["<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width, initial-scale=1'>",
         "<title>One-Word Substitution — Master List</title>",
         f"<style>{PAGE_CSS}</style></head><body>",
         "<h1>🎯 One-Word Substitution — Master List</h1>"]
    badge = (f"<span class='newbadge'>{today_count} new today</span>"
             if today_count else "")
    p.append(
        f"<blockquote><strong>{len(entries)} unique substitutions</strong>{badge}, "
        "grouped by theme, sourced from SSC-CGL PYQ papers + word banks, updated "
        "daily from newspapers, articles, speeches & books. "
        "Rows added <strong>today are highlighted</strong> 🆕.<br><br>"
        "<strong>How to use:</strong> read the phrase, cover the word, recall it. "
        "Learn each theme as a family.</blockquote>")

    p.append("<h2 id='contents'>🧭 Contents</h2>")
    p.append("<table><thead><tr><th>#</th><th>Theme</th><th>Words</th>"
             "<th>New</th></tr></thead><tbody>")
    for i, g in enumerate(used, 1):
        n_new = sum(1 for e in buckets[g] if e.get("added") == today_str)
        p.append(f"<tr><td class='count'>{i}</td>"
                 f"<td><a href='#{_anchor(g)}'>{_esc(g)}</a></td>"
                 f"<td class='count'>{len(buckets[g])}</td>"
                 f"<td class='count'>{n_new or ''}</td></tr>")
    p.append("</tbody></table>")

    for g in used:
        p.append(f"<h2 id='{_anchor(g)}'>{_esc(g)} "
                 "<a class='backtop' href='#contents'>↑ top</a></h2>")
        p.append("<table><thead><tr><th>Phrase / Expression</th><th>One Word</th>"
                 "<th>Meaning / Hook</th><th>Source</th></tr></thead><tbody>")
        for e in sorted(buckets[g], key=lambda x: x["word"].lower()):
            cls = " class='today'" if e.get("added") == today_str else ""
            p.append(
                f"<tr{cls}><td>{_esc(e.get('phrase',''))}</td>"
                f"<td><strong>{_esc(e['word'])}</strong></td>"
                f"<td>{_esc(e.get('meaning',''))}</td>"
                f"<td>{_esc(e.get('source',''))}</td></tr>")
        p.append("</tbody></table>")

    p.append("<hr><p><strong>Sources:</strong> SSC-CGL PYQ papers, curated word "
             "banks; daily additions from newspapers, articles, speeches & books.</p>")
    p.append("</body></html>")
    OUTPUT.write_text("\n".join(p), encoding="utf-8")
    return today_count


def main():
    log("=== OWS build started ===")
    today = datetime.date.today().strftime("%Y-%m-%d")
    store = load_json(STORE, {"entries": []})
    entries = store.get("entries", [])
    have = {e["word"].lower() for e in entries}

    added = 0
    if "--rebuild" not in sys.argv:
        for e in load_json(NEW_TODAY, []):
            w = (e.get("word") or "").strip()
            if not w or w.lower() in have:
                continue
            have.add(w.lower())
            entries.append({"word": w, "phrase": e.get("phrase", ""),
                            "meaning": e.get("meaning", ""),
                            "source": e.get("source", "Daily (newspaper/article)"),
                            "added": today})
            added += 1
        store["entries"] = entries
        STORE.write_text(json.dumps(store, ensure_ascii=False, indent=2),
                         encoding="utf-8")
        # clear the drop-box so the same words aren't re-flagged tomorrow
        NEW_TODAY.write_text("[]", encoding="utf-8")

    n_today = write_html(entries, today)
    log(f"Merged {added} new; {len(entries)} total; {n_today} highlighted today "
        f"-> {OUTPUT.name}")
    html_to_pdf(OUTPUT, delete_html=True, log=log)  # mobile-friendly PDF; drop HTML
    log("=== OWS build finished ===")


if __name__ == "__main__":
    main()
