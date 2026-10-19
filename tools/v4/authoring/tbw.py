import json, pathlib
ROOT = pathlib.Path('/workspace/derm-teach/website')
SLUGS = {p.stem for p in (ROOT/'content/conditions').glob('*.json')}
def S(id, title, *blocks, short=None):
    if isinstance(title, tuple): title, short = title
    d = {"id": id, "title": title, "blocks": list(blocks)}
    if short: d["short"] = short
    return d
def H(t, id=None): return {"h": t, **({"id": id} if id else {})}
def H4(t): return {"h4": t}
def UL(*x): return {"ul": list(x)}
def OL(*x): return {"ol": list(x)}
def N(t, *sub): return {"t": t, "sub": list(sub)}
def FIG(x, cap=None):
    d = {"fig": x}
    if cap: d["caption"] = cap
    return d
def AI(f, cap, alt=None): return {"ai": f, "caption": cap, "alt": alt or cap}
def MECH(*steps): return {"mech": [dict(k=k, t=t, img=img, caption=cap) if img else dict(k=k, t=t) for k, t, img, cap in steps]}
def HISTO(*x): return {"histo": list(x)}
def LES(*x, key="lesions"):
    out = []
    for it in x:
        name, t, photo = it[:3]
        d = {"name": name, "t": t}
        if photo: d["photo"] = photo
        if len(it) > 3 and it[3]: d.update(it[3])
        out.append(d)
    return {key: out}
def VAR(*x): return LES(*x, key="variants")
def MAP(img, cap, *pts): return {"bodymap": {"img": {"ai": img}, "caption": cap, "pts": list(pts)}}
def DDX(*rows):
    out = []
    for r in rows:
        name, f = r[0], r[1]
        d = {"name": name.lstrip("!"), "f": f}
        if name.startswith("!"): d["danger"] = True
        if len(r) > 2 and r[2]:
            assert r[2] in SLUGS, r[2]; d["link"] = r[2]
        if len(r) > 3 and r[3]: d["photo"] = r[3]
        out.append(d)
    return {"ddx": out}
def DRUGS(*x): return {"drugs": list(x)}
def D(name, **kw): return dict(name=name, **kw)
def LAD(*x): return {"ladder": [dict(k=k, t=t, tone=tone) for k, t, tone in x]}
def REF(*x): return {"refer": [dict(when=w, t=t) for w, t in x]}
def PEARLS(*x): return {"pearls": list(x)}
def CO(tone, title, text=None, lst=None):
    d = {"callout": tone, "title": title}
    if text: d["text"] = text
    if lst: d["list"] = lst
    return d
def TABLE(head, *rows, caption=None):
    t = {"head": head, "rows": [list(r) for r in rows]}
    if caption: t["caption"] = caption
    return {"table": t}
def WRITE(slug, key_facts, sections, quiz, refs=(), see_also=()):
    for s in see_also: assert s in SLUGS, s
    d = {"_note": "v4 textbook page. Draft for clinical sign-off; doses only as in source notes / BNF.",
         "key_facts": key_facts, "sections": sections, "quiz": [dict(q=q, a=a) for q, a in quiz],
         "references": [dict(label=l, url=u) for l, u in refs], "see_also": list(see_also)}
    (ROOT/'content/textbook'/f'{slug}.json').write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    print('wrote', slug, len(json.dumps(d)))
