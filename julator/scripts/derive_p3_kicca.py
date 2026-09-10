#!/usr/bin/env python3
"""
Generate data/p3/kicca.yaml -- the กิจจสังคหะ scheme fragment for /julator/p3.

Sources / cross-checks (three independent derivations must agree):
  * reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L369-L726 -- the authoritative text.
      - จิต by กิจ: built here from "การจำแนกกิจ ๑๔ โดยจิต" (L420-448, per-กิจ lists).
      - the transpose "การจำแนกจิต โดยกิจ ๑๔" (L449-477) + the กิจ/ฐาน คาถา
        (L502-513) give the set-size buckets this script asserts:
          ทำ ๑ กิจ ๑๐๐, ๒ กิจ ๒, ๓ กิจ ๙, ๔ กิจ ๘, ๕ กิจ ๒  (นับพิสดาร).
      - เจตสิก by กิจ: authored here from "การจำแนกเจตสิก ๕๒ โดยกิจ ๑๔"
        (L540-600).  Size buckets: ๑ กิจ = ๑๗, ๔ = ๒, ๕ = ๒๑, ๖ = ๑, ๗ = ๑,
        ๙ = ๓, ๑๔ = ๗.
        NOTE: the text's heading for วิตก/วิจาร/อธิโมกข์ reads "ทำหน้าที่ ๘" but
        the list it then gives enumerates NINE กิจ (อาวัชชน สัมปฏิจฉน สันตีรณ
        โวฏฐัพพน included) and the julatri reconstruction below also yields 9.
        We follow the enumerated list (9).
  * ../../julatri/abhidhamma-julatri/data/data.json
      - each เจตสิก's authored กิจ-set is independently reconstructed: union the
        กิจ-set of every citta the เจตสิก occurs in (julatri cetasikaToCittas x
        the per-citta กิจ built from the *other* text section above).  The two
        must match for all 52 -- this ties L420-448, L540-600 and julatri
        together.

ฐาน ๑๐ is *not* a separate axis: it is กิจ ๑๔ with the five ปัญจวิญญาณกิจ
(ทัสสน สวน ฆายน สายน ผุสน) merged into one ปัญจวิญญาณฐาน; every count is
unchanged (๑/๒/๓/๔/๕ กิจ = ๑/๒/๓/๔/๕ ฐาน).  Recorded in the scheme note.

Run: python3 scripts/derive_p3_kicca.py   (then: python3 scripts/build_data.py)
"""
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
JULATRI_JSON = ROOT.parent.parent / "julatri" / "abhidhamma-julatri" / "data" / "data.json"
PARAMATTHA = ROOT / "data" / "paramattha.yaml"
OUT = ROOT / "data" / "p3" / "kicca.yaml"

# กิจ ๑๔ in textbook order (L390-403)
KICCA_ORDER = [
    "patisandhi", "bhavanga", "avajjana", "dassana", "savana", "ghayana",
    "sayana", "phusana", "sampaticchana", "santirana", "votthapana", "javana",
    "tadarammana", "cuti",
]
KICCA_THAI = {
    "patisandhi": "ปฏิสนธิกิจ", "bhavanga": "ภวังคกิจ", "avajjana": "อาวัชชนกิจ",
    "dassana": "ทัสสนกิจ", "savana": "สวนกิจ", "ghayana": "ฆายนกิจ",
    "sayana": "สายนกิจ", "phusana": "ผุสนกิจ", "sampaticchana": "สัมปฏิจฉนกิจ",
    "santirana": "สันตีรณกิจ", "votthapana": "โวฏฐัพพนกิจ", "javana": "ชวนกิจ",
    "tadarammana": "ตทารัมมณกิจ", "cuti": "จุติกิจ",
}


def die(msg):
    sys.exit(f"derive_p3_kicca: {msg}")


def ordered(xs):
    return sorted(set(xs), key=KICCA_ORDER.index)


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
SAMPATICCHANA = ["ahetuka-akusalavipaka-sampaticchana", "ahetuka-kusalavipaka-sampaticchana"]
UPEKKHA_SANT = ["ahetuka-akusalavipaka-upekkhasantirana", "ahetuka-kusalavipaka-upekkhasantirana"]
SOMANASSA_SANT = ["ahetuka-kusalavipaka-somanassasantirana"]
SANTIRANA3 = UPEKKHA_SANT + SOMANASSA_SANT
PANCADVARAVAJJANA = ["ahetuka-pancadvaravajjana"]
MANODVARAVAJJANA = ["ahetuka-manodvaravajjana"]
HASITUPPADA = ["ahetuka-hasituppada"]

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
JAVANA_ALL = (
    KAMA_JAVANA + RUPA_KUSALA + RUPA_KIRIYA + ARUPA_KUSALA + ARUPA_KIRIYA + LOKUTTARA
)  # 87

# per-กิจ citta lists, straight from "การจำแนกกิจ ๑๔ โดยจิต" (L420-448)
KICCA_SOURCES = [
    (["patisandhi", "bhavanga", "cuti"], UPEKKHA_SANT + MAHAVIPAKA + MAHAGGATA_VIPAKA),  # 19
    (["avajjana"], PANCADVARAVAJJANA + MANODVARAVAJJANA),  # 2
    (["dassana"], DVIPANCA["cakkhu"]),  # 2
    (["savana"], DVIPANCA["sota"]),  # 2
    (["ghayana"], DVIPANCA["ghana"]),  # 2
    (["sayana"], DVIPANCA["jivha"]),  # 2
    (["phusana"], DVIPANCA["kaya"]),  # 2
    (["sampaticchana"], SAMPATICCHANA),  # 2
    (["santirana"], SANTIRANA3),  # 3
    (["votthapana"], MANODVARAVAJJANA),  # 1
    (["javana"], JAVANA_ALL),  # 87 (พิสดาร)
    (["tadarammana"], SANTIRANA3 + MAHAVIPAKA),  # 11
]
EXPECT_KICCA = {
    "patisandhi": 19, "bhavanga": 19, "avajjana": 2, "dassana": 2, "savana": 2,
    "ghayana": 2, "sayana": 2, "phusana": 2, "sampaticchana": 2, "santirana": 3,
    "votthapana": 1, "javana": 87, "tadarammana": 11, "cuti": 19,
}
CITTA_GROUPINGS = [
    {"id": "k1", "thai": "จิตทำกิจเดียว", "size": 1, "expect": 100},
    {"id": "k2", "thai": "จิตทำ ๒ กิจ", "size": 2, "expect": 2},
    {"id": "k3", "thai": "จิตทำ ๓ กิจ", "size": 3, "expect": 9},
    {"id": "k4", "thai": "จิตทำ ๔ กิจ", "size": 4, "expect": 8},
    {"id": "k5", "thai": "จิตทำ ๕ กิจ", "size": 5, "expect": 2},
]
CETA_GROUPINGS = [
    {"id": "c1", "thai": "เจตสิกทำกิจเดียว (ชวนกิจ)", "size": 1, "expect": 17},
    {"id": "c4", "thai": "เจตสิกทำ ๔ กิจ", "size": 4, "expect": 2},
    {"id": "c5", "thai": "เจตสิกทำ ๕ กิจ", "size": 5, "expect": 21},
    {"id": "c6", "thai": "เจตสิกทำ ๖ กิจ", "size": 6, "expect": 1},
    {"id": "c7", "thai": "เจตสิกทำ ๗ กิจ", "size": 7, "expect": 1},
    {"id": "c9", "thai": "เจตสิกทำ ๙ กิจ", "size": 9, "expect": 3},
    {"id": "c14", "thai": "เจตสิกทำกิจทั้ง ๑๔", "size": 14, "expect": 7},
]

GATHA = (
    "ปฏิสนฺธาทโย นาม กิจฺจเภเทน จุทฺทส / ทสธา ฐานเภเทน จิตฺตุปฺปาทา ปกาสิตา\n"
    "อฏฺฐสฏฺฐิ ตถา เทฺว จ นวาฏฺฐ เทฺว ยถากฺกมํ / เอก ทฺวิ ติ จตุ ปญฺจ กิจฺจฏฺฐานานิ นิทฺทิเส"
)
NOTES = [
    "จิตและเจตสิกทุกดวงย่อมทำกิจเสมอ ไม่มีดวงใดเกิดขึ้นโดยไม่มีกิจ",
    {"t": "<strong>จิต</strong> — จำแนกโดยกิจ ๑๔ ที่ทำได้ (๑–๕ กิจต่อดวง)",
     "sub": [
         "ทำ ๑ กิจ ๑๐๐ · ๒ กิจ ๒ · ๓ กิจ ๙ · ๔ กิจ ๘ · ๕ กิจ ๒ (นับพิสดาร; ๖๘ สำหรับจิตทำกิจเดียวในนัย ๘๙)",
     ]},
    {"t": "<strong>ฐาน ๑๐</strong> — ยุบทัสสน สวน ฆายน สายน ผุสน (ปัญจวิญญาณกิจ ๕) เข้าเป็นปัญจวิญญาณฐานเดียว",
     "sub": [
         "จำนวนนับไม่เปลี่ยน (๑/๒/๓/๔/๕ กิจ = ๑/๒/๓/๔/๕ ฐาน)",
     ]},
    {"t": "<strong>เจตสิก</strong> — จำแนกโดยกิจ ๑๔ ที่ทำได้",
     "sub": [
         "อกุศล ๑๔ + วิรตี ๓ ทำเฉพาะชวนกิจ",
         "สัพพจิตตสาธารณ ๗ ทำได้ครบทั้ง ๑๔ กิจ",
     ]},
    "ตำราพาดหัวว่า วิตก วิจาร อธิโมกข์ ทำ ๘ กิจ แต่แจกแจงไว้ ๙ กิจ — เว็บนี้ยึดตามรายการ ๙ กิจ ซึ่งตรงกับการทานกับข้อมูลจิต–เจตสิกของจูฬตรี",
]


def main():
    if not JULATRI_JSON.exists():
        die(f"julatri data.json not found: {JULATRI_JSON}")
    jd = json.load(open(JULATRI_JSON, encoding="utf-8"))
    para = yaml.safe_load(open(PARAMATTHA, encoding="utf-8"))

    citta_ids = [c["id"] for c in para["citta"]]
    citta_id_set = set(citta_ids)
    cetasikas = para["cetasika"]
    ceta_ids = [c["id"] for c in cetasikas]
    by_group = {}
    for c in cetasikas:
        by_group.setdefault(c["group"], []).append(c["id"])

    jcittas = {c["id"]: c for c in jd["cittas"]}
    if set(jcittas) != citta_id_set:
        die("julatri citta id set != paramattha.yaml citta id set")

    # sanity: every source list resolves to real citta ids, lengths as expected
    for name, lst, n in [
        ("AKUSALA", AKUSALA, 12), ("MAHAKUSALA", MAHAKUSALA, 8),
        ("MAHAVIPAKA", MAHAVIPAKA, 8), ("MAHAKIRIYA", MAHAKIRIYA, 8),
        ("MAHAGGATA_VIPAKA", MAHAGGATA_VIPAKA, 9), ("LOKUTTARA", LOKUTTARA, 40),
        ("KAMA_JAVANA", KAMA_JAVANA, 29), ("JAVANA_ALL", JAVANA_ALL, 87),
    ]:
        if len(lst) != n:
            die(f"{name}: expected {n} ids, got {len(lst)}")
    used = set()
    for _, lst in KICCA_SOURCES:
        used |= set(lst)
    for cid in used:
        if cid not in citta_id_set:
            die(f"kicca source names non-citta id {cid!r}")

    # ---- จิต by กิจ (accumulate the per-กิจ lists) ----
    citta_kicca = {cid: [] for cid in citta_ids}
    for kiccas, cids in KICCA_SOURCES:
        for cid in cids:
            for k in kiccas:
                if k not in citta_kicca[cid]:
                    citta_kicca[cid].append(k)
    citta_kicca = {cid: ordered(v) for cid, v in citta_kicca.items()}

    empty = [cid for cid, v in citta_kicca.items() if not v]
    if empty:
        die(f"จิต with no กิจ (text says none exist): {empty}")

    got = Counter()
    for v in citta_kicca.values():
        got.update(v)
    got = {k: got.get(k, 0) for k in KICCA_ORDER}
    if got != EXPECT_KICCA:
        die(f"per-กิจ จิต totals {got} != text {EXPECT_KICCA}")

    size_c = Counter(len(v) for v in citta_kicca.values())
    for g in CITTA_GROUPINGS:
        if size_c.get(g["size"], 0) != g["expect"]:
            die(f"จิต set-size {g['size']} = {size_c.get(g['size'], 0)} != คาถา {g['expect']}")
    if sum(size_c.values()) != 121 or set(size_c) - {1, 2, 3, 4, 5}:
        die(f"จิต set-size distribution unexpected: {dict(size_c)}")

    # ---- เจตสิก by กิจ (authored from L540-600) ----
    akusala_ceta = (
        by_group["moha-catuka"] + by_group["lobha-tika"] + by_group["dosa-catuka"]
        + by_group["thina-duka"] + by_group["vicikiccha"]
    )
    if len(akusala_ceta) != 14:
        die(f"อกุศลเจตสิก != 14: {akusala_ceta}")

    FIVE = ["patisandhi", "bhavanga", "cuti", "javana", "tadarammana"]
    NINE = ["patisandhi", "bhavanga", "cuti", "avajjana", "sampaticchana",
            "santirana", "votthapana", "javana", "tadarammana"]
    authored = {}
    for cid in akusala_ceta + by_group["virati"]:
        authored[cid] = ["javana"]
    for cid in by_group["appamanna"]:
        authored[cid] = ["patisandhi", "bhavanga", "cuti", "javana"]
    for cid in by_group["sobhana-sadharana"] + ["panna", "chanda"]:
        authored[cid] = list(FIVE)
    authored["piti"] = ["patisandhi", "bhavanga", "cuti", "santirana", "javana", "tadarammana"]
    authored["viriya"] = ["patisandhi", "bhavanga", "cuti", "avajjana", "votthapana",
                          "javana", "tadarammana"]
    for cid in ("vitakka", "vicara", "adhimokkha"):
        authored[cid] = list(NINE)
    for cid in by_group["sabbacitta-sadharana"]:
        authored[cid] = list(KICCA_ORDER)

    missing = set(ceta_ids) - set(authored)
    if missing:
        die(f"no กิจ-set authored for เจตสิก: {sorted(missing)}")

    size_e = Counter(len(v) for v in authored.values())
    for g in CETA_GROUPINGS:
        if size_e.get(g["size"], 0) != g["expect"]:
            die(f"เจตสิก set-size {g['size']} = {size_e.get(g['size'], 0)} != text {g['expect']}")

    # ---- independent reconstruction from julatri co-occurrence ----
    c2c = jd["cetasikaToCittas"]
    for cid in ceta_ids:
        recon = set()
        for x in c2c.get(cid, []):
            recon |= set(citta_kicca[x])
        if ordered(recon) != ordered(authored[cid]):
            die(f"เจตสิก {cid}: authored {ordered(authored[cid])} "
                f"!= julatri reconstruction {ordered(recon)}")

    ceta_expect = Counter()
    for v in authored.values():
        ceta_expect.update(v)
    ceta_expect = {k: ceta_expect.get(k, 0) for k in KICCA_ORDER}

    def categories():
        return [{"id": k, "thai": KICCA_THAI[k]} for k in KICCA_ORDER]

    kicca = {
        "id": "kicca",
        "thai": "กิจจสังคหะ",
        "source": "reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L369-L726",
        "gatha": GATHA,
        "notes": NOTES,
        "citta": {
            "axis": "กิจ ๑๔ ที่ทำได้",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CITTA_GROUPINGS,
            "expect": {k: EXPECT_KICCA[k] for k in KICCA_ORDER},
            "assignments": [{"ref": cid, "cats": citta_kicca[cid]} for cid in citta_ids],
        },
        "cetasika": {
            "axis": "กิจ ๑๔ ที่ทำได้",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CETA_GROUPINGS,
            "expect": ceta_expect,
            "assignments": [{"ref": cid, "cats": ordered(authored[cid])} for cid in ceta_ids],
        },
    }

    header = (
        "# ปริจเฉทที่ ๓ ปกิณณกสังคหะ -- scheme fragment: กิจจสังคหะ.\n"
        "#\n"
        "# GENERATED by scripts/derive_p3_kicca.py (verified against\n"
        "# reference/01-...md L369-L726 -- per-กิจ lists, transpose คาถา, and the\n"
        "# เจตสิก section -- and cross-checked against julatri co-occurrence).\n"
        "# Re-run that script to regenerate; do not hand-edit.\n"
        "#\n"
        f"#   จิต by กิจ set-size: {dict(sorted(size_c.items()))}  (100/2/9/8/2)\n"
        f"#   จิต per-กิจ: {got}\n"
        f"#   เจตสิก by กิจ set-size: {dict(sorted(size_e.items()))}  (17/2/21/1/1/3/7)\n"
        f"#   เจตสิก per-กิจ: {ceta_expect}\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(kicca, f, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)

    print(f"Wrote {OUT}")
    print(f"  จิต ๑๒๑ by กิจ set-size: {dict(sorted(size_c.items()))}  (ทำ 1/2/3/4/5 กิจ = 100/2/9/8/2)")
    print(f"  จิต per-กิจ: {got}")
    print(f"  เจตสิก ๕๒ by กิจ set-size: {dict(sorted(size_e.items()))}  (1/4/5/6/7/9/14 = 17/2/21/1/1/3/7)")
    print(f"  เจตสิก per-กิจ: {ceta_expect}")


if __name__ == "__main__":
    main()
