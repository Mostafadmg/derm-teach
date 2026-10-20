#!/usr/bin/env python3
"""Build the teaching PDF from the built website (single source of truth).
Run after `python3 build.py --strict`, with the derm-teach venv (WeasyPrint):
    /workspace/derm-teach/.venv/bin/python tools/pdf/build_pdf.py [--only=cat1,cat2] [--out=path.pdf]
Reads conditions/*.html, categories order from content/, legacy front/back matter from ../build/*.html,
downscales images for print into ../build/pdf-img, and writes the PDF + an HTML snapshot."""
import hashlib, json, re, sys, time, datetime
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from PIL import Image

WEB = Path(__file__).resolve().parents[2]
ROOT = WEB.parent
LEG = ROOT / "build"
CACHE = ROOT / "build/pdf-img"; CACHE.mkdir(parents=True, exist_ok=True)
ARGS = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
OUT = Path(ARGS.get("out", WEB / "assets/pdf/Primary-Care-Dermatology-Pharmacist-Prescriber.pdf"))
ONLY = set(ARGS["only"].split(",")) if ARGS.get("only") else None

load = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))
SITE = load(WEB / "content/site.json")
CATS = sorted(load(WEB / "content/categories.json"), key=lambda c: c.get("order", 99))
CAT_BY_ID = {c["id"]: c for c in CATS}
CONDS = [load(f) for f in sorted((WEB / "content/conditions").glob("*.json")) if not f.name.startswith("_")]
CONDS = [d for d in CONDS if d.get("status") == "published"]
if ARGS.get("slugs"): CONDS = [d for d in CONDS if d["slug"] in ARGS["slugs"].split(",")]
CONDS.sort(key=lambda d: (CAT_BY_ID[d["category"]].get("order", 99), d["order"], d["title"]))
SLUGS = {d["slug"] for d in CONDS}
BY_CAT = {c["id"]: [d for d in CONDS if d["category"] == c["id"]] for c in CATS}

# ---------------------------------------------------------------- images
def img_url(src, base):
    """local, print-sized copy of an image referenced from an HTML file in `base`"""
    if not src or src.startswith(("http:", "https:", "data:")):
        return src
    p = (base / src.split("?")[0]).resolve()
    if not p.exists():
        print("  missing image", p); return src
    ai = "/img/ai/" in str(p)
    mx = 1000 if ai else 640
    key = hashlib.md5(f"{p}:{p.stat().st_mtime}:{mx}".encode()).hexdigest()[:16]
    out = CACHE / f"{key}.jpg"
    if not out.exists():
        im = Image.open(p)
        if im.mode in ("RGBA", "LA", "P"):
            im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[-1]); im = bg
        im = im.convert("RGB"); im.thumbnail((mx, mx), Image.LANCZOS)
        im.save(out, "JPEG", quality=68 if ai else 66, optimize=True, progressive=False)
    return out.as_uri()

def fix_links(root, base):
    for a in root.find_all("a", href=True):
        h = a["href"]
        m = re.match(r"^(?:\.\./)?(?:conditions/)?([a-z0-9-]+)\.html(?:#.*)?$", h)
        mc = re.match(r"^(?:\.\./)?categories/([a-z0-9-]+)\.html", h)
        if h.startswith(("http:", "https:", "mailto:")):
            continue
        if mc and mc.group(1) in CAT_BY_ID: a["href"] = f"#cat-{mc.group(1)}"
        elif m and m.group(1) in SLUGS: a["href"] = f"#c-{m.group(1)}"
        elif "credits.html" in h: a["href"] = "#credits"
        elif h.startswith("#"): pass
        else: a.unwrap()

def clean(root, base, prefix):
    for sel in ["nav.crumbs", "nav.prevnext", "aside.toc", ".toc-tools", "button.btn-sm", ".lb-bar", "script",
                ".les-state", ".chip-ph img", "[data-print]", ".gal-tools", ".sr-only"]:
        for e in root.select(sel): e.decompose()
    for b in root.select("button.f-btn"): b.unwrap()
    for b in root.find_all("button"): b.name = "span"
    for d in root.find_all("details"): d["open"] = ""
    for img in root.find_all("img"):
        img["src"] = img_url(img.get("src"), base)
        for k in ("loading", "decoding", "srcset", "sizes"): img.attrs.pop(k, None)
    # unique ids per page
    for e in root.find_all(id=True): e["id"] = f"{prefix}-{e['id']}"
    for a in root.find_all("a", href=True):
        if a["href"].startswith("#") and not a["href"].startswith(("#c-", "#cat-", "#credits")):
            a["href"] = f"#{prefix}-{a['href'][1:]}"
    fix_links(root, base)
    return root

# ---------------------------------------------------------------- pages
def condition_html(d):
    f = WEB / "conditions" / f"{d['slug']}.html"
    s = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
    base = f.parent
    head = s.select_one("section.tb-head, section.page-head")
    body = s.select_one("article.tb-body, article.cond-body")
    for x in (head, body): clean(x, base, d["slug"])
    if head.h1: head.h1["class"] = head.h1.get("class", []) + ["c-title"]
    kind = "tb" if "tb-head" in head.get("class", []) else "art"
    return (f'<section class="cond cond-{kind}{" layout-article" if kind == "art" else ""}" id="c-{d["slug"]}" data-cat="{d["category"]}">'
            f'{head.decode_contents() if head.select_one(".wrap") is None else head.select_one(".wrap").decode_contents()}'
            f'<div class="cond-main">{body.decode_contents()}</div></section>')

def legacy(fname, sid=None, title=None):
    p = LEG / fname
    s = BeautifulSoup(p.read_text(encoding="utf-8"), "lxml")
    secs = s.select("section.front")
    if title: secs = [x for x in secs if x.get("data-title") == title]
    out = []
    for x in secs:
        for img in x.find_all("img"): img["src"] = img_url(img.get("src"), p.parent)
        for e in x.find_all(id=True): e["id"] = "leg-" + e["id"]
        for a in x.find_all("a", href=True):
            if not a["href"].startswith(("http", "mailto")): a.unwrap()
        out.append(f'<section class="legacy">{x.decode_contents()}</section>')
    return "".join(out)

def credits_html():
    f = WEB / "credits.html"; s = BeautifulSoup(f.read_text(encoding="utf-8"), "lxml")
    m = s.select_one("main") or s.body
    for e in m.select("header.topbar, footer, .drawer, .lightbox, nav.crumbs, .chips.jump, form, input"):
        e.decompose()
    clean(m, f.parent, "cr")
    for img in m.find_all("img"): img.decompose()   # credits list is text-only in print (thumbnails already appear with every figure)
    return m.decode_contents()

def cover_photos():
    """six real clinical photographs (card photos) for the cover"""
    man = {}
    for ps in load(WEB / "content/photo-sets.json"):
        for m in load(WEB / ps["manifest"]):
            code = Path(m["filename"]).name.split("_")[0]
            man[code if ps["id"] == "core" else f'{ps["id"]}:{code}'] = WEB / ps["dir"] / m["filename"]
    picks = ["eczema-dermatitis", "psoriasis", "acne-vulgaris", "impetigo", "melanoma", "tinea", "urticaria-angioedema"]
    out = []
    for slug in picks:
        f = WEB / "content/conditions" / f"{slug}.json"
        if not f.exists(): continue
        d = load(f)
        ci = d.get("card_image")
        ci = ci.get("dermnet") if isinstance(ci, dict) else ci
        if ci in man:
            out.append(f'<div class="cv-ph"><img src="{img_url(str(man[ci]), WEB)}" alt=""></div>')
    return "".join(out[:6])

def main():
    t0 = time.time()
    cats = [c for c in CATS if BY_CAT[c["id"]] and (not ONLY or c["id"] in ONLY)]
    body_cats = [c for c in cats if c["id"] != "exam-review"]
    exam = [c for c in cats if c["id"] == "exam-review"]
    today = datetime.date.today().strftime("%-d %B %Y")
    n_pages = sum(len(BY_CAT[c["id"]]) for c in body_cats)
    toc = []
    for i, c in enumerate(body_cats, 1):
        items = "".join(f'<li><a href="#c-{d["slug"]}">{d["title"]}</a></li>' for d in BY_CAT[c["id"]])
        toc.append(f'<li class="ptoc-ch"><a href="#cat-{c["id"]}"><b>{i}</b> {c["title"]}</a><ol>{items}</ol></li>')
    app = [("A", "Exam review: modules 2, 4 and 5", "app-exam"), ("B", "Shared red flags and study tips", "app-rf"),
           ("C", "Course module overviews (original guide)", "app-mod"), ("D", "Sources and further reading", "app-src"),
           ("E", "Image credits and photo attributions", "credits")]
    toc.append('<li class="ptoc-ch ptoc-app"><b>Appendices</b><ol>' + "".join(
        f'<li><a href="#{a}">{k} · {t}</a></li>' for k, t, a in app) + "</ol></li>")
    parts = [f"""
<section class="cover">
  <p class="cv-k">Teaching &amp; revision guide · UK primary care · {today}</p>
  <h1 class="cv-t">Primary Care Dermatology for Pharmacist Prescribers</h1>
  <p class="cv-s">Diagnose, differentiate &amp; manage — the Derm Teach library in print</p>
  <div class="cv-grid">{cover_photos()}</div>
  <p class="cv-who"><b>{SITE.get('owner', 'Mostafa Damghani')}</b><br>Pharmacist independent prescriber · personal study notes</p>
  <p class="cv-meta">{len(body_cats)} chapters · {n_pages} condition pages · exam review appendix · real clinical photographs © DermNet or named holders · AI teaching diagrams are labelled</p>
  <p class="cv-disc"><b>Personal study resource, not clinical guidance.</b> Doses, licences and pathways change: always check the current BNF / BNF for Children, NICE CKS, SmPC, MHRA alerts and your local formulary before prescribing.</p>
</section>
<section class="front" id="howto"><h2 class="fm-h">How to use this edition</h2>
<p>This PDF is generated directly from the Derm Teach website, so every condition page has the same 13-part textbook structure as the site: overview, epidemiology, aetiology, step-by-step pathophysiology, clinical features, diagnosis, differentials (with real photographs), management with drug cards and a treatment ladder, red flags and referral, complications, prescriber pearls, a self-check quiz, references and the full photo gallery.</p>
<ul><li><b>Real photographs</b> carry their holder and source under each image. <b>AI diagrams</b> are labelled “AI diagram” and are teaching illustrations only.</li>
<li>Coloured boxes: <b>red</b> = red flags / urgent referral, <b>green</b> = prescriber pearls, <b>blue</b> = key facts.</li>
<li>Page references in the contents and cross-links between conditions are clickable.</li>
<li>Appendix A reproduces the module 2, 4 and 5 exam reviews; appendix B is a one-page red-flag summary for quick revision.</li></ul>
</section>
{legacy('00-front.html', title='Core prescribing principles')}
<section class="toc-page" id="contents"><h2 class="fm-h">Contents</h2><ol class="ptoc">{''.join(toc)}</ol></section>
"""]
    for i, c in enumerate(body_cats, 1):
        ds = BY_CAT[c["id"]]
        lst = "".join(f"<li>{d['title']}</li>" for d in ds)
        parts.append(f'<section class="chap" id="cat-{c["id"]}" style="--accent:{c.get("accent", "#0d5e63")}"><p class="ch-n">Chapter {i}</p>'
                     f'<h1 class="ch-t">{c["title"]}</h1><p class="ch-b">{c.get("blurb", "")}</p><ol class="ch-l">{lst}</ol></section>')
        for d in ds:
            parts.append(condition_html(d)); print(f"  {d['slug']}", flush=True)
    parts.append('<section class="chap app" id="app-exam"><p class="ch-n">Appendix A</p><h1 class="ch-t">Exam review</h1>'
                 '<p class="ch-b">The module 2, 4 and 5 end-of-module exams with the recommended UK answer and why the distractors are wrong.</p></section>')
    for c in exam:
        for d in BY_CAT[c["id"]]: parts.append(condition_html(d))
    parts.append('<section class="chap app" id="app-rf"><p class="ch-n">Appendix B</p><h1 class="ch-t">Shared red flags &amp; study tips</h1></section>')
    parts.append(legacy("06-back.html", title="Shared red flags") + legacy("06-back.html", title="Study tips"))
    parts.append('<section class="chap app" id="app-mod"><p class="ch-n">Appendix C</p><h1 class="ch-t">Course module overviews</h1>'
                 '<p class="ch-b">Carried over from the original guide. Chapter letters refer to the original edition; the content now lives in the chapters above.</p></section>')
    for f in ("10A-modules1-2-overview.html", "06X-modules3-5-overview.html", "05M-module6-overview.html", "08X0-fold-overview.html"):
        parts.append(legacy(f))
    parts.append(legacy("00-front.html", title="Quick visual comparison"))
    parts.append('<section class="chap app" id="app-src"><p class="ch-n">Appendix D</p><h1 class="ch-t">Sources &amp; further reading</h1></section>')
    parts.append(legacy("06-back.html", title="Sources"))
    parts.append(f'<section class="chap app" id="credits"><p class="ch-n">Appendix E</p><h1 class="ch-t">Image credits</h1></section><section class="credits">{credits_html()}</section>')
    css = "".join(f'<link rel="stylesheet" href="{(WEB / "assets/css" / n).as_uri()}">' for n in ("style.css", "v3.css", "v4.css", "v5.css"))
    css += f'<link rel="stylesheet" href="{(WEB / "tools/pdf/pdf.css").as_uri()}">'
    html = (f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Primary Care Dermatology for Pharmacist Prescribers</title>'
            f'<meta name="author" content="{SITE.get("owner", "Mostafa Damghani")}"><meta name="description" content="Derm Teach — printed edition">{css}</head>'
            f'<body class="pdf">{"".join(parts)}</body></html>')
    snap = ROOT / "build/pdf-snapshot.html"; snap.write_text(html, encoding="utf-8")
    print(f"html assembled in {time.time() - t0:.0f}s; rendering…", flush=True)
    from weasyprint import HTML
    doc = HTML(string=html, base_url=str(WEB) + "/").render()
    print(f"laid out {len(doc.pages)} pages in {time.time() - t0:.0f}s", flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.write_pdf(str(OUT))
    if OUT.parent == WEB / "assets/pdf":
        (OUT.parent / "pdf-meta.json").write_text(json.dumps({"file": OUT.name, "pages": len(doc.pages),
            "mb": round(OUT.stat().st_size / 1e6, 1), "built": today}) + "\n")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB, {len(doc.pages)} pages) in {time.time() - t0:.0f}s")

if __name__ == "__main__":
    main()
