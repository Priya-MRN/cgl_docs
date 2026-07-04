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
sys.path.insert(0, str(BASE_DIR.parent))  # repo root, for html_to_pdf
from html_to_pdf import html_to_pdf  # noqa: E402

WORD_BANK_FILE = BASE_DIR / "word_bank.json"
USED_WORDS_FILE = BASE_DIR / "used_words.json"
OUTPUT_DIR = BASE_DIR / "Daily-Words"
# Single master file that is OVERWRITTEN each day. All words ever produced are
# merged into it, deduped, and grouped by meaning (similar words together).
# Output is a self-contained HTML page (with working in-page anchors) — no .md.
MASTER_FILE = OUTPUT_DIR / "Editorial_Vocabulary.html"
# Canonical store backing the master file (the words + which days they came in).
MASTER_STORE = BASE_DIR / "master_words.json"
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
# Grouping: cluster similar words by meaning so they sit together
# ---------------------------------------------------------------------------
# Ordered theme groups. First matching rule wins; anything unmatched lands in
# OTHER. Each rule is matched against the lowercased "meaning + easy synonyms".
OTHER_GROUP = "Other & Mixed"
GROUPS = [
    ("📉 Decline, Fall & Weaken",
     r"\b(fall|fell|drop|decline|decrease|weak|weaken|shrink|reduce|wear away|"
     r"fade|lessen|subside|run low|wither|collapse|crash|dive|tumble|sink)\b"),
    ("📈 Increase, Rise & Spread",
     r"\b(increase|rise|spread|grow|multiply|spike|surge|momentum|push|"
     r"widespread|everywhere|unchecked|rampant)\b"),
    ("🗯️ Criticism & Condemnation",
     r"\b(criticis|criticize|condemn|attack|scold|rant|harsh|smear|defame|"
     r"lament|complain|blame|denounce|indict)\b"),
    ("👏 Praise, Support & Strengthen",
     r"\b(praise|support|strengthen|boost|reinforce|encourage|back|champion|"
     r"promote|nurture|foster|empower|endorse|loyal|approve|welcome|embrace)\b"),
    ("🚧 Block, Hinder & Suppress",
     r"\b(block|hinder|obstruct|prevent|slow|stop|suppress|choke|restrict|"
     r"thwart|foil|limit|restrain|control|curb|cut short|impede|stymie)\b"),
    ("⚔️ Conflict, Crisis & Disorder",
     r"\b(conflict|crisis|chaos|unrest|disorder|turmoil|riot|deadlock|impasse|"
     r"havoc|war|trouble|ruin|curse|mess|disturbance|upset)\b"),
    ("💥 Harm, Damage & Worsen",
     r"\b(harm|damage|spoil|ruin|worsen|aggravate|inflict|disable|"
     r"endanger|risk|sabotage|undermine|cripple)\b"),
    ("🔥 Severity, Seriousness & Urgency",
     r"\b(severe|serious|strict|tough|grave|urgent|extreme|intense|"
     r"stern|sharp|gloomy|grim|bleak|stark|dire|acute|fierce|forceful)\b"),
    ("❓ Difference, Disagreement & Doubt",
     r"\b(difference|differ|disagree|dispute|controvers|gap|inequalit|"
     r"oddit|irregularit|unclear|hazy|vague|doubt|sceptic|distrust|cynical)\b"),
    ("🌱 Beginnings, Change & Turning Points",
     r"\b(begin|new|emerging|start|spark|trigger|catalyst|revival|comeback|"
     r"turning point|milestone|reform|revamp|change|ignite|introduce|herald|usher)\b"),
    ("💰 Wealth, Money & Economy",
     r"\b(money|profit|wealth|wealthy|rich|prosperous|economic|cutbacks|thrift|"
     r"lucrative|affluent|waste)\b"),
    ("🎯 Skill, Care & Wisdom",
     r"\b(skill|skilled|expert|careful|thorough|wise|sensible|practical|"
     r"nimble|adept|deft|prudent|painstaking)\b"),
    ("🗣️ Speech, Persuasion & Claims",
     r"\b(say|said|speech|claim|accuse|promise|pledge|beg|plead|repeat|restate|"
     r"persuasive|oratory|rhetoric|implied|unspoken|appeal)\b"),
    ("⚡ Strong Feeling, Energy & Zeal",
     r"\b(passion|passionate|enthusiasm|energy|eager|zeal|fervour|fervent|"
     r"intense feeling|courage|stir|spur)\b"),
    ("🔍 Examination, Judgement & Standards",
     r"\b(examin|inspect|review|investigat|inquiry|measure|assess|judge|"
     r"benchmark|standard|scrutiny|gauge|probe|yardstick)\b"),
    ("🤝 Agreement, Unity & Cooperation",
     r"\b(agreement|agree|unity|unite|together|alliance|union|accord|"
     r"cooperat|coalition|consensus|cohesion|reconcile|harmonis|settle)\b"),
    ("⭐ Certainty, Importance & Authority",
     r"\b(certain|unavoidable|inevitable|order|authority|duty|burden|"
     r"responsib|supreme|chief|most important|paramount|mandate|onus)\b"),
    ("🌫️ Hidden, Unclear & Secret",
     r"\b(hidden|secret|dormant|implied|unseen|murky|disguise|conceal|"
     r"latent|veneer|facade|opaque|obscure)\b"),
    ("🧱 Real, Concrete & Practical",
     r"\b(real|concrete|clearly seen|practical|relevant|apt|sturdy|"
     r"strong and healthy|tangible|robust|pertinent|salient)\b"),
    ("✊ Reject, Revenge & Force",
     r"\b(reject|refuse|revenge|retaliat|seize|grab|by force|surrender|yield|"
     r"give up|spurn|wrest|cede|reprisal|forfeit)\b"),
    ("⏳ Time, Lateness & Approach",
     r"\b(soon|near|approach|impending|about to happen|late|overdue|short time|"
     r"forerunner|omen|imminent|looming|belated|harbinger|aftermath|brief|"
     r"lasting|temporary|fleeting|ephemeral)\b"),
    ("🎭 Lies, Trickery & Deception",
     r"\b(lie|telling the truth|not telling|fake|falsehood|deceive|deceiv|"
     r"trick|trickery|cheat|flatter|not genuine|forge|fraud|mislead|pretend|"
     r"sham|hypocri|spurious|specious|dishonest|fabricat)\b"),
    ("🧗 Problems, Obstacles & Setbacks",
     r"\b(problem|obstacle|difficulty|setback|hurdle|barrier|delay|"
     r"backlash|flaw|fault|weakness|drawback|snag|complicat|stumbling)\b"),
    ("🧠 Thinking, Reasoning & Memory",
     r"\b(think|consider|ponder|reflect|reason|deduce|infer|recall|"
     r"remember|deliberat|contemplat|mull|reckon|weigh|conclude|surmise)\b"),
    ("⚖️ Fairness, Honesty & Truth",
     r"\b(fair|just|honest|truth|frank|candid|sincere|impartial|"
     r"unbiased|equitable|credible|integrity|forthright|transparent)\b"),
    ("🌀 Hostility, Bitterness & Stubbornness",
     r"\b(hostile|bitter|angry|stubborn|defiant|obstinate|grudge|"
     r"acrimon|inimical|recalcitrant|vituperat|spite|malice|enmity|grievance)\b"),
    ("👑 Power, Control & Influence",
     r"\b(power|control|influence|authority|dominate|rule|sway|grip|"
     r"clout|command|wield|oust|depose|reign|leverage)\b"),
    ("😀 Hope, Calm & Positivity",
     r"\b(hope|hopeful|optimis|cheerful|calm|composed|serene|positive|"
     r"upbeat|sanguine|buoyant|content|reassur|soothe|placate)\b"),
    ("🌑 Bad, Harmful & Unpleasant",
     r"\b(bad|harmful|unpleasant|nasty|wicked|evil|shameless|disgust|"
     r"notorious|infamous|egregious|flagrant|adverse|inimical|innocuous|"
     r"shocking|brazen|wanton)\b"),
    ("📦 Amount, Size & Plenty",
     r"\b(amount|plenty|plentiful|enough|abundant|ample|large|huge|"
     r"countless|myriad|scarce|meagre|scanty|hefty|sparse|copious|surplus)\b"),
    ("🪞 Difference, Comparison & Opposite",
     r"\b(opposite|contrast|compare|comparison|side by side|model|pattern|"
     r"typical example|antithesis|paradigm|juxtapose|quintessential|analog)\b"),
    ("🗃️ Catch, Hold & Seize",
     r"\b(catch|arrest|hold|grip|grab|capture|seize|cling|stick to|"
     r"adhere|abide|nab|clutch|grasp)\b"),
    ("📌 Cause, Effect & Consequence",
     r"\b(cause|lead to|result|consequence|effect|outcome|trigger|"
     r"bring about|repercussion|backlash|breed|stem from)\b"),
    ("🔺 Highest & Lowest Points",
     r"\b(highest|lowest|peak|summit|climax|final point|top point|"
     r"worst point|most successful|reach a final|zenith|nadir|heyday|"
     r"pinnacle|juncture|culminat|apex)\b"),
    ("🍀 Luck, Chance & Fate",
     r"\b(luck|lucky|unlucky|chance|fate|fortune|misfortune|by chance|"
     r"fortuitous|hapless|serendip|providence|destiny)\b"),
    ("🗨️ Talkative, Loud & Wordy",
     r"\b(talkative|talking a lot|wordy|loud|chatty|verbose|long-winded|"
     r"loquacious|garrulous|vociferous|voluble|fancy.*language|florid)\b"),
    ("😢 Sadness, Regret & Complaint",
     r"\b(sad|sadness|sorrow|grief|mourn|regret|tearful|gloom|"
     r"lament|lachrymose|querulous|melanchol|woe|despair)\b"),
    ("🦅 Boldness, Recklessness & Daring",
     r"\b(bold|daring|reckless|rash|without thinking|fearless|"
     r"audacious|impetuous|headlong|brash|intrepid|temerity)\b"),
    ("😨 Shyness, Caution & Restraint",
     r"\b(shy|timid|cautious|reserved|restraint|hesitant|reluctant|"
     r"diffident|wary|coy|demure|circumspect)\b"),
    ("🪢 Unity, Sameness & Division",
     r"\b(same|alike|uniform|identical|split|divide|separate|opposing groups|"
     r"homogeneous|polaris|cleave|dissent|schism|fragment)\b"),
    ("🛠️ Correct, Fix & Improve",
     r"\b(correct|fix|repair|mend|improve|set right|put right|amend|"
     r"rectify|redress|remedy|restore|refine|ameliorate)\b"),
    ("🎚️ Use, Need & Involve",
     r"\b(use up|involve|require|need|depend|entail|consume|exhaust|"
     r"deplete|necessitate|hinge|utilise)\b"),
    ("🚫 Useless, Hopeless & Empty",
     r"\b(useless|pointless|hopeless|in vain|empty|worthless|"
     r"futile|fruitless|vain|barren|hollow|inane)\b"),
    ("🧩 Complicated, Confusing & Vague",
     r"\b(complicated|complex|confusing|tangled|maze|intricate|"
     r"labyrinth|convoluted|perplex|baffl|ambiguous|equivocal)\b"),
    ("🌟 Quality, Character & Behaviour",
     r"\b(behaviour|character|nature|trait|quality|manner|attitude|temperament|"
     r"disposition|conduct|personality)\b"),
]
GROUP_ORDER = [name for name, _ in GROUPS] + [OTHER_GROUP]


def group_for(entry):
    text = (entry.get("meaning", "") + " " + entry.get("easy", "")).lower()
    for name, pattern in GROUPS:
        if re.search(pattern, text):
            return name
    return OTHER_GROUP


def _split_emoji(group):
    """Group names are stored as '<emoji> Text'. Return (emoji, text)."""
    m = re.match(r"^([^\w\s]+(?:️)?)\s+(.*)$", group)
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return "", group.strip()


def _anchor(heading):
    """Reproduce the GitHub / VS Code heading-slug algorithm EXACTLY so the
    Contents links always match the rendered heading anchors:
      1. lowercase
      2. remove every char that is not a letter, number, space or hyphen
         (emoji, '&', ',', etc. are deleted IN PLACE — surrounding spaces stay)
      3. turn each space into a single hyphen
    Note: 'Fall & Weaken' -> 'fall  weaken' -> 'fall--weaken' (double hyphen),
    which is what the renderers actually produce. Matching it is what makes the
    links work."""
    text = heading.strip().lower()
    text = re.sub(r"[^\w \-]", "", text, flags=re.UNICODE)   # delete punctuation/emoji in place
    text = re.sub(r"[^\x00-\x7f]", "", text)                  # drop any remaining non-ascii (accents)
    return text.replace(" ", "-")


# ---------------------------------------------------------------------------
# Output: the SINGLE master file (overwritten each run) as a self-contained,
# styled HTML page with working in-page anchor links.
# ---------------------------------------------------------------------------
import html as _html

_PAGE_CSS = """
  :root{ --ink:#1a1a2e; --accent:#c0392b; }
  body{ font-family:"Segoe UI",Arial,sans-serif; color:var(--ink); max-width:1000px;
        margin:0 auto; padding:28px; line-height:1.5; }
  h1{ color:#fff; background:linear-gradient(135deg,#16213e,#0f3460); padding:18px 22px;
      border-radius:12px; font-size:1.6em; }
  h2{ color:#0f3460; border-left:7px solid var(--accent); padding:6px 12px;
      background:#f3f6fb; border-radius:0 8px 8px 0; margin-top:30px; scroll-margin-top:14px; }
  blockquote{ background:#fff8e1; border-left:5px solid #f1c40f; margin:12px 0;
      padding:10px 16px; border-radius:0 8px 8px 0; }
  table{ border-collapse:collapse; width:100%; margin:12px 0; font-size:.95em; }
  th{ background:#0f3460; color:#fff; text-align:left; padding:8px 11px; }
  td{ border:1px solid #d0d7e2; padding:7px 11px; vertical-align:top; }
  tr:nth-child(even){ background:#f5f8fc; }
  a{ color:#0f3460; text-decoration:none; }
  a:hover{ text-decoration:underline; }
  .toc th,.toc td{ }
  .count{ text-align:center; font-weight:600; }
  .backtop{ font-size:.8em; }
  /* TODAY's newly-added words highlighted */
  tr.today{ background:#fff3cd !important; }
  tr.today td:first-child::after{ content:" 🆕"; }
  .newbadge{ background:#e67e22; color:#fff; border-radius:6px; padding:1px 8px;
      font-size:.8em; margin-left:8px; }
  hr{ border:0; border-top:2px dashed #cfd8e3; margin:22px 0; }
"""


def _esc(s):
    return _html.escape(s or "", quote=False)


def write_master(words, days, today_str=None):
    """Render every unique word into ONE self-contained, grouped HTML page.
    Words whose 'added' == today_str are highlighted as TODAY's new words."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    from collections import defaultdict
    buckets = defaultdict(list)
    for e in words:
        buckets[group_for(e)].append(e)
    used_groups = [g for g in GROUP_ORDER if buckets[g]]
    today_count = sum(1 for e in words if e.get("added") == today_str) if today_str else 0

    p = []
    p.append("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>")
    p.append("<meta name='viewport' content='width=device-width, initial-scale=1'>")
    p.append("<title>Daily Editorial Vocabulary — Master List</title>")
    p.append(f"<style>{_PAGE_CSS}</style></head><body>")
    p.append("<h1>📚 Daily Editorial Vocabulary — Master List</h1>")
    badge = (f"<span class='newbadge'>{today_count} new today</span>"
             if today_count else "")
    p.append(
        f"<blockquote><strong>{len(words)} unique words</strong>{badge}, grouped by "
        "meaning so similar words sit together. Updated daily — new words are "
        "merged in, duplicates are never repeated. Rows added <strong>today are "
        "highlighted</strong> 🆕.<br><br><strong>How to use:</strong> "
        "pick a group, read each <em>meaning</em> and <em>example</em> aloud, cover "
        "the meaning, and recall it.</blockquote>")

    # Contents (anchors target the slug of each group's text)
    p.append("<h2 id='contents'>🧭 Contents</h2>")
    p.append("<table class='toc'><thead><tr><th>#</th><th>Group</th>"
             "<th>Words</th><th>New</th></tr></thead><tbody>")
    for i, g in enumerate(used_groups, 1):
        emoji, text = _split_emoji(g)
        slug = _anchor(text)
        n_new = sum(1 for e in buckets[g] if e.get("added") == today_str) if today_str else 0
        p.append(f"<tr><td class='count'>{i}</td>"
                 f"<td><a href='#{slug}'>{_esc(g)}</a></td>"
                 f"<td class='count'>{len(buckets[g])}</td>"
                 f"<td class='count'>{n_new or ''}</td></tr>")
    p.append("</tbody></table>")

    # Group sections
    for g in used_groups:
        emoji, text = _split_emoji(g)
        slug = _anchor(text)
        p.append(f"<h2 id='{slug}'>{_esc(g)} "
                 "<a class='backtop' href='#contents'>↑ top</a></h2>")
        p.append("<table><thead><tr><th>Word</th><th>Part of Speech</th>"
                 "<th>Meaning</th><th>Easy Synonyms</th><th>Example</th>"
                 "</tr></thead><tbody>")
        for e in sorted(buckets[g], key=lambda x: x["word"].lower()):
            ex = f"<em>{_esc(e['example'])}</em>" if e.get("example") else ""
            cls = " class='today'" if e.get("added") == today_str and today_str else ""
            p.append(
                f"<tr{cls}><td><strong>{_esc(e['word'])}</strong></td>"
                f"<td>{_esc(e.get('pos',''))}</td>"
                f"<td>{_esc(e.get('meaning',''))}</td>"
                f"<td>{_esc(e.get('easy',''))}</td>"
                f"<td>{ex}</td></tr>")
        p.append("</tbody></table>")

    nice_days = ", ".join(days)
    p.append("<hr>")
    p.append(f"<p><strong>Days merged:</strong> {len(days)} ({_esc(nice_days)})<br>"
             "<strong>Sources:</strong> Curated word bank + mined editorial words.</p>")
    p.append("</body></html>")

    with open(MASTER_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(p))
    return MASTER_FILE


def update_index():
    """Point the README at the single master file."""
    store = load_json(MASTER_STORE, {"words": [], "days": []})
    lines = [
        "# Daily Editorial Vocabulary — Index",
        "",
        "Auto-generated editorial vocabulary, mined from national + "
        "international newspaper editorials with a curated SSC/UPSC fallback "
        "bank. All words are merged into **one** grouped master file (similar "
        "words together, no duplicates).",
        "",
        f"**Unique words so far:** {len(store.get('words', []))}  ",
        f"**Days merged:** {len(store.get('days', []))}",
        "",
        "👉 **[Open the master list (PDF) »](Daily-Words/Editorial_Vocabulary.pdf)** "
        "— mobile-friendly; rebuilt automatically each day.",
        "",
    ]
    with open(BASE_DIR / "README.md", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    log("=== Daily vocab run started ===")
    today = datetime.date.today()
    today_str = today.strftime("%Y-%m-%d")

    # Master store: the canonical, deduped word list + the days we've merged.
    store = load_json(MASTER_STORE, {"words": [], "days": []})
    master_words = store.get("words", [])
    days = store.get("days", [])
    have = {w["word"].lower() for w in master_words}

    if today_str in days and "--force" not in sys.argv:
        log(f"Already merged today ({today_str}). Use --force to add more.")
        return

    entries = pick_words()
    if not entries:
        log("ERROR: no words could be selected. Check word_bank.json.")
        sys.exit(1)

    # Merge ONLY genuinely new words into the master list (group similar later).
    # New words are stamped with today's date so the HTML can highlight them.
    added = 0
    for e in entries:
        if e["word"].lower() not in have:
            have.add(e["word"].lower())
            master_words.append({
                "word": e["word"], "pos": e.get("pos", ""),
                "meaning": e.get("meaning", ""), "easy": e.get("easy", ""),
                "example": e.get("example", ""), "added": today_str,
            })
            added += 1
    if today_str not in days:
        days.append(today_str)
    days = sorted(set(days))

    save_json(MASTER_STORE, {"words": master_words, "days": days})

    fname = write_master(master_words, days, today_str)
    html_to_pdf(fname, delete_html=True, log=log)  # mobile-friendly PDF; drop HTML
    log(f"Merged {added} new words ({len(master_words)} total) -> {fname.name}")

    # Keep used_words.json in sync so pick_words() never re-offers a known word.
    save_json(USED_WORDS_FILE, [w["word"] for w in master_words])

    update_index()
    log("=== Daily vocab run finished ===")


if __name__ == "__main__":
    main()
