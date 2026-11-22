import json

import pandas as pd
import pytest

from data import DataError, latest_completed_session, validate
from dry_run import client_order_id, load_ledger, plan

LIMIT = 0.01


def long_df(n=210, now="2024-08-01 05:00"):
    """Rising series ending on the last completed session before `now`, so the target is 1."""
    end = latest_completed_session(pd.Timestamp(now, tz="UTC"))
    idx = pd.date_range(end=end, periods=n, freq="D", name="date")
    c = pd.Series(range(100, 100 + n), index=idx, dtype=float)
    return pd.DataFrame({"open": c - 0.5, "high": c + 1, "low": c - 1, "close": c, "volume": 1.0})


NOW = pd.Timestamp("2024-08-01 05:00", tz="UTC")


@pytest.mark.parametrize("breaker, message", [
    (lambda d: pd.concat([d, d.iloc[[-1]]]), "duplicate"),
    (lambda d: d.drop(d.index[100]), "missing session"),
    (lambda d: d.assign(close=d["close"].where(d.index != d.index[5], 0.0)), "non-positive"),
    (lambda d: d.assign(low=d["low"].where(d.index != d.index[5], 1e9)), "high below low"),
    (lambda d: d.assign(close=d["close"].where(d.index != d.index[5], float("nan"))), "NaN"),
    (lambda d: d.iloc[:-1], "stale"),
])
def test_validation_blocks_bad_data(breaker, message):
    with pytest.raises(DataError, match=message):
        validate(breaker(long_df()), now=NOW)


def test_validation_accepts_good_fresh_data():
    validate(long_df(), now=NOW)


def test_latest_session_is_previous_utc_day():
    assert latest_completed_session(pd.Timestamp("2024-08-01 00:30", tz="UTC")) == pd.Timestamp("2024-07-31", tz="UTC")


def test_plan_buy_then_duplicate(tmp_path):
    df = long_df()
    ledger = load_ledger(tmp_path / "ledger.json")
    first = plan(df, ledger, "BTCUSDT", LIMIT, now=NOW)
    assert first["action"] == "buy" and first["units"] == LIMIT
    assert first["client_order_id"] == client_order_id("BTCUSDT", df.index[-1]) == "trend-BTCUSDT-20240731"
    ledger["orders"][first["client_order_id"]] = {**first, "status": "planned"}
    second = plan(df, ledger, "BTCUSDT", LIMIT, now=NOW)
    assert second["action"] == "duplicate"  # running twice can't create a second order


def test_plan_holds_when_already_at_target():
    ledger = {"position_units": LIMIT, "orders": {}}
    assert plan(long_df(), ledger, "BTCUSDT", LIMIT, now=NOW)["action"] == "hold"


def test_plan_sells_when_below_sma():
    df = long_df()
    df.loc[df.index[-1], ["open", "close", "low", "high"]] = [1.0, 1.0, 0.5, 1.5]
    r = plan(df, {"position_units": LIMIT, "orders": {}}, "BTCUSDT", LIMIT, now=NOW)
    assert r["action"] == "sell" and r["units"] == LIMIT


@pytest.mark.parametrize("ledger, now, reason", [
    ({"position_units": 5.0, "orders": {}}, NOW, "unexpected position"),
    ({"position_units": 0.0, "orders": {"x": {"status": "unknown"}}}, NOW, "status unknown"),
    ({"position_units": 0.0, "orders": {}}, NOW + pd.Timedelta(days=2), "stale"),
])
def test_plan_blocks(ledger, now, reason):
    r = plan(long_df(), ledger, "BTCUSDT", LIMIT, now=now)
    assert r["action"] == "blocked" and reason in r["reason"]


def test_pause_switch(tmp_path):
    pause = tmp_path / "PAUSE"
    pause.write_text("")
    r = plan(long_df(), {"position_units": 0.0, "orders": {}}, "BTCUSDT", LIMIT, now=NOW, pause_file=pause)
    assert r["action"] == "blocked" and "pause" in r["reason"]
