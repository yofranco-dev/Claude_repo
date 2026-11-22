"""Print today's entry signals with stop, target and position size. No orders are placed.

Usage: python scan_today.py --equity 10000 [--risk 0.02] [--offline]
--offline uses the CSVs in data/ instead of downloading fresh candles.
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.append(str(HERE.parent / "trend_bot"))
from data import DataError, download, validate  # noqa: E402

from fetch import COINS  # noqa: E402
from portfolio import load_basket  # noqa: E402
from strategy import Rules, entry_signals, signal_strength  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--equity", type=float, required=True)
    ap.add_argument("--risk", type=float, default=0.02)
    ap.add_argument("--offline", action="store_true")
    a = ap.parse_args()
    R = Rules()
    if a.offline:
        dfs = load_basket()
    else:
        dfs = {}
        for c in COINS:
            try:
                df = download(f"{c}USDT", "2024-01-01")
                validate(df)  # blocks on stale or broken data
                dfs[c] = df
            except (DataError, Exception) as e:
                print(f"{c}: skipped ({e})", file=sys.stderr)
    if "BTC" not in dfs:
        sys.exit("BTC data unavailable: cannot check the market filter. No signals.")
    btc = dfs["BTC"]["close"]
    rows = []
    for k, df in dfs.items():
        if entry_signals(df, btc, R).iloc[-1]:
            rows.append((signal_strength(df, R).iloc[-1], k, df["close"].iloc[-1], df.index[-1]))
    size = a.equity * a.risk / R.stop
    if not rows:
        print("No entry signals at the latest close.")
    for _, k, close, day in sorted(rows, reverse=True):
        print(f"{day:%Y-%m-%d} {k:6s} BUY at next open (~{close:,.4g}) | stop −{R.stop:.0%} | "
              f"target +{R.target:.1%} | size ${size:,.0f} (risks ${a.equity * a.risk:,.0f})")


if __name__ == "__main__":
    main()
