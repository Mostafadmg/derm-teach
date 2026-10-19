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


def figure(ph, cls=""):
    if not ph:
        return ""
    badge = ('<span class="badge badge-ai">AI diagram</span>' if ph["kind"] == "ai"
             else f'<span class="badge badge-dn">{esc(ph.get("site", "DermNet"))}</span>')
    credit = esc(ph["credit"])
    if ph["href"]:
        credit += f' — <a href="{esc(ph["href"])}" target="_blank" rel="noopener">source</a>'
    return (
        f'<figure class="ph ph-{ph["kind"]} {cls}">'
        f'<button type="button" class="ph-btn" data-lb data-src="{esc(ph["src"])}" '
        f'data-caption="{esc(ph["caption"])}" data-credit="{esc(ph["credit"])}" data-href="{esc(ph["href"])}" '
        f'aria-label="Enlarge: {esc(ph["alt"])}">'
        f'<img src="{esc(ph["src"])}" alt="{esc(ph["alt"])}" loading="lazy" width="{ph["w"]}" height="{ph["h"]}">'
        f'{badge}<span class="zoom" aria-hidden="true">⤢</span></button>'
        f'<figcaption><span class="tp">{md(ph["caption"], "")}</span>'
        f'<span class="credit">{credit}</span></figcaption></figure>'
    )


# ---------------------------------------------------------------- blocks
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
            t = b["table"]
            head = t.get("head", [])
            rows = "".join(
                "<tr>" + "".join(
                    f'<td data-label="{esc(head[i]) if i < len(head) else ""}">{md(cell, prefix)}</td>'
                    for i, cell in enumerate(r)) + "</tr>"
                for r in t["rows"])
            cap = f'<caption>{md(t["caption"], prefix)}</caption>' if t.get("caption") else ""
            out.append(f'<div class="table-wrap"><table class="rtable">{cap}<thead><tr>'
                       + "".join(f"<th>{esc(h)}</th>" for h in head)
                       + f"</tr></thead><tbody>{rows}</tbody></table></div>")
        elif "callout" in b:
            tone = b["callout"] if b["callout"] in ("info", "tip", "warn", "danger") else "info"
            inner = ""
            if b.get("text"):
                inner += f"<p>{md(b['text'], prefix)}</p>"
            if b.get("list"):
                inner += "<ul>" + "".join(f"<li>{md(x, prefix)}</li>" for x in b["list"]) + "</ul>"
            title = f'<p class="callout-title">{md(b.get("title", ""), prefix)}</p>' if b.get("title") else ""
            out.append(f'<aside class="callout callout-{tone}">{title}{inner}</aside>')
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
            f'<summary><span class="nav-ico">{icon(c["icon"])}</span><span>{esc(c["title"])}</span>'
            f'<span class="nav-count">{len(BY_CAT[c["id"]])}</span></summary>'
            f'<ul><li><a class="nav-all" href="{prefix}categories/{c["id"]}.html"{cur}>Category overview →</a></li>'
            + "".join(items) + "</ul></details>")
    return (
        '<div class="drawer-backdrop" data-drawer-close hidden></div>'
        '<nav class="drawer" id="drawer" aria-label="Library" aria-hidden="true">'
        '<div class="drawer-head"><span>Browse library</span>'
        '<button type="button" class="icon-btn" data-drawer-close aria-label="Close menu">✕</button></div>'
        f'<a class="drawer-home" href="{prefix}index.html">⌂ Home</a>'
        + "".join(parts) +
        f'<a class="drawer-home" href="{prefix}credits.html">Image credits</a></nav>'
    )


def search_box(cls="search", placeholder="Search conditions… e.g. tinea, boil, guttate"):
    return (
        f'<div class="{cls}" role="search">'
        '<svg class="search-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'
        f'<input type="search" class="search-input" placeholder="{placeholder}" '
        'aria-label="Search conditions" autocomplete="off" spellcheck="false">'
        '<ul class="search-results" role="listbox" hidden></ul></div>'
    )


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
<meta name="theme-color" content="#0f4c5c">
<link rel="stylesheet" href="{prefix}assets/css/style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230f4c5c'/%3E%3Ccircle cx='16' cy='16' r='8' fill='none' stroke='%23fff' stroke-width='2.5'/%3E%3Ccircle cx='16' cy='16' r='2.5' fill='%23fff'/%3E%3C/svg%3E">
</head>
<body class="{body_cls}" data-root="{prefix}">
<a class="skip" href="#main">Skip to content</a>
<header class="topbar">
  <div class="topbar-in">
    <button type="button" class="icon-btn menu-btn" data-drawer-open aria-controls="drawer" aria-expanded="false" aria-label="Open library menu">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      <span class="menu-label">Browse</span>
    </button>
    <a class="brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true"></span><span class="brand-text"><b>{esc(SITE['title'])}</b><small>{esc(SITE['subtitle'])}</small></span></a>
    {search_box("search search-top", "Search conditions…")}
  </div>
</header>
{nav_drawer(prefix, active_slug, active_cat)}
<main id="main">
{body}
</main>
<footer class="footer">
  <div class="wrap footer-in">
    <p class="disclaimer"><strong>Personal study resource.</strong> These are {esc(SITE['owner'])}’s own learning notes. They are not a clinical guideline and are not for patient-facing use. Doses, licences and pathways change, so always check the current <a href="https://bnf.nice.org.uk/" target="_blank" rel="noopener">BNF</a>, <a href="https://cks.nice.org.uk/" target="_blank" rel="noopener">NICE CKS</a>, SmPC, MHRA alerts and your local formulary before prescribing.</p>
    <p class="disclaimer">Clinical photographs © <a href="https://dermnetnz.org/" target="_blank" rel="noopener">DermNet</a> or the named holder, reproduced for personal education under the <a href="https://dermnetnz.org/image-licence" target="_blank" rel="noopener">DermNet image licence</a> with attribution on every image. Images marked “AI diagram” are AI-generated teaching illustrations, not clinical photographs. <a href="{prefix}credits.html">Full image credits</a>.</p>
    <p class="foot-meta">{esc(SITE['title'])} · {year} · UK English · Built from <code>content/*.json</code></p>
  </div>
</footer>
<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Image viewer" hidden>
  <button type="button" class="lb-close icon-btn" aria-label="Close">✕</button>
  <button type="button" class="lb-prev icon-btn" aria-label="Previous image">‹</button>
  <figure class="lb-fig"><img alt=""><figcaption><span class="lb-cap"></span><span class="lb-credit"></span><span class="lb-count"></span></figcaption></figure>
  <button type="button" class="lb-next icon-btn" aria-label="Next image">›</button>
</div>
<script src="{prefix}assets/js/search-index.js"></script>
<script src="{prefix}assets/js/app.js"></script>
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
        return '<div class="card-thumb card-thumb-empty" aria-hidden="true">' + icon(CAT_BY_ID[d["category"]]["icon"], "ico ico-xl") + "</div>"
    ph = resolve_photo(item, prefix, d["slug"])
    if not ph:
        return ""
    return f'<div class="card-thumb"><img src="{esc(ph["src"])}" alt="" loading="lazy"></div>'


def count_photos(d):
    n = 0
    for g in d.get("photos", []):
        n += len(g.get("items", []))
    return n


# ---------------------------------------------------------------- pages
def build_home():
    p = ""
    cards = []
    for c in CATS:
        conds = BY_CAT[c["id"]]
        pub = [d for d in conds if d["status"] == "published"]
        soon = c.get("status") != "published"
        lis = "".join(
            f'<li><a href="conditions/{d["slug"]}.html">{esc(d["title"])}</a>'
            + ("" if d["status"] == "published" else ' <span class="pill pill-soon">soon</span>') + "</li>"
            for d in conds)
        meta = (f'{len(pub)} condition{"s" if len(pub) != 1 else ""}' if not soon
                else f'{len(conds)} topics · coming soon')
        cards.append(
            f'<article class="cat-card{" is-soon" if soon else ""}" style="--accent:{c["accent"]}">'
            f'<a class="cat-card-link" href="categories/{c["id"]}.html" aria-label="{esc(c["title"])}"></a>'
            f'<div class="cat-card-top"><span class="cat-ico">{icon(c["icon"])}</span>'
            f'<span class="cat-meta">{meta}</span></div>'
            f'<h3>{esc(c["title"])}</h3><p>{esc(c["blurb"])}</p>'
            f'<ul class="cat-list">{lis}</ul>'
            f'<span class="cat-go">Open category →</span></article>')

    steps = "".join(f'<li><span>{i+1}</span>{esc(lbl)}</li>' for i, (_, _, lbl) in enumerate(SECTIONS + [("photos", "photos", "Photos & diagrams")]))
    pearls = "".join(f"<li>{md(x, p)}</li>" for x in SITE.get("cross_cutting_pearls", []))
    flags = "".join(f"<li>{esc(x)}</li>" for x in SITE.get("shared_red_flags", []))
    n_pub = sum(1 for d in CONDS if d["status"] == "published")
    n_ph = len(MANIFEST)
    n_soon = sum(1 for d in CONDS if d["status"] != "published")
    body = f"""
<section class="hero">
  <div class="wrap hero-in">
    <p class="eyebrow">{esc(SITE['owner'])} · Teaching library</p>
    <h1>Primary-care dermatology,<br>organised for prescribers.</h1>
    <p class="lede">{esc(SITE['tagline'])}</p>
    {search_box("search search-hero")}
    <ul class="stats"><li><b>{len(CATS)}</b> categories</li><li><b>{n_pub}</b> condition pages</li><li><b>{n_soon}</b> pages coming soon</li><li><b>{n_ph}</b> clinical photos</li></ul>
  </div>
</section>
<section class="wrap block">
  <div class="block-head"><h2>Browse by category</h2><p>Pick a category, then a condition.</p></div>
  <div class="cat-grid">{''.join(cards)}</div>
</section>
<section class="wrap block two-col">
  <div class="panel">
    <h2>How every condition page is laid out</h2>
    <ol class="flow">{steps}</ol>
    <p class="muted">Desktop: use the sticky contents bar on the right. Phone: swipe the section chips and tap a heading to collapse it.</p>
  </div>
  <div class="panel panel-danger">
    <h2>Shared red flags</h2>
    <p class="muted">Emergencies that cut across every category, so escalate the same day:</p>
    <ul class="flag-list">{flags}</ul>
  </div>
</section>
<section class="wrap block">
  <div class="panel">
    <h2>Cross-cutting prescriber pearls</h2>
    <ul class="pearl-list cols">{pearls}</ul>
  </div>
</section>
"""
    (ROOT / "index.html").write_text(page(SITE["title"], p, body, body_cls="home"), encoding="utf-8")


def build_category(c):
    p = "../"
    conds = BY_CAT[c["id"]]
    cards = []
    for d in conds:
        soon = d["status"] != "published"
        never = d.get("glance", {}).get("never_miss", "")
        aka = "".join(f'<span class="chip">{esc(a)}</span>' for a in d.get("aka", [])[:4])
        cards.append(
            f'<article class="cond-card{" is-soon" if soon else ""}" id="{esc(d["slug"])}">'
            f'<a class="cond-card-link" href="{p}conditions/{d["slug"]}.html" aria-label="{esc(d["title"])}"></a>'
            f'{thumb_for(d, p)}<div class="cond-card-body">'
            f'<h3>{esc(d["title"])}' + (' <span class="pill pill-soon">Coming soon</span>' if soon else "") + "</h3>"
            f'<p>{md(d.get("summary", ""), p)}</p>'
            + (f'<p class="never"><b>Never miss:</b> {md(never, p)}</p>' if never else "")
            + f'<div class="chips">{aka}</div>'
            f'<span class="cond-meta">{count_photos(d)} images · {"Read page →" if not soon else "View outline →"}</span>'
            "</div></article>")
    soon_note = ""
    if c.get("status") != "published":
        soon_note = ('<aside class="callout callout-info"><p class="callout-title">Ready for content</p>'
                     '<p>Each topic below already has its own page, with section anchors (<code>#what</code>, <code>#cause</code> … <code>#pearls</code>). '
                     'To publish one, fill in its JSON file in <code>content/conditions/</code>, set <code>"status": "published"</code>, and run <code>python3 build.py</code>. '
                     'See <code>ADD_CONDITION.md</code>.</p></aside>')
    body = f"""
<section class="cat-hero" style="--accent:{c['accent']}">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p}index.html">Home</a><span>›</span><span aria-current="page">{esc(c['title'])}</span></nav>
    <div class="cat-hero-row"><span class="cat-ico cat-ico-lg">{icon(c['icon'])}</span>
    <div><h1>{esc(c['title'])}</h1><p class="lede">{esc(c['blurb'])}</p></div></div>
  </div>
</section>
<section class="wrap block">
  {soon_note}
  <div class="cond-grid">{''.join(cards)}</div>
</section>
"""
    out = ROOT / "categories" / f"{c['id']}.html"
    out.write_text(page(c["title"], p, body, desc=c["blurb"], active_cat=c["id"]), encoding="utf-8")


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
        toc.append(f'<li><a href="#{anchor}" data-toc="{anchor}"><span>{num}</span>{label}</a></li>')
        if blocks:
            lc = {"red_flags": "flag-list", "pearls": "pearl-list"}.get(key, "")
            inner = render_blocks(blocks, p, f"{ctx}/{key}", lc)
        else:
            inner = ('<div class="placeholder"><p><b>Content coming soon.</b> This section is wired up and ready. '
                     f'Add blocks to <code>sections.{key}</code> in <code>content/conditions/{esc(d["slug"])}.json</code>.</p></div>')
        tone = {"red_flags": " sec-danger", "pearls": " sec-tip", "management": " sec-rx"}.get(key, "")
        secs.append(
            f'<section class="sec{tone}" id="{anchor}" aria-labelledby="h-{anchor}"><details open>'
            f'<summary><span class="sec-num">{num}</span><h2 id="h-{anchor}">{label}</h2><span class="chev" aria-hidden="true"></span></summary>'
            f'<div class="sec-body">{inner}</div></details></section>')

    for a in (d.get("article", []) if article else []):
        num += 1
        anchor = a["id"]
        toc.append(f'<li><a href="#{esc(anchor)}" data-toc="{esc(anchor)}"><span>{num}</span>{esc(a.get("short", a["title"]))}</a></li>')
        tone = {"danger": " sec-danger", "tip": " sec-tip", "rx": " sec-rx"}.get(a.get("tone", ""), "")
        secs.append(
            f'<section class="sec{tone}" id="{esc(anchor)}" aria-labelledby="h-{esc(anchor)}"><details open>'
            f'<summary><span class="sec-num">{num}</span><h2 id="h-{esc(anchor)}">{esc(a["title"])}</h2><span class="chev" aria-hidden="true"></span></summary>'
            f'<div class="sec-body">{render_blocks(a.get("blocks", []), p, f"{ctx}/{anchor}")}</div></details></section>')

    # photos
    num += 1
    if article:
        num -= 1
    else:
        toc.append(f'<li><a href="#photos" data-toc="photos"><span>{num}</span>Photos</a></li>')
    groups = []
    for g in d.get("photos", []):
        figs = "".join(figure(resolve_photo(x, p, ctx)) for x in g.get("items", []))
        tone = " gal-danger" if g.get("tone") == "danger" else ""
        groups.append(f'<div class="gal-group{tone}"><h3>{md(g.get("title", ""), p)}</h3><div class="gallery">{figs}</div></div>')
    if not groups:
        groups.append('<div class="placeholder"><p><b>Photos coming soon.</b> Add DermNet codes or AI images to <code>photos</code>.</p></div>')
    if not article:
      secs.append(
        f'<section class="sec" id="photos" aria-labelledby="h-photos"><details open>'
        f'<summary><span class="sec-num">{num}</span><h2 id="h-photos">Photos &amp; diagrams</h2><span class="chev" aria-hidden="true"></span></summary>'
        f'<div class="sec-body"><p class="muted small">Tap any image to enlarge. DermNet photographs are © DermNet or the named holder, with the source linked under each image. Images marked <span class="badge badge-ai badge-inline">AI diagram</span> are AI-generated teaching illustrations.</p>'
        f'{"".join(groups)}</div></details></section>')

    # references
    if d.get("references"):
        num += 1
        toc.append(f'<li><a href="#references" data-toc="references"><span>{num}</span>References</a></li>')
        def ref_li(r):
            u = r["url"]
            if u.startswith("condition:"):
                slug = u.split(":", 1)[1]
                if slug not in SLUGS:
                    WARNINGS.append(f"{ctx}: reference to unknown condition '{slug}'")
                return f'<li><a href="{p}conditions/{esc(slug)}.html">{esc(r["label"])}</a></li>'
            return f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(r["label"])}</a></li>'
        refs = "".join(ref_li(r) for r in d["references"])
        secs.append(
            f'<section class="sec" id="references" aria-labelledby="h-references"><details open>'
            f'<summary><span class="sec-num">{num}</span><h2 id="h-references">References &amp; further reading</h2><span class="chev" aria-hidden="true"></span></summary>'
            f'<div class="sec-body"><ul class="ref-list">{refs}</ul></div></details></section>')

    soon_banner = ""
    if soon:
        planned = "".join(f"<li>{md(x, p)}</li>" for x in d.get("planned", []))
        mod = d.get("module", "a future module")
        soon_banner = (f'<aside class="callout callout-info soon-banner"><p class="callout-title">Coming soon: {esc(mod)}</p>'
                       '<p>This page is a stub waiting for its research pack. Every section below has its anchor in place, '
                       'and the clinical photos (with attribution) are already filed in the Photos section.</p>'
                       + (f"<p><b>Planned coverage:</b></p><ul>{planned}</ul>" if planned else "") + "</aside>")

    # prev / next (within whole library)
    prev_d = seq[idx - 1] if idx > 0 else None
    next_d = seq[idx + 1] if idx + 1 < len(seq) else None
    pn = '<nav class="prevnext" aria-label="More conditions">'
    pn += (f'<a class="pn pn-prev" href="{p}conditions/{prev_d["slug"]}.html"><small>← Previous</small><b>{esc(prev_d["title"])}</b></a>'
           if prev_d else "<span></span>")
    pn += (f'<a class="pn pn-next" href="{p}conditions/{next_d["slug"]}.html"><small>Next →</small><b>{esc(next_d["title"])}</b></a>'
           if next_d else "<span></span>")
    pn += "</nav>"

    body = f"""
<section class="cond-head" style="--accent:{c['accent']}">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{p}index.html">Home</a><span>›</span><a href="{p}categories/{c['id']}.html">{esc(c['title'])}</a><span>›</span><span aria-current="page">{esc(d['title'])}</span></nav>
    <div class="cond-head-grid{' has-hero' if hero else ''}">
      <div>
        <a class="cat-pill" href="{p}categories/{c['id']}.html">{icon(c['icon'])}{esc(c['title'])}</a>
        <h1>{esc(d['title'])}{' <span class="pill pill-soon">Coming soon</span>' if soon else ''}</h1>
        {f'<p class="module-tag">{esc(d["module"])}</p>' if d.get("module") else ''}
        <p class="lede">{md(d.get('summary', ''), p)}</p>
        {f'<div class="chips chips-aka"><span class="chips-label">Covers</span>{aka}</div>' if aka else ''}
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
      <div class="toc-tools"><button type="button" class="btn-sm" data-expand>Expand all</button><button type="button" class="btn-sm" data-collapse>Collapse all</button></div>
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
                        body_cls="condition"), encoding="utf-8")


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
    for ps in PHOTO_SETS:
        rows = []
        for m in [x for x in MANIFEST if x["_set"] == ps["id"]]:
            pages = ", ".join(sorted(used.get(m["_key"], []))) or "—"
            ref = m["_code"] if ps["id"] == "core" else m["_key"]
            cap = m.get("dermnet_caption") or m.get("source_caption") or ""
            rows.append(
                f'<tr><td data-label="Image"><img class="credit-thumb" src="{esc(m["_dir"])}/{esc(m["filename"])}" alt="" loading="lazy"></td>'
                f'<td data-label="Code"><code>{esc(ref)}</code></td>'
                f'<td data-label="Caption">{esc(cap)}</td>'
                f'<td data-label="©">{esc(m.get("copyright") or "")}</td>'
                f'<td data-label="Source"><a href="{esc(m["source_page_url"])}" target="_blank" rel="noopener">{esc(m["source_page_url"].replace("https://", ""))}</a></td>'
                f'<td data-label="Used on">{esc(pages)}</td></tr>')
        tables.append(f'<h2 class="credits-h" id="set-{ps["id"]}">{esc(ps["label"])} <small>({len(rows)} images · <code>{esc(ps["dir"])}</code>)</small></h2>'
                      '<div class="table-wrap"><table class="rtable credits"><thead><tr><th>Image</th><th>Code</th><th>Caption</th><th>©</th><th>Source page</th><th>Used on</th></tr></thead>'
                      f'<tbody>{"".join(rows)}</tbody></table></div>')
    ai = sorted(x.name for x in (ROOT / "assets/img/ai").glob("*.jpg"))
    ai_li = "".join(f"<li><code>{esc(x)}</code></li>" for x in ai)
    body = f"""
<section class="cat-hero" style="--accent:#0f4c5c"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>›</span><span aria-current="page">Image credits</span></nav>
<h1>Image credits &amp; attribution</h1>
<p class="lede">Clinical photographs are from <a href="https://dermnetnz.org/" target="_blank" rel="noopener">DermNet</a>, plus a few Wikimedia Commons and open-access images, each credited to its holder. DermNet images are reproduced for personal, non-commercial study under the <a href="https://dermnetnz.org/image-licence" target="_blank" rel="noopener">DermNet image licence</a>, as watermarked low-resolution web versions. Copyright remains with DermNet or the named holder.</p>
</div></section>
<section class="wrap block">
{''.join(tables)}
<div class="panel" style="margin-top:2rem"><h2>AI teaching illustrations</h2>
<p class="muted">These were generated for this library as conceptual diagrams. They are not clinical photographs and must not be used for diagnosis.</p><ul class="ai-files">{ai_li}</ul></div>
</section>"""
    (ROOT / "credits.html").write_text(page("Image credits", p, body), encoding="utf-8")


def build_search_index():
    idx = []
    for d in CONDS:
        c = CAT_BY_ID[d["category"]]
        idx.append({
            "t": d["title"], "a": d.get("aka", []), "c": c["title"], "cid": c["id"],
            "s": re.sub(r"\*+", "", d.get("summary", ""))[:180],
            "u": f"conditions/{d['slug']}.html", "soon": d["status"] != "published",
            "col": c["accent"],
        })
    for c in CATS:
        idx.append({"t": c["title"], "a": [c.get("short", "")], "c": "Category", "cid": c["id"],
                    "s": c["blurb"][:180], "u": f"categories/{c['id']}.html", "soon": False,
                    "col": c["accent"], "cat": True})
    js = "/* generated by build.py — do not edit */\nwindow.DERM_SEARCH = " + json.dumps(idx, ensure_ascii=False) + ";\n"
    (ROOT / "assets/js/search-index.js").write_text(js, encoding="utf-8")


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
    pub = sum(1 for d in CONDS if d["status"] == "published")
    print(f"Built: index.html, credits.html, {len(CATS)} category pages, {len(CONDS)} condition pages "
          f"({pub} published, {len(CONDS) - pub} coming soon).")
    for w in WARNINGS:
        print("  WARNING:", w)
    return 1 if WARNINGS and "--strict" in sys.argv else 0


if __name__ == "__main__":
    sys.exit(main())
