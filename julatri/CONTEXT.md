# Abhidhamma Julatri (อภิธรรมชั้นจูฬตรี)

An interactive study site for the จูฬตรี level of the Thai Abhidhamma curriculum (อภิธรรมโชติกะวิทยาลัย), covering จิต-เจตสิก classification and the three nayas from ปริจเฉทที่ ๒ of the Abhidhammatthasangaha. Primary source: the official จูฬตรี textbook ("ปรมัตถโชติกะ ปริจเฉทที่ ๑-๒-๖" by พระสัทธัมมโชติกะ ธัมมาจริยะ, มูลนิธิสัทธัมมโชติกะ).

## Language

**จิต (Citta)**:
A moment of consciousness. Classified into 89 (or 121, พิสดาร-expanded) types across kāmāvacara, rūpāvacara, arūpāvacara, and lokuttara realms. This project uses 121: standard for kāmāvacara/rūpāvacara/arūpāvacara, พิสดาร-expanded for โลกุตตรจิต (see below) — 121 total.

**เจตสิก (Cetasika)**:
A mental factor that arises together with a citta, sharing its object, base, arising, and ceasing. There are 52, grouped into อัญญสมานาเจตสิก (13), อกุศลเจตสิก (14), and โสภณเจตสิก (25).

**อกุศลจิต**:
The 12 unwholesome cittas (โลภมูลจิต 8, โทสมูลจิต 2, โมหมูลจิต 2).

**อเหตุกจิต**:
The 18 "rootless" cittas — no hetu (root) cetasika present. Includes the 10 dvi-pañca-viññāṇa (bare sense-consciousness), sampaṭicchana, santīraṇa, the two āvajjana, and hasituppāda (the Arahant's smile-producing citta).

**กามาวจรโสภณจิต**:
The 24 "beautiful" sense-sphere cittas: 8 มหากุศล (active wholesome), 8 มหาวิปาก (their resultants), 8 มหากิริยา (the same pattern as functional-only, for Arahants).

**มหัคคตจิต**:
The 27 "exalted" cittas of jhāna attainment: 15 รูปาวจร (5 rūpa-jhāna levels × kusala/vipāka/kiriya) + 12 อรูปาวจร (4 arūpa levels × kusala/vipāka/kiriya).

**โลกุตตรจิต**:
The supramundane cittas (4 magga + 4 phala). This project uses the 121-system's พิสดาร (elaborated) form — each of the 8 expanded into 5 jhāna-factor levels, 40 cittas total — not the abbreviated (ย่อ) 8-citta form.

**สัมปโยคนัย (Sampayoga-naya)**:
The method that takes each เจตสิก in turn and lists every จิต it can arise in (cetasika → citta direction). Correct spelling confirmed against the official textbook (chapter heading, p. 40).
_Avoid_: สัมโยคนัย (common misspelling, missing the ป)

**สังคหนัย (Sangaha-naya)**:
The method that takes each จิต in turn and lists every เจตสิก that arises in it (citta → cetasika direction). The reverse mapping of สัมปโยคนัย, over the same underlying data.

**ตทุภยมิสสกนัย (Tadubhaya-missaka-naya)**:
The method that, for a given เจตสิก, finds every *other* เจตสิก that can co-occur with it in the same จิต. Derived by composing สัมปโยคนัย (get the citta set for the cetasika) with สังคหนัย (get the cetasika set for each of those cittas), then taking the union minus itself. Answers a cetasika↔cetasika question, not a citta↔cetasika one.
_Avoid_: มิสสกสังคหะ (a different, unrelated จูฬโท concept — a category in the four-fold sammuccaya list, not this pairing method)

## Data model

All three nayas are computed views over a single underlying dataset: the set of citta↔cetasika edges (which เจตสิก occur in which จิต). สัมปโยคนัย and สังคหนัย are the two directional traversals of that edge set; ตทุภยมิสสกนัย is a second-order relation (cetasika↔cetasika) derived from composing both traversals. The edges are authored once; all three views are computed, not separately maintained.

All 121 cittas (89 kāma/rūpa/arūpa + 40 พิสดาร-expanded lokuttara) and all 52 cetasikas are entered, verified against the official textbook's per-citta tables (pp. 50-56) and cross-checked against its summary diagram (p. 56).

Array order within each group in `data/cittas.yaml` determines row layout in the UI (`CITTA_GROUPS` in `js/app.js`, via each group's `rows` or `chunkSize`) — it's not arbitrary. อเหตุกจิต renders as 3 uneven rows (7/8/3, by resultant-type, matching the textbook's own grouping — not "all 10 dvi-pañca-viññāṇa first"). รูปาวจร/อรูปาวจร/โลกุตตร render as even rows grouped by kind/stage first and jhāna-level second (matching the textbook's summary diagram, p. 56), so their YAML entries are ordered kind-major / stage-major, not jhāna-level-major.
