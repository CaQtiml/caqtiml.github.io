#!/usr/bin/env python3
"""
One-off seed: build data/paramattha.yaml (the canonical id + label registry for
จิต ๑๒๑ / เจตสิก ๕๒ / รูป ๒๘ / นิพพาน) by copying the id space from the sibling
julatri project.

    python3 scripts/seed_paramattha.py

This is deliberately a copy, not a live import -- see docs/adr/0001. Re-run only
when intentionally re-syncing the id space with julatri; review the diff by hand.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
JULATRI = ROOT.parent.parent / "julatri" / "abhidhamma-julatri" / "data"
OUT = ROOT / "data" / "paramattha.yaml"


def load(name):
    with open(JULATRI / name, encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    if not JULATRI.exists():
        sys.exit(f"julatri data dir not found: {JULATRI}")

    cittas = load("cittas.yaml")
    cetasikas = load("cetasikas.yaml")
    rupas = load("rupas.yaml")["rupas"]

    doc = {
        "citta": [
            {"id": c["id"], "thai": c["thai"], "group": c["group"], "pali": c.get("pali", "")}
            for c in cittas
        ],
        "cetasika": [
            {"id": c["id"], "thai": c["thai"], "group": c["group"], "meaning": c.get("meaning", "")}
            for c in cetasikas
        ],
        "rupa": [
            {"id": r["id"], "thai": r["thai"], "group": r["group"]}
            for r in rupas
        ],
        "nibbana": [
            {"id": "nibbana", "thai": "นิพพาน", "group": "nibbana"}
        ],
    }

    header = (
        "# ปรมัตถ์ id + label registry -- the shared key space for the p3 and p7 tools.\n"
        "# SEEDED from ../../julatri/abhidhamma-julatri/data/{cittas,cetasikas,rupas}.yaml\n"
        "# by scripts/seed_paramattha.py. This repo owns this copy -- see docs/adr/0001\n"
        "# for why it is a copy and not a live import.\n"
        f"# Counts: citta {len(doc['citta'])}, cetasika {len(doc['cetasika'])}, "
        f"rupa {len(doc['rupa'])}, nibbana {len(doc['nibbana'])}.\n"
    )
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump(doc, f, allow_unicode=True, sort_keys=False, width=1000)

    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
