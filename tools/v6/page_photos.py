#!/usr/bin/env python3
"""Give pages that lacked real photos a card photo, a gallery group and clinical-features figures (v6 set)."""
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent)); import dn
def ind(p):
    l = p.read_text().split("\n")[1]; return len(l) - len(l.lstrip(" "))
ROOT = Path(__file__).resolve().parents[2]
P = {  # slug: [(spec, teaching point)]  first item becomes the card photo unless the page already has a real one
 "ingrowing-toenail": [("dn:ingrown-toenail:0", "Ingrowing toenail: the lateral nail edge digs into an inflamed, swollen nail fold."),
                       ("dn:ingrown-toenail:1", "Granulation tissue overgrowing the nail fold in a longstanding ingrowing toenail."),
                       ("dn:ingrown-toenail:2", "Ingrowing toenail with periungual inflammation of the big toe.")],
 "milia": [("dn:milium:1", "Periocular milia: tiny firm white keratin cysts around the eyes."),
           ("dn:milium:0", "Neonatal milia on the nose and cheeks; they clear without treatment."),
           ("dn:milium:5", "Secondary milia after blistering (here pemphigoid) — a clue to a past subepidermal blister.")],
 "addisons-disease": [("cm:File:WomenWithAddison.jpg", "Generalised tanned hyperpigmentation in Addison's disease (ACTH drives melanogenesis).")],
 "melanoma-immunotherapy": [("dn:cutaneous-adverse-effects-of-checkpoint-inhibitors:0", "Eczematous dermatitis induced by pembrolizumab (anti-PD-1)."),
                            ("dn:cutaneous-adverse-effects-of-checkpoint-inhibitors:1", "Lichenoid dermatitis induced by nivolumab."),
                            ("dn:cutaneous-adverse-effects-of-checkpoint-inhibitors:2", "Psoriasis triggered by pembrolizumab.")],
 "skin-surgery-preop": [("dn:excision-of-skin-lesions:0", "Elliptical excision wound before closure."),
                        ("dn:excision-of-skin-lesions:1", "The same wound after primary closure with sutures."),
                        ("dn:excision-of-skin-lesions:2", "Healed linear scar after elliptical excision.")],
 "teledermatology": [("dn:dermoscopy:0", "Dermoscopic skin examination — the image that travels with a teledermatology referral."),
                     ("dn:dermoscopy:1", "Clinical photography for a teledermatology referral: overview, close-up and dermoscopy.")],
 "perioral-dermatitis": [("dn:periorificial-dermatitis:0", "Perioral papules sparing the skin immediately next to the lips."),
                         ("dn:periorificial-dermatitis:7", "Florid perioral dermatitis after potent topical steroid use on the face.")],
 "blue-naevus": [("dn:blue-naevus:0", "Blue naevus: a small, uniform slate-blue papule."),
                 ("dn:blue-naevus:2", "Blue naevus on the hand.")],
 "dress": [("dn:drug-hypersensitivity-syndrome:0", "Widespread morbilliform eruption of DRESS — check for fever, facial oedema, nodes, eosinophils and liver function.")],
 "lipoma": [("dn:lipoma:0", "Soft, mobile subcutaneous lipoma on the shoulder.")],
 "ace-inhibitor-angioedema": [("dn:angioedema:0", "Severe lip angioedema without wheals — typical of ACE-inhibitor (bradykinin) angioedema.")],
 "emollients": [("dn:emollients-and-moisturisers:1", "Emollients range from light lotions to very greasy ointments — the right one is the one the patient will use.")],
}
EXAM = {"exam-module-2": "m2w3:A03", "exam-module-4": "m4w1:G01", "exam-module-5": "m5w1:N01"}
def code(spec, slug, tp):
    if spec.startswith("dn:"):
        _, t, i = spec.split(":"); return "v6:" + dn.get(t, i, slug, tp)
    if spec.startswith("cm:"): return "v6:" + dn.commons(spec[3:], slug, tp)
    return spec
added = 0
for slug, items in P.items():
    cp = ROOT / "content/conditions" / f"{slug}.json"; d = json.loads(cp.read_text())
    codes = [(code(s, slug, tp), tp) for s, tp in items]
    have = {i if isinstance(i, str) else i.get("dermnet") for g in d.get("photos", []) for i in g.get("items", [])}
    new = [c for c, _ in codes if c not in have]
    if new:
        d.setdefault("photos", []).insert(0, {"title": "Clinical photographs", "items": new}); added += len(new)
    if not d.get("card_image"): d["card_image"] = codes[0][0]
    cp.write_text(json.dumps(d, ensure_ascii=False, indent=ind(cp)) + "\n")
    sp = ROOT / "content/textbook-src" / f"{slug}.json"
    if sp.exists():
        e = json.loads(sp.read_text()); e["cf_figs"] = [{"dermnet": c, "caption": tp} for c, tp in codes]
        sp.write_text(json.dumps(e, ensure_ascii=False, indent=1))
        subprocess.run([sys.executable, str(ROOT / "tools/v4/convert.py"), slug], check=True, capture_output=True)
    else:
        print("no textbook-src:", slug)
for slug, c in EXAM.items():
    cp = ROOT / "content/conditions" / f"{slug}.json"; d = json.loads(cp.read_text())
    d["card_image"] = c; cp.write_text(json.dumps(d, ensure_ascii=False, indent=ind(cp)) + "\n")
print("photos added to galleries:", added)
