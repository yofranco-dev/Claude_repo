"""Download a broad, survivorship-reduced coin universe (Binance USDT pairs, incl. delisted coins)
plus BTC from Bitstamp back to 2013. History up to a fixed end date, so reruns give the same data.

Binance keeps candles for delisted pairs (LUNA, FTT, BCHSV, SRM, ...). When a symbol was reused
for a different coin (LUNA after the 2022 collapse), the series is split at the gap and the later
segment is saved as <SYM>_2, so two different coins are never stitched together.
"""
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent / "trend_bot"))
sys.path.append(str(HERE.parent / "fib_swing"))
from data import download  # noqa: E402
from fetch import bitstamp_daily  # noqa: E402

END = "2026-11-21"
COINS = """ETH BNB XRP SOL ADA DOGE TRX LINK AVAX DOT LTC BCH XLM ATOM ETC NEAR FIL UNI MATIC
LUNA FTT EOS XMR BCHSV WAVES IOTA NEO XTZ ZEC DASH VET THETA ALGO ICP SAND MANA AXS CRV AAVE SHIB
APT ARB OP SUI PEPE TON ONT QTUM ICX HBAR EGLD FTM KSM COMP MKR SNX GRT CHZ ENJ BAT ZIL RUNE GALA
APE INJ FET RNDR RENDER STX IMX OMG HNT SRM ANKR LUNC""".split()
OUT = HERE / "data"


def segments(df: pd.DataFrame, max_gap_days: int = 7):
    gaps = df.index.to_series().diff() > pd.Timedelta(days=max_gap_days)
    seg_id = gaps.cumsum()
    return [g for _, g in df.groupby(seg_id)]


def save(df, name):
    out = df.copy()
    out.index = out.index.strftime("%Y-%m-%d")
    out.index.name = "date"
    out.to_csv(OUT / f"{name}.csv")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    save(bitstamp_daily(end=END), "BTC")
    print("BTC: Bitstamp 2013+")
    for c in COINS:
        try:
            df = download(f"{c}USDT", "2017-08-17", end=END)
        except Exception as e:
            print(c, "failed:", e); continue
        if df.empty:
            print(c, "no data"); continue
        for i, seg in enumerate(segments(df)):
            name = c if i == 0 else f"{c}_{i + 1}"
            if len(seg) >= 30:
                save(seg, name)
                print(f"{name}: {seg.index[0]:%Y-%m-%d} -> {seg.index[-1]:%Y-%m-%d} ({len(seg)} days)")
