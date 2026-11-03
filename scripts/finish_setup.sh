#!/usr/bin/env bash
# One-shot: push today's changes, run the tracker once, wait for it, and verify every output.
set -u
cd "$(dirname "$0")/.."
REPO=remick2/tennis-model
G() { git -c user.name="Remick (via Claude)" -c user.email="remick2@users.noreply.github.com" "$@"; }

echo "== push"
G add -A src scripts requirements.txt .github data/scorecard.md README.md 2>/dev/null
G diff --cached --quiet || G commit -qm "Setup: finish script

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01PpCzPU2SVdK4bhDSKcL3Ux"
G pull --rebase --autostash -q && G push -q && git log --oneline -1

echo "== dispatch test run"
before=$(gh run list -L 1 --repo $REPO --json databaseId --jq '.[0].databaseId')
gh api -X POST repos/$REPO/actions/workflows/snapshot.yml/dispatches -f ref=main -f 'inputs[pinnacle]=auto'
for i in $(seq 1 60); do
  id=$(gh run list -L 1 --repo $REPO --json databaseId --jq '.[0].databaseId')
  [ "$id" != "$before" ] && break; sleep 5
done
for i in $(seq 1 60); do
  st=$(gh run view "$id" --repo $REPO --json status --jq .status)
  [ "$st" = "completed" ] && break; sleep 10
done
gh run view "$id" --repo $REPO --json conclusion,jobs --jq '"conclusion: \(.conclusion)", (.jobs[0].steps[] | "  \(.conclusion)\t\(.name)")'
echo "== key log lines"
gh run view "$id" --repo $REPO --log 2>/dev/null | grep -E "pinnacle:|tonic:|credits left|Traceback|Error|flag" | sed 's/^.*Z //' | head -20

echo "== pull results"
G pull --rebase --autostash -q
ls data/tonic 2>/dev/null && cat data/tonic/status.txt 2>/dev/null
[ -f data/tonic/picks.csv ] && wc -l data/tonic/picks.csv
[ -f data/tonic/raw_sample.txt ] && head -c 1500 data/tonic/raw_sample.txt
head -12 data/scorecard.md
