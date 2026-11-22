"""Swing breakout strategy with fixed take-profit and stop-loss (daily candles).

Entry signal at a completed daily close (all must be true):
  1. close > highest high of the previous 20 sessions   (breakout)
  2. close > 200-session SMA of the coin                (coin in an uptrend)
  3. BTC close > BTC 200-session SMA                    (crypto market in an uptrend)
Entry: next session's open.
Exits (checked on each session's high/low, starting with the entry session):
  * stop loss   : price <= entry x (1 - stop)     -> filled at the stop, or at the open if it gaps below
  * take profit : price >= entry x (1 + target)   -> filled at the target, or at the open if it gaps above
  * time stop   : after max_days sessions, exit at that session's close
  If the stop and the target are both inside one candle, the STOP is assumed to hit first (conservative).
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class Rules:
    breakout_len: int = 20
    trend_len: int = 200
    target: float = 0.105     # +10.5% gross take profit, about +10% net of costs
    stop: float = 0.20        # -20% stop loss
    max_days: int = 90


def entry_signals(df: pd.DataFrame, btc_close: pd.Series, r: Rules = Rules()) -> pd.Series:
    """Boolean per session, using only data up to and including that session's close."""
    c = df["close"]
    breakout = c > df["high"].rolling(r.breakout_len).max().shift(1)
    trend = c > c.rolling(r.trend_len, min_periods=r.trend_len).mean()
    btc_sma = btc_close.rolling(r.trend_len, min_periods=r.trend_len).mean()
    regime = (btc_close > btc_sma).reindex(df.index, fill_value=False)
    return (breakout & trend & regime).fillna(False).astype(bool)


def signal_strength(df: pd.DataFrame, r: Rules = Rules()) -> pd.Series:
    """How far the close is above the prior 20-day high, used to rank same-day signals."""
    return df["close"] / df["high"].rolling(r.breakout_len).max().shift(1) - 1


def check_exit(open_: float, high: float, low: float, close: float, entry: float,
               days_held: int, r: Rules = Rules()) -> tuple[float, str] | None:
    """Return (exit_price, reason) if the trade exits during this session, else None."""
    stop_px, tgt_px = entry * (1 - r.stop), entry * (1 + r.target)
    if low <= stop_px:
        return min(stop_px, open_), "stop"
    if high >= tgt_px:
        return max(tgt_px, open_), "target"
    if days_held >= r.max_days:
        return close, "time"
    return None
