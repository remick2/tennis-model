#!/usr/bin/env bash
# Private repo: one cycle per run (Actions minutes are limited).
# Public repo (minutes free): run a cycle every hour at :17 for ~5h40m, then hand off to a new run.
# Handoff is defensive because GitHub's API sometimes returns 500s for minutes at a time:
#   - the next run is requested an hour early (it waits in the concurrency queue until this one ends),
#     retrying with backoff; a pending cron run or the watchdog workflow also fills the gap if all fail
#   - unpushed commits get one last push (with backoff) before exiting
set -u
cd "$(dirname "$0")/.."
start=$(date +%s)
fails=0
handed_off=0
bash scripts/cycle.sh || fails=$((fails + 1))

private=$(gh api "repos/$GITHUB_REPOSITORY" --jq .private 2>/dev/null || echo true)
if [ "$private" != "false" ]; then
  exit $fails
fi

dispatch_next() {
  for i in 1 2 3 4 5 6 7 8; do
    if gh workflow run snapshot.yml --ref main -f pinnacle=auto; then
      echo "next run requested (attempt $i)"; return 0
    fi
    sleep $(( i * 30 ))
  done
  echo "could not request the next run; watchdog/cron will restart tracking"; return 1
}

while :; do
  now=$(date +%s)
  next=$(( now / 3600 * 3600 + 17 * 60 ))
  [ "$next" -le "$now" ] && next=$(( next + 3600 ))
  [ $(( next - start )) -gt $(( 340 * 60 )) ] && break
  # last cycle of this run: queue the successor now, so a GitHub hiccup at the very end can't break the chain
  if [ "$handed_off" -eq 0 ] && [ $(( next + 3600 - start )) -gt $(( 340 * 60 )) ]; then
    dispatch_next && handed_off=1
  fi
  sleep $(( $(date +%s) < next ? next - $(date +%s) : 0 ))
  bash scripts/cycle.sh || fails=$((fails + 1))
done

[ "$handed_off" -eq 0 ] && dispatch_next
for i in 1 2 3 4 5; do git pull --rebase -q && git push -q && break; sleep $(( i * 20 )); done
[ "$fails" -gt 0 ] && echo "$fails cycle(s) failed" && exit 1
exit 0
