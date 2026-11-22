"""Target-weight portfolio engine for long/cash crypto strategies.

Timeline per day t:
  open t : execute trades toward the targets decided at the close of t-1 (at the open, with cost)
  close t: mark equity, then the strategy may set new targets for the next open.
Rules that make the backtest hard to fool:
  * Costs are charged on every traded dollar (cost per side includes fee + spread/slippage).
  * Sells execute before buys; buys are scaled down if cash is short (no leverage, no shorting).
  * A coin whose price history ENDS (delisted / collapsed) while held is sold at its last close.
  * A coin with a missing day keeps its last close for marking and cannot be traded that day.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
STABLES = {"USDC", "BUSD", "TUSD", "FDUSD", "DAI", "USDP", "PAXG"}


@dataclass
class Panel:
    dates: pd.DatetimeIndex
    coins: list
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    v: np.ndarray
    last_idx: np.ndarray      # last row with data for each coin
    first_idx: np.ndarray

    def frame(self, arr) -> pd.DataFrame:
        return pd.DataFrame(arr, index=self.dates, columns=self.coins)


def load_panel(folder: Path = HERE / "data", coins: list | None = None, start: str | None = None) -> Panel:
    files = sorted(folder.glob("*.csv"))
    dfs = {}
    for f in files:
        k = f.stem
        if k in STABLES or (coins is not None and k not in coins):
            continue
        df = pd.read_csv(f, parse_dates=["date"]).set_index("date")
        df.index = df.index.tz_localize("UTC") if df.index.tz is None else df.index
        dfs[k] = df
    cal = dfs["BTC"].index if start is None else dfs["BTC"].index[dfs["BTC"].index >= pd.Timestamp(start, tz="UTC")]
    names = ["BTC"] + sorted(k for k in dfs if k != "BTC")
    get = lambda col: np.column_stack([dfs[k][col].reindex(cal).to_numpy(float) for k in names])
    c = get("close")
    has = ~np.isnan(c)
    last = np.array([np.where(has[:, j])[0].max() if has[:, j].any() else -1 for j in range(len(names))])
    first = np.array([np.where(has[:, j])[0].min() if has[:, j].any() else len(cal) for j in range(len(names))])
    return Panel(cal, names, get("open"), get("high"), get("low"), c, get("volume"), last, first)


@dataclass
class Result:
    equity: pd.Series
    weights: pd.DataFrame
    turnover: float                      # one-way traded notional / average equity, per year
    episodes: pd.DataFrame               # per-coin holding episodes (flat -> held -> flat)
    trades: int
    extra: dict = field(default_factory=dict)


def simulate(P: Panel, targets: pd.DataFrame | Callable, cost: float, rule: Callable,
             start: str | None = None, end: str | None = None, initial: float = 10_000.0,
             overlay: Callable | None = None) -> Result:
    """targets: DataFrame (dates x coins) of weights decided at each close, NaN = no new decision,
    or a callable f(t) -> array. rule(current_w, target_w) -> bool array of coins to trade.
    overlay(t, equity_history) -> multiplier applied to targets (path-dependent risk overlays)."""
    T, K = P.c.shape
    tg = targets.reindex(columns=P.coins).to_numpy(float) if isinstance(targets, pd.DataFrame) else None
    lo = 0 if start is None else P.dates.searchsorted(pd.Timestamp(start, tz="UTC"))
    hi = T if end is None else P.dates.searchsorted(pd.Timestamp(end, tz="UTC"), side="right")
    last_close = np.full(K, np.nan)
    units = np.zeros(K)
    cash = initial
    eq_hist, w_hist = [], []
    traded = 0.0
    n_trades = 0
    ep_open = {}      # coin -> dict(cost_in, proceeds, start)
    episodes = []
    pending = None

    def book(j, d_units, px, day):
        nonlocal cash, traded, n_trades
        notional = abs(d_units) * px
        fee = notional * cost
        if d_units > 0:
            cash -= notional + fee
            e = ep_open.setdefault(j, {"cost_in": 0.0, "proceeds": 0.0, "start": day})
            e["cost_in"] += notional + fee
        else:
            cash += notional - fee
            ep_open[j]["proceeds"] += notional - fee
        units[j] += d_units
        traded += notional
        n_trades += 1
        if units[j] <= 1e-12 and j in ep_open:
            e = ep_open.pop(j)
            units[j] = 0.0
            episodes.append({"coin": P.coins[j], "start": e["start"], "end": day,
                             "pnl": e["proceeds"] - e["cost_in"],
                             "return": e["proceeds"] / e["cost_in"] - 1})

    for t in range(lo, hi):
        day = P.dates[t]
        o = P.o[t]
        # delisted while held -> liquidate at last close
        for j in np.where((units > 0) & (P.last_idx < t))[0]:
            book(j, -units[j], last_close[j], day)
        mark = np.where(np.isnan(o), last_close, o)
        equity = cash + np.nansum(units * mark)
        if pending is not None and equity > 0:
            cur_w = np.where(units > 0, units * mark / equity, 0.0)
            tradable = ~np.isnan(o)
            want = np.nan_to_num(pending, nan=-1)
            decide = (want >= 0) & tradable & rule(cur_w, np.where(want >= 0, want, cur_w))
            # sells first
            for j in np.where(decide & (want < cur_w))[0]:
                d = (want[j] - cur_w[j]) * equity / o[j]
                book(j, max(d, -units[j]), o[j], day)
            buys = np.where(decide & (want > cur_w))[0]
            need = sum((want[j] - cur_w[j]) * equity * (1 + cost) for j in buys)
            scale = min(1.0, cash / need) if need > 0 else 1.0
            for j in buys:
                d = (want[j] - cur_w[j]) * equity * scale / o[j]
                if d * o[j] > 1.0:
                    book(j, d, o[j], day)
        c = P.c[t]
        last_close = np.where(np.isnan(c), last_close, c)
        eq_close = cash + np.nansum(units * last_close)
        eq_hist.append(eq_close)
        w_hist.append(np.where(units > 0, units * last_close / eq_close, 0.0))
        # decide targets for tomorrow's open
        nxt = tg[t] if tg is not None else targets(t)
        if overlay is not None and nxt is not None:
            nxt = np.where(np.isnan(nxt), np.nan, nxt * overlay(t, eq_hist))
        pending = None if nxt is None or np.all(np.isnan(nxt)) else nxt

    eq = pd.Series(eq_hist, index=P.dates[lo:hi], name="equity")
    for j, e in list(ep_open.items()):  # mark open episodes at the end
        val = units[j] * last_close[j] * (1 - cost)
        episodes.append({"coin": P.coins[j], "start": e["start"], "end": None,
                         "pnl": e["proceeds"] + val - e["cost_in"], "return": (e["proceeds"] + val) / e["cost_in"] - 1})
    yrs = max(len(eq) / 365.25, 1e-9)
    return Result(eq, pd.DataFrame(w_hist, index=eq.index, columns=P.coins),
                  traded / eq.mean() / yrs, pd.DataFrame(episodes), n_trades)


# ---------------- statistics ----------------
def stats(r: Result, btc_close: pd.Series | None = None) -> dict:
    eq = r.equity
    ret = eq.pct_change().dropna()
    yrs = len(eq) / 365.25
    cagr = (eq.iloc[-1] / eq.iloc[0]) ** (1 / yrs) - 1
    vol = ret.std() * np.sqrt(365)
    dd = float((eq / eq.cummax() - 1).min())
    out = {"cagr": cagr, "vol": vol, "sharpe": ret.mean() / ret.std() * np.sqrt(365) if ret.std() > 0 else 0.0,
           "max_dd": dd, "calmar": cagr / abs(dd) if dd < 0 else np.inf, "turnover": r.turnover,
           "total_return": eq.iloc[-1] / eq.iloc[0] - 1, "exposure": r.weights.sum(axis=1).mean()}
    ep = r.episodes
    if len(ep):
        w, l = ep.pnl[ep.pnl > 0], ep.pnl[ep.pnl <= 0]
        out.update(win_rate=(ep.pnl > 0).mean(), profit_factor=w.sum() / -l.sum() if l.sum() < 0 else np.inf,
                   episodes=len(ep), avg_win=ep["return"][ep.pnl > 0].mean(), avg_loss=ep["return"][ep.pnl <= 0].mean())
        held = r.weights.gt(0).sum()
        coins_used = (held > 0).sum()
        out["round_trips_per_coin_yr"] = len(ep) / max(coins_used, 1) / yrs
    if btc_close is not None:
        b = btc_close.reindex(eq.index).pct_change().reindex(ret.index).fillna(0)
        beta = np.cov(ret, b)[0, 1] / b.var()
        out["beta"] = beta
        out["alpha_ann"] = (ret.mean() - beta * b.mean()) * 365
        resid = ret - beta * b
        out["alpha_t"] = resid.mean() / (resid.std() / np.sqrt(len(resid)))
    return out


def band_rule(abs_band: float | None = None, rel_band: float | None = None, min_trade: float = 0.0):
    """Trade a coin when |target - current| exceeds abs_band (fraction of equity) OR rel_band x current
    (either threshold triggers), ignoring changes below min_trade.
    Full entries (from 0) and full exits (to 0) always trade."""
    def rule(cur, tgt):
        d = np.abs(tgt - cur)
        entry_exit = ((cur == 0) & (tgt > 0.005)) | ((tgt == 0) & (cur > 0))
        a = np.full_like(cur, np.inf) if abs_band is None else np.full_like(cur, abs_band)
        r = np.full_like(cur, np.inf) if rel_band is None else rel_band * cur
        resize = (d > np.minimum(a, r)) & (d >= max(min_trade, 1e-9))
        return entry_exit | resize
    return rule
