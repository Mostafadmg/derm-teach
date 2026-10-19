# Derm Teach v3 – "lesson" layout: pilot and rollout

The pilot lives in `/workspace/derm-teach/website-v3/`, a copy of `website/`. Nothing in `website/` or `build/site_fold/` was touched, and nothing was committed or pushed.
To build it: `python3 build.py --strict`. To preview it: `python3 -m http.server 8803 --bind 127.0.0.1`.

## 1. What changed

| Piece | File | Role |
|---|---|---|
| Transformer | `tools/v3/to_steps.py` | Turns the condition JSON into 9 lesson steps (`derive`) and merges an optional curated overlay (`steps_for`). It changes no content JSON. CLI: `--report` shows curated vs auto; no argument writes `content/steps/_auto/<slug>.json` drafts. |
| Curated overlays | `content/steps/<slug>.json` | Condensed, visual-first text plus image placement for the 6 pilot pages: psoriasis, eczema-dermatitis, acne-vulgaris, basal-cell-carcinoma, bullous-pemphigoid, viral-warts. |
| Build | `build.py` | Adds a new `build_condition` (lesson layout) and `build_category` (module list). The old renderers are kept as `build_condition_v2` / `build_category_v2`; `layout: "article"` pages still use v2. Conditions now build before categories. Font preload and `v3.css` are linked. Source-badge and thumb-credit overlays are removed. In `--strict` mode the build warns if any photo in `d["photos"]` is missing from the page. |
| Styles | `assets/css/v3.css` | Loaded after `style.css`, so `style.css` is unchanged. Covers fonts, spacing scale, stepper, overview panel, filmstrips, ladder, flow, quiz, module list, dark mode and print. |
| Behaviour | `assets/js/app.js` (block appended at the end) | Progress in `localStorage["dt-progress-v1"]`, "Step x of n", Next-step buttons, step ticks, mobile sticky step bar, `--stepbar`, module progress, Reset. |
| Fonts | `assets/fonts/*.woff2` | Plus Jakarta Sans (UI and headings) and Source Sans 3 (body), self-hosted, OFL. |
| AI images | `assets/img/ai/v3-*.jpg` (originals in `tools/v3/ai-src/`) | `tools/v3/import_ai.py <src> <name>` trims white space, pads and saves as jpg q86. |
| QA | `tools/v3/shots.py` | WebKit iPhone 13 and desktop 1280, light and dark. Checks start-scroll, horizontal overflow, header overlap after a step jump, and JS errors. Options: `--steps` (per-step shots), `--full` (full page), `--only=`. Writes `screenshots/checks.json`. |

### How no content is lost
- Every step ends with a collapsed **More detail** block. It renders the original JSON sections word for word and keeps their old anchor ids.
- The condensed text sits on top of the original; nothing is replaced.
- Photos are placed in the step their group belongs to.
- All photos also appear in a collapsed **Full photo gallery** at the end.
- The strict build warns about any photo that ends up nowhere.

## 2. Plugging into build/site_fold (so reruns keep it)

`site_fold` (gen.py → enrich.py → exam.py → fixurls.py) writes only to `website/content/conditions/*.json`. v3 is purely presentation plus an overlay in a separate folder, so a fold rerun cannot overwrite it.

1. Once the other agent has finished and pushed, diff `website/build.py` against the pilot copy (it has changed since the copy was taken). Re-apply the v3 hunks: the `V3` import block, the new `build_condition` / `build_category`, the reordered `main()`, the extra `<link>`/preload tags in `page()`, and the overlay removal in `figure()` / `thumb_for()`. The simplest way is to paste the v3 block above `build_credits()` and rename the two old functions.
2. Copy these files as they are:
   - `tools/v3/`
   - `assets/css/v3.css`
   - `assets/fonts/`
   - `assets/img/ai/v3-*`
   - `content/steps/*.json` (not `_auto/`)
   - the v3 block at the end of `assets/js/app.js`
3. Add a step after `fixurls.py`: `python3 website/tools/v3/to_steps.py --report`. It lists pages that are still auto-only and flags overlays whose referenced photo codes no longer exist.
4. `python3 build.py --strict`, then `python3 tools/v3/shots.py` (it must report overflowX 0 and scrollY 0 for every page).
5. Curation loop for each page: copy `content/steps/_auto/<slug>.json` to `content/steps/<slug>.json`. Shorten the bullets to 1 line each (bold the key term) and place photos and AI images. Then get a clinical review and rebuild. Doses must be copied from the source JSON only.

All 146 pages already render in the v3 layout using auto-derived steps. Curation improves the wording and image placement; it is not needed for the page to work.

## 3. AI illustration plan

House style, used for every prompt:
- flat medical illustration on a pure white background, soft teal/coral palette;
- no text or labels, no photoreal patients;
- labels, arrows, flowcharts and ladders are done in HTML/SVG, never baked into the image.

Every image is read and checked before it is used.
Captions say "AI-generated illustration".

Image types:
- **A** skin cross-section (pathophysiology, for "Why it happens");
- **B** body or face distribution map (for "What you'll see");
- **C** morphology schematic or "this vs that" split (for features and lookalikes);
- **D** mechanism or technique (e.g. emollient fingertip unit, cryotherapy, punch biopsy, dressings).

| Category (conditions) | Types | Est. images |
|---|---|---|
| Lumps, lesions & cancer (22) | A (tumour depth), B (sun-exposed sites), C (ABCDE, BCC/SCC/SK lookalikes) | 55 |
| Viral & infestations (10) | A, B, C (burrow, vesicle clusters, dermatome) | 25 |
| Inflammatory (9) | A, B, C | 24 |
| Vasculitis (8) | A (vessel wall), B, C (palpable purpura vs petechiae) | 18 |
| Childhood & neonatal (7) | B (infant maps), C | 16 |
| Drug eruptions (7) | A, B, D (timeline graphic is HTML) | 15 |
| Systemic disease (7) | B, C | 14 |
| Therapeutics (7) | D (FTU, application, wet wraps, steroid ladder art) | 14 |
| Bacterial (6) / Tropical (6) | A, B, C | 26 |
| Pigmentation, cosmetic-hair, hair-scalp, hands-feet-folds, blistering, skin-surgery (5 each) | A, B, C/D (follicle, nail unit, blister level, excision ellipse) | 70 |
| Acne, ulcers/red leg, older skin, nails, photodermatoses (4 each) | A, B, C | 45 |
| Fungal (3), exam-review (3), foundations (2) | A/C (skin layers, lesion morphology glossary) | 15 |
| **Total** | about 2–3 per condition | **≈ 335–360** (pilot so far: 13) |

Some images can be reused across pages (normal skin layers, blister levels, hair follicle, nail unit, face zones), which brings the number of unique images down by about 15%.

Expected regeneration rate: about 15%. In the pilot, 2 of 15 drafts had anatomically wrong distributions:
- psoriasis map with front-view elbows;
- eczema map with front knees instead of the popliteal fossae.

Body maps need the most checking.

Effort:
- about 20–30 min per condition for overlay curation plus images plus review;
- about 50–70 h for all 140 remaining pages;
- doing the top 40 high-yield conditions first is about 15–20 h.

## 4. Caveats
- The overlays are hand-condensed from the existing JSON and need a clinical sign-off. Doses and durations appear only where the source content states them.
- Progress is stored on the device (localStorage) and is not synced. A step counts as done after about 4 s in view plus scrolling past it, or when you tap Next.
- Auto-mode pages are readable but wordier, since bullets are clipped source sentences; curation fixes this.
- The pilot copy of content JSON is a snapshot. Rebase on the latest `website/content` before rollout.
- AI illustrations are schematic and are not suitable as diagnostic images. DermNet photos remain the clinical reference, with a credit and Source link under each image and no overlays.
