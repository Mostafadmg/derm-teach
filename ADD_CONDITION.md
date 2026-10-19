# How to add (or finish) a condition

Each condition is **one JSON file** in `content/conditions/`. Run `python3 build.py` after any change.
Files whose names start with `_` (e.g. `_template.json`) are ignored.

## 1. Skeleton

```json
{
  "slug": "seborrhoeic-dermatitis",          // file name and URL: conditions/<slug>.html
  "title": "Seborrhoeic dermatitis",
  "aka": ["dandruff", "cradle cap"],         // extra search terms, shown as "Covers" chips
  "category": "inflammatory",                // id from content/categories.json
  "status": "published",                     // or "coming-soon" (shows a stub banner)
  "order": 3,                                // position inside the category
  "module": "Module 4 · Week 2",             // optional tag
  "summary": "One or two sentences used on the category list and in search.",
  "card_image": "A12",                       // optional thumbnail (a photo code)
  "hero": {"ai": "eczema-diagram.jpg", "caption": "..."},   // optional
  "glance": { "think": "", "engine": "", "backbone": "", "never_miss": "" },
  "sections": {
    "what": [], "cause": [], "features": [], "diagnosis": [],
    "differentials": [], "management": [], "red_flags": [], "pearls": []
  },
  "planned": ["Only used on stubs: bullet list of planned topics"],
  "photos": [
    {"title": "Scalp and face", "items": ["A12", "A13"]},
    {"title": "Red flag: ...", "tone": "danger", "items": ["m6w4:W4A-15"]}
  ],
  "references": ["NICE CKS: Seborrhoeic dermatitis (2024)"]
}
```
(Comments are for explanation only. JSON does not allow them. Start from `content/conditions/_template.json`.)

The section order is fixed, so every page reads the same way. An empty section shows a "Content coming soon" placeholder but keeps its anchor.

## 2. Content blocks (inside each section array)

| Block | JSON |
|---|---|
| Paragraph | `"Plain text with **bold**, *italic*, [link](https://…), [another page](condition:tinea)"` |
| Sub-heading | `{"h": "Topical options"}` |
| Bullet list | `{"list": ["one", "two"]}` |
| Numbered steps | `{"ol": ["first", "second"]}` |
| Table | `{"table": {"head": ["Drug", "Dose"], "rows": [["Clotrimazole 1%", "BD–TDS"]]}}`, which becomes stacked cards on phones |
| Callout | `{"callout": "info" \| "tip" \| "warn" \| "danger", "title": "…", "text": "…"}` (or `"list": [...]`) |
| Single figure | `{"figure": {"photo": "A01", "caption": "optional override"}}` or `{"figure": {"ai": "file.jpg", "caption": "…"}}` |
| Figure row | `{"figures": [{"photo": "A01"}, {"photo": "m5w1:L03"}]}` |

In `red_flags` and `pearls`, plain strings become icon bullet lists.
Avoid `***triple***` asterisks. Use `**bold**` only.

## 3. Photo codes

* A **code** is the first part of the image file name before `_` (`A01_plaque_psoriasis.jpg` → `A01`).
* Core adult set (`assets/img/dermnet/`): bare code, e.g. `"A01"`.
* Other sets: `"<set>:<code>"`, e.g. `"m5w2:Q03"` or `"m6w4:W4C-02"`. Set ids are in `content/photo-sets.json`.
* Captions, credit lines, source links and the credits page are all filled in automatically from the set's manifest. Unknown codes give a build warning.
* AI diagrams: `{"ai": "file.jpg"}` from `assets/img/ai/`.

## 4. Add a new photo set (e.g. a new week)

1. Copy the images into `assets/img/<setid>/` (flat folder, keep the file names).
2. Copy the manifest (`filename`, `teaching_point`, `dermnet_caption`/`source_caption`, `source_site`, `source_page_url`, `copyright`, `attribution`) to `content/manifests/<setid>.json`.
3. Add `{"id": "<setid>", "label": "Module X · Week Y", "dir": "assets/img/<setid>", "manifest": "content/manifests/<setid>.json"}` to `content/photo-sets.json`.
4. Use the photos as `"<setid>:<code>"`.

## 5. Add a category

Add an entry to `content/categories.json`: `id`, `title`, `blurb`, `icon` (one of flame, follicle, ring, bacteria, baby, virus, leg, drop, hourglass, sparkle), `order`, `status` (`published`/`coming-soon`), `soon_note`.

## 6. Publish a stub

Open the stub (e.g. `scabies.json`), fill in `glance` and `sections` from the research pack (paraphrase it in UK English), optionally delete `planned`, set `"status": "published"`, then rebuild. Check with `python3 build.py --strict`.
