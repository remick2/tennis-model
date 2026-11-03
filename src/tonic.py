"""Log Tennis Tonic's daily picks so we can grade them (Phase 2 side test).

Tennis Tonic's head-to-head page lists upcoming matches; the player marked with "2 sets" / "3 sets"
is their pick (winner + set count). No probabilities and no public track record, so we log picks
forward and the scorecard grades: does their pick win more often than the market price said?

Fetched honestly (plain request, identifying user agent). If the site blocks automated requests we
stop there; no workarounds. Writes data/tonic/picks.csv (de-duplicated by date + match).
"""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "tonic"
URL = "https://tennistonic.com/head-to-head/"
UA = "tennis-model/1.0 (personal research project; one request per hour)"
SETS = re.compile(r"^([23]) sets$")


def parse(text):
    """Lines: [Name, (N sets)?, 'VS', Name, (N sets)?, time/when]. Tournament header lines precede blocks."""
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    picks, tourney = [], None
    for i, l in enumerate(lines):
        if l != "VS" or i < 1:
            continue
        a_sets = SETS.match(lines[i - 1])
        a = lines[i - 2] if a_sets else lines[i - 1]
        j = i + 1
        b = lines[j] if j < len(lines) else ""
        b_sets = SETS.match(lines[j + 1]) if j + 1 < len(lines) else None
        # tournament header: the line before a block that isn't part of the previous block
        k = i - (3 if a_sets else 2)
        if k >= 1 and lines[k] in ("Hard", "Clay", "Grass", "I.hard", "Carpet"):
            tourney = lines[k - 1]
        if a_sets or b_sets:
            pick, opp, n = (a, b, a_sets.group(1)) if a_sets else (b, a, b_sets.group(1))
            picks.append({"tourney": tourney, "pick": pick, "opp": opp, "sets": int(n)})
    return pd.DataFrame(picks)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(URL, headers={"User-Agent": UA}, timeout=30)
    except requests.RequestException as e:
        print("tonic: request failed:", e); return
    status = OUT / "status.txt"
    status.write_text(f"{datetime.now(timezone.utc).isoformat()} HTTP {r.status_code} bytes {len(r.content)}\n")
    if r.status_code != 200:
        print(f"tonic: HTTP {r.status_code}; not retrying or working around it"); return
    text = BeautifulSoup(r.text, "html.parser").get_text("\n")
    d = parse(text)
    if d.empty:
        (OUT / "raw_sample.txt").write_text(text[:200_000])  # for fixing the parser
        print("tonic: page fetched but no picks parsed; saved raw_sample.txt"); return
    d.insert(0, "date", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    f = OUT / "picks.csv"
    old = pd.read_csv(f) if f.exists() else pd.DataFrame()
    allp = pd.concat([old, d]).drop_duplicates(["date", "pick", "opp"], keep="first")
    allp.to_csv(f, index=False)
    print(f"tonic: {len(d)} picks parsed, {len(allp)} logged")


if __name__ == "__main__":
    if len(sys.argv) > 1:  # parse a saved page text: python tonic.py page.txt
        print(parse(Path(sys.argv[1]).read_text()).to_string())
    else:
        main()
