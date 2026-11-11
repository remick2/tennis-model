#!/usr/bin/env bash
# One consensus cycle: scan + log + grade (consensus.py) -> GitHub issues for alerts -> commit.
# consensus.py writes one .md per alert (paper play, roster warning, official report); line 1 is the title.
set -u
cd "$(dirname "$0")/.."
git pull --rebase -q || true                 # pick up tennis/check-in commits
out=$(mktemp -d)
python consensus/consensus.py "$out"
rc=$?
for f in "$out"/*.md; do
  [ -s "$f" ] || continue
  title=$(head -n 1 "$f")
  tail -n +2 "$f" > "$f.body"
  gh issue create --title "$title" --body-file "$f.body" || echo "issue failed: $title"
done
git add consensus/signals.csv consensus/summary.md
for f in consensus/reports_sent.txt consensus/health.json consensus/roster.json; do [ -f "$f" ] && git add "$f"; done
git diff --cached --quiet || git commit -qm "consensus $(date -u +%Y-%m-%dT%H:%MZ)"
for i in 1 2 3; do git pull --rebase -q && git push -q && break; sleep 5; done
exit $rc
