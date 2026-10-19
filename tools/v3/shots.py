#!/usr/bin/env python3
"""v3 screenshots + layout checks. Needs `python3 -m http.server 8803` in website-v3/.
WebKit iPhone 13 emulation and WebKit desktop 1280, light and dark.
Usage: shots.py [--full] [--only=psoriasis,...]   → website-v3/screenshots/"""
import json, sys, pathlib
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[2]
import os
OUT = pathlib.Path(os.environ.get("SHOTS_OUT", ROOT / "screenshots")); OUT.mkdir(parents=True, exist_ok=True)
BASE = os.environ.get("SHOTS_BASE", "http://127.0.0.1:8803/")
PAGES = {"psoriasis": "conditions/psoriasis.html", "viral-warts": "conditions/viral-warts.html",
         "bcc": "conditions/basal-cell-carcinoma.html", "bp": "conditions/bullous-pemphigoid.html",
         "acne": "conditions/acne-vulgaris.html", "eczema": "conditions/eczema-dermatitis.html",
         "module-inflammatory": "categories/inflammatory.html", "home": "index.html"}
only = [x for a in sys.argv if a.startswith("--only=") for x in a.split("=", 1)[1].split(",")]
full = "--full" in sys.argv
for x in only:  # any condition slug can be named directly
    if x not in PAGES and (ROOT / "conditions" / f"{x}.html").exists(): PAGES[x] = f"conditions/{x}.html"
CHECK = """() => {
  const de = document.documentElement, top = document.querySelector('.topbar').getBoundingClientRect().bottom;
  const wide = [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect();
     return r.width && (r.right > de.clientWidth + 1) && !e.closest('.strip,.toc-list,.table-wrap,.lightbox,.drawer,.search-results'); })
     .slice(0, 5).map(e => e.tagName + '.' + e.className);
  return {scrollY: window.scrollY, overflowX: de.scrollWidth - de.clientWidth, wide, headerBottom: top};
}"""
JUMP = """(id) => { const a = document.querySelector('[data-toc="'+id+'"]'); if (!a) return null;
  document.documentElement.style.scrollBehavior = 'auto'; a.click();
  return new Promise(r => setTimeout(() => { const h = document.getElementById(id).querySelector('h2') || document.getElementById(id);
    const bar = document.querySelector('.stepper'); const sb = bar && innerWidth < 1100 ? bar.getBoundingClientRect().bottom : 0;
    const tb = document.querySelector('.topbar').getBoundingClientRect().bottom;
    r({headingTop: Math.round(h.getBoundingClientRect().top), coveredUntil: Math.round(Math.max(sb, tb))}); }, 900)); }"""
report = {}
with sync_playwright() as p:
    wk = p.webkit.launch()
    iphone = p.devices["iPhone 13"]
    for scheme in ("light", "dark"):
        for dev, opts in (("iphone", dict(iphone)), ("desktop", {"viewport": {"width": 1280, "height": 860}, "device_scale_factor": 1})):
            ctx = wk.new_context(color_scheme=scheme, **opts)
            pg = ctx.new_page(); errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            for name, rel in PAGES.items():
                if only and name not in only: continue
                pg.goto(BASE + rel, wait_until="networkidle"); pg.wait_for_timeout(500)
                r = pg.evaluate(CHECK)
                pg.evaluate("Promise.all([...document.images].map(i=>{i.loading='eager'; return i.decode().catch(()=>{})}))")
                pg.wait_for_timeout(300)
                pg.screenshot(path=str(OUT / f"{name}-{dev}-{scheme}{'-full' if full else ''}.png"), full_page=full, scale=("css" if full else "device"))
                if rel.startswith("conditions/"):
                    r["jump"] = pg.evaluate(JUMP, "differentials")
                    pg.screenshot(path=str(OUT / f"{name}-{dev}-{scheme}-jump.png"))
                    pg.evaluate("window.scrollTo(0,0)")
                if "--steps" in sys.argv and rel.startswith("conditions/") and scheme == "light":
                    for sid in pg.evaluate("[...document.querySelectorAll('.step[id]')].map(s=>s.id)"):
                        pg.evaluate(JUMP, sid)
                        pg.screenshot(path=str(OUT / f"step-{name}-{dev}-{sid}.png"))
                report[f"{name}-{dev}-{scheme}"] = r
            if errs: report[f"jserr-{dev}-{scheme}"] = errs
            ctx.close()
    wk.close()
(OUT / "checks.json").write_text(json.dumps(report, indent=1))
for k, v in report.items(): print(k, v)
