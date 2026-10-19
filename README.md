# Derm Teach

Personal study site for UK pharmacist independent prescriber (IP) dermatology teaching: a static library of primary-care skin conditions (category → condition), with UK-focused management notes, red flags, and teaching photos.

**Browse online:** [https://mostafadmg.github.io/derm-teach/](https://mostafadmg.github.io/derm-teach/)

**Open locally** (from this repo root):

```bash
python3 -m http.server 8000
```

Then visit [http://localhost:8000](http://localhost:8000). You can also open `index.html` directly in a browser.

**Rebuild** after editing JSON under `content/`:

```bash
python3 build.py
```

Clinical photos are credited on the [credits page](credits.html), including **DermNet** (dermnetnz.org) and other holders listed there. Personal educational material only — check current BNF and NICE CKS for practice.

For adding conditions and folder layout, see [ADD_CONDITION.md](ADD_CONDITION.md).
