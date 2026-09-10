#!/usr/bin/env python3
"""
Generate data/p3/hetu.yaml -- the เหตุสังคหะ scheme fragment for /julator/p3.

Sources / cross-checks (two independent derivations must agree):
  * reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L157-L363 -- the authoritative text.
      - จิต by set-size (คาถา L221-224, พิสดาร):
          อเหตุก ๑๘ / เอกเหตุก ๒ / ทวิเหตุก ๒๒ / ติเหตุก ๗๙
      - per-เหตุ จิต counts fall straight out of the "การนับจำนวนเหตุ โดยพิสดาร
        ๒๘๓" table (L328-363): โลภ ๘, โทส ๒, โมห ๑๒, อโลภ ๙๑, อโทส ๙๑, อโมห ๗๙.
      - เจตสิก by set-size, อคหิตัคคหนนัย (L253-295):
          เหตุ ๑ = ๓, เหตุ ๒ = ๙, เหตุ ๓ = ๒๗, เหตุ ๔ = ๐, เหตุ ๕ = ๑, เหตุ ๖ = ๑๒.
  * ../../julatri/abhidhamma-julatri/data/data.json
      - each citta's เหตุ set is the intersection of its `cetasikas` with the six
        root เจตสิก {โลภ โทส โมห อโลภ อโทส ปัญญา}; this script asserts the
        set-size totals equal the จูฬโท คาถา before anything is written.
      - each เจตสิก's authored เหตุ set (อคหิตัคคหนนัย, from the text's wording)
        is re-derived from julatri's cetasikaToCittas: union the root sets of
        every citta the เจตสิก occurs in, then drop the เจตสิก's own root
        ("เหตุที่ยังไม่ถูกถือเอา"). The two must match for all 52.

Run: python3 scripts/derive_p3_hetu.py   (then: python3 scripts/build_data.py)
"""
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
JULATRI_JSON = ROOT.parent.parent / "julatri" / "abhidhamma-julatri" / "data" / "data.json"
PARAMATTHA = ROOT / "data" / "paramattha.yaml"
OUT = ROOT / "data" / "p3" / "hetu.yaml"

HETU_ORDER = ["lobha", "dosa", "moha", "alobha", "adosa", "amoha"]
HETU_THAI = {
    "lobha": "โลภเหตุ", "dosa": "โทสเหตุ", "moha": "โมหเหตุ",
    "alobha": "อโลภเหตุ", "adosa": "อโทสเหตุ", "amoha": "อโมหเหตุ",
}
# เหตุ category  ->  its องค์ธรรม (a เจตสิก id in paramattha.yaml)
HETU_ONGKHATHAM = {
    "lobha": "lobha", "dosa": "dosa", "moha": "moha",
    "alobha": "alobha", "adosa": "adosa", "amoha": "panna",
}
# the six root เจตสิก ids  ->  the เหตุ category each one *is*
CETA_ROOT = {v: k for k, v in HETU_ONGKHATHAM.items()}


def die(msg):
    sys.exit(f"derive_p3_hetu: {msg}")


def ordered(cats):
    return sorted(set(cats), key=HETU_ORDER.index)


# ---- เจตสิก ๕๒ by co-occurring เหตุ ๖, อคหิตัคคหนนัย (text L253-L295) ----
# keyed by julator cetasika id / group; groups expanded against paramattha.yaml.
CETA_HETU_INDIVIDUAL = {
    # ๒. เอกเหตุกเจตสิก -- เหตุ ๑ (๓)
    "lobha": ["moha"],
    "dosa": ["moha"],
    "vicikiccha": ["moha"],
    # ๓. ทวิเหตุกเจตสิก -- เหตุ ๒ (๙)
    "moha": ["lobha", "dosa"],
    "ditthi": ["lobha", "moha"],
    "mana": ["lobha", "moha"],
    "issa": ["dosa", "moha"],
    "macchariya": ["dosa", "moha"],
    "kukkucca": ["dosa", "moha"],
    "alobha": ["adosa", "amoha"],
    "adosa": ["alobha", "amoha"],
    "panna": ["alobha", "adosa"],
    # ๔. ติเหตุกเจตสิก -- เหตุ ๓ (๒๗): 5 อกุศล here + โสภณ ๒๒ below
    "ahirika": ["lobha", "dosa", "moha"],
    "anottappa": ["lobha", "dosa", "moha"],
    "uddhacca": ["lobha", "dosa", "moha"],
    "thina": ["lobha", "dosa", "moha"],
    "middha": ["lobha", "dosa", "moha"],
    # ๖. ปัญจเหตุกเจตสิก -- เหตุ ๕ (๑)
    "piti": ["lobha", "moha", "alobha", "adosa", "amoha"],
}
# โสภณเจตสิก ๒๒ (เว้น อโลภะ อโทสะ ปัญญา) -> เหตุ ๓ {อโลภ อโทส อโมห}
SOBHANA_22_GROUPS = ["sobhana-sadharana", "virati", "appamanna"]
SOBHANA_22_EXCLUDE = {"alobha", "adosa"}  # panna is its own group (pannindriya)
SOBHANA_22_SET = ["alobha", "adosa", "amoha"]
# ๗. ฉเหตุกเจตสิก -- เหตุ ๖ (๑๒): อัญญสมาน ๑๒ (เว้น ปีติ)
ANNASAMANA_GROUPS = ["sabbacitta-sadharana", "pakinnaka"]
ANNASAMANA_ALL_SIX = list(HETU_ORDER)

CITTA_GROUPINGS = [
    {"id": "ahetuka", "thai": "อเหตุกจิต (ไม่ประกอบด้วยเหตุ)", "size": 0, "expect": 18},
    {"id": "eka", "thai": "เอกเหตุกจิต (เหตุ ๑)", "size": 1, "expect": 2},
    {"id": "dvi", "thai": "ทวิเหตุกจิต (เหตุ ๒)", "size": 2, "expect": 22},
    {"id": "ti", "thai": "ติเหตุกจิต (เหตุ ๓)", "size": 3, "expect": 79},
]
CETA_GROUPINGS = [
    {"id": "zero", "thai": "อเหตุกเจตสิก (ไม่มีเหตุ)", "size": 0, "expect": 0},
    {"id": "one", "thai": "เจตสิกมีเหตุ ๑", "size": 1, "expect": 3},
    {"id": "two", "thai": "เจตสิกมีเหตุ ๒", "size": 2, "expect": 9},
    {"id": "three", "thai": "เจตสิกมีเหตุ ๓", "size": 3, "expect": 27},
    {"id": "four", "thai": "เจตสิกมีเหตุ ๔", "size": 4, "expect": 0},
    {"id": "five", "thai": "เจตสิกมีเหตุ ๕", "size": 5, "expect": 1},
    {"id": "six", "thai": "เจตสิกมีเหตุ ๖", "size": 6, "expect": 12},
]

GATHA = (
    "โลโภ โทโส จ โมโห จ เหตู อกุสลา ตโย / อโลภาโทสาโมหา จ กุสลาพฺยากตา ตถา\n"
    "อเหตุกากฺขรตฺเสก- เหตุกา เทฺว ทฺวาวีสติ / ทฺวิเหตุกา มตา สตฺต- จตฺตาลีส ติเหตุกา"
)
NOTES = [
    {"t": "<strong>จิต</strong> — จำแนกโดยเหตุ ๖ ที่ประกอบร่วม (๐–๓ เหตุต่อดวง)",
     "sub": [
         "คาถาสรุป: อเหตุก ๑๘ · เอกเหตุก ๒ · ทวิเหตุก ๒๒ · ติเหตุก ๗๙ (นับพิสดาร)",
     ]},
    {"t": "<strong>เจตสิก</strong> — จำแนกโดยเหตุ ๖ ที่เกิดร่วม ตามอคหิตัคคหนนัย",
     "sub": [
         "นับเฉพาะเหตุอื่นที่ยังไม่ถูกถือเอา ไม่นับตนเอง",
     ]},
    "<strong>องค์ธรรมของเหตุ ๖</strong> — โลภ โทส โมห อโลภ อโทส และปัญญาเจตสิก",
]


def main():
    if not JULATRI_JSON.exists():
        die(f"julatri data.json not found: {JULATRI_JSON}")
    jd = json.load(open(JULATRI_JSON, encoding="utf-8"))
    para = yaml.safe_load(open(PARAMATTHA, encoding="utf-8"))

    citta_ids = [c["id"] for c in para["citta"]]
    cetasikas = para["cetasika"]
    ceta_ids = [c["id"] for c in cetasikas]
    ceta_by_group = {}
    for c in cetasikas:
        ceta_by_group.setdefault(c["group"], []).append(c["id"])

    jcittas = {c["id"]: c for c in jd["cittas"]}
    if set(jcittas) != set(citta_ids):
        die("julatri citta id set != paramattha.yaml citta id set")

    # ---- จิต by เหตุ, from julatri per-citta cetasikas ----
    citta_hetu = {}
    for cid in citta_ids:
        roots = ordered(CETA_ROOT[x] for x in jcittas[cid]["cetasikas"] if x in CETA_ROOT)
        citta_hetu[cid] = roots
    size_c = Counter(len(v) for v in citta_hetu.values())
    for g in CITTA_GROUPINGS:
        if size_c.get(g["size"], 0) != g["expect"]:
            die(f"จิต set-size {g['size']} count {size_c.get(g['size'], 0)} != คาถา {g['expect']}")
    if any(k > 3 for k in size_c):
        die(f"จิต with >3 เหตุ: {size_c}")

    citta_expect = Counter()
    for roots in citta_hetu.values():
        citta_expect.update(roots)
    citta_expect = {k: citta_expect.get(k, 0) for k in HETU_ORDER}
    # cross-check against the text's "โดยพิสดาร ๒๘๓" table (L328-L363)
    expect_283 = {"lobha": 8, "dosa": 2, "moha": 12, "alobha": 91, "adosa": 91, "amoha": 79}
    if citta_expect != expect_283:
        die(f"จิต per-เหตุ totals {citta_expect} != text ๒๘๓ table {expect_283}")
    if sum(citta_expect.values()) != 283:
        die(f"จิต เหตุ พิสดาร sum {sum(citta_expect.values())} != 283")

    # ---- เจตสิก by เหตุ, อคหิตัคคหนนัย: authored from the text's wording ----
    authored = dict(CETA_HETU_INDIVIDUAL)
    for grp in SOBHANA_22_GROUPS:
        for cid in ceta_by_group.get(grp, []):
            if cid in SOBHANA_22_EXCLUDE:
                continue
            authored[cid] = list(SOBHANA_22_SET)
    for grp in ANNASAMANA_GROUPS:
        for cid in ceta_by_group.get(grp, []):
            if cid == "piti":
                continue
            authored[cid] = list(ANNASAMANA_ALL_SIX)

    missing = set(ceta_ids) - set(authored)
    if missing:
        die(f"no เหตุ-set authored for เจตสิก: {sorted(missing)}")
    extra = set(authored) - set(ceta_ids)
    if extra:
        die(f"authored เหตุ-set for unknown เจตสิก id: {sorted(extra)}")

    size_e = Counter(len(v) for v in authored.values())
    for g in CETA_GROUPINGS:
        if size_e.get(g["size"], 0) != g["expect"]:
            die(f"เจตสิก set-size {g['size']} count {size_e.get(g['size'], 0)} != text {g['expect']}")

    # ---- independent reconstruction from julatri co-occurrence ----
    c2c = jd["cetasikaToCittas"]
    for cid in ceta_ids:
        roots = set()
        for x in c2c.get(cid, []):
            roots |= set(citta_hetu[x])
        roots.discard(CETA_ROOT.get(cid))  # a root เจตสิก does not count itself
        recon = ordered(roots)
        if recon != ordered(authored[cid]):
            die(f"เจตสิก {cid}: authored {ordered(authored[cid])} != julatri reconstruction {recon}")

    ceta_expect = Counter()
    for s in authored.values():
        ceta_expect.update(s)
    ceta_expect = {k: ceta_expect.get(k, 0) for k in HETU_ORDER}

    def categories():
        return [{"id": k, "thai": HETU_THAI[k]} for k in HETU_ORDER]

    hetu = {
        "id": "hetu",
        "thai": "เหตุสังคหะ",
        "source": "reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L157-L363",
        "gatha": GATHA,
        "notes": NOTES,
        "ongkhatham": {k: HETU_ONGKHATHAM[k] for k in HETU_ORDER},
        "citta": {
            "axis": "เหตุ ๖ ที่ประกอบ",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CITTA_GROUPINGS,
            "expect": citta_expect,
            "assignments": [{"ref": cid, "cats": citta_hetu[cid]} for cid in citta_ids],
        },
        "cetasika": {
            "axis": "เหตุ ๖ ที่เกิดร่วม (อคหิตัคคหนนัย)",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CETA_GROUPINGS,
            "expect": ceta_expect,
            "assignments": [{"ref": cid, "cats": ordered(authored[cid])} for cid in ceta_ids],
        },
    }

    header = (
        "# ปริจเฉทที่ ๓ ปกิณณกสังคหะ -- scheme fragment: เหตุสังคหะ.\n"
        "#\n"
        "# GENERATED by scripts/derive_p3_hetu.py (verified against\n"
        "# reference/01-...md L157-L363 and cross-checked with julatri).\n"
        "# Re-run that script to regenerate; do not hand-edit.\n"
        "#\n"
        f"#   จิต by เหตุ set-size: {dict(sorted(size_c.items()))}\n"
        f"#   จิต per-เหตุ (= text ๒๘๓ table): {citta_expect}\n"
        f"#   เจตสิก by เหตุ set-size: {dict(sorted(size_e.items()))}\n"
        f"#   เจตสิก per-เหตุ: {ceta_expect}\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(hetu, f, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)

    print(f"Wrote {OUT}")
    print(f"  จิต ๑๒๑ by เหตุ set-size: {dict(sorted(size_c.items()))}  (อเหตุก/เอก/ทวิ/ติ = 18/2/22/79)")
    print(f"  จิต per-เหตุ: {citta_expect}  (sum {sum(citta_expect.values())} = พิสดาร ๒๘๓)")
    print(f"  เจตสิก ๕๒ by เหตุ set-size: {dict(sorted(size_e.items()))}  (1/2/3/5/6 = 3/9/27/1/12)")
    print(f"  เจตสิก per-เหตุ: {ceta_expect}")


if __name__ == "__main__":
    main()
