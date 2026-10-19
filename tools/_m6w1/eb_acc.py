import json
from pathlib import Path
C = Path("/workspace/derm-teach/website/content/conditions")

# ---------------- EB
P = C / "epidermolysis-bullosa.json"
d = json.loads(P.read_text())
d["aka"] = d["aka"] + ["Kindler EB", "RDEB", "COL7A1", "DEBRA"]
d.update({
 "status": "published",
 "module": "Module 6 · Week 1: epidermolysis bullosa",
 "summary": "A group of inherited disorders in which skin (and often mucosa) blisters with minimal friction. Primary care recognises it, handles the baby safely and refers urgently to a specialist EB centre. Long-term care is MDT-led, with the IP supporting dressings, pain, nutrition and medicines.",
 "card_image": "m6w1:H01",
 "hero": {"ai": "eb-skin-fragility.jpg", "alt": "AI diagram of the level of skin split in EB simplex, junctional and dystrophic EB compared with normal skin"},
 "glance": {
  "think": "A newborn or infant with **blisters or raw areas from ordinary handling**, at friction sites, ± absent skin at birth, nail changes or mouth blisters. Or a toddler whose feet blister when they start walking.",
  "engine": "Faulty **adhesion proteins** (keratins, laminin-332, type VII collagen, kindlin-1) let the skin split at a set level under minor shear.",
  "backbone": "**Urgent referral to a specialist EB service.** Meanwhile: no adhesives, gentle lifting, non-adherent silicone dressings, pain relief, and family support (DEBRA UK).",
  "never_miss": "Hoarse cry or stridor (airway involvement in junctional EB), dehydration or sepsis in a blistering neonate, and a **changing chronic wound in recessive dystrophic EB** (squamous cell carcinoma)."
 },
 "sections": {
  "what": [
   "**Epidermolysis bullosa (EB)** is a group of rare **inherited ‘mechanobullous’ disorders**. The skin, and often the mucous membranes, blister or shear off after minimal friction or trauma (‘butterfly skin’). Severity ranges from blisters on the feet after a long walk to life-limiting widespread disease.",
   "It is classified by the **level at which the skin splits**:",
   {"table": {"head": ["Type", "Level of split", "Key protein (examples)", "Clinical gist"], "rows": [
    ["**EB simplex** (most common)", "Within the epidermis (basal keratinocytes)", "Keratins 5 and 14", "Often milder; localised hand and foot blisters, worse in heat. Usually heals without scarring"],
    ["**Junctional EB**", "Lamina lucida of the basement membrane", "Laminin-332, collagen XVII, integrin α6β4", "Severe forms present at birth with widespread erosions, mouth and airway involvement. Can be life-limiting"],
    ["**Dystrophic EB**", "Below the lamina densa", "**Type VII collagen (COL7A1)**", "Heals with **scarring and milia**. Recessive form (RDEB) causes mitten deformity, strictures and a high **SCC** risk"],
    ["**Kindler EB**", "Mixed levels", "Kindlin-1", "Blistering in infancy, then photosensitivity and poikiloderma"]
   ]}},
   "Do not confuse with **EB acquisita**, an autoimmune blistering disease of adults."
  ],
  "cause": [
   {"list": [
    "Mutations in genes for the proteins that **anchor the skin layers together**. When they are missing or faulty, ordinary shear forces tear the skin at that level.",
    "Inheritance is **autosomal dominant or recessive** depending on subtype. Recessive dystrophic EB (COL7A1) is the classic severe scarring form.",
    "Repeated wounding and healing drives **chronic inflammation, scarring and fibrosis**. In RDEB this leads to fused fingers and toes, oesophageal strictures and aggressive cutaneous **squamous cell carcinoma** in chronic wounds, often from adolescence or early adulthood.",
    "Heat, sweating, friction and poorly fitting footwear worsen blistering, especially in EB simplex."
   ]}
  ],
  "features": [
   {"list": [
    "**Blisters and erosions at friction sites:** hands, feet, knees, elbows, nappy area, beltline. They may be present **at birth** or appear with handling, feeding, crawling or walking.",
    "Areas of **absent skin at birth**, often on the lower legs (EB with congenital absence of skin, Bart syndrome; see [Aplasia cutis congenita](condition:aplasia-cutis)).",
    "**Nail dystrophy** or loss; **milia** and **atrophic scars** at healed sites (especially dystrophic EB).",
    "**Mucosal involvement:** mouth blisters and feeding difficulty, oesophageal blistering and strictures (dysphagia), eye erosions, and a **hoarse cry or stridor** in junctional EB.",
    "Severe RDEB: chronic non-healing wounds, **mitten deformity** of hands and feet, anaemia, poor growth, dental disease, constipation and chronic pain and itch.",
    "**Localised EB simplex** often first shows up when the child starts walking: blisters on the soles, worse in summer."
   ]}
  ],
  "diagnosis": [
   {"list": [
    "Primary care makes the **clinical suspicion**, not the subtype. Any neonate or infant with unexplained blistering or fragility should be treated as possible EB until a specialist says otherwise.",
    "Ask about **family history** of fragile skin or blistering, and consanguinity.",
    "Definitive diagnosis is at a **specialist EB centre**: a skin biopsy of a fresh, induced blister for **immunofluorescence mapping** and/or electron microscopy, plus **genetic testing**.",
    "Exclude infection on the same pathway (bacterial swabs, HSV PCR) because blistering neonates may have infection instead of, or as well as, EB."
   ]},
   {"callout": "info", "title": "UK specialist EB services", "text": "The UK has nationally commissioned EB centres for children (e.g. **Great Ormond Street** and **Birmingham Children’s Hospital**) and adults, working with **DEBRA UK** nurses and support workers. A suspected new case is usually discussed directly with the on-call dermatology team."}
  ],
  "differentials": [
   {"table": {"head": ["Look-alike", "Distinguishing clues"], "rows": [
    ["Sucking blisters", "One or two blisters on the hand, wrist or lip of a well newborn. No new blisters with handling"],
    ["Friction blisters", "Clear cause, localised, no family history, normal skin elsewhere"],
    ["[Bullous impetigo](condition:impetigo) / staphylococcal scalded skin", "Infection signs, flaccid blisters, crust; SSSS is tender, red and peels widely. Swab"],
    ["Neonatal HSV or varicella", "Grouped vesicles or punched-out erosions, unwell baby. Urgent PCR and antivirals"],
    ["Incontinentia pigmenti", "Usually girls. Linear vesicles along **Blaschko’s lines**, then warty, then pigmented stages"],
    ["Bullous mastocytosis", "Blisters over thickened, yellow-brown skin; Darier’s sign (urticates when rubbed)"],
    ["Neonatal autoimmune blistering (maternal pemphigus or pemphigoid antibodies)", "Mother has the disease; transient and self-resolving"],
    ["Burns, scalds or non-accidental injury", "Pattern and history. EB must be considered before assumptions are made, but follow safeguarding procedures if the picture does not fit"]
   ]}}
  ],
  "management": [
   "**EB is a specialist, multidisciplinary condition.** The pharmacist or IP’s job is early recognition, safe interim handling, and supporting the specialist plan in the community.",
   {"h": "At first suspicion"},
   {"ol": [
    "**Refer urgently** to paediatric dermatology or the regional EB service. For a neonate, this is a same-day discussion.",
    "**Handle gently:** lift the baby on a soft pad or sheet, supporting the bottom and neck. Do not lift under the arms. Avoid rubbing, and keep the baby cool.",
    "**No adhesive tapes, plasters, ECG dots or wristbands on the skin.** Use soft silicone tapes and dressings only, and pad the cot sides.",
    "Leave blisters intact unless trained. EB nurses teach **lancing with a sterile needle** to drain fluid (preventing spread), leaving the roof as a natural dressing.",
    "Cover erosions with **non-adherent dressings** (soft silicone, lipido-colloid or petrolatum gauze) and a soft retention bandage. Lubricate with white soft paraffin.",
    "Assess **feeding** (mouth blisters), **pain** and signs of **infection** or dehydration."
   ]},
   {"h": "Ongoing community support (under the specialist plan)"},
   {"list": [
    "**Dressings and emollients:** prescribe the specialist-recommended silicone and non-adherent products and quantities. Large, regular supplies are normal. Avoid substitutions without checking with the EB team.",
    "**Pain and itch:** regular analgesia, and pre-emptive analgesia before dressing changes as advised. Itch is a major burden; follow the specialist plan for emollients and antihistamines.",
    "**Infection:** colonisation is common. Treat **clinically significant infection** after discussion with the EB team; avoid long courses of topical antibiotics. Swab before treating.",
    "**Nutrition and gut:** dietitian input, iron and vitamin supplements, laxatives for constipation, and **liquid or dispersible formulations** if there are oral or oesophageal strictures.",
    "**Medicines optimisation:** avoid rectal routes where possible, check interactions, and choose formulations that do not need swallowing large tablets.",
    "**Specialist wound therapy (awareness):** birch triterpenes gel (**Filsuvez**, Oleogel-S10) is licensed for partial-thickness wounds in junctional and dystrophic EB and is started by specialists.",
    "**RDEB:** support **regular skin surveillance**. Any wound that changes, grows, becomes painful or fails to heal needs urgent dermatology review for SCC.",
    "**Families:** signpost **DEBRA UK** early. Genetic counselling for future pregnancies is arranged by the specialist service."
   ]},
   {"callout": "tip", "title": "Practical advice for milder EB simplex", "list": [
    "Soft, well-fitting, breathable footwear and moisture-wicking socks. Keep feet cool.",
    "Drain new blisters with a sterile needle and keep the roof on; cover with a non-adherent dressing.",
    "Plan for worse blistering in hot weather and with new activities."
   ]}
  ],
  "red_flags": [
   "**Any neonate or infant with unexplained skin fragility or blistering:** urgent specialist referral (same day for neonates).",
   "**Hoarse cry, stridor or breathing difficulty** (airway involvement in junctional EB): emergency.",
   "Poor feeding, **dehydration**, weight loss or failure to thrive.",
   "Fever, spreading redness, or an unwell baby or child: possible **sepsis**.",
   "New **dysphagia** or food sticking (oesophageal stricture).",
   "In recessive dystrophic EB: a **wound that changes**, enlarges, becomes heaped-up or painful, or will not heal. Urgent review for **squamous cell carcinoma**."
  ],
  "pearls": [
   "**Think EB in any blistering neonate**, but exclude infection at the same time.",
   "‘No sticky things on the skin’ is the most useful single instruction for any team caring for a baby with suspected EB.",
   "Pop and drain, don’t de-roof: the blister roof is the best dressing.",
   "Dressing and emollient prescriptions are large and ongoing. Make sure repeat systems and formulary teams know the patient.",
   "**Never assume rough handling** without considering genuine skin fragility, but do not let the diagnosis close down safeguarding thinking.",
   "Even mild EB simplex benefits from a confirmed diagnosis, which guides footwear, activities and genetic advice.",
   "**Skin of colour:** redness is subtler. Look for erosions, milia, scarring and post-inflammatory pigment change."
  ]
 },
 "photos": [
  {"title": "Neonatal and generalised EB", "items": ["m6w1:H01", "m6w1:H02"]},
  {"title": "Acral and friction-site blistering", "items": ["m6w1:H03"]},
  {"title": "Recessive dystrophic EB: scarring and milia", "tone": "danger", "items": ["m6w1:H04"]},
  {"title": "AI teaching illustration", "items": [{"ai": "eb-skin-fragility.jpg", "caption": "Level of the split in EB simplex, junctional and dystrophic EB compared with normal skin."}]}
 ],
 "references": [
  {"label": "DermNet: Epidermolysis bullosa", "url": "https://dermnetnz.org/topics/epidermolysis-bullosa"},
  {"label": "DermNet: EB with congenital absence of skin", "url": "https://dermnetnz.org/topics/epidermolysis-bullosa-with-congenital-absence-of-skin"},
  {"label": "Great Ormond Street Hospital: Epidermolysis bullosa", "url": "https://www.gosh.nhs.uk/conditions-and-treatments/conditions-we-treat/epidermolysis-bullosa/"},
  {"label": "DEBRA UK", "url": "https://www.debra.org.uk/"},
  {"label": "BNF: Birch bark extract (Filsuvez)", "url": "https://bnf.nice.org.uk/"}
 ]
})
d.pop("planned", None)
P.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")

# ---------------- ACC
P = C / "aplasia-cutis.json"
d = json.loads(P.read_text())
d["aka"] = d["aka"] + ["Adams–Oliver syndrome", "Bart syndrome", "membranous aplasia cutis", "carbimazole embryopathy"]
d.update({
 "status": "published",
 "module": "Module 6 · Week 1: aplasia cutis congenita",
 "summary": "A baby born with a sharply defined patch of missing skin, usually on the scalp vertex. Small superficial lesions heal with bland wound care to a hairless scar. Large, deep, midline or hair-collar lesions need imaging and specialist care.",
 "card_image": "m6w1:H05",
 "glance": {
  "think": "A well-demarcated **ulcer, erosion, shiny membrane or scar on the scalp at birth**, usually near the vertex, with no hair growing in it.",
  "engine": "Localised failure of skin development in utero. Causes include genetics, vascular disruption, amniotic bands, intrauterine infection and teratogens such as **carbimazole/methimazole**.",
  "backbone": "Bland, protective wound care for small lesions. **Image and refer** when the lesion is large, deep, midline, multiple or has a hair collar.",
  "never_miss": "**Hair collar sign** (possible underlying neural tissue or skull defect), deep defects over the sagittal sinus (bleeding, infection), and associated limb, heart or blistering problems."
 },
 "sections": {
  "what": [
   "**Aplasia cutis congenita (ACC)** is the congenital, localised **absence of skin**. The depth varies from epidermis only to full-thickness defects through to skull bone and dura.",
   {"list": [
    "About **70–80%** are a **solitary lesion on the scalp vertex**, near the hair whorl. Less commonly on the trunk or limbs.",
    "Defects present at birth may be **healed in utero** (atrophic, hairless scar), a **raw ulcer or erosion**, or a thin shiny **membrane** (membranous ACC).",
    "Most cases are isolated and heal well. A minority are part of a **syndrome** or have an underlying defect."
   ]}
  ],
  "cause": [
   "ACC has **many causes**, and often none is found:",
   {"list": [
    "**Genetic:** familial forms, and syndromes such as **Adams–Oliver** (scalp ACC with limb defects ± heart and vascular anomalies), trisomy 13 and others.",
    "**Vascular disruption** or placental infarcts, a co-twin death (fetus papyraceus), and **amniotic bands**.",
    "**Intrauterine infection:** varicella, HSV.",
    "**Teratogens:** maternal **carbimazole or methimazole** (the classic pharmacy link), and also misoprostol, valproate and cocaine.",
    "**Mechanical tension** on the scalp at the vertex during rapid fetal brain growth.",
    "**With epidermolysis bullosa:** absent skin on the legs and feet with blistering (Bart syndrome). See [Epidermolysis bullosa](condition:epidermolysis-bullosa)."
   ]}
  ],
  "features": [
   {"list": [
    "A **sharply demarcated, round, oval or stellate** area, usually 1–2 cm, on the scalp vertex at birth. It may be an erosion, ulcer, crusted area, translucent membrane or blister-like (bullous) lesion.",
    "Heals over weeks to months to a **smooth, hairless (alopecic), atrophic scar**.",
    "**Hair collar sign:** a ring of **longer, darker, coarser hair** around a scalp lesion. This marks a possible **neural tube closure defect** (ectopic neural tissue, encephalocele or meningocele).",
    "Other warning features: **large size** (>4–5 cm), **multiple** lesions, **midline** site, a **vascular stain** or swelling nearby, a **pulsating or fluctuant** lesion, or neurological signs.",
    "Trunk and limb ACC is often symmetrical and may follow a fetus papyraceus or come with EB."
   ]}
  ],
  "diagnosis": [
   {"list": [
    "**Clinical diagnosis at birth.** Document size, depth, appearance (ulcer, membrane, scar) and any hair collar, with photographs.",
    "Take a **maternal history**: antithyroid drugs (carbimazole/methimazole), other medicines, infections in pregnancy, twin pregnancy, family history of scalp defects or limb anomalies.",
    "Rule out **birth trauma** (forceps, ventouse, fetal scalp electrode) by history and appearance.",
    "Examine **limbs, heart and the rest of the skin** for associated anomalies and blistering.",
    "**Imaging** (ultrasound ± MRI, arranged by specialists) for large, deep, midline, membranous or hair-collar lesions, to look for skull and CNS defects."
   ]}
  ],
  "differentials": [
   {"table": {"head": ["Look-alike", "Distinguishing clues"], "rows": [
    ["Birth trauma (forceps, ventouse, scalp electrode)", "History of instrumental delivery or monitoring; lesion shape matches the instrument; heals with normal hair"],
    ["Neonatal HSV erosions", "Grouped vesicles or punched-out erosions, often at an electrode site, appearing after birth; baby may be unwell. Urgent"],
    ["EB with congenital absence of skin", "Absent skin on the legs or feet plus blistering elsewhere"],
    ["Naevus sebaceous", "Yellow-orange, waxy, hairless plaque on the scalp; raised, not ulcerated or atrophic"],
    ["Encephalocele, heterotopic brain tissue, sinus pericranii", "Swelling, compressibility, pulsation, hair collar sign; needs imaging"],
    ["Focal dermal hypoplasia and other genodermatoses", "Multiple linear lesions, fat herniation, other anomalies. Specialist"]
   ]}}
  ],
  "management": [
   "Most ACC is small and superficial, and heals with **simple, protective wound care**. The IP’s role is to support safe wound care, spot the lesions that need imaging, and pick up the medication history.",
   {"h": "Small, superficial, isolated scalp lesion"},
   {"list": [
    "**Gentle cleansing** with saline or water. Do not scrub or pick at crust.",
    "Keep the wound **moist** with a bland ointment such as white soft paraffin, and cover with a **non-adherent dressing** if needed.",
    "**Protect from trauma.** Avoid tight hats or headbands, and no adhesive dressings on the scalp.",
    "Use a topical antibacterial **only if clinically infected**, following local guidance. Swab first.",
    "Expect healing over weeks to months, leaving a **hairless scar**. Scar revision or tissue expansion can be considered in later childhood if the patch is noticeable."
   ]},
   {"h": "Large, deep, multiple, membranous, midline or hair-collar lesions"},
   {"list": [
    "**Urgent referral** to neonatology or paediatrics, with plastic surgery and neurosurgery input as needed.",
    "Imaging before any procedure. **Never probe** a deep scalp defect.",
    "Large defects over the vertex risk **sagittal sinus haemorrhage, thrombosis and meningitis**, and are managed with specialist dressings or grafting."
   ]},
   {"h": "Pharmacist angle"},
   {"list": [
    "Recognise the **carbimazole/methimazole** association in the maternal medication history and flag it to the specialist team. This is relevant for counselling about future pregnancies (propylthiouracil is often preferred in the first trimester).",
    "**Do not advise stopping** maternal antithyroid treatment yourself. Untreated hyperthyroidism in pregnancy is dangerous; changes are for the obstetric and endocrine team.",
    "Counsel parents that the scar and patch of hair loss are usually permanent but rarely cause problems, and that hair can be styled to cover it."
   ]}
  ],
  "red_flags": [
   "**Hair collar sign**, a swelling, or a pulsating or compressible scalp lesion: image before assuming it is ‘just a scar’.",
   "**Large (>4–5 cm), deep, or multiple** defects, especially over the midline vertex (sagittal sinus).",
   "Bleeding, discharge, fever or signs of infection or meningitis in a baby with a scalp defect.",
   "Associated **limb defects**, heart murmur or vascular anomalies (Adams–Oliver).",
   "ACC with **blistering** or absent skin on the legs (EB-associated).",
   "Neurological signs, poor feeding or an unwell baby."
  ],
  "pearls": [
   "**Hair collar = image.** It is the single most important sign to look for.",
   "Never probe a deep scalp defect.",
   "**ACC + limb defects → Adams–Oliver. ACC + blistering → EB.**",
   "Ask about **carbimazole** in pregnancy. It is a classic exam and practice link.",
   "Most small vertex lesions just need gentle, moist wound care and reassurance.",
   "**Skin of colour:** the healed scar may be hypo- or hyperpigmented. Use the absent hair and atrophy to recognise it."
  ]
 },
 "photos": [
  {"title": "Aplasia cutis congenita: scalp vertex defect at birth", "tone": "danger", "items": ["m6w1:H05"]},
  {"title": "Healed aplasia cutis: atrophic, hairless scar", "items": ["m6w1:H06"]},
  {"title": "Related: EB with fragile, absent skin", "items": ["m6w1:H01"]}
 ],
 "references": [
  {"label": "DermNet: Aplasia cutis congenita", "url": "https://dermnetnz.org/topics/aplasia-cutis"},
  {"label": "DermNet: EB with congenital absence of skin", "url": "https://dermnetnz.org/topics/epidermolysis-bullosa-with-congenital-absence-of-skin"},
  {"label": "BNF: Carbimazole (pregnancy cautions)", "url": "https://bnf.nice.org.uk/drugs/carbimazole/"}
 ]
})
d.pop("planned", None)
P.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
print("ok")
