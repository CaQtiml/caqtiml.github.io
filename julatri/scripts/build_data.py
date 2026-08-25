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

# รูป ๒๘ (รูปสมุทเทสนัย only -- ch.6, data/rupas.yaml). Group -> bucket, per the
# source's own 18 นิปผันนรูป / 10 อนิปผันนรูป split (lines 102-126). Only this one
# นัย is modeled so far -- see CONTEXT.md for why the other 4 aren't here yet.
_RUPA_GROUP_BUCKET = {
    "mahabhuta": "นิปผันน",
    "pasada": "นิปผันน",
    "visaya": "นิปผันน",
    "bhava": "นิปผันน",
    "hadaya": "นิปผันน",
    "jivita": "นิปผันน",
    "ahara": "นิปผันน",
    "pariccheda": "อนิปผันน",
    "vinnatti": "อนิปผันน",
    "vikara": "อนิปผันน",
    "lakkhana": "อนิปผันน",
}
_RUPA_PASADA_GROUP = "pasada"
_EXPECTED_RUPA_TOTAL = 28
_EXPECTED_RUPA_BUCKET_TOTALS = {"นิปผันน": 18, "อนิปผันน": 10}

_PASADA_IDS = {"cakkhu-pasada", "sota-pasada", "ghana-pasada", "jivha-pasada", "kaya-pasada"}
_VISAYA_IDS = {"rupa-rammana", "sadda-rammana", "gandha-rammana", "rasa-rammana"}
_MAHABHUTA_IDS = {"pathavi", "apo", "tejo", "vayo"}
_VIKARA_IDS = {"lahuta", "muduta", "kammannata"}
_LAKKHANA_IDS = {"upacaya", "santati", "jarata", "aniccata"}
_VINNATTI_IDS = {"kaya-vinnatti", "vaci-vinnatti"}

# รูปวิภาคนัย: the 11 คู่ (ch.6, lines 561-703), each an explicit bipartition of
# the same 28 รูป by id -- hardcoded rather than derived from `group` because 3
# of the 11 (โอฬาริก/สันติเก/สัปปฏิฆ) share a 12-item set that cuts across
# mahabhuta (includes ปถวี/เตโช/วาโย but excludes อาโป), so no clean
# group-based rule exists. Negative side = every other รูป id.
#
# คู่ที่ ๘ (upadinna) is the one exception to "counts sum to 28": the source
# itself states อุปาทินนรูป=18/อนุปาทินนรูป="๔๐" (line 593), but the 40 is a
# รูปสมุฏฐานนัย cause-instance sum (จิตตช15+อุตุช13+อาหารช12) that
# double-counts รูป arising from >1 cause -- the actual unique-รูป count on the
# "not กัมมชรูป" side is 28-18=10, which is what's validated and shown here.
# See CONTEXT.md for the full explanation; don't "fix" this back to 40.
_RUPA_VIBHAGA_PAIRS = {
    "ajjhattika": ("อัชฌัตติกรูป", "พาหิรรูป", set(_PASADA_IDS)),
    "vatthu": ("วัตถุรูป", "อวัตถุรูป", _PASADA_IDS | {"hadaya-vatthu"}),
    "dvara": ("ทวารรูป", "อทวารรูป", _PASADA_IDS | {"kaya-vinnatti", "vaci-vinnatti"}),
    "indriya": ("อินทริยรูป", "อนินทริยรูป", _PASADA_IDS | {"itthi-bhava", "purisa-bhava", "jivitindriya"}),
    "olarika": ("โอฬาริกรูป", "สุขุมรูป", _PASADA_IDS | _VISAYA_IDS | {"pathavi", "tejo", "vayo"}),
    "santike": ("สันติเกรูป", "ทูเรรูป", _PASADA_IDS | _VISAYA_IDS | {"pathavi", "tejo", "vayo"}),
    "sappatigha": ("สัปปฏิฆรูป", "อัปปฏิฆรูป", _PASADA_IDS | _VISAYA_IDS | {"pathavi", "tejo", "vayo"}),
    "upadinna": ("อุปาทินนรูป", "อนุปาทินนรูป",
                 _MAHABHUTA_IDS | _PASADA_IDS | {"rupa-rammana", "gandha-rammana", "rasa-rammana"}
                 | {"itthi-bhava", "purisa-bhava", "hadaya-vatthu", "jivitindriya", "kabalinkara-ahara", "akasadhatu"}),
    "sanidassana": ("สนิทัสสนรูป", "อนิทัสสนรูป", {"rupa-rammana"}),
    "gocaraggahaka": ("โคจรัคคาหกรูป", "อโคจรัคคาหกรูป", set(_PASADA_IDS)),
    "avinibbhoga": ("อวินิพโภครูป", "วินิพโภครูป",
                     _MAHABHUTA_IDS | {"rupa-rammana", "gandha-rammana", "rasa-rammana", "kabalinkara-ahara"}),
}

# Expected (positive, negative) counts per pair, per source lines 563-605 --
# except "upadinna", checked against 18/10 (unique รูป), not the source's own
# "40" aggregate (see comment above).
_EXPECTED_VIBHAGA_TOTALS = {
    "ajjhattika": (5, 23),
    "vatthu": (6, 22),
    "dvara": (7, 21),
    "indriya": (8, 20),
    "olarika": (12, 16),
    "santike": (12, 16),
    "sappatigha": (12, 16),
    "upadinna": (18, 10),
    "sanidassana": (1, 27),
    "gocaraggahaka": (5, 23),
    "avinibbhoga": (8, 20),
}

# รูปสมุฏฐานนัย (ch.6, lines 707-831): 4 causes + a 5th "no cause" bucket
# (นกุโตจิสมุฏฐานิกรูป, for ลักขณรูป ๔). Not a bipartition like
# _RUPA_VIBHAGA_PAIRS -- a รูป can belong to more than one cause at once, so
# each entry is just (label, positive id set). "kamma"/"avinibbhoga" reuse
# the exact sets already validated above rather than retyping them.
_AVINIBBHOGA_IDS = _RUPA_VIBHAGA_PAIRS["avinibbhoga"][2]
_RUPA_SAMUTTHANA = {
    "kamma": ("กรรม", _RUPA_VIBHAGA_PAIRS["upadinna"][2]),
    "citta": ("จิต", _VINNATTI_IDS | {"sadda-rammana"} | _VIKARA_IDS | _AVINIBBHOGA_IDS | {"akasadhatu"}),
    "utu": ("อุตุ", {"sadda-rammana"} | _VIKARA_IDS | _AVINIBBHOGA_IDS | {"akasadhatu"}),
    "ahara": ("อาหาร", _VIKARA_IDS | _AVINIBBHOGA_IDS | {"akasadhatu"}),
    "nakutoci": ("นกุโตจิสมุฏฐานิกรูป", set(_LAKKHANA_IDS)),
}
_EXPECTED_SAMUTTHANA_TOTALS = {"kamma": 18, "citta": 15, "utu": 13, "ahara": 12, "nakutoci": 4}
_EXPECTED_SAMUTTHANA_CLASS_TOTALS = {"เอกันตะ": 11, "อเนกันตะ": 13, "นกุโตจิ": 4}

# จิตตชรูปนัย (ch.6, lines 874-923), coarse (activity-label) granularity only
# -- see CONTEXT.md for why the finer จิต-group->รูป-id table (lines 892-923)
# isn't modeled. Counts are stated in the source against a 75-of-89 baseline;
# this dataset's lokuttara group is already the 121-total พิสดาร expansion
# (40 instead of 8), so any rule that touches lokuttara lands on a bigger
# number here than the source's own -- documented per-activity below and in
# CONTEXT.md, not treated as an error.

# ทวิปัญจวิญญาณ ๑๐ + อรูปวิบาก ๔: always excluded from every จิตตชรูป activity
# (ch.6 lines 729-731), identifiable from fields already in cittas.yaml.
def _always_ineligible_citta_ids(cittas):
    ids = set()
    for c in cittas:
        if c["group"] == "ahetuka" and c["pali"].startswith("ทวิปัญจวิญญาณ"):
            ids.add(c["id"])
        if c["group"] == "arupa-jhana" and c["thai"].endswith("(วิบาก)"):
            ids.add(c["id"])
    return ids


# กามชวนะ ๒๙ (ch.6 line 882 etc.): all of the 5 กามาวจรชวนจิต groups,
# unconditionally, plus หสิตุปปาทจิต.
def _kamajavana_ids(cittas):
    groups = {"lobha-mula", "dosa-mula", "moha-mula", "mahakusala", "mahakiriya"}
    ids = {c["id"] for c in cittas if c["group"] in groups}
    ids.add("ahetuka-hasituppada")
    return ids


# อภิญญาจิต ๒ (ch.6 line 890): the 5th-jhāna รูปาวจรกุศล/กิริยาจิต specifically
# -- reuses the same "ปัญจมฌาน" id-substring convention as citta_vedana above.
def _abhinna_ids(cittas):
    return {
        c["id"]
        for c in cittas
        if c["group"] == "rupa-jhana" and "ปัญจมฌาน" in c["id"] and not c["thai"].endswith("(วิบาก)")
    }


# อัปปนาชวนะ (ch.6 line 888): รูปาวจร/อรูปาวจร กุศล+กิริยา (excludes วิบาก) plus
# every โลกุตตรจิต (magga and phala both count; no วิบาก-only exclusion for
# lokuttara in the source). In this dataset's 121-expanded lokuttara group,
# this pulls in all 40 lokuttara entries, not the source's base 8 -- see
# CONTEXT.md for why iriyapatha_yai_tangman's total is 88, not 56.
def _appana_javana_ids(cittas):
    ids = {
        c["id"]
        for c in cittas
        if c["group"] in ("rupa-jhana", "arupa-jhana") and (c["thai"].endswith("(กุศล)") or c["thai"].endswith("(กิริยา)"))
    }
    ids |= {c["id"] for c in cittas if c["group"] == "lokuttara"}
    return ids


def _build_cittaja_activities(cittas):
    always_ineligible = _always_ineligible_citta_ids(cittas)
    samanya_ids = {c["id"] for c in cittas} - always_ineligible
    hasa_ids = {c["id"] for c in cittas if citta_vedana(c) == "โสมนัส" and c["group"] in ("lobha-mula", "mahakusala", "mahakiriya")}
    hasa_ids.add("ahetuka-hasituppada")
    roditta_ids = {c["id"] for c in cittas if c["group"] == "dosa-mula"}
    kamajavana_ids = _kamajavana_ids(cittas)
    abhinna_ids = _abhinna_ids(cittas)
    manodvaravajjana_ids = {"ahetuka-manodvaravajjana"}
    iriya_noi_vaca_yai_ids = kamajavana_ids | manodvaravajjana_ids | abhinna_ids
    appana_javana_ids = _appana_javana_ids(cittas)
    yai_tangman_ids = manodvaravajjana_ids | kamajavana_ids | appana_javana_ids

    return [
        ("samanya", "จิตตชรูปสามัญ", samanya_ids),
        ("hasa", "การหัวเราะ", hasa_ids),
        ("roditta", "การร้องไห้", roditta_ids),
        ("iriyapatha_noi", "อิริยาบถน้อย", iriya_noi_vaca_yai_ids),
        ("vaca", "การพูด", iriya_noi_vaca_yai_ids),
        ("iriyapatha_yai", "อิริยาบถใหญ่ทั้ง ๔", iriya_noi_vaca_yai_ids),
        ("iriyapatha_yai_tangman", "อิริยาบถใหญ่ทั้ง ๔ ตั้งมั่น", yai_tangman_ids),
    ]


_EXPECTED_CITTAJA_TOTALS = {
    "samanya": 107,
    "hasa": 13,
    "roditta": 2,
    "iriyapatha_noi": 32,
    "vaca": 32,
    "iriyapatha_yai": 32,
    "iriyapatha_yai_tangman": 88,
}


def main():
    cittas = load("cittas.yaml")
    cetasikas = load("cetasikas.yaml")
    rupas = load("rupas.yaml")["rupas"]
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

    # รูป ๒๘: purely structural validation -- no relation to derive for this
    # first slice, just confirm the data matches the source's own stated counts.
    rupa_ids = [r["id"] for r in rupas]
    if len(rupa_ids) != len(set(rupa_ids)):
        errors.append("rupas.yaml: has duplicate รูป ids")
    for rupa in rupas:
        if rupa["group"] not in _RUPA_GROUP_BUCKET:
            errors.append(f"{rupa['id']}: group {rupa['group']!r} has no known นิปผันน/อนิปผันน bucket")
        has_kicha = "kicha" in rupa
        is_pasada = rupa["group"] == _RUPA_PASADA_GROUP
        if has_kicha != is_pasada:
            errors.append(f"{rupa['id']}: กิจ field should be present only on ปสาทรูป entries (group={rupa['group']!r}, has_kicha={has_kicha})")

    if not errors:
        from collections import Counter

        sankhara_totals = Counter(citta_sankhara(c) for c in cittas)
        vedana_totals = Counter(citta_vedana(c) for c in cittas)
        if dict(sankhara_totals) != _EXPECTED_SANKHARA_TOTALS:
            errors.append(f"สังขารเภทนัย totals {dict(sankhara_totals)} != expected {_EXPECTED_SANKHARA_TOTALS}")
        if dict(vedana_totals) != _EXPECTED_VEDANA_TOTALS:
            errors.append(f"เวทนาเภทนัย totals {dict(vedana_totals)} != expected {_EXPECTED_VEDANA_TOTALS}")

        if len(rupas) != _EXPECTED_RUPA_TOTAL:
            errors.append(f"รูป total {len(rupas)} != expected {_EXPECTED_RUPA_TOTAL}")
        rupa_bucket_totals = Counter(_RUPA_GROUP_BUCKET[r["group"]] for r in rupas)
        if dict(rupa_bucket_totals) != _EXPECTED_RUPA_BUCKET_TOTALS:
            errors.append(f"นิปผันน/อนิปผันน totals {dict(rupa_bucket_totals)} != expected {_EXPECTED_RUPA_BUCKET_TOTALS}")

        for pair_key, (pos_label, neg_label, pos_ids) in _RUPA_VIBHAGA_PAIRS.items():
            unknown = pos_ids - set(rupa_ids)
            if unknown:
                errors.append(f"รูปวิภาคนัย {pair_key!r}: unknown รูป id(s) {unknown}")
                continue
            expected_pos, expected_neg = _EXPECTED_VIBHAGA_TOTALS[pair_key]
            actual_pos = len(pos_ids)
            actual_neg = len(rupas) - actual_pos
            if (actual_pos, actual_neg) != (expected_pos, expected_neg):
                errors.append(
                    f"รูปวิภาคนัย {pair_key!r} ({pos_label}/{neg_label}): counts "
                    f"{(actual_pos, actual_neg)} != expected {(expected_pos, expected_neg)}"
                )

        for cause_key, (cause_label, cause_ids) in _RUPA_SAMUTTHANA.items():
            unknown = cause_ids - set(rupa_ids)
            if unknown:
                errors.append(f"รูปสมุฏฐานนัย {cause_key!r}: unknown รูป id(s) {unknown}")
                continue
            expected = _EXPECTED_SAMUTTHANA_TOTALS[cause_key]
            if len(cause_ids) != expected:
                errors.append(
                    f"รูปสมุฏฐานนัย {cause_key!r} ({cause_label}): count {len(cause_ids)} != expected {expected}"
                )

        samutthana_class_totals = Counter()
        for rid in rupa_ids:
            causes = [k for k, (_, ids) in _RUPA_SAMUTTHANA.items() if k != "nakutoci" and rid in ids]
            if rid in _RUPA_SAMUTTHANA["nakutoci"][1]:
                samutthana_class_totals["นกุโตจิ"] += 1
            elif len(causes) == 1:
                samutthana_class_totals["เอกันตะ"] += 1
            elif len(causes) > 1:
                samutthana_class_totals["อเนกันตะ"] += 1
            else:
                errors.append(f"รูปสมุฏฐานนัย: {rid!r} has no cause and is not in นกุโตจิ bucket")
        if not errors and dict(samutthana_class_totals) != _EXPECTED_SAMUTTHANA_CLASS_TOTALS:
            errors.append(
                f"เอกันตะ/อเนกันตะ/นกุโตจิ totals {dict(samutthana_class_totals)} != expected {_EXPECTED_SAMUTTHANA_CLASS_TOTALS}"
            )

        cittaja_activities = _build_cittaja_activities(cittas)
        for key, label, ids in cittaja_activities:
            unknown = ids - {c["id"] for c in cittas}
            if unknown:
                errors.append(f"จิตตชรูปนัย {key!r}: unknown จิต id(s) {unknown}")
                continue
            expected = _EXPECTED_CITTAJA_TOTALS[key]
            if len(ids) != expected:
                errors.append(f"จิตตชรูปนัย {key!r} ({label}): count {len(ids)} != expected {expected}")

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

    # รูปวิภาคนัย: per-รูป side + label for each of the 11 คู่, for the
    # rupa.html lens overlay (mirrors citta_lenses above, one shared circle
    # type instead of two, so no cross-highlight index is needed).
    rupa_lenses = {}
    for rupa in rupas:
        entry = {}
        for pair_key, (pos_label, neg_label, pos_ids) in _RUPA_VIBHAGA_PAIRS.items():
            entry[pair_key] = pos_label if rupa["id"] in pos_ids else neg_label
        rupa_lenses[rupa["id"]] = entry

    # รูปสมุฏฐานนัย: per-รูป cause list + เอกันตะ/อเนกันตะ/นกุโตจิ class, for the
    # rupa.html สมุฏฐานนัย tab (bidirectional, so also emit the 5 cause
    # entries themselves for the right-panel).
    rupa_samutthana_causes = [
        {"key": key, "label": label} for key, (label, _) in _RUPA_SAMUTTHANA.items()
    ]
    rupa_samutthana = {}
    for rupa in rupas:
        rid = rupa["id"]
        causes = [k for k, (_, ids) in _RUPA_SAMUTTHANA.items() if k != "nakutoci" and rid in ids]
        if rid in _RUPA_SAMUTTHANA["nakutoci"][1]:
            cls = "นกุโตจิ"
        elif len(causes) == 1:
            cls = "เอกันตะ"
        else:
            cls = "อเนกันตะ"
        rupa_samutthana[rid] = {"causes": causes, "class": cls}

    # จิตตชรูปนัย (coarse): 7 activities + which of the 14 always-ineligible
    # จิต to render disabled in the right panel (see CONTEXT.md).
    cittaja_activities = _build_cittaja_activities(cittas)
    cittaja_activities_out = [
        {"key": key, "label": label, "cittaIds": sorted(ids)} for key, label, ids in cittaja_activities
    ]
    always_ineligible = _always_ineligible_citta_ids(cittas)
    citta_eligibility = {c["id"]: c["id"] not in always_ineligible for c in cittas}

    output = {
        "cittas": cittas,
        "cetasikas": cetasikas,
        "cetasikaToCittas": cetasika_to_cittas,
        "cooccurrence": cooccurrence,
        "cittaLenses": citta_lenses,
        "rupas": rupas,
        "rupaLenses": rupa_lenses,
        "rupaSamutthana": rupa_samutthana,
        "rupaSamutthanaCauses": rupa_samutthana_causes,
        "cittajaActivities": cittaja_activities_out,
        "cittaEligibility": citta_eligibility,
    }

    out_path = DATA / "data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Wrote {out_path} ({len(cittas)} cittas, {len(cetasikas)} cetasikas, {len(rupas)} rupas)")


if __name__ == "__main__":
    main()
