"""Dry run: after a daily close, print the order the rule wants. No broker, no API keys.

Safety checks, any of which blocks new orders (exit code 2):
  * a PAUSE file exists next to this script (pause switch)
  * data is stale, has gaps or duplicates, or has invalid prices
  * the ledger holds a position that is neither flat nor the bot's own
  * the ledger has an order whose status is unknown (e.g. a submit that timed out)

Idempotency: each session's order gets a deterministic client order ID
(trend-<SYMBOL>-<YYYYMMDD>). If the ledger already holds that ID, nothing new is created.
The ledger (ledger.json) stands in for "check broker positions and open orders".
When a real paper broker is added, look up an order by this ID before retrying a submit.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

from data import DataError, LIVE_DIR, download, load_ohlcv, save, validate
from strategy import SMA_LEN, latest_target

HERE = Path(__file__).resolve().parent
EMPTY_LEDGER = {"position_units": 0.0, "orders": {}}


def client_order_id(symbol: str, session: pd.Timestamp) -> str:
    return f"trend-{symbol}-{session:%Y%m%d}"


def load_ledger(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else json.loads(json.dumps(EMPTY_LEDGER))


def plan(df: pd.DataFrame, ledger: dict, symbol: str, max_units: float, now=None, pause_file: Path | None = None) -> dict:
    """Return {'action': 'buy'|'sell'|'hold'|'duplicate'|'blocked', ...}. Pure apart from reading pause_file."""
    if pause_file is not None and pause_file.exists():
        return {"action": "blocked", "reason": f"pause switch is on ({pause_file.name} exists)"}
    try:
        validate(df, now=now, require_fresh=True)
    except DataError as e:
        return {"action": "blocked", "reason": f"data check failed: {e}"}
    unknown = [k for k, o in ledger["orders"].items() if o.get("status") == "unknown"]
    if unknown:
        return {"action": "blocked", "reason": f"order status unknown for {unknown}; reconcile before trading"}
    pos = float(ledger["position_units"])
    if pos < 0 or pos > max_units:
        return {"action": "blocked", "reason": f"unexpected position {pos} (allowed 0 to {max_units})"}

    session = df.index[-1]
    cid = client_order_id(symbol, session)
    if cid in ledger["orders"]:
        return {"action": "duplicate", "client_order_id": cid, "order": ledger["orders"][cid]}
    target = latest_target(df["close"], SMA_LEN)
    want_units = max_units if target == 1 else 0.0
    delta = want_units - pos
    base = {"client_order_id": cid, "session": f"{session:%Y-%m-%d}", "target": target,
            "close": float(df["close"].iloc[-1]),
            "sma": float(df["close"].iloc[-SMA_LEN:].mean()), "position_units": pos}
    if abs(delta) < 1e-12:
        return {**base, "action": "hold"}
    return {**base, "action": "buy" if delta > 0 else "sell", "units": abs(delta), "when": "next session open"}


def main() -> int:
    p = argparse.ArgumentParser(description="Print intended orders (dry run)")
    p.add_argument("--symbol", default="BTCUSDT")
    p.add_argument("--max-units", type=float, default=0.01, help="position limit, in coins")
    p.add_argument("--csv", help="use this CSV instead of downloading fresh data")
    p.add_argument("--ledger", default=str(HERE / "ledger.json"))
    p.add_argument("--record", action="store_true", help="write the planned order into the ledger as 'planned'")
    a = p.parse_args()

    if a.csv:
        df = load_ohlcv(a.csv)
    else:
        df = download(a.symbol, "2017-08-17")
        save(df, LIVE_DIR / f"{a.symbol}_1d.csv")
    ledger_path = Path(a.ledger)
    ledger = load_ledger(ledger_path)
    result = plan(df, ledger, a.symbol, a.max_units, pause_file=HERE / "PAUSE")
    print(json.dumps(result, indent=2, default=str))

    if result["action"] == "blocked":
        print("BLOCKED: no order created.", file=sys.stderr)
        return 2
    if a.record and result["action"] in ("buy", "sell", "hold"):
        ledger["orders"][result["client_order_id"]] = {**result, "status": "planned"}
        ledger_path.write_text(json.dumps(ledger, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
