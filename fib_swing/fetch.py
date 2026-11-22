"""Download BTC/USD daily candles from Bitstamp (history back to 2013; public API, no key).

Altcoin candles are reused from ../swing/data (Binance, 2017+). There is no free altcoin
history before 2017 for these coins; most of them did not exist yet.
"""
import time
from pathlib import Path

import pandas as pd
import requests

OUT = Path(__file__).resolve().parent / "data"
URL = "https://www.bitstamp.net/api/v2/ohlc/{pair}/"


def bitstamp_daily(pair: str = "btcusd", start: str = "2013-01-01", end: str = "2026-11-21") -> pd.DataFrame:
    t = int(pd.Timestamp(start, tz="UTC").timestamp())
    stop = int(pd.Timestamp(end, tz="UTC").timestamp())
    rows = []
    while t <= stop:
        r = requests.get(URL.format(pair=pair), params={"step": 86400, "limit": 1000, "start": t}, timeout=30)
        r.raise_for_status()
        batch = r.json()["data"]["ohlc"]
        if not batch:
            break
        rows += batch
        t = int(batch[-1]["timestamp"]) + 86400
        time.sleep(0.3)
    df = pd.DataFrame(rows).astype(float)
    df["date"] = pd.to_datetime(df["timestamp"], unit="s", utc=True)
    df = df.drop_duplicates("date").set_index("date")[["open", "high", "low", "close", "volume"]]
    return df[df.index <= pd.Timestamp(end, tz="UTC")]


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    df = bitstamp_daily()
    full = pd.date_range(df.index[0], df.index[-1], freq="D", tz="UTC")
    missing = full.difference(df.index)
    print(f"BTC: {len(df)} days {df.index[0]:%Y-%m-%d} -> {df.index[-1]:%Y-%m-%d}, missing days: {len(missing)}")
    out = df.copy(); out.index = out.index.strftime("%Y-%m-%d"); out.index.name = "date"
    out.to_csv(OUT / "BTCUSD_bitstamp_1d.csv")
