import sys; sys.path.insert(0, '/workspace/derm-teach/website/tools/v4'); from split import *

# ---------- DRESS / AGEP
page('dress', base='dress-agep', title='DRESS (drug reaction with eosinophilia and systemic symptoms)', order=3, card_image='m1w3:C01',
 aka=['DRESS', 'DIHS', 'drug hypersensitivity syndrome', 'drug reaction with eosinophilia', 'RegiSCAR', 'allopurinol', 'carbamazepine'],
 summary='A delayed (2–8 weeks), multi-organ drug reaction: widespread rash, fever, facial oedema, lymphadenopathy, eosinophilia and liver, kidney, lung or heart involvement. Same-day hospital assessment.',
 what=["**DRESS** (drug reaction with eosinophilia and systemic symptoms; also called DIHS) is a delayed, multi-organ reaction with fever, rash and internal organ involvement. Mortality is about **2–10%**."],
 cause=[L("Type IVb (Th2 / eosinophil) reaction with **sequential herpesvirus reactivation** (HHV-6, then EBV/CMV), which explains the relapsing course.",
          "Culprits: **allopurinol**, **carbamazepine**, phenytoin, lamotrigine, phenobarbital, **sulfonamides/dapsone**, minocycline, vancomycin, abacavir/nevirapine, strontium.",
          "Latency **2–8 weeks** (the longest of the severe drug reactions).")],
 features=[L("Morbilliform rash that becomes infiltrated and oedematous, often **over 50% of body surface**; may become exfoliative.",
            "**Facial oedema** (key sign); fever above 38 °C; **lymphadenopathy**.",
            "Blood: eosinophilia (over 1.5 × 10⁹/L), atypical lymphocytes.",
            "**Organ involvement**: liver (commonest), kidney, lung, heart (myocarditis), thyroid.",
            "Course over weeks to months with relapses; **late autoimmune disease** (thyroiditis, type 1 diabetes).",
            "**RegiSCAR** score grades the likelihood of DRESS.")],
 diagnosis=["FBC with differential and film, LFT, U&E, urinalysis, troponin/ECG if symptomatic, TFT, lipase, HHV-6 PCR and skin biopsy. Patch testing later can help identify the culprit."],
 differentials=["Viral exanthem, lymphoma (especially angioimmunoblastic), hypereosinophilic syndrome, SJS/TEN, Kawasaki disease, simple [morbilliform drug eruption](condition:morbilliform-drug-eruption)."],
 management=[L("**Stop the culprit**, document, Yellow Card, and avoid for life (including cross-reacting drugs).",
              "**Same-day hospital assessment** if fever, facial oedema, eosinophilia or abnormal LFTs.",
              "Mild disease without significant organ involvement: potent topical steroids.",
              "With organ involvement: **systemic corticosteroids** (e.g. prednisolone 0.5–1 mg/kg/day) **tapered slowly over 6–12 weeks**: rapid tapers cause relapse.",
              "Monitor organs for months, and check **TFT and glucose** for 1–2 years."),
             H("IP scope"), "Recognise, stop, refer, document, Yellow Card. After discharge: support the specialist steroid taper (steroid card if prolonged) and monitor TFT/glucose per the specialist letter."],
 red_flags=["Fever + rash + facial oedema or lymphadenopathy **2–8 weeks** after a new anticonvulsant, allopurinol or sulfonamide: **same-day admission** (hepatitis, nephritis and myocarditis can follow).",
            "Allopurinol (HLA-B*58:01), carbamazepine (HLA-B*15:02) and lamotrigine are high-risk starts: counsel to report a rash early."],
 pearls=["DRESS has the **longest latency** of the severe drug reactions (2–8 weeks).", "\"**Allopurinol + CKD + recent start + rash** = DRESS/SJS risk\": dose adjustment and HLA-B*58:01 awareness."],
 photos=[{"title": "DRESS", "items": ["m1w3:C01"]}], refs=[("DermNet: Drug hypersensitivity syndrome (DRESS)", "https://dermnetnz.org/topics/drug-hypersensitivity-syndrome")])

page('agep', base='dress-agep', title='AGEP (acute generalised exanthematous pustulosis)', order=4, card_image='m1w3:C02',
 aka=['AGEP', 'acute generalised exanthematous pustulosis', 'pustular drug eruption', 'toxic pustuloderma'],
 summary='Sudden sheets of tiny sterile non-follicular pustules on red, swollen skin within hours to 2 days of a drug (often an antibiotic), with fever. Usually settles in 1–2 weeks once the drug is stopped.',
 what=["**AGEP** (acute generalised exanthematous pustulosis) is an abrupt eruption of **sterile, non-follicular pinhead pustules** on oedematous erythema. It is usually self-limiting; mortality is under 5%."],
 cause=[L("Type IVd reaction: drug-specific T cells release **IL-8 (CXCL8)**, recruiting neutrophils into the epidermis.",
          "Culprits: **aminopenicillins**, macrolides, cephalosporins, **pristinamycin**, **hydroxychloroquine**, **diltiazem**, terbinafine.",
          "Latency **under 48 hours** for antibiotics; up to 1–2 weeks for some drugs.",
          "IL36RN variants overlap with generalised pustular psoriasis.")],
 features=[L("Pinhead pustules on erythema, starting in the **flexures and face** and becoming generalised; burning or itch.",
            "Fever above 38 °C; neutrophilia; mild organ involvement in up to 20%.",
            "Resolves in 1–2 weeks with **collarette desquamation**.")],
 diagnosis=["Clinical with history; FBC (neutrophilia), U&E, LFT. Biopsy shows subcorneal or intraepidermal spongiform pustules (to distinguish it from pustular psoriasis). The EuroSCAR score helps. Patch testing later."],
 differentials=["**Generalised pustular psoriasis** (history of psoriasis, slower onset, longer course), subcorneal pustular dermatosis, pustular DRESS, folliculitis, SJS/TEN (early AGEP can show Nikolsky-like sloughing)."],
 management=[L("**Stop the drug**, document, Yellow Card, avoid for life.", "Potent topical steroid; antipyretics; supportive care. Systemic steroids are rarely needed.", "Usually managed in dermatology, with admission if unwell.")],
 red_flags=["Widespread pustules within days of an antibiotic: **same-day dermatology**.", "Mucosal erosions, skin sloughing or systemic organ dysfunction: hospital."],
 pearls=["AGEP has the **shortest latency** of the severe drug reactions (hours to 2 days).", "Pustules in AGEP are **non-follicular** (unlike folliculitis)."],
 photos=[{"title": "AGEP", "items": ["m1w3:C02", "m1w3:C03"]}], refs=[("DermNet: AGEP", "https://dermnetnz.org/topics/acute-generalised-exanthematous-pustulosis")])

steps('dress', manage={"lead": "Recognise, stop, admit.", "rungs": [
  {"k": "Stop and record", "tone": "base", "points": ["Stop the culprit; record the allergy; Yellow Card."]},
  {"k": "Mild, no organ involvement", "tone": "first", "points": ["Potent topical steroid under specialist care; monitor bloods."]},
  {"k": "Organ involvement", "tone": "refer", "points": ["Hospital care; slow steroid taper over 6–12 weeks."], "rx": [{"drug": "Prednisolone (specialist)", "dose": "0.5–1 mg/kg/day", "dur": "taper over 6–12 weeks", "note": "Rapid tapers cause relapse."}]}]},
 refer={"items": [{"when": "same-day", "t": "Rash + fever + facial oedema / lymph nodes 2–8 weeks after a new high-risk drug."}, {"when": "routine", "t": "Follow-up TFT and glucose for 1–2 years (late autoimmunity)."}]},
 quiz=[{"q": "What is the typical latency of DRESS?", "a": "2–8 weeks after starting the drug."}, {"q": "Name three common culprits.", "a": "Allopurinol, carbamazepine (and other aromatic anticonvulsants), sulfonamides/dapsone, minocycline."}, {"q": "Which organ is most often involved?", "a": "The liver."}, {"q": "Why taper steroids slowly?", "a": "Rapid tapers cause relapse (linked to herpesvirus reactivation)."}])
steps('agep', manage={"lead": "Stop the drug; it settles in 1–2 weeks.", "rungs": [
  {"k": "Stop and record", "tone": "base", "points": ["Stop the culprit; record allergy; Yellow Card."]},
  {"k": "Symptom control", "tone": "first", "points": ["Potent topical steroid, emollients, antipyretics."]},
  {"k": "Unwell", "tone": "refer", "points": ["Same-day dermatology or admission."]}]},
 refer={"items": [{"when": "same-day", "t": "Widespread pustules with fever within days of a new drug."}]},
 quiz=[{"q": "What is the typical latency of AGEP after an antibiotic?", "a": "Under 48 hours."}, {"q": "Which cytokine drives the neutrophils in AGEP?", "a": "IL-8 (CXCL8)."}, {"q": "Main differential?", "a": "Generalised pustular psoriasis."}, {"q": "How does AGEP resolve?", "a": "Over 1–2 weeks with collarette desquamation after stopping the drug."}])
retire('dress-agep', 'DRESS & AGEP (severe drug reactions)', 'This topic has been split into two pages.', ['dress', 'agep'])

# ---------- vascular birthmarks
page('infantile-haemangioma', base='vascular-birthmarks', title='Infantile haemangioma (strawberry mark)', order=4, card_image='m6w1:G01',
 aka=['infantile haemangioma', 'strawberry naevus', 'strawberry mark', 'haemangioma', 'PHACE', 'propranolol', 'timolol'],
 summary='A benign vascular tumour that appears in the first weeks, grows fast for a few months, then slowly involutes. Refer high-risk sites early (ideally by about 4 weeks), while propranolol works best.',
 what=["An **infantile haemangioma (IH)** is a benign vascular **tumour** of infancy. It is absent or a faint mark at birth, **grows rapidly** (mostly in the first 1–3 months, largely complete by about 5 months), plateaus, then **involutes** over years. About **4–10%** of infants are affected."],
 cause=[L("Clonal endothelial proliferation, **GLUT-1 positive** (unlike malformations and congenital haemangiomas).", "Risk factors: prematurity, low birth weight, female sex, multiple pregnancy, placental anomalies.")],
 features=[T(["Type", "Appearance"], ["Superficial", "Bright red, raised, well-defined (‘strawberry’)"], ["Deep", "Bluish, rubbery swelling under the skin"], ["Mixed", "Both"]),
           "Haemangiomas can occur anywhere, most often on the head and neck. **5 or more** skin haemangiomas raise concern for **liver haemangiomas**. White surface change can herald **ulceration**.",
           {"figure": {"ai": "haemangioma-natural-history.jpg", "caption": "Natural history of infantile haemangioma: appearance (0–2 weeks), rapid growth (1–6 months), slow involution, and completion (5–7+ years)."}}],
 diagnosis=[L("Usually **clinical**.", "Ultrasound if deep, or uncertain against a malformation or soft-tissue mass. MRI for complex facial or segmental lesions.", "Abdominal ultrasound if there are 5 or more skin lesions.")],
 differentials=[T(["Look-alike", "Distinguishing clues"], ["**Port-wine stain** (see [Port-wine stain](condition:port-wine-stain))", "Present at birth, flat, **grows with the child**, no rapid tumour growth"], ["Congenital haemangioma", "Fully formed at birth; different natural history"], ["Venous or lymphatic malformation", "Soft, compressible, persistent; imaging differs"], ["Pyogenic granuloma", "Later onset; often a pedunculated bleeding papule"])],
 management=[H("Uncomplicated small haemangioma"), "Active observation with **photo documentation**. Reassure parents about involution.",
             H("Refer promptly (ideally by about 4 weeks of age if high risk)"),
             L("**Periocular** (risk to vision and amblyopia)", "**Beard or airway** distribution (risk of stridor)", "**Lip or perioral** (feeding)", "Nasal tip, large facial, or **segmental** (PHACE risk with large facial segmental lesions)", "**Perineal or flexural** (ulceration)", "**Ulcerated, bleeding or rapidly enlarging**", "**5 or more** skin lesions", "Breast (girls) or large scalp lesions"),
             H("Specialist treatment"),
             L("Oral **propranolol** is first line for problematic IH. It is started and supervised by a specialist, with heart rate, BP and glucose monitoring. Feed regularly, and **hold doses if the baby is unwell or not feeding**.", "Topical **timolol** for selected small, thin, superficial lesions (off-label; NICE ESUOM47).", "Wound care, analgesia and antibiotics for ulceration; laser or surgery for selected residual changes.")],
 red_flags=["High-risk haemangioma sites (listed above): **do not wait to see if it goes away**.", "Stridor or noisy breathing with a beard-area haemangioma: **urgent**.", "Ulcerated or bleeding haemangioma."],
 pearls=["The rapid growth window is early, so **late referral misses the easiest window for treatment**.", "IP role: recognise high-risk sites, explain that beta-blockers are specialist-supervised, and support dressings for ulceration under the specialist plan.", "BAD patient leaflet and the Birthmark Support Group are useful for families."],
 photos=[{"title": "Infantile haemangioma: proliferating, involuting, high-risk sites", "items": ["m6w1:G01", "m6w1:G04", "m6w1:G03", "m6w1:G02"]}],
 refs=[("DermNet: Infantile haemangioma", "https://dermnetnz.org/topics/infantile-haemangioma"), ("PCDS: Strawberry naevus", "https://www.pcds.org.uk/clinical-guidance/strawberry-naevus-syn.-haemangioma-of-infancy"), ("NICE ESUOM47: Topical timolol", "https://www.nice.org.uk/advice/esuom47")])

page('port-wine-stain', base='vascular-birthmarks', title='Port-wine stain (capillary malformation)', order=5, card_image='m6w1:G16',
 aka=['port-wine stain', 'capillary malformation', 'naevus flammeus', 'Sturge-Weber', 'Klippel-Trénaunay', 'vascular birthmark'],
 summary='A flat red or purple capillary malformation present at birth that grows with the child and never involutes. Facial V1 stains need assessment for Sturge–Weber syndrome; pulsed dye laser is specialist.',
 what=["A **port-wine stain (PWS)** is a **capillary malformation**: present at birth as a flat red or purple patch, it **grows in proportion with the child**, may darken and thicken with age, and **never involutes**. It affects about **0.3%** of newborns."],
 cause=["Dilated, malformed dermal capillaries, usually from a **somatic mosaic GNAQ** mutation; reduced nerve supply to the vessels lets them dilate progressively."],
 features=[L("Flat, well-demarcated pink, red or purple patch, often unilateral and following a dermatome-like segment.", "With age: darker colour, thickening and **cobblestone** nodules (vascular blebs), soft-tissue overgrowth.", "Blanches partly on pressure; does not grow out of proportion.")],
 diagnosis=["Clinical. MRI brain and eye review for facial V1 stains (Sturge–Weber); limb imaging and leg-length check for limb stains with overgrowth."],
 differentials=[T(["Look-alike", "Distinguishing clues"], ["**Salmon patch** (naevus simplex)", "Pale pink, midline (nape, glabella, eyelids); fades in the first years"], ["**Infantile haemangioma** (see [Infantile haemangioma](condition:infantile-haemangioma))", "Absent or faint at birth, then rapid growth and involution"], ["Venous malformation", "Blue, compressible, swells when dependent"])],
 management=[L("Reassure for small, uncomplicated stains; camouflage cosmetics.", "**Pulsed dye laser** is specialist, and earlier childhood referral is often preferred.", "**Facial PWS in the V1 distribution: consider Sturge–Weber** (neurology and ophthalmology for glaucoma and seizures).", "**Limb PWS with overgrowth: consider Klippel–Trénaunay** and related syndromes.")],
 red_flags=["Facial segmental port-wine stain with eye or neurological symptoms (seizures, glaucoma).", "Limb asymmetry or overgrowth."],
 pearls=["A malformation is not a tumour: be clear with parents whether it is a PWS or a haemangioma.", "PWS does not fade; salmon patches do."],
 photos=[{"title": "Port-wine stain (capillary malformation)", "items": ["m6w1:G16", "m6w1:G17"]}],
 refs=[("DermNet: Capillary vascular malformation", "https://dermnetnz.org/topics/capillary-vascular-malformation"), ("BAD PIL: Port wine stains", "https://www.bad.org.uk/pils/port-wine-stains/")])

steps('infantile-haemangioma', manage={"lead": "Watch most; refer high-risk ones early.", "rungs": [
  {"k": "Uncomplicated", "tone": "base", "points": ["Active observation with photographs; reassure."]},
  {"k": "Small superficial (specialist)", "tone": "first", "points": ["Topical timolol (off-label; NICE ESUOM47)."]},
  {"k": "Problematic / high-risk", "tone": "refer", "points": ["Oral propranolol, specialist-initiated with monitoring; hold doses if not feeding or unwell."]}]},
 refer={"items": [{"when": "urgent", "t": "Periocular, airway/beard, lip, nasal tip, segmental facial, perineal, ulcerated or ≥5 lesions: refer ideally by about 4 weeks of age."}, {"when": "same-day", "t": "Stridor with a beard-area haemangioma."}]},
 quiz=[{"q": "When does most haemangioma growth occur?", "a": "In the first 1–3 months; largely complete by about 5 months."}, {"q": "Which marker distinguishes IH from malformations?", "a": "GLUT-1."}, {"q": "What does ≥5 skin haemangiomas prompt?", "a": "Abdominal (liver) ultrasound."}, {"q": "First-line systemic treatment?", "a": "Oral propranolol, started by a specialist."}])
steps('port-wine-stain', manage={"lead": "Reassure; screen facial and limb stains; laser is specialist.", "rungs": [
  {"k": "Reassure", "tone": "base", "points": ["Explain permanence; camouflage."]},
  {"k": "Laser", "tone": "refer", "points": ["Pulsed dye laser via specialist; earlier childhood treatment often preferred."]}]},
 refer={"items": [{"when": "urgent", "t": "Facial V1 stain: ophthalmology (glaucoma) and neurology (Sturge–Weber)."}, {"when": "routine", "t": "Limb stain with overgrowth or asymmetry."}]},
 quiz=[{"q": "Does a port-wine stain fade?", "a": "No; it grows with the child and may darken and thicken."}, {"q": "Which mutation is usually responsible?", "a": "Somatic mosaic GNAQ."}, {"q": "Which syndrome must be considered with a V1 facial stain?", "a": "Sturge–Weber syndrome."}, {"q": "How is a salmon patch different?", "a": "Pale, midline and fades in early childhood."}])
retire('vascular-birthmarks', 'Infantile haemangioma & port-wine stain', 'This topic has been split into two pages.', ['infantile-haemangioma', 'port-wine-stain'])

# ---------- ulcers
page('arterial-leg-ulcer', base='arterial-neuropathic-ulcers', title='Arterial (ischaemic) leg ulcer', order=3, card_image='m5w2:S01',
 aka=['arterial ulcer', 'ischaemic ulcer', 'peripheral arterial disease', 'PAD', 'critical limb ischaemia'],
 summary='Punched-out, painful, distal ulcers from peripheral arterial disease. Never compress an ischaemic limb; refer urgently to vascular, same day for critical limb ischaemia.',
 what=["An **arterial ulcer** is skin loss caused by tissue **ischaemia** from peripheral arterial disease. It accounts for about 10–20% of leg ulcers, alone or mixed with venous disease."],
 cause=["Atherosclerosis (or embolism) reduces flow, so poorly perfused sites become necrotic after minor trauma. Risk factors: smoking, diabetes, hypertension, hyperlipidaemia, CKD and age."],
 features=[L("Site: toes, heel, bony prominences, lateral malleolus, shin.", "**Punched-out**, deep, dry or necrotic base.", "Pain often **severe**, worse on elevation and at night (eased by hanging the leg out of bed).", "Foot: cold, pale or mottled, shiny, hairless, weak or absent pulses; dependent rubor; **claudication**.")],
 diagnosis=[L("Examine pulses and measure **ABPI** (or TBPI in diabetes, where calcified vessels give falsely high ABPI).", "Urgent vascular assessment (duplex, angiography) for critical limb ischaemia.")],
 differentials=["[Venous leg ulcer](condition:venous-leg-ulcer) (gaiter area, shallow, exudative), [diabetic foot ulcer](condition:diabetic-foot-ulcer), pressure ulcer, [pyoderma gangrenosum](condition:pyoderma-gangrenosum), vasculitis, malignancy."],
 management=[L("**Do not compress** ischaemic limbs.", "Urgent **vascular referral**, especially with rest pain, gangrene or critical ischaemia.", "Risk factors: stop smoking, antiplatelet and statin therapy (NICE CG147 and vascular advice); optimise blood pressure and diabetes.", "Analgesia, and wound care directed by tissue viability or vascular.")],
 red_flags=["**Critical limb ischaemia:** rest pain, gangrene, tissue loss, or a cold pulseless foot: **same-day vascular**.", "Acute limb ischaemia (pain, pallor, pulselessness, paraesthesia, paralysis, perishingly cold): emergency."],
 pearls=["**Any leg ulcer may be mixed.** Always assess the arterial supply before compression.", "Painful ulcer worse on elevation suggests arterial."],
 photos=[{"title": "Ischaemic ulcers", "items": ["m5w2:S01"]}],
 refs=[("NICE CG147: Peripheral arterial disease", "https://www.nice.org.uk/guidance/cg147"), ("DermNet: Arterial ulcer", "https://dermnetnz.org/topics/arterial-ulcer")])

page('diabetic-foot-ulcer', base='arterial-neuropathic-ulcers', title='Neuropathic and diabetic foot ulcers', order=4, card_image='m5w2:S03',
 aka=['neuropathic ulcer', 'diabetic foot ulcer', 'diabetic foot', 'NG19', 'osteomyelitis', 'Charcot foot', 'neuro-ischaemic foot'],
 summary='Painless ulcers on plantar pressure points surrounded by callus, from loss of protective sensation. Any diabetic foot ulcer needs referral to the foot care service within 1 working day (NICE NG19).',
 what=["A **neuropathic ulcer** follows loss of **protective sensation**, with or without deformity and ischaemia (‘neuro-ischaemic’ foot). Most are **diabetic foot ulcers**, a leading cause of amputation."],
 cause=["Peripheral neuropathy (usually diabetes; also alcohol, B12 deficiency, leprosy) means repetitive trauma goes unnoticed. Deep ulcers can reach bone, with a risk of **osteomyelitis**."],
 features=[L("Site: **plantar** metatarsal heads, heel, tips of toes, under bunions.", "Deep, punched-out, surrounded by **callus**; may reach bone.", "Often **painless**; warm foot with good pulses (unless neuro-ischaemic).", "Clawed toes, Charcot deformity, dry fissured skin.")],
 diagnosis=[L("Test sensation with a **10 g monofilament** and vibration.", "Pulses and ABPI/TBPI (neuro-ischaemic foot).", "**Probe to bone**, plus X-ray or MRI if osteomyelitis is suspected.", "Deep tissue samples rather than surface swabs if infected.")],
 differentials=["[Arterial ulcer](condition:arterial-leg-ulcer), pressure ulcer (immobile or paraplegic patients), [venous ulcer](condition:venous-leg-ulcer), malignancy (non-healing)."],
 management=[L("**Any diabetic foot ulcer:** refer urgently to the **multidisciplinary foot care service** or foot protection service (within 1 working day, NICE NG19).", "**Offloading**, glycaemic optimisation, debridement, and assessment for infection, which may need admission and IV antibiotics.", "Diabetic foot infection: follow NICE NG19 and local antimicrobial guidance.")],
 red_flags=["Diabetic foot with **spreading redness, fever, crepitus or wet necrosis**: **ED / same-day admission**.", "Probe to bone, or suspected osteomyelitis or **Charcot foot** (hot, swollen foot in neuropathy).", "**Never ignore a ‘small’ plantar ulcer in diabetes.**"],
 pearls=["Teach **daily foot checks**, sensible footwear and podiatry follow-up; never walk barefoot with neuropathy.", "Painless ulcer under a callus suggests neuropathic."],
 photos=[{"title": "Neuropathic plantar / pressure ulcers", "items": ["m5w2:S03", "m5w2:S04", "m5w2:S05", "m5w2:S02"]}],
 refs=[("NICE NG19: Diabetic foot problems", "https://www.nice.org.uk/guidance/ng19"), ("DermNet: Diabetic foot ulcer", "https://dermnetnz.org/topics/diabetic-foot-ulcer")])

steps('arterial-leg-ulcer', manage={"lead": "Revascularise; never compress.", "rungs": [
  {"k": "Risk factors", "tone": "base", "points": ["Stop smoking; antiplatelet and statin per NICE CG147; optimise BP and diabetes."]},
  {"k": "Wound care", "tone": "first", "points": ["Analgesia; dry, protective dressings guided by tissue viability."]},
  {"k": "Vascular", "tone": "refer", "points": ["Urgent vascular assessment for revascularisation."]}],
  "limits": [{"k": "Compression", "t": "Contraindicated in significant arterial disease (low ABPI).", "tone": "danger"}]},
 refer={"items": [{"when": "same-day", "t": "Rest pain, gangrene, tissue loss or a cold pulseless foot."}, {"when": "urgent", "t": "Any suspected arterial ulcer: vascular surgery."}]},
 quiz=[{"q": "Where do arterial ulcers occur?", "a": "Toes, heel, bony prominences, lateral malleolus."}, {"q": "Why can ABPI mislead in diabetes?", "a": "Calcified vessels give falsely high readings; use toe pressures (TBPI)."}, {"q": "What eases ischaemic rest pain?", "a": "Hanging the leg down (dependency)."}, {"q": "What must you never do?", "a": "Apply compression to an ischaemic limb."}])
steps('diabetic-foot-ulcer', manage={"lead": "Refer within 1 working day; offload.", "rungs": [
  {"k": "Prevention", "tone": "base", "points": ["Daily foot checks, footwear, podiatry; glycaemic control."]},
  {"k": "Any ulcer", "tone": "refer", "points": ["Multidisciplinary foot care service within 1 working day; offloading, debridement."]},
  {"k": "Infected", "tone": "refer", "points": ["Antibiotics per NICE NG19 and local guidance; admit if severe."]}]},
 refer={"items": [{"when": "same-day", "t": "Spreading infection, fever, crepitus, wet necrosis or suspected Charcot foot."}, {"when": "urgent", "t": "Any diabetic foot ulcer (within 1 working day)."}]},
 quiz=[{"q": "How is protective sensation tested?", "a": "10 g monofilament (plus vibration)."}, {"q": "What does a positive probe-to-bone test suggest?", "a": "Osteomyelitis."}, {"q": "How quickly should a diabetic foot ulcer be referred?", "a": "Within 1 working day to the foot care service (NG19)."}, {"q": "What is a hot swollen foot in neuropathy until proven otherwise?", "a": "Charcot neuroarthropathy."}])
retire('arterial-neuropathic-ulcers', 'Arterial & neuropathic ulcers', 'This topic has been split into two pages.', ['arterial-leg-ulcer', 'diabetic-foot-ulcer'])
print('part1 ok')
