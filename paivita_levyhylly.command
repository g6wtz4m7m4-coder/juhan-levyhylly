#!/bin/bash
set -e
cd "$(dirname "$0")"
python3 -m json.tool albums.json >/dev/null
if git diff --quiet -- albums.json; then echo "Ei julkaistavia muutoksia."; exit 0; fi
git add albums.json
git commit -m "${1:-Korjaa levyhyllyn albumitietoja}"
git push origin main
echo "Valmis."
