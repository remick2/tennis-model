#!/usr/bin/env bash
# One tracker cycle: results -> snapshot -> alerts -> scorecard -> commit. Used by the workflow
# (once per run while the repo is private, hourly inside a long run once it's public).
set -u
cd "$(dirname "$0")/.."
git pull --rebase -q || true                          # pick up consensus/check-in commits
find data/ratings.pkl -mmin +1440 -delete 2>/dev/null  # rebuild ratings once a day (new results)

(cd src && python -W ignore kalshi_results.py | tail -3) || echo "results update failed; using last file"
(cd src && set -o pipefail && python -W ignore snapshot.py > ../snapshot.log 2>&1)
snap=$?
tail -60 snapshot.log
grep -E '^(pinnacle:|odds-api credits left)' snapshot.log || true  # credit lines can fall outside the tail
rm -f snapshot.log
(cd src && python notify.py > ../alert.md) || echo "notify failed"
if [ -s alert.md ]; then
  gh issue create --title "Paper flag: $(date -u -d '-7 hours' '+%a %b %-d %-I:%M%p') MT" --body-file alert.md
fi
(cd src && python -W ignore scorecard.py > /dev/null) || echo "scorecard failed"

git add data/snapshots data/results_kalshi.csv
for p in data/arbs data/notified_arbs.csv data/notified.csv data/scorecard.md data/tonic; do
  [ -e "$p" ] && git add "$p"
done
git diff --cached --quiet || git commit -qm "snapshot $(date -u +%Y-%m-%dT%H:%MZ)"
# GitHub sometimes 500s for minutes at a time: back off. Anything still unpushed rides along with the
# next cycle's push (commits stay local within the run), and loop.sh pushes once more before it exits.
for i in 1 2 3 4 5 6; do git pull --rebase -q && git push -q && break; sleep $(( i * 20 )); done
exit $snap
