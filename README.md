# Derm Teach: personal dermatology teaching library

A static, mobile-friendly website for primary-care dermatology, written for UK pharmacist independent prescribers.
Browse by **Category → Condition**. Every condition follows the same path:
What it is → How it's caused → Features → Diagnosis → Differentials → Management (UK pharmacist/IP) → Red flags → Pearls → Photos.

> Personal study resource. Always check the current BNF and NICE CKS. Clinical photos © DermNet (dermnetnz.org) and other credited holders; see `credits.html`.

---

## 1. Open it locally (no install needed)

**Option A: double-click**
Open `index.html` in Chrome, Edge, Firefox or Safari. Everything works from `file://`, including search, the lightbox and navigation. Nothing is fetched from the internet.

**Option B: simple local server** (nicer URLs; use this to view it on your phone over Wi-Fi)
```bash
cd /workspace/derm-teach/website
python3 -m http.server 8000
```
Then open <http://localhost:8000>. On a phone on the same network, use `http://<computer-ip>:8000`.

The site is fully static. To share or host it, copy the whole `website/` folder (e.g. to GitHub Pages or Netlify, or as a zip).

## 2. Rebuild after editing content

The HTML pages are **generated**. Edit the JSON in `content/`, then run:
```bash
cd /workspace/derm-teach/website
python3 build.py            # builds and prints any warnings
python3 build.py --strict   # fails if there are warnings (unknown photo codes, broken condition links)
```
Python 3 standard library only. No npm or pip.

## 3. Folder structure

```
website/
├── index.html, credits.html          ← generated
├── categories/*.html                 ← generated, one per category
├── conditions/*.html                 ← generated, one per condition
├── build.py                          ← the generator
├── content/
│   ├── site.json                     ← title, tagline, shared pearls & red flags
│   ├── categories.json               ← category list (order, icon, status)
│   ├── photo-sets.json               ← registry of photo folders + manifests
│   ├── manifests/*.json              ← photo captions/attribution (one per set)
│   └── conditions/*.json             ← ONE FILE PER CONDITION (_template.json is skipped)
└── assets/
    ├── css/style.css, js/app.js
    ├── js/search-index.js            ← generated search data
    └── img/
        ├── dermnet/                  ← core adult photos (set "core")
        ├── m5w1 m5w2 m5w3 m6w1 … m6w6/  ← per-week photo sets, each with ATTRIBUTION.md
        └── ai/                       ← AI teaching diagrams
```

## 4. Add a condition (quick version)

1. Copy `content/conditions/_template.json` to `content/conditions/<slug>.json`.
2. Set `slug`, `title`, `category` (an id from `categories.json`) and `summary`, then fill in the `sections`.
3. Add photos by code: `"A01"` (core set) or `"m6w4:W4C-03"` (other sets). The codes come from the image filenames.
4. Run `python3 build.py`. The page, category list, search and credits all update.

Full details, block types and examples are in **[ADD_CONDITION.md](ADD_CONDITION.md)**.

## 5. Current contents

| Category | Status | Pages |
|---|---|---|
| Inflammatory skin | full | Eczema/dermatitis, Psoriasis |
| Acne & follicles | full + stubs | Acne vulgaris · *stubs:* Acne mimics (rosacea/perioral/folliculitis), Acanthosis nigricans |
| Infections: fungal | full | Tinea, Pityriasis versicolor, Candida & intertrigo |
| Infections: bacterial | full | Impetigo (+MRSA), Cellulitis & erysipelas, Folliculitis, Boils & carbuncles |
| Infections: viral & infestations | full + stubs | Viral warts · *stubs:* Scabies, Head lice, Lyme disease, Blister beetle dermatitis, Papular urticaria |
| Ulcers & red leg | full | Venous leg ulcer, Pyoderma gangrenosum, Arterial & neuropathic ulcers, Red leg (cellulitis mimics) |
| Pigmentation | full + stubs | Progressive macular hypomelanosis · *stubs:* Melasma, Pigmented contact/lichenoid, Phytophotodermatitis & amyloid, Vitiligo/PIH in skin of colour |
| Childhood & neonatal | full | Neonatal rashes, Neonatal/infantile acne, Napkin dermatitis, Vascular birthmarks, Pigmented birthmarks, Epidermolysis bullosa, Aplasia cutis |
| Older skin | stubs | Itch & xerosis, Skin fragility, Actinic & seborrhoeic keratoses, Photoageing |
| Cosmetic & hair | full + stubs | Acne scars & keloids, Androgenetic alopecia, Cosmetic procedures · *stubs:* Facial ageing & botulinum toxin, Solar lentigines, IPL & eyelash |

**Stubs** (`"status": "coming-soon"`) are for weeks whose research packs are not written yet (Module 5 Week 3; Module 6 Weeks 2–5). Their photos are already filed and credited. To publish one, write its sections and change `status` to `"published"`.
