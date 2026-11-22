"""Grid search on the DEVELOPMENT period only (2013-2022). The 2023+ test period is not touched here.

Selection rule (fixed before looking at results):
  TP1 >= +10% from entry, development win rate >= 70%, >= 150 trades -> highest profit factor.
"""
import itertools
import json
from dataclasses import asdict
from pathlib import Path

import pandas as pd

import dominance
from portfolio import Money, load_universe, run, summary
from strategy import Rules

DEV_END = "2022-12-31"
OUT = Path(__file__).resolve().parent / "reports"
FIBS = {"1.272/1.618/2.618": (1.272, 1.618, 2.618), "1.618/2.618/4.236": (1.618, 2.618, 4.236),
        "1.272/1.618/2.0": (1.272, 1.618, 2.0), "1.618/2.0/2.618": (1.618, 2.0, 2.618)}
WEIGHTS = {"thirds": (1 / 3, 1 / 3, 1 / 3), "50/25/25": (0.5, 0.25, 0.25)}


def grid():
    for lb, fk, sl, ms, mt, dom, wk in itertools.product(
            [20, 50, 90], FIBS, [0.0, 0.236, 0.382, 0.5], [0.2, 0.3], [0.0, 0.05, 0.10], [True, False], WEIGHTS):
        yield Rules(lookback=lb, fibs=FIBS[fk], weights=WEIGHTS[wk], stop_level=sl, max_stop=ms,
                    min_tp1=mt, use_dominance=dom)


def main():
    OUT.mkdir(exist_ok=True)
    dfs = load_universe()
    dom, _ = dominance.get(dfs)
    rows = []
    for r in grid():
        t, eq = run(dfs, r, Money(), dom, end=DEV_END)
        rows.append({**asdict(r), **summary(t, eq, Money().initial)})
    R = pd.DataFrame(rows)
    R.to_csv(OUT / "grid_dev.csv", index=False)
    ok = R[(R.min_tp1 >= 0.10) & (R.win_rate >= 0.70) & (R.trades >= 150)]
    print(f"{len(R)} configs; {len(ok)} meet the rule")
    cols = ["lookback", "fibs", "weights", "stop_level", "max_stop", "min_tp1", "use_dominance",
            "trades", "win_rate", "avg_win", "avg_loss", "profit_factor", "cagr", "max_dd", "tp1_rate", "tp2_rate", "tp3_rate"]
    pd.set_option("display.width", 250)
    print(ok.sort_values("profit_factor", ascending=False)[cols].head(10).round(3).to_string(index=False))
    if len(ok):
        best = ok.sort_values("profit_factor", ascending=False).iloc[0]
        choice = {k: (list(best[k]) if isinstance(best[k], tuple) else best[k]) for k in asdict(Rules())}
        (OUT / "chosen_rules.json").write_text(json.dumps(choice, indent=2, default=float))
        print("chosen:", choice)
    # context: what is reachable at all with TP1 >= 10%
    t10 = R[R.min_tp1 >= 0.10]
    print("\nWith TP1 >= 10%: best dev win rate =", round(t10.win_rate.max(), 3),
          "| best PF among win>=60% =", round(t10[t10.win_rate >= .6].profit_factor.max(), 3))


if __name__ == "__main__":
    main()
