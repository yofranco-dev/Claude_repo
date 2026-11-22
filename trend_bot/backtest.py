"""Simulated execution for the 200-SMA trend rule.

Timeline for each session t:
  1. At the open of t, fill the order decided at the close of t-1, at open[t] +/- slippage, plus a fee.
  2. At the close of t, mark equity and compute a new target from closes up to and including t.
Nothing ever fills at the close of the bar that produced the signal.

Position sizing: long means 100% of equity in the coin (fractional units allowed); cash means 0%.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

from data import RESEARCH_DIR, load_ohlcv, validate
from strategy import SMA_LEN, target_positions


@dataclass
class Result:
    equity: pd.Series                      # equity at each session's close
    fills: list[dict] = field(default_factory=list)
    trades: list[dict] = field(default_factory=list)   # round trips
    bh_equity: pd.Series | None = None
    initial_cash: float = 10_000.0


def max_drawdown(eq: pd.Series) -> float:
    return float((eq / eq.cummax() - 1).min()) if len(eq) else 0.0


def run_backtest(df: pd.DataFrame, sma_len: int = SMA_LEN, fee: float = 0.001, slippage: float = 0.0005,
                 initial_cash: float = 10_000.0, start: str | None = None, end: str | None = None) -> Result:
    """Indicators use the full history in df. Fills and equity are recorded only inside [start, end]."""
    targets = target_positions(df["close"], sma_len)
    dates = df.index
    lo = 0 if start is None else dates.searchsorted(pd.Timestamp(start, tz="UTC"))
    hi = len(df) if end is None else dates.searchsorted(pd.Timestamp(end, tz="UTC"), side="right")
    first = max(lo, sma_len)  # first session whose open can receive a signal (bar sma_len-1 has the first SMA)
    if first >= hi:
        raise ValueError("not enough data after warm-up")

    cash, units, entry = initial_cash, 0.0, None
    fills, trades, eq = [], [], {}
    o, c = df["open"].to_numpy(), df["close"].to_numpy()
    for t in range(first, hi):
        want = targets.iloc[t - 1]           # decided at the previous close
        if want == 1 and units == 0:
            px = o[t] * (1 + slippage)
            units = cash / (px * (1 + fee))
            fills.append({"date": dates[t], "side": "buy", "price": px, "units": units, "fee": units * px * fee})
            entry = {"entry_date": dates[t], "entry_price": px, "cost": cash}
            cash = 0.0
        elif want == 0 and units > 0:
            px = o[t] * (1 - slippage)
            proceeds = units * px * (1 - fee)
            fills.append({"date": dates[t], "side": "sell", "price": px, "units": units, "fee": units * px * fee})
            trades.append({**entry, "exit_date": dates[t], "exit_price": px, "return": proceeds / entry["cost"] - 1})
            cash, units, entry = proceeds, 0.0, None
        eq[dates[t]] = cash + units * c[t]
    if entry is not None:
        trades.append({**entry, "exit_date": None, "exit_price": c[hi - 1],
                       "return": units * c[hi - 1] / entry["cost"] - 1})

    # Buy & hold from the same first session, with the same entry costs
    bh_units = initial_cash / (o[first] * (1 + slippage) * (1 + fee))
    bh = pd.Series(bh_units * c[first:hi], index=dates[first:hi])
    return Result(pd.Series(eq), fills, trades, bh, initial_cash)


def summarize(r: Result) -> dict:
    eq, bh = r.equity, r.bh_equity
    years = (eq.index[-1] - eq.index[0]).days / 365.25 or 1
    closed = [t for t in r.trades if t["exit_date"] is not None]
    tot = eq.iloc[-1] / r.initial_cash - 1
    bh_tot = bh.iloc[-1] / r.initial_cash - 1
    return {
        "start": eq.index[0], "end": eq.index[-1],
        "fills": len(r.fills), "round_trips": len(closed),
        "win_rate": sum(t["return"] > 0 for t in closed) / len(closed) if closed else float("nan"),
        "total_return": tot, "cagr": (1 + tot) ** (1 / years) - 1, "max_dd": max_drawdown(eq),
        "bh_return": bh_tot, "bh_cagr": (1 + bh_tot) ** (1 / years) - 1, "bh_max_dd": max_drawdown(bh),
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Backtest the 200-SMA trend rule")
    p.add_argument("--csv", default=str(RESEARCH_DIR / "BTCUSDT_1d.csv"))
    p.add_argument("--sma", type=int, default=SMA_LEN)
    p.add_argument("--fee", type=float, default=0.001, help="fee per side, e.g. 0.001 = 0.10%%")
    p.add_argument("--slippage", type=float, default=0.0005, help="slippage per side")
    p.add_argument("--holdout-start", default="2024-11-22",
                   help="final test period start; it is never used to choose rules")
    p.add_argument("--out", default=str(Path(__file__).resolve().parent / "reports" / "REPORT.md"))
    a = p.parse_args()

    df = load_ohlcv(a.csv)
    validate(df, require_fresh=False)
    hold = pd.Timestamp(a.holdout_start, tz="UTC")
    periods = {
        "Development": (None, (hold - pd.Timedelta(days=1)).strftime("%Y-%m-%d")),
        "Holdout (final test)": (a.holdout_start, None),
        "Full history": (None, None),
    }
    rows, results = [], {}
    for name, (s, e) in periods.items():
        r = run_backtest(df, a.sma, a.fee, a.slippage, start=s, end=e)
        results[name] = r
        rows.append((name, summarize(r)))

    L = [f"# Trend bot backtest: {Path(a.csv).stem}", "",
         f"Rule: hold 100% of equity in the coin when the daily close is above its {a.sma}-session SMA, "
         f"otherwise hold cash. Decisions are made at the close and filled at the next session's open. "
         f"Costs are {a.fee:.2%} fee and {a.slippage:.2%} slippage per side. The rule was fixed before testing "
         f"and has no tuned parameters. The holdout period starts {a.holdout_start}.", "",
         "| Period | Dates | Fills | Round trips | Win rate | Return | CAGR | Max DD | Buy & hold return | B&H CAGR | B&H max DD |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, s in rows:
        L.append(f"| {name} | {s['start']:%Y-%m-%d} → {s['end']:%Y-%m-%d} | {s['fills']} | {s['round_trips']} | "
                 f"{s['win_rate']:.0%} | {s['total_return']:+.0%} | {s['cagr']:+.1%} | {s['max_dd']:.0%} | "
                 f"{s['bh_return']:+.0%} | {s['bh_cagr']:+.1%} | {s['bh_max_dd']:.0%} |")
    L += ["", "## Round trips (full history)", "", "| Entry | Exit | Entry price | Exit price | Return |", "|---|---|---|---|---|"]
    for t in results["Full history"].trades:
        ex = f"{t['exit_date']:%Y-%m-%d}" if t["exit_date"] is not None else "open"
        L.append(f"| {t['entry_date']:%Y-%m-%d} | {ex} | {t['entry_price']:,.2f} | {t['exit_price']:,.2f} | {t['return']:+.1%} |")
    L += ["", "Win rate is shown for reference only. Trend rules usually win less than half their trades "
          "and earn their return from a few large trends. Judge this rule on drawdown versus buy & hold, not win rate.",
          "", "*Research code, not financial advice.*"]
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n")
    print("\n".join(L[:len(rows) + 6]))
    print(f"\nFull report: {out}")


if __name__ == "__main__":
    main()
