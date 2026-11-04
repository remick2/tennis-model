#!/usr/bin/env bash
# Same pattern as scripts/loop.sh (tennis), on its own schedule so the two never block each other.
# Private repo: one cycle per run. Public repo (free minutes): a cycle every hour at :40 for ~5h40m,
# then start the next run ourselves, since GitHub's cron drops many scheduled runs. The hourly cron
# in consensus.yml is only a backup starter; its concurrency group keeps one run going at a time.
set -u
cd "$(dirname "$0")/.."
start=$(date +%s)
fails=0
bash consensus/cycle.sh || fails=$((fails + 1))

private=$(gh api "repos/$GITHUB_REPOSITORY" --jq .private 2>/dev/null || echo true)
if [ "$private" != "false" ]; then
  exit $fails
fi

while :; do
  now=$(date +%s)
  next=$(( now / 3600 * 3600 + 40 * 60 ))
  [ "$next" -le "$now" ] && next=$(( next + 3600 ))
  [ $(( next - start )) -gt $(( 340 * 60 )) ] && break
  sleep $(( next - now ))
  bash consensus/cycle.sh || fails=$((fails + 1))
done

gh workflow run consensus.yml --ref main && echo "next run dispatched"
[ "$fails" -gt 0 ] && echo "$fails cycle(s) failed" && exit 1
exit 0
