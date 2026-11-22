"""Event-driven backtester for a trend-filtered RSI(2) pullback strategy on crypto.

Strategy (long only, one position per coin):
  Entry  : close > EMA(trend_len)  AND  RSI(2) < rsi_entry   -> buy at NEXT bar's open
  Exit   : close > SMA(exit_len)                             -> sell at NEXT bar's open
           or close < entry - stop_atr * ATR(14)  (stop)     -> sell at NEXT bar's open
           or max_bars held (time stop)                      -> sell at NEXT bar's open
Signals use only closed candles; fills happen on the following open (no look-ahead).
Costs: fee + slippage charged on BOTH sides of every trade.
"""
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FEE = 0.001        # 0.10% per side (Binance spot taker)
SLIPPAGE = 0.0005  # 0.05% per side


@dataclass(frozen=True)
class Params:
    trend_len: int = 200
    rsi_entry: float = 10.0
    exit_len: int = 5
    stop_atr: float = 3.0
    max_bars: int = 30


def load(symbol: str, interval: str = "4h") -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / f"{symbol}_{interval}.csv", index_col="time", parse_dates=True)


def rsi(close: pd.Series, n: int) -> pd.Series:
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    pc = df["close"].shift()
    tr = pd.concat([df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


def run(df: pd.DataFrame, p: Params, start=None, end=None) -> pd.DataFrame:
    """Return a DataFrame of closed trades. Indicators are computed on full history
    (warm-up), but only entries whose signal bar is in [start, end] are taken."""
    c = df["close"]
    ema = c.ewm(span=p.trend_len, adjust=False).mean()
    r2 = rsi(c, 2)
    sma = c.rolling(p.exit_len).mean()
    a = atr(df)
    o = df["open"].to_numpy()
    cl, em, rr, sm, at = c.to_numpy(), ema.to_numpy(), r2.to_numpy(), sma.to_numpy(), a.to_numpy()
    idx = df.index
    lo = 0 if start is None else idx.searchsorted(pd.Timestamp(start, tz="UTC"))
    hi = len(df) if end is None else idx.searchsorted(pd.Timestamp(end, tz="UTC"), side="right")
    lo = max(lo, p.trend_len)

    trades, in_pos, entry_i, entry_px, stop = [], False, 0, 0.0, 0.0
    for i in range(lo, len(df) - 1):
        if not in_pos:
            if i >= hi:
                break
            if cl[i] > em[i] and rr[i] < p.rsi_entry:
                in_pos, entry_i = True, i + 1
                entry_px = o[i + 1] * (1 + SLIPPAGE)
                stop = cl[i] - p.stop_atr * at[i]
        else:
            reason = None
            if cl[i] < stop:
                reason = "stop"
            elif cl[i] > sm[i]:
                reason = "target"
            elif i + 1 - entry_i >= p.max_bars:
                reason = "time"
            if reason:
                exit_px = o[i + 1] * (1 - SLIPPAGE)
                ret = (exit_px * (1 - FEE)) / (entry_px * (1 + FEE)) - 1
                trades.append({"entry_time": idx[entry_i], "exit_time": idx[i + 1],
                               "entry": entry_px, "exit": exit_px, "ret": ret,
                               "bars": i + 1 - entry_i, "reason": reason})
                in_pos = False
    return pd.DataFrame(trades)


def stats(t: pd.DataFrame) -> dict:
    if t.empty:
        return {"trades": 0, "win_rate": 0.0, "avg_win": 0.0, "avg_loss": 0.0,
                "profit_factor": 0.0, "expectancy": 0.0, "total_return": 0.0, "max_dd": 0.0}
    r = t["ret"]
    wins, losses = r[r > 0], r[r <= 0]
    eq = (1 + r).cumprod()
    dd = (eq / eq.cummax() - 1).min()
    gl = -losses.sum()
    return {"trades": len(r), "win_rate": (r > 0).mean(),
            "avg_win": wins.mean() if len(wins) else 0.0,
            "avg_loss": losses.mean() if len(losses) else 0.0,
            "profit_factor": wins.sum() / gl if gl > 0 else np.inf,
            "expectancy": r.mean(), "total_return": eq.iloc[-1] - 1, "max_dd": dd}
