"""Portfolio backtest with money management and three-stage Fibonacci exits.

Money management:
  * Risk `risk_per_trade` of current equity between entry and the initial stop:
        position value = equity x risk / stop_distance   (capped at `max_position` of equity)
  * At most `max_positions` open; never spend more cash than available (no leverage).
  * Same-day signals are ranked by breakout strength.
Costs: fee + slippage on every fill (each partial exit is its own fill).
"""
from __future__ import annotations

import glob
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from strategy import Position, Rules, fib_levels, prepare, step

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent / "trend_bot"))


@dataclass(frozen=True)
class Money:
    initial: float = 10_000.0
    risk_per_trade: float = 0.02
    max_position: float = 0.25
    max_positions: int = 8
    fee: float = 0.001
    slippage: float = 0.0005


def load_universe() -> dict[str, pd.DataFrame]:
    from data import load_ohlcv, validate
    dfs = {"BTC": load_ohlcv(HERE / "data" / "BTCUSD_bitstamp_1d.csv")}
    for p in sorted(glob.glob(str(HERE.parent / "swing" / "data" / "*USDT_1d.csv"))):
        k = Path(p).stem.replace("USDT_1d", "")
        if k != "BTC":
            dfs[k] = load_ohlcv(p)
    for df in dfs.values():
        validate(df, require_fresh=False)
    return dfs


def run(dfs, rules: Rules = Rules(), money: Money = Money(), dominance: pd.Series | None = None,
        start: str | None = None, end: str | None = None):
    P = prepare(dfs, rules, dominance)
    cal, coins = P["cal"], P["coins"]
    lo = 0 if start is None else cal.searchsorted(pd.Timestamp(start, tz="UTC"))
    hi = len(cal) if end is None else cal.searchsorted(pd.Timestamp(end, tz="UTC"), side="right")
    cash, open_pos, trades, curve, pending = money.initial, {}, [], {}, []
    last = {}
    cost_in, cost_out = (1 + money.slippage) * (1 + money.fee), (1 - money.slippage) * (1 - money.fee)

    for t in range(lo, hi):
        day = cal[t]
        equity = cash + sum(p.units_left * last.get(k, p.entry) for k, p in open_pos.items())
        # entries at the open
        for k in pending:
            a = coins[k]
            o = a["o"][t]
            if k in open_pos or len(open_pos) >= money.max_positions or np.isnan(o):
                continue
            entry = o * (1 + money.slippage)
            tps, stop = fib_levels(a["ll"][t - 1], a["hh"][t - 1], rules.fibs, rules.stop_level)
            stop = max(stop, entry * (1 - rules.max_stop))
            if stop >= entry or tps[0] <= entry or tps[0] / entry - 1 < rules.min_tp1:
                continue  # gapped past the setup, or TP1 too close
            dist = 1 - stop / entry
            value = min(equity * money.risk_per_trade / dist, equity * money.max_position, cash / (1 + money.fee))
            if value < 10:
                continue
            cash -= value * (1 + money.fee)
            open_pos[k] = Position(k, entry, value / entry, tps, stop, rules.weights, day,
                                   value * (1 + money.fee), equity)
        pending = []
        # exits
        for k in list(open_pos):
            a, p = coins[k], open_pos[k]
            o, h, l, c = a["o"][t], a["h"][t], a["l"][t], a["c"][t]
            if np.isnan(o):
                continue

            def sell(units, px, reason, p=p):
                nonlocal cash
                units = min(units, p.units_left)
                got = units * px * cost_out
                cash += got
                p.proceeds += got
                p.units_left -= units
                p.fills.append(reason)

            if step(p, o, h, l, c, rules.max_days, sell):
                trades.append({"coin": k, "entry_date": p.entry_date, "exit_date": day, "entry": p.entry,
                               "tp1": p.tps[0], "tp2": p.tps[1], "tp3": p.tps[2], "stop": p.init_stop, "stop_pct": 1 - p.init_stop / p.entry,
                               "tp1_pct": p.tps[0] / p.entry - 1, "exits": "+".join(p.fills),
                               "stage": p.stage, "return": p.proceeds / p.cost - 1,
                               "pnl": p.proceeds - p.cost,
                               "account_impact": (p.proceeds - p.cost) / p.equity_at_entry})
                del open_pos[k]
        for k, a in coins.items():
            if not np.isnan(a["c"][t]):
                last[k] = a["c"][t]
        curve[day] = cash + sum(p.units_left * last[k] for k, p in open_pos.items())
        cands = [(coins[k]["strength"][t], k) for k in coins if coins[k]["sig"][t] and k not in open_pos]
        pending = [k for _, k in sorted(cands, reverse=True)]
    return pd.DataFrame(trades), pd.Series(curve, name="equity")


def summary(trades: pd.DataFrame, equity: pd.Series, initial: float) -> dict:
    yrs = max((equity.index[-1] - equity.index[0]).days / 365.25, 1e-9)
    tot = equity.iloc[-1] / initial - 1
    base = {"total_return": tot, "cagr": (1 + tot) ** (1 / yrs) - 1,
            "max_dd": float((equity / equity.cummax() - 1).min())}
    if trades.empty:
        return {**base, "trades": 0, "win_rate": np.nan, "avg_win": np.nan, "avg_loss": np.nan,
                "profit_factor": np.nan, "tp1_rate": np.nan, "tp2_rate": np.nan, "tp3_rate": np.nan,
                "expectancy": np.nan, "worst_account": np.nan}
    r = trades["return"]
    w, ls = r[r > 0], r[r <= 0]
    return {**base, "trades": len(r), "win_rate": (r > 0).mean(), "avg_win": w.mean(), "avg_loss": ls.mean(),
            "profit_factor": w.sum() / -ls.sum() if ls.sum() < 0 else np.inf,
            "tp1_rate": (trades["stage"] >= 1).mean(), "tp2_rate": (trades["stage"] >= 2).mean(),
            "tp3_rate": (trades["stage"] >= 3).mean(), "expectancy": r.mean(),
            "worst_account": trades["account_impact"].min()}
