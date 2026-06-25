# -*- coding: utf-8 -*-
"""
INDEPENDENT verifier for the Direction Sense set.
Re-parse the WRITTEN markdown: confirm 500 Q + 500 A, keyed option value ==
stated answer string, 4 DISTINCT options each. Cross-check every key against
the JSON sidecar (written == computed) for all 500. Then INDEPENDENTLY
RE-SIMULATE the movement/turn logic from scratch (re-implemented here, NOT
imported from the generator) for the structured path carried in the sidecar
meta, and for >=100 questions confirm the simulated answer matches the key.

NO unicode emoji - plain "PASS"/"FAIL".
"""
import re
import json
import math

PATH = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_06_Direction_Sense_500.md"
SIDECAR = r"d:/Documents/cgl_docs/SSC-CGL-AIR10-Master-Repository/Practice-Sets-500/Reasoning_06_Direction_Sense_500.key.json"

# ---- independent re-implementation of the movement model ----
# +x East, +y North.
_VEC = {"North": (0, 1), "South": (0, -1), "East": (1, 0), "West": (-1, 0)}
_CW = ["North", "East", "South", "West"]
_DIR8 = {
    (0, 1): "North", (0, -1): "South", (1, 0): "East", (-1, 0): "West",
    (1, 1): "North-East", (1, -1): "South-East",
    (-1, 1): "North-West", (-1, -1): "South-West",
}


def _turn(facing, d):
    i = _CW.index(facing)
    if d == "right":
        return _CW[(i + 1) % 4]
    if d == "left":
        return _CW[(i - 1) % 4]
    if d == "around":
        return _CW[(i + 2) % 4]
    raise ValueError(d)


def _sim(start, facing, moves):
    x, y = start
    f = facing
    for mv in moves:
        kind = mv[0]
        if kind == "walk":
            _, dd, dist = mv
            vx, vy = _VEC[dd]
            x += vx * dist
            y += vy * dist
            f = dd
        elif kind == "turn_walk":
            _, td, dist = mv
            f = _turn(f, td)
            vx, vy = _VEC[f]
            x += vx * dist
            y += vy * dist
        else:
            raise ValueError(mv)
    return x, y, f


def _dir8(dx, dy):
    sx = (dx > 0) - (dx < 0)
    sy = (dy > 0) - (dy < 0)
    if sx == 0 and sy == 0:
        return "same point"
    return _DIR8[(sx, sy)]


def _fmt(x):
    if isinstance(x, float) and abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    if isinstance(x, int):
        return str(x)
    return str(x)


txt = open(PATH, encoding="utf-8").read()
sidecar = json.load(open(SIDECAR, encoding="utf-8"))

qpart, apart = txt.split("# =================== ANSWER KEY")

qs = {}
qpat = re.compile(
    r"\*\*Q(\d+)\.\*\*\s+(.*?)\n\(a\)\s*(.*?)\s\s+\(b\)\s*(.*?)\s\s+\(c\)\s*(.*?)\s\s+\(d\)\s*(.*?)\n",
    re.S,
)
for m in qpat.finditer(qpart):
    n = int(m.group(1))
    stem = m.group(2).replace("\n", " ").strip()
    opts = [m.group(3).strip(), m.group(4).strip(), m.group(5).strip(), m.group(6).strip()]
    qs[n] = (stem, opts)

ans = {}
apat = re.compile(r"\*\*Q(\d+)\.\s*\(([abcd])\)\s*(.*?)\*\*\s*\*\[")
for m in apat.finditer(apart):
    ans[int(m.group(1))] = (m.group(2), m.group(3).strip())

print(f"Parsed {len(qs)} questions, {len(ans)} answers, sidecar has {len(sidecar)} keys")
assert len(qs) == 500, f"question count {len(qs)} != 500"
assert len(ans) == 500, f"answer count {len(ans)} != 500"
assert len(sidecar) == 500, f"sidecar count {len(sidecar)} != 500"

mismatch = 0
resimulated = 0
type_counts = {}

for n in range(1, 501):
    stem, opts = qs[n]
    letter, aval = ans[n]
    li = "abcd".index(letter)
    keyed_opt = opts[li]

    # 1) keyed option string == stated answer string
    if keyed_opt != aval:
        print(f"Q{n}: keyed option[{letter}]='{keyed_opt}' != stated answer '{aval}'")
        mismatch += 1
        continue
    # 2) 4 distinct options
    if len(set(opts)) != 4:
        print(f"Q{n}: options not distinct: {opts}")
        mismatch += 1
    # 3) sidecar cross-check (written == computed)
    sc = sidecar[str(n)]
    if sc["answer"] != keyed_opt:
        print(f"Q{n}: sidecar answer '{sc['answer']}' != keyed '{keyed_opt}'")
        mismatch += 1

    # 4) INDEPENDENT re-simulation from the structured path in the sidecar meta.
    meta = sc["meta"]
    t = meta["type"]
    exp = None
    if t == "distance":
        moves = [tuple(mv) for mv in meta["moves"]]
        x, y, _ = _sim(tuple(meta["start"]), meta["facing"], moves)
        dist = round(math.hypot(x, y))
        # confirm clean integer (Pythagorean)
        if dist * dist != x * x + y * y:
            print(f"Q{n}: distance not a clean integer ({x},{y})")
            mismatch += 1
        exp = _fmt(dist) + " m"
    elif t == "direction":
        moves = [tuple(mv) for mv in meta["moves"]]
        x, y, _ = _sim(tuple(meta["start"]), meta["facing"], moves)
        exp = _dir8(x, y)
    elif t == "facing":
        f = meta["facing"]
        for td in meta["turns"]:
            f = _turn(f, td)
        exp = f
    elif t == "two_people":
        m1 = [tuple(mv) for mv in meta["m1"]]
        m2 = [tuple(mv) for mv in meta["m2"]]
        x1, y1, _ = _sim((0, 0), "North", m1)
        x2, y2, _ = _sim((0, 0), "North", m2)
        dist = round(math.hypot(x1 - x2, y1 - y2))
        if dist * dist != (x1 - x2) ** 2 + (y1 - y2) ** 2:
            print(f"Q{n}: two_people distance not clean")
            mismatch += 1
        exp = _fmt(dist) + " m"
    elif t == "howfar_dir":
        moves = [tuple(mv) for mv in meta["moves"]]
        x, y, _ = _sim(tuple(meta["start"]), meta["facing"], moves)
        # answer format "<dist> m <dir>"
        exp = f"{meta['answer_dist']} m {meta['answer_dir']}"
        # also independently confirm dist/dir from the simulation
        if meta["answer_dir"] in ("East", "West"):
            sim_dist, sim_dir = abs(x), ("East" if x > 0 else "West")
        else:
            sim_dist, sim_dir = abs(y), ("North" if y > 0 else "South")
        if f"{sim_dist} m {sim_dir}" != exp:
            print(f"Q{n}: howfar re-sim '{sim_dist} m {sim_dir}' != meta '{exp}'")
            mismatch += 1
    elif t == "net_axis":
        moves = [tuple(mv) for mv in meta["moves"]]
        x, y, _ = _sim(tuple(meta["start"]), meta["facing"], moves)
        if meta["axis"] == "NS":
            val, d = abs(y), ("North" if y > 0 else "South")
        else:
            val, d = abs(x), ("East" if x > 0 else "West")
        exp = f"{val} m {d}"
    elif t == "shadow":
        if meta["mode"] == "absolute":
            sun = meta["sun"]
            opp = {"East": "West", "West": "East", "North": "South", "South": "North"}
            exp = opp[sun]
        else:
            sun = meta["sun"]
            opp = {"East": "West", "West": "East", "North": "South", "South": "North"}
            shadow_dir = opp[sun]
            face = meta["facing"]
            rel = {
                face: "in front of him",
                _turn(face, "around"): "behind him",
                _turn(face, "right"): "to his right",
                _turn(face, "left"): "to his left",
            }
            exp = rel[shadow_dir]

    if exp is not None:
        resimulated += 1
        type_counts[t] = type_counts.get(t, 0) + 1
        if exp != keyed_opt:
            print(f"Q{n} RE-SIM[{t}]: simulated '{exp}' != keyed '{keyed_opt}'")
            mismatch += 1

print(f"Independently re-simulated {resimulated} questions from the parsed path.")
print("Re-simulated type breakdown:", type_counts)
assert resimulated >= 100, f"only {resimulated} re-simulated (<100)"

# ====================================================================
# SECOND, STRONGER PASS: parse the path purely from the STEM TEXT
# (ignoring the sidecar meta) and re-simulate. This proves the written
# English of the question is itself consistent with the keyed answer.
# ====================================================================
stem_checked = 0
stem_mismatch = 0
stem_types = {}

for n in range(1, 501):
    stem, opts = qs[n]
    letter, aval = ans[n]

    # ---- PATTERN 1: pure turn sequence ----
    # "... is facing <DIR>. He turns <t>, then turns <t>, ... facing now?"
    mface = re.search(r"is facing (North|South|East|West)\. He turns (.+?)\. "
                      r"Which direction is he facing now", stem)
    if mface:
        start_face = mface.group(1)
        seq = mface.group(2)
        turns = [w.strip() for w in re.split(r",?\s*then turns\s*", seq)]
        turns = [t for t in turns if t in ("left", "right", "around")]
        f = start_face
        for td in turns:
            f = _turn(f, td)
        if f != aval:
            print(f"Q{n} STEM turn-seq: simulated '{f}' != keyed '{aval}'")
            stem_mismatch += 1
        stem_checked += 1
        stem_types["turn_seq"] = stem_types.get("turn_seq", 0) + 1
        continue

    # ---- PATTERN 2: forward-then-turn distance ----
    # "is facing <DIR>. He walks <a> m forward, then turns <t> and walks <b> m.
    #  How far ..."
    mdt = re.search(r"is facing (North|South|East|West)\. He walks (\d+) m forward, "
                    r"then turns (left|right) and walks (\d+) m\. How far", stem)
    if mdt:
        sf, a, td, b = mdt.group(1), int(mdt.group(2)), mdt.group(3), int(mdt.group(4))
        moves = [("walk", sf, a), ("turn_walk", td, b)]
        x, y, _ = _sim((0, 0), sf, moves)
        exp = _fmt(round(math.hypot(x, y))) + " m"
        if exp != aval:
            print(f"Q{n} STEM dist-turn: simulated '{exp}' != keyed '{aval}'")
            stem_mismatch += 1
        stem_checked += 1
        stem_types["dist_turn"] = stem_types.get("dist_turn", 0) + 1
        continue

    # ---- PATTERN 3: two people from same point, perpendicular walks ----
    # "<N1> walks <a> m towards <D1>, and <N2> walks <b> m towards <D2>.
    #  What is the distance between them now?"
    mtp = re.search(r"walks (\d+) m towards (North|South|East|West), and \w+ walks "
                    r"(\d+) m towards (North|South|East|West)\. What is the distance "
                    r"between them now", stem)
    if mtp:
        a, d1d, b, d2d = int(mtp.group(1)), mtp.group(2), int(mtp.group(3)), mtp.group(4)
        x1, y1, _ = _sim((0, 0), "North", [("walk", d1d, a)])
        x2, y2, _ = _sim((0, 0), "North", [("walk", d2d, b)])
        exp = _fmt(round(math.hypot(x1 - x2, y1 - y2))) + " m"
        if exp != aval:
            print(f"Q{n} STEM two-people: simulated '{exp}' != keyed '{aval}'")
            stem_mismatch += 1
        stem_checked += 1
        stem_types["two_people"] = stem_types.get("two_people", 0) + 1
        continue

    # ---- PATTERN 4: absolute shadow ----
    msh = re.search(r"The sun is in the (North|South|East|West)\. In which direction "
                    r"does the shadow of the pole fall", stem)
    if msh:
        sun = msh.group(1)
        opp = {"East": "West", "West": "East", "North": "South", "South": "North"}
        exp = opp[sun]
        if exp != aval:
            print(f"Q{n} STEM shadow: simulated '{exp}' != keyed '{aval}'")
            stem_mismatch += 1
        stem_checked += 1
        stem_types["shadow"] = stem_types.get("shadow", 0) + 1
        continue

print(f"Re-parsed PATH FROM STEM TEXT and re-simulated {stem_checked} questions.")
print("Stem-parse type breakdown:", stem_types)
assert stem_checked >= 100, f"only {stem_checked} stem-parsed (<100)"
mismatch += stem_mismatch

print(f"Total mismatches: {mismatch}")
print("RESULT:", "PASS" if mismatch == 0 else "FAIL")
assert mismatch == 0, "verification FAILED"
