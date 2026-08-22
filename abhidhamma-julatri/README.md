# อภิธรรมชั้นจูฬตรี

Interactive study site for the จูฬตรี level of the Thai Abhidhamma curriculum. See [CONTEXT.md](./CONTEXT.md) for terminology.

## Editing content

- `data/cittas.yaml` and `data/cetasikas.yaml` are the source of truth — edit these, not `data/data.json` (which is generated).
- `lessons/*.md` hold prose explanations.

After editing either YAML file, regenerate the JSON the site actually loads:

```
python3 scripts/build_data.py
```

This also validates your edit (catches count mismatches, unknown cetasika ids, duplicates) before writing `data/data.json` — commit both the YAML change and the regenerated JSON together.

## Running locally

No build step for the site itself — it's plain HTML/CSS/JS. Serve the folder with any static server, e.g.:

```
python3 -m http.server 8000
```

then open `http://localhost:8000`.

## Deploying

Push to GitHub and enable GitHub Pages (Settings → Pages → deploy from the branch root). No further configuration needed.
