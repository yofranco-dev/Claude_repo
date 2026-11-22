"""Signal rule: long when the completed close is above its N-session simple moving average.

The rule sees only completed bars. Its output for bar t is the target position to hold
from the NEXT session's open. It is never used to fill at bar t's own close.
"""
from __future__ import annotations

import pandas as pd

SMA_LEN = 200


def target_positions(close: pd.Series, sma_len: int = SMA_LEN) -> pd.Series:
    """Target exposure (1 = long, 0 = cash) decided at each bar's close.

    During warm-up, before sma_len closes exist, the target is 0, so no trade is made.
    A rolling mean only looks backwards, so changing later bars cannot change earlier signals.
    """
    sma = close.rolling(sma_len, min_periods=sma_len).mean()
    return (close > sma).astype(int).where(sma.notna(), 0).rename("target")


def latest_target(close: pd.Series, sma_len: int = SMA_LEN) -> int:
    if len(close) < sma_len:
        raise ValueError(f"need at least {sma_len} completed sessions, got {len(close)}")
    return int(target_positions(close, sma_len).iloc[-1])
