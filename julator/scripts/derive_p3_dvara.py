#!/usr/bin/env python3
"""
Generate data/p3/dvara.yaml -- the ทวารสังคหะ scheme fragment for /julator/p3.

Source: reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L730-L897 (the authoritative text).
There is no julatri cross-check here: a เจตสิก's ทวาร depends on the *object* it
takes, not only on its host จิต's door-set (อัปปมัญญา is the flagged case -- it
rides มหากุศล/มหากิริยา, which arise in all 6 doors, yet occurs only in มโนทวาร
because it takes a สัตวบัญญัติ).  Verification is internal instead:

  * จิต by ทวาร ๖ (each จิต arises in a SET of 0-6 doors) is built from the
    5-way คาถา split (L812-851):
        เอกทวาริก ๓๖/๖๘ · ปัญจทวาริก ๓ · ฉทวาริกแน่นอน ๓๑ ·
        ฉทวาริก-หรือ-ทวารวิมุตต ๑๐ · ทวารวิมุตตแน่นอน ๙          -> 121
    Asserted: set-size buckets 0/1/5/6 = 9/68/3/41 (พิสดาร), AND the per-ทวาร
    totals reproduce the textbook's headline "การจำแนกจิต โดยทวาร ๖" (L751-770):
        จักขุ..กายทวาริกจิต ๔๖ each, มโนทวาริกจิต ๙๙, ทวารวิมุตตจิต ๑๙.
  * เจตสิก by ทวาร ๖ (L853-895): อัปปมัญญา ๒ = {มโนทวาร} only; the other ๕๐
    arise in all ๖ ทวาร.  Buckets: ๑ ทวาร = ๒, ๖ ทวาร = ๕๐.

ทวารวิมุตต (เกิดพ้นทวาร) is modelled as the EMPTY door-set (set-size 0), the
same way อเหตุก is size-0 in เหตุสังคหะ.  The 10 จิต that are "ฉทวาริก หรือ
ทวารวิมุตต" (อุเบกขาสันตีรณ ๒ มหาวิปาก ๘) carry the full 6-door set; their
door-freed role in ปฏิสนธิ/ภวังค/จุติ is described in the scheme note.
เอกันตะ (แน่นอน) / อเนกันตะ (ไม่แน่นอน) per door is not modelled in this pass.

Run: python3 scripts/derive_p3_dvara.py   (then: python3 scripts/build_data.py)
"""
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PARAMATTHA = ROOT / "data" / "paramattha.yaml"
OUT = ROOT / "data" / "p3" / "dvara.yaml"

DVARA_ORDER = ["cakkhu", "sota", "ghana", "jivha", "kaya", "mano"]
DVARA_THAI = {
    "cakkhu": "จักขุทวาร", "sota": "โสตทวาร", "ghana": "ฆานทวาร",
    "jivha": "ชิวหาทวาร", "kaya": "กายทวาร", "mano": "มโนทวาร",
}
PANCA = ["cakkhu", "sota", "ghana", "jivha", "kaya"]


def die(msg):
    sys.exit(f"derive_p3_dvara: {msg}")


def ordered(xs):
    return sorted(set(xs), key=DVARA_ORDER.index)


# ---- citta id groups ----
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
SAMPATICCHANA = ["ahetuka-akusalavipaka-sampaticchana", "ahetuka-kusalavipaka-sampaticchana"]
PANCADVARAVAJJANA = ["ahetuka-pancadvaravajjana"]
MANODHATU = PANCADVARAVAJJANA + SAMPATICCHANA  # 3
MANODVARAVAJJANA = ["ahetuka-manodvaravajjana"]
HASITUPPADA = ["ahetuka-hasituppada"]
UPEKKHA_SANT = ["ahetuka-akusalavipaka-upekkhasantirana", "ahetuka-kusalavipaka-upekkhasantirana"]
SOMANASSA_SANT = ["ahetuka-kusalavipaka-somanassasantirana"]

MAHAKUSALA = [f"mahakusala-{i}" for i in range(1, 9)]
MAHAVIPAKA = [f"mahavipaka-{i}" for i in range(1, 9)]
MAHAKIRIYA = [f"mahakiriya-{i}" for i in range(1, 9)]

JHANA5 = ["ปฐมฌาน", "ทุติยฌาน", "ตติยฌาน", "จตุตถฌาน", "ปัญจมฌาน"]
RUPA_KUSALA = [f"rupa-{j}-kusala" for j in JHANA5]
RUPA_VIPAKA = [f"rupa-{j}-vipaka" for j in JHANA5]
RUPA_KIRIYA = [f"rupa-{j}-kiriya" for j in JHANA5]
ARUPA = ["akasanancayatana", "vinnanancayatana", "akincannayatana", "nevasannanasannayatana"]
ARUPA_KUSALA = [f"arupa-{n}-kusala" for n in ARUPA]
ARUPA_VIPAKA = [f"arupa-{n}-vipaka" for n in ARUPA]
ARUPA_KIRIYA = [f"arupa-{n}-kiriya" for n in ARUPA]
MAHAGGATA_VIPAKA = RUPA_VIPAKA + ARUPA_VIPAKA  # 9

PHASES = ["sotapatti", "sakadagami", "anagami", "arahatta"]
LOKUTTARA = [f"{p}-{mp}-{j}" for p in PHASES for mp in ("magga", "phala") for j in JHANA5]  # 40

KAMA_JAVANA = AKUSALA + HASITUPPADA + MAHAKUSALA + MAHAKIRIYA  # 29
APPANA_JAVANA = RUPA_KUSALA + RUPA_KIRIYA + ARUPA_KUSALA + ARUPA_KIRIYA + LOKUTTARA  # 58

# per-citta door-set, from the 5-way คาถา split (L812-851)
DVARA_SOURCES = [
    (["cakkhu"], DVIPANCA["cakkhu"]),
    (["sota"], DVIPANCA["sota"]),
    (["ghana"], DVIPANCA["ghana"]),
    (["jivha"], DVIPANCA["jivha"]),
    (["kaya"], DVIPANCA["kaya"]),
    (PANCA, MANODHATU),  # ปัญจทวาริก ๓
    (DVARA_ORDER,  # ฉทวาริก: แน่นอน ๓๑ + (ฉทวาริก-หรือ-วิมุตต) ๑๐
     SOMANASSA_SANT + MANODVARAVAJJANA + KAMA_JAVANA + UPEKKHA_SANT + MAHAVIPAKA),
    (["mano"], APPANA_JAVANA),  # เอกทวาริก (มโนทวาร) -- อัปปนาชวนะ ๕๘
    # มหัคคตวิปาก ๙ -> {} (ทวารวิมุตตแน่นอน): no entry, stays empty
]
EXPECT_CITTA = {"cakkhu": 46, "sota": 46, "ghana": 46, "jivha": 46, "kaya": 46, "mano": 99}
CITTA_GROUPINGS = [
    {"id": "vimutta", "thai": "ทวารวิมุตตจิต (ไม่เกิดทางทวาร)", "size": 0, "expect": 9},
    {"id": "eka", "thai": "เอกทวาริกจิต (เกิดทางทวารเดียว)", "size": 1, "expect": 68},
    {"id": "panca", "thai": "ปัญจทวาริกจิต (เกิดทางปัญจทวาร)", "size": 5, "expect": 3},
    {"id": "cha", "thai": "ฉทวาริกจิต (เกิดได้ทั้ง ๖ ทวาร)", "size": 6, "expect": 41},
]
CETA_GROUPINGS = [
    {"id": "eka", "thai": "เอกทวาริกเจตสิก (เฉพาะมโนทวาร)", "size": 1, "expect": 2},
    {"id": "cha", "thai": "ฉทวาริกเจตสิก (เกิดได้ทั้ง ๖ ทวาร)", "size": 6, "expect": 50},
]

GATHA = (
    "เอกทฺวาริกจิตฺตานิ ปญฺจทฺวาริกานิ จ / ฉทฺวาริกวิมุตฺตานิ วิมุตฺตานิ จ สพฺพถา\n"
    "ฉตฺตึส ตถา ตีณิ เอกตฺตึส ยถากฺกมํ / ทสธา นวธา เจติ ปญฺจธา ปริทีปเย"
)
NOTES = [
    {"t": "<strong>ทวาร ๖</strong> — ประตูที่วิถีจิตอาศัยเกิด",
     "sub": [
         "จักขุ โสต ฆาน ชิวหา กายทวาร — องค์ธรรมคือ ปสาทรูป ๕",
         "มโนทวาร — องค์ธรรมคือ ภวังคจิต ๑๙",
     ]},
    {"t": "<strong>จิต</strong> — จำแนกโดยทวารที่เกิดได้ (๐–๖ ทวาร): ทวารวิมุตต ๙ · เอกทวาริก ๖๘ · ปัญจทวาริก ๓ · ฉทวาริก ๔๑ (นับพิสดาร)",
     "sub": [
         "คาถาแบ่งละเอียดเป็น ๕ พวก: เอกทวาริก ๓๖ (๖๘) · ปัญจทวาริก ๓ · ฉทวาริกแน่นอน ๓๑ · ฉทวาริก-หรือ-ทวารวิมุตต ๑๐ (อุเบกขาสันตีรณ ๒ มหาวิปาก ๘ — เว็บนี้จัดเข้ากลุ่มฉทวาริก ให้ครบ ๖ ทวาร) · ทวารวิมุตตแน่นอน ๙ (มหัคคตวิปาก ๙)",
     ]},
    "<strong>เจตสิก</strong> — อัปปมัญญา ๒ เกิดเฉพาะมโนทวาร (รับสัตวบัญญัติเป็นอารมณ์); เจตสิกที่เหลือ ๕๐ เกิดได้ทั้ง ๖ ทวาร",
    "เว็บนี้ยังไม่ได้แยกเอกันตะ (เกิดแน่นอน) / อเนกันตะ (ไม่แน่นอน) ในแต่ละทวาร",
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

    for name, lst, n in [
        ("MANODHATU", MANODHATU, 3), ("KAMA_JAVANA", KAMA_JAVANA, 29),
        ("APPANA_JAVANA", APPANA_JAVANA, 58), ("MAHAVIPAKA", MAHAVIPAKA, 8),
        ("MAHAGGATA_VIPAKA", MAHAGGATA_VIPAKA, 9), ("LOKUTTARA", LOKUTTARA, 40),
    ]:
        if len(lst) != n:
            die(f"{name}: expected {n} ids, got {len(lst)}")
    used = set()
    for _, lst in DVARA_SOURCES:
        used |= set(lst)
    for cid in used:
        if cid not in citta_id_set:
            die(f"dvara source names non-citta id {cid!r}")

    # ---- จิต by ทวาร ----
    citta_dvara = {cid: [] for cid in citta_ids}
    for doors, cids in DVARA_SOURCES:
        for cid in cids:
            for d in doors:
                if d not in citta_dvara[cid]:
                    citta_dvara[cid].append(d)
    citta_dvara = {cid: ordered(v) for cid, v in citta_dvara.items()}

    got = Counter()
    for v in citta_dvara.values():
        got.update(v)
    got = {k: got.get(k, 0) for k in DVARA_ORDER}
    if got != EXPECT_CITTA:
        die(f"per-ทวาร จิต totals {got} != textbook headline {EXPECT_CITTA}")

    size_c = Counter(len(v) for v in citta_dvara.values())
    for g in CITTA_GROUPINGS:
        if size_c.get(g["size"], 0) != g["expect"]:
            die(f"จิต door-set-size {g['size']} = {size_c.get(g['size'], 0)} != คาถา {g['expect']}")
    if sum(size_c.values()) != 121 or set(size_c) - {0, 1, 5, 6}:
        die(f"จิต door-set-size distribution unexpected: {dict(size_c)}")
    vimutta = sorted(cid for cid, v in citta_dvara.items() if not v)
    if set(vimutta) != set(MAHAGGATA_VIPAKA):
        die(f"ทวารวิมุตตแน่นอน should be มหัคคตวิปาก ๙, got {vimutta}")

    # ---- เจตสิก by ทวาร ----
    authored = {}
    for cid in ceta_ids:
        authored[cid] = list(DVARA_ORDER)
    for cid in by_group["appamanna"]:
        authored[cid] = ["mano"]
    if len(by_group["appamanna"]) != 2:
        die("อัปปมัญญาเจตสิก != 2")

    size_e = Counter(len(v) for v in authored.values())
    for g in CETA_GROUPINGS:
        if size_e.get(g["size"], 0) != g["expect"]:
            die(f"เจตสิก door-set-size {g['size']} = {size_e.get(g['size'], 0)} != text {g['expect']}")

    ceta_expect = Counter()
    for v in authored.values():
        ceta_expect.update(v)
    ceta_expect = {k: ceta_expect.get(k, 0) for k in DVARA_ORDER}

    def categories():
        return [{"id": k, "thai": DVARA_THAI[k]} for k in DVARA_ORDER]

    dvara = {
        "id": "dvara",
        "thai": "ทวารสังคหะ",
        "source": "reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L730-L897",
        "gatha": GATHA,
        "notes": NOTES,
        "citta": {
            "axis": "ทวาร ๖ ที่เกิดได้",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CITTA_GROUPINGS,
            "expect": {k: EXPECT_CITTA[k] for k in DVARA_ORDER},
            "assignments": [{"ref": cid, "cats": citta_dvara[cid]} for cid in citta_ids],
        },
        "cetasika": {
            "axis": "ทวาร ๖ ที่เกิดได้",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CETA_GROUPINGS,
            "expect": ceta_expect,
            "assignments": [{"ref": cid, "cats": ordered(authored[cid])} for cid in ceta_ids],
        },
    }

    header = (
        "# ปริจเฉทที่ ๓ ปกิณณกสังคหะ -- scheme fragment: ทวารสังคหะ.\n"
        "#\n"
        "# GENERATED by scripts/derive_p3_dvara.py (verified against\n"
        "# reference/01-...md L730-L897: the 5-way คาถา split and the per-ทวาร\n"
        "# headline totals must both reproduce; no julatri cross-check -- a\n"
        "# เจตสิก's ทวาร depends on its object, not its host จิต's door-set).\n"
        "# Re-run that script to regenerate; do not hand-edit.\n"
        "#\n"
        f"#   จิต by ทวาร set-size: {dict(sorted(size_c.items()))}  (วิมุตต/เอก/ปัญจ/ฉ = 9/68/3/41)\n"
        f"#   จิต per-ทวาร: {got}  (จักขุ..กาย ๔๖, มโน ๙๙)\n"
        f"#   เจตสิก by ทวาร set-size: {dict(sorted(size_e.items()))}  (1/6 = 2/50)\n"
        f"#   เจตสิก per-ทวาร: {ceta_expect}\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(dvara, f, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)

    print(f"Wrote {OUT}")
    print(f"  จิต ๑๒๑ by ทวาร set-size: {dict(sorted(size_c.items()))}  (ทวารวิมุตต/เอก/ปัญจ/ฉ = 9/68/3/41)")
    print(f"  จิต per-ทวาร: {got}  (จักขุ..กายทวาริก ๔๖, มโนทวาริก ๙๙)")
    print(f"  เจตสิก ๕๒ by ทวาร set-size: {dict(sorted(size_e.items()))}  (เอก/ฉ = 2/50)")


if __name__ == "__main__":
    main()
