#!/usr/bin/env bash
# Download match data (Sackmann archive mirror, pinned) + odds/results dataset (latest weekly update).
set -euo pipefail
mkdir -p "$(dirname "$0")/../data/raw"
cd "$(dirname "$0")/../data/raw"
mkdir -p atp wta odds
SACK=https://huggingface.co/datasets/Aneeshers/tennis-sackmann-archive/resolve/8ac86f7c62889b5d5c4cfec4c6403edcb8c5d993
while read -r f; do [ -s "$f" ] || curl -sSLf -m 120 "$SACK/$f" -o "$f"; done < ../../scripts/sackmann_files.txt
ODDS=https://huggingface.co/datasets/minmaxxxer/atp-wta-matches-with-odds/resolve/main
for f in atp_matches_2025 atp_matches_2026 wta_matches_2025 wta_matches_2026; do
  curl -sSLf -m 120 "$ODDS/$f.csv" -o "odds/$f.csv"
done
echo "data ok: $(ls atp | wc -l) atp, $(ls wta | wc -l) wta, $(ls odds | wc -l) odds files"
