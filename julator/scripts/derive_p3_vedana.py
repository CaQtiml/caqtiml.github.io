#!/usr/bin/env python3
"""
Generate data/p3.yaml with the เวทนาสังคหะ scheme fully populated (the other 5
schemes stay as stubs).

Sources / cross-checks:
  * reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L52-L153 -- the authoritative text.
    - จิต by เวทนา ๕: สุข 1, ทุกข์ 1, โสมนัส 62, โทมนัส 2, อุเบกขา 55  (คาถาที่ ๒)
    - เจตสิก by set-size: 6 / 28 / 11 / 0 / 6 / 1
  * ../../julatri/abhidhamma-julatri/data/data.json -- per-citta เวทนา is taken
    from julatri's cittaLenses (verified there against the จูฬตรี textbook
    pp.50-56); this script asserts its totals equal the จูฬโท คาถา totals, i.e.
    two independent sources agree before anything is written.
  * every non-เวทนา เจตสิก's authored เวทนา-set is re-checked against the actual
    co-occurrence in julatri's cetasikaToCittas.

Run: python3 scripts/derive_p3_vedana.py   (then: python3 scripts/build_data.py)
"""
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
JULATRI_JSON = ROOT.parent.parent / "julatri" / "abhidhamma-julatri" / "data" / "data.json"
PARAMATTHA = ROOT / "data" / "paramattha.yaml"
OUT = ROOT / "data" / "p3" / "vedana.yaml"

TH2CAT = {"สุข": "sukha", "ทุกข์": "dukkha", "โสมนัส": "somanassa", "โทมนัส": "domanassa", "อุเบกขา": "upekkha"}
CAT_ORDER = ["sukha", "dukkha", "somanassa", "domanassa", "upekkha"]
CAT_THAI = {"sukha": "สุขเวทนา", "dukkha": "ทุกขเวทนา", "somanassa": "โสมนัสเวทนา", "domanassa": "โทมนัสเวทนา", "upekkha": "อุเบกขาเวทนา"}

# เจตสิก -> the เวทนา ๕ it co-occurs with, straight from the text's own wording
# (L127-L147). Keys are julatri cetasika-group ids; expanded to member ids below.
CETASIKA_GROUP_VEDANA = {
    # ๑. เกิดกับเวทนาเดียว (6)
    "dosa-catuka": ["domanassa"],          # โทจตุก ๔  -> โทมนัส
    "vicikiccha": ["upekkha"],             # วิจิกิจฉา ๑ -> อุเบกขา
    # piti handled individually (pakinnaka is otherwise a 3-vedana group)
    # ๒. เกิดกับ ๒ เวทนา (28): โสมนัส + อุเบกขา
    "lobha-tika": ["somanassa", "upekkha"],
    "sobhana-sadharana": ["somanassa", "upekkha"],
    "virati": ["somanassa", "upekkha"],
    "appamanna": ["somanassa", "upekkha"],
    "pannindriya": ["somanassa", "upekkha"],
    # ๓. เกิดกับ ๓ เวทนา (11): โสมนัส + โทมนัส + อุเบกขา
    "moha-catuka": ["somanassa", "domanassa", "upekkha"],
    "thina-duka": ["somanassa", "domanassa", "upekkha"],
    # pakinnaka minus piti -> 3-vedana; piti -> โสมนัส only
    # ๕. เกิดกับ ๕ เวทนา (6): สัพพจิตตสาธารณ ๖ เว้นเวทนา
    "sabbacitta-sadharana": ["sukha", "dukkha", "somanassa", "domanassa", "upekkha"],
}
PAKINNAKA_NON_PITI = ["somanassa", "domanassa", "upekkha"]

# The text's own summary buckets (L127-L147), checked by set size.
CETASIKA_GROUPINGS = [
    {"id": "one",   "thai": "เกิดกับเวทนาเดียว", "size": 1, "expect": 6},
    {"id": "two",   "thai": "เกิดกับ ๒ เวทนา",   "size": 2, "expect": 28},
    {"id": "three", "thai": "เกิดกับ ๓ เวทนา",   "size": 3, "expect": 11},
    {"id": "four",  "thai": "เกิดกับ ๔ เวทนา",   "size": 4, "expect": 0},
    {"id": "five",  "thai": "เกิดกับ ๕ เวทนา",   "size": 5, "expect": 6},
    {"id": "none",  "thai": "ไม่เกิดกับเวทนา",    "size": 0, "expect": 1},
]

GATHA = (
    "สุขํ ทุกฺขมุเปกฺขาติ ติวิธา ตตฺถ เวทนา / โสมนสฺสํ โทมนสฺสมิติ เภเทน ปญฺจธา\n"
    "สุขเมกตฺถ ทุกฺขญฺจ โทมนสฺสํ ทฺวเย ฐิตํ / ทฺวาสฏฺฐีสุ โสมนสฺสํ ปญฺจปญฺญาสเกตรา"
)


def die(msg):
    sys.exit(f"derive_p3_vedana: {msg}")


def main():
    if not JULATRI_JSON.exists():
        die(f"julatri data.json not found: {JULATRI_JSON}")
    jd = json.load(open(JULATRI_JSON, encoding="utf-8"))
    para = yaml.safe_load(open(PARAMATTHA, encoding="utf-8"))

    citta_ids = [c["id"] for c in para["citta"]]
    cetasikas = para["cetasika"]
    ceta_by_group = {}
    for c in cetasikas:
        ceta_by_group.setdefault(c["group"], []).append(c["id"])

    # ---- จิต by เวทนา ๕, from julatri cittaLenses ----
    lenses = jd["cittaLenses"]
    if set(lenses) != set(citta_ids):
        die("julatri citta id set != paramattha.yaml citta id set")
    citta_assign = []
    ccount = {k: 0 for k in CAT_ORDER}
    for cid in citta_ids:
        th = lenses[cid]["vedana"]
        if th not in TH2CAT:
            die(f"unknown เวทนา {th!r} for {cid}")
        cat = TH2CAT[th]
        citta_assign.append({"ref": cid, "cats": [cat]})
        ccount[cat] += 1
    expect_citta = {"sukha": 1, "dukkha": 1, "somanassa": 62, "domanassa": 2, "upekkha": 55}
    if ccount != expect_citta:
        die(f"จิต by เวทนา ๕ totals {ccount} != จูฬโท คาถา {expect_citta}")

    # ---- เจตสิก by co-occurring เวทนา ๕, from the text's wording ----
    ceta_sets = {}
    for group, cats in CETASIKA_GROUP_VEDANA.items():
        for cid in ceta_by_group.get(group, []):
            ceta_sets[cid] = list(cats)
    for cid in ceta_by_group.get("pakinnaka", []):
        ceta_sets[cid] = ["somanassa"] if cid == "piti" else list(PAKINNAKA_NON_PITI)
    ceta_sets["vedana"] = []  # เวทนา is not classified by itself (L146-147)

    missing = set(c["id"] for c in cetasikas) - set(ceta_sets)
    if missing:
        die(f"no เวทนา-set assigned for เจตสิก: {sorted(missing)}")

    # size-bucket check against the text's 6/28/11/0/6/1
    size_counts = {g["id"]: 0 for g in CETASIKA_GROUPINGS}
    for cid, s in ceta_sets.items():
        for g in CETASIKA_GROUPINGS:
            if len(s) == g["size"]:
                size_counts[g["id"]] += 1
    for g in CETASIKA_GROUPINGS:
        if size_counts[g["id"]] != g["expect"]:
            die(f"เจตสิก set-size {g['id']} ({g['size']}) count {size_counts[g['id']]} != text {g['expect']}")

    # cross-check every non-เวทนา เจตสิก against julatri actual co-occurrence
    c2c = jd["cetasikaToCittas"]
    for cid, s in ceta_sets.items():
        if cid == "vedana":
            continue
        actual = sorted({TH2CAT[lenses[x]["vedana"]] for x in c2c[cid]}, key=CAT_ORDER.index)
        if actual != sorted(s, key=CAT_ORDER.index):
            die(f"เจตสิก {cid}: authored set {s} != julatri co-occurrence {actual}")

    ceta_assign = [
        {"ref": c["id"], "cats": sorted(ceta_sets[c["id"]], key=CAT_ORDER.index)}
        for c in cetasikas
    ]
    expect_ceta = {k: 0 for k in CAT_ORDER}
    for a in ceta_assign:
        for cat in a["cats"]:
            expect_ceta[cat] += 1

    def categories():
        return [{"id": k, "thai": CAT_THAI[k]} for k in CAT_ORDER]

    vedana = {
        "id": "vedana",
        "thai": "เวทนาสังคหะ",
        "source": "reference/01-ปริจเฉทที่3-ปกิณณกสังคหะ.md L52-L153",
        "gatha": GATHA,
        "notes": [
            {"t": "<strong>จิต</strong> — จำแนกโดยอินทริยเภทนัย (เวทนา ๕) แต่ละดวงมีเวทนาเดียว",
             "sub": [
                 "ปุ่มด้านบนสลับ เวทนา ๕ (อินทริยเภทนัย) ↔ เวทนา ๓ (อารัมมณานุภวนลักขณนัย — ยุบโสมนัส→สุข, โทมนัส→ทุกข์)",
             ]},
            {"t": "<strong>เจตสิก</strong> — จำแนกโดยเวทนา ๕ ที่เกิดร่วม (๐–๕ เวทนาต่อดวง)",
             "sub": [
                 "เวทนาเจตสิกเองไม่จัดเข้าเวทนาใด (ไม่เกิดร่วมกับตนเอง)",
             ]},
        ],
        "views": [
            {"id": "vedana5", "thai": "เวทนา ๕ (อินทริยเภทนัย)"},
            {"id": "vedana3", "thai": "เวทนา ๓ (อารัมมณานุภวนลักขณนัย)",
             "collapse": {"somanassa": "sukha", "domanassa": "dukkha"}},
        ],
        "citta": {
            "axis": "เวทนา ๕",
            "cardinality": "partition",
            "categories": categories(),
            "expect": expect_citta,
            "assignments": citta_assign,
        },
        "cetasika": {
            "axis": "เวทนา ๕ ที่เกิดร่วม",
            "cardinality": "matrix",
            "categories": categories(),
            "groupings": CETASIKA_GROUPINGS,
            "expect": expect_ceta,
            "assignments": ceta_assign,
        },
    }

    header = (
        "# ปริจเฉทที่ ๓ ปกิณณกสังคหะ -- scheme fragment: เวทนาสังคหะ.\n"
        "#\n"
        "# GENERATED by scripts/derive_p3_vedana.py (verified against\n"
        "# reference/01-...md L52-L153 and cross-checked with julatri).\n"
        "# Re-run that script to regenerate; do not hand-edit.\n"
        "# build_data.py assembles data/p3/*.yaml (in P3_ORDER) into data.json;\n"
        "# a scheme with no fragment renders as a disabled stub tab.\n"
        "#\n"
        "# scheme shape: see docs/SHARED-UNDERSTANDING.md and CONTEXT.md.\n"
        f"#   จิต by เวทนา ๕: {expect_citta}\n"
        f"#   เจตสิก by เวทนา ๕: {expect_ceta}\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(vedana, f, allow_unicode=True, sort_keys=False, width=1000, default_flow_style=False)

    print(f"Wrote {OUT}")
    print(f"  จิต ๑๒๑ by เวทนา ๕: {expect_citta}")
    print(f"  เจตสิก ๕๒ by เวทนา ๕: {expect_ceta}")
    print(f"  เจตสิก set-size buckets: {size_counts}")


if __name__ == "__main__":
    main()
