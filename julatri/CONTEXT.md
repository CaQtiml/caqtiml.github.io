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

**กามาวจร**:
The sense-sphere realm/scope — covers อกุศลจิต, อเหตุกจิต, and กามาวจรโสภณจิต (54 cittas total). Vacanattha (ch.1): `กาเมติ = กาโม` / `กามสฺส ภโว = กาโม` (the realm where sense-desire arises, or sense-desire itself) → `กาเม อวจรตีติ = กามาวจรํ` (a citta that habitually arises in that realm). No single UI element renders "กามาวจร" itself — it's the umbrella over `lobha-mula`/`dosa-mula`/`moha-mula`/`ahetuka`/`mahakusala`/`mahavipaka`/`mahakiriya` in `CITTA_GROUPS`.

**กามาวจรโสภณจิต**:
The 24 "beautiful" sense-sphere cittas: 8 มหากุศล (active wholesome), 8 มหาวิปาก (their resultants), 8 มหากิริยา (the same pattern as functional-only, for Arahants).

**มหัคคตจิต**:
The 27 "exalted" cittas of jhāna attainment: 15 รูปาวจร (5 rūpa-jhāna levels × kusala/vipāka/kiriya) + 12 อรูปาวจร (4 arūpa levels × kusala/vipāka/kiriya). Vacanattha (ch.1, line 573): `มหนฺตํ คโตติ = มหคฺคโต` — a citta that has attained greatness/excellence. Like กามาวจร, this umbrella term (over `rupa-jhana`/`arupa-jhana` in `CITTA_GROUPS`) has no dedicated UI element of its own.

**โลกียจิต / โลกุตตรจิต**:
โลกียจิต is the 81 mundane cittas (กามาวจร 54 + มหัคคตะ 27); โลกุตตรจิต is the supramundane cittas (4 magga + 4 phala). This project uses the 121-system's พิสดาร (elaborated) form of โลกุตตรจิต — each of the 8 expanded into 5 jhāna-factor levels, 40 cittas total — not the abbreviated (ย่อ) 8-citta form. Vacanattha for โลกียะ (ch.1, line 579): `โลเก นิยุตฺตาติ = โลกิยา` — dhammas perpetually engaged in the 3 worlds (kāma/rūpa/arūpa loka). โลกียจิต itself, like กามาวจร and มหัคคตะ, has no dedicated `CITTA_GROUPS` entry — `lokuttara` is the only lokuttara/lokiya-axis group rendered directly.

**จำแนกนัย ๙ (nine classification lenses for จิต ๑๒๑)**:
ชาติ/ภูมิ/โสภณ/โลก/เหตุ/ฌาน/เวทนา/สัมปโยค/สังขารเภทนัย (ch.1, lines 639-707) — 9 ways to cut across the `CITTA_GROUPS` hierarchy (e.g. "all 62 โสมนัสสหคตจิต" spans multiple groups). Exposed in `data.json` as `cittaLenses`, computed in `scripts/build_data.py`, and browsable via the "เน้นตาม" overlay in `js/app.js` — available in สังคหนัย mode only (hidden in the other 2), since a lens match highlights both the matching cittas and, via their สังคหนัย edges, every cetasika that appears in at least one of them; that citta→cetasika direction is what สังคหนัย mode is already showing, so the overlay layers naturally on top of it. 8 of the 9 are implemented: ชาติ/ภูมิ/โสภณ/โลก/เหตุ/ฌาน are fully determined by a citta's `group`; เวทนา and สังขาร vary within a group but were successfully reconciled against the book's own totals (line 685-707: สุข=1/ทุกข์=1/โสมนัส=62/โทมนัส=2/อุเบกขา=55; อสังขาริก=37/สสังขาริก=84) via a derivation from `group` + a numeric id/`order` suffix, with those totals re-checked at every `build_data.py` run. **สัมปโยคเภทนัย is deliberately left unimplemented** — the book states its totals (สัมปยุตต์=87, วิปปยุตต์=34) but leaves the exact per-citta membership as "ฯลฯ" (unstated); the most obvious derivation (ทิฏฐิ/ญาณ-presence, all อเหตุกจิต→วิปปยุตต์, all ฌานจิต→สัมปยุตต์) lands on 83/38, not 87/34, and the discrepancy hasn't been resolved. Don't add a `sampayoga` lens without either finding the source's exact citta list or having it manually re-derived and checked against 87/34.

**นิยตโยคีเจตสิก / อนิยตโยคีเจตสิก**:
Whether a cetasika accompanies its citta *unconditionally* whenever that citta arises. 41 cetasikas are นิยตโยคี (unconditional); 11 are อนิยตโยคี (conditional), split into 3 further categories (ch.2, line 409): **กทาจิ** — arises only sometimes, alone (มานะ); **นานากทาจิ** — arises only sometimes, and never simultaneously with its named siblings (อิสสา/มัจฉริยะ/กุกกุจจะ; the 3 วิรตี in lokiya context; กรุณา/มุทิตา); **สหกทาจิ** — arises only sometimes, but always as a pair when it does (ถีนะ/มิทธะ). Modeled in `data/cetasikas.yaml` via `combination_type` and `excludes` on the 11 affected cetasikas — everything else is implicitly นิยตโยคี. Browsable via the "เน้นตาม (เจตสิก)" overlay in `js/app.js` (`#combo-overlay`) — available in สัมปโยคนัย mode only (เจตสิก is the source type there; สังคหนัย treats เจตสิก as a target, ตทุภยมิสสกนัย as a cetasika↔cetasika relation), same hide-and-reset-on-mode-switch pattern as the จิต lens overlay (`updateComboAvailability`). Selecting a category highlights the matched เจตสิก *and*, via their สัมปโยคนัย edges, every จิต at least one of them occurs in — mirroring how the จิต lens overlay highlights the เจตสิก reachable from its matched จิต.

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
