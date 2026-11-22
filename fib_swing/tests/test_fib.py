import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from portfolio import Money, run  # noqa: E402
from strategy import Position, Rules, fib_levels, step  # noqa: E402


def test_fib_levels_by_hand():
    # swing L=100, H=200 (range 100): 1.272 -> 227.2, 1.618 -> 261.8, 2.618 -> 361.8; stop 0.382 -> 138.2
    tps, stop = fib_levels(100, 200, (1.272, 1.618, 2.618), 0.382)
    assert tps == pytest.approx([227.2, 261.8, 361.8]) and stop == pytest.approx(138.2)


def pos(entry=100.0, tps=(120.0, 140.0, 180.0), stop=80.0):
    return Position("X", entry, 3.0, list(tps), stop, (1 / 3, 1 / 3, 1 / 3), pd.Timestamp("2024-01-01", tz="UTC"), 300, 1000)


class Book:
    def __init__(self, p):
        self.p, self.fills = p, []

    def __call__(self, units, px, reason):
        units = min(units, self.p.units_left)
        self.p.units_left -= units
        self.fills.append((round(units, 6), px, reason))


def drive(p, bars, max_days=100):
    b = Book(p)
    for bar in bars:
        if step(p, *bar, max_days, b):
            return b.fills, True
    return b.fills, False


def test_three_take_profits_in_thirds():
    fills, done = drive(pos(), [(100, 121, 100.5, 120), (120, 141, 120.5, 140), (140, 181, 139, 180)])
    assert done and fills == [(1, 120, "tp1"), (1, 140, "tp2"), (1, 180, "tp3")]


def test_breakeven_after_tp1():
    p = pos()
    fills, done = drive(p, [(100, 121, 99, 120), (110, 112, 99, 100)])
    assert done and fills == [(1, 120, "tp1"), (2, 100, "trail1")]  # rest stopped at entry (breakeven)


def test_stop_moves_to_tp1_after_tp2():
    fills, done = drive(pos(), [(100, 141, 101, 139), (130, 131, 118, 119)])
    assert done and fills[:2] == [(1, 120, "tp1"), (1, 140, "tp2")] and fills[2] == (1, 120, "trail2")


def test_stop_first_when_both_in_one_candle():
    fills, done = drive(pos(), [(100, 125, 79, 100)])
    assert done and fills == [(3, 80, "stop")]


def test_gap_down_fills_at_open():
    fills, _ = drive(pos(), [(70, 72, 65, 71)])
    assert fills == [(3, 70, "stop")]


def test_tp_then_back_through_new_stop_same_candle_is_worst_case():
    # TP1 hit and the same candle trades back below entry: assume the rest is stopped at breakeven
    fills, done = drive(pos(), [(101, 121, 95, 100)])
    assert done and fills == [(1, 120, "tp1"), (2, 100, "trail1")]


def test_time_stop():
    fills, done = drive(pos(), [(100, 105, 95, 101)] * 3, max_days=3)
    assert done and fills == [(3, 101, "time")]


def test_portfolio_sizing_risks_two_percent():
    # BTC: flat at 100 (range 90-110), then breakout; stop at swing low 90 -> 10% away (entry 112)
    n = 230
    idx = pd.date_range("2020-01-01", periods=n, freq="D", tz="UTC")
    c = [100.0] * (n - 3) + [115.0, 112.0, 80.0]
    o = [100.0] * (n - 3) + [100.0, 112.0, 112.0]
    h = [110.0] * (n - 3) + [115.0, 113.0, 112.0]
    l = [90.0] * (n - 3) + [99.0, 111.0, 80.0]
    df = pd.DataFrame({"open": o, "high": h, "low": l, "close": c, "volume": 1.0}, index=idx)
    df.iloc[:200, :4] = df.iloc[:200, :4] * 0.5  # put the 200-day SMA below price
    r = Rules(lookback=20, fibs=(1.618, 2.618, 4.236), stop_level=0.0, max_stop=0.3, min_tp1=0.0, use_dominance=False)
    t, _ = run({"BTC": df}, r, Money(fee=0, slippage=0))
    tr = t.iloc[0]
    assert tr["entry"] == 112 and tr["stop"] == pytest.approx(90) and tr["exits"] == "stop"
    assert tr["account_impact"] == pytest.approx(-0.02)  # lose exactly the 2% risk budget
