#!/usr/bin/env python3
"""
Generate data/p3/arammana.yaml -- the อารัมมณสังคหะ scheme fragment for /julator/p3.

Source: reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L901-L1417 (the authoritative text).
There is no julatri cross-check here (julatri has no อารมณ์ lens).  Verification is
internal, the same way derive_p3_dvara.py checks itself:

  * จิต by อารมณ์ ๖ (each จิต takes a SET of 1/5/6 of รูป สัทท คันธ รส โผฏฐัพพ
    ธัมมารมณ์) is built from the per-นัย breakdown (L997-L1009, L1024-L1101):
        ทวิปัญจวิญญาณจิต ๑๐  -> ๑ วิสยารมณ์ ต่อดวง            (L1028-1041)
        มโนธาตุ ๓            -> ปัญจารมณ์ ๕ (ไม่มีธัมมารมณ์)   (L1043-1044, L1259)
        อารมณ์ครบ ๖ ๔๓ ดวง  = สันตีรณ ๓ + มหาวิปาก ๘ + หสิตุปปาท ๑ (L1046)
                              + อกุศล ๑๒ + มหากุศล ๘ + มหากิริยา ๘
                              + มโนทวาราวัชชน ๑ + อภิญญา ๒       (L1089-1100)
        ธัมมารมณ์อย่างเดียว ๖๕ = รูปาวจร ๑๓ (ฌาน ๑-๔ กุศล/วิปาก/กิริยา ๑๒
                              + ปัญจมฌานวิปาก ๑) + อรูป ๑๒ + โลกุตตร ๔๐
    Asserted: set-size buckets 1/5/6 = 75/3/43, AND the per-อารมณ์ totals
    reproduce the textbook headline "การจำแนกจิตที่รับอารมณ์ โดยแน่นอนและไม่
    แน่นอนรวมกัน" (L1343-1362):
        รูป/สัทท/คันธ/รส/โผฏฐัพพารมณ์ ๔๘ ดวงเท่ากัน, ธัมมารมณ์ ๗๖ (ระบบ ๘๙)
        = ๑๐๘ (นับพิสดาร ๑๒๑; โลกุตตร ๔๐ แทน ๘).
    The main อารัมมณ-คาถา (L992-995, and the ปัญหา at L1744-1746) enumerates
    the ๗ นัย เอกันตะ ๔ / อเนกันตะ ๓ -- ปญฺจวีส ๒๕ · ฉ ๖ · เอกวีสติ ๒๑ ·
    อฏฺฐ ๘ · วีส ๒๐ · ปญฺจ ๕ · ฉ ๖ (รวม ๙๑; นัย ๔ = ๘ ในระบบ ๘๙, ๔๐ ในพิสดาร).
    That split is asserted here as a die() gate (it cannot be a groupings
    bucket -- build_data groupings key on cats-set size only, and two นัย
    share the same size-6 set).  L1227 (ธัมมารมณ์อย่างเดียว ๓๕) and L1362
    (ธัมมารมณ์ ๗๖) are re-derived on the ๘๙ basis as extra gates.
  * เจตสิก by อารมณ์ ๖ (L1364-L1416, "การจำแนกเจตสิก โดยอารมณ์ ๒๑"):
    L1408-1409 -- รูป..โผฏฐัพพารมณ์ ไม่แน่นอน ๕๐ (เว้น อัปปมัญญา ๒), แน่นอน ไม่มี.
    L1414-1415 -- ธัมมารมณ์ แน่นอน ๒ (อัปปมัญญา ๒) + ไม่แน่นอน ๕๐ = ๕๒.
    So อัปปมัญญาเจตสิก ๒ (กรุณา มุทิตา) take {ธัมมารมณ์} only (a สัตวบัญญัติ);
    the other ๕๐ take all ๖.  Buckets: ๑ อารมณ์ = ๒, ๖ อารมณ์ = ๕๐.  Every
    เจตสิก takes an object -- there is NO empty set here (unlike เวทนาเจตสิก
    in เวทนาสังคหะ, which does not co-arise with itself).

อภิญญาจิต ๒ = รูปาวจรปัญจมฌานกุศลจิต / กิริยาจิต (no separate id in the ๑๒๑
space).  In their abhiññā role they know รูป เสียง จิตของผู้อื่น etc., so in a
per-id set model these two ids carry the full อารมณ์ ๖ set; their pure-jhāna
บัญญัติ (ธัมมารมณ์) object is the reason the textbook can also count them under
เอกันตะ นัย ๓.  The other รูปาวจรจิต ๑๓ and อรูปาวจรจิต ๑๒ take ธัมมารมณ์ only.

กาล ๓ (อดีต/ปัจจุบัน/อนาคต/กาลวิมุตต), เอกันตะ–อเนกันตะ (๗ นัย), and อารมณ์
พิสดาร ๒๑ are large parts of the text but are orthogonal axes, not a coarsening
of อารมณ์ ๖ (no clean views/collapse), so they are described in the scheme note
and deferred -- exactly as ทวารสังคหะ deferred เอกันตะ/อเนกันตะ.

Run: python3 scripts/derive_p3_arammana.py   (then: python3 scripts/build_data.py)
"""
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PARAMATTHA = ROOT / "data" / "paramattha.yaml"
HETU_YAML = ROOT / "data" / "p3" / "hetu.yaml"
OUT = ROOT / "data" / "p3" / "arammana.yaml"

ARAMMANA_ORDER = ["rupa", "satta", "gandha", "rasa", "photthabba", "dhamma"]
ARAMMANA_THAI = {
    "rupa": "รูปารมณ์", "satta": "สัททารมณ์", "gandha": "คันธารมณ์",
    "rasa": "รสารมณ์", "photthabba": "โผฏฐัพพารมณ์", "dhamma": "ธัมมารมณ์",
}
PANCA = ["rupa", "satta", "gandha", "rasa", "photthabba"]
ALL6 = list(ARAMMANA_ORDER)


def die(msg):
    sys.exit(f"derive_p3_arammana: {msg}")


def ordered(xs):
    return sorted(set(xs), key=ARAMMANA_ORDER.index)


# ---- citta id groups (from data/paramattha.yaml naming) ----
LOBHAMULA = [f"lobhamula-{i}" for i in range(1, 9)]
DOSAMULA = [f"dosamula-{i}" for i in range(1, 3)]
MOHAMULA = [f"mohamula-{i}" for i in range(1, 3)]
AKUSALA = LOBHAMULA + DOSAMULA + MOHAMULA  # 12

DVIPANCA = {
    "cakkhu": ["ahetuka-akusalavipaka-cakkhu", "ahetuka-kusalavipaka-cakkhu"],
    "sota": ["ahetuka-akusalavipaka-sota", "ahetuka-kusalavipaka-sota"],
    "ghana": ["ahetuka-akusalavipaka-ghana", "ahetuka-kusalavipaka-ghana"],
    "jivha": ["ahetuka-akusalavipaka-jivha", "ahetuka-kusalavipaka-jivha"],
    "kaya": ["ahetuka-akusalavipaka-kaya", "ahetuka-kusalavipaka-kaya"],
}
DVIPANCA_ALL = [cid for k in ("cakkhu", "sota", "ghana", "jivha", "kaya") for cid in DVIPANCA[k]]  # 10
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
# ญาณสัมปยุตต = ดวงที่ ๑ ๒ ๕ ๖  ·  ญาณวิปปยุตต = ดวงที่ ๓ ๔ ๗ ๘
# (cross-checked below against data/p3/hetu.yaml: ญาณสัมปยุตต <=> มีอโมหเหตุ)
MAHAKUSALA_NANASAMP = [f"mahakusala-{i}" for i in (1, 2, 5, 6)]
MAHAKUSALA_NANAVIPP = [f"mahakusala-{i}" for i in (3, 4, 7, 8)]
MAHAKIRIYA_NANASAMP = [f"mahakiriya-{i}" for i in (1, 2, 5, 6)]
MAHAKIRIYA_NANAVIPP = [f"mahakiriya-{i}" for i in (3, 4, 7, 8)]

JHANA5 = ["ปฐมฌาน", "ทุติยฌาน", "ตติยฌาน", "จตุตถฌาน", "ปัญจมฌาน"]
JHANA14 = JHANA5[:4]
RUPA_KUSALA = [f"rupa-{j}-kusala" for j in JHANA5]
RUPA_VIPAKA = [f"rupa-{j}-vipaka" for j in JHANA5]
RUPA_KIRIYA = [f"rupa-{j}-kiriya" for j in JHANA5]
RUPA_ALL15 = RUPA_KUSALA + RUPA_VIPAKA + RUPA_KIRIYA  # 15
ABHINNA_KUSALA = ["rupa-ปัญจมฌาน-kusala"]
ABHINNA_KIRIYA = ["rupa-ปัญจมฌาน-kiriya"]
ABHINNA = ABHINNA_KUSALA + ABHINNA_KIRIYA  # 2
# รูปาวจรจิต ๑๓ ที่รับธัมมารมณ์ (บัญญัติ) อย่างเดียว: ฌาน ๑-๔ ทั้ง ๓ ชาติ + ปัญจมฌานวิปาก
RUPA_DHAMMA_ONLY = (
    [f"rupa-{j}-{k}" for j in JHANA14 for k in ("kusala", "vipaka", "kiriya")]
    + ["rupa-ปัญจมฌาน-vipaka"]
)  # 13

ARUPA_NAMES = ["akasanancayatana", "vinnanancayatana", "akincannayatana", "nevasannanasannayatana"]
ARUPA = {n: [f"arupa-{n}-{k}" for k in ("kusala", "vipaka", "kiriya")] for n in ARUPA_NAMES}
ARUPA_ALL = [cid for n in ARUPA_NAMES for cid in ARUPA[n]]  # 12

PHASES = ["sotapatti", "sakadagami", "anagami", "arahatta"]
LOKUTTARA = [f"{p}-{mp}-{j}" for p in PHASES for mp in ("magga", "phala") for j in JHANA5]  # 40

# per-citta อารมณ์ ๖ set, accumulated (from the per-นัย breakdown, L997-L1101)
ARAMMANA_SOURCES = [
    (["rupa"], DVIPANCA["cakkhu"]),
    (["satta"], DVIPANCA["sota"]),
    (["gandha"], DVIPANCA["ghana"]),
    (["rasa"], DVIPANCA["jivha"]),
    (["photthabba"], DVIPANCA["kaya"]),
    (PANCA, MANODHATU),  # ปัญจารมณ์ ๕ (ไม่มีธัมมารมณ์)
    (ALL6,  # อารมณ์ครบ ๖ -- ๔๓ ดวง
     AKUSALA + SANTIRANA3 + MAHAVIPAKA + HASITUPPADA
     + MAHAKUSALA + MAHAKIRIYA + MANODVARAVAJJANA + ABHINNA),
    (["dhamma"], RUPA_DHAMMA_ONLY + ARUPA_ALL + LOKUTTARA),  # ธัมมารมณ์อย่างเดียว -- ๖๕ ดวง
]
EXPECT_CITTA = {"rupa": 48, "satta": 48, "gandha": 48, "rasa": 48, "photthabba": 48, "dhamma": 108}
CITTA_GROUPINGS = [
    {"id": "eka", "thai": "จิตที่รับอารมณ์ได้ประเภทเดียว", "size": 1, "expect": 75},
    {"id": "panca", "thai": "จิตที่รับปัญจารมณ์ ๕ (มโนธาตุ ๓)", "size": 5, "expect": 3},
    {"id": "cha", "thai": "จิตที่รับอารมณ์ครบ ๖", "size": 6, "expect": 43},
]

# the ๗ นัย เอกันตะ ๔ / อเนกันตะ ๓ (main อารัมมณ-คาถา L992-995; ปัญหา L1744-1746).
# Overlapping lists on purpose: อภิญญาจิต ๒ fall in both นัย ๓ and นัย ๖/๗
# (the คาถา total is ๙๑, i.e. ๘๙ + อภิญญา ๒ นับซ้ำ).
CATHA_NAYA = {
    1: DVIPANCA_ALL + MANODHATU + SANTIRANA3 + MAHAVIPAKA + HASITUPPADA,       # กามารมณ์ แน่นอน ๒๕
    2: ARUPA["vinnanancayatana"] + ARUPA["nevasannanasannayatana"],           # มหัคคตารมณ์ แน่นอน ๖
    3: RUPA_ALL15 + ARUPA["akasanancayatana"] + ARUPA["akincannayatana"],     # บัญญัติอารมณ์ แน่นอน ๒๑
    4: LOKUTTARA,                                                             # นิพพานารมณ์ แน่นอน ๘ (๔๐ พิสดาร)
    5: AKUSALA + MAHAKUSALA_NANAVIPP + MAHAKIRIYA_NANAVIPP,                   # อเนกันตะ ๒๐
    6: MAHAKUSALA_NANASAMP + ABHINNA_KUSALA,                                  # อเนกันตะ ๕
    7: MAHAKIRIYA_NANASAMP + ABHINNA_KIRIYA + MANODVARAVAJJANA,               # อเนกันตะ ๖
}
EXPECT_NAYA = {1: 25, 2: 6, 3: 21, 4: 40, 5: 20, 6: 5, 7: 6}  # นัย ๔ = ๘ ในระบบ ๘๙

CETA_GROUPINGS = [
    {"id": "eka", "thai": "เจตสิกที่รับธัมมารมณ์อย่างเดียว (อัปปมัญญา ๒)", "size": 1, "expect": 2},
    {"id": "cha", "thai": "เจตสิกที่รับอารมณ์ได้ทั้ง ๖ (อีก ๕๐)", "size": 6, "expect": 50},
]

GATHA = (
    "ปญฺจวีส ปริตฺตมฺหิ ฉ จิตฺตานิ มหคฺคเต / เอกวีสติ โวหาเร อฏฺฐ นิพฺพานโคจเร\n"
    "วีสานุตฺตรมุตฺตมฺหิ อฏฺฐวีสติ กามโต / ปญฺจ สพฺพตฺถ ฉจฺเจติ สตฺตธา ตตฺถ สงฺคโห"
)
NOTES = [
    {"t": "<strong>อารมณ์ ๖</strong> — ธรรมชาติที่จิตเจตสิกยึดหน่วง",
     "sub": [
         "รูปารมณ์ (สี) · สัททารมณ์ (เสียง) · คันธารมณ์ (กลิ่น) · รสารมณ์ (รส) · โผฏฐัพพารมณ์ (เย็น ร้อน อ่อน แข็ง หย่อน ตึง)",
         "ธัมมารมณ์ — องค์ธรรมคือ จิต เจตสิก ปสาทรูป ๕ สุขุมรูป ๑๖ นิพพาน บัญญัติ",
     ]},
    {"t": "<strong>จิต</strong> — จำแนกโดยอารมณ์ ๖ ที่รับได้ (๑ / ๕ / ๖ อารมณ์ต่อดวง)",
     "sub": [
         "รับประเภทเดียว ๗๕ · รับปัญจารมณ์ ๕ (มโนธาตุ ๓) ๓ · รับครบ ๖ ๔๓",
         "รวมแต่ละอารมณ์: รูป–โผฏฐัพพารมณ์ ๔๘ ดวงเท่ากัน; ธัมมารมณ์ ๑๐๘ (นับพิสดาร ๑๒๑; ๗๖ ในระบบ ๘๙ โดยโลกุตตรจิต ๘ แทน ๔๐)",
         "อภิญญาจิต ๒ (รูปาวจรปัญจมฌานกุศล/กิริยา) จัดเข้ากลุ่มรับอารมณ์ครบ ๖ เพราะทำหน้าที่อภิญญา รู้รูป เสียง จิตของผู้อื่น ฯลฯ (ในนัย ๘๙ ตำรานับอภิญญาแยกต่างหากเป็นนัย ๙๑)",
     ]},
    {"t": "<strong>เจตสิก</strong> — อัปปมัญญา ๒ (กรุณา มุทิตา) รับธัมมารมณ์ (สัตวบัญญัติ) อย่างเดียว; อีก ๕๐ รับได้ทั้ง ๖",
     "sub": [
         "ทุกดวงมีอารมณ์เสมอ ไม่มีดวงที่ไม่รับอารมณ์",
     ]},
    "เว็บนี้ยังไม่ได้แยก กาล ๓ (อดีต ปัจจุบัน อนาคต กาลวิมุตต), เอกันตะ ๔ – อเนกันตะ ๓ (๗ นัย ตามคาถา ปญฺจวีส… = ๒๕/๖/๒๑/๘/๒๐/๕/๖ รวม ๙๑) และอารมณ์พิสดาร ๒๑ ซึ่งเป็นแกนคนละแกนกับอารมณ์ ๖",
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

    # ---- id-group length gates (die() up front, like derive_p3_dvara.py) ----
    for name, lst, n in [
        ("AKUSALA", AKUSALA, 12), ("DVIPANCA_ALL", DVIPANCA_ALL, 10),
        ("MANODHATU", MANODHATU, 3), ("SANTIRANA3", SANTIRANA3, 3),
        ("MAHAKUSALA", MAHAKUSALA, 8), ("MAHAVIPAKA", MAHAVIPAKA, 8),
        ("MAHAKIRIYA", MAHAKIRIYA, 8), ("RUPA_ALL15", RUPA_ALL15, 15),
        ("ABHINNA", ABHINNA, 2), ("RUPA_DHAMMA_ONLY", RUPA_DHAMMA_ONLY, 13),
        ("ARUPA_ALL", ARUPA_ALL, 12), ("LOKUTTARA", LOKUTTARA, 40),
        ("MAHAKUSALA_NANASAMP", MAHAKUSALA_NANASAMP, 4),
        ("MAHAKIRIYA_NANASAMP", MAHAKIRIYA_NANASAMP, 4),
    ]:
        if len(lst) != n:
            die(f"{name}: expected {n} ids, got {len(lst)}")

    used = set()
    for _, lst in ARAMMANA_SOURCES:
        used |= set(lst)
    if used != citta_id_set:
        die(f"อารมณ์ sources do not partition จิต ๑๒๑: "
            f"missing {sorted(citta_id_set - used)}, extra {sorted(used - citta_id_set)}")
    seen = []
    for _, lst in ARAMMANA_SOURCES:
        seen += lst
    if len(seen) != 121:
        die(f"อารมณ์ sources overlap: {len(seen)} assignments for 121 จิต")

    # ---- cross-check ญาณสัมปยุตต indices against hetu.yaml (อโมหเหตุ) ----
    if HETU_YAML.exists():
        hetu = yaml.safe_load(open(HETU_YAML, encoding="utf-8"))
        hcats = {a["ref"]: set(a["cats"]) for a in hetu["citta"]["assignments"]}
        for cid in MAHAKUSALA + MAHAKIRIYA:
            want_samp = cid in (MAHAKUSALA_NANASAMP + MAHAKIRIYA_NANASAMP)
            has_amoha = "amoha" in hcats.get(cid, set())
            if want_samp != has_amoha:
                die(f"ญาณสัมปยุตต mismatch vs hetu.yaml for {cid}: "
                    f"nanasampayutta={want_samp} but amoha={has_amoha}")

    # ---- คาถา ๗ นัย เอกันตะ ๔ / อเนกันตะ ๓ (L992-995, L1744-1746) ----
    for k in range(1, 8):
        lst = CATHA_NAYA[k]
        bad = [x for x in lst if x not in citta_id_set]
        if bad:
            die(f"นัย {k} names non-citta id {bad}")
        if len(set(lst)) != len(lst):
            die(f"นัย {k} has duplicate ids")
        if len(lst) != EXPECT_NAYA[k]:
            die(f"นัย {k} = {len(lst)} != คาถา {EXPECT_NAYA[k]}")
    catha_total_91 = sum(EXPECT_NAYA.values()) - EXPECT_NAYA[4] + 8  # 25+6+21+8+20+5+6
    if catha_total_91 != 91:
        die(f"คาถา ๗ นัย total (ระบบ ๘๙+อภิญญา ๒) = {catha_total_91} != 91")

    # ---- จิต by อารมณ์ ๖ ----
    citta_aram = {cid: [] for cid in citta_ids}
    for cats, cids in ARAMMANA_SOURCES:
        for cid in cids:
            for a in cats:
                if a not in citta_aram[cid]:
                    citta_aram[cid].append(a)
    citta_aram = {cid: ordered(v) for cid, v in citta_aram.items()}

    if any(not v for v in citta_aram.values()):
        die("จิต with no อารมณ์ (text says every จิต takes one): "
            f"{[c for c, v in citta_aram.items() if not v]}")

    got = Counter()
    for v in citta_aram.values():
        got.update(v)
    got = {k: got.get(k, 0) for k in ARAMMANA_ORDER}
    if got != EXPECT_CITTA:
        die(f"per-อารมณ์ จิต totals {got} != textbook headline {EXPECT_CITTA}")

    size_c = Counter(len(v) for v in citta_aram.values())
    for g in CITTA_GROUPINGS:
        if size_c.get(g["size"], 0) != g["expect"]:
            die(f"จิต อารมณ์-set-size {g['size']} = {size_c.get(g['size'], 0)} != {g['expect']}")
    if sum(size_c.values()) != 121 or set(size_c) - {1, 5, 6}:
        die(f"จิต อารมณ์-set-size distribution unexpected: {dict(size_c)}")

    # ---- ๘๙-basis cross-checks (L1227, L1362) ----
    dhamma_only_89 = len(RUPA_DHAMMA_ONLY) + len(ABHINNA) + len(ARUPA_ALL) + 8  # 13+2+12+8
    if dhamma_only_89 != 35:
        die(f"ธัมมารมณ์อย่างเดียว (ระบบ ๘๙) = {dhamma_only_89} != 35 (L1227)")
    cha6_count = size_c[6]  # 43 -- the all-6 group carries no โลกุตตร, unchanged in ๘๙
    dhamma_total_89 = cha6_count + len(RUPA_DHAMMA_ONLY) + len(ARUPA_ALL) + 8  # 43+13+12+8
    if dhamma_total_89 != 76:
        die(f"ธัมมารมณ์ รวม (ระบบ ๘๙) = {dhamma_total_89} != 76 (L1362)")

    # ---- เจตสิก by อารมณ์ ๖ (L1364-L1416) ----
    if len(by_group["appamanna"]) != 2:
        die(f"อัปปมัญญาเจตสิก != 2: {by_group['appamanna']}")
    ceta_aram = {}
    for cid in ceta_ids:
        ceta_aram[cid] = ["dhamma"] if cid in by_group["appamanna"] else list(ALL6)

    size_e = Counter(len(v) for v in ceta_aram.values())
    for g in CETA_GROUPINGS:
        if size_e.get(g["size"], 0) != g["expect"]:
            die(f"เจตสิก อารมณ์-set-size {g['size']} = {size_e.get(g['size'], 0)} != text {g['expect']}")
    if sum(size_e.values()) != 52 or set(size_e) - {1, 6}:
        die(f"เจตสิก อารมณ์-set-size distribution unexpected: {dict(size_e)}")

    ceta_expect = Counter()
    for v in ceta_aram.values():
        ceta_expect.update(v)
    ceta_expect = {k: ceta_expect.get(k, 0) for k in ARAMMANA_ORDER}
    if ceta_expect != {"rupa": 50, "satta": 50, "gandha": 50, "rasa": 50, "photthabba": 50, "dhamma": 52}:
        die(f"per-อารมณ์ เจตสิก totals {ceta_expect} != text (L1408-1415)")

    def categories():
        return [{"id": k, "thai": ARAMMANA_THAI[k]} for k in ARAMMANA_ORDER]

    arammana = {
        "id": "arammana",
        "thai": "อารัมมณสังคหะ",
        "source": "reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L901-L1417",
        "gatha": GATHA,
        "notes": NOTES,
        "citta": {
            "axis": "อารมณ์ ๖ ที่รับได้",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CITTA_GROUPINGS,
            "expect": {k: EXPECT_CITTA[k] for k in ARAMMANA_ORDER},
            "assignments": [{"ref": cid, "cats": citta_aram[cid]} for cid in citta_ids],
        },
        "cetasika": {
            "axis": "อารมณ์ ๖ ที่รับได้",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CETA_GROUPINGS,
            "expect": ceta_expect,
            "assignments": [{"ref": cid, "cats": ordered(ceta_aram[cid])} for cid in ceta_ids],
        },
    }

    header = (
        "# ปริจเฉทที่ ๓ ปกิณณกสังคหะ -- scheme fragment: อารัมมณสังคหะ.\n"
        "#\n"
        "# GENERATED by scripts/derive_p3_arammana.py (verified against\n"
        "# reference/01-...md L901-L1417: the per-นัย breakdown, the ๗ นัย\n"
        "# เอกันตะ/อเนกันตะ คาถา (๒๕/๖/๒๑/๘/๒๐/๕/๖), and the per-อารมณ์ headline\n"
        "# totals must all reproduce; no julatri cross-check -- julatri has no\n"
        "# อารมณ์ lens).  Re-run that script to regenerate; do not hand-edit.\n"
        "#\n"
        f"#   จิต by อารมณ์ set-size: {dict(sorted(size_c.items()))}  (เอก/ปัญจ/ฉ = 75/3/43)\n"
        f"#   จิต per-อารมณ์: {got}  (รูป..โผฏฐัพพ ๔๘, ธัมม ๑๐๘ พิสดาร / ๗๖ ในระบบ ๘๙)\n"
        f"#   เจตสิก by อารมณ์ set-size: {dict(sorted(size_e.items()))}  (1/6 = 2/50)\n"
        f"#   เจตสิก per-อารมณ์: {ceta_expect}\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(arammana, f, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)

    print(f"Wrote {OUT}")
    print(f"  จิต ๑๒๑ by อารมณ์ ๖ set-size: {dict(sorted(size_c.items()))}  (เอก/ปัญจ/ฉ = 75/3/43)")
    print(f"  จิต per-อารมณ์: {got}  (รูป..โผฏฐัพพ ๔๘, ธัมมารมณ์ ๑๐๘ พิสดาร; ๗๖ ในระบบ ๘๙)")
    print(f"  เจตสิก ๕๒ by อารมณ์ ๖ set-size: {dict(sorted(size_e.items()))}  (เอก/ฉ = 2/50)")
    print(f"  เจตสิก per-อารมณ์: {ceta_expect}")
    print(f"  คาถา ๗ นัย เอกันตะ/อเนกันตะ: {[EXPECT_NAYA[k] for k in range(1, 8)]}  (รวม ๙๑)")


if __name__ == "__main__":
    main()
