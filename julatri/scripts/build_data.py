#!/usr/bin/env python3
"""
Converts data/*.yaml into data/data.json for the static site.

Run this after editing data/cittas.yaml or data/cetasikas.yaml, then commit
the regenerated data/data.json alongside your edit:

    python3 scripts/build_data.py

สังคหนัย (citta -> cetasika) is authored directly in cittas.yaml.
สัมปโยคนัย (cetasika -> citta) and ตทุภยมิสสกนัย (cetasika -> cetasika, i.e.
which cetasikas co-occur in some shared citta) are both computed here, not
authored separately - see CONTEXT.md for why.
"""
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


# จำแนกจิต ๑๒๑ โดย ๖ ใน ๙ นัย ที่กำหนดได้ตรงตัวจาก CITTA_GROUPS (ch.1 lines 639-707).
# เวทนาเภทนัย/สัมปโยคเภทนัย/สังขารเภทนัย ไม่รวมไว้ที่นี่ เพราะแปรผันภายในกลุ่มเดียวกัน
# (ต้องเก็บเป็นฟิลด์ต่อดวงจิตแยกต่างหาก ยังไม่ได้ยืนยันครบทุกดวง)
CITTA_GROUP_LENSES = {
    "lobha-mula": {"jati": "อกุศล", "bhumi": "กาม", "sobhana": "อโสภณ", "loka": "โลกีย", "hetu": "สเหตุก", "jhana": "อฌาน"},
    "dosa-mula": {"jati": "อกุศล", "bhumi": "กาม", "sobhana": "อโสภณ", "loka": "โลกีย", "hetu": "สเหตุก", "jhana": "อฌาน"},
    "moha-mula": {"jati": "อกุศล", "bhumi": "กาม", "sobhana": "อโสภณ", "loka": "โลกีย", "hetu": "สเหตุก", "jhana": "อฌาน"},
    "ahetuka": {"jati": "วิบาก/กริยา", "bhumi": "กาม", "sobhana": "อโสภณ", "loka": "โลกีย", "hetu": "อเหตุก", "jhana": "อฌาน"},
    "mahakusala": {"jati": "กุศล", "bhumi": "กาม", "sobhana": "โสภณ", "loka": "โลกีย", "hetu": "สเหตุก", "jhana": "อฌาน"},
    "mahavipaka": {"jati": "วิบาก", "bhumi": "กาม", "sobhana": "โสภณ", "loka": "โลกีย", "hetu": "สเหตุก", "jhana": "อฌาน"},
    "mahakiriya": {"jati": "กริยา", "bhumi": "กาม", "sobhana": "โสภณ", "loka": "โลกีย", "hetu": "สเหตุก", "jhana": "อฌาน"},
    "rupa-jhana": {"jati": "กุศล/วิบาก/กริยา", "bhumi": "รูป", "sobhana": "โสภณ", "loka": "โลกีย", "hetu": "สเหตุก", "jhana": "ฌาน"},
    "arupa-jhana": {"jati": "กุศล/วิบาก/กริยา", "bhumi": "อรูป", "sobhana": "โสภณ", "loka": "โลกีย", "hetu": "สเหตุก", "jhana": "ฌาน"},
    "lokuttara": {"jati": "กุศล/วิบาก", "bhumi": "โลกุตตร", "sobhana": "โสภณ", "loka": "โลกุตตร", "hetu": "สเหตุก", "jhana": "ฌาน"},
}

# สังขารเภทนัย + เวทนาเภทนัย (ch.1 lines 685-707 give the totals; per-citta values
# reconciled against those totals below and against the per-group pali-name
# breakdown ch.1 lines 307-396, e.g. "โสมนสฺสสหคตํ...อสงฺขาริกํ" etc.). Derived
# from group + a numeric suffix on id (or the `order` field where present) --
# no new fields needed in cittas.yaml.
_ID_SUFFIX = re.compile(r"-(\d+)$")


def _citta_index(citta):
    if "order" in citta:
        return citta["order"]
    m = _ID_SUFFIX.search(citta["id"])
    return int(m.group(1)) if m else None


def citta_sankhara(citta):
    g = citta["group"]
    if g in ("ahetuka", "moha-mula"):
        return "อสังขาริก"
    if g in ("rupa-jhana", "arupa-jhana", "lokuttara"):
        return "สสังขาริก"
    if g in ("lobha-mula", "dosa-mula", "mahakusala", "mahavipaka", "mahakiriya"):
        return "อสังขาริก" if _citta_index(citta) % 2 == 1 else "สสังขาริก"
    raise ValueError(f"no สังขารเภทนัย rule for group {g!r} ({citta['id']})")


# The 4 อเหตุกจิต that break the "kaya-viññāṇa is dukkha/sukha, everything else
# in the group is upekkha except these two" pattern (ch.1 lines 328-354).
_AHETUKA_VEDANA = {
    "ahetuka-akusalavipaka-kaya": "ทุกข์",
    "ahetuka-kusalavipaka-kaya": "สุข",
    "ahetuka-kusalavipaka-somanassasantirana": "โสมนัส",
    "ahetuka-hasituppada": "โสมนัส",
}


def citta_vedana(citta):
    g = citta["group"]
    cid = citta["id"]
    if g == "dosa-mula":
        return "โทมนัส"
    if g == "moha-mula":
        return "อุเบกขา"
    if g in ("lobha-mula", "mahakusala", "mahavipaka", "mahakiriya"):
        return "โสมนัส" if _citta_index(citta) <= 4 else "อุเบกขา"
    if g == "arupa-jhana":
        return "อุเบกขา"
    if g in ("rupa-jhana", "lokuttara"):
        return "อุเบกขา" if "ปัญจมฌาน" in cid else "โสมนัส"
    if g == "ahetuka":
        return _AHETUKA_VEDANA.get(cid, "อุเบกขา")
    raise ValueError(f"no เวทนาเภทนัย rule for group {g!r} ({cid})")


# Expected totals per ch.1 lines 685-707 -- build fails loudly if a future
# cittas.yaml edit (reordering, new group) silently breaks the derivation above.
_EXPECTED_SANKHARA_TOTALS = {"อสังขาริก": 37, "สสังขาริก": 84}
_EXPECTED_VEDANA_TOTALS = {"โสมนัส": 62, "อุเบกขา": 55, "โทมนัส": 2, "ทุกข์": 1, "สุข": 1}


def main():
    cittas = load("cittas.yaml")
    cetasikas = load("cetasikas.yaml")
    cetasika_ids = {c["id"] for c in cetasikas}
    cetasika_by_id = {c["id"]: c for c in cetasikas}

    errors = []

    for citta in cittas:
        declared = citta.get("count")
        actual = len(citta["cetasikas"])
        if declared != actual:
            errors.append(
                f"{citta['id']}: count says {declared} but cetasikas list has {actual}"
            )
        unknown = set(citta["cetasikas"]) - cetasika_ids
        if unknown:
            errors.append(f"{citta['id']}: references unknown cetasika id(s) {unknown}")
        if len(citta["cetasikas"]) != len(set(citta["cetasikas"])):
            errors.append(f"{citta['id']}: has duplicate cetasika ids in its list")
        if citta["group"] not in CITTA_GROUP_LENSES:
            errors.append(f"{citta['id']}: group {citta['group']!r} has no CITTA_GROUP_LENSES entry")
        try:
            citta_sankhara(citta)
            citta_vedana(citta)
        except ValueError as e:
            errors.append(str(e))

    # excludes must be declared symmetrically and reference known ids
    for ceta in cetasikas:
        for other_id in ceta.get("excludes", []):
            if other_id not in cetasika_ids:
                errors.append(f"{ceta['id']}: excludes unknown cetasika id {other_id!r}")
                continue
            other = cetasika_by_id[other_id]
            if ceta["id"] not in other.get("excludes", []):
                errors.append(
                    f"{ceta['id']} excludes {other_id}, but {other_id} does not exclude {ceta['id']} back"
                )

    if not errors:
        from collections import Counter

        sankhara_totals = Counter(citta_sankhara(c) for c in cittas)
        vedana_totals = Counter(citta_vedana(c) for c in cittas)
        if dict(sankhara_totals) != _EXPECTED_SANKHARA_TOTALS:
            errors.append(f"สังขารเภทนัย totals {dict(sankhara_totals)} != expected {_EXPECTED_SANKHARA_TOTALS}")
        if dict(vedana_totals) != _EXPECTED_VEDANA_TOTALS:
            errors.append(f"เวทนาเภทนัย totals {dict(vedana_totals)} != expected {_EXPECTED_VEDANA_TOTALS}")

    if errors:
        print("Data validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    # สัมปโยคนัย: reverse index, cetasika -> [citta ids]
    cetasika_to_cittas = {c["id"]: [] for c in cetasikas}
    for citta in cittas:
        for ceta_id in citta["cetasikas"]:
            cetasika_to_cittas[ceta_id].append(citta["id"])

    # ตทุภยมิสสกนัย: for each cetasika, every other cetasika sharing >=1 citta with it,
    # minus any declared excludes (cetasikas that share a citta's สังคหนัย set but are
    # นานากทาจิ / never actually present together -- see CONTEXT.md).
    cooccurrence = {c["id"]: set() for c in cetasikas}
    for citta in cittas:
        members = citta["cetasikas"]
        for a in members:
            for b in members:
                if a != b:
                    cooccurrence[a].add(b)
    for ceta in cetasikas:
        excludes = set(ceta.get("excludes", []))
        if excludes:
            cooccurrence[ceta["id"]] -= excludes
    cooccurrence = {k: sorted(v) for k, v in cooccurrence.items()}

    # จำแนกนัย ๘ ใน ๙ (see CITTA_GROUP_LENSES + citta_sankhara/citta_vedana above),
    # attached per-citta for the UI overlay. สัมปโยคเภทนัย (the 9th) is deliberately
    # left out -- its per-citta membership doesn't reconcile from the textbook's
    # own stated totals (87/34) via the derivation tried so far; see CONTEXT.md.
    citta_lenses = {
        citta["id"]: {
            **CITTA_GROUP_LENSES[citta["group"]],
            "vedana": citta_vedana(citta),
            "sankhara": citta_sankhara(citta),
        }
        for citta in cittas
    }

    output = {
        "cittas": cittas,
        "cetasikas": cetasikas,
        "cetasikaToCittas": cetasika_to_cittas,
        "cooccurrence": cooccurrence,
        "cittaLenses": citta_lenses,
    }

    out_path = DATA / "data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Wrote {out_path} ({len(cittas)} cittas, {len(cetasikas)} cetasikas)")


if __name__ == "__main__":
    main()
