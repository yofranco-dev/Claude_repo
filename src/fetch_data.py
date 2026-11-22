"""Download historical OHLCV candles from Binance's public market-data API."""
import argparse
import time
from pathlib import Path

import pandas as pd
import requests

BASE = "https://data-api.binance.vision/api/v3/klines"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def fetch(symbol: str, interval: str, start: str) -> pd.DataFrame:
    start_ms = int(pd.Timestamp(start, tz="UTC").timestamp() * 1000)
    rows = []
    while True:
        r = requests.get(BASE, params={"symbol": symbol, "interval": interval,
                                       "startTime": start_ms, "limit": 1000}, timeout=30)
        r.raise_for_status()
        batch = r.json()
        if not batch:
            break
        rows.extend(batch)
        start_ms = batch[-1][0] + 1
        if len(batch) < 1000:
            break
        time.sleep(0.2)
    df = pd.DataFrame(rows, columns=["open_time", "open", "high", "low", "close", "volume",
                                     "close_time", "qv", "n", "tb", "tq", "ig"])
    df = df[["open_time", "open", "high", "low", "close", "volume"]].astype(float)
    df["time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df.drop(columns="open_time").set_index("time")
    # Drop the still-forming last candle
    return df.iloc[:-1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--symbols", nargs="+", default=["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"])
    p.add_argument("--interval", default="4h")
    p.add_argument("--start", default="2019-01-01")
    a = p.parse_args()
    DATA_DIR.mkdir(exist_ok=True)
    for s in a.symbols:
        df = fetch(s, a.interval, a.start)
        out = DATA_DIR / f"{s}_{a.interval}.csv"
        df.to_csv(out)
        print(f"{s}: {len(df)} candles {df.index[0]} -> {df.index[-1]} -> {out.name}")


if __name__ == "__main__":
    main()
