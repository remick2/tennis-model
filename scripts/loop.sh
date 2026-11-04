#!/usr/bin/env bash
# Private repo: one cycle per run (Actions minutes are limited).
# Public repo (minutes free): run a cycle every hour at :17 for ~5h40m, then start the next run
# ourselves, so tracking doesn't depend on GitHub's unreliable cron. The hourly cron stays as a backup
# starter; the workflow's concurrency group keeps only one run going at a time.
set -u
cd "$(dirname "$0")/.."
start=$(date +%s)
fails=0
bash scripts/cycle.sh || fails=$((fails + 1))

private=$(gh api "repos/$GITHUB_REPOSITORY" --jq .private 2>/dev/null || echo true)
if [ "$private" != "false" ]; then
  exit $fails
fi

while :; do
  now=$(date +%s)
  next=$(( now / 3600 * 3600 + 17 * 60 ))
  [ "$next" -le "$now" ] && next=$(( next + 3600 ))
  [ $(( next - start )) -gt $(( 340 * 60 )) ] && break
  sleep $(( next - now ))
  bash scripts/cycle.sh || fails=$((fails + 1))
done

gh workflow run snapshot.yml --ref main -f pinnacle=auto && echo "next run dispatched"
[ "$fails" -gt 0 ] && echo "$fails cycle(s) failed" && exit 1
exit 0
