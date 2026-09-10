# Abhidhamma Julato (อภิธรรมชั้นจูฬโท)

An interactive study site for the **จูฬโท** (จูฬอาภิธัมมิกะโท) level of the Thai
Abhidhamma curriculum (อภิธรรมโชติกะวิทยาลัย), covering **ปริจเฉทที่ ๓ ปกิณณกสังคหะ**
and **ปริจเฉทที่ ๗ สมุจจยสังคหะ** of the Abhidhammatthasangaha. Primary source: the
official จูฬโท textbook (ปรมัตถโชติกะ, มูลนิธิสัทธัมมโชติกะ), transcribed in
`reference/`.

The จิต ๑๒๑ / เจตสิก ๕๒ / รูป ๒๘ vocabulary is shared with the sibling **จูฬตรี**
project — see `../../julatri/abhidhamma-julatri/CONTEXT.md` for those definitions.
This file defines only the terms specific to จูฬโท.

## Language

**จูฬโท (จูฬอาภิธัมมิกะโท)**:
The second course of the ชั้นตรี tier of the อภิธรรมโชติกะวิทยาลัย curriculum,
following จูฬตรี. Its syllabus is ปริจเฉทที่ ๓ and ๗ of the Abhidhammatthasangaha.
On this site the level is romanised "julato" and the two chapters are reached at
`/julator/p3` and `/julator/p7`.

**ปกิณณกสังคหะ (ปริจเฉทที่ ๓ — "p3")**:
The "miscellaneous compendium". Re-classifies the จิต ๑๒๑ and เจตสิก ๕๒ (already
enumerated in ปริจเฉท ๑–๒) under six cross-cutting schemes: เวทนาสังคหะ,
เหตุสังคหะ, กิจจสังคหะ, ทวารสังคหะ, อารัมมณสังคหะ, วัตถุสังคหะ.

**สมุจจยสังคหะ (ปริจเฉทที่ ๗ — "p7")**:
The "categories compendium". Gathers dhammas into named traditional sets (อาสวะ ๔,
นีวรณะ ๖, สังโยชน์ ๑๐, อินทรีย์ ๒๒, โพชฌงค์ ๗, …) organised under four สังคหะ:
อกุศลสังคหะ, มิสสกสังคหะ, โพธิปักขิยสังคหะ, สัพพสังคหะ.

**นัย / scheme (p3)**:
One of the six classification axes of ปกิณณกสังคหะ. Each นัย partitions or maps
the จิต/เจตสิก set by a single principle (feeling, root, function, door, object,
physical base). In the data model each นัย is one entry under `p3.yaml → schemes`.

**partition axis vs. matrix axis** (`cardinality`):
A distinction in *how* a p3 axis-block relates จิต or เจตสิก to its categories —
recorded **per axis-block**, not per นัย, because a นัย can classify จิต and
เจตสิก with different cardinalities.
A **partition** axis places each ปรมัตถ์ in exactly one category (e.g. จิต by
เวทนา ๕ — each จิต has one feeling). A **matrix** axis is many-to-many: the
ปรมัตถ์ carries a *set* of 0..N categories (e.g. เจตสิก by เวทนา; จิต and เจตสิก
by เหตุ ๖). A matrix block may also carry `groupings` — summary buckets keyed by
set size (e.g. เหตุ: 0/1/2/3 เหตุ per จิต = อเหตุก ๑๘ / เอกเหตุก ๒ / ทวิเหตุก ๒๒
/ ติเหตุก ๗๙). The UI tints a partition node with its one category colour and
gives a matrix node a strip of category dots.

**สังคหะ (p7)**:
One of the four top-level groupings of ปริจเฉท ๗. Each สังคหะ contains several
**dhamma-sets**.

**dhamma-set (p7)**:
A named traditional list — อาสวะ ๔, นีวรณะ ๖, สังโยชน์ ๑๐, and so on. In the data
model, one entry under `p7.yaml → sangahas[].sets`. Its `count_label` is the
canonical count (๔, ๑๐, …); its `members` are the individual named dhammas in it.

**องค์ธรรม (ongkhatham)**:
The ปรมัตถ์ reality (a specific เจตสิก, จิต, รูป, or นิพพาน) that a named dhamma
*is*. E.g. the องค์ธรรม of กามาสวะ is the เจตสิก โลภะ. In the data model each p7
member lists its องค์ธรรม as ปรมัตถ์ ids; the build inverts this into the
reverse index "which sets does this เจตสิก appear in?".

**ปรมัตถ์ id space**:
The canonical id + Thai-label registry in `data/paramattha.yaml`: จิต ๑๒๑,
เจตสิก ๕๒, รูป ๒๘, นิพพาน ๑ (202 ids). Both `p3.yaml` and `p7.yaml` key their data
to these ids, and `scripts/build_data.py` rejects any reference that does not
resolve. The registry is a **copy** seeded from the จูฬตรี project's YAML by
`scripts/seed_paramattha.py`; see `docs/adr/0001`.

## เวทนาสังคหะ (p3 scheme `vedana` — resolved)

Classifies จิต and เจตสิก by เวทนา (feeling). The textbook gives two granularities:

**เวทนา ๕ (อินทริยเภทนัย)** — สุขเวทนา, ทุกขเวทนา, โสมนัสเวทนา, โทมนัสเวทนา,
อุเบกขาเวทนา. The by-อินทรีย์ reading; the site's default.

**เวทนา ๓ (อารัมมณานุภวนลักขณนัย)** — สุข, ทุกข์, อุเบกขา. A coarsening of เวทนา ๕:
โสมนัส collapses into สุข, โทมนัส into ทุกข์. Modelled as a `views` sub-toggle
with a `collapse` map, not as separate data.

**จิต by เวทนา** — a *partition*: each จิต has exactly one เวทนา.
เวทนา ๕ counts: สุข 1, ทุกข์ 1, โสมนัส 62, โทมนัส 2, อุเบกขา 55 (คาถาที่ ๒).
เวทนา ๓ counts: สุข 63, ทุกข์ 3, อุเบกขา 55.

**เจตสิก by เวทนา** — a *matrix*: each เจตสิก co-occurs with a *set* of 0–5 เวทนา.
The textbook's summary buckets the 52 by that set's size: เกิดกับ ๑ เวทนา (6),
๒ (28), ๓ (11), ๔ (0), ๕ (6), และ เวทนาเจตสิก เอง ที่ไม่จัดเข้าเวทนาใด (1). Those
counts are kept as an `expect` gate in `build_data.py`; the UI shows each
เจตสิก's set as coloured dots and in the info panel rather than as headings.

**Panel layout** — both panels are organised by the standard จิต / เจตสิก groups
(โลภมูลจิต ๘ … โลกุตตรจิต ๔๐; สัพพจิตตสาธารณ ๗ …), in the textbook's order and row
structure, exactly as the julatri site. เวทนา is an overlay on that layout
(node colour + category rail + cross-highlight), not a re-grouping.

**เวทนาเจตสิก** is not classified by เวทนา — a factor does not co-arise with
itself. Its set is empty; it sits in its own bucket.

Data: `data/p3/vedana.yaml`, generated by `scripts/derive_p3_vedana.py` (verified
against `reference/01-…md` L52–L153 and cross-checked against julatri's per-citta
เวทนา and cetasika co-occurrence).

## เหตุสังคหะ (p3 scheme `hetu` — resolved)

Classifies จิต and เจตสิก by **เหตุ ๖** (root): โลภเหตุ, โทสเหตุ, โมหเหตุ (อกุศล /
อโสภณ) and อโลภเหตุ, อโทสเหตุ, อโมหเหตุ (โสภณ). องค์ธรรม of the six: โลภ, โทส, โมห,
อโลภ, อโทส เจตสิก and — for อโมหเหตุ — ปัญญาเจตสิก.

**จิต by เหตุ** — a *matrix* (each จิต co-arises with 0–3 เหตุ), summarised by the
คาถา as size buckets: อเหตุกจิต ๑๘, เอกเหตุกจิต ๒, ทวิเหตุกจิต ๒๒, ติเหตุกจิต ๗๙
(นับพิสดาร; ๔๗ in the ๘๙ system). Per-เหตุ จิต totals — โลภ ๘, โทส ๒, โมห ๑๒,
อโลภ ๙๑, อโทส ๙๑, อโมห ๗๙ — reproduce the textbook's "การนับจำนวนเหตุ โดยพิสดาร
๒๘๓" table exactly.

**เจตสิก by เหตุ** — a *matrix*, taken by **อคหิตัคคหนนัย** (count only the *other*
roots that accompany the เจตสิก; a root เจตสิก does not count itself). Size buckets
(reference L253–L295): เหตุ ๑ = ๓, เหตุ ๒ = ๙, เหตุ ๓ = ๒๗, เหตุ ๔ = ๐, เหตุ ๕ = ๑
(ปีติ), เหตุ ๖ = ๑๒ (อัญญสมาน ๑๒ เว้นปีติ). The other reading in the text,
**คหิตัคคหนนัย** (context-dependent, counts a เจตสิก once per จิต-context), is not
modelled — it is a per-occurrence tally, not a per-เจตสิก set.

Data: `data/p3/hetu.yaml`, generated by `scripts/derive_p3_hetu.py`. Both the จิต
and the เจตสิก sets are derived twice — once from the textbook's wording, once
reconstructed from julatri's per-citta root membership — and the build fails
unless the two agree.

**Panel layout** is the same as [เวทนาสังคหะ](#เวทนาสังคหะ-p3-scheme-vedana--resolved):
standard จิต / เจตสิก groups in julatri order; เหตุ is an overlay (dots on every
node since both axes are matrix, plus the category rail and cross-highlight).

## กิจจสังคหะ (p3 scheme `kicca` — resolved)

Classifies จิต and เจตสิก by **กิจ ๑๔** (function): ปฏิสนธิ ภวังค อาวัชชน ทัสสน สวน
ฆายน สายน ผุสน สัมปฏิจฉน สันตีรณ โวฏฐัพพน ชวน ตทารัมมณ จุติ. Every จิต and เจตสิก
does at least one กิจ — none arise functionless.

**จิต by กิจ** — a *matrix* (๑–๕ กิจ per จิต), คาถา size buckets: ทำ ๑ กิจ ๑๐๐,
๒ กิจ ๒, ๓ กิจ ๙, ๔ กิจ ๘, ๕ กิจ ๒ (นับพิสดาร; ๖๘ for the ๑-กิจ bucket in the ๘๙
system). Per-กิจ จิต totals: ปฏิสนธิ/ภวังค/จุติ ๑๙ each, อาวัชชน ๒, ทัสสน..ผุสน ๒
each, สัมปฏิจฉน ๒, สันตีรณ ๓, โวฏฐัพพน ๑, ชวน ๘๗, ตทารัมมณ ๑๑.

**เจตสิก by กิจ** — a *matrix*. Size buckets (reference L540–L600): ๑ กิจ = ๑๗
(อกุศล ๑๔ + วิรตี ๓, all ชวนกิจ), ๔ = ๒ (อัปปมัญญา), ๕ = ๒๑ (โสภณสาธารณ ๑๙ +
ปัญญา + ฉันทะ), ๖ = ๑ (ปีติ), ๗ = ๑ (วีริยะ), ๙ = ๓ (วิตก วิจาร อธิโมกข์), ๑๔ = ๗
(สัพพจิตตสาธารณ). The text *heads* the วิตก/วิจาร/อธิโมกข์ entry "ทำหน้าที่ ๘" but
enumerates ๙ กิจ (อาวัชชน สัมปฏิจฉน สันตีรณ โวฏฐัพพน included); the julatri
reconstruction also yields ๙, so this project models ๙.

**ฐาน ๑๐** is not a separate axis — it is กิจ ๑๔ with the five ปัญจวิญญาณกิจ
(ทัสสน สวน ฆายน สายน ผุสน) merged into ปัญจวิญญาณฐาน; every count is unchanged
(๑/๒/๓/๔/๕ กิจ = ๑/๒/๓/๔/๕ ฐาน). Recorded in the scheme note, not as data. The
ฐาน ๒๕ (พิสดาร / โดยวิถี) material is วิถี-position counting, out of scope.

Data: `data/p3/kicca.yaml`, generated by `scripts/derive_p3_kicca.py`. The จิต
sets are built from the per-กิจ lists (L420–448); the เจตสิก sets are authored
from L540–600; and every เจตสิก set is independently reconstructed from julatri
co-occurrence (union the กิจ-sets of the cittas it occurs in) — the build fails
unless all three agree.

## ทวารสังคหะ (p3 scheme `dvara` — resolved)

Classifies จิต and เจตสิก by **ทวาร ๖** (door): จักขุ โสต ฆาน ชิวหา กายทวาร
(องค์ธรรม = ปสาทรูป ๕) and มโนทวาร (องค์ธรรม = ภวังคจิต ๑๙).

**จิต by ทวาร** — a *matrix* (๐–๖ ทวาร per จิต). **ทวารวิมุตต** (arising free of
any door — ปฏิสนธิ/ภวังค/จุติ role) is modelled as the *empty* door-set (size 0),
the same way อเหตุก is size-0 in เหตุสังคหะ. Size buckets: ทวารวิมุตต ๙
(มหัคคตวิปาก ๙), เอกทวาริก ๖๘, ปัญจทวาริก ๓ (มโนธาตุ ๓), ฉทวาริก ๔๑. The คาถา's
finer 5-way split (เอกทวาริก ๓๖/๖๘ · ปัญจทวาริก ๓ · ฉทวาริกแน่นอน ๓๑ · ฉทวาริก-
หรือ-ทวารวิมุตต ๑๐ [อุเบกขาสันตีรณ ๒ มหาวิปาก ๘] · ทวารวิมุตตแน่นอน ๙) lives in the
note; the ๑๐ mixed จิต carry the full 6-door set. Per-ทวาร totals reproduce the
textbook headline: จักขุ..กายทวาริกจิต ๔๖ each, มโนทวาริกจิต ๙๙, ทวารวิมุตตจิต ๑๙.

**เจตสิก by ทวาร** — a *matrix*. อัปปมัญญาเจตสิก ๒ arise only in มโนทวาร (they take
a สัตวบัญญัติ object); the other ๕๐ arise in all ๖ ทวาร. Buckets: ๑ ทวาร = ๒,
๖ ทวาร = ๕๐.

**เอกันตะ (เกิดแน่นอน) / อเนกันตะ (ไม่แน่นอน)** per door — a large part of the
text — is **not modelled in this pass**. Noted in the scheme note.

Data: `data/p3/dvara.yaml`, generated by `scripts/derive_p3_dvara.py`. No julatri
cross-check (a เจตสิก's ทวาร depends on its object, not its host จิต's door-set —
อัปปมัญญา is the flagged case). Verification is internal: the 5-way คาถา split and
the per-ทวาร headline totals must both reproduce.

## อารัมมณสังคหะ (p3 scheme `arammana` — resolved)

Classifies จิต and เจตสิก by **อารมณ์ ๖** (object): รูปารมณ์ (สี), สัททารมณ์
(เสียง), คันธารมณ์ (กลิ่น), รสารมณ์ (รส), โผฏฐัพพารมณ์ (เย็น ร้อน อ่อน แข็ง หย่อน
ตึง), ธัมมารมณ์ (องค์ธรรม = จิต, เจตสิก, ปสาทรูป ๕, สุขุมรูป ๑๖, นิพพาน, บัญญัติ).

**จิต by อารมณ์ ๖** — a *matrix* (๑ / ๕ / ๖ อารมณ์ per จิต). Size buckets:
รับประเภทเดียว ๗๕ (ทวิปัญจวิญญาณ ๑๐ อย่างละ ๑ วิสยารมณ์ + รูปาวจรฌาน ๑–๔,
รูปาวจรปัญจมฌานวิปาก, อรูปาวจร ๑๒, โลกุตตร ๔๐ — ธัมมารมณ์อย่างเดียว ๖๕),
รับปัญจารมณ์ ๕ = ๓ (มโนธาตุ ๓; ref L1259), รับครบ ๖ = ๔๓ (อกุศล ๑๒ + สันตีรณ ๓ +
มหาวิปาก ๘ + หสิตุปปาท ๑ + มหากุศล ๘ + มหากิริยา ๘ + มโนทวาราวัชชน ๑ + อภิญญา ๒;
ref L1046, L1089–L1100). Per-อารมณ์ totals reproduce the textbook headline
(L1343–L1362): รูป..โผฏฐัพพารมณ์ ๔๘ ดวงเท่ากัน, ธัมมารมณ์ ๑๐๘ (นับพิสดาร ๑๒๑;
๗๖ ในระบบ ๘๙ โดยโลกุตตรจิต ๘ แทน ๔๐ — เทียบ kicca).

**อภิญญาจิต ๒** = รูปาวจรปัญจมฌานกุศล/กิริยาจิต (ไม่มี id แยกในระบบ ๑๒๑). จัดเข้า
กลุ่มรับอารมณ์ครบ ๖ เพราะทำหน้าที่อภิญญา รู้รูป เสียง จิตของผู้อื่น ฯลฯ ได้; ที่
ตำรานับ อภิญญา ๒ แยก (เป็นนัย ๙๑) เพราะในบทบาทฌานล้วน จิตคู่นี้รับบัญญัติ
(ธัมมารมณ์) อย่างเดียว.

**เจตสิก by อารมณ์ ๖** — a *matrix*. อัปปมัญญาเจตสิก ๒ (กรุณา มุทิตา) รับ
ธัมมารมณ์ (สัตวบัญญัติ) อย่างเดียว; อีก ๕๐ รับได้ทั้ง ๖ (ref L1408–L1409,
L1414–L1415). Buckets: ๑ อารมณ์ = ๒, ๖ อารมณ์ = ๕๐. Per-อารมณ์: รูป..โผฏฐัพพารมณ์
๕๐ ดวง, ธัมมารมณ์ ๕๒. Every เจตสิก takes an object — there is **no empty set**
here (unlike เวทนาเจตสิก in
[เวทนาสังคหะ](#เวทนาสังคหะ-p3-scheme-vedana--resolved)). The finer readings —
วิรตี ๓ take only ปรมัตถ์, อิสสา takes only พหิทธ — sit below อารมณ์ ๖ and are
noted, not modelled.

**กาล ๓** (อดีต/ปัจจุบัน/อนาคต/กาลวิมุตต), **เอกันตะ ๔ – อเนกันตะ ๓** (the ๗ นัย
of the main คาถา, ปญฺจวีส… = ๒๕/๖/๒๑/๘/๒๐/๕/๖ รวม ๙๑) and **อารมณ์พิสดาร ๒๑** are
orthogonal to อารมณ์ ๖ (no clean `views`/`collapse`) and are **not modelled in
this pass** — described in the scheme note, exactly as ทวารสังคหะ deferred
เอกันตะ/อเนกันตะ. The ๗-นัย คาถา totals are still reproduced as an assertion gate
in the generator.

Data: `data/p3/arammana.yaml`, generated by `scripts/derive_p3_arammana.py`. No
julatri cross-check (julatri has no อารมณ์ lens). Verification is internal: the
per-นัย breakdown, the ๗-นัย คาถา (๒๕/๖/๒๑/๘/๒๐/๕/๖), the per-อารมณ์ headline
totals, and the ๘๙-basis figures (ธัมมารมณ์อย่างเดียว ๓๕ L1227, ธัมมารมณ์ ๗๖
L1362) must all reproduce. The ญาณสัมปยุตต indices (มหากุศล/มหากิริยา ดวงที่
๑ ๒ ๕ ๖) are additionally cross-checked against `data/p3/hetu.yaml` (อโมหเหตุ).

**Panel layout** is the same as the other schemes: standard จิต / เจตสิก groups
in julatri order; อารมณ์ is an overlay (dots on every node since both axes are
matrix, plus the category rail and cross-highlight).

## วัตถุสังคหะ (p3 scheme `vatthu` — resolved)

Classifies จิต and เจตสิก by **วัตถุ ๖** (physical base a จิต/เจตสิก rests on):
จักขุ โสต ฆาน ชิวหา กายวัตถุ (องค์ธรรม = ปสาทรูป ๕) and หทัยวัตถุ (องค์ธรรม =
หทยรูป).

**จิต by วัตถุ** — a *matrix*, but degenerate: a จิต rests on **at most one**
วัตถุ (0 or 1). **ไม่อาศัยวัตถุรูป** (อรูปวิปากจิต ๔ — arise only in อรูปภูมิ) is
the *empty* วัตถุ-set (size 0), the same way อเหตุก is size-0 in เหตุ and
ทวารวิมุตต is size-0 in ทวาร. Size buckets: ไม่อาศัยวัตถุ ๔, อาศัยวัตถุเดียว ๑๑๗.
The คาถา (เตจตฺตาลีส นิสฺสาย…ปการุปฺปา อนิสฺสิตา) splits จิต three ways by
*certainty*: อาศัยวัตถุรูปแน่นอน ๔๓, อาศัยบ้าง–ไม่อาศัยบ้าง ๔๒, ไม่อาศัยแน่นอน ๔
(= ๘๙). Mapped onto ๑๒๑ this is ๔๗ / ๗๐ / ๔ — the difference is โลกุตตรจิต:
โสดาปัตติมรรค ๑→๕ (goes in the แน่นอน group — the first path never arises in
อรูปภูมิ; L1514), โลกุตตรอื่น ๗→๓๕ (ไม่แน่นอน group). Per-วัตถุ totals over all
๑๒๑ จิต: จักขุ..กายวัตถุ ๒ each, หทัยวัตถุ ๑๐๗ (๓๗ แน่นอน + ๗๐ ไม่แน่นอน); the
textbook headline "จิต ๔๓ ที่อาศัยแน่นอน โดยวัตถุ ๖" (จักขุ..กาย ๒, หทัย ๓๓ in
the ๘๙ system) is reproduced as an internal assertion.

**เจตสิก by วัตถุ** — a *matrix*. **สัพพจิตตสาธารณเจตสิก ๗** rest on all ๖ วัตถุ
(they ride the ทวิปัญจวิญญาณ ๑๐, which rest on the ๕ ปสาท, and every other จิต,
which rests on หทัย). The other **๔๕** rest on หทัยวัตถุ only — ปกิณณก ๖ / อกุศล
๑๐ / โสภณ ๒๓ do not accompany the ทวิปัญจวิญญาณ ๑๐. Every one of the ๕๒ rests on
หทัยวัตถุ, so there is no size-0 bucket. Buckets: ๑ วัตถุ = ๔๕, ๖ วัตถุ = ๗.
Per-วัตถุ: จักขุ..กายวัตถุ ๗ each, หทัยวัตถุ ๕๒.

**เอกันตะ (อาศัยแน่นอน) / อเนกันตะ (อาศัยไม่แน่นอน)** — the modality of the
หทัยวัตถุ attachment (necessary vs. contingent on the จิต/เจตสิก arising in
ปัญจโวการภูมิ) — is **not modelled as a sub-axis** (orthogonal to the ๖ วัตถุ,
not a category collapse). It is described in the scheme note as the คาถา 3-way
split; on จิต the internal gate checks it, on เจตสิก the "อาศัยวัตถุรูปแน่นอน ๖"
(โทจตุกเจตสิก ๔ + อัปปมัญญาเจตสิก ๒) vs "ไม่แน่นอน ๔๖" is asserted but not shown.
Deferred exactly as ทวารสังคหะ deferred เอกันตะ/อเนกันตะ per door.

Data: `data/p3/vatthu.yaml`, generated by `scripts/derive_p3_vatthu.py`. No
julatri cross-check — julatri has no วัตถุ lens. Verification is internal: the
คาถา 3-way totals (๔๓/๔๒/๔ in the ๘๙ system), the per-วัตถุ headline for จิต ๔๓
แน่นอน, and the full ๑๒๑-basis per-วัตถุ totals must all reproduce.

**Panel layout** is the same as the other schemes: standard จิต / เจตสิก groups
in julatri order; วัตถุ is an overlay (dots on every node — both axes matrix —
plus the category rail and cross-highlight). Palette `--vt-*` in `shell.css`
reuses ทวาร's sense-base hues; หทัยวัตถุ = the มโนทวาร slate.

## สมุจจยสังคหะ (p7 — resolved)

The four สังคหะ of ปริจเฉท ๗, filled one สังคหะ per subagent against
`reference/02-…md` (2026-08-30): **อกุศล ๙ หมวด · มิสสก ๗ · โพธิปักขิย ๗ ·
สัพพ ๕ = ๒๘ dhamma-sets, ~๑๙๘ named members.**

**Data pipeline.** One hand-verified fragment per สังคหะ at
`data/p7/<sangaha>.yaml` (the สังคหะ dict: `id`, `thai`, optional
`gatha`/`source`/`note`, `sets[]`), assembled by `scripts/assemble_p7.py` in
`SANGAHA_ORDER` → `data/p7.yaml` (generated — never hand-edit). Per-set
verification record: `docs/p7-verification/<sangaha>.md`. `build_data.py`
checks every `ongkhatham` id against `paramattha.yaml` and every
`expect == len(members)`, and emits `p7.reverse` (ปรมัตถ์ id →
`[{sangaha, set, member}]`).

**Member shape.** Each `members[]` entry names its **องค์ธรรม as ปรมัตถ์ id(s)**
(`ongkhatham`); the host-จิต phrase ("โลภเจตสิก ที่ใน โลภมูลจิต ๘") is prose in
the member `note`. Where the องค์ธรรม is a whole ปรมัตถ์ class (มนินทรีย์ = จิต
๑๒๑; วิญญาณขันธ์; จิตตาธิปติ; รูปขันธ์ = รูป ๒๘; …) every id is enumerated in
full so the tool's cross-highlight is complete.

**`count_label` vs `expect`.** `count_label` is the traditional display count
(Thai numerals); `expect` is the number of *named* members. They diverge where
the คาถา counts *distinct ปรมัตถ์*: นีวรณะ ๖ names / ๘ องค์ธรรม (ถีนมิทธ = ถีนะ
+ มิทธะ; อุทธัจจกุกกุจจ = อุทธัจจะ + กุกกุจจะ), อนุสัย ๗ / ๖ (กามราค + ภวราค =
โลภะ), มิสสก ฌานังคะ ๗ / ๕ (โสมนัส·โทมนัส·อุเบกขา = เวทนา), มัคคังคะ ๑๒ / ๙
(สัมมา+มิจฉา สังกัปปะ·วายามะ·สมาธิ share วิตก·วิริยะ·เอกัคคตา), อินทรีย์ ๒๒ /
๑๖. Each such gap is spelled out in that set's `note`.

### Modeling calls a reviewer (careful Abhidhamma student) should eyeball

1. **สังโยชน์ ๑๐** (อกุศล): the **สุตตันตนัย** list is `members`; the
   **อภิธรรมนัย** list and the โอรัมภาคิย/อุทธัมภาคิย breakdowns are in the set
   `note`, not modelled — so `issa` / `macchariya` (อภิธรรมนัย only) are in no
   `ongkhatham`. The คาถา's "นว" (๙) matches neither นัย's distinct-ปรมัตถ์
   total in this textbook. *Main call to confirm.*
2. **โพธิปักขิย**: the ๓๗ องค์ collapse to **๑๔ distinct องค์ธรรม** (ฐาน counts
   สติ ๘ · วิริยะ ๙ · เอกัคคตา ๔ · ปัญญา ๕ · สัทธา ๒ · ๑ each for ฉันทะ, จิต,
   ตัตรมัชฌัตตตา, ปัสสัทธิ [กาย+จิตต- as one], ปีติ, วิตก, สัมมาวาจา/กัมมันตะ/
   อาชีวะ). **จิตติทธิบาท = กุศลจิต** (มหากุศล ๘ + รูปกุศล ๕ + อรูปกุศล ๔ +
   มัคคจิต ๒๐ = ๓๗ ในระบบ ๑๒๑; "๒๑" ในระบบ ๘๙) — the text (L931, L1212)
   excludes กิริยา and ผลจิต, not "all 121".
3. **สัพพ**: **รูปขันธ์/รูปุปาทานักขันธ์ = รูป ๒๘** (per the member line + ปัญจขันธ์
   คาถา), *not* นิปผันนรูป ๑๘ — the 18-vs-28 frame surfaces instead as
   **สุขุมรูป ๑๖** inside ธัมมายตนะ / ธัมมธาตุ. **สังขารุปาทานักขันธ์ keeps all
   ๕๐ factors** (the text excludes only เวทนา·สัญญา, not โลกุตตร-only factors).
   All counts use the **๑๒๑ basis** (`paramattha.yaml` has no ๘๙ ids); the
   text's ๘๙-system figures (มโนวิญญาณธาตุ ๗๖ → ๑๐๘; โลกียจิต ๘๑ = ๑๒๑ − ๔๐
   โลกุตตร) are preserved in member `note`s.
4. **`jivitindriya` id collision** — `paramattha.yaml` uses the one id string
   for both ชีวิตรูป and ชีวิตินทรียเจตสิก (id space is per-kind; p7's
   `ongkhatham` check flattens kinds). It is therefore cited **once**:
   ชีวิตินทรีย์ (มิสสก อินทรีย์) carries 1 id for 2 realities;
   ธัมมายตนะ/ธัมมธาตุ carry 68 for 69; ทุกขสัจจะ 159 for 160. Known limitation,
   not a data error.
5. **Stub spellings corrected to the source**: `อุปาทานขันธ์` → **อุปาทานักขันธ์**,
   `อริยสัจ` → **อริยสัจจะ**. Source OCR typos left flagged in member `note`s
   (ปฏิม→ปฏิฆ สังโยชน์; โลก→โลภ เหตุ; อกุศล intro "๓๖" vs ๓๙).

Deferred (described in the owning set's `note`, **not** built as structure):
กิเลส พิสดาร ๑,๕๐๐ · สังโยชน์ สุตตันต/อภิธรรม & โอรัมภาคิย/อุทธัมภาคิย ·
อินทรีย์ ๒๒ จำแนกโดยภูมิ · อธิบดี "เกิดทีละ ๑" · องค์มรรค ๘ โดยสีล/สมาธิ/ปัญญาขันธ์ ·
อริยสัจจ ๔ โดยเหตุ-ผล / โลกีย-โลกุตตร · ขันธวิมุตต์ / สัจจวิมุตต์ reasoning · the
"จิตที่ไม่ได้องค์ฌาน/มรรค/อินทรีย์/พละ" คาถา. Same pattern as p3 deferring
เอกันตะ/อเนกันตะ and กาล ๓.

### The p7 tool

`p7/index.html` + **its own `p7/app.js`** (not shared with p3 — the interaction
model is different: no per-นัย axis, no partition/matrix cardinality, no
category rail). Left panel = the active สังคหะ's dhamma-sets as header + member
chips (text-heavy → chips, not circles); a 4-tab สังคหะ switcher above.
Right panel = every ปรมัตถ์ (จิต ๑๒๑ · เจตสิก ๕๒ · รูป ๒๘ · นิพพาน ๑ = ๒๐๒
`.node` circles) in the standard จูฬตรี groups, always all shown. Hover/click
either side cross-highlights the other via `p7.reverse`; the info panel shows
องค์ธรรม chips + the set's คาถา + "ปรากฏใน N หมวด" list. Selecting a ปรมัตถ์
whose sets are not under the active tab **auto-switches** to the first สังคหะ
that contains it and badges every tab with its match count. Palette `--rupa-*`
/ `--nibbana-*` in `shell.css`. Headless test: `scripts/test_p7_render.js`.
