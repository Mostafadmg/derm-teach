# Derm Teach v4: textbook-style condition pages (DermNet / Medscape order).
# Executed inside build.py's namespace (uses md, esc, ui, uix, fig3, render_table, render_blocks, BY_SLUG ...).
# Content: content/textbook/<slug>.json  ->  {"key_facts": [...], "sections": [{"id","title","blocks"}], "quiz": [...]}
# Every page also gets the collapsed photo gallery and the references from the condition JSON.

TB_DIR = CONTENT / "textbook"
TB_ORDER = ["overview", "epidemiology", "aetiology", "pathophysiology", "clinical-features", "diagnosis",
            "differentials", "management", "red-flags", "complications", "pearls"]


def tb_exists(slug):
    return (TB_DIR / f"{slug}.json").exists()


_KV = re.compile(r'^<strong>([^<]{1,60}?)(:)</strong>\s*(\S.*)$', re.S)
_KV2 = re.compile(r'^<strong>([^<]{1,60}?)</strong>:\s*(\S.*)$', re.S)


def tb_kv(html_s):
    """'<strong>Label:</strong> value' -> stacked label/value (text unchanged; colon kept for screen readers/copy)"""
    m = _KV.match(html_s) or _KV2.match(html_s)
    if not m:
        return None
    k, v = m.group(1).strip(), m.groups()[-1]
    return f'<span class="kv-k">{k}<span class="kv-c">:</span></span> <span class="kv-v">{v}</span>'


def tb_li(x, p):
    if isinstance(x, str):
        h = md(x, p); kv = tb_kv(h)
        return f'<li class="kv">{kv}</li>' if kv else f"<li>{h}</li>"
    sub = x.get("sub") or []
    h = md(x["t"], p); kv = tb_kv(h)
    subh = f'<ul>{"".join(tb_li(s, p) for s in sub)}</ul>' if sub else ""
    return (f'<li class="kv">{kv}' if kv else f'<li>{h}') + subh + "</li>"


def tb_ul(items, p, cls=""):
    lis = [tb_li(x, p) for x in items]
    nkv = sum(1 for x in lis if x.startswith('<li class="kv">'))
    if lis and nkv * 2 >= len(lis) and nkv >= 2:
        cls = (cls + " tb-kv").strip()
    c = f' class="{cls}"' if cls else ""
    return f"<ul{c}>" + "".join(lis) + "</ul>"


def tb_fig(item, p, ctx, cls=""):
    if isinstance(item, dict) and "photo" in item and "dermnet" not in item and "ai" not in item:
        item = dict(item, dermnet=item["photo"])
    return fig3(item, p, ctx, cls)


def tb_photo_item(x):
    """photo field: 'm6w3:N01' | {'ai': ...} | None"""
    ph = x.get("photo") or x.get("img")
    if not ph:
        return None
    if isinstance(ph, str):
        return {"dermnet": ph} if not ph.endswith(".jpg") else {"ai": ph}
    return ph


_CASE = re.compile(r'^\s*(Case\s*\d+[a-z]?)\s*[:.\u2013\u2014-]\s*(\S.*)$', re.S | re.I)


def tb_blocks(blocks, p, ctx):
    out = []
    case_open = False
    for b in blocks:
        if isinstance(b, str):
            out.append(f"<p>{md(b, p)}</p>")
            continue
        k = next(iter(b))
        if k == "p":
            out.append(f"<p>{md(b['p'], p)}</p>")
        elif k == "h":
            hid = f' id="{esc(b["id"])}"' if b.get("id") else ""
            if case_open:
                out.append("</div>"); case_open = False
            cm = _CASE.match(b["h"])
            if cm:
                out.append(f'<div class="tb-case"><h3 class="tb-h3 tb-case-h"{hid}><span class="case-badge">{esc(cm.group(1))}<span class="kv-c">:</span></span> '
                           f'<span class="case-t">{md(cm.group(2), p)}</span></h3>')
                case_open = True
            else:
                out.append(f'<h3 class="tb-h3"{hid}>{md(b["h"], p)}</h3>')
        elif k == "h4":
            out.append(f'<h4 class="tb-h4">{md(b["h4"], p)}</h4>')
        elif k == "ul":
            out.append(tb_ul(b["ul"], p, "tb-ul"))
        elif k == "ol":
            out.append('<ol class="tb-ol">' + "".join(tb_li(x, p) for x in b["ol"]) + "</ol>")
        elif k == "table":
            t = dict(b["table"]); cap = t.pop("caption", "")
            out.append(render_table(t, p) + (f'<p class="tb-note">{md(cap, p)}</p>' if cap else ""))
        elif k == "callout":
            out.append(render_blocks([b], p, ctx))
        elif k == "fig":
            cap = b.get("caption")
            item = b["fig"] if isinstance(b["fig"], dict) else ({"ai": b["fig"]} if b["fig"].endswith(".jpg") else {"dermnet": b["fig"]})
            if cap:
                item = dict(item, caption=cap)
            out.append(f'<div class="tb-fig">{fig3(item, p, ctx, "f-tb")}</div>')
        elif k == "figs":
            items = []
            for it in b["figs"]:
                if isinstance(it, str):
                    it = {"ai": it} if it.endswith(".jpg") else {"dermnet": it}
                items.append(fig3(it, p, ctx, "f-tb"))
            out.append(f'<div class="tb-figs n{min(len(items), 3)}">{"".join(items)}</div>')
        elif k == "mech":
            steps = []
            for i, s in enumerate(b["mech"]):
                img = tb_photo_item(s)
                fig = fig3(dict(img, caption=s.get("caption", "")), p, ctx, "f-mech") if img else ""
                steps.append(f'<li class="mech-step{" has-img" if fig else ""}"><div class="mech-t"><span class="mech-n" aria-hidden="true">{i + 1}</span>'
                             f'<div><p class="mech-k">{md(s["k"], p)}</p>' + (f'<p>{md(s["t"], p)}</p>' if s.get("t") else "")
                             + (tb_ul(s["pts"], p, "tb-ul") if s.get("pts") else "") + f"</div></div>{fig}</li>")
            out.append(f'<ol class="mech">{"".join(steps)}</ol>')
        elif k == "histo":
            out.append(f'<div class="tb-box tb-histo"><p class="tb-box-k">{uix("search", "ui ui-sm")}Histopathology</p>{tb_ul(b["histo"], p, "tb-ul")}</div>')
        elif k in ("lesions", "variants"):
            cards = []
            for v in b[k]:
                img = tb_photo_item(v)
                fig = fig3(dict(img, caption=v.get("caption")) if v.get("caption") else img, p, ctx, "f-les", cap=bool(v.get("caption"))) if img else ""
                link = (f' <a class="tb-link" href="{p}conditions/{esc(v["link"])}.html">Open page{ui("arrow", "ui ui-xs")}</a>' if v.get("link") in BY_SLUG else "")
                cards.append(f'<li class="les-card{" is-danger" if v.get("danger") else ""}"><h4>{md(v["name"], p)}</h4>'
                             f'<p>{md(v.get("t", ""), p)}{link}</p>{fig}</li>')
            out.append(f'<ul class="les-cards">{"".join(cards)}</ul>')
        elif k == "bodymap":
            bm = b["bodymap"]
            img = tb_photo_item(bm)
            fig = fig3(dict(img, caption=bm.get("caption", "")), p, ctx, "f-map") if img else ""
            out.append(f'<div class="tb-map">{tb_ul(bm.get("pts", []), p, "tb-ul")}{fig}</div>')
        elif k == "ddx":
            rows = []
            for r in b["ddx"]:
                img = tb_photo_item(r)
                if not img and r.get("link") in BY_SLUG and BY_SLUG[r["link"]].get("card_image"):
                    ci = BY_SLUG[r["link"]]["card_image"]
                    img = {"dermnet": ci} if isinstance(ci, str) else ci
                th = (f'<div class="dd-th">{fig3(img, p, ctx, "f-thumb", cap=False)}</div>' if img
                      else f'<div class="dd-th is-empty" aria-hidden="true">{uix("alert" if r.get("danger") else "eye", "ui ui-sm")}</div>')
                name = md(r["name"], p)
                if r.get("link") in BY_SLUG:
                    name = f'<a href="{p}conditions/{esc(r["link"])}.html">{name}</a>'
                rows.append(f'<tr class="{"is-danger" if r.get("danger") else ""}"><td class="dd-img">{th}</td><th scope="row">{name}</th>'
                            f'<td>{md(r["f"], p)}</td></tr>')
            out.append('<div class="dd-wrap"><table class="dd"><thead><tr><th scope="col"><span class="sr-only">Photo</span></th>'
                       '<th scope="col">Condition</th><th scope="col">Distinguishing features</th></tr></thead>'
                       f'<tbody>{"".join(rows)}</tbody></table></div>')
        elif k == "drugs":
            cards = []
            for dr in b["drugs"]:
                rows = "".join(f'<div class="dc-row"><dt>{lbl}</dt><dd>{md(dr[key], p) if isinstance(dr[key], str) else tb_ul(dr[key], p)}</dd></div>'
                               for key, lbl in (("dose", "Dose"), ("use", "Use"), ("cautions", "Cautions"), ("counsel", "Counselling"),
                                                ("monitor", "Monitoring")) if dr.get(key))
                cards.append(f'<article class="dc{" dc-spec" if dr.get("specialist") else ""}"><header><h4>{md(dr["name"], p)}</h4>'
                             + (f'<span class="dc-cls">{md(dr["cls"], p)}</span>' if dr.get("cls") else "")
                             + (f'<span class="dc-tag">Specialist only</span>' if dr.get("specialist") else "")
                             + f"</header><dl>{rows}</dl></article>")
            out.append(f'<div class="dcs">{"".join(cards)}</div>')
        elif k == "ladder":
            rungs = []
            for i, r in enumerate(b["ladder"]):
                rungs.append(f'<li class="lad tone-{esc(r.get("tone", ""))}"><span class="lad-n" aria-hidden="true">{i + 1}</span>'
                             f'<div><p class="lad-k">{md(r["k"], p)}</p><p class="lad-t">{md(r["t"], p)}</p></div></li>')
            out.append(f'<ol class="lads" aria-label="Treatment ladder">{"".join(rungs)}</ol>')
        elif k == "refer":
            items = "".join(
                f'<li class="rf tone-{URGENCY.get(x.get("when", "routine"), URGENCY["routine"])[1]}">'
                f'<span class="rf-tag">{URGENCY.get(x.get("when", "routine"), URGENCY["routine"])[0]}</span><p>{md(x["t"], p)}</p></li>'
                for x in b["refer"])
            out.append(f'<ul class="rfs">{items}</ul>')
        elif k == "pearls":
            out.append('<ul class="pearls">' + "".join(
                f'<li><span class="pe-ico">{uix("bulb", "ui ui-sm")}</span><p>{md(x, p)}</p></li>' for x in b["pearls"]) + "</ul>")
        else:
            WARNINGS.append(f"{ctx}: unknown textbook block '{k}'")
    if case_open:
        out.append("</div>")
    return "\n".join(out)


def build_condition_tb(d, idx, seq):
    p = "../"
    c = CAT_BY_ID[d["category"]]
    ctx = d["slug"]
    tb = load_json(TB_DIR / f"{d['slug']}.json")
    secs, toc = [], []
    for s in tb["sections"]:
        sid = s["id"]
        tone = {"red-flags": " tb-danger", "pearls": " tb-tip"}.get(sid, "")
        secs.append(f'<section class="sec tb-sec{tone}" id="{esc(sid)}" aria-labelledby="h-{esc(sid)}">'
                    f'<h2 id="h-{esc(sid)}">{esc(s["title"])}</h2>{tb_blocks(s.get("blocks", []), p, f"{ctx}/{sid}")}</section>')
        toc.append(f'<li><a href="#{esc(sid)}" data-toc="{esc(sid)}">{esc(s.get("short", s["title"]))}</a></li>')
    # self-check (optional, collapsed)
    if tb.get("quiz"):
        qs = "".join(f'<li><details class="qa"><summary><span class="qa-n">Q{i + 1}</span><span class="qa-q">{md(x["q"], p)}</span>'
                     f'<span class="qa-reveal">Reveal</span></summary><p class="qa-a">{uix("check", "ui ui-sm")}<span>{md(x["a"], p)}</span></p></details></li>'
                     for i, x in enumerate(tb["quiz"]))
        secs.append(f'<section class="sec tb-sec tb-quiz" id="quiz" aria-labelledby="h-quiz"><details class="tb-fold">'
                    f'<summary><h2 id="h-quiz">Self-check quiz</h2><small>{len(tb["quiz"])} questions · optional</small>{ui("chev-d", "ui chev")}</summary>'
                    f'<ol class="quiz">{qs}</ol></details></section>')
        toc.append('<li><a href="#quiz" data-toc="quiz">Self-check</a></li>')
    # references (open) + gallery (collapsed)
    refs = list(d.get("references", [])) + [r for r in tb.get("references", []) if r["url"] not in {x["url"] for x in d.get("references", [])}]
    if refs:
        def ref_li(r):
            u = r["url"]
            if u.startswith("condition:"):
                return f'<li><a href="{p}conditions/{esc(u.split(":", 1)[1])}.html">{esc(r["label"])}</a></li>'
            host = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
            return f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(r["label"])}</a><span class="ref-host">{esc(host)}</span></li>'
        secs.append(f'<section class="sec tb-sec" id="references" aria-labelledby="h-references"><h2 id="h-references">References</h2>'
                    f'<ol class="ref-list">{"".join(ref_li(r) for r in refs)}</ol></section>')
        toc.append('<li><a href="#references" data-toc="references">References</a></li>')
    n_img = count_photos(d)
    if d.get("photos"):
        groups = []
        for g in d["photos"]:
            figs = "".join(fig3(x, p, ctx) for x in g.get("items", []))
            groups.append(f'<div class="gal-group{" gal-danger" if g.get("tone") == "danger" else ""}"><h3>{md(g.get("title", ""), p)}<span class="gal-n">{len(g.get("items", []))}</span></h3>'
                          f'<div class="gallery g3">{figs}</div></div>')
        secs.append(f'<section class="sec tb-sec tb-gal" id="photos" aria-labelledby="h-photos"><details class="tb-fold">'
                    f'<summary><h2 id="h-photos">Photo gallery</h2><small>{plural(n_img, "image")}</small>{ui("chev-d", "ui chev")}</summary>'
                    f'<div class="tb-gal-body">{"".join(groups)}</div></details></section>')
        toc.append('<li><a href="#photos" data-toc="photos">Photos</a></li>')
    prev_d = seq[idx - 1] if idx > 0 else None
    next_d = seq[idx + 1] if idx + 1 < len(seq) else None

    def pn_link(x, cls, lbl):
        cx = CAT_BY_ID[x["category"]]
        return (f'<a class="pn {cls}" href="{p}conditions/{x["slug"]}.html" style="--accent:{cx["accent"]}">'
                f'<small>{lbl}</small><b>{esc(x["title"])}</b><span class="pn-cat">{esc(cx["title"])}</span></a>')
    pn = ('<nav class="prevnext" aria-label="More conditions">'
          + (pn_link(prev_d, "pn-prev", f'{ui("arrow-l", "ui ui-xs")}Previous') if prev_d else "<span></span>")
          + (pn_link(next_d, "pn-next", f'Next{ui("arrow", "ui ui-xs")}') if next_d else "<span></span>") + "</nav>")
    aka = d.get("aka", [])
    aka_html = "".join(f'<span class="chip-soft">{esc(a)}</span>' for a in aka[:6]) + (f'<span class="chip-soft is-more">+{len(aka) - 6}</span>' if len(aka) > 6 else "")
    kf = tb.get("key_facts") or []
    kf_html = (f'<aside class="keyfacts" aria-label="Key facts"><p class="kf-k">Key facts</p>{tb_ul(kf, p, "kf-list")}</aside>' if kf else "")
    see = tb.get("see_also") or []
    see_html = ("".join(f'<a class="chip-soft chip-link" href="{p}conditions/{esc(s)}.html">{esc(BY_SLUG[s]["title"])}</a>' for s in see if s in BY_SLUG))
    body = f"""
<section class="tb-head" id="top" style="--accent:{c['accent']}">
  <div class="wrap">
    {crumbs([("Home", f"{p}index.html"), (c['title'], f"{p}categories/{c['id']}.html"), (d['title'], None)])}
    <p class="lesson-k"><a href="{p}categories/{c['id']}.html">{icon(c['icon'])}{esc(c['title'])}</a>{f'<span>{esc(d["module"])}</span>' if d.get("module") else ''}</p>
    <h1>{esc(d['title'])}</h1>
    <p class="lede">{md(d.get('summary', ''), p)}</p>
    {f'<div class="chip-row aka"><span class="chip-lbl">Also called</span>{aka_html}</div>' if aka else ''}
    {f'<div class="chip-row aka"><span class="chip-lbl">Related pages</span>{see_html}</div>' if see_html else ''}
    {kf_html}
  </div>
</section>
<div class="wrap cond-layout tb-layout" style="--accent:{c['accent']}">
  <aside class="toc tb-toc" aria-label="On this page">
    <div class="toc-in">
      <p class="toc-title">On this page</p>
      <ol class="toc-list">{''.join(toc)}</ol>
      <div class="toc-tools"><button type="button" class="btn-sm" data-print>{ui("print", "ui ui-xs")}Print</button></div>
    </div>
  </aside>
  <article class="cond-body tb-body">
    {''.join(secs)}
    {pn}
  </article>
</div>
"""
    out = ROOT / "conditions" / f"{d['slug']}.html"
    out.write_text(page(d["title"], p, body, desc=d.get("summary", ""), active_slug=d["slug"], active_cat=c["id"],
                        body_cls="condition textbook"), encoding="utf-8")
    html_s = out.read_text(encoding="utf-8")
    for g in d.get("photos", []):
        for it in g.get("items", []):
            ph = resolve_photo(it, p, ctx)
            if ph and f'data-src="{esc(ph["src"])}"' not in html_s:
                WARNINGS.append(f"{ctx}: photo {it} not placed on the page")
    LESSON_META[d["slug"]] = {"steps": 0, "mins": 0, "sections": len(tb["sections"])}


# ---------------------------------------------------------------- split pages (old combined slugs)
def build_redirects():
    f = CONTENT / "redirects.json"
    if not f.exists():
        return
    for old, r in load_json(f).items():
        links = "".join(f'<li><a href="{esc(t)}.html">{esc(BY_SLUG[t]["title"])}</a></li>' for t in r["to"] if t in BY_SLUG)
        first = r["to"][0]
        body = (f'<section class="tb-head"><div class="wrap"><h1>{esc(r["title"])}</h1>'
                f'<p class="lede">{esc(r.get("note", "This topic now has separate pages."))}</p>'
                f'<ul class="tb-ul split-list">{links}</ul></div></section>')
        html_s = page(r["title"], "../", body, desc=r.get("note", ""), body_cls="redirect")
        html_s = html_s.replace("<head>", f'<head><link rel="canonical" href="{esc(first)}.html">', 1)
        (ROOT / "conditions" / f"{old}.html").write_text(html_s, encoding="utf-8")
