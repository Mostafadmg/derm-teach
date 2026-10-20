#!/usr/bin/env python3
"""DermNet helper. `dn.py list <topic>...` lists gallery images; `dn.py get <topic> <idx> <condition-slug> "<teaching point>"`
downloads one into assets/img/v6 and appends it to content/manifests/v6.json (code V6-nnn). Prints the code."""
import html, json, re, sys, urllib.request, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
MAN = ROOT / "content/manifests/v6.json"
UA = {"User-Agent": "Mozilla/5.0 (derm-teach personal study notes)"}
_cache = {}
def _next(man):
    return max([int(Path(m["filename"]).name[1:4]) for m in man] or [0]) + 1
def topic(t):
    if t in _cache: return _cache[t]
    req = urllib.request.Request(f"https://dermnetnz.org/topics/{t}", headers=UA)
    try: h = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    except Exception as e: _cache[t] = None; return None
    out, seen = [], set()
    for tag in re.findall(r'<img[^>]+js-gallery-image[^>]*>', h):
        a = dict((k, html.unescape(v)) for k, v in re.findall(r'([\w-]+)="([^"]*)"', tag))
        if a.get("src") in seen: continue
        seen.add(a["src"]); out.append(a)
    _cache[t] = out; return out
def get(t, idx, cond, tp):
    imgs = topic(t); a = imgs[int(idx)]
    man = json.loads(MAN.read_text()) if MAN.exists() else []
    url = "https://dermnetnz.org" + a["src"]
    for m in man:
        if m["direct_image_url"] == url: return Path(m["filename"]).name.split("_")[0]
    code = f"V{_next(man):03d}"
    fn = f"{cond}/{code}_{Path(a['src']).name}"
    dest = ROOT / "assets/img/v6" / fn; dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
    cap = a.get("data-headline") or a.get("alt") or t.replace("-", " ").capitalize()
    cr = a.get("data-copyright") or "© DermNet"
    page = f"https://dermnetnz.org/topics/{t}"
    man.append({"filename": fn, "condition": cond, "section": cond, "teaching_point": tp or cap, "dermnet_caption": cap,
                "source_site": "DermNet (dermnetnz.org)", "source_page_url": page, "direct_image_url": url, "copyright": cr,
                "width": int(a.get("width", 640)), "height": int(a.get("height", 480)), "bytes": dest.stat().st_size,
                "licence_note": "DermNet image licence: https://dermnetnz.org/image-licence (watermarked low-res; personal/educational use with attribution)",
                "attribution": f"Image: DermNet — {cap} ({cr}) — {page}"})
    MAN.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
    return code

def commons(title, cond, tp, cap=None):
    """Download a Wikimedia Commons file (≤800px) with licence + author into the v6 set."""
    import urllib.parse
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": title, "prop": "imageinfo",
                                "iiprop": "url|extmetadata|size", "iiurlwidth": 800})
    d = json.loads(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers=UA), timeout=30).read())
    p = next(iter(d["query"]["pages"].values())); ii = p["imageinfo"][0]; m = ii["extmetadata"]
    g = lambda k: re.sub(r"\s+", " ", re.sub("<[^>]+>", "", html.unescape(m.get(k, {}).get("value", "")))).strip()
    lic, artist = g("LicenseShortName"), g("Artist") or "Unknown author"
    url = ii.get("thumburl") or ii["url"]
    man = json.loads(MAN.read_text()) if MAN.exists() else []
    for x in man:
        if x["direct_image_url"] == url: return Path(x["filename"]).name.split("_")[0]
    code = f"V{_next(man):03d}"
    ext = Path(urllib.parse.urlparse(url).path).suffix.lower() or ".jpg"
    fn = f"{cond}/{code}_commons{ext}"
    dest = ROOT / "assets/img/v6" / fn; dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())
    cap = cap or title[5:].rsplit(".", 1)[0]
    cr = f"{artist} · {lic}"
    man.append({"filename": fn, "condition": cond, "section": cond, "teaching_point": tp, "source_caption": cap,
                "source_site": "Wikimedia Commons", "source_page_url": ii["descriptionurl"], "direct_image_url": url,
                "copyright": cr, "width": ii.get("thumbwidth", ii["width"]), "height": ii.get("thumbheight", ii["height"]),
                "bytes": dest.stat().st_size, "licence_note": f"{lic} — {g('LicenseUrl') or ii['descriptionurl']}",
                "attribution": f"Image: {cap} — {cr} — via Wikimedia Commons ({ii['descriptionurl']})"})
    MAN.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n")
    return code

if __name__ == "__main__":
    if sys.argv[1] == "list":
        for t in sys.argv[2:]:
            imgs = topic(t)
            print(f"== {t}: " + ("404" if imgs is None else str(len(imgs))))
            for i, a in enumerate(imgs or []): print(f"  {i:2d} {a.get('data-headline') or a.get('alt')} | {a.get('data-copyright','')} | {a['src'].split('/')[-1]}")
    elif sys.argv[1] == "commons":
        print("v6:" + commons(*sys.argv[2:]))
    else:
        print("v6:" + get(*sys.argv[2:6]))
