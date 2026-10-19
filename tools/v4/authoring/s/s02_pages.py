import sys, json; sys.path.insert(0, '/workspace/derm-teach/website/tools/v4'); from split import *

# ---------- acne scars / keloids
page('acne-scars', base='acne-scars-keloids', title='Acne scars', order=1, card_image='m6w6:I01',
 aka=['acne scarring', 'ice-pick scars', 'boxcar scars', 'rolling scars', 'atrophic scars', 'post-inflammatory hyperpigmentation', 'subcision', 'TCA CROSS'],
 summary='Atrophic acne scars (ice-pick, boxcar, rolling), how to tell scar from pigment, and which specialist modalities suit which scar. Prevention is treating active acne early; scarring is a NICE referral trigger.',
 what=[{"callout": "info", "title": "Scope: counselling and recognition", "text": "For the pharmacist/IP, this page covers recognising scar types, setting expectations, safety and referral. It is **not** a procedure how-to."},
       "Acne scarring is fibrous remodelling after inflammatory acne. **Atrophic** scars follow collagen destruction; raised scars are covered on [Keloids and hypertrophic scars](condition:keloids-hypertrophic-scars). Scars are usually permanent but may soften with time or combined treatment. The psychological impact is often high, even when scarring looks ‘mild’."],
 cause=[L("Inflammatory nodules and cysts cause net **collagen destruction**, giving **atrophic** scars.", "Risk rises with acne severity and duration, delay in treatment, picking (acne excoriée) and smoking.", "**Post-inflammatory erythema and hyper- or hypopigmentation** are colour change, not true scarring, but patients often call both ‘scars’.")],
 features=[T(["Type", "Appearance", "Typical sites"], ["Ice-pick", "Narrow, deep, V-shaped; deeper than wide (about 60–70% of atrophic scars)", "Cheeks"], ["Boxcar", "Round or oval depressions with sharp vertical edges", "Cheeks, temples"], ["Rolling", "Wider, sloping edges, tethered by dermal bands", "Cheeks"], ["Perifollicular elastolysis", "Small, pale, follicular atrophic scars", "Back, chest"], ["PIH / PIE (not scar)", "Flat brown or red marks; no change in skin contour", "Anywhere acne occurred"])],
 diagnosis=["Clinical: history of acne plus scar morphology. Document **Fitzpatrick skin type**, whether acne is still active, and the patient’s goals."],
 differentials=[T(["Look-alike", "Distinguishing clues"], ["PIH or erythema alone", "Flat colour change, with no depression"], ["Chickenpox scars", "History of varicella; scattered"], ["Traumatic or surgical scar", "History of injury"])],
 management=[H("Prevent"), "Treat active acne **early and adequately** (see [Acne vulgaris](condition:acne-vulgaris)). **Scarring is a referral trigger** under NICE NG198. Treat active acne first, before any scar procedures.",
             H("Specialist modalities (overview)"),
             T(["Scar type", "Options (specialist or cosmetic)"], ["Ice-pick", "**TCA CROSS** (chemical reconstruction of skin scars), punch excision or grafting"], ["Boxcar", "Resurfacing (fractional lasers, peels), punch techniques, microneedling"], ["Rolling", "**Subcision**, dermal fillers or fat, microneedling, fractional laser"]),
             "Combined, multi-session approaches are usual. Refer to dermatology, plastic surgery or a reputable aesthetic clinic, and explain that the aim is **improvement, not removal**."],
 red_flags=["Scarring or significant distress at any acne severity: refer (NG198).", "Low mood, anxiety or body dysmorphic concerns: signpost or refer for mental health support."],
 pearls=["**Separate scar from pigment.** The treatments are different.", "Check isotretinoin status before procedures: see [Cosmetic procedures](condition:cosmetic-procedures)."],
 photos=[{"title": "Atrophic acne scars: ice-pick, rolling, boxcar", "items": ["m6w6:I01", "m6w6:I02", "m6w6:I03", "m6w6:I06", "m6w6:I04"]}, {"title": "Pigment, not scar: PIH", "items": ["m6w6:I05"]}],
 refs=[("DermNet: Acne scarring", "https://dermnetnz.org/topics/acne-scarring"), ("NICE NG198: Acne (referral for scarring)", "https://www.nice.org.uk/guidance/ng198")])

page('keloids-hypertrophic-scars', base='acne-scars-keloids', title='Keloids and hypertrophic scars', order=2, card_image='m6w6:J01',
 aka=['keloid', 'hypertrophic scar', 'raised scar', 'silicone gel', 'intralesional steroid'],
 summary='Raised scars from excess collagen: hypertrophic scars stay within the wound and often settle; keloids spread beyond it, persist and recur after excision. Silicone and steroid first; procedures are specialist.',
 what=["A **hypertrophic scar** is a raised scar that stays **within** the original wound and often improves over 1–2 years. A **keloid** is firm scar tissue that grows **beyond** the original wound border, persists and often recurs after excision."],
 cause=[L("Excess collagen production with reduced breakdown during wound healing.", "Triggers: acne, piercing, surgery (especially under tension), burns, vaccination, minor trauma.", "**Keloids** are much more common in **skin of colour** and run in families.")],
 features=[T(["", "Hypertrophic scar", "Keloid"], ["Border", "Stays within the wound", "Extends **beyond** the wound"], ["Onset", "Weeks after injury", "Months, may keep growing"], ["Course", "Often flattens over 1–2 years", "Persists; **high recurrence** after excision"], ["Sites", "Anywhere, under tension", "Earlobes, jawline, chest, shoulders, upper back"]),
           "Keloids may itch or hurt."],
 diagnosis=["Clinical. Biopsy only for an atypical, rapidly growing or ulcerated ‘keloid’ (exclude dermatofibrosarcoma protuberans or other tumour)."],
 differentials=[T(["Look-alike", "Distinguishing clues"], ["[Dermatofibroma](condition:dermatofibroma)", "Small firm papule, dimple sign"], ["[DFSP](condition:dermatofibrosarcoma-protuberans)", "Slowly enlarging plaque without a clear injury: biopsy"], ["Sarcoidosis in a scar", "Purple papules in old scars; systemic signs"])],
 management=[L("Prevention: avoid elective procedures (piercing, cosmetic surgery) on keloid-prone sites in people with a keloid history.", "**Silicone gel or sheet** (OTC) for months, not weeks; pressure (earlobe pressure clips).", "Potent topical steroid under occlusion for early raised scars.", "Specialist: **intralesional steroid**, cryotherapy, pulsed dye laser, careful excision with adjuvant therapy (**high recurrence** after excision alone)."),
             "Explain that the aim is **improvement, not removal**."],
 red_flags=["A rapidly growing or atypical ‘keloid’: exclude a tumour.", "Keloid tendency or skin of colour before elective procedures: experienced operator only."],
 pearls=["Keloids extend beyond the wound; hypertrophic scars do not.", "OTC silicone gel is a reasonable first step for early raised scars: months, not weeks."],
 photos=[{"title": "Keloid and hypertrophic scars", "items": ["m6w6:J01", "m6w6:J02", "m6w6:J03", "m6w6:J04"]}],
 refs=[("DermNet: Keloid and hypertrophic scar", "https://dermnetnz.org/topics/keloid-and-hypertrophic-scar")])

steps('acne-scars', features={"visuals": [{"ai": "v3-atrophic-scar-types.jpg", "caption": "Atrophic acne scars: ice-pick, boxcar and rolling.", "alt": "Atrophic scar types"}]},
 manage={"lead": "Prevent by treating acne early; scar treatment is specialist and multi-session.", "rungs": [
  {"k": "Prevent", "tone": "base", "points": ["Treat active acne **early and adequately**; scarring = refer (NG198)."]},
  {"k": "Specialist: atrophic", "tone": "refer", "points": ["Ice-pick: TCA CROSS, punch excision / grafting.", "Boxcar: fractional laser, peels, punch, microneedling.", "Rolling: subcision, fillers, microneedling, laser."]}],
  "limits": [{"k": "Expectations", "t": "Improvement, not removal."}, {"k": "Isotretinoin", "t": "Check status before procedures."}, {"k": "Skin of colour", "t": "Higher PIH risk: experienced operator only.", "tone": "danger"}]},
 refer={"items": [{"when": "routine", "t": "Scarring or significant distress at any acne severity (NG198)."}, {"when": "routine", "t": "Low mood or body dysmorphic concerns: mental-health support."}]},
 quiz=[{"q": "Which atrophic scar type is commonest?", "a": "Ice-pick (about 60–70%)."}, {"q": "What treatment suits rolling scars?", "a": "Subcision (± fillers, microneedling, laser)."}, {"q": "How do you tell PIH from a scar?", "a": "PIH is flat colour change with no contour change."}, {"q": "What does NICE say about scarring?", "a": "Scarring is a referral trigger at any acne severity."}])
steps('keloids-hypertrophic-scars', features={"visuals": [{"ai": "v3-hypertrophic-vs-keloid.jpg", "caption": "Hypertrophic scar (left) stays inside the wound outline; a keloid (right) spreads beyond it.", "alt": "Hypertrophic scar vs keloid"}]},
 manage={"lead": "Silicone and steroid first; procedures are specialist.", "rungs": [
  {"k": "Early raised scar", "tone": "base", "points": ["**Silicone gel or sheet** for months; pressure for earlobes."]},
  {"k": "Persistent", "tone": "first", "points": ["Potent topical steroid under occlusion."]},
  {"k": "Specialist", "tone": "refer", "points": ["Intralesional steroid, cryotherapy, pulsed dye laser, excision with adjuvant (high recurrence)."]}]},
 refer={"items": [{"when": "urgent", "t": "Rapidly growing or atypical ‘keloid’: exclude a tumour."}, {"when": "routine", "t": "Symptomatic or disfiguring keloids."}]},
 quiz=[{"q": "Key difference between keloid and hypertrophic scar?", "a": "Keloids extend beyond the original wound; hypertrophic scars do not."}, {"q": "Which skin types are most keloid-prone?", "a": "Skin of colour (Fitzpatrick IV–VI), with family history."}, {"q": "First-line OTC treatment?", "a": "Silicone gel or sheet for months."}, {"q": "Why avoid excision alone?", "a": "Keloids recur in most cases without adjuvant therapy."}])
retire('acne-scars-keloids', 'Acne scars & keloids', 'This topic has been split into two pages.', ['acne-scars', 'keloids-hypertrophic-scars'])

# ---------- IPL / eyelash
page('intense-pulsed-light', base='ipl-eyelash', title='Intense pulsed light (IPL)', order=6, card_image='m6w5:W5D-01',
 aka=['IPL', 'intense pulsed light', 'photofacial', 'photorejuvenation', 'hypopigmentation after IPL'],
 summary='Counselling on intense pulsed light for redness, pigment and hair: who is a good candidate, what to expect, and the burn and pigment risks, especially in tanned or darker skin.',
 what=["**Intense pulsed light (IPL)** is a non-laser flashlamp delivering broad-spectrum light through filters to treat vascular redness, solar lentigines and unwanted dark hair, with modest texture benefit."],
 cause=[L("Selective photothermolysis: melanin and oxyhaemoglobin absorb the light and heat up; dermal heating may remodel collagen modestly.", "Darker or tanned skin absorbs more epidermal energy, giving a higher risk of burns and pigment change.")],
 features=[L("Sessions often 3–6, weeks apart; treated pigment darkens like “coffee grounds” then flakes over 1–2 weeks.", "Adverse effects: burns, blistering, **hypo-/hyperpigmentation** (sometimes grid footprints), scarring, paradoxical hair growth, eye injury.")],
 diagnosis=["Before IPL: confirm the diagnosis of every pigmented spot (no undiagnosed lesions), Fitzpatrick type, recent tan, photosensitising drugs and HSV history. Melasma is generally a poor IPL candidate."],
 differentials=[T(["Request", "Better framed as"], ["Diffuse redness + lentigines", "IPL photofacial after a skin cancer check"], ["Discrete stubborn lentigo", "Often a pigment laser rather than IPL"], ["Melasma", "Sunscreen + medical therapy; avoid heat devices first-line (see [Melasma](condition:melasma-facial-melanosis))"])],
 management=[H("IPL counselling (UK)"), L("Check practitioner training, insurance, patch test and (in Wales) HIW registration for Class 3B/4 lasers/IPL in independent clinics.", "Contraindications/cautions: undiagnosed pigmented lesions, active infection/HSV, recent tan, photosensitivity disorders, many photosensitising drugs; extra caution in skin types IV–VI and on isotretinoin (many delay treatment).", "Aftercare: SPF, gentle skincare, no picking; seek review for blistering or infection.", "See also [solar lentigines](condition:solar-lentigines) and [photoageing](condition:photoageing).")],
 red_flags=["Eye pain or visual change during/after IPL: **urgent ophthalmology**.", "Blistering burns or striped hypopigmentation: stop further treatment; specialist wound/pigment advice.", "Undiagnosed changing pigmented lesion: cancel IPL; refer."],
 pearls=["IPL is versatile but unforgiving on tanned or darker skin without expert settings.", "Coffee-ground darkening is expected; picking prolongs marks."],
 photos=[{"title": "IPL effects and adverse effects", "items": ["m6w5:W5D-01", "m6w5:W5D-02", "m6w5:W5D-03", "m6w5:W5D-04"]}],
 refs=[("DermNet: Intense pulsed light", "https://dermnetnz.org/topics/intense-pulsed-light-therapy"), ("DermNet: Lasers in dermatology", "https://dermnetnz.org/topics/lasers")])

page('eyelash-enhancement', base='ipl-eyelash', title='Eyelash enhancement (bimatoprost)', order=7, card_image='m6w5:W5E-01',
 aka=['bimatoprost', 'Latisse', 'eyelash growth', 'eyelash serum', 'hypotrichosis of the eyelashes', 'madarosis'],
 summary='Counselling on bimatoprost (a prostamide) for longer, darker lashes: how it works, permanent iris darkening, reversible eyelid pigmentation and when to exclude a disease cause of lash loss.',
 what=["**Eyelash enhancement** options include cosmetics, lifts and **bimatoprost** (a prostamide also used in glaucoma drops) applied to the upper lid margin to lengthen lashes."],
 cause=["Bimatoprost increases eyelash length, thickness and darkness by **extending anagen** and stimulating follicle melanogenesis; periocular skin and iris melanocytes can also respond."],
 features=[L("Longer, darker lashes over weeks to months.", "Side effects: periocular hyperpigmentation, **iris colour change** (especially hazel/green eyes), itch, redness; periorbital fat atrophy (glaucoma-dose context).")],
 diagnosis=["Before use: exclude a disease cause of sparse lashes (**madarosis**): alopecia areata, thyroid disease, blepharitis, trichotillomania, chemotherapy."],
 differentials=[T(["Cause of sparse lashes", "Clue"], ["[Alopecia areata](condition:alopecia-areata)", "Patchy loss elsewhere; exclamation-mark hairs"], ["[Trichotillomania](condition:trichotillomania)", "Broken lashes of different lengths"], ["Blepharitis", "Crusted, red lid margins"], ["Thyroid disease", "Loss of the outer brows; systemic symptoms"])],
 management=[H("Bimatoprost eyelash counselling"), L("Explain cosmetic versus glaucoma origins; apply only as directed to the upper lid margin, not into the eye for cosmetic use.", "Warn about **permanent iris darkening**, reversible periocular skin darkening, possible hair growth on unintended skin if the product migrates, and ocular irritation.", "Avoid with active ocular inflammation unless an ophthalmologist agrees; remove contact lenses as per product advice.", "Effects reverse over weeks to months if stopped.", "Check the current SmPC/BNF; this page does not cover off-label periocular protocols.")],
 red_flags=["Eye pain, redness or visual change: stop and seek ophthalmology review.", "Patients on glaucoma drops: discuss with their ophthalmologist (additive effect on intraocular pressure)."],
 pearls=["Eyelash serums sold cosmetically vary widely; prescription bimatoprost needs proper counselling on iris pigment."],
 photos=[{"title": "Bimatoprost eyelash growth", "items": ["m6w5:W5E-01", "m6w5:W5E-02"]}],
 refs=[("BNF: Bimatoprost", "https://bnf.nice.org.uk/drugs/bimatoprost/")])

steps('intense-pulsed-light', manage={"lead": "Right patient, right operator, sun-safe aftercare.", "rungs": [
  {"k": "Select", "tone": "base", "points": ["Diagnose every pigmented lesion first; check skin type, tan, drugs, HSV."]},
  {"k": "Treat", "tone": "first", "points": ["3–6 sessions by a trained, registered operator; patch test."]},
  {"k": "Aftercare", "tone": "second", "points": ["SPF, no picking; review blistering or infection."]}]},
 refer={"items": [{"when": "same-day", "t": "Eye pain or visual change after IPL: ophthalmology."}, {"when": "urgent", "t": "Undiagnosed changing pigmented lesion: suspected cancer pathway."}]},
 quiz=[{"q": "What are IPL's target chromophores?", "a": "Melanin and oxyhaemoglobin (and hair melanin)."}, {"q": "Who is at higher risk of IPL burns and pigment change?", "a": "Tanned or darker skin (types IV–VI)."}, {"q": "Is melasma a good IPL indication?", "a": "Generally no; heat can worsen it."}, {"q": "What is the 'coffee grounds' effect?", "a": "Expected darkening of treated pigment that flakes off over 1–2 weeks."}])
steps('eyelash-enhancement', manage={"lead": "Counsel on iris colour before starting.", "rungs": [
  {"k": "Exclude disease", "tone": "base", "points": ["Check for alopecia areata, blepharitis, thyroid disease, trichotillomania."]},
  {"k": "Bimatoprost", "tone": "first", "points": ["Apply to the upper lid margin as licensed; effects over weeks to months."], "rx": [{"drug": "Bimatoprost (eyelash)", "dose": "as per SmPC/BNF", "dur": "continuous", "note": "Permanent iris darkening possible; periocular pigment reverses."}]}]},
 refer={"items": [{"when": "routine", "t": "Lash loss with scalp or brow loss, or lid disease: GP/dermatology/ophthalmology."}, {"when": "urgent", "t": "Eye pain, redness or visual change on treatment."}]},
 quiz=[{"q": "How does bimatoprost lengthen lashes?", "a": "It prolongs the anagen (growth) phase."}, {"q": "Which side effect is permanent?", "a": "Iris darkening."}, {"q": "Which effect reverses on stopping?", "a": "Periocular skin darkening and the lash growth."}, {"q": "What is madarosis?", "a": "Loss of eyelashes or eyebrows, which may signal disease."}])
retire('ipl-eyelash', 'IPL & eyelash enhancement', 'This topic has been split into two pages.', ['intense-pulsed-light', 'eyelash-enhancement'])

# ---------- special naevi
P = 'spitz-blue-halo-naevi'
page('halo-naevus', base=P, title='Halo naevus (Sutton naevus)', order=18, card_image='m2w4:E01',
 aka=['halo naevus', 'Sutton naevus', 'leukoderma acquisitum centrifugum'],
 summary='A mole surrounded by a symmetrical white ring as the immune system clears it; common in children and teenagers and linked with vitiligo. A new halo in an adult over 40, or an atypical centre, needs assessment for melanoma.',
 what=["A **halo naevus** is a melanocytic naevus surrounded by a symmetrical **depigmented ring**, caused by immune destruction of the naevus. It is common in children and teenagers and may be multiple."],
 cause=["Cytotoxic T cells recognise naevus melanocytes and destroy them and the surrounding normal melanocytes; there is an **association with vitiligo**."],
 features=[L("Central brown naevus with a round or oval white ring; over months the centre fades and may disappear.", "The white area later repigments in many.", "Back is the commonest site.")],
 diagnosis=["Clinical with dermoscopy: a regular globular or homogeneous centre with a white halo. An asymmetric or atypical centre, or onset over 40, needs specialist assessment."],
 differentials=["Melanoma with regression or a halo (adults, atypical centre), [vitiligo](condition:hypopigmentation-skin-of-colour), post-inflammatory hypopigmentation."],
 management=[L("Reassure if the central naevus is benign and symmetrical.", "**Refer an adult (over 40) with a new halo, or any atypical central lesion** (melanoma can provoke halos).", "Sun-protect the white ring (it burns easily).", "Examine the skin for vitiligo and other atypical naevi.")],
 red_flags=["Atypical central lesion or new halo in an adult: **suspected cancer pathway**."],
 pearls=["Halo naevi are benign in children; the halo is a sign of immune clearance, not of cancer."],
 photos=[{"title": "Halo naevus", "items": ["m2w4:E01", "m2w4:E02"]}], refs=[("DermNet: Halo naevus", "https://dermnetnz.org/topics/halo-naevus")])

page('blue-naevus', base=P, title='Blue naevus', order=19, card_image='m2w4:E03',
 aka=['blue naevus', 'blue nevus', 'cellular blue naevus', 'Tyndall effect'],
 summary='A steel-blue, firm, dome-shaped papule from pigment-producing melanocytes deep in the dermis. Long-standing and stable lesions are benign; new, enlarging or large lesions in adults need assessment.',
 what=["A **blue naevus** is a benign collection of pigment-producing **dermal melanocytes**. It appears as a steel-blue, firm, dome-shaped papule, usually under 1 cm, often appearing in childhood or adolescence."],
 cause=["Melanocytes arrested in the dermis during their embryonic migration; GNAQ/GNA11 mutations. The colour is blue because deep pigment scatters back mainly blue light (**Tyndall effect**)."],
 features=[L("Uniform slate- or steel-blue dome papule.", "Head and neck, backs of hands and feet, buttocks.", "**Cellular blue naevus**: larger (over 1 cm), often on the buttocks or scalp.")],
 diagnosis=["Clinical with dermoscopy (structureless homogeneous blue pigmentation). Excise if new in an adult, changing or large."],
 differentials=["**Nodular or metastatic melanoma** (can look blue), traumatic tattoo, venous lake, pigmented BCC, angiokeratoma."],
 management=[L("Reassure if long-standing and stable.", "Refer if new in an adult, enlarging, or over 1 cm (cellular blue naevus; melanoma differential).")],
 red_flags=["New or changing blue papule in an adult, or a history of melanoma (metastasis looks blue): **suspected cancer pathway**."],
 pearls=["Blue = deep pigment (Tyndall effect); brown = pigment near the surface."],
 photos=[{"title": "Blue naevus", "items": ["m2w4:E03"]}], refs=[("DermNet: Blue naevus", "https://dermnetnz.org/topics/blue-naevus")])

page('spitz-naevus', base=P, title='Spitz and Reed naevi', order=20, card_image='m2w4:E04',
 aka=['Spitz naevus', 'Reed naevus', 'pigmented spindle cell naevus', 'atypical Spitz tumour', 'spitzoid melanoma'],
 summary='Benign naevi of large epithelioid or spindle melanocytes that grow quickly in children and can mimic melanoma. Children under 12 with typical lesions may be monitored by specialists; adolescents and adults usually need excision.',
 what=["A **Spitz naevus** is a benign naevus made of large epithelioid and/or spindle melanocytes, typically a fast-growing pink or pigmented dome in a **child**. A **Reed naevus** (pigmented spindle cell naevus) is a dark, symmetrical variant, often on the thigh of young women."],
 cause=["Driven by HRAS mutations or kinase fusions (ALK, ROS1, NTRK and others); growth is followed by stabilisation. **Atypical Spitz tumours** lie between benign Spitz naevi and spitzoid melanoma."],
 features=[L("**Spitz**: pink-red or pigmented, dome-shaped, smooth, rapidly growing over months in a child; face and limbs. Dermoscopy: starburst or dotted vessels.", "**Reed**: black, symmetrical, starburst pattern; thigh in young women.")],
 diagnosis=["Dermoscopy plus age and growth pattern. Excision for histology in adolescents and adults, and in any atypical lesion; specialist histopathology review."],
 differentials=["**Spitzoid melanoma** (adults, asymmetry), pyogenic granuloma, juvenile xanthogranuloma, haemangioma, dermatofibroma, nodular melanoma."],
 management=[L("Children under 12 with a typical lesion: specialist may monitor with dermoscopy.", "**Adolescents/adults: excision** (atypical Spitz tumour and spitzoid melanoma differential).", "Reed naevi are usually excised for histology.")],
 red_flags=["A Spitz-like lesion in an adult, or any atypical, ulcerated or rapidly growing lesion: **suspected cancer pathway**."],
 pearls=["Rapid growth worries parents but is typical of Spitz naevi in children; age decides how worried to be."],
 photos=[{"title": "Spitz and Reed naevi", "items": ["m2w4:E04", "m2w4:E05"]}], refs=[("DermNet: Spitz naevus", "https://dermnetnz.org/topics/spitz-naevus")])

for s in ('halo-naevus', 'blue-naevus', 'spitz-naevus'):
    steps(s, manage={"lead": {"halo-naevus": "Reassure children; assess adults.", "blue-naevus": "Reassure if stable; excise if new or changing in an adult.", "spitz-naevus": "Monitor typical lesions in young children; excise in teens and adults."}[s], "rungs": [
        {"k": "Typical, stable", "tone": "base", "points": ["Reassure; photograph; sun protection."]},
        {"k": "Atypical or adult", "tone": "refer", "points": ["Dermatology via the suspected cancer pathway; excision for histology."]}]},
      refer={"items": [{"when": "urgent", "t": {"halo-naevus": "New halo over 40 or atypical centre.", "blue-naevus": "New, enlarging or >1 cm blue lesion in an adult.", "spitz-naevus": "Spitz-like lesion in an adolescent or adult; any atypical features."}[s]}]},
      quiz={"halo-naevus": [{"q": "What causes the white ring?", "a": "T-cell destruction of the naevus and surrounding melanocytes."}, {"q": "Which condition is associated?", "a": "Vitiligo."}, {"q": "When should a halo naevus be referred?", "a": "New halo in an adult over 40, or an atypical central lesion."}],
            "blue-naevus": [{"q": "Why does a blue naevus look blue?", "a": "Deep dermal pigment scatters blue light (Tyndall effect)."}, {"q": "Which dangerous lesion can look blue?", "a": "Nodular or metastatic melanoma."}, {"q": "Size threshold for concern?", "a": "Over 1 cm (cellular blue naevus) or enlarging."}],
            "spitz-naevus": [{"q": "Typical patient with a Spitz naevus?", "a": "A child with a fast-growing pink dome."}, {"q": "What is a Reed naevus?", "a": "A pigmented spindle-cell naevus: dark symmetrical starburst, often on a young woman's thigh."}, {"q": "Management in adults?", "a": "Excision (spitzoid melanoma differential)."}]}[s])

# recurrent naevus, spilus, acral -> melanocytic-naevi
p = C / 'conditions/melanocytic-naevi.json'; d = json.loads(p.read_text())
if not any(isinstance(b, dict) and b.get('h') == 'Other naevus types' for b in d['sections']['features']):
    d['sections']['features'] += [H('Other naevus types'), T(["Naevus", "Key features", "Management"],
        ["**Recurrent naevus** (\"pseudomelanoma\")", "Pigment returning in a scar after a shave or incomplete excision", "Refer **with the previous histology**; it mimics melanoma on dermoscopy"],
        ["Naevus spilus (speckled lentiginous)", "Tan patch with darker speckles", "Monitor; small melanoma risk"],
        ["Acral naevus", "Parallel-**furrow** pattern on dermoscopy", "Parallel-**ridge** pattern = melanoma (see [melanoma](condition:melanoma))"]),
        "Special naevi have their own pages: [halo naevus](condition:halo-naevus), [blue naevus](condition:blue-naevus) and [Spitz and Reed naevi](condition:spitz-naevus)."]
    d['photos'].append({"title": "Recurrent naevus in a scar", "items": ["m2w4:E06"]})
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1))
retire(P, 'Halo, blue, Spitz & recurrent naevi', 'This topic has been split into separate pages. Recurrent naevi, naevus spilus and acral naevi are covered on the moles page.', ['halo-naevus', 'blue-naevus', 'spitz-naevus', 'melanocytic-naevi'])

# ---------- perioral dermatitis (acne-mimics stays as a differential page)
page('perioral-dermatitis', base='acne-mimics', title='Perioral (periorificial) dermatitis', order=3, card_image='m6w2:K09',
 aka=['perioral dermatitis', 'periorificial dermatitis', 'periocular dermatitis', 'steroid-induced perioral dermatitis'],
 summary='Small red papules and pustules around the mouth, nose or eyes with a clear rim next to the lips, often provoked by topical or inhaled steroids and heavy creams. Stop the steroid, expect a rebound, and treat with topical metronidazole or azelaic acid, or an oral tetracycline.',
 what=["**Perioral dermatitis** (periorificial dermatitis) is a common facial eruption of small papules and pustules around the mouth, nose and sometimes eyes, with a characteristic **clear zone next to the lip vermilion**. It mainly affects women aged 20–45 and children."],
 cause=[L("**Topical corticosteroids** on the face are the commonest trigger; also inhaled or nasal steroids, and heavy moisturisers or foundations.", "Fluorinated toothpaste and barrier disruption may contribute.")],
 features=[L("Monomorphic 1–2 mm red papules, papulovesicles and pustules on a red, sometimes scaly background.", "Around the mouth, nasolabial folds, chin; may involve the sides of the nose and eyelids (**periocular**).", "**Vermilion sparing**: a narrow clear rim around the lips.", "Burning or tightness more than itch; no comedones.")],
 diagnosis=["Clinical. Ask specifically about steroid creams, inhalers, nasal sprays and cosmetics."],
 differentials=[T(["Look-alike", "Clues"], ["[Rosacea](condition:rosacea)", "Older; flushing; central face; no clear perioral rim"], ["[Acne vulgaris](condition:acne-vulgaris)", "Comedones; polymorphic lesions"], ["Seborrhoeic dermatitis", "Greasy scale in nasolabial folds and brows"], ["[Contact dermatitis](condition:contact-dermatitis)", "Itch, eczematous, linked to a product"])],
 management=[L("**Stop the facial steroid** (taper systemic or high-potency use with the prescriber; never stop inhaled asthma steroids: rinse and wipe the face after use).", "Warn of a **rebound flare** for 1–2 weeks after stopping.", "‘Zero therapy’: stop all creams and cosmetics; use a gentle cleanser only.", "Topical **metronidazole** or **azelaic acid**.", "Oral tetracycline for 6–8 weeks if needed (erythromycin if under 12).")],
 red_flags=["Granulomatous or periocular disease not responding, or diagnostic doubt: dermatology."],
 pearls=["Pharmacists often spot inhaled-steroid perioral dermatitis: advise rinsing and wiping the face after inhalers.", "Hydrocortisone makes it look better briefly, then worse."],
 photos=[{"title": "Steroid-induced perioral dermatitis", "items": ["m6w2:K09"]}],
 refs=[("DermNet: Periorificial dermatitis", "https://dermnetnz.org/topics/periorificial-dermatitis"), ("NICE CKS: Perioral dermatitis", "https://cks.nice.org.uk/topics/perioral-dermatitis/")])
steps('perioral-dermatitis', manage={"lead": "Stop the steroid; expect a rebound; treat for weeks.", "rungs": [
  {"k": "Stop triggers", "tone": "base", "points": ["Stop facial steroids and heavy creams; gentle cleanser only."]},
  {"k": "Topical", "tone": "first", "points": ["Topical metronidazole or azelaic acid."]},
  {"k": "Oral", "tone": "second", "points": ["Oral tetracycline 6–8 weeks if needed (erythromycin if under 12)."]}]},
 refer={"items": [{"when": "routine", "t": "Not responding after 8–12 weeks, granulomatous or periocular disease, diagnostic doubt."}]},
 quiz=[{"q": "Commonest trigger of perioral dermatitis?", "a": "Topical (or inhaled/nasal) corticosteroids on the face."}, {"q": "What is the classic sign around the lips?", "a": "A clear rim next to the vermilion (vermilion sparing)."}, {"q": "What happens after stopping the steroid?", "a": "A rebound flare for 1–2 weeks."}, {"q": "Oral option in under-12s?", "a": "Erythromycin (tetracyclines avoided)."}])
p = C / 'conditions/acne-mimics.json'; d = json.loads(p.read_text())
m = d['sections']['management']
for i, b in enumerate(m):
    if isinstance(b, dict) and b.get('h') == 'Steroid / perioral dermatitis':
        m.insert(i + 2, "Perioral dermatitis now has its own page: [Perioral dermatitis](condition:perioral-dermatitis).") if "perioral-dermatitis)" not in json.dumps(m) else None
        break
d['title'] = 'Acne mimics: rosacea, steroid eruptions and folliculitis'
p.write_text(json.dumps(d, ensure_ascii=False, indent=1))
print('part2 ok')
