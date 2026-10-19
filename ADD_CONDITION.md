# How to add (or update) a condition: v4 textbook format

Every condition page is built from up to four files. Run `python3 build.py --strict` after any change.

| File | What it holds | Who edits it |
|---|---|---|
| `content/conditions/<slug>.json` | Metadata (title, aka, category, order, module, summary, card_image), the **course notes** in `sections`, `photos` (gallery) and `references`. Schema: `content/conditions/_template.json`. | You |
| `content/steps/<slug>.json` | Structured extras: variant cards with photos, differential cards, drug rungs (`manage.rungs[].rx`), referral items, quiz, AI visuals. Optional. | You (optional) |
| `content/textbook-src/<slug>.json` | **Researched enrichment** (DermNet, Medscape, NICE CKS, BNF): `kf` key facts, `epi`, `aet`, `myths`, `mech` (numbered mechanism steps, each with an optional AI image), `histo`, `lesions`, `dist`, `special`, `ddx_add`, `drugs`, `comp`, `prog`, `pearls`, `refs`, `see_also`, `quiz`. | You (via `tools/v4/authoring/enr.py`) |
| `content/textbook/<slug>.json` | The **page itself** (13-section textbook layout). Normally **generated** by `tools/v4/convert.py` from the three files above. Hand-written pages carry `"_authored": true` and are never overwritten. | Generated, or hand-authored with `tools/v4/authoring/tbw.py` |

## Section order (fixed)
Overview · Epidemiology · Aetiology (causes, risk factors, myths) · Pathophysiology (numbered steps with AI images, histopathology) · Clinical features (symptoms, lesions with photos, distribution/body map, variants, special groups) · Diagnosis and investigations · Differential diagnoses (table with thumbnails) · Management (principles, conservative, drug cards, treatment ladder, referral) · Red flags · Complications and prognosis · Prescriber pearls · Self-check quiz (collapsed) · References · Photo gallery (collapsed).

## Steps for a new condition
1. Copy `content/conditions/_template.json` to `content/conditions/<slug>.json`; fill metadata, course notes and photos.
2. Research: `python3 tools/v4/research.py <slug>` saves a condensed DermNet + Medscape note to `/workspace/cur/research/<slug>.md` (override URLs in `tools/v4/research_map.json`).
3. Write the enrichment with the helper (UK framing: NICE CKS and BNF; keep the course-vs-UK corrections; **doses only as stated in the source notes or BNF**):
   ```python
   import sys; sys.path.insert(0, 'tools/v4/authoring'); from enr import *
   E('<slug>', kf=[...], epi=[...], aet=[...], myths=[...],
     mech=[("Step title", "What happens", "v4-xyz.jpg", "Caption"), ("Next step", "...")],
     histo=[...], comp=[...], prog=[...], see_also=['other-slug'])
   ```
   `E()` writes `content/textbook-src/<slug>.json` and runs `tools/v4/convert.py <slug>`.
4. AI images: house style (soft pastel teal/coral/cream, white background, **no text**), checked by eye, imported with
   `python3 tools/v3/import_ai.py <src.jpg> v4-<name>` (no extension), then referenced in `mech` or attached with `IMG(slug, step_index, file, caption)`.
5. `python3 build.py --strict`, then screenshot checks (`tools/v3/shots.py --full --only=<slug>`), then commit and push.

## Splitting a combined page
Create one condition JSON per disease, delete the old one, and add the old slug to `content/redirects.json`:
`{"old-slug": {"title": "Old title", "note": "This topic has been split.", "to": ["new-a", "new-b"]}}`. The build writes a chooser page at the old URL. Update `condition:` links (`rg 'condition:old-slug' content`).

## Retired tools
The old `site_fold` pipeline (`/workspace/derm-teach/build/site_fold/*`, `fold_*.py`, `tools/_m6w1/*.py`, `tools/v3/to_steps.py`) wrote straight into `content/conditions` and `content/steps`. These scripts now exit immediately, so they cannot undo splits or overwrite authored pages. Do not re-enable them.

## Content blocks (course notes in `content/conditions/<slug>.json`)
Paragraph string (supports `**bold**`, `*italic*`, `[link](https://…)`, `[page](condition:slug)`), `{"h": "Sub-heading"}`, `{"list": [...]}`, `{"ol": [...]}`, `{"table": {"head": [...], "rows": [[...]]}}`, `{"callout": "info|tip|warn|danger", "title": "…", "text": "…"}`, `{"figure": {"photo": "A01"}}`, `{"figures": [...]}`.
Photo codes: core set bare (`"A01"`), other sets `"<set>:<code>"` (ids in `content/photo-sets.json`). AI images: `{"ai": "file.jpg"}` from `assets/img/ai/`.
