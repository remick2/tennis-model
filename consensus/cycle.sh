#!/usr/bin/env bash
# One consensus cycle: scan + log + grade (consensus.py) -> GitHub issues for alerts -> commit.
set -u
cd "$(dirname "$0")/.."
git pull --rebase -q || true                 # pick up tennis/check-in commits
out=$(mktemp -d)
python consensus/consensus.py "$out"
rc=$?
stamp=$(TZ=America/Denver date '+%a %b %-d %-I:%M%p')
if [ -s "$out/play.md" ]; then
  gh issue create --title "Consensus paper play: $stamp MT" --body-file "$out/play.md" || echo "issue failed"
fi
if [ -s "$out/week.md" ]; then
  gh issue create --title "Consensus weekly check-in: $(TZ=America/Denver date '+%b %-d')" --body-file "$out/week.md" || echo "issue failed"
fi
git add consensus/signals.csv consensus/summary.md
[ -f consensus/last_checkin.txt ] && git add consensus/last_checkin.txt
git diff --cached --quiet || git commit -qm "consensus $(date -u +%Y-%m-%dT%H:%MZ)"
for i in 1 2 3; do git pull --rebase -q && git push -q && break; sleep 5; done
exit $rc
