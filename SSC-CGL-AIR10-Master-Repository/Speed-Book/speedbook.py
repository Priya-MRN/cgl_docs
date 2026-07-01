#!/usr/bin/env python3
"""
SSC CGL Speed Book — generator
==============================
Renders speedbook.json into ONE self-contained HTML revision book of high-value
SSC tricks. Every trick is a card with the fixed 7-part anatomy:

  ✅ SSC shortcut          (the rule)
  🧮 Mental calculation    (how to do it in your head)
  🔎 When to use           (trigger conditions)
  🚫 When NOT to use       (wrong contexts)
  ⚠️ Common traps          (what examiners exploit)
  📝 PYQ example           (worked, with answer)
  ❌ Where the shortcut fails (the edge case that breaks it)

Each trick object in speedbook.json:
  {
    "id": "PL-02",                 # stable id (topic-prefix + number)
    "topic": "Profit & Loss",      # group heading
    "name": "Two articles, same SP",
    "shortcut": "...", "mental": "...", "whenUse": "...", "whenNotUse": "...",
    "traps": "...", "pyq": "...", "fails": "...",
    "priority": "high"             # high | medium  (optional, for a star)
  }

Run:  py speedbook.py            (rebuild Speed-Book.html from the JSON)
Add tricks by editing speedbook.json (or dropping into new_tricks.json, then run).
"""
import re
import sys
import json
import html as _html
import datetime
from pathlib import Path
from collections import defaultdict, OrderedDict

BASE = Path(__file__).resolve().parent
DATA = BASE / "speedbook.json"
DROP = BASE / "new_tricks.json"          # optional drop-box for new tricks
OUT = BASE / "Speed-Book.html"
LOG = BASE / "run.log"

# Order topics appear in the book (anything else falls to the end, alpha).
TOPIC_ORDER = [
    "Percentage", "Profit & Loss", "Ratio & Proportion", "Average & Mixtures",
    "Simple & Compound Interest", "Time & Work", "Time, Speed & Distance",
    "Number System", "Algebra", "Geometry & Mensuration", "Trigonometry",
    "Data Interpretation",
    "Reasoning", "English", "General Awareness",
]

PARTS = [
    ("shortcut",   "✅ SSC Shortcut"),
    ("mental",     "🧮 Mental Calculation"),
    ("whenUse",    "🔎 When to Use"),
    ("whenNotUse", "🚫 When NOT to Use"),
    ("traps",      "⚠️ Common Traps"),
    ("pyq",        "📝 PYQ Example"),
    ("fails",      "❌ Where the Shortcut Fails"),
]


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


def _anchor(s):
    t = re.sub(r"[^\w \-]", "", s.lower(), flags=re.UNICODE)
    t = re.sub(r"[^\x00-\x7f]", "", t)
    return t.strip().replace(" ", "-")


CSS = """
  :root{ --ink:#1a1a2e; --accent:#c0392b; }
  body{ font-family:"Segoe UI",Arial,sans-serif; color:var(--ink); max-width:1000px;
        margin:0 auto; padding:28px; line-height:1.5; }
  h1{ color:#fff; background:linear-gradient(135deg,#7d1128,#c0392b); padding:18px 22px;
      border-radius:12px; font-size:1.6em; }
  h2{ color:#7d1128; border-left:7px solid var(--accent); padding:6px 12px;
      background:#fdeff0; border-radius:0 8px 8px 0; margin-top:34px; scroll-margin-top:14px; }
  blockquote{ background:#fff8e1; border-left:5px solid #f1c40f; margin:12px 0;
      padding:10px 16px; border-radius:0 8px 8px 0; }
  .card{ border:1px solid #e3c9cd; border-radius:10px; padding:0; margin:16px 0;
      overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,.06); }
  .card h3{ margin:0; padding:10px 16px; background:#7d1128; color:#fff; font-size:1.05em; }
  .card .id{ font-size:.8em; opacity:.8; font-weight:normal; }
  .star{ color:#ffd166; }
  table.parts{ border-collapse:collapse; width:100%; margin:0; }
  table.parts td{ border-top:1px solid #eee; padding:8px 14px; vertical-align:top; font-size:.95em; }
  table.parts td.k{ width:210px; font-weight:600; color:#7d1128; background:#fcf5f6; white-space:nowrap; }
  td.pyq{ background:#f3f8ff; }
  td.fail{ background:#fff4f4; }
  a{ color:#7d1128; text-decoration:none; } a:hover{ text-decoration:underline; }
  .count{ text-align:center; font-weight:600; }
  .backtop{ font-size:.75em; font-weight:normal; }
  hr{ border:0; border-top:2px dashed #e3c9cd; margin:22px 0; }
"""


def topic_key(t):
    return (TOPIC_ORDER.index(t) if t in TOPIC_ORDER else len(TOPIC_ORDER), t)


def render(tricks):
    buckets = defaultdict(list)
    for t in tricks:
        buckets[t.get("topic", "Misc")].append(t)
    topics = sorted(buckets, key=topic_key)

    p = ["<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>",
         "<meta name='viewport' content='width=device-width, initial-scale=1'>",
         "<title>SSC CGL Speed Book — Tricks &amp; Shortcuts</title>",
         f"<style>{CSS}</style></head><body>",
         "<h1>⚡ SSC CGL Speed Book — Tricks &amp; Shortcuts</h1>"]
    p.append(
        f"<blockquote><strong>{len(tricks)} high-value tricks</strong> across "
        f"{len(topics)} topics. Each card gives the <strong>shortcut · mental "
        "calculation · when to use · when NOT to use · traps · PYQ · where it "
        "fails</strong>.<br><br><strong>How to revise:</strong> read the shortcut, "
        "cover the card, redo the PYQ in your head, and re-read <em>where it fails</em> "
        "— that line is what saves marks.</blockquote>")

    # Contents
    p.append("<h2 id='contents'>🧭 Contents</h2>")
    p.append("<table><thead><tr><th>#</th><th>Topic</th><th>Tricks</th>"
             "</tr></thead><tbody>")
    for i, t in enumerate(topics, 1):
        p.append(f"<tr><td class='count'>{i}</td>"
                 f"<td><a href='#{_anchor(t)}'>{_esc(t)}</a></td>"
                 f"<td class='count'>{len(buckets[t])}</td></tr>")
    p.append("</tbody></table>")

    # Topic sections
    for t in topics:
        p.append(f"<h2 id='{_anchor(t)}'>{_esc(t)} "
                 "<a class='backtop' href='#contents'>↑ top</a></h2>")
        for tr in sorted(buckets[t], key=lambda x: x.get("id", "")):
            star = " <span class='star'>★</span>" if tr.get("priority") == "high" else ""
            tid = f"<span class='id'>{_esc(tr.get('id',''))}</span> " if tr.get("id") else ""
            p.append("<div class='card'>")
            p.append(f"<h3>{tid}{_esc(tr.get('name','(unnamed trick)'))}{star}</h3>")
            p.append("<table class='parts'><tbody>")
            for key, label in PARTS:
                val = tr.get(key, "").strip()
                if not val:
                    continue
                cls = "pyq" if key == "pyq" else ("fail" if key == "fails" else "")
                p.append(f"<tr><td class='k'>{label}</td>"
                         f"<td class='{cls}'>{_esc(val)}</td></tr>")
            p.append("</tbody></table></div>")

    p.append("<hr><p><strong>Goal:</strong> 200–300 tricks by exam time. Add new ones "
             "to <code>speedbook.json</code> (or <code>new_tricks.json</code>) and run "
             "<code>py speedbook.py</code>.</p>")
    p.append("</body></html>")
    OUT.write_text("\n".join(p), encoding="utf-8")


def main():
    log("=== Speed Book build started ===")
    data = load_json(DATA, {"tricks": []})
    tricks = data.get("tricks", [])
    ids = {t.get("id") for t in tricks if t.get("id")}

    # merge optional drop-box (new tricks), skipping duplicate ids
    added = 0
    for nt in load_json(DROP, []):
        if nt.get("id") and nt["id"] in ids:
            continue
        ids.add(nt.get("id"))
        tricks.append(nt)
        added += 1
    if added:
        data["tricks"] = tricks
        DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        DROP.write_text("[]", encoding="utf-8")

    render(tricks)
    log(f"Merged {added} new; {len(tricks)} tricks total -> {OUT.name}")
    log("=== Speed Book build finished ===")


if __name__ == "__main__":
    main()
