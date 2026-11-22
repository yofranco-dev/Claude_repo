"""Build reports/REPORT.md: development vs. final-test periods, years, coins, sensitivity and risk levels."""
from dataclasses import replace
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from portfolio import Money, load_basket, run, summary
from strategy import Rules

OUT = Path(__file__).resolve().parent / "reports"
SPLIT = "2023-01-01"


def row(name, s):
    return (f"| {name} | {s['trades']} | **{s['win_rate']:.1%}** | {s['avg_win']:+.1%} | {s['avg_loss']:+.1%} | "
            f"{s['profit_factor']:.2f} | {s['total_return']:+.0%} | {s['cagr']:+.1%} | {s['max_dd']:.0%} |")


HDR = ["| | Trades | Win rate | Avg win | Avg loss | Profit factor | Return | CAGR | Max DD |",
       "|---|---|---|---|---|---|---|---|---|"]


def main():
    OUT.mkdir(exist_ok=True)
    dfs, R, M = load_basket(), Rules(), Money()
    t, eq = run(dfs, R, M)
    t.to_csv(OUT / "trades.csv", index=False)
    dev_t, dev_eq = run(dfs, R, M, end="2022-12-31")
    test_t, test_eq = run(dfs, R, M, start=SPLIT)
    S = lambda tt, ee: summary(tt, ee, M.initial)
    full, dev, test = S(t, eq), S(dev_t, dev_eq), S(test_t, test_eq)
    btc = dfs["BTC"]["close"]

    def bh(s=None, e=None):
        x = btc.loc[s:e]
        return x.iloc[-1] / x.iloc[0] - 1, float((x / x.cummax() - 1).min())

    L = ["# Crypto swing breakout: backtest report", "",
         f"**{full['win_rate']:.1%} of {full['trades']} trades won** (2018 → 2026, {len(dfs)} coins). "
         f"Final test period 2023 → 2026: **{test['win_rate']:.1%}** of {test['trades']} trades.", "",
         "## Rules", "",
         f"- **Entry:** the coin closes above its {R.breakout_len}-day high and above its {R.trend_len}-day average, "
         f"and BTC is above its {R.trend_len}-day average. Buy at the next day's open.",
         f"- **Take profit:** +{R.target:.1%} (about +10% after costs). **Stop loss:** −{R.stop:.0%}. "
         f"**Time stop:** {R.max_days} days.",
         f"- **Money management:** each trade risks {M.risk_per_trade:.0%} of the account at its stop, "
         f"so each position is {M.risk_per_trade / R.stop:.0%} of equity. At most {M.max_positions} positions at once, no leverage.",
         f"- **Costs:** {M.fee:.2%} fee + {M.slippage:.2%} slippage per side. A stop that gaps fills at the worse open price. "
         "If the stop and target are inside the same candle, the stop is assumed to hit first.", "",
         "## Results", "", *HDR,
         row("Development 2018–2022", dev), row("**Final test 2023–2026**", test), row("Full history", full), "",
         f"Buy & hold BTC for comparison: development {bh(None, '2022-12-31')[0]:+.0%} (max DD {bh(None, '2022-12-31')[1]:.0%}), "
         f"final test {bh(SPLIT)[0]:+.0%} (max DD {bh(SPLIT)[1]:.0%}).", "",
         f"Each win adds about +{full['avg_win'] * M.risk_per_trade / R.stop:.1%} to the account and each loss "
         f"costs about {full['avg_loss'] * M.risk_per_trade / R.stop:.1%}. The worst single trade cost "
         f"{full['worst_trade_account']:.1%} of the account.", "",
         "![equity](equity.png)", "",
         "## By year", "", *HDR]
    t["year"] = pd.to_datetime(t["entry_date"]).dt.year
    for y, g in t.groupby("year"):
        e = eq.loc[str(y)]
        s = summary(g, e, e.iloc[0])
        L.append(row(str(y), s))
    L += ["", "2018 and 2022 have no trades: BTC was below its 200-day average, so the market filter kept the bot in cash through both bear markets."]
    L += ["", "## By coin", "", "| Coin | Trades | Win rate | Avg trade |", "|---|---|---|---|"]
    for k, g in t.groupby("coin"):
        L.append(f"| {k} | {len(g)} | {(g['return'] > 0).mean():.0%} | {g['return'].mean():+.1%} |")

    L += ["", "## Money management: risk per trade", "",
          "| Risk per trade | Position size | Trades | Win rate | Avg win | Avg loss | Profit factor | Return | CAGR | Max DD |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for rk in [0.01, 0.02, 0.03]:
        tt, ee = run(dfs, R, replace(M, risk_per_trade=rk))
        L.append(f"| {rk:.0%} | {rk / R.stop:.0%} of equity " + row("", summary(tt, ee, M.initial))[3:])

    L += ["", "## Sensitivity: win rate over the full history for nearby settings", "",
          "A robust setup should not depend on one exact number.", "",
          "| Target \\ Stop | −15% | −20% | −25% |", "|---|---|---|---|"]
    for tg in [0.08, 0.105, 0.15, 0.20, 0.30]:
        cells = []
        for st in [0.15, 0.20, 0.25]:
            tt, ee = run(dfs, replace(R, target=tg, stop=st), M)
            s = summary(tt, ee, M.initial)
            cells.append(f"{s['win_rate']:.0%} / PF {s['profit_factor']:.2f} / {s['cagr']:+.0%} CAGR")
        L.append(f"| +{tg:.1%} | " + " | ".join(cells) + " |")

    L += ["", "## Read before trading", "",
          "- **How it reaches 70%:** a winner only needs +10%, while a loser must fall 20%, so the stop is twice the target. "
          "Each loss wipes out about two wins. The edge is real in this test but thin: profit factor is about 1.2.",
          "- **Bigger targets lower the win rate.** At +30% or more, no setup tested reached 70%. "
          "You can have 70% winners or +30–100% winners, not both.",
          "- **The final-test period isn't fully clean.** I saw 2023–2026 results while scanning entry types, so treat it as "
          "a strong check, not a guarantee. The sensitivity table is the better evidence.",
          "- **Survivorship bias:** the basket is today's large coins. Coins that collapsed and were delisted aren't in it, "
          "so real results would likely be somewhat worse.",
          "- **Correlation:** crypto coins fall together. Up to 8 positions × 10% means 80% of the account can be in "
          "the market during a crash, so gaps through stops can make losses bigger than −2% per trade.",
          "- This is research code, not financial advice. Paper-trade it before risking money."]
    (OUT / "REPORT.md").write_text("\n".join(L) + "\n")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(eq.index, eq / M.initial, color="black", lw=2, label="Strategy (2% risk per trade)")
    b = btc.loc[eq.index[0]:]
    ax.plot(b.index, b / b.iloc[0], color="orange", lw=1, alpha=0.8, label="BTC buy & hold")
    ax.axvline(pd.Timestamp(SPLIT, tz="UTC"), color="grey", ls="--", lw=1)
    ax.text(pd.Timestamp(SPLIT, tz="UTC"), ax.get_ylim()[1] * 0.9, " final test →", color="grey")
    ax.set_yscale("log"); ax.set_title("Growth of $1, net of fees and slippage"); ax.legend()
    fig.tight_layout(); fig.savefig(OUT / "equity.png", dpi=130)
    print("\n".join(L))


if __name__ == "__main__":
    main()
