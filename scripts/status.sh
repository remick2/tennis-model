#!/usr/bin/env bash
# "check" in one command: health, data freshness, the gate, the paper bot, recent alerts.
# Usage: bash scripts/status.sh   (from a clone with gh authenticated). Relay the output; don't re-derive it.
cd "$(dirname "$0")/.." || exit 1
R=remick2/tennis-model
git pull -q --rebase 2>/dev/null || true
echo "== now: $(date -u '+%Y-%m-%d %H:%M')Z ($(TZ=America/Denver date '+%a %-I:%M%p') MT)"
echo "== runs (want one in_progress or queued each)"
for wf in arbscan.yml bot.yml snapshot.yml; do
  printf '%-14s %s\n' "$wf" "$(gh api "repos/$R/actions/workflows/$wf/runs?per_page=3" -q '[.workflow_runs[]|.status+(if .conclusion then "/"+.conclusion else "" end)]|join(", ")' 2>/dev/null)"
done
echo "== data freshness (stale = a run is stuck even if it says in_progress)"
python3 - <<'PY'
import glob, pandas as pd
now = pd.Timestamp.now(tz="UTC")
def newest(pat, lim):
    fs = sorted(glob.glob(pat))[-3:]
    ts = [pd.to_datetime(pd.read_csv(f, usecols=["ts"]).ts, utc=True, format="ISO8601").max() for f in fs]
    if not ts: return "NO FILES"
    age = (now - max(ts)).total_seconds() / 60
    return f"{age:.0f} min old" + ("" if age <= lim else f"   <-- STALE (limit {lim} min)")
print("scanner scans :", newest("data/arbscan/*_scans.csv", 30))
print("bot cycles    :", newest("data/bot/*_cycles.csv", 30))
PY
echo "snapshot commit: $(git log -1 --format='%cr' -- data/snapshots)   (limit 90 min)"
echo
cat data/gate.md 2>/dev/null || echo "data/gate.md missing: run python3 src/gate.py"
echo "== paper bot"
sed -n 3,12p data/bot/summary.md 2>/dev/null
echo "== live trading"
if [ -f data/live/ENABLED ]; then echo "ENABLED file present: $(head -c 40 data/live/ENABLED | tr '\n' ' ')"; else echo "OFF (no data/live/ENABLED)"; fi
[ -f data/live/auth_check.json ] && echo "auth check done: $(python3 -c "import json;d=json.load(open('data/live/auth_check.json'));print(d['ts'], 'kalshi', d['kalshi_balance'], 'polyus', d['polyus_balance'], [(p['idx'],p['code']) for p in d['previews']])")"
echo "== issues, last 48h (skip Consensus ones: separate project)"
gh api "repos/$R/issues?state=all&per_page=15&since=$(date -u -d '-48 hours' +%Y-%m-%dT%H:%M:%SZ)" -q '.[]|"#\(.number) \(.state) \(.created_at[5:16]) \(.title)"' 2>/dev/null | grep -vi consensus
