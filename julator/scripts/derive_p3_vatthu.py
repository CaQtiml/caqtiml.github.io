#!/usr/bin/env python3
"""
Generate data/p3/vatthu.yaml -- the วัตถุสังคหะ scheme fragment for /julator/p3.

Source: reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L1421-L1550 (the authoritative
text).  There is no julatri cross-check here -- julatri has no วัตถุ lens.
Verification is internal, the same way derive_p3_dvara.py works:

  * จิต by วัตถุ ๖ (each จิต arises on a SET of 0-1 วัตถุ -- a จิต rests on at
    most one วัตถุ, so the "matrix" is really a partition-with-empty-case).
    Built from the คาถา 3-way split (L1461-L1470, L1503-L1534):
        อาศัยวัตถุรูปแน่นอน ๔๓ (๘๙) / ๔๗ (พิสดาร)  -- ทวิปัญจวิญญาณ ๑๐ each on
            its own ปสาท; the rest on หทัยวัตถุ (arise only in ปัญจโวการภูมิ).
        อาศัยบ้าง-ไม่อาศัยบ้าง ๔๒ (๘๙) / ๗๐ (พิสดาร)  -- {หทัยวัตถุ} when in
            ปัญจโวการภูมิ, no วัตถุ when in อรูปภูมิ.
        ไม่อาศัยวัตถุรูปแน่นอน ๔  -- อรูปวิปากจิต ๔ (arise only in อรูปภูมิ).
    Asserted:
      - the ๘๙-basis คาถา totals reproduce: 43 / 42 / 4 (เตจตฺตาลีส เทฺวจตฺตาลีส
        ... ปการุปฺปา อนิสฺสิตา).
      - set-size buckets (พิสดาร ๑๒๑): 0 = 4 (อรูปวิปาก), 1 = 117.
      - the per-วัตถุ headline "การจำแนกจิต ๔๓ ที่อาศัยวัตถุรูปเกิดแน่นอน โดย
        วัตถุรูป ๖" (L1503-L1512): จักขุ..กายวัตถุ ๒ ดวง each, หทัยวัตถุ ๓๓
        (๘๙-basis) -- and its พิสดาร form จักขุ..กาย ๒, หทัย ๓๗ (โสดาปัตติมรรค
        ๑->๕).
      - the full-matrix per-วัตถุ totals over all ๑๒๑ จิต: จักขุ..กาย ๒ each,
        หทัยวัตถุ ๑๐๗ (= ๓๗ แน่นอน + ๗๐ ไม่แน่นอน).  This is the `expect` gate
        in build_data.py (which counts ๑๒๑-basis ids).
  * เจตสิก by วัตถุ ๖ (L1535-L1549): สัพพจิตตสาธารณเจตสิก ๗ ride the
    ทวิปัญจวิญญาณ ๑๐, so they rest on all ๖ วัตถุ; the other ๔๕ เจตสิก rest on
    หทัยวัตถุ only (ปกิณณก/อกุศล/โสภณ เจตสิก do not accompany ทวิปัญจวิญญาณ).
    Every one of the ๕๒ rests on หทัยวัตถุ.  Buckets: ๑ วัตถุ = ๔๕, ๖ วัตถุ = ๗.
    Asserted: per-วัตถุ จักขุ..กาย ๗ each, หทัยวัตถุ ๕๒; and the text's
    "อาศัยวัตถุรูปแน่นอน ๖" = โทจตุกเจตสิก ๔ + อัปปมัญญาเจตสิก ๒, "ไม่แน่นอน ๔๖".

"ไม่อาศัยวัตถุรูปเกิด" (อรูปวิปาก ๔) is modelled as the EMPTY วัตถุ-set
(set-size 0), the same way อเหตุก is size-0 in เหตุสังคหะ and ทวารวิมุตต is
size-0 in ทวารสังคหะ.  เอกันตะ (อาศัยแน่นอน) / อเนกันตะ (อาศัยไม่แน่นอน) is NOT
a modelled sub-axis -- it is described in the scheme note as the คาถา 3-way
split, exactly as ทวารสังคหะ deferred เอกันตะ/อเนกันตะ per door.

Run: python3 scripts/derive_p3_vatthu.py   (then: python3 scripts/build_data.py)
"""
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PARAMATTHA = ROOT / "data" / "paramattha.yaml"
OUT = ROOT / "data" / "p3" / "vatthu.yaml"

VATTHU_ORDER = ["cakkhu", "sota", "ghana", "jivha", "kaya", "hadaya"]
VATTHU_THAI = {
    "cakkhu": "จักขุวัตถุ", "sota": "โสตวัตถุ", "ghana": "ฆานวัตถุ",
    "jivha": "ชิวหาวัตถุ", "kaya": "กายวัตถุ", "hadaya": "หทัยวัตถุ",
}
PASADA = ["cakkhu", "sota", "ghana", "jivha", "kaya"]


def die(msg):
    sys.exit(f"derive_p3_vatthu: {msg}")


def ordered(xs):
    return sorted(set(xs), key=VATTHU_ORDER.index)


# ---- citta id groups (from data/paramattha.yaml naming) ----
LOBHAMULA = [f"lobhamula-{i}" for i in range(1, 9)]
DOSAMULA = [f"dosamula-{i}" for i in range(1, 3)]
MOHAMULA = [f"mohamula-{i}" for i in range(1, 3)]

DVIPANCA = {
    "cakkhu": ["ahetuka-akusalavipaka-cakkhu", "ahetuka-kusalavipaka-cakkhu"],
    "sota": ["ahetuka-akusalavipaka-sota", "ahetuka-kusalavipaka-sota"],
    "ghana": ["ahetuka-akusalavipaka-ghana", "ahetuka-kusalavipaka-ghana"],
    "jivha": ["ahetuka-akusalavipaka-jivha", "ahetuka-kusalavipaka-jivha"],
    "kaya": ["ahetuka-akusalavipaka-kaya", "ahetuka-kusalavipaka-kaya"],
}
SAMPATICCHANA = ["ahetuka-akusalavipaka-sampaticchana", "ahetuka-kusalavipaka-sampaticchana"]
PANCADVARAVAJJANA = ["ahetuka-pancadvaravajjana"]
MANODHATU = PANCADVARAVAJJANA + SAMPATICCHANA  # 3
MANODVARAVAJJANA = ["ahetuka-manodvaravajjana"]
HASITUPPADA = ["ahetuka-hasituppada"]
UPEKKHA_SANT = ["ahetuka-akusalavipaka-upekkhasantirana", "ahetuka-kusalavipaka-upekkhasantirana"]
SOMANASSA_SANT = ["ahetuka-kusalavipaka-somanassasantirana"]
SANTIRANA3 = UPEKKHA_SANT + SOMANASSA_SANT  # 3

MAHAKUSALA = [f"mahakusala-{i}" for i in range(1, 9)]
MAHAVIPAKA = [f"mahavipaka-{i}" for i in range(1, 9)]
MAHAKIRIYA = [f"mahakiriya-{i}" for i in range(1, 9)]

JHANA5 = ["ปฐมฌาน", "ทุติยฌาน", "ตติยฌาน", "จตุตถฌาน", "ปัญจมฌาน"]
RUPA_KUSALA = [f"rupa-{j}-kusala" for j in JHANA5]
RUPA_VIPAKA = [f"rupa-{j}-vipaka" for j in JHANA5]
RUPA_KIRIYA = [f"rupa-{j}-kiriya" for j in JHANA5]
RUPAVACARA = RUPA_KUSALA + RUPA_VIPAKA + RUPA_KIRIYA  # 15
ARUPA = ["akasanancayatana", "vinnanancayatana", "akincannayatana", "nevasannanasannayatana"]
ARUPA_KUSALA = [f"arupa-{n}-kusala" for n in ARUPA]
ARUPA_VIPAKA = [f"arupa-{n}-vipaka" for n in ARUPA]
ARUPA_KIRIYA = [f"arupa-{n}-kiriya" for n in ARUPA]

PHASES = ["sotapatti", "sakadagami", "anagami", "arahatta"]
LOKUTTARA = [f"{p}-{mp}-{j}" for p in PHASES for mp in ("magga", "phala") for j in JHANA5]  # 40
SOTAPATTI_MAGGA = [f"sotapatti-magga-{j}" for j in JHANA5]  # 5
LOKUTTARA_OTHER = [c for c in LOKUTTARA if c not in SOTAPATTI_MAGGA]  # 35

# ---- the 3-way คาถา split (L1461-L1470), mapped onto the ๑๒๑ id space ----
# (วัตถุ-set, citta-ids)
# A. อาศัยวัตถุรูปแน่นอน -- always rests on exactly one วัตถุ (ปัญจโวการภูมิ only)
GROUP_A = [
    (["cakkhu"], DVIPANCA["cakkhu"]),
    (["sota"], DVIPANCA["sota"]),
    (["ghana"], DVIPANCA["ghana"]),
    (["jivha"], DVIPANCA["jivha"]),
    (["kaya"], DVIPANCA["kaya"]),
    (["hadaya"], DOSAMULA + MANODHATU + SANTIRANA3 + HASITUPPADA + MAHAVIPAKA
     + RUPAVACARA + SOTAPATTI_MAGGA),
]
# B. อาศัยบ้าง-ไม่อาศัยบ้าง -- {หทัยวัตถุ} in ปัญจโวการภูมิ, {} in อรูปภูมิ
GROUP_B_IDS = (
    LOBHAMULA + MOHAMULA + MANODVARAVAJJANA + MAHAKUSALA + MAHAKIRIYA
    + ARUPA_KUSALA + ARUPA_KIRIYA + LOKUTTARA_OTHER
)
# C. ไม่อาศัยวัตถุรูปแน่นอน -- empty วัตถุ-set (อรูปภูมิ only)
GROUP_C_IDS = ARUPA_VIPAKA

# per-วัตถุ headline "การจำแนกจิต ๔๓ ที่อาศัยวัตถุรูปเกิดแน่นอน" (L1503-L1512),
# ๘๙-basis: จักขุ..กายวัตถุ ๒ each, หทัยวัตถุ ๓๓
EXPECT_A89 = {"cakkhu": 2, "sota": 2, "ghana": 2, "jivha": 2, "kaya": 2, "hadaya": 33}
# same table นับพิสดาร (โสดาปัตติมรรค ๑ -> ๕): หทัยวัตถุ ๓๗
EXPECT_A121 = {"cakkhu": 2, "sota": 2, "ghana": 2, "jivha": 2, "kaya": 2, "hadaya": 37}
# full-matrix per-วัตถุ over all ๑๒๑ จิต -- the build_data.py `expect` gate
EXPECT_CITTA = {"cakkhu": 2, "sota": 2, "ghana": 2, "jivha": 2, "kaya": 2, "hadaya": 107}

CITTA_GROUPINGS = [
    {"id": "anissita", "thai": "จิตที่ไม่อาศัยวัตถุรูปเกิด (อรูปวิปาก ๔)", "size": 0, "expect": 4},
    {"id": "ekavatthu", "thai": "จิตที่อาศัยวัตถุรูปเกิด (วัตถุเดียว)", "size": 1, "expect": 117},
]
CETA_GROUPINGS = [
    {"id": "eka", "thai": "เจตสิกที่อาศัยเฉพาะหทัยวัตถุ", "size": 1, "expect": 45},
    {"id": "cha", "thai": "เจตสิกที่อาศัยได้ทั้ง ๖ วัตถุ (สัพพจิตตสาธารณ ๗)", "size": 6, "expect": 7},
]

GATHA = (
    "ฉ วตฺถุํ นิสฺสิตา กาเม สตฺต รูเป จตุพฺพิธา / ติวตฺถุํ นิสฺสิตารูเป ธาตุวกานิสฺสิตา มตา ฯ\n"
    "เตจตฺตาลีส นิสฺสาย เทฺวจตฺตาลีส ชายเร / นิสฺสาย จ อนิสฺสาย ปการุปฺปา อนิสฺสิตา ฯ"
)
NOTES = [
    {"t": "<strong>วัตถุ ๖</strong> — รูปที่เป็นที่อาศัยเกิดของจิตเจตสิก",
     "sub": [
         "จักขุ โสต ฆาน ชิวหา กายวัตถุ — องค์ธรรมคือ ปสาทรูป ๕",
         "หทัยวัตถุ — องค์ธรรมคือ หทยรูป",
     ]},
    {"t": "<strong>จิต</strong> — อาศัยวัตถุได้อย่างมากเพียงวัตถุเดียว: อาศัยวัตถุรูป ๑๑๗ · ไม่อาศัยวัตถุรูป (อรูปวิปาก ๔) = ๐ วัตถุ (นับพิสดาร ๑๒๑)",
     "sub": [
         "คาถาแบ่ง ๓ พวกตามความแน่นอน — (๑) อาศัยแน่นอน ๔๓ ในนัย ๘๙ / ๔๗ พิสดาร: ทวิปัญจวิญญาณ ๑๐ อาศัยปสาทของตน ที่เหลืออาศัยหทัยวัตถุ เพราะเกิดเฉพาะปัญจโวการภูมิ",
         "(๒) อาศัยบ้างไม่อาศัยบ้าง ๔๒ ในนัย ๘๙ / ๗๐ พิสดาร: อาศัยหทัยวัตถุเมื่อเกิดในปัญจโวการภูมิ ไม่อาศัยเมื่อเกิดในอรูปภูมิ",
         "(๓) ไม่อาศัยแน่นอน ๔ (อรูปวิปาก)",
         "ส่วนต่าง ๘๙ ↔ พิสดาร ๑๒๑ อยู่ที่โลกุตตรจิต: โสดาปัตติมรรค ๑→๕ (พวกที่ ๑), โลกุตตรอื่น ๗→๓๕ (พวกที่ ๒); หทัยวัตถุ ๗๕ ดวงในนัย ๘๙ (แน่นอน ๓๓ + ไม่แน่นอน ๔๒) นับพิสดารเป็น ๑๐๗",
     ]},
    {"t": "<strong>เจตสิก</strong> — สัพพจิตตสาธารณ ๗ อาศัยได้ทั้ง ๖ วัตถุ (ประกอบกับทวิปัญจวิญญาณ ๑๐); เจตสิกที่เหลือ ๔๕ อาศัยเฉพาะหทัยวัตถุ — และทั้ง ๕๒ ดวงอาศัยหทัยวัตถุได้",
     "sub": [
         "โทจตุก ๔ อัปปมัญญา ๒ อาศัยวัตถุรูปแน่นอน (เกิดเฉพาะปัญจโวการภูมิ), อีก ๔๖ ดวงไม่แน่นอน",
     ]},
    "เว็บนี้ไม่ได้ทำเอกันตะ (อาศัยแน่นอน) / อเนกันตะ (อาศัยไม่แน่นอน) เป็นแกนย่อย — ดูการแบ่ง ๓ พวกข้างบนแทน",
]


def main():
    para = yaml.safe_load(open(PARAMATTHA, encoding="utf-8"))
    citta_ids = [c["id"] for c in para["citta"]]
    citta_id_set = set(citta_ids)
    cetasikas = para["cetasika"]
    ceta_ids = [c["id"] for c in cetasikas]
    by_group = {}
    for c in cetasikas:
        by_group.setdefault(c["group"], []).append(c["id"])

    # ---- id-group length gates ----
    for name, lst, n in [
        ("LOBHAMULA", LOBHAMULA, 8), ("DOSAMULA", DOSAMULA, 2), ("MOHAMULA", MOHAMULA, 2),
        ("MANODHATU", MANODHATU, 3), ("SANTIRANA3", SANTIRANA3, 3),
        ("MAHAKUSALA", MAHAKUSALA, 8), ("MAHAVIPAKA", MAHAVIPAKA, 8),
        ("MAHAKIRIYA", MAHAKIRIYA, 8), ("RUPAVACARA", RUPAVACARA, 15),
        ("ARUPA_KUSALA", ARUPA_KUSALA, 4), ("ARUPA_VIPAKA", ARUPA_VIPAKA, 4),
        ("ARUPA_KIRIYA", ARUPA_KIRIYA, 4), ("LOKUTTARA", LOKUTTARA, 40),
        ("SOTAPATTI_MAGGA", SOTAPATTI_MAGGA, 5), ("LOKUTTARA_OTHER", LOKUTTARA_OTHER, 35),
        ("GROUP_B_IDS", GROUP_B_IDS, 70), ("GROUP_C_IDS", GROUP_C_IDS, 4),
    ]:
        if len(lst) != n:
            die(f"{name}: expected {n} ids, got {len(lst)}")

    used = set(GROUP_B_IDS) | set(GROUP_C_IDS)
    for _, lst in GROUP_A:
        used |= set(lst)
    for cid in used:
        if cid not in citta_id_set:
            die(f"vatthu source names non-citta id {cid!r}")
    if used != citta_id_set:
        die(f"vatthu จิต partition misses/adds ids: {citta_id_set ^ used}")

    # ---- จิต by วัตถุ ----
    citta_vatthu = {cid: [] for cid in citta_ids}
    group_a_ids = []
    for cats, cids in GROUP_A:
        for cid in cids:
            group_a_ids.append(cid)
            for v in cats:
                if v not in citta_vatthu[cid]:
                    citta_vatthu[cid].append(v)
    for cid in GROUP_B_IDS:
        citta_vatthu[cid] = ["hadaya"]
    for cid in GROUP_C_IDS:
        citta_vatthu[cid] = []
    citta_vatthu = {cid: ordered(v) for cid, v in citta_vatthu.items()}

    if len(group_a_ids) != len(set(group_a_ids)):
        die("GROUP_A lists a จิต twice")
    if len(group_a_ids) != 47:
        die(f"GROUP_A (พิสดาร) should be ๔๗ จิต, got {len(group_a_ids)}")

    # ๘๙-basis คาถา totals (โสดาปัตติมรรค ๑, โลกุตตรอื่น ๗)
    a89 = len(group_a_ids) - len(SOTAPATTI_MAGGA) + 1        # 47 - 5 + 1
    b89 = len(GROUP_B_IDS) - len(LOKUTTARA_OTHER) + 7        # 70 - 35 + 7
    c89 = len(GROUP_C_IDS)
    if (a89, b89, c89) != (43, 42, 4):
        die(f"คาถา 3-way (นัย ๘๙) = {a89}/{b89}/{c89} != 43/42/4 "
            "(เตจตฺตาลีส เทฺวจตฺตาลีส ... ปการุปฺปา อนิสฺสิตา)")
    if a89 + b89 + c89 != 89:
        die(f"นัย ๘๙ total {a89 + b89 + c89} != 89")

    # per-วัตถุ headline for GROUP_A -- ๘๙ and ๑๒๑ bases
    got_a121 = Counter()
    for cid in group_a_ids:
        got_a121.update(citta_vatthu[cid])
    got_a121 = {k: got_a121.get(k, 0) for k in VATTHU_ORDER}
    if got_a121 != EXPECT_A121:
        die(f"GROUP_A per-วัตถุ (พิสดาร) {got_a121} != textbook {EXPECT_A121}")
    got_a89 = dict(got_a121)
    got_a89["hadaya"] = got_a121["hadaya"] - (len(SOTAPATTI_MAGGA) - 1)  # 37 -> 33
    if got_a89 != EXPECT_A89:
        die(f"GROUP_A per-วัตถุ (นัย ๘๙) {got_a89} != textbook headline {EXPECT_A89}")

    # full-matrix per-วัตถุ over all ๑๒๑ จิต
    got = Counter()
    for v in citta_vatthu.values():
        got.update(v)
    got = {k: got.get(k, 0) for k in VATTHU_ORDER}
    if got != EXPECT_CITTA:
        die(f"per-วัตถุ จิต totals (๑๒๑) {got} != {EXPECT_CITTA}")

    size_c = Counter(len(v) for v in citta_vatthu.values())
    for g in CITTA_GROUPINGS:
        if size_c.get(g["size"], 0) != g["expect"]:
            die(f"จิต วัตถุ-set-size {g['size']} = {size_c.get(g['size'], 0)} != {g['expect']}")
    if sum(size_c.values()) != 121 or set(size_c) - {0, 1}:
        die(f"จิต วัตถุ-set-size distribution unexpected: {dict(size_c)}")
    anissita = sorted(cid for cid, v in citta_vatthu.items() if not v)
    if set(anissita) != set(ARUPA_VIPAKA):
        die(f"ไม่อาศัยวัตถุรูปแน่นอน should be อรูปวิปาก ๔, got {anissita}")

    # ---- เจตสิก by วัตถุ (L1535-L1549) ----
    sabba7 = by_group["sabbacitta-sadharana"]
    if len(sabba7) != 7:
        die(f"สัพพจิตตสาธารณเจตสิก != 7: {sabba7}")
    dojatuka = by_group["dosa-catuka"]        # โทสะ อิสสา มัจฉริยะ กุกกุจจะ
    appamanna = by_group["appamanna"]         # กรุณา มุทิตา
    if len(dojatuka) != 4 or len(appamanna) != 2:
        die(f"โทจตุกเจตสิก/อัปปมัญญาเจตสิก != 4/2: {dojatuka} {appamanna}")

    authored = {}
    for cid in ceta_ids:
        authored[cid] = ["hadaya"]
    for cid in sabba7:
        authored[cid] = list(VATTHU_ORDER)

    # text checks: "อาศัยวัตถุรูปแน่นอน ๖" = โทจตุกะ ๔ + อัปปมัญญา ๒ ; "ไม่แน่นอน ๔๖"
    nissita_certain = set(dojatuka) | set(appamanna)
    if len(nissita_certain) != 6:
        die(f"เจตสิก อาศัยวัตถุรูปแน่นอน != 6: {sorted(nissita_certain)}")
    if len(set(ceta_ids) - nissita_certain) != 46:
        die(f"เจตสิก อาศัยวัตถุรูปไม่แน่นอน != 46")

    size_e = Counter(len(v) for v in authored.values())
    for g in CETA_GROUPINGS:
        if size_e.get(g["size"], 0) != g["expect"]:
            die(f"เจตสิก วัตถุ-set-size {g['size']} = {size_e.get(g['size'], 0)} != {g['expect']}")
    if sum(size_e.values()) != 52 or set(size_e) - {1, 6}:
        die(f"เจตสิก วัตถุ-set-size distribution unexpected: {dict(size_e)}")

    ceta_expect = Counter()
    for v in authored.values():
        ceta_expect.update(v)
    ceta_expect = {k: ceta_expect.get(k, 0) for k in VATTHU_ORDER}
    if ceta_expect != {"cakkhu": 7, "sota": 7, "ghana": 7, "jivha": 7, "kaya": 7, "hadaya": 52}:
        die(f"per-วัตถุ เจตสิก totals {ceta_expect} != จักขุ..กาย ๗, หทัย ๕๒")

    def categories():
        return [{"id": k, "thai": VATTHU_THAI[k]} for k in VATTHU_ORDER]

    vatthu = {
        "id": "vatthu",
        "thai": "วัตถุสังคหะ",
        "source": "reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L1421-L1550",
        "gatha": GATHA,
        "notes": NOTES,
        "citta": {
            "axis": "วัตถุ ๖ ที่อาศัยเกิด",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CITTA_GROUPINGS,
            "expect": {k: EXPECT_CITTA[k] for k in VATTHU_ORDER},
            "assignments": [{"ref": cid, "cats": citta_vatthu[cid]} for cid in citta_ids],
        },
        "cetasika": {
            "axis": "วัตถุ ๖ ที่อาศัยเกิด",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CETA_GROUPINGS,
            "expect": ceta_expect,
            "assignments": [{"ref": cid, "cats": ordered(authored[cid])} for cid in ceta_ids],
        },
    }

    header = (
        "# ปริจเฉทที่ ๓ ปกิณณกสังคหะ -- scheme fragment: วัตถุสังคหะ.\n"
        "#\n"
        "# GENERATED by scripts/derive_p3_vatthu.py (verified against\n"
        "# reference/01-...md L1421-L1550: the คาถา 3-way split (43/42/4 in the\n"
        "# ๘๙ system), the per-วัตถุ headline for จิต ๔๓ แน่นอน, and the full\n"
        "# ๑๒๑-basis per-วัตถุ totals must all reproduce; no julatri cross-check\n"
        "# -- julatri has no วัตถุ lens).\n"
        "# Re-run that script to regenerate; do not hand-edit.\n"
        "#\n"
        f"#   จิต by วัตถุ set-size: {dict(sorted(size_c.items()))}  (อรูปวิปาก ๐ = 4, วัตถุเดียว = 117)\n"
        f"#   จิต per-วัตถุ (๑๒๑): {got}  (จักขุ..กาย ๒, หทัย ๑๐๗)\n"
        f"#   คาถา 3-way (นัย ๘๙): แน่นอน {a89} / ไม่แน่นอน {b89} / ไม่อาศัย {c89}  (= 89)\n"
        f"#   จิต ๔๓ แน่นอน per-วัตถุ (นัย ๘๙): {got_a89}  (จักขุ..กาย ๒, หทัย ๓๓)\n"
        f"#   เจตสิก by วัตถุ set-size: {dict(sorted(size_e.items()))}  (1/6 = 45/7)\n"
        f"#   เจตสิก per-วัตถุ: {ceta_expect}  (จักขุ..กาย ๗, หทัย ๕๒)\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(vatthu, f, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)

    print(f"Wrote {OUT}")
    print(f"  จิต ๑๒๑ by วัตถุ set-size: {dict(sorted(size_c.items()))}  (ไม่อาศัย/วัตถุเดียว = 4/117)")
    print(f"  จิต per-วัตถุ (๑๒๑): {got}  (จักขุ..กายวัตถุ ๒, หทัยวัตถุ ๑๐๗)")
    print(f"  คาถา 3-way (นัย ๘๙): อาศัยแน่นอน {a89} / อาศัยไม่แน่นอน {b89} / ไม่อาศัยแน่นอน {c89}")
    print(f"  เจตสิก ๕๒ by วัตถุ set-size: {dict(sorted(size_e.items()))}  (เฉพาะหทัย/ครบ ๖ = 45/7)")
    print(f"  เจตสิก per-วัตถุ: {ceta_expect}")


if __name__ == "__main__":
    main()
