#!/usr/bin/env python3
"""
Derm Teach static site builder.

Reads content from ./content (categories.json, site.json, conditions/*.json,
dermnet-manifest.json) and writes plain static HTML:

  index.html                      home (browse by category)
  categories/<category-id>.html   one page per category
  conditions/<slug>.html          one page per condition
  credits.html                    image credits / attributions
  assets/js/search-index.js       client-side search data

Pure Python 3 standard library. Run:  python3 build.py
The generated HTML works straight from the file system (file://) or any static server.
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def asset_v(rel):
    """Short content hash for cache-busting CSS/JS, so phones pick up presentation fixes at once."""
    import hashlib
    try: return "?v=" + hashlib.sha1((ROOT / "assets" / rel).read_bytes()).hexdigest()[:10]
    except OSError: return ""
CONTENT = ROOT / "content"
WARNINGS = []

SECTIONS = [
    ("what", "what", "What it is"),
    ("cause", "cause", "How it’s caused"),
    ("features", "features", "Clinical features"),
    ("diagnosis", "diagnosis", "Diagnosis"),
    ("differentials", "differentials", "Differentials"),
    ("management", "management", "Management (UK pharmacist / IP)"),
    ("red_flags", "red-flags", "Red flags & referral"),
    ("pearls", "pearls", "Prescriber pearls"),
]
GLANCE = [
    ("think", "Think of it when"),
    ("engine", "What drives it"),
    ("backbone", "Backbone of care"),
    ("never_miss", "Never miss"),
]

ICONS = {
    "pill": '<rect x="3.5" y="8.5" width="17" height="7" rx="3.5" transform="rotate(-35 12 12)"/><path d="M9.6 8.6l4.8 6.8"/>',
    "capsule": '<path d="M10.5 4.5a4.2 4.2 0 0 1 6 6l-6 6a4.2 4.2 0 0 1-6-6Z"/><path d="M7.5 7.5l6 6"/><path d="M18 17.5h3M19.5 16v3"/>',
    "vessel": '<path d="M3 8c3 0 3 3 6 3s3-3 6-3 3 3 6 3"/><path d="M3 15c3 0 3 3 6 3s3-3 6-3 3 3 6 3"/><path d="M8 12.5h.01M14 13h.01"/>',
    "body": '<circle cx="12" cy="5" r="2.2"/><path d="M12 8v7M7 10.5l5-1.5 5 1.5M9.5 21l2.5-6 2.5 6"/><circle cx="12" cy="12" r="1.2"/>',
    "mole": '<path d="M3 18h18"/><path d="M8 18c0-3.5 1.6-6 4-6s4 2.5 4 6"/><path d="M10.6 14.6h.01M13 15.5h.01"/><path d="M5 9l1.5 1M19 9l-1.5 1M12 5v2"/>',
    "scalpel": '<path d="M4 20l9.5-9.5 3 3L7 23"/><path d="M13.5 10.5l5-5.5a2 2 0 0 1 2.8 2.8l-4.8 5.7"/>',
    "virus": '<circle cx="12" cy="12" r="5"/><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.9 2.9M15.5 15.5l2.9 2.9M5.6 18.4l2.9-2.9M15.5 8.5l2.9-2.9"/>',
    "leg": '<path d="M9 3v8.5c0 2-1 3.5-1 5.5 0 1.7 1 3 3 3h5.5c1 0 1.5-.8 1-1.6L15 16.5c-.6-1-1-2-1-3.2V3"/><path d="M11 13.5h.01"/>',
    "drop": '<path d="M12 3.5c3.2 4 6 7.4 6 10.5a6 6 0 0 1-12 0c0-3.1 2.8-6.5 6-10.5Z"/><path d="M12 20a6 6 0 0 0 6-6"/>',
    "hourglass": '<path d="M7 3h10M7 21h10M8 3c0 5 8 5 8 9s-8 4-8 9M16 3c0 5-8 5-8 9s8 4 8 9"/>',
    "sparkle": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8Z"/><path d="M18.5 16.5l.7 1.8 1.8.7-1.8.7-.7 1.8-.7-1.8-1.8-.7 1.8-.7Z"/>',
    "flame": '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.2 1-3.6 2.2-4.8.2 1.6 1 2.6 2 3 0-3 .3-5.6.8-8.2Z"/>',
    "follicle": '<circle cx="12" cy="12" r="8"/><path d="M12 20V9"/><path d="M9.5 10.5c.8-1 1.6-1.5 2.5-1.5s1.7.5 2.5 1.5"/><circle cx="12" cy="7" r="1.2"/>',
    "ring": '<circle cx="12" cy="12" r="7.5" stroke-dasharray="2.4 2"/><circle cx="12" cy="12" r="3.2"/>',
    "bacteria": '<rect x="5" y="8.5" width="14" height="7" rx="3.5"/><path d="M3 9l2 1.5M3 15l2-1.5M21 9l-2 1.5M21 15l-2-1.5M9 12h.01M12 12h.01M15 12h.01"/>',
    "book": '<path d="M5 4.5A1.5 1.5 0 0 1 6.5 3H19v15H6.5A1.5 1.5 0 0 0 5 19.5Z"/><path d="M5 19.5A1.5 1.5 0 0 0 6.5 21H19"/><path d="M9 7h6M9 10.5h6"/>',
    "hand": '<path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V11M11 10V4.5a1.5 1.5 0 0 1 3 0V11M14 10.5V6a1.5 1.5 0 0 1 3 0v7.5c0 4-2.7 7-6.5 7-2.6 0-4.3-1.3-5.6-3.5L3.6 13.6a1.4 1.4 0 0 1 2.3-1.6L8 14"/>',
    "nail": '<path d="M8 21V8a4 4 0 0 1 8 0v13"/><rect x="9.5" y="5" width="5" height="5.5" rx="2.2"/>',
    "blister": '<path d="M3 17h18"/><path d="M6.5 17c0-3.6 2.5-6.5 5.5-6.5s5.5 2.9 5.5 6.5"/><path d="M10 13.5c.6-.6 1.3-.9 2-.9"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.5M12 19v2.5M2.5 12H5M19 12h2.5M5.3 5.3l1.8 1.8M16.9 16.9l1.8 1.8M5.3 18.7l1.8-1.8M16.9 7.1l1.8-1.8"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.4 3.5 5.3 3.5 8.5s-1.1 6.1-3.5 8.5c-2.4-2.4-3.5-5.3-3.5-8.5s1.1-6.1 3.5-8.5Z"/>',
    "comb": '<path d="M4 9h16v3H4z"/><path d="M6 12v6M9 12v6M12 12v6M15 12v6M18 12v6"/>',
    "check": '<rect x="4" y="3.5" width="16" height="17" rx="2"/><path d="M8 12l2.5 2.5L16 9"/>',
    "baby": '<circle cx="12" cy="8.5" r="4.5"/><path d="M10.4 8.6h.01M13.6 8.6h.01M10.6 10.4c.8.6 2 .6 2.8 0"/><path d="M6 21c.6-3.6 3-5.5 6-5.5s5.4 1.9 6 5.5"/>',
}


def icon(name, cls="ico"):
    p = ICONS.get(name, ICONS["ring"])
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{p}</svg>')


def esc(s):
    return html.escape(str(s), quote=True)


def load_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"JSON error in {p}: {e}")


# ---------------------------------------------------------------- data
SITE = load_json(CONTENT / "site.json")
CATS = sorted(load_json(CONTENT / "categories.json"), key=lambda c: c.get("order", 99))
CAT_BY_ID = {c["id"]: c for c in CATS}
# Photo sets: each set = one image folder + one manifest (see content/photo-sets.json).
# Reference a photo as "A01" (core set) or "<set>:<code>", e.g. "m5w1:L01" or "m6w4:W4A-01".
PHOTO_SETS = load_json(CONTENT / "photo-sets.json")
MANIFEST = []
PHOTO_BY_CODE = {}
for ps in PHOTO_SETS:
    for m in load_json(ROOT / ps["manifest"]):
        code = Path(m["filename"]).name.split("_")[0]
        m = dict(m, _set=ps["id"], _dir=ps["dir"], _code=code, _key=f'{ps["id"]}:{code}')
        MANIFEST.append(m)
        PHOTO_BY_CODE[m["_key"]] = m
        if ps["id"] == "core":
            PHOTO_BY_CODE[code] = m

CONDS = []
for f in sorted((CONTENT / "conditions").glob("*.json")):
    if f.name.startswith("_"):
        continue  # _template.json etc.
    d = load_json(f)
    d.setdefault("slug", f.stem)
    if d["slug"] != f.stem:
        WARNINGS.append(f"{f.name}: slug '{d['slug']}' differs from file name; using file name")
        d["slug"] = f.stem
    if d.get("category") not in CAT_BY_ID:
        sys.exit(f"{f.name}: unknown category '{d.get('category')}' (see content/categories.json)")
    d.setdefault("status", "published")
    d.setdefault("order", 99)
    d.setdefault("aka", [])
    d.setdefault("sections", {})
    d.setdefault("photos", [])
    d.setdefault("references", [])
    CONDS.append(d)

CONDS.sort(key=lambda c: (CAT_BY_ID[c["category"]].get("order", 99), c["order"], c["title"]))
BY_CAT = {c["id"]: [d for d in CONDS if d["category"] == c["id"]] for c in CATS}
SLUGS = {d["slug"] for d in CONDS}


# ---------------------------------------------------------------- inline markup
def md(s, prefix):
    """Tiny inline markup: **bold**, *italic*, [text](url) and [text](condition:slug)."""
    s = esc(s)

    def link(m):
        text, url = m.group(1), html.unescape(m.group(2))
        if url.startswith("condition:"):
            slug = url.split(":", 1)[1]
            if slug not in SLUGS:
                WARNINGS.append(f"link to unknown condition '{slug}'")
            return f'<a href="{prefix}conditions/{esc(slug)}.html">{text}</a>'
        ext = url.startswith("http")
        return f'<a href="{esc(url)}"{" target=_blank rel=noopener" if ext else ""}>{text}</a>'

    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    return s


# ---------------------------------------------------------------- photos
def resolve_photo(item, prefix, ctx=""):
    """Return a dict for a DermNet code ("A01"), {"dermnet": "A01", "caption": ...} or {"ai": file, "caption": ...}."""
    if isinstance(item, str):
        item = {"dermnet": item}
    if "dermnet" in item:
        m = PHOTO_BY_CODE.get(item["dermnet"])
        if not m:
            WARNINGS.append(f"{ctx}: unknown photo code '{item['dermnet']}'")
            return None
        site = m.get("source_site") or "DermNet"
        is_dn = "dermnet" in site.lower()
        cap = m.get("dermnet_caption") or m.get("source_caption") or m.get("teaching_point", "")[:80]
        holder = m.get("copyright") or ""
        return {
            "kind": "dermnet" if is_dn else "other",
            "site": "DermNet" if is_dn else site,
            "src": f"{prefix}{m['_dir']}/{m['filename']}",
            "caption": item.get("caption") or m.get("teaching_point") or cap,
            "alt": cap,
            "credit": f"{'DermNet' if is_dn else site} — {cap}" + (f" ({holder})" if holder else ""),
            "href": m["source_page_url"],
            "w": m.get("width", 640), "h": m.get("height", 480),
        }
    if "ai" in item:
        p = ROOT / "assets/img/ai" / item["ai"]
        if not p.exists():
            WARNINGS.append(f"{ctx}: AI image not found assets/img/ai/{item['ai']}")
        return {
            "kind": "ai",
            "src": f"{prefix}assets/img/ai/{item['ai']}",
            "caption": item.get("caption", ""),
            "alt": item.get("alt") or item.get("caption", "AI teaching illustration"),
            "credit": "AI-generated teaching illustration — not a clinical photograph",
            "href": "", "w": 1280, "h": 720,
        }
    WARNINGS.append(f"{ctx}: photo item not understood: {item}")
    return None


# ---------------------------------------------------------------- UI (redesign)
from datetime import datetime  # noqa: E402

UI = {
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h10"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "moon": '<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z"/>',
    "x": '<path d="M6 6l12 12M18 6 6 18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "arrow-l": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "chev": '<path d="m9 6 6 6-6 6"/>',
    "chev-d": '<path d="m6 9 6 6 6-6"/>',
    "alert": '<path d="M12 3.5 2.5 20h19L12 3.5Z"/><path d="M12 10v4.5M12 17.5h.01"/>',
    "refer": '<circle cx="12" cy="12" r="9"/><path d="M8 12h8M13 8.5l3.5 3.5-3.5 3.5"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.9 7.5-9.5V6L12 3Z"/><path d="m9 12 2 2 4-4"/>',
    "pill": '<rect x="3" y="8.5" width="18" height="7" rx="3.5" transform="rotate(-45 12 12)"/><path d="m9.5 9.5 5 5"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5.5M12 7.5h.01"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.7.5 1.1 1.3 1.1 2.2h5c0-.9.4-1.7 1.1-2.2A6 6 0 0 0 12 3Z"/>',
    "image": '<rect x="3" y="4.5" width="18" height="15" rx="2.5"/><circle cx="9" cy="10" r="1.8"/><path d="m21 16-5-5-8.5 8.5"/>',
    "external": '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    "expand": '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "layers": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>',
    "home": '<path d="M4 11 12 4l8 7v8.5a.5.5 0 0 1-.5.5H15v-6H9v6H4.5a.5.5 0 0 1-.5-.5V11Z"/>',
    "print": '<path d="M7 9V4h10v5M7 17H5a1 1 0 0 1-1-1v-5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v5a1 1 0 0 1-1 1h-2"/><rect x="7" y="14" width="10" height="6" rx="1"/>',
}


def ui(name, cls="ui", size=None):
    s = f' width="{size}" height="{size}"' if size else ""
    return (f'<svg class="{cls}" viewBox="0 0 24 24"{s} fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{UI[name]}</svg>')


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def module_rank(d):
    """(module, week) parsed from the optional free-text module tag; used only for ordering."""
    m = re.findall(r"Module\s+(\d+)\s*·\s*Week\s+(\d+)", d.get("module") or "")
    return max(((int(a), int(b)) for a, b in m), default=(0, 0))


# ---------------------------------------------------------------- photos
def figure(ph, cls=""):
    if not ph:
        return ""
    ai = ph["kind"] == "ai"
    # no source badge over real photos: the credit line and Source link sit under each image
    badge = '<span class="badge badge-ai">AI diagram</span>' if ai else ""
    src = (f' <a class="src-link" href="{esc(ph["href"])}" target="_blank" rel="noopener">Source{ui("external", "ui ui-xs")}</a>'
           if ph["href"] else "")
    credit = f'<span class="credit">{esc(ph["credit"])}{src}</span>'
    return (
        f'<figure class="ph ph-{ph["kind"]} {cls}">'
        f'<button type="button" class="ph-btn" data-lb data-src="{esc(ph["src"])}" '
        f'data-caption="{esc(ph["caption"])}" data-credit="{esc(ph["credit"])}" data-href="{esc(ph["href"])}" '
        f'data-ai="{1 if ai else 0}" aria-label="Enlarge image: {esc(ph["alt"])}">'
        f'<img src="{esc(ph["src"])}" alt="{esc(ph["alt"])}" loading="lazy" decoding="async" width="{ph["w"]}" height="{ph["h"]}">'
        f'{badge}<span class="zoom" aria-hidden="true">{ui("expand", "ui ui-sm")}</span></button>'
        f'<figcaption><span class="tp">{md(ph["caption"], "")}</span>{credit}</figcaption></figure>'
    )


# ---------------------------------------------------------------- blocks
CALLOUT_KIND = {
    # kind: (icon, eyebrow label)
    "redflag": ("alert", "Red flag"),
    "refer": ("refer", "Refer"),
    "uk": ("shield", "UK guidance"),
    "caution": ("alert", "Caution"),
    "tip": ("pill", "Prescriber tip"),
    "note": ("info", "Note"),
}


def callout_kind(tone, title, text):
    """Presentation-only classification of a callout (no schema change): picks icon + label."""
    t = f"{title} {text}".lower()
    if tone == "danger":
        return "refer" if re.search(r"\brefer|same[- ]day|urgent|999|a&e\b", title.lower()) else "redflag"
    if re.search(r"\brefer(ral)?\b|same[- ]day|two[- ]week wait|2ww", title.lower()):
        return "refer"
    if tone == "warn":
        if re.search(r"\buk\b|bnf|nice|cks|mhra|smpc|licen[cs]|formulary|not recommended|correction|stewardship", t):
            return "uk"
        return "caution"
    if tone == "tip":
        return "tip"
    return "note"


def render_table(t, prefix):
    head = t.get("head", [])
    # columns headed "Correction", "Recommended", "UK" get a highlight (UK-guidance corrections)
    hl = {i for i, h in enumerate(head) if re.search(r"correction|recommended|\(uk\)", str(h), re.I)}
    ncol = max([len(head)] + [len(r) for r in t["rows"]])
    rows = "".join(
        "<tr>" + "".join(
            f'<td data-label="{esc(head[i]) if i < len(head) else ""}"{" class=col-uk" if i in hl else ""}>{md(cell, prefix)}</td>'
            for i, cell in enumerate(r)) + "</tr>"
        for r in t["rows"])
    cap = f'<caption>{md(t["caption"], prefix)}</caption>' if t.get("caption") else ""
    wide = " is-wide" if ncol >= 5 else ""
    return (f'<div class="table-wrap{wide}"><table class="rtable">{cap}<thead><tr>'
            + "".join(f'<th scope="col"{" class=col-uk" if i in hl else ""}>{esc(h)}</th>' for i, h in enumerate(head))
            + f"</tr></thead><tbody>{rows}</tbody></table></div>")


def render_blocks(blocks, prefix, ctx, list_cls=""):
    out = []
    loose = []  # consecutive plain strings in red_flags/pearls become one list

    def flush():
        if loose:
            out.append(f'<ul class="{list_cls}">' + "".join(f"<li>{md(x, prefix)}</li>" for x in loose) + "</ul>")
            loose.clear()

    for b in blocks:
        if isinstance(b, str):
            if list_cls:
                loose.append(b)
            else:
                out.append(f"<p>{md(b, prefix)}</p>")
            continue
        flush()
        if "h" in b:
            out.append(f'<h3>{md(b["h"], prefix)}</h3>')
        elif "list" in b and "callout" not in b:
            out.append("<ul>" + "".join(f"<li>{md(x, prefix)}</li>" for x in b["list"]) + "</ul>")
        elif "ol" in b:
            out.append('<ol class="steps">' + "".join(f"<li>{md(x, prefix)}</li>" for x in b["ol"]) + "</ol>")
        elif "table" in b:
            out.append(render_table(b["table"], prefix))
        elif "callout" in b:
            tone = b["callout"] if b["callout"] in ("info", "tip", "warn", "danger") else "info"
            kind = callout_kind(tone, b.get("title", ""), b.get("text", ""))
            ico, label = CALLOUT_KIND[kind]
            inner = ""
            if b.get("text"):
                inner += f"<p>{md(b['text'], prefix)}</p>"
            if b.get("list"):
                inner += "<ul>" + "".join(f"<li>{md(x, prefix)}</li>" for x in b["list"]) + "</ul>"
            title = f'<p class="callout-title">{md(b.get("title", ""), prefix)}</p>' if b.get("title") else ""
            out.append(f'<aside class="callout callout-{tone} co-{kind}"><span class="co-ico">{ui(ico)}</span>'
                       f'<div class="co-body"><p class="co-label">{label}</p>{title}{inner}</div></aside>')
        elif "figure" in b:
            out.append(figure(resolve_photo(b["figure"], prefix, ctx), "ph-inline"))
        elif "figures" in b:
            out.append('<div class="gallery">' + "".join(
                figure(resolve_photo(x, prefix, ctx)) for x in b["figures"]) + "</div>")
        else:
            WARNINGS.append(f"{ctx}: unknown block {list(b)[:3]}")
    flush()
    return "\n".join(out)


# ---------------------------------------------------------------- layout
def nav_drawer(prefix, active_slug=None, active_cat=None):
    parts = []
    for c in CATS:
        items = []
        for d in BY_CAT[c["id"]]:
            soon = ' <span class="pill pill-soon">soon</span>' if d["status"] != "published" else ""
            cur = ' aria-current="page"' if d["slug"] == active_slug else ""
            items.append(f'<li><a href="{prefix}conditions/{d["slug"]}.html"{cur}>{esc(d["title"])}{soon}</a></li>')
        open_ = " open" if (active_cat == c["id"]) else ""
        cur = ' aria-current="page"' if (active_cat == c["id"] and not active_slug) else ""
        parts.append(
            f'<details class="nav-cat" style="--accent:{c["accent"]}"{open_}>'
            f'<summary><span class="nav-ico">{icon(c["icon"])}</span><span class="nav-t">{esc(c["title"])}</span>'
            f'<span class="nav-count">{len(BY_CAT[c["id"]])}</span>{ui("chev", "ui nav-chev")}</summary>'
            f'<ul><li><a class="nav-all" href="{prefix}categories/{c["id"]}.html"{cur}>Category overview</a></li>'
            + "".join(items) + "</ul></details>")
    return (
        '<div class="drawer-backdrop" data-drawer-close hidden></div>'
        '<nav class="drawer" id="drawer" aria-label="Library" aria-hidden="true" inert>'
        '<div class="drawer-head"><span class="drawer-title">Library</span>'
        f'<button type="button" class="icon-btn" data-drawer-close aria-label="Close menu">{ui("x")}</button></div>'
        '<div class="drawer-scroll">'
        f'<a class="drawer-link" href="{prefix}index.html">{ui("home")}Home</a>'
        + "".join(parts) +
        f'<a class="drawer-link" href="{prefix}credits.html">{ui("image")}Image credits</a></div></nav>'
    )


def search_box(cls="search", placeholder="Search conditions, synonyms or categories…", kbd=True):
    return (
        f'<div class="{cls}" role="search">'
        f'{ui("search", "search-ico")}'
        f'<input type="search" class="search-input" placeholder="{placeholder}" '
        'aria-label="Search conditions, synonyms and categories" autocomplete="off" spellcheck="false" '
        'role="combobox" aria-expanded="false" aria-autocomplete="list">'
        + ('<kbd class="search-kbd" aria-hidden="true">/</kbd>' if kbd else "")
        + '<ul class="search-results" role="listbox" hidden></ul></div>'
    )


THEME_BOOT = ("<script>(function(){try{var t=localStorage.getItem('dt-theme');"
              "if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}catch(e){}})()</script>")


def page(title, prefix, body, *, desc="", active_slug=None, active_cat=None, body_cls=""):
    full_title = f"{title} · {SITE['title']}" if title != SITE["title"] else f"{SITE['title']} · {SITE['subtitle']}"
    year = "2026"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc or SITE['tagline'])}">
<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b1214" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">
{THEME_BOOT}
<link rel="preload" href="{prefix}assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}assets/css/style.css{asset_v("css/style.css")}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='9' fill='%230d5e63'/%3E%3Ccircle cx='16' cy='16' r='8' fill='none' stroke='%23fff' stroke-width='2.5'/%3E%3Ccircle cx='16' cy='16' r='2.5' fill='%23fff'/%3E%3C/svg%3E">
</head>
<body class="{body_cls}" data-root="{prefix}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="{prefix}index.html" aria-label="{esc(SITE['title'])} home"><span class="brand-mark" aria-hidden="true"></span><span class="brand-text"><b>{esc(SITE['title'])}</b><small>{esc(SITE['subtitle'])}</small></span></a>
    <button type="button" class="nav-btn" data-drawer-open aria-controls="drawer" aria-expanded="false">{ui("layers")}<span>Browse</span></button>
    {search_box("search search-top", "Search conditions…")}
    <div class="top-actions">
      <button type="button" class="icon-btn search-toggle" aria-label="Search" aria-expanded="false">{ui("search")}</button>
      <button type="button" class="icon-btn theme-toggle" aria-label="Toggle dark mode" title="Toggle dark mode">{ui("moon", "ui i-moon")}{ui("sun", "ui i-sun")}</button>
      <button type="button" class="icon-btn menu-btn" data-drawer-open aria-controls="drawer" aria-expanded="false" aria-label="Open library menu">{ui("menu")}</button>
    </div>
  </div>
  <div class="progress" aria-hidden="true"><span></span></div>
</header>
{nav_drawer(prefix, active_slug, active_cat)}
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="wrap footer-in">
    <div class="foot-brand"><a class="brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true"></span><span class="brand-text"><b>{esc(SITE['title'])}</b><small>{esc(SITE['subtitle'])}</small></span></a>
    <p class="foot-meta">{esc(SITE['owner'])} · {year} · UK English</p>
    <p class="foot-links"><a href="{prefix}index.html#categories">All categories</a><a href="{prefix}credits.html">Image credits</a><a href="https://bnf.nice.org.uk/" target="_blank" rel="noopener">BNF</a><a href="https://cks.nice.org.uk/" target="_blank" rel="noopener">NICE CKS</a></p></div>
    <div class="foot-notes">
    <p class="disclaimer"><strong>Personal study resource.</strong> These are {esc(SITE['owner'])}’s own learning notes. They are not a clinical guideline and are not for patient-facing use. Doses, licences and pathways change, so always check the current <a href="https://bnf.nice.org.uk/" target="_blank" rel="noopener">BNF</a>, <a href="https://cks.nice.org.uk/" target="_blank" rel="noopener">NICE CKS</a>, SmPC, MHRA alerts and your local formulary before prescribing.</p>
    <p class="disclaimer">Clinical photographs © <a href="https://dermnetnz.org/" target="_blank" rel="noopener">DermNet</a> or the named holder, reproduced for personal education under the <a href="https://dermnetnz.org/image-licence" target="_blank" rel="noopener">DermNet image licence</a> with attribution on every image. Images marked “AI diagram” are AI-generated teaching illustrations, not clinical photographs. <a href="{prefix}credits.html">Full image credits</a>.</p>
    </div>
  </div>
</footer>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer" hidden>
  <div class="lb-bar"><span class="lb-count"></span><button type="button" class="lb-close icon-btn" aria-label="Close image viewer">{ui("x")}</button></div>
  <button type="button" class="lb-prev icon-btn" aria-label="Previous image">{ui("arrow-l")}</button>
  <figure class="lb-fig"><div class="lb-stage"><img alt=""></div><figcaption><span class="lb-cap"></span><span class="lb-credit"></span></figcaption></figure>
  <button type="button" class="lb-next icon-btn" aria-label="Next image">{ui("arrow")}</button>
</div>
<script src="{prefix}assets/js/search-index.js"></script>
<script src="{prefix}assets/js/app.js{asset_v("js/app.js")}"></script>
</body>
</html>
"""


def thumb_for(d, prefix):
    item = d.get("card_image")
    if not item:
        for g in d.get("photos", []):
            if g.get("items"):
                item = g["items"][0]
                break
    if not item:
        return ('<div class="card-thumb card-thumb-empty" aria-hidden="true">'
                + icon(CAT_BY_ID[d["category"]]["icon"], "ico ico-xl") + "</div>")
    ph = resolve_photo(item, prefix, d["slug"])
    if not ph:
        return ""
    tag = '<span class="thumb-credit">AI diagram</span>' if ph["kind"] == "ai" else ""   # no source tag over photos
    return (f'<div class="card-thumb"><img src="{esc(ph["src"])}" alt="" loading="lazy" decoding="async">'
            f'{tag}</div>')


def count_photos(d):
    n = 0
    for g in d.get("photos", []):
        n += len(g.get("items", []))
    return n


def crumbs(items):
    """items: list of (label, href or None)."""
    out = []
    for i, (lbl, href) in enumerate(items):
        if i:
            out.append(ui("chev", "ui crumb-sep"))
        out.append(f'<a href="{href}">{esc(lbl)}</a>' if href else f'<span aria-current="page">{esc(lbl)}</span>')
    return f'<nav class="crumbs" aria-label="Breadcrumb">{"".join(out)}</nav>'


def first_seen():
    """Generated ledger (assets/data/first-seen.json) of when each page first appeared in a build.
    Seeded from content-file mtimes the first time; used only to order 'Recently added'."""
    p = ROOT / "assets/data/first-seen.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    seeded = p.exists()
    led = load_json(p) if seeded else {}
    now = datetime.now().strftime("%Y-%m-%dT%H:%M")
    for d in CONDS:
        if d["slug"] not in led:
            f = CONTENT / "conditions" / f"{d['slug']}.json"
            led[d["slug"]] = now if seeded else datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%dT%H:%M")
    led = {k: v for k, v in sorted(led.items()) if k in SLUGS}
    p.write_text(json.dumps(led, indent=1) + "\n", encoding="utf-8")
    return led


def cond_card(d, p, show_cat=False):
    c = CAT_BY_ID[d["category"]]
    soon = d["status"] != "published"
    never = d.get("glance", {}).get("never_miss", "")
    aka = "".join(f'<span class="chip">{esc(a)}</span>' for a in d.get("aka", [])[:3])
    n = count_photos(d)
    top = (f'<span class="card-cat" style="--accent:{c["accent"]}">{icon(c["icon"])}{esc(c.get("short") or c["title"])}</span>'
           if show_cat else (f'<span class="card-mod">{esc(d["module"])}</span>' if d.get("module") else ""))
    return (
        f'<article class="cond-card{" is-soon" if soon else ""}" id="{esc(d["slug"])}" style="--accent:{c["accent"]}">'
        f'{thumb_for(d, p)}<div class="cond-card-body">{top}'
        f'<h3><a class="stretch" href="{p}conditions/{d["slug"]}.html">{esc(d["title"])}</a>'
        + (' <span class="pill pill-soon">Coming soon</span>' if soon else "") + "</h3>"
        f'<p class="cond-sum">{md(d.get("summary", ""), p)}</p>'
        + (f'<div class="never"><p><span>Never miss</span>{md(never, p)}</p></div>' if never and not show_cat else "")
        + (f'<div class="chips">{aka}</div>' if aka and not show_cat else "")
        + f'<span class="cond-meta"><span>{ui("image", "ui ui-xs")}{plural(n, "image")}</span>'
        f'<span class="go">{"Read" if not soon else "Outline"}{ui("arrow", "ui ui-xs")}</span></span>'
        "</div></article>")


# ---------------------------------------------------------------- pages
def build_home():
    p = ""
    cards = []
    for c in CATS:
        conds = BY_CAT[c["id"]]
        pub = [d for d in conds if d["status"] == "published"]
        soon = c.get("status") != "published"
        names = ", ".join(esc(d["title"]) for d in conds[:3]) + ("…" if len(conds) > 3 else "")
        meta = plural(len(pub), "page") if not soon else f"{len(conds)} topics · soon"
        cards.append(
            f'<article class="cat-card{" is-soon" if soon else ""}" style="--accent:{c["accent"]}">'
            f'<div class="cat-card-top"><span class="cat-ico">{icon(c["icon"])}</span>'
            f'<span class="count">{meta}</span></div>'
            f'<h3><a class="stretch" href="categories/{c["id"]}.html">{esc(c["title"])}</a></h3>'
            f'<p class="cat-blurb">{esc(c["blurb"])}</p>'
            f'<p class="cat-names">{names}</p>'
            f'<span class="cat-go">Explore{ui("arrow", "ui ui-xs")}</span></article>')

    led = first_seen()
    recent = sorted((d for d in CONDS if d["status"] == "published"),
                    key=lambda d: (led.get(d["slug"], ""), module_rank(d), d["title"]), reverse=True)[:6]
    recent_html = "".join(cond_card(d, p, show_cat=True) for d in recent)

    steps = "".join(f'<li><span>{i+1:02d}</span>{esc(lbl)}</li>' for i, (_, _, lbl) in enumerate(SECTIONS + [("photos", "photos", "Photos & diagrams")]))
    pearls = "".join(f"<li>{md(x, p)}</li>" for x in SITE.get("cross_cutting_pearls", []))
    flags = "".join(f"<li>{esc(x)}</li>" for x in SITE.get("shared_red_flags", []))
    n_pub = sum(1 for d in CONDS if d["status"] == "published")
    n_ph = len(MANIFEST)
    popular = [s for s in ("psoriasis", "eczema-dermatitis", "acne-vulgaris", "tinea", "cellulitis-erysipelas", "scabies") if s in SLUGS][:6]
    by_slug = {d["slug"]: d for d in CONDS}
    try_links = "".join(f'<a class="try" href="conditions/{s}.html">{esc(by_slug[s]["title"])}</a>' for s in popular)
    body = f"""
<section class="hero">
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="eyebrow"><span class="dot"></span>{esc(SITE['owner'])} · Teaching library</p>
      <h1>Primary-care dermatology, <span class="grad">organised for prescribers.</span></h1>
      <p class="lede">{esc(SITE['tagline'])}</p>
      {search_box("search search-hero", "Search conditions, e.g. tinea, boil…")}
      {f'<p class="tries"><span>Popular:</span>{try_links}</p>' if try_links else ''}
    </div>
    <aside class="hero-card" aria-label="Shared red flags">
      <p class="hero-card-k">{ui("alert", "ui ui-sm")}Never-miss emergencies</p>
      <ul class="flag-list compact">{flags}</ul>
      <p class="muted small">Escalate the same day, across every category.</p>
    </aside>
  </div>
  <div class="wrap"><ul class="stats">
    <li><b>{len(CATS)}</b><span>categories</span></li><li><b>{n_pub}</b><span>condition pages</span></li>
    <li><b>{n_ph}</b><span>clinical photos</span></li><li><b>UK</b><span>NICE · CKS · BNF aligned</span></li></ul></div>
</section>
<section class="wrap block" id="categories">
  <div class="block-head"><div><p class="kicker">Browse</p><h2>Categories</h2></div><p class="muted">Pick a category, then a condition.</p></div>
  <div class="cat-grid">{''.join(cards)}</div>
</section>
<section class="wrap block">
  <div class="block-head"><div><p class="kicker">{ui("clock", "ui ui-xs")}Latest</p><h2>Recently added</h2></div><p class="muted">The newest pages in the library.</p></div>
  <div class="cond-grid recent">{recent_html}</div>
</section>
<section class="wrap block two-col">
  <div class="panel">
    <p class="kicker">Structure</p>
    <h2>Every condition page reads the same way</h2>
    <ol class="flow">{steps}</ol>
    <p class="muted small">Desktop: use the sticky contents on the right. Phone: swipe the section chips under the top bar, and tap a heading to collapse it.</p>
  </div>
  <div class="panel">
    <p class="kicker">{ui("bulb", "ui ui-xs")}Prescriber pearls</p>
    <h2>Cross-cutting principles</h2>
    <ul class="pearl-list">{pearls}</ul>
  </div>
</section>
"""
    (ROOT / "index.html").write_text(page(SITE["title"], p, body, body_cls="home"), encoding="utf-8")


def build_category(c):
    p = "../"
    conds = BY_CAT[c["id"]]
    cards = [cond_card(d, p) for d in conds]
    n_img = sum(count_photos(d) for d in conds)
    soon_note = ""
    if c.get("status") != "published":
        soon_note = ('<aside class="callout callout-info co-note"><span class="co-ico">' + ui("info") + '</span><div class="co-body">'
                     '<p class="co-label">Note</p><p class="callout-title">Ready for content</p>'
                     '<p>Each topic below already has its own page, with section anchors (<code>#what</code>, <code>#cause</code> … <code>#pearls</code>). '
                     'To publish one, fill in its JSON file in <code>content/conditions/</code>, set <code>"status": "published"</code>, and run <code>python3 build.py</code>. '
                     'See <code>ADD_CONDITION.md</code>.</p></div></aside>')
    i = next(k for k, x in enumerate(CATS) if x["id"] == c["id"])
    prv, nxt = (CATS[i - 1] if i else None), (CATS[i + 1] if i + 1 < len(CATS) else None)
    pn = '<nav class="prevnext" aria-label="More categories">'
    pn += (f'<a class="pn pn-prev" href="{prv["id"]}.html"><small>{ui("arrow-l", "ui ui-xs")}Previous category</small><b>{esc(prv["title"])}</b></a>' if prv else "<span></span>")
    pn += (f'<a class="pn pn-next" href="{nxt["id"]}.html"><small>Next category{ui("arrow", "ui ui-xs")}</small><b>{esc(nxt["title"])}</b></a>' if nxt else "<span></span>")
    pn += "</nav>"
    body = f"""
<section class="page-head" style="--accent:{c['accent']}">
  <div class="wrap">
    {crumbs([("Home", f"{p}index.html"), (c['title'], None)])}
    <div class="cat-hero-row"><span class="cat-ico cat-ico-lg">{icon(c['icon'])}</span>
    <div><h1>{esc(c['title'])}</h1><p class="lede">{esc(c['blurb'])}</p>
    <p class="head-meta">{plural(len(conds), "page")} · {plural(n_img, "image")}</p></div></div>
  </div>
</section>
<section class="wrap block">
  {soon_note}
  <div class="cond-grid">{''.join(cards)}</div>
  {pn}
</section>
"""
    out = ROOT / "categories" / f"{c['id']}.html"
    out.write_text(page(c["title"], p, body, desc=c["blurb"], active_cat=c["id"], body_cls="category"), encoding="utf-8")


def sec_html(anchor, num, label, inner, tone="", extra=""):
    return (f'<section class="sec{tone}" id="{esc(anchor)}" aria-labelledby="h-{esc(anchor)}"><details open>'
            f'<summary><span class="sec-num">{num:02d}</span><h2 id="h-{esc(anchor)}">{label}</h2>{extra}'
            f'{ui("chev-d", "ui chev")}</summary>'
            f'<div class="sec-body">{inner}</div></details></section>')


def build_condition(d, idx, seq):
    p = "../"
    c = CAT_BY_ID[d["category"]]
    soon = d["status"] != "published"
    ctx = d["slug"]

    # header
    aka = "".join(f'<span class="chip">{esc(a)}</span>' for a in d.get("aka", []))
    glance = d.get("glance", {})
    glance_html = ""
    if any(glance.get(k) for k, _ in GLANCE):
        glance_html = '<div class="glance">' + "".join(
            f'<div class="glance-item glance-{k}"><span class="glance-k">{lbl}</span><p>{md(glance.get(k, ""), p)}</p></div>'
            for k, lbl in GLANCE if glance.get(k)) + "</div>"
    hero = ""
    if d.get("hero"):
        ph = resolve_photo(d["hero"], p, ctx)
        if ph:
            hero = f'<div class="cond-hero-img">{figure(ph, "ph-hero")}</div>'

    # sections
    toc = []
    secs = []
    num = 0
    article = d.get("layout") == "article"
    for key, anchor, label in ([] if article else SECTIONS):
        blocks = d["sections"].get(key, [])
        num += 1
        toc.append(f'<li><a href="#{anchor}" data-toc="{anchor}"><span>{num:02d}</span>{label}</a></li>')
        if blocks:
            lc = {"red_flags": "flag-list", "pearls": "pearl-list"}.get(key, "")
            inner = render_blocks(blocks, p, f"{ctx}/{key}", lc)
        else:
            inner = ('<div class="placeholder"><p><b>Content coming soon.</b> This section is wired up and ready. '
                     f'Add blocks to <code>sections.{key}</code> in <code>content/conditions/{esc(d["slug"])}.json</code>.</p></div>')
        tone = {"red_flags": " sec-danger", "pearls": " sec-tip", "management": " sec-rx"}.get(key, "")
        extra = {"management": '<span class="sec-tag">Pharmacist / IP</span>',
                 "red_flags": f'<span class="sec-tag sec-tag-danger">{ui("alert", "ui ui-xs")}Escalate</span>'}.get(key, "")
        secs.append(sec_html(anchor, num, label, inner, tone, extra))

    for a in (d.get("article", []) if article else []):
        num += 1
        anchor = a["id"]
        toc.append(f'<li><a href="#{esc(anchor)}" data-toc="{esc(anchor)}"><span>{num:02d}</span>{esc(a.get("short", a["title"]))}</a></li>')
        tone = {"danger": " sec-danger", "tip": " sec-tip", "rx": " sec-rx"}.get(a.get("tone", ""), "")
        secs.append(sec_html(anchor, num, esc(a["title"]), render_blocks(a.get("blocks", []), p, f"{ctx}/{anchor}"), tone))

    # photos
    n_img = count_photos(d)
    if not article:
        num += 1
        toc.append(f'<li><a href="#photos" data-toc="photos"><span>{num:02d}</span>Photos</a></li>')
        groups = []
        for g in d.get("photos", []):
            items = g.get("items", [])
            figs = "".join(figure(resolve_photo(x, p, ctx)) for x in items)
            tone = " gal-danger" if g.get("tone") == "danger" else ""
            groups.append(f'<div class="gal-group{tone}"><h3>{md(g.get("title", ""), p)}<span class="gal-n">{len(items)}</span></h3>'
                          f'<div class="gallery">{figs}</div></div>')
        if not groups:
            groups.append('<div class="placeholder"><p><b>Photos coming soon.</b> Add DermNet codes or AI images to <code>photos</code>.</p></div>')
        intro = ('<p class="gal-note">' + ui("image", "ui ui-sm") + '<span>Select any image to enlarge. Photographs are © DermNet or the named holder, '
                 'with the source linked under each image. Images marked <span class="badge badge-ai badge-inline">AI diagram</span> are AI-generated teaching illustrations.</span></p>')
        secs.append(sec_html("photos", num, "Photos &amp; diagrams", intro + "".join(groups),
                             extra=f'<span class="sec-tag">{plural(n_img, "image")}</span>' if n_img else ""))

    # references
    if d.get("references"):
        num += 1
        toc.append(f'<li><a href="#references" data-toc="references"><span>{num:02d}</span>References</a></li>')

        def ref_li(r):
            u = r["url"]
            if u.startswith("condition:"):
                slug = u.split(":", 1)[1]
                if slug not in SLUGS:
                    WARNINGS.append(f"{ctx}: reference to unknown condition '{slug}'")
                return f'<li><a href="{p}conditions/{esc(slug)}.html">{esc(r["label"])}</a></li>'
            host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
            return (f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(r["label"])}</a>'
                    f'<span class="ref-host">{esc(host)}</span></li>')
        refs = "".join(ref_li(r) for r in d["references"])
        secs.append(sec_html("references", num, "References &amp; further reading", f'<ol class="ref-list">{refs}</ol>'))

    soon_banner = ""
    if soon:
        planned = "".join(f"<li>{md(x, p)}</li>" for x in d.get("planned", []))
        mod = d.get("module", "a future module")
        soon_banner = (f'<aside class="callout callout-info co-note soon-banner"><span class="co-ico">{ui("clock")}</span><div class="co-body">'
                       f'<p class="co-label">Coming soon</p><p class="callout-title">{esc(mod)}</p>'
                       '<p>This page is a stub waiting for its research pack. Every section below has its anchor in place, '
                       'and the clinical photos (with attribution) are already filed in the Photos section.</p>'
                       + (f"<p><b>Planned coverage:</b></p><ul>{planned}</ul>" if planned else "") + "</div></aside>")

    # prev / next (within whole library)
    prev_d = seq[idx - 1] if idx > 0 else None
    next_d = seq[idx + 1] if idx + 1 < len(seq) else None

    def pn_link(x, cls, lbl):
        cx = CAT_BY_ID[x["category"]]
        return (f'<a class="pn {cls}" href="{p}conditions/{x["slug"]}.html" style="--accent:{cx["accent"]}">'
                f'<small>{lbl}</small><b>{esc(x["title"])}</b><span class="pn-cat">{esc(cx["title"])}</span></a>')
    pn = '<nav class="prevnext" aria-label="More conditions">'
    pn += pn_link(prev_d, "pn-prev", f'{ui("arrow-l", "ui ui-xs")}Previous') if prev_d else "<span></span>"
    pn += pn_link(next_d, "pn-next", f'Next{ui("arrow", "ui ui-xs")}') if next_d else "<span></span>"
    pn += "</nav>"

    meta = []
    if d.get("module"):
        meta.append(f'<span>{esc(d["module"])}</span>')
    if not article and n_img:
        meta.append(f'<span>{plural(n_img, "image")}</span>')
    meta = " · ".join(meta)
    body = f"""
<section class="page-head cond-head" style="--accent:{c['accent']}">
  <div class="wrap">
    {crumbs([("Home", f"{p}index.html"), (c['title'], f"{p}categories/{c['id']}.html"), (d['title'], None)])}
    <div class="cond-head-grid{' has-hero' if hero else ''}">
      <div class="cond-head-copy">
        <a class="cat-pill" href="{p}categories/{c['id']}.html">{icon(c['icon'])}{esc(c['title'])}</a>
        <h1>{esc(d['title'])}{' <span class="pill pill-soon">Coming soon</span>' if soon else ''}</h1>
        <p class="lede">{md(d.get('summary', ''), p)}</p>
        {f'<p class="head-meta">{meta}</p>' if meta else ''}
        {f'<div class="chips chips-aka"><span class="chips-label">Also covers</span>{aka}</div>' if aka else ''}
      </div>
      {hero}
    </div>
    {glance_html}
  </div>
</section>
<div class="wrap cond-layout" style="--accent:{c['accent']}">
  <aside class="toc" aria-label="On this page">
    <div class="toc-in">
      <p class="toc-title">On this page</p>
      <ol class="toc-list">{''.join(toc)}</ol>
      <div class="toc-tools"><button type="button" class="btn-sm" data-expand>Expand all</button><button type="button" class="btn-sm" data-collapse>Collapse all</button><button type="button" class="btn-sm" data-print>{ui("print", "ui ui-xs")}Print</button></div>
    </div>
  </aside>
  <article class="cond-body">
    {soon_banner}
    {''.join(secs)}
    {pn}
  </article>
</div>
"""
    out = ROOT / "conditions" / f"{d['slug']}.html"
    out.write_text(page(d["title"], p, body, desc=d.get("summary", ""), active_slug=d["slug"], active_cat=c["id"],
                        body_cls="condition" + (" layout-article" if article else "")), encoding="utf-8")


def build_credits():
    p = ""
    used = {}
    for d in CONDS:
        for g in d.get("photos", []):
            for it in g.get("items", []):
                code = it if isinstance(it, str) else it.get("dermnet")
                if code:
                    used.setdefault(code, set()).add(d["title"])

    def norm_code(c):
        return c if ":" in c else f"core:{c}"
    used = {norm_code(k): v for k, v in used.items()}
    tables = []
    jump = []
    for ps in PHOTO_SETS:
        rows = []
        for m in [x for x in MANIFEST if x["_set"] == ps["id"]]:
            pages = ", ".join(sorted(used.get(m["_key"], []))) or "—"
            ref = m["_code"] if ps["id"] == "core" else m["_key"]
            cap = m.get("dermnet_caption") or m.get("source_caption") or ""
            rows.append(
                f'<tr><td data-label="Image"><img class="credit-thumb" src="{esc(m["_dir"])}/{esc(m["filename"])}" alt="" loading="lazy" decoding="async"></td>'
                f'<td data-label="Code"><code>{esc(ref)}</code></td>'
                f'<td data-label="Caption">{esc(cap)}</td>'
                f'<td data-label="©">{esc(m.get("copyright") or "")}</td>'
                f'<td data-label="Source"><a href="{esc(m["source_page_url"])}" target="_blank" rel="noopener">{esc(m["source_page_url"].replace("https://", ""))}</a></td>'
                f'<td data-label="Used on">{esc(pages)}</td></tr>')
        jump.append(f'<a class="chip" href="#set-{ps["id"]}">{esc(ps["label"].split(" — ")[0])}</a>')
        tables.append(f'<h2 class="credits-h" id="set-{ps["id"]}">{esc(ps["label"])} <small>{len(rows)} images · <code>{esc(ps["dir"])}</code></small></h2>'
                      '<div class="table-wrap is-wide"><table class="rtable credits"><thead><tr><th>Image</th><th>Code</th><th>Caption</th><th>©</th><th>Source page</th><th>Used on</th></tr></thead>'
                      f'<tbody>{"".join(rows)}</tbody></table></div>')
    ai = sorted(x.name for x in (ROOT / "assets/img/ai").glob("*.jpg"))
    ai_li = "".join(f"<li><code>{esc(x)}</code></li>" for x in ai)
    body = f"""
<section class="page-head"><div class="wrap">
{crumbs([("Home", "index.html"), ("Image credits", None)])}
<h1>Image credits &amp; attribution</h1>
<p class="lede">Clinical photographs are from <a href="https://dermnetnz.org/" target="_blank" rel="noopener">DermNet</a>, plus a few Wikimedia Commons and open-access images, each credited to its holder. DermNet images are reproduced for personal, non-commercial study under the <a href="https://dermnetnz.org/image-licence" target="_blank" rel="noopener">DermNet image licence</a>, as watermarked low-resolution web versions. Copyright remains with DermNet or the named holder.</p>
<div class="chips jump">{''.join(jump)}</div>
</div></section>
<section class="wrap block credits-page">
{''.join(tables)}
<div class="panel" style="margin-top:2rem"><h2>AI teaching illustrations</h2>
<p class="muted">These were generated for this library as conceptual diagrams. They are not clinical photographs and must not be used for diagnosis.</p><ul class="ai-files">{ai_li}</ul></div>
</section>"""
    (ROOT / "credits.html").write_text(page("Image credits", p, body, body_cls="credits"), encoding="utf-8")


def build_search_index():
    idx = []
    for d in CONDS:
        c = CAT_BY_ID[d["category"]]
        idx.append({
            "t": d["title"], "a": d.get("aka", []), "c": c["title"], "cid": c["id"],
            "s": re.sub(r"\*+", "", d.get("summary", ""))[:180],
            "u": f"conditions/{d['slug']}.html", "soon": d["status"] != "published",
            "col": c["accent"], "m": d.get("module", ""),
        })
    for c in CATS:
        idx.append({"t": c["title"], "a": [c.get("short", "")], "c": "Category", "cid": c["id"],
                    "s": c["blurb"][:180], "u": f"categories/{c['id']}.html", "soon": False,
                    "col": c["accent"], "cat": True, "n": len(BY_CAT[c["id"]])})
    data = json.dumps(idx, ensure_ascii=False)
    (ROOT / "assets/data").mkdir(parents=True, exist_ok=True)
    (ROOT / "assets/data/search-index.json").write_text(data + "\n", encoding="utf-8")
    # The same index as a script, so search also works when opened from file:// (no fetch needed).
    js = "/* generated by build.py from the same data as assets/data/search-index.json — do not edit */\nwindow.DERM_SEARCH = " + data + ";\n"
    (ROOT / "assets/js/search-index.js").write_text(js, encoding="utf-8")


LINK_RE = re.compile(r'(?:href|src)="([^"]*)"')
ID_RE = re.compile(r'\sid="([^"]+)"')


def check_links():
    """Verify every relative href/src in the generated HTML points at a real file (and #anchor, if given)."""
    pages = [ROOT / "index.html", ROOT / "credits.html"] + sorted((ROOT / "categories").glob("*.html")) + sorted((ROOT / "conditions").glob("*.html"))
    text = {f.resolve(): f.read_text(encoding="utf-8") for f in pages}
    ids = {}
    bad = set()
    for f in pages:
        for raw in LINK_RE.findall(text[f.resolve()]):
            u = html.unescape(raw)
            if not u or re.match(r"^(https?:|mailto:|data:|tel:|javascript:)", u):
                continue
            path, _, frag = u.partition("#")
            path = path.split("?")[0]
            t = (f.parent / path).resolve() if path else f.resolve()
            if not t.exists():
                bad.add(f"{f.relative_to(ROOT)} → {u}")
            elif frag and t in text:
                if t not in ids:
                    ids[t] = set(ID_RE.findall(text[t]))
                if frag not in ids[t]:
                    bad.add(f"{f.relative_to(ROOT)} → {u} (missing #{frag})")
    for b in sorted(bad):
        WARNINGS.append(f"broken link: {b}")


def main():
    (ROOT / "categories").mkdir(exist_ok=True)
    (ROOT / "conditions").mkdir(exist_ok=True)
    # remove stale generated pages (e.g. after renaming a condition)
    for folder, keep in (("conditions", {d["slug"] for d in CONDS}), ("categories", {c["id"] for c in CATS})):
        for f in (ROOT / folder).glob("*.html"):
            if f.stem not in keep:
                f.unlink()
    build_home()
    for c in CATS:
        build_category(c)
    for i, d in enumerate(CONDS):
        build_condition(d, i, CONDS)
    build_credits()
    build_search_index()
    check_links()
    pub = sum(1 for d in CONDS if d["status"] == "published")
    print(f"Built: index.html, credits.html, {len(CATS)} category pages, {len(CONDS)} condition pages "
          f"({pub} published, {len(CONDS) - pub} coming soon).")
    for w in WARNINGS:
        print("  WARNING:", w)
    return 1 if WARNINGS and "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
