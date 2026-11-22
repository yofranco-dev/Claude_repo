"""Portfolio backtest with money management across a basket of coins.

Money management:
  * Fixed-fractional risk: each new trade risks `risk_per_trade` of current equity at its stop.
    position size = equity x risk_per_trade / stop  (2% risk / 20% stop = 10% of equity per trade)
  * At most `max_positions` open at once, and never more cash than is available (no leverage).
  * If several coins signal on the same day, the strongest breakouts are taken first.
Costs: `fee` and `slippage` per side on every fill. A stop that gaps fills at the (worse) open.
"""
from __future__ import annotations

import argparse
import glob
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from strategy import Rules, check_exit, entry_signals, signal_strength

HERE = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Money:
    initial: float = 10_000.0
    risk_per_trade: float = 0.02
    max_positions: int = 8
    fee: float = 0.001
    slippage: float = 0.0005


def load_basket(folder: Path = HERE / "data") -> dict[str, pd.DataFrame]:
    import sys
    sys.path.append(str(HERE.parent / "trend_bot"))
    from data import load_ohlcv, validate
    out = {}
    for p in sorted(glob.glob(str(folder / "*_1d.csv"))):
        df = load_ohlcv(p)
        validate(df, require_fresh=False)
        out[Path(p).stem.replace("USDT_1d", "")] = df
    return out


def run(dfs: dict[str, pd.DataFrame], rules: Rules = Rules(), money: Money = Money(),
        start: str | None = None, end: str | None = None):
    btc = dfs["BTC"]["close"]
    sig = {k: entry_signals(d, btc, rules) for k, d in dfs.items()}
    strength = {k: signal_strength(d, rules) for k, d in dfs.items()}
    days = sorted(set().union(*[d.index for d in dfs.values()]))
    days = [d for d in days if (start is None or d >= pd.Timestamp(start, tz="UTC"))
            and (end is None or d <= pd.Timestamp(end, tz="UTC"))]

    cash, open_pos, trades, curve = money.initial, {}, [], {}
    pending: list[str] = []          # coins to buy at today's open (signalled at yesterday's close)
    last_close: dict[str, float] = {}
    for day in days:
        # 1) entries at the open, sized from current equity
        equity_now = cash + sum(p["units"] * last_close.get(k, p["entry"]) for k, p in open_pos.items())
        for k in pending:
            df = dfs[k]
            if day not in df.index or k in open_pos or len(open_pos) >= money.max_positions:
                continue
            px = df.at[day, "open"] * (1 + money.slippage)
            alloc = min(equity_now * money.risk_per_trade / rules.stop, cash / (1 + money.fee))
            if alloc < 10:  # not enough cash
                continue
            units = alloc / px
            cash -= alloc * (1 + money.fee)
            open_pos[k] = {"entry": px, "units": units, "entry_date": day, "days": 0, "cost": alloc * (1 + money.fee),
                           "equity_at_entry": equity_now}
        pending = []
        # 2) exits during the session (including the entry session)
        for k in list(open_pos):
            df, p = dfs[k], open_pos[k]
            if day not in df.index:
                continue
            o, h, l, c = df.loc[day, ["open", "high", "low", "close"]]
            ex = check_exit(o, h, l, c, p["entry"], p["days"], rules)
            p["days"] += 1
            if ex:
                px = ex[0] * (1 - money.slippage)
                proceeds = p["units"] * px * (1 - money.fee)
                cash += proceeds
                trades.append({"coin": k, "entry_date": p["entry_date"], "exit_date": day, "entry": p["entry"],
                               "exit": px, "reason": ex[1], "days": p["days"],
                               "return": proceeds / p["cost"] - 1,
                               "pnl": proceeds - p["cost"],
                               "account_impact": (proceeds - p["cost"]) / p["equity_at_entry"]})
                del open_pos[k]
        # 3) mark to market, then collect today's signals for tomorrow's open
        for k, df in dfs.items():
            if day in df.index:
                last_close[k] = df.at[day, "close"]
        curve[day] = cash + sum(p["units"] * last_close[k] for k, p in open_pos.items())
        cands = [(strength[k].get(day, 0), k) for k in dfs if day in sig[k].index and sig[k].at[day] and k not in open_pos]
        pending = [k for _, k in sorted(cands, reverse=True)]
    return pd.DataFrame(trades), pd.Series(curve, name="equity")


def summary(trades: pd.DataFrame, equity: pd.Series, initial: float) -> dict:
    yrs = max((equity.index[-1] - equity.index[0]).days / 365.25, 1e-9)
    r = trades["return"] if len(trades) else pd.Series(dtype=float)
    wins, losses = r[r > 0], r[r <= 0]
    tot = equity.iloc[-1] / initial - 1
    return {"trades": len(r), "win_rate": (r > 0).mean() if len(r) else float("nan"),
            "target_hits": (trades["reason"] == "target").mean() if len(r) else float("nan"),
            "avg_win": wins.mean(), "avg_loss": losses.mean(),
            "profit_factor": wins.sum() / -losses.sum() if len(losses) and losses.sum() < 0 else float("inf"),
            "total_return": tot, "cagr": (1 + tot) ** (1 / yrs) - 1,
            "max_dd": float((equity / equity.cummax() - 1).min()),
            "worst_trade_account": trades["account_impact"].min() if len(r) else float("nan")}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--risk", type=float, default=0.02)
    ap.add_argument("--max-positions", type=int, default=8)
    a = ap.parse_args()
    dfs = load_basket()
    t, eq = run(dfs, money=Money(risk_per_trade=a.risk, max_positions=a.max_positions))
    print(summary(t, eq, 10_000))
