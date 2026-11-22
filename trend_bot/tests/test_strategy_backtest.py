import pandas as pd
import pytest

from backtest import max_drawdown, run_backtest, summarize
from strategy import latest_target, target_positions


def test_targets_match_hand_calculation(tiny):
    assert target_positions(tiny["close"], 3).tolist() == [0, 0, 0, 1, 1, 0, 0, 1]


def test_fills_at_next_open_not_signal_close(tiny):
    r = run_backtest(tiny, sma_len=3, fee=0, slippage=0)
    buy, sell = r.fills
    # signal on day 3 (close 13) -> filled at day-4 OPEN 15, not 13 or day-4 close 14
    assert (buy["side"], buy["date"].day, buy["price"]) == ("buy", 5, 15.0)
    # exit signal on day 5 (close 9) -> filled at day-6 OPEN 9, not day-6 close 8
    assert (sell["side"], sell["date"].day, sell["price"]) == ("sell", 7, 9.0)
    assert len(r.fills) == 2  # day-7 signal has no next session, so no fill


def test_equity_and_returns_by_hand(tiny):
    r = run_backtest(tiny, sma_len=3, fee=0, slippage=0, initial_cash=10_000)
    units = 10_000 / 15
    assert r.equity.tolist() == pytest.approx([10_000, units * 14, units * 9, 6_000, 6_000])
    assert r.trades[0]["return"] == pytest.approx(-0.4)
    s = summarize(r)
    assert s["total_return"] == pytest.approx(-0.4)
    assert s["max_dd"] == pytest.approx(-0.4)  # 10000 -> 6000
    # buy & hold buys at the same first tradable open (day 3 open = 12), marked at day-7 close 12
    assert s["bh_return"] == pytest.approx(0.0)


def test_costs_and_slippage_are_applied_both_sides(tiny):
    fee, slip = 0.01, 0.02
    r = run_backtest(tiny, sma_len=3, fee=fee, slippage=slip, initial_cash=10_000)
    buy_px, sell_px = 15 * (1 + slip), 9 * (1 - slip)
    units = 10_000 / (buy_px * (1 + fee))
    assert r.fills[0]["price"] == pytest.approx(buy_px)
    assert r.fills[1]["price"] == pytest.approx(sell_px)
    assert r.equity.iloc[-1] == pytest.approx(units * sell_px * (1 - fee))


def test_no_future_data_in_signals(tiny):
    base = target_positions(tiny["close"], 3)
    for k in range(len(tiny)):
        future_changed = tiny.copy()
        future_changed.iloc[k + 1:, :4] *= 7  # wreck every later bar
        assert target_positions(future_changed["close"], 3).iloc[: k + 1].equals(base.iloc[: k + 1])


def test_no_future_data_in_fills(tiny):
    """Changing bar t's close can't change any fill at or before t."""
    base = run_backtest(tiny, sma_len=3, fee=0, slippage=0)
    changed = tiny.copy()
    changed.loc[changed.index[4], ["close", "high"]] = [1_000.0, 1_001.0]  # day-4 close (fill day of the buy)
    r = run_backtest(changed, sma_len=3, fee=0, slippage=0)
    assert r.fills[0] == base.fills[0]


def test_no_trades_during_warmup():
    idx = pd.date_range("2024-01-01", periods=6, freq="D", tz="UTC")
    rising = pd.DataFrame({"open": range(1, 7), "close": range(2, 8)}, index=idx).astype(float)
    rising["high"], rising["low"], rising["volume"] = rising["close"] + 1, rising["open"] - 0.5, 1.0
    t = target_positions(rising["close"], 4)
    assert t.iloc[:3].tolist() == [0, 0, 0]  # no SMA yet, so cash
    r = run_backtest(rising, sma_len=4, fee=0, slippage=0)
    assert r.fills[0]["date"] == idx[4]  # first SMA on day 3 -> first possible fill on day 4
    with pytest.raises(ValueError):
        run_backtest(rising, sma_len=6)
    with pytest.raises(ValueError):
        latest_target(rising["close"].iloc[:3], 4)


def test_deterministic(tiny):
    a = run_backtest(tiny, sma_len=3)
    b = run_backtest(tiny, sma_len=3)
    assert a.fills == b.fills and a.equity.equals(b.equity)


def test_max_drawdown():
    assert max_drawdown(pd.Series([100, 120, 60, 90, 130])) == pytest.approx(-0.5)
