"""Fetch DermNet + Medscape background for a condition and save a condensed research note.
Usage: python3 tools/v4/research.py slug [slug...]   -> /workspace/cur/research/<slug>.md
Optional overrides in tools/v4/research_map.json: {"slug": {"dermnet": "topic-path", "medscape": "1234567"}}"""
import json, re, sys, html, subprocess, pathlib, difflib
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path("/workspace/cur/research"); OUT.mkdir(parents=True, exist_ok=True)
UA = "Mozilla/5.0"
MAP = json.loads((ROOT / "tools/v4/research_map.json").read_text()) if (ROOT / "tools/v4/research_map.json").exists() else {}

def get(url):
    r = subprocess.run(["curl", "-sL", "-m", "25", "-A", UA, "-w", "\n%{http_code}", url], capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    return body if code.strip() == "200" else ""

def text(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S)
    s = re.sub(r"<li[^>]*>", "\n- ", s); s = re.sub(r"<(p|br|tr|h\d)[^>]*>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", s)).strip()

def ms_index():
    idx = {}
    for f in OUT.glob("ms-*.html"):
        for u, t in re.findall(r'href="(?:https?:)?//emedicine\.medscape\.com/article/(\d+)-overview"[^>]*>([^<]+)</a>', f.read_text(errors="ignore")):
            idx[html.unescape(t).strip().lower()] = u
    return idx

def sections(h, tag, want, cap):
    parts = re.split(rf"(<{tag}[^>]*>.*?</{tag}>)", h, flags=re.S)
    out = []
    for i in range(1, len(parts) - 1, 2):
        t = text(parts[i])
        if any(w in t.lower() for w in want):
            body = text(parts[i + 1])
            body = re.split(r"\n\s*(Previous|References|Next|ADVERTISEMENT|Bibliography)\s*\n", body)[0]
            body = re.sub(r"\s*\[\s*[\d ,–-]+\]", "", body)[:cap]
            out.append(f"### {t}\n{body}")
    return out

def run(slug):
    d = json.loads((ROOT / f"content/conditions/{slug}.json").read_text())
    m = MAP.get(slug, {})
    notes = [f"# {d['title']}  ({slug})"]
    dn = m.get("dermnet")
    if not dn:
        for r in d.get("references", []):
            u = r["url"] if isinstance(r, dict) else ""
            if "dermnetnz.org/topics/" in u: dn = u.split("/topics/")[1].strip("/"); break
    dn = dn or slug
    h = get(f"https://dermnetnz.org/topics/{dn}")
    if h:
        notes.append(f"DermNet: https://dermnetnz.org/topics/{dn}")
        notes += sections(h, "h2", ["who gets", "what causes", "complication", "outcome", "prognosis", "histolog", "patholog"], 900)
    else:
        notes.append(f"DermNet: not found ({dn})")
    ms = m.get("medscape")
    if not ms:
        idx = ms_index(); keys = [d["title"].lower()] + [a.lower() for a in d.get("aka", [])[:4]]
        for k in keys:
            k = re.sub(r"\(.*?\)|:.*", "", k).strip()
            best = difflib.get_close_matches(k, idx.keys(), n=1, cutoff=0.82)
            if best: ms = idx[best[0]]; notes.append(f"(medscape match: {best[0]})"); break
    if ms and ms != "none":
        h = get(f"https://emedicine.medscape.com/article/{ms}-overview")
        if h:
            notes.append(f"Medscape: https://emedicine.medscape.com/article/{ms}-overview")
            notes += sections(h, "h2", ["epidemiology", "pathophysiology", "etiology", "prognosis"], 1000)
    (OUT / f"{slug}.md").write_text("\n".join(notes))
    print(slug, len("\n".join(notes)), "dn" if "DermNet: http" in notes[1] else "-", "ms" if ms else "-")

if __name__ == "__main__":
    for s in sys.argv[1:]:
        try: run(s)
        except Exception as e: print(s, "ERR", e)
