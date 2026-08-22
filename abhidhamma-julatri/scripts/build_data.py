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
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    cittas = load("cittas.yaml")
    cetasikas = load("cetasikas.yaml")
    cetasika_ids = {c["id"] for c in cetasikas}

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

    # ตทุภยมิสสกนัย: for each cetasika, every other cetasika sharing >=1 citta with it
    cooccurrence = {c["id"]: set() for c in cetasikas}
    for citta in cittas:
        members = citta["cetasikas"]
        for a in members:
            for b in members:
                if a != b:
                    cooccurrence[a].add(b)
    cooccurrence = {k: sorted(v) for k, v in cooccurrence.items()}

    output = {
        "cittas": cittas,
        "cetasikas": cetasikas,
        "cetasikaToCittas": cetasika_to_cittas,
        "cooccurrence": cooccurrence,
    }

    out_path = DATA / "data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Wrote {out_path} ({len(cittas)} cittas, {len(cetasikas)} cetasikas)")


if __name__ == "__main__":
    main()
