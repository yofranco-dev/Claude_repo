"""Variant B: same RSI(2) pullback entry, but exit at a fixed take-profit / stop in ATR units.

Exits are checked intrabar on each candle's high/low. If both the stop and the target fall
inside one candle, the STOP is assumed to hit first (conservative). Gaps fill at the open.
Parameters are chosen on 2019-2022 only (win rate >= 70%, best expectancy), then tested 2023-now.
"""
import itertools
from pathlib import Path

import pandas as pd

from backtest import FEE, SLIPPAGE, atr, load, rsi, stats

SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
OUT = Path(__file__).resolve().parent.parent / "reports"
MAX_BARS = 30


def run(df, trend_len, rsi_entry, tp_atr, sl_atr, start=None, end=None):
    c = df["close"]
    em = c.ewm(span=trend_len, adjust=False).mean().to_numpy()
    r = rsi(c, 2).to_numpy()
    a = atr(df).to_numpy()
    o, h, l, cl = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    idx = df.index
    i = max(trend_len, 0 if start is None else idx.searchsorted(pd.Timestamp(start, tz="UTC")))
    hi = len(df) if end is None else idx.searchsorted(pd.Timestamp(end, tz="UTC"), side="right")
    trades = []
    while i < min(hi, len(df) - 1):
        if not (cl[i] > em[i] and r[i] < rsi_entry):
            i += 1
            continue
        e = o[i + 1] * (1 + SLIPPAGE)
        tgt, stp = e + tp_atr * a[i], e - sl_atr * a[i]
        x, reason, j = None, None, i + 1
        while j < len(df):
            if l[j] <= stp:
                x, reason = min(stp, o[j]), "stop"; break
            if h[j] >= tgt:
                x, reason = max(tgt, o[j]), "target"; break
            if j - (i + 1) >= MAX_BARS:
                x, reason = cl[j], "time"; break
            j += 1
        if x is None:
            break  # still open at end of data
        x *= 1 - SLIPPAGE
        trades.append({"entry_time": idx[i + 1], "exit_time": idx[j], "entry": e, "exit": x,
                       "ret": x * (1 - FEE) / (e * (1 + FEE)) - 1, "reason": reason})
        i = j + 1
    return pd.DataFrame(trades)


def pooled(dfs, p, start=None, end=None):
    ts = [run(dfs[s], *p, start=start, end=end).assign(symbol=s) for s in dfs]
    return pd.concat([t for t in ts if not t.empty], ignore_index=True)


def main():
    dfs = {s: load(s) for s in SYMBOLS}
    grid = list(itertools.product([100, 200], [5, 10, 25], [0.5, 1.0, 1.5], [2, 3, 4]))
    rows = []
    for p in grid:
        st = stats(pooled(dfs, p, end="2022-12-31 23:59"))
        rows.append((p, st))
    ok = [(p, st) for p, st in rows if st["trades"] >= 100 and st["win_rate"] >= 0.70]
    p, is_st = max(ok, key=lambda x: x[1]["expectancy"])
    oos = pooled(dfs, p, start="2023-01-01")
    oos.to_csv(OUT / "trades_oos_variant_b.csv", index=False)
    oos_st = stats(oos)

    f = lambda st: (f"| {st['trades']} | {st['win_rate']:.1%} | {st['avg_win']:+.2%} | {st['avg_loss']:+.2%} | "
                    f"{st['profit_factor']:.2f} | {st['expectancy']:+.2%} | {st['max_dd']:.0%} |")
    L = ["# Variant B: RSI(2) pullback with a fixed ATR take-profit", "",
         f"Chosen in-sample: EMA({p[0]}) trend filter, RSI(2) < {p[1]}, take-profit +{p[2]}×ATR, "
         f"stop −{p[3]}×ATR, {MAX_BARS}-candle time stop. Costs: {FEE:.2%} fee + {SLIPPAGE:.2%} slippage per side.", "",
         "| Period | Trades | Win rate | Avg win | Avg loss | Profit factor | Avg trade | Max DD |",
         "|---|---|---|---|---|---|---|---|",
         "| In-sample 2019–2022 " + f(is_st), "| **Out-of-sample 2023–now** " + f(oos_st), "",
         "| Coin | Trades | Win rate | Avg win | Avg loss | Profit factor | Avg trade | Max DD |",
         "|---|---|---|---|---|---|---|---|"]
    for s in SYMBOLS:
        L.append(f"| {s} " + f(stats(oos[oos.symbol == s])))
    L += ["", "## Every parameter set that reached 70% or more in-sample, and how it did out-of-sample",
          "Shown for transparency. Picking a row from this table using its out-of-sample column would be "
          "data snooping, so the 2023+ data would no longer be an honest test.", "",
          "| Trend | RSI< | TP×ATR | SL×ATR | IS win rate | IS avg trade | OOS trades | OOS win rate | OOS PF | OOS avg trade | OOS max DD |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for q, st in sorted(ok, key=lambda x: -x[1]["expectancy"]):
        o = stats(pooled(dfs, q, start="2023-01-01"))
        L.append(f"| {q[0]} | {q[1]} | {q[2]} | {q[3]} | {st['win_rate']:.1%} | {st['expectancy']:+.2%} | "
                 f"{o['trades']} | {o['win_rate']:.1%} | {o['profit_factor']:.2f} | {o['expectancy']:+.2%} | {o['max_dd']:.0%} |")
    L += ["", "**Takeaway:** a tight take-profit with a wide stop makes win rate easy to push past 70% (some rows exceed 85%), "
          "but each loss is several times bigger than each win. After about 0.3% round-trip costs, profit per trade is "
          "near zero or negative. Win rate alone is not a measure of a profitable strategy; check profit factor and drawdown."]
    (OUT / "VARIANT_B.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
