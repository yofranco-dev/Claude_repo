"""Optimise on in-sample data only, then validate out-of-sample and with walk-forward.

Outputs (in reports/): REPORT.md, trades_oos.csv, walkforward.csv, equity_oos.png
"""
import itertools
from pathlib import Path

import pandas as pd

from backtest import FEE, SLIPPAGE, Params, load, run, stats

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
IS_END, OOS_START = "2022-12-31 23:59", "2023-01-01"
TARGET_WR, MIN_TRADES = 0.70, 100
OUT = Path(__file__).resolve().parent.parent / "reports"

GRID = [Params(*g) for g in itertools.product(
    [100, 200],           # trend_len
    [5, 10, 15, 25],      # rsi_entry
    [3, 5, 10],           # exit_len
    [2, 3, 5, 99],        # stop_atr (99 = effectively no stop)
    [20, 60],             # max_bars
)]


def pooled(dfs, p, start=None, end=None):
    ts = [run(dfs[s], p, start, end).assign(symbol=s) for s in dfs]
    return pd.concat([t for t in ts if not t.empty], ignore_index=True)


def optimise(dfs, end):
    """Pick params with highest expectancy among those with >=70% win rate in-sample.
    If none reach 70%, fall back to the highest in-sample win rate (flagged as fallback)."""
    results = [(p, stats(pooled(dfs, p, end=end))) for p in GRID]
    results = [(p, st) for p, st in results if st["trades"] >= MIN_TRADES]
    ok = [(p, st) for p, st in results if st["win_rate"] >= TARGET_WR]
    if ok:
        p, st = max(ok, key=lambda x: x[1]["expectancy"])
        return p, {**st, "fallback": False}
    p, st = max(results, key=lambda x: x[1]["win_rate"])
    return p, {**st, "fallback": True}


def fmt(st):
    return (f"| {st['trades']} | {st['win_rate']:.1%} | {st['avg_win']:+.2%} | {st['avg_loss']:+.2%} | "
            f"{st['profit_factor']:.2f} | {st['expectancy']:+.2%} | {st['total_return']:+.0%} | {st['max_dd']:.0%} |")


HDR = ("| Trades | Win rate | Avg win | Avg loss | Profit factor | Avg trade | Compounded | Max DD |\n"
       "|---|---|---|---|---|---|---|---|")


def main():
    OUT.mkdir(exist_ok=True)
    dfs = {s: load(s) for s in SYMBOLS}

    # 1) In-sample optimisation, untouched out-of-sample test
    p, is_st = optimise(dfs, IS_END)
    oos = pooled(dfs, p, start=OOS_START)
    oos_st = stats(oos)
    oos.sort_values("entry_time").to_csv(OUT / "trades_oos.csv", index=False)

    # 2) Anchored walk-forward: re-optimise on all data before each year, trade that year
    wf_rows, wf_trades = [], []
    for year in range(2021, 2027):
        wp, wst = optimise(dfs, f"{year - 1}-12-31 23:59")
        t = pooled(dfs, wp, start=f"{year}-01-01", end=f"{year}-12-31 23:59")
        st = stats(t)
        wf_trades.append(t)
        wf_rows.append({"year": year, **wp.__dict__, **st, "fallback": wst["fallback"]})
    wf = pd.DataFrame(wf_rows)
    wf.to_csv(OUT / "walkforward.csv", index=False)
    wf_all = stats(pd.concat(wf_trades, ignore_index=True))

    # 3) Breakdowns of the out-of-sample run
    per_coin = {s: stats(oos[oos.symbol == s]) for s in SYMBOLS}
    oos["year"] = pd.to_datetime(oos["entry_time"]).dt.year
    per_year = {y: stats(g) for y, g in oos.groupby("year")}
    bh = {s: dfs[s].loc[OOS_START:, "close"].iloc[-1] / dfs[s].loc[OOS_START:, "close"].iloc[0] - 1 for s in SYMBOLS}

    # 4) Equity chart: equal-weight portfolio, 1/5 of capital per coin
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 4.5))
        port = None
        for s in SYMBOLS:
            ts = oos[oos.symbol == s].set_index(pd.to_datetime(oos[oos.symbol == s]["exit_time"]))["ret"]
            eq = (1 + ts).cumprod()
            ax.plot(eq.index, eq.values, lw=1, alpha=0.6, label=s)
            daily = eq.resample("1D").last().ffill()
            port = daily / 5 if port is None else port.add(daily / 5, fill_value=0.2)
        ax.plot(port.index, port.values, color="black", lw=2.2, label="Equal-weight portfolio")
        ax.axhline(1, color="grey", lw=0.6)
        ax.set_title("Out-of-sample equity (2023 → today), growth of $1, net of fees & slippage")
        ax.legend(ncol=3, fontsize=8); fig.tight_layout(); fig.savefig(OUT / "equity_oos.png", dpi=130)
    except ImportError:
        pass

    passed = oos_st["win_rate"] >= TARGET_WR
    L = [
        "# Crypto RSI(2) Pullback Strategy: Backtest Report", "",
        f"**Result: out-of-sample win rate {oos_st['win_rate']:.1%} across {oos_st['trades']} trades: "
        f"{'PASSES' if passed else 'FAILS'} the 70% target.**", "",
        "## Strategy (long only, 4-hour candles)",
        f"- **Trend filter:** close above EMA({p.trend_len})",
        f"- **Entry:** RSI(2) below {p.rsi_entry:g}, bought at the next candle's open",
        f"- **Exit:** close above SMA({p.exit_len}), or stop at entry close − {p.stop_atr:g}×ATR(14), "
        f"or after {p.max_bars} candles; filled at the next open",
        f"- **Costs:** {FEE:.2%} fee and {SLIPPAGE:.2%} slippage on each side, so about {2*(FEE+SLIPPAGE):.1%} per round trip",
        f"- **Coins:** {', '.join(SYMBOLS)} (Binance spot)", "",
        "## 1. In-sample vs. out-of-sample",
        "Parameters were chosen **only** from 2019–2022 data. The 2023 to today period was never seen during tuning.", "",
        "| Period | " + HDR.split("\n")[0][2:], "|---" + HDR.split("\n")[1],
        "| In-sample 2019–2022 " + fmt(is_st), "| **Out-of-sample 2023–now** " + fmt(oos_st), "",
        "## 2. Walk-forward (re-optimised each year on all prior data only)", "",
        "| Year | Params (trend/rsi/exit/stop/bars) | Trades | Win rate | Profit factor | Avg trade |", "|---|---|---|---|---|---|",
    ]
    for r in wf_rows:
        L.append(f"| {r['year']} | {r['trend_len']}/{r['rsi_entry']:g}/{r['exit_len']}/{r['stop_atr']:g}/{r['max_bars']} | "
                 f"{r['trades']} | {r['win_rate']:.1%}{' (fallback*)' if r['fallback'] else ''} | {r['profit_factor']:.2f} | {r['expectancy']:+.2%} |")
    L += [f"| **All years** | | **{wf_all['trades']}** | **{wf_all['win_rate']:.1%}** | "
          f"**{wf_all['profit_factor']:.2f}** | **{wf_all['expectancy']:+.2%}** |", "",
          "\\* Fallback: no parameter set reached 70% on that year's training data, so the highest-win-rate set was used.", "",
          "## 3. Out-of-sample by coin", "", "| Coin " + HDR.split("\n")[0][1:] + " Buy & hold |", "|---" + HDR.split("\n")[1] + "---|"]
    for s, st in per_coin.items():
        L.append(f"| {s} " + fmt(st) + f" {bh[s]:+.0%} |")
    L += ["", "## 4. Out-of-sample by year", "", "| Year " + HDR.split("\n")[0][1:], "|---" + HDR.split("\n")[1]]
    for y, st in per_year.items():
        L.append(f"| {y} " + fmt(st))
    L += ["", "![equity](equity_oos.png)", "",
          "## Caveats",
          "- A high win rate comes from small, frequent wins and fewer, larger losses (compare avg win vs. avg loss). "
          "A single bad stretch can give back many wins.",
          "- 'Compounded' assumes 100% of that coin's allocation goes into every trade, applied to each coin's trades one after another. "
          "'Max DD' is measured on closed trades only; drawdown while a trade is open can be deeper.",
          "- The strategy is long-only, so a long bear market produces few or losing trades. Buy & hold beat it on some coins in this bull period.",
          "- Past performance does not guarantee future results. This is research code, not financial advice. Paper-trade it before risking money.",
          ]
    (OUT / "REPORT.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
