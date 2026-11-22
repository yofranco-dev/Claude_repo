"""Download daily candles for a basket of large-cap coins (Binance public API)."""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "trend_bot"))
from data import download, save  # noqa: E402

COINS = ["BTC", "ETH", "BNB", "XRP", "SOL", "ADA", "DOGE", "TRX", "LINK", "AVAX",
         "DOT", "LTC", "BCH", "XLM", "ATOM", "ETC", "NEAR", "FIL", "UNI", "MATIC"]
OUT = Path(__file__).resolve().parent / "data"

if __name__ == "__main__":
    for c in COINS:
        try:
            df = download(f"{c}USDT", "2017-08-17", end="2026-11-21")
        except Exception as e:  # delisted pairs, etc.
            print(c, "skipped:", e); continue
        save(df, OUT / f"{c}USDT_1d.csv")
        print(f"{c}: {len(df)} days {df.index[0]:%Y-%m-%d} -> {df.index[-1]:%Y-%m-%d}")
