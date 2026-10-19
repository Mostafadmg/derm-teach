"""Helper for researched enrichment files: content/textbook-src/<slug>.json, merged by tools/v4/convert.py."""
import json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
SLUGS = {p.stem for p in (ROOT / "content/conditions").glob("*.json")}
AI = {p.name for p in (ROOT / "assets/img/ai").glob("*.jpg")}
def M(k, t, img=None, cap=""):
    if img: assert img in AI, img
    return {"k": k, "t": t, **({"img": img, "cap": cap} if img else {})}
def DD(name, f, link=None, photo=None):
    d = {"name": name.lstrip("!"), "f": f}
    if name.startswith("!"): d["danger"] = True
    if link: assert link in SLUGS, link; d["link"] = link
    if photo: d["photo"] = photo
    return d
def E(slug, **kw):
    assert slug in SLUGS, slug
    for s in kw.get("see_also", []): assert s in SLUGS, s
    if "mech" in kw: kw["mech"] = [m if isinstance(m, dict) else M(*m) for m in kw["mech"]]
    if "refs" in kw: kw["refs"] = [list(r) for r in kw["refs"]]
    if "quiz" in kw: kw["quiz"] = [dict(q=q, a=a) for q, a in kw["quiz"]]
    (ROOT / "content/textbook-src" / f"{slug}.json").write_text(json.dumps(kw, ensure_ascii=False, indent=1), encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "tools/v4/convert.py"), slug], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip()[-400:])
def IMG(slug, idx, img, cap):
    """attach an AI image to mechanism step idx (0-based) of an existing enrichment file"""
    assert img in AI, img
    p = ROOT / "content/textbook-src" / f"{slug}.json"; d = json.loads(p.read_text())
    d["mech"][idx].update(img=img, cap=cap); p.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    r = subprocess.run([sys.executable, str(ROOT / "tools/v4/convert.py"), slug], capture_output=True, text=True); print(r.stdout.strip())
