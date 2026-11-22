"""Fibonacci swing breakout with BTC-dominance rotation and three take-profit levels.

Everything is decided at a completed daily close and filled at the next open.

1. Market filter: BTC close > BTC 200-day SMA (no new trades in a crypto bear market).
2. Rotation (BTC dominance):
     * BTC can be traded whenever the market filter is on.
     * An alt can be traded only when BTC dominance is FALLING (alts gaining on BTC)
       AND the alt itself is outperforming BTC (ALT/BTC above its 50-day SMA).
   Without a real BTC.D series, dominance uses a proxy: an equal-weight index of the alts'
   prices in BTC. Index above its 50-day SMA = dominance falling. See dominance.py.
3. Entry: close breaks above the prior `lookback`-day high, and the coin is above its 200-day SMA.
4. Fibonacci levels from the prior swing (L = lowest low, H = highest high of the prior
   `lookback` days; range = H - L):
     TP1, TP2, TP3 = L + f * range for the three extension ratios (default 1.272 / 1.618 / 2.618)
     Stop = L + stop_level * range (default 0.382, the 61.8% retracement of the swing), capped
     so the stop is never more than `max_stop` below the entry.
5. Exits: sell a third at each TP. After TP1 the stop moves to breakeven; after TP2 it moves to TP1.
   If the stop and a TP fall inside the same candle, the stop is assumed first (conservative).
   Time stop after `max_days`.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Rules:
    lookback: int = 20
    trend_len: int = 200
    rel_len: int = 50
    fibs: tuple = (1.272, 1.618, 2.618)
    weights: tuple = (1 / 3, 1 / 3, 1 / 3)
    stop_level: float = 0.382        # stop at L + 0.382*range (= 61.8% retracement)
    max_stop: float = 0.25           # never risk more than 25% below entry on price
    min_tp1: float = 0.0             # skip setups whose TP1 is closer than this (e.g. 0.10 = +10%)
    use_dominance: bool = True
    max_days: int = 120


def fib_levels(low: float, high: float, fibs=(1.272, 1.618, 2.618), stop_level: float = 0.382):
    rng = high - low
    return [low + f * rng for f in fibs], low + stop_level * rng


@dataclass
class Position:
    coin: str
    entry: float
    units: float
    tps: list
    stop: float
    weights: tuple
    entry_date: pd.Timestamp
    cost: float
    equity_at_entry: float
    stage: int = 0
    days: int = 0
    units_left: float = field(init=False)
    proceeds: float = 0.0
    fills: list = field(default_factory=list)
    init_stop: float = field(init=False)

    def __post_init__(self):
        self.units_left = self.units
        self.init_stop = self.stop


def step(p: Position, o: float, h: float, l: float, c: float, max_days: int, sell) -> bool:
    """Process one session for an open position. `sell(units, price, reason)` books a fill.
    Returns True when the position is fully closed."""
    if l <= p.stop:
        sell(p.units_left, min(p.stop, o), "stop" if p.stage == 0 else f"trail{p.stage}")
        return True
    stage_before = p.stage
    while p.stage < len(p.tps) and h >= p.tps[p.stage]:
        k = p.stage
        units = p.units * p.weights[k] if k < len(p.tps) - 1 else p.units_left
        sell(units, max(p.tps[k], o), f"tp{k + 1}")
        p.stage += 1
        p.stop = p.entry if p.stage == 1 else p.tps[p.stage - 2]
    if p.stage == len(p.tps) or p.units_left <= 1e-12:
        return True
    if p.stage > stage_before and l <= p.stop:
        # A TP was hit and the candle also traded back through the moved stop. The order inside
        # the candle is unknown, so assume the worst: the rest is stopped out at the new stop.
        sell(p.units_left, p.stop, f"trail{p.stage}")
        return True
    p.days += 1
    if p.days >= max_days:
        sell(p.units_left, c, "time")
        return True
    return False


def prepare(dfs: dict[str, pd.DataFrame], rules: Rules, dominance: pd.Series | None) -> dict:
    """Precompute aligned arrays per coin on BTC's calendar."""
    btc = dfs["BTC"]
    cal = btc.index
    bc = btc["close"]
    market_ok = (bc > bc.rolling(rules.trend_len, min_periods=rules.trend_len).mean()).to_numpy()
    dom_falling = None
    if dominance is not None:
        d = dominance.reindex(cal)
        dom_falling = (d < d.rolling(rules.rel_len, min_periods=rules.rel_len).mean()).to_numpy()
    out = {"cal": cal, "coins": {}}
    for k, df in dfs.items():
        df = df.reindex(cal)
        c = df["close"]
        hh = df["high"].rolling(rules.lookback, min_periods=rules.lookback).max().shift(1)
        ll = df["low"].rolling(rules.lookback, min_periods=rules.lookback).min().shift(1)
        sig = (c > hh) & (c > c.rolling(rules.trend_len, min_periods=rules.trend_len).mean())
        sig = sig.fillna(False).to_numpy() & market_ok
        if k != "BTC" and rules.use_dominance:
            rel = c / bc
            outperf = (rel > rel.rolling(rules.rel_len, min_periods=rules.rel_len).mean()).fillna(False).to_numpy()
            sig = sig & outperf & (dom_falling if dom_falling is not None else False)
        out["coins"][k] = {
            "o": df["open"].to_numpy(), "h": df["high"].to_numpy(), "l": df["low"].to_numpy(),
            "c": c.to_numpy(), "sig": sig, "hh": hh.to_numpy(), "ll": ll.to_numpy(),
            "strength": (c / hh - 1).to_numpy(),
        }
    return out
