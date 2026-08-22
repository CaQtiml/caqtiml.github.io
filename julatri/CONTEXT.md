# Abhidhamma Julatri (อภิธรรมชั้นจูฬตรี)

An interactive study site for the จูฬตรี level of the Thai Abhidhamma curriculum (อภิธรรมโชติกะวิทยาลัย), covering จิต-เจตสิก classification and the three nayas from ปริจเฉทที่ ๒ of the Abhidhammatthasangaha. Primary source: the official จูฬตรี textbook ("ปรมัตถโชติกะ ปริจเฉทที่ ๑-๒-๖" by พระสัทธัมมโชติกะ ธัมมาจริยะ, มูลนิธิสัทธัมมโชติกะ).

## Language

**จิต (Citta)**:
A moment of consciousness. Classified into 89 (or 121, expanded) types across kāmāvacara, rūpāvacara, arūpāvacara, and lokuttara realms.

**เจตสิก (Cetasika)**:
A mental factor that arises together with a citta, sharing its object, base, arising, and ceasing. There are 52, grouped into อัญญสมานาเจตสิก (13), อกุศลเจตสิก (14), and โสภณเจตสิก (25).

**อกุศลจิต**:
The 12 unwholesome cittas (โลภมูลจิต 8, โทสมูลจิต 2, โมหมูลจิต 2). The pilot dataset for this project's first slice.

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
