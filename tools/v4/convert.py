"""Derm Teach v4: generate a textbook page (content/textbook/<slug>.json) from
   content/conditions/<slug>.json (full notes) + content/steps/<slug>.json (structured visuals, drugs, ladder, quiz)
   + content/textbook-src/<slug>.json (researched enrichment: epidemiology, mechanism steps, histology, complications ...).
Authored pages (textbook JSON with "_authored": true) are never overwritten.
Usage: python3 tools/v4/convert.py slug [slug ...] | --all"""
import json, re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
C, ST, TB, SRC = (ROOT / "content" / x for x in ("conditions", "steps", "textbook", "textbook-src"))
RESEARCH = pathlib.Path("/workspace/cur/research")
PATHO = re.compile(r"how it is caused|patho|mechanism|how it works|why it happens|four linked", re.I)
REDF = re.compile(r"^red flags?\b|red flags? / refer|when to refer|^refer", re.I)
EPI = re.compile(r"epidemiolog|who gets|prevalence", re.I)


def load(p):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def blk(b):
    if isinstance(b, str):
        return b
    k = next(iter(b))
    if k == "list": return {"ul": b["list"]}
    if k == "ol": return {"ol": b["ol"]}
    if k == "h": return {"h": b["h"]} if b["h"].strip() else None
    if k == "table": return {"table": b["table"]}
    if k == "callout": return b
    if k == "figure":
        f = b["figure"]; f = dict(f, dermnet=f["photo"]) if "photo" in f else f
        return {"fig": {x: y for x, y in f.items() if x != "photo"}}
    if k == "figures":
        return {"figs": [({"dermnet": x["photo"], **({"caption": x["caption"]} if x.get("caption") else {})} if "photo" in x else x) for x in b["figures"]]}
    return b


def segs(blocks):
    """split into [(heading, [blocks])], heading None for the lead segment"""
    out = [[None, []]]
    for b in blocks:
        if isinstance(b, dict) and "h" in b:
            out.append([b["h"], []])
        else:
            out[-1][1].append(b)
    return [(h, bl) for h, bl in out if h or bl]


def emit(sg, demote=False):
    out = []
    for h, bl in sg:
        if h:
            out.append({"h4": h} if demote else {"h": h})
        out += [x for x in (blk(b) for b in bl) if x]
    return out


def photo_of(x):
    return x.get("photo") or (x.get("ai") and {"ai": x["ai"]})


def figs_from(visuals):
    return [{"ai": v["ai"], "caption": v.get("caption", ""), "alt": v.get("alt", v.get("caption", ""))} for v in visuals or [] if v.get("ai")]


def strip_auto_lead(t):
    return re.sub(r"^\*\*[^*]{1,30}:\*\*\s*", "", t)


def convert(slug, force=False):
    tbp = TB / f"{slug}.json"
    old = load(tbp)
    if old and old.get("_authored") and not force:
        return "authored (kept)"
    d = load(C / f"{slug}.json")
    st = load(ST / f"{slug}.json") or load(ST / "_auto" / f"{slug}.json") or {}
    E = load(SRC / f"{slug}.json") or {}
    S = d.get("sections", {})
    secs = {}

    def add(sid, *blocks):
        secs.setdefault(sid, []).extend(b for b in blocks if b)

    # 1 overview
    add("overview", *E.get("overview_pre", []))
    add("overview", *emit(segs(S.get("what", [])), demote=True))
    add("overview", *E.get("overview", []))
    # 2 epidemiology
    epi = E.get("epi", [])
    if epi:
        add("epidemiology", {"ul": epi})
    # 3 aetiology  +  4 pathophysiology
    cause_patho, cause_rest = [], []
    for h, bl in segs(S.get("cause", [])):
        (cause_patho if h and PATHO.search(h) else cause_rest).append((h, bl))
    if E.get("aet_lead"): add("aetiology", E["aet_lead"])
    add("aetiology", *emit(cause_rest))
    if E.get("aet"): add("aetiology", {"h": "Risk factors and associations"}, {"ul": E["aet"]})
    if E.get("myths"): add("aetiology", {"h": "Myths to address"}, {"ul": E["myths"]})
    cv = figs_from((st.get("cause") or {}).get("visuals"))
    used_ai = set()
    if E.get("mech"):
        steps = []
        for m in E["mech"]:
            s = {"k": m["k"], "t": m["t"]}
            if m.get("img"):
                s["img"] = m["img"]; s["caption"] = m.get("cap", ""); used_ai.add(m["img"])
            steps.append(s)
        if E.get("patho_lead"): add("pathophysiology", E["patho_lead"])
        add("pathophysiology", {"mech": steps})
    add("pathophysiology", *emit(cause_patho))
    rest_cv = [v for v in cv if v["ai"] not in used_ai]
    if rest_cv:
        add("pathophysiology" if (E.get("mech") or cause_patho) else "aetiology",
            {"fig": rest_cv[0]} if len(rest_cv) == 1 else {"figs": rest_cv})
    if E.get("histo"): add("pathophysiology", {"histo": E["histo"]})
    # 5 clinical features
    fe = st.get("features") or {}
    add("clinical-features", *E.get("cf_pre", []))
    add("clinical-features", *emit(segs(S.get("features", []))))
    if fe.get("photo") and not E.get("no_feature_photo"):
        add("clinical-features", {"fig": {"dermnet": fe["photo"]}})
    if E.get("lesions"): add("clinical-features", {"h": "Lesions and morphology"}, {"lesions": E["lesions"]})
    fv = [v for v in figs_from(fe.get("visuals")) if v["ai"] not in used_ai]
    maps = [v for v in fv if "map" in v["ai"] or "distribution" in v["ai"] or "sites" in v["ai"]]
    for v in maps:
        add("clinical-features", {"h": "Distribution"}, {"bodymap": {"img": {"ai": v["ai"]}, "caption": v["caption"], "pts": E.get("dist", [])}})
    if not maps and E.get("dist"):
        add("clinical-features", {"h": "Distribution"}, {"ul": E["dist"]})
    other = [v for v in fv if v not in maps]
    if other: add("clinical-features", {"fig": other[0]} if len(other) == 1 else {"figs": other})
    var = (fe.get("variants") or {}).get("items") or []
    if var:
        add("clinical-features", {"h": (fe.get("variants") or {}).get("title") or "Variants and subtypes"},
            {"variants": [{"name": v["name"], "t": v.get("t", "") + (f" *Site: {v['where']}.*" if v.get("where") else ""),
                           **({"photo": v["photo"]} if v.get("photo") else {}), **({"danger": True} if v.get("tone") == "danger" else {})} for v in var]})
    if E.get("special"): add("clinical-features", {"h": "Special groups"}, {"ul": E["special"]})
    # 6 diagnosis
    add("diagnosis", *emit(segs(S.get("diagnosis", []))))
    cf = st.get("confirm") or {}
    if len(json.dumps(S.get("diagnosis", []))) < 400 and cf.get("cols"):
        for col in cf["cols"]:
            add("diagnosis", {"h4": col["k"]}, {"ul": col.get("points", [])})
    if cf.get("visuals"): add("diagnosis", {"figs": figs_from(cf["visuals"])})
    if E.get("dx"): add("diagnosis", *E["dx"])
    # 7 differentials
    dd = st.get("differentials") or {}
    rows = [{"name": c["name"], "f": c.get("clue", ""), **({"link": c["link"]} if c.get("link") else {}),
             **({"photo": c["photo"]} if c.get("photo") else {}), **({"danger": True} if c.get("tone") == "danger" else {})}
            for c in dd.get("cards", [])]
    rows += E.get("ddx_add", [])
    if rows: add("differentials", {"ddx": rows})
    if dd.get("more"): add("differentials", dd["more"])
    dsg = segs(S.get("differentials", []))
    keep = []
    for h, bl in dsg:
        bl2 = [b for b in bl if not (rows and isinstance(b, dict) and "table" in b and len(rows) >= 4)]
        if bl2 or (h and not rows): keep.append((h, bl2))
    add("differentials", *emit(keep, demote=True))
    # 8 management
    man_rf, man = [], []
    for h, bl in segs(S.get("management", [])):
        (man_rf if h and REDF.search(h) else man).append((h, bl))
    add("management", *E.get("mx_pre", []))
    add("management", *emit(man))
    mg = st.get("manage") or {}
    if mg.get("visuals"): add("management", {"figs": figs_from(mg["visuals"])} if len(mg["visuals"]) > 1 else {"fig": figs_from(mg["visuals"])[0]})
    drugs = []
    for r in mg.get("rungs", []):
        for rx in r.get("rx", []) or []:
            dz = " · ".join(x for x in (rx.get("dose"), rx.get("dur")) if x)
            drugs.append({"name": rx["drug"], "cls": r["k"], **({"dose": dz} if dz else {}), **({"cautions": rx["note"]} if rx.get("note") else {}),
                          **({"specialist": True} if r.get("tone") == "refer" or "specialist" in r["k"].lower() else {})})
    drugs += E.get("drugs", [])
    if drugs: add("management", {"h": "Medicines at a glance"}, {"drugs": drugs})
    if mg.get("sites"): add("management", {"h": "By site or situation"}, {"ul": [f"**{s['k']}**: {s['t']}" for s in mg["sites"]]})
    if mg.get("rungs"):
        lad = []
        for r in mg["rungs"]:
            t = "; ".join(rx["drug"] for rx in r.get("rx") or []) or " ".join(strip_auto_lead(p) for p in (r.get("points") or [])[:2])
            lad.append({"k": r["k"], "t": t, "tone": r.get("tone", "base")})
        add("management", {"h": "Treatment ladder"}, {"ladder": lad})
    if mg.get("limits"):
        add("management", {"callout": "warn", "title": "Prescribing limits and pitfalls", "list": [f"**{x['k']}**: {x['t']}" for x in mg["limits"]]})
    ref = (st.get("refer") or {}).get("items") or []
    if ref: add("management", {"h": "Referral"}, {"refer": [{"when": x.get("when", "routine"), "t": x["t"]} for x in ref]})
    # 9 red flags
    rf = [b for b in S.get("red_flags", [])]
    if rf: add("red-flags", {"ul": [b for b in rf if isinstance(b, str)]}, *[blk(b) for b in rf if not isinstance(b, str)])
    add("red-flags", *emit(man_rf, demote=True))
    # 10 complications
    if E.get("comp"): add("complications", {"h": "Complications"}, {"ul": E["comp"]})
    if E.get("prog"): add("complications", {"h": "Prognosis"}, {"ul": E["prog"]})
    # 11 pearls
    pe = S.get("pearls", [])
    pstr = [b for b in pe if isinstance(b, str)]
    if pstr: add("pearls", {"pearls": pstr})
    add("pearls", *emit(segs([b for b in pe if not isinstance(b, str)])))
    if E.get("pearls"): add("pearls", {"pearls": E["pearls"]})

    TITLES = {"overview": "Overview", "epidemiology": "Epidemiology", "aetiology": ("Aetiology: causes and risk factors", "Aetiology"),
              "pathophysiology": ("Pathophysiology and pathology", "Pathophysiology"), "clinical-features": "Clinical features",
              "diagnosis": ("Diagnosis and investigations", "Diagnosis"), "differentials": ("Differential diagnoses", "Differentials"),
              "management": "Management", "red-flags": ("Red flags and when to refer", "Red flags"),
              "complications": ("Complications and prognosis", "Complications"), "pearls": ("Prescriber pearls (UK pharmacist IP)", "Pearls")}
    TITLES.update({k: tuple(v) if isinstance(v, list) else v for k, v in (E.get("titles") or {}).items()})
    out = []
    for sid in ["overview", "epidemiology", "aetiology", "pathophysiology", "clinical-features", "diagnosis", "differentials",
                "management", "red-flags", "complications", "pearls"]:
        if secs.get(sid):
            t = TITLES[sid]
            s = {"id": sid, "title": t if isinstance(t, str) else t[0], "blocks": secs[sid]}
            if not isinstance(t, str): s["short"] = t[1]
            out.append(s)
    kf = E.get("kf") or [p["t"] for p in (st.get("glance") or {}).get("points", [])]
    quiz = E.get("quiz") or st.get("quiz") or []
    refs = [dict(label=l, url=u) for l, u in E.get("refs", [])]
    note = RESEARCH / f"{slug}.md"
    if note.exists():
        nt = note.read_text()
        for lbl, rx in (("DermNet", r"^DermNet: (https://\S+)"), ("Medscape", r"^Medscape: (https://\S+)")):
            m = re.search(rx, nt, re.M)
            if m and m.group(1) not in {r["url"] for r in refs} and m.group(1) not in json.dumps(d.get("references", [])):
                refs.append({"label": f"{lbl}: {E.get('ref_title') or d['title']}", "url": m.group(1)})
    tb = {"_generated": "tools/v4/convert.py (edit content/textbook-src/<slug>.json or the condition JSON, then re-run)",
          "key_facts": kf, "sections": out, "quiz": quiz, "references": refs, "see_also": E.get("see_also", [])}
    tbp.write_text(json.dumps(tb, ensure_ascii=False, indent=1), encoding="utf-8")
    return f"{len(out)} sections, {len(json.dumps(tb))} B" + ("" if E else " (NO enrichment)")


if __name__ == "__main__":
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    if args == ["--all"]:
        args = sorted(p.stem for p in C.glob("*.json") if not p.stem.startswith("_") and not p.stem.startswith("exam-"))
    for s in args:
        print(s, convert(s, force))
