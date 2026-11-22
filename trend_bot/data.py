"""Daily OHLCV loading, downloading and validation.

Crypto trades 24/7, so a "session" is one UTC calendar day: the candle that opens at
00:00 UTC and closes at 23:59:59 UTC. The latest *completed* session as of a given moment
is therefore the previous UTC day.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
RESEARCH_DIR = HERE / "data" / "research"   # frozen copy, committed, used for backtests
LIVE_DIR = HERE / "data" / "live"           # fresh copy, git-ignored, used for dry runs
BINANCE = "https://data-api.binance.vision/api/v3/klines"
COLUMNS = ["open", "high", "low", "close", "volume"]


class DataError(ValueError):
    """Raised when data is unsafe to trade on. Callers must not generate orders."""


def load_ohlcv(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns:
        raise DataError(f"{path}: missing 'date' column")
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise DataError(f"{path}: missing columns {missing}")
    df["date"] = pd.to_datetime(df["date"], utc=True)
    return df.set_index("date")[COLUMNS].astype(float)


def latest_completed_session(now: pd.Timestamp | None = None) -> pd.Timestamp:
    now = pd.Timestamp.now(tz="UTC") if now is None else pd.Timestamp(now)
    if now.tzinfo is None:
        now = now.tz_localize("UTC")
    return now.normalize() - pd.Timedelta(days=1)


def validate(df: pd.DataFrame, now: pd.Timestamp | None = None, require_fresh: bool = True) -> None:
    """Raise DataError if the data has problems that should block trading."""
    if df.empty:
        raise DataError("no rows")
    if df.index.has_duplicates:
        dups = df.index[df.index.duplicated()].strftime("%Y-%m-%d").tolist()
        raise DataError(f"duplicate dates: {dups[:5]}")
    if not df.index.is_monotonic_increasing:
        raise DataError("dates are not in ascending order")
    if df[COLUMNS].isna().any().any():
        raise DataError("missing (NaN) values")
    px = df[["open", "high", "low", "close"]]
    if (px <= 0).any().any():
        raise DataError("non-positive prices")
    if (df["volume"] < 0).any():
        raise DataError("negative volume")
    if (df["high"] < df["low"]).any():
        raise DataError("high below low")
    if (df["high"] < px.max(axis=1)).any() or (df["low"] > px.min(axis=1)).any():
        raise DataError("open/close outside the high-low range")
    gaps = df.index.to_series().diff().dropna()
    if (gaps != pd.Timedelta(days=1)).any():
        first = gaps[gaps != pd.Timedelta(days=1)].index[0]
        raise DataError(f"missing session(s) before {first:%Y-%m-%d}")
    if require_fresh:
        expected = latest_completed_session(now)
        if df.index[-1] < expected:
            raise DataError(f"stale data: last session {df.index[-1]:%Y-%m-%d}, expected {expected:%Y-%m-%d}")


def download(symbol: str, start: str, end: str | None = None, now: pd.Timestamp | None = None) -> pd.DataFrame:
    """Download completed daily candles from Binance's public API (no key needed)."""
    import requests

    last_ok = latest_completed_session(now) if end is None else pd.Timestamp(end, tz="UTC")
    start_ms = int(pd.Timestamp(start, tz="UTC").timestamp() * 1000)
    rows = []
    while True:
        r = requests.get(BINANCE, params={"symbol": symbol, "interval": "1d",
                                          "startTime": start_ms, "limit": 1000}, timeout=30)
        r.raise_for_status()
        batch = r.json()
        rows += batch
        if len(batch) < 1000:
            break
        start_ms = batch[-1][0] + 1
        time.sleep(0.2)
    df = pd.DataFrame([b[:6] for b in rows], columns=["t"] + COLUMNS).astype(float)
    df["date"] = pd.to_datetime(df["t"], unit="ms", utc=True)
    df = df.set_index("date")[COLUMNS]
    return df[df.index <= last_ok]  # never keep the still-forming candle


def save(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = df.copy()
    out.index = out.index.strftime("%Y-%m-%d")
    out.index.name = "date"
    out.to_csv(path)


def main() -> None:
    p = argparse.ArgumentParser(description="Download daily candles")
    p.add_argument("--symbol", default="BTCUSDT")
    p.add_argument("--start", default="2017-08-17")
    p.add_argument("--research-end", help="freeze a research snapshot ending on this date (YYYY-MM-DD)")
    a = p.parse_args()
    if a.research_end:
        df = download(a.symbol, a.start, end=a.research_end)
        path = RESEARCH_DIR / f"{a.symbol}_1d.csv"
    else:
        df = download(a.symbol, a.start)
        path = LIVE_DIR / f"{a.symbol}_1d.csv"
    validate(df, require_fresh=not a.research_end)
    save(df, path)
    print(f"{a.symbol}: {len(df)} sessions {df.index[0]:%Y-%m-%d} -> {df.index[-1]:%Y-%m-%d} saved to {path}")


if __name__ == "__main__":
    main()
