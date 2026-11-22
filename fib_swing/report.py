"""Run the rules chosen by optimize.py on the untouched 2023+ test period and write reports/REPORT.md."""
import json
from dataclasses import replace
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

import dominance
from portfolio import Money, load_universe, run, summary
from strategy import Rules

OUT = Path(__file__).resolve().parent / "reports"
DEV_END, TEST_START = "2022-12-31", "2023-01-01"


def chosen_rules() -> Rules:
    j = json.loads((OUT / "chosen_rules.json").read_text())
    return Rules(lookback=int(j["lookback"]), trend_len=int(j["trend_len"]), rel_len=int(j["rel_len"]),
                 fibs=tuple(j["fibs"]), weights=tuple(j["weights"]), stop_level=float(j["stop_level"]),
                 max_stop=float(j["max_stop"]), min_tp1=float(j["min_tp1"]),
                 use_dominance=bool(j["use_dominance"]), max_days=int(j["max_days"]))


HDR = ["| | Trades | Win rate | Avg win | Avg loss | Profit factor | Hit TP1 / TP2 / TP3 | Return | CAGR | Max DD |",
       "|---|---|---|---|---|---|---|---|---|---|"]


def row(name, s):
    if not s["trades"]:
        return f"| {name} | 0 | – | – | – | – | – | {s['total_return']:+.0%} | {s['cagr']:+.1%} | {s['max_dd']:.0%} |"
    return (f"| {name} | {s['trades']} | **{s['win_rate']:.1%}** | {s['avg_win']:+.1%} | {s['avg_loss']:+.1%} | "
            f"{s['profit_factor']:.2f} | {s['tp1_rate']:.0%} / {s['tp2_rate']:.0%} / {s['tp3_rate']:.0%} | "
            f"{s['total_return']:+.0%} | {s['cagr']:+.1%} | {s['max_dd']:.0%} |")


def main():
    dfs, M, R = load_universe(), Money(), chosen_rules()
    dom, dom_src = dominance.get(dfs)
    S = lambda t, e: summary(t, e, M.initial)
    t_all, eq_all = run(dfs, R, M, dom)
    t_dev, eq_dev = run(dfs, R, M, dom, end=DEV_END)
    t_test, eq_test = run(dfs, R, M, dom, start=TEST_START)
    t_all.to_csv(OUT / "trades.csv", index=False)
    dev, test, full = S(t_dev, eq_dev), S(t_test, eq_test), S(t_all, eq_all)
    btc = dfs["BTC"]["close"]
    bh = lambda s=None, e=None: (btc.loc[s:e].iloc[-1] / btc.loc[s:e].iloc[0] - 1,
                                float((btc.loc[s:e] / btc.loc[s:e].cummax() - 1).min()))
    f = R.fibs
    L = ["# Fibonacci swing breakout: backtest report", "",
         f"**Final test 2023 → 2026 (untouched until this run): {test['win_rate']:.1%} of {test['trades']} trades won.** "
         f"Development 2013 → 2022: {dev['win_rate']:.1%} of {dev['trades']} trades.", "",
         "## Rules (chosen on 2013–2022 only, by a rule fixed in advance)", "",
         "- **Market filter:** BTC above its 200-day average. No new trades in bear markets.",
         f"- **Entry:** the coin closes above its prior {R.lookback}-day high and above its 200-day average. Buy at the next open.",
         f"- **Fibonacci levels:** taken from the prior {R.lookback}-day swing, from its low L to its high H:",
         f"  - **TP1** = {f[0]} extension, **TP2** = {f[1]}, **TP3** = {f[2]}. Sell "
         f"{' / '.join(f'{w:.0%}' for w in R.weights)} of the position at each.",
         f"  - **Stop** = {'the swing low L' if R.stop_level == 0 else f'L + {R.stop_level} × range'}, "
         f"never more than {R.max_stop:.0%} below entry.",
         "  - The stop moves to breakeven after TP1, and up to TP1 after TP2.",
         f"- **Filter:** skip any setup whose TP1 is less than +{R.min_tp1:.0%} above the entry.",
         f"- **BTC dominance rotation:** {'ON' if R.use_dominance else 'OFF'}. "
         "The development data preferred it off; see the comparison below.",
         f"- **Money management:** risk {M.risk_per_trade:.0%} of the account between entry and stop, cap any position at "
         f"{M.max_position:.0%} of the account, at most {M.max_positions} positions, no leverage.",
         f"- **Costs:** {M.fee:.2%} fee + {M.slippage:.2%} slippage on every fill. Gaps fill at the worse open. "
         "If a stop and a TP are in the same candle, the stop is counted first.",
         f"- **Data:** BTC from Bitstamp since 2013-01-01; {len(dfs) - 1} alts from Binance since 2017–2020.", "",
         "## Results", "", *HDR, row("Development 2013–2022", dev), row("**Final test 2023–2026**", test),
         row("Full history", full), "",
         f"BTC buy & hold: development {bh(None, DEV_END)[0]:+,.0%} (max DD {bh(None, DEV_END)[1]:.0%}); "
         f"test {bh(TEST_START)[0]:+.0%} (max DD {bh(TEST_START)[1]:.0%}).", "",
         f"Worst single trade: {full['worst_account']:.1%} of the account. Average TP1 distance: "
         f"{t_all['tp1_pct'].mean():+.0%}; average stop distance: {t_all['stop_pct'].mean():.0%}.", "",
         "![equity](equity.png)", "",
         "## How trades ended (full history)", "", "| Exit path | Trades | Avg return |", "|---|---|---|"]
    for path, g in t_all.groupby("exits"):
        L.append(f"| {path} | {len(g)} | {g['return'].mean():+.1%} |")

    L += ["", "## BTC vs. alts (full history)", "", "| | Trades | Win rate | Avg trade |", "|---|---|---|---|"]
    for name, g in [("BTC", t_all[t_all.coin == "BTC"]), ("Alts", t_all[t_all.coin != "BTC"])]:
        L.append(f"| {name} | {len(g)} | {(g['return'] > 0).mean():.0%} | {g['return'].mean():+.1%} |")

    L += ["", f"## BTC dominance rotation: on vs. off (same other rules), dominance source: {dom_src}", "", *HDR]
    for flag in (True, False):
        r2 = replace(R, use_dominance=flag)
        L.append(row(f"Dominance {'ON' if flag else 'OFF'}, dev", S(*run(dfs, r2, M, dom, end=DEV_END))))
        L.append(row(f"Dominance {'ON' if flag else 'OFF'}, test", S(*run(dfs, r2, M, dom, start=TEST_START))))

    L += ["", "## By year", "", *HDR]
    t_all["year"] = pd.to_datetime(t_all["entry_date"]).dt.year
    for y in range(2013, 2027):
        g, e = t_all[t_all.year == y], eq_all.loc[str(y)]
        L.append(row(str(y), summary(g, e, e.iloc[0])))

    L += ["", "## Money management: risk per trade", "", *HDR]
    for rk in (0.01, 0.02, 0.03):
        L.append(row(f"{rk:.0%} risk", S(*run(dfs, R, replace(M, risk_per_trade=rk), dom))))

    L += ["", "## Read before trading", "",
          "- **Few trades:** the +10% TP1 filter and the market filter make this selective, at about 20–30 trades a year. "
          "Small samples swing a lot; one bad year can look very different from the average.",
          "- **How the win rate works:** most \"wins\" hit TP1 and then exit at breakeven on the rest. Those are small wins "
          "of about a third of the TP1 move. The large wins come from reaching TP2 and TP3.",
          "- **Wide stop:** the stop sits at the swing low, up to 30% away. Money management keeps each loss near 2% of "
          "the account, which also means positions are small.",
          "- **BTC dominance is a proxy** unless you add `data/BTC.D.csv`, a TradingView export of CRYPTOCAP:BTC.D. "
          "Then rerun `optimize.py` and `report.py`.",
          "- **Bias:** the coin list is today's survivors. I tested 1,152 setting combinations on development data, "
          "so some of the development result is luck. The 2023–26 test is the honest number.",
          "- Research code, not financial advice. Paper-trade first."]
    (OUT / "REPORT.md").write_text("\n".join(L) + "\n")

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(eq_all.index, eq_all / M.initial, color="black", lw=2, label="Strategy (2% risk per trade)")
    b = btc.loc[eq_all.index[0]:]
    ax.plot(b.index, b / b.iloc[0], color="orange", lw=1, alpha=0.8, label="BTC buy & hold")
    ax.axvline(pd.Timestamp(TEST_START, tz="UTC"), color="grey", ls="--", lw=1)
    ax.set_yscale("log"); ax.set_title("Growth of $1 (log scale), net of costs. Dashed line = start of final test")
    ax.legend(); fig.tight_layout(); fig.savefig(OUT / "equity.png", dpi=130)
    print("\n".join(L))


if __name__ == "__main__":
    main()
