"""Split helpers (Oct 2026). Used by tools/v4/authoring/s/*.py. See ADD_CONDITION.md 'Splitting a combined page'."""
import json, pathlib, shutil, re
ROOT = pathlib.Path(__file__).resolve().parents[2]
C = ROOT / "content"
BK = pathlib.Path("/workspace/backups/splits")
def _w(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
def L(*items): return {"list": list(items)}
def H(t): return {"h": t}
def T(head, *rows): return {"table": {"head": head, "rows": [list(r) for r in rows]}}
def page(slug, base=None, **c):
    b = json.loads((C / "conditions" / f"{base}.json").read_text()) if base and (C / "conditions" / f"{base}.json").exists() else {}
    d = {"slug": slug, "title": c.pop("title"), "category": c.pop("category", b.get("category")), "status": "published",
         "order": c.pop("order", b.get("order", 1)), "module": c.pop("module", b.get("module", "")),
         "aka": c.pop("aka", []), "summary": c.pop("summary"), **({"card_image": c.pop("card_image")} if "card_image" in c else {}),
         "sections": {k: c.pop(k, []) for k in ("what", "cause", "features", "diagnosis", "differentials", "management", "red_flags", "pearls")},
         "photos": c.pop("photos", []), "references": [{"label": l, "url": u} for l, u in c.pop("refs", [])]}
    assert not c, c
    _w(C / "conditions" / f"{slug}.json", d)
def steps(slug, **d):
    d = {"_note": "curated (split page, Oct 2026)", **d}
    _w(C / "steps" / f"{slug}.json", d)
def retire(old, title, note, to):
    r = json.loads((C / "redirects.json").read_text()); r[old] = {"title": title, "note": note, "to": to}; _w(C / "redirects.json", r)
    for sub in ("conditions", "steps", "steps/_auto", "textbook", "textbook-src"):
        p = C / sub / f"{old}.json"
        if p.exists():
            (BK / sub).mkdir(parents=True, exist_ok=True); shutil.move(str(p), str(BK / sub / p.name))
def relink(old, default):
    """replace condition:old links with condition:default in all content JSON; returns files touched"""
    hits = []
    for p in C.rglob("*.json"):
        s = p.read_text(encoding="utf-8")
        if f"condition:{old})" in s or f'"link": "{old}"' in s or f'"{old}"' in s and p.parent.name in ("textbook-src",):
            s2 = s.replace(f"condition:{old})", f"condition:{default})").replace(f'"link": "{old}"', f'"link": "{default}"')
            if p.parent.name == "textbook-src": s2 = s2.replace(f'"{old}"', f'"{default}"')
            if s2 != s: p.write_text(s2, encoding="utf-8"); hits.append(str(p.relative_to(ROOT)))
    return hits
