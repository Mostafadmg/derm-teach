#!/usr/bin/env python3
"""v3 'visual steps' transformer.

Turns one condition JSON (content/conditions/<slug>.json, the schema in ADD_CONDITION.md) into the
step structure the v3 condition template renders:

    overview → why → what you’ll see → confirm → lookalikes → treat → refer → pearls → self-check

* If a curated overlay exists (content/steps/<slug>.json) it wins, key by key.
* Anything the overlay does not set is derived automatically from the section JSON (derive()).
* The original sections are never rewritten: build.py renders them verbatim in each step's
  'More detail' block (SECTION_TO_STEP), so no clinical content can be lost by condensing.

CLI:
    python3 tools/v3/to_steps.py                 # write content/steps/_auto/<slug>.json for every page
    python3 tools/v3/to_steps.py psoriasis acne-vulgaris
    python3 tools/v3/to_steps.py --report        # coverage: which pages are curated / auto, photo groups placed
The _auto files are review drafts: copy one to content/steps/<slug>.json and condense it to curate a page.
Pure standard library; safe to re-run (idempotent, writes only under content/steps/_auto/).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "content"
STEPS_DIR = CONTENT / "steps"

STEPS = [  # (key, anchor, title, short label) — teaching order of a lesson
    ("glance", "overview", "Overview", "Overview"),
    ("cause", "cause", "Why it happens", "Why"),
    ("features", "features", "What you’ll see", "See"),
    ("confirm", "diagnosis", "Confirm the diagnosis", "Confirm"),
    ("differentials", "differentials", "Lookalikes", "Lookalikes"),
    ("manage", "management", "Treat", "Treat"),
    ("refer", "red-flags", "Red flags & referral", "Refer"),
    ("pearls", "pearls", "Prescriber pearls", "Pearls"),
    ("quiz", "self-check", "Quick self-check", "Self-check"),
]
# which original sections are shown verbatim under each step's "More detail" (id = old section anchor)
SECTION_TO_STEP = {
    "glance": [("what", "what", "What it is")],
    "cause": [("cause", "cause-detail", "How it’s caused")],
    "features": [("features", "features-detail", "Clinical features")],
    "confirm": [("diagnosis", "diagnosis-detail", "Diagnosis")],
    "differentials": [("differentials", "differentials-detail", "Differentials")],
    "manage": [("management", "management-detail", "Management (UK pharmacist / IP)")],
    "refer": [("red_flags", "red-flags-detail", "Red flags & referral")],
    "pearls": [("pearls", "pearls-detail", "Prescriber pearls")],
}
SHORT = 230  # characters: longer items stay in "More detail" in auto mode


def plain(s):
    return re.sub(r"\*+|\[([^\]]+)\]\([^)]+\)", lambda m: m.group(1) or "", str(s))


def is_short(s):
    return len(plain(s)) <= SHORT


def lists_in(blocks):
    for b in blocks:
        if isinstance(b, dict) and "list" in b and "callout" not in b:
            yield b["list"]
        elif isinstance(b, dict) and "ol" in b:
            yield b["ol"]


def tables_in(blocks):
    return [b["table"] for b in blocks if isinstance(b, dict) and "table" in b]


def subsections(blocks):
    """Split a section into (heading, blocks) chunks on {"h": ...}."""
    out, cur = [], ("", [])
    for b in blocks:
        if isinstance(b, dict) and "h" in b:
            if cur[1] or cur[0]:
                out.append(cur)
            cur = (b["h"], [])
        else:
            cur[1].append(b)
    if cur[1] or cur[0]:
        out.append(cur)
    return out


def urgency(text):
    t = plain(text).lower()
    if re.search(r"\b999\b|emergenc|airway|stridor|anaphyla", t):
        return "emergency"
    if re.search(r"same[- ]day|same day|admit|hospital|immediate", t):
        return "same-day"
    if re.search(r"urgent|suspected cancer|2ww|two[- ]week|same[- ]week|rheumatolog", t):
        return "urgent"
    if re.search(r"\bdo not\b|\bnever\b", t):
        return "never"
    return "routine"


RUNG_RULES = [
    ("base", r"self[- ]care|otc|general|every|lifestyle|skin care|advice"),
    ("first", r"first[- ]line|initial|mild|step 1|topical"),
    ("second", r"second[- ]line|if not|moderate|step 2|oral"),
    ("third", r"severe|extensive|third|step 3"),
    ("refer", r"specialist|refer|systemic|biolog|secondary care|isotretinoin|hospital"),
]


def rung_tone(h):
    h = plain(h).lower()
    for tone, rx in RUNG_RULES:
        if re.search(rx, h):
            return tone
    return ""


def condition_index():
    idx = {}
    for f in sorted((CONTENT / "conditions").glob("*.json")):
        if f.name.startswith("_"):
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        slug = f.stem
        for name in [d.get("title", "")] + list(d.get("aka", [])):
            n = re.sub(r"\s*\(.*?\)", "", name).lower().strip()
            if len(n) > 3:
                idx.setdefault(n, slug)
    return idx


def match_slug(name, idx, self_slug):
    n = re.sub(r"\s*\(.*?\)", "", plain(name)).lower().strip()
    if n in idx and idx[n] != self_slug:
        return idx[n]
    for k, s in idx.items():  # "Tinea corporis" → "tinea"; prefer longest key
        if s != self_slug and (n.startswith(k) or k.startswith(n)) and min(len(k), len(n)) >= 5:
            return s
    return None


def group_step(g):
    t = (g.get("title") or "").lower()
    if g.get("tone") == "danger" or "red flag" in t:
        return "refer"
    if re.search(r"\bvs\b|differential|mimic|pairing|look-alike", t):
        return "differentials"
    if re.search(r"dermoscop|histolog|grading", t):
        return "confirm"
    return "features"


def derive(d, idx=None):
    """Auto-derive the step structure from a condition's section JSON (no curation)."""
    idx = idx if idx is not None else condition_index()
    sec = d.get("sections", {})
    g = d.get("glance", {})
    out = {"_auto": True}
    icons = {"think": ("eye", "Spot it"), "engine": ("layers", "Why"), "backbone": ("pill", "Treat"), "never_miss": ("alert", "Never miss")}
    out["glance"] = {
        "chips": [x for x in [d.get("module")] if x] + list(d.get("aka", []))[:3],
        "points": [dict(icon=icons[k][0], k=icons[k][1], t=g[k], **({"tone": "danger"} if k == "never_miss" else {}))
                   for k in ("think", "engine", "backbone", "never_miss") if g.get(k)],
    }
    # recognise
    feats = sec.get("features", [])
    pts = [x for lst in lists_in(feats) for x in lst if is_short(x)][:6]
    variants = []
    for t in tables_in(feats):
        head = [str(h).lower() for h in t.get("head", [])]
        if head and re.search(r"type|pattern|subtype|variant|form|lesion", head[0]) and len(head) >= 2:
            for r in t["rows"]:
                variants.append({"name": plain(r[0]), "t": r[1] if len(r) > 1 else "",
                                 "where": r[2] if len(r) > 2 and head[2:3] and not re.search(r"photo", head[2]) else ""})
            break
    visuals = []
    for b in sec.get("cause", []) + feats:
        if isinstance(b, dict) and "figure" in b and "ai" in b["figure"]:
            visuals.append(b["figure"])
    cause_pts = [x for lst in lists_in(sec.get("cause", [])) for x in lst if is_short(x)][:6]
    cause_vis = [b["figure"] for b in sec.get("cause", []) if isinstance(b, dict) and "figure" in b and "ai" in b["figure"]]
    out["cause"] = {"points": cause_pts, "visuals": cause_vis[:2]}
    out["features"] = {"photo": d.get("card_image"), "points": pts, "visuals": [v for v in visuals if v not in cause_vis][:2],
                       "variants": {"title": "Types to recognise", "items": variants} if variants else None}
    # confirm
    cols, misc = {}, []
    for lst in lists_in(sec.get("diagnosis", [])):
        for x in lst:
            m = re.match(r"\*\*([^*:]{2,30}):?\*\*:?\s*(.*)", x)
            if m and is_short(m.group(2)):
                cols.setdefault(m.group(1).strip(" :"), []).append(m.group(2))
            elif is_short(x):
                misc.append(x)
    col_icons = {"history": "chat", "exam": "eye", "severity": "gauge", "test": "flask", "investig": "flask"}
    cl = [{"k": k[:1].upper() + k[1:], "icon": next((v for kk, v in col_icons.items() if kk in k.lower()), "check"), "points": v} for k, v in cols.items()]
    if misc:
        cl.append({"k": "Key points", "icon": "check", "points": misc})
    out["confirm"] = {"cols": cl[:4]}
    # differentials
    cards = []
    for t in tables_in(sec.get("differentials", [])):
        head = [str(h).lower() for h in t.get("head", [])]
        if len(head) == 2 or (head and re.search(r"look|differential|mimic|condition", head[0])):
            for r in t["rows"]:
                if len(r) >= 2 and r[0]:
                    c = {"name": plain(r[0]), "clue": r[1]}
                    s = match_slug(r[0], idx, d["slug"])
                    if s:
                        c["link"] = s
                    cards.append(c)
    out["differentials"] = {"cards": cards}
    # manage: sub-headed chunks that look like a ladder
    rungs = []
    for h, blocks in subsections(sec.get("management", [])):
        tone = rung_tone(h)
        if not tone:
            continue
        p = [x for lst in lists_in(blocks) for x in lst if is_short(x)] or [b for b in blocks if isinstance(b, str) and is_short(b)]
        if p:
            rungs.append({"k": plain(h), "tone": tone, "points": p[:5]})
    order = {"base": 0, "first": 1, "second": 2, "third": 3, "refer": 4}
    rungs.sort(key=lambda r: order[r["tone"]])
    out["manage"] = {"rungs": rungs if len(rungs) >= 2 else []}
    # refer + pearls
    rf = [b for b in sec.get("red_flags", []) if isinstance(b, str)]
    out["refer"] = {"items": [{"when": urgency(x), "t": x} for x in rf if is_short(x)]}
    out["pearls"] = [{"icon": "bulb", "t": x} for x in sec.get("pearls", []) if isinstance(x, str) and is_short(x)][:8]
    # quick self-check: recall questions built from the glance summary and the first red flag
    title = d.get("title", "this condition")
    qs = [("think", f"When should you think of {title}?"), ("engine", "What drives it?"),
          ("backbone", "What is the backbone of care?"), ("never_miss", "What must you never miss?")]
    out["quiz"] = [{"q": q, "a": g[k]} for k, q in qs if g.get(k)]
    if rf:
        out["quiz"].append({"q": "Name a red flag that needs escalation.", "a": rf[0]})
    # photo groups → steps
    for i, gr in enumerate(d.get("photos", [])):
        out.setdefault(group_step(gr), {}).setdefault("groups", []).append(i)
    return out


def load_overlay(slug):
    f = STEPS_DIR / f"{slug}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def steps_for(d, idx=None):
    """Curated overlay merged over the auto derivation (overlay wins per step key).
    Photo groups not placed by the overlay fall back to their auto step, so none are dropped."""
    auto = derive(d, idx)
    ov = load_overlay(d["slug"])
    if not ov:
        return auto
    out = {"_auto": False}
    for key, *_ in STEPS:
        out[key] = ov[key] if key in ov else auto.get(key)
    placed = {i for k, *_ in STEPS if isinstance(out.get(k), dict) for i in out[k].get("groups", [])}
    for i, gr in enumerate(d.get("photos", [])):
        if i not in placed:
            st = group_step(gr)
            out[st] = dict(out.get(st) or {})
            out[st]["groups"] = list(out[st].get("groups", [])) + [i]
    return out


def main(argv):
    slugs = [a for a in argv if not a.startswith("--")]
    files = [CONTENT / "conditions" / f"{s}.json" for s in slugs] if slugs else sorted(
        f for f in (CONTENT / "conditions").glob("*.json") if not f.name.startswith("_"))
    idx = condition_index()
    if "--report" in argv:
        cur = auto = 0
        for f in files:
            d = json.loads(f.read_text(encoding="utf-8")); d.setdefault("slug", f.stem)
            st = steps_for(d, idx)
            kind = "auto" if st["_auto"] else "curated"
            cur += kind == "curated"; auto += kind == "auto"
            n = {k: len((st.get(k) or {}).get("groups", [])) for k in ("features", "confirm", "differentials", "refer") if isinstance(st.get(k), dict)}
            print(f"{kind:8} {f.stem:40} groups→ {n}")
        print(f"\n{cur} curated, {auto} auto")
        return 0
    outdir = STEPS_DIR / "_auto"
    outdir.mkdir(parents=True, exist_ok=True)
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8")); d.setdefault("slug", f.stem)
        (outdir / f.name).write_text(json.dumps(derive(d, idx), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(files)} auto step drafts to {outdir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
