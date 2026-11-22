import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from portfolio import Money, run, summary  # noqa: E402
from strategy import Rules, check_exit, entry_signals  # noqa: E402

R = Rules(breakout_len=3, trend_len=3, target=0.10, stop=0.20, max_days=5)


# ---------- exit logic, hand-checked with entry = 100 (stop 80, target 110) ----------
@pytest.mark.parametrize("bar, expected", [
    ((100, 105, 95, 102), None),                 # nothing hit
    ((100, 111, 95, 108), (110, "target")),      # target hit intraday -> filled at target
    ((115, 120, 112, 118), (115, "target")),     # gap above target -> filled at the better open
    ((100, 105, 79, 90), (80, "stop")),          # stop hit intraday -> filled at stop
    ((70, 75, 65, 72), (70, "stop")),            # gap below stop -> filled at the WORSE open
    ((100, 112, 78, 105), (80, "stop")),         # both in one candle -> stop assumed first
])
def test_check_exit(bar, expected):
    got = check_exit(*bar, entry=100, days_held=0, r=R)
    if expected is None:
        assert got is None
    else:
        assert got[1] == expected[1] and got[0] == pytest.approx(expected[0])


def test_time_stop():
    assert check_exit(100, 105, 95, 103, entry=100, days_held=5, r=R) == (103, "time")
    assert check_exit(100, 105, 95, 103, entry=100, days_held=4, r=R) is None


# ---------- signals ----------
def frame(closes, opens=None, start="2024-01-01"):
    idx = pd.date_range(start, periods=len(closes), freq="D", tz="UTC")
    c = pd.Series(closes, index=idx, dtype=float)
    o = pd.Series(opens if opens is not None else closes, index=idx, dtype=float)
    return pd.DataFrame({"open": o, "high": pd.concat([o, c], axis=1).max(axis=1),
                         "low": pd.concat([o, c], axis=1).min(axis=1), "close": c, "volume": 1.0})


def test_breakout_signal_by_hand():
    # closes 10 10 10 12 11: on day 3 close 12 > prior 3-day high 10 and > SMA3 (10.67)
    df = frame([10, 10, 10, 12, 11])
    s = entry_signals(df, df["close"], R)
    assert s.tolist() == [False, False, False, True, False]


def test_signals_never_use_future_bars():
    df = frame([10, 11, 10, 12, 13, 9, 14, 15, 11, 16])
    base = entry_signals(df, df["close"], R)
    for k in range(len(df)):
        d2 = df.copy()
        d2.iloc[k + 1:, :4] *= 3
        assert entry_signals(d2, d2["close"], R).iloc[: k + 1].equals(base.iloc[: k + 1])


def test_btc_regime_filter_blocks_entries():
    df = frame([10, 10, 10, 12, 11])
    falling_btc = pd.Series([50, 40, 30, 20, 10], index=df.index, dtype=float)
    assert not entry_signals(df, falling_btc, R).any()


# ---------- portfolio + money management ----------
def test_entry_next_open_sizing_and_target_exit():
    # signal at day-3 close (12); buy at day-4 OPEN (13); target 14.3 reached on day 5
    df = frame([10, 10, 10, 12, 13, 15, 15], opens=[10, 10, 10, 11, 13, 13, 15])
    m = Money(initial=10_000, risk_per_trade=0.02, max_positions=8, fee=0, slippage=0)
    t, eq = run({"BTC": df}, R, m)
    first = t.iloc[0]
    assert first["entry_date"] == df.index[4] and first["entry"] == 13
    assert first["reason"] == "target" and first["exit"] == pytest.approx(14.3)
    # position = 2% risk / 20% stop = 10% of equity = $1,000 -> +10% = +$100 = +1% of account
    assert first["pnl"] == pytest.approx(100)
    assert first["account_impact"] == pytest.approx(0.01)


def test_stop_loss_costs_about_risk_per_trade():
    df = frame([10, 10, 10, 12, 13, 10, 10], opens=[10, 10, 10, 11, 13, 13, 10])
    df.loc[df.index[5], "low"] = 10.0   # 13 * 0.8 = 10.4 stop -> hit
    m = Money(initial=10_000, risk_per_trade=0.02, fee=0, slippage=0)
    t, _ = run({"BTC": df}, R, m)
    s = t.iloc[0]
    assert s["reason"] == "stop" and s["exit"] == pytest.approx(10.4)
    assert s["account_impact"] == pytest.approx(-0.02)


def test_max_positions_cap():
    # signal day 3 -> buy day-4 open 12.5 -> target 13.75 hit on day 5 (high 14)
    df = frame([10, 10, 10, 12, 13, 14, 14, 14], opens=[10, 10, 10, 11, 12.5, 13, 14, 14])
    coins = {"BTC": df, **{f"C{i}": df.copy() for i in range(5)}}
    t, _ = run(coins, R, Money(max_positions=2, fee=0, slippage=0))
    # all 6 coins signal on the same day; only 2 may be bought
    first_day = t[t["entry_date"] == df.index[4]]
    assert len(first_day) == 2 and (first_day["reason"] == "target").all()


def test_no_leverage():
    df = frame([10, 10, 10, 12, 13, 13.5, 13.6, 13.7], opens=[10, 10, 10, 11, 12.5, 13, 13.5, 13.6])
    coins = {"BTC": df, **{f"C{i}": df.copy() for i in range(30)}}
    _, eq = run(coins, R, Money(risk_per_trade=0.5, max_positions=50, fee=0, slippage=0))
    assert (eq > 0).all()


def test_summary_win_rate():
    t = pd.DataFrame({"return": [0.1, 0.1, -0.2], "reason": ["target", "target", "stop"],
                      "account_impact": [0.01, 0.01, -0.02]})
    eq = pd.Series([100.0, 101, 102, 100], index=pd.date_range("2024-01-01", periods=4, tz="UTC"))
    s = summary(t, eq, 100)
    assert s["win_rate"] == pytest.approx(2 / 3) and s["profit_factor"] == pytest.approx(1.0)
