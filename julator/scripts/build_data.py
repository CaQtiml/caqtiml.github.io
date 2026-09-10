#!/usr/bin/env python3
"""
Compile data/*.yaml -> data/data.json for the static site.

    python3 scripts/build_data.py

Sources:
  data/paramattha.yaml  canonical id space (จิต ๑๒๑ / เจตสิก ๕๒ / รูป ๒๘ / นิพพาน).
                        Seeded from julatri -- see scripts/seed_paramattha.py + adr/0001.
  data/p3/<scheme>.yaml ปริจเฉทที่ ๓ ปกิณณกสังคหะ -- one fragment per นัย, each the
                        scheme dict itself. Assembled here in P3_ORDER; a นัย with
                        no fragment becomes a disabled stub tab. Each is generated
                        by its own scripts/derive_p3_<scheme>.py.
  data/p7.yaml          ปริจเฉทที่ ๗ สมุจจยสังคหะ -- dhamma-set <-> ปรมัตถ์ index.

Validation (build fails on any):
  * a p3 assignment `ref` that is not a paramattha id of the right kind
    (citta block -> citta id, cetasika block -> cetasika id)
  * a `cats` entry not in that block's `categories`
  * cardinality: partition -> every assignment has exactly 1 cat
  * an `expect` per-category count that does not match
  * a `groupings[].expect` set-size count that does not match
  * a `views[].collapse` key/value not a category id
  * a p7 `ongkhatham` id not in paramattha, or an `expect` member count mismatch

p3 scheme shape (per docs/SHARED-UNDERSTANDING.md):
  schemes:
    - id: <slug>
      thai: <name>
      source: <ref>            # optional
      gatha: <pali>            # optional
      note: <text>             # optional (legacy flat string)
      notes: [ <str> | {t, sub:[<str>...]} ]   # optional bulleted explanation
      views:                   # optional sub-toggles
        - { id: <slug>, thai: <label>, collapse: { <cat>: <cat> } }
      citta: <axis-block> | null
      cetasika: <axis-block> | null
  axis-block:
    axis: <label>
    cardinality: partition | matrix
    categories: [ { id, thai }, ... ]
    groupings: [ { id, thai, size, expect } ]   # optional (matrix summary buckets)
    expect: { <cat id>: <int> }                 # optional
    assignments: [ { ref: <paramattha id>, cats: [<cat id>...], note? } ]
"""
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

# the 6 ปกิณณกสังคหะ นัย, in textbook order. Each has a fragment at
# data/p3/<id>.yaml (the scheme dict) once built; the rest render as stub tabs.
P3_ORDER = [
    ("vedana", "เวทนาสังคหะ"),
    ("hetu", "เหตุสังคหะ"),
    ("kicca", "กิจจสังคหะ"),
    ("dvara", "ทวารสังคหะ"),
    ("arammana", "อารัมมณสังคหะ"),
    ("vatthu", "วัตถุสังคหะ"),
]


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_p3():
    schemes = []
    for sid, thai in P3_ORDER:
        frag = DATA / "p3" / f"{sid}.yaml"
        if frag.exists():
            sch = yaml.safe_load(frag.read_text(encoding="utf-8")) or {}
            sch.setdefault("id", sid)
            sch.setdefault("thai", thai)
            schemes.append(sch)
        else:
            schemes.append({"id": sid, "thai": thai, "citta": None, "cetasika": None})
    return {"schemes": schemes}


def check_axis(errors, where, block, kind, ids_of_kind):
    """Validate one citta/cetasika axis-block of a p3 scheme.

    `ids_of_kind` is the set of paramattha ids of exactly this kind -- the id
    space is per-kind, so `jivitindriya` (both a เจตสิก and a รูป) is only a
    collision if the two kinds are flattened, which we never do here.
    """
    if block is None:
        return
    cats = {c["id"] for c in block.get("categories", [])}
    if not cats:
        errors.append(f"{where}: axis-block has no categories")
    card = block.get("cardinality")
    if card not in ("partition", "matrix"):
        errors.append(f"{where}: cardinality must be 'partition' or 'matrix', got {card!r}")

    seen = set()
    got = Counter()
    size_counts = Counter()
    for asg in block.get("assignments", []) or []:
        ref = asg.get("ref")
        if ref in seen:
            errors.append(f"{where}: duplicate assignment for {ref!r}")
        seen.add(ref)
        if ref not in ids_of_kind:
            errors.append(f"{where}: ref {ref!r} is not a {kind} id in paramattha.yaml")
        bad = [c for c in asg.get("cats", []) if c not in cats]
        if bad:
            errors.append(f"{where}: {ref!r} uses undeclared categor(y/ies) {bad}")
        if card == "partition" and len(asg.get("cats", [])) != 1:
            errors.append(f"{where}: partition scheme but {ref!r} has {len(asg.get('cats', []))} cats")
        for c in asg.get("cats", []):
            got[c] += 1
        size_counts[len(asg.get("cats", []))] += 1

    exp = block.get("expect")
    if exp:
        for cat_id, want in exp.items():
            if cat_id not in cats:
                errors.append(f"{where}: expect names unknown category {cat_id!r}")
            elif got.get(cat_id, 0) != want:
                errors.append(f"{where}: category {cat_id!r} count {got.get(cat_id, 0)} != expected {want}")

    for g in block.get("groupings", []) or []:
        if size_counts.get(g["size"], 0) != g["expect"]:
            errors.append(
                f"{where}: grouping {g['id']!r} (size {g['size']}) count "
                f"{size_counts.get(g['size'], 0)} != expected {g['expect']}"
            )


def main():
    para = load("paramattha.yaml")
    p3 = load_p3()
    p7 = load("p7.yaml")

    ids_by_kind = {
        kind: {entry["id"] for entry in para.get(kind, [])}
        for kind in ("citta", "cetasika", "rupa", "nibbana")
    }
    all_para_ids = set().union(*ids_by_kind.values())

    errors = []

    # ---- p3 ----
    p3_schemes = p3.get("schemes", []) or []
    for sch in p3_schemes:
        sid = sch.get("id", "<no id>")
        check_axis(errors, f"p3 {sid!r} .citta", sch.get("citta"), "citta", ids_by_kind["citta"])
        check_axis(errors, f"p3 {sid!r} .cetasika", sch.get("cetasika"), "cetasika", ids_by_kind["cetasika"])
        all_cats = set()
        for blk in (sch.get("citta"), sch.get("cetasika")):
            if blk:
                all_cats |= {c["id"] for c in blk.get("categories", [])}
        for v in sch.get("views", []) or []:
            for k, val in (v.get("collapse") or {}).items():
                if k not in all_cats or val not in all_cats:
                    errors.append(f"p3 {sid!r} view {v.get('id')!r}: collapse {k!r}->{val!r} not category ids")

    # ---- p7 ----
    p7_sangahas = p7.get("sangahas", []) or []
    for sg in p7_sangahas:
        for dset in sg.get("sets", []) or []:
            for member in dset.get("members", []) or []:
                unknown = [i for i in member.get("ongkhatham", []) or [] if i not in all_para_ids]
                if unknown:
                    errors.append(f"p7 {sg.get('id')}/{dset.get('id')}/{member.get('id', '?')}: unknown ปรมัตถ์ id(s) {unknown}")
            exp = dset.get("expect")
            if exp is not None and len(dset.get("members", []) or []) != exp:
                errors.append(f"p7 set {dset.get('id')!r}: member count {len(dset.get('members', []) or [])} != expected {exp}")

    if errors:
        print("Data validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    # ---- p3: reverse index paramattha id -> {scheme: [cats]} per axis ----
    p3_reverse = {"citta": {}, "cetasika": {}}
    for sch in p3_schemes:
        for kind in ("citta", "cetasika"):
            blk = sch.get(kind)
            if not blk:
                continue
            for asg in blk.get("assignments", []) or []:
                p3_reverse[kind].setdefault(asg["ref"], {})[sch["id"]] = asg.get("cats", [])

    # ---- p7 reverse index: ปรมัตถ์ id -> [{sangaha, set, member}] ----
    p7_reverse = {}
    for sg in p7_sangahas:
        for dset in sg.get("sets", []) or []:
            for member in dset.get("members", []) or []:
                for pid in member.get("ongkhatham", []) or []:
                    p7_reverse.setdefault(pid, []).append(
                        {"sangaha": sg["id"], "set": dset["id"], "member": member.get("id")}
                    )

    output = {
        "paramattha": para,
        "p3": {"schemes": p3_schemes, "reverse": p3_reverse},
        "p7": {"sangahas": p7_sangahas, "reverse": p7_reverse},
    }

    out_path = DATA / "data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    n_para = sum(len(para.get(k, [])) for k in ("citta", "cetasika", "rupa", "nibbana"))
    filled = [s["id"] for s in p3_schemes if s.get("citta") or s.get("cetasika")]
    print(
        f"Wrote {out_path} ({n_para} ปรมัตถ์ ids; "
        f"p3 schemes filled: {filled or 'none'}; "
        f"{sum(len(sg.get('sets', []) or []) for sg in p7_sangahas)} p7 dhamma-sets)"
    )


if __name__ == "__main__":
    main()
