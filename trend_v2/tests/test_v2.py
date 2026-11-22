import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from engine import Panel, band_rule, simulate, stats  # noqa: E402
from strategies import core_targets, donchian_signal, universe_mask  # noqa: E402


def panel(prices: dict, opens: dict | None = None, vols: dict | None = None, start="2024-01-01"):
    n = max(len(v) for v in prices.values())
    dates = pd.date_range(start, periods=n, freq="D", tz="UTC")
    coins = list(prices)
    pad = lambda x: np.array(list(x) + [np.nan] * (n - len(x)), float)
    c = np.column_stack([pad(prices[k]) for k in coins])
    o = np.column_stack([pad((opens or prices)[k]) for k in coins])
    v = np.column_stack([pad((vols or {}).get(k, [1.0] * len(prices[k]))) for k in coins])
    hi, lo = np.fmax(o, c), np.fmin(o, c)
    has = ~np.isnan(c)
    last = np.array([np.where(has[:, j])[0].max() for j in range(len(coins))])
    first = np.array([np.where(has[:, j])[0].min() for j in range(len(coins))])
    return Panel(dates, coins, o, hi, lo, c, v, last, first)


def targets(P, rows: dict):
    t = pd.DataFrame(np.nan, index=P.dates, columns=P.coins)
    for i, w in rows.items():
        t.iloc[i] = w
    return t


ALWAYS = band_rule(abs_band=0.0)


def test_fill_at_next_open_with_costs():
    # decide 100% BTC at day-0 close -> buy at day-1 OPEN (11), not day-0 close (10)
    P = panel({"BTC": [10, 12, 15]}, opens={"BTC": [10, 11, 14]})
    r = simulate(P, targets(P, {0: [1.0]}), cost=0.01, rule=ALWAYS)
    units = 10_000 / (11 * 1.01)
    assert r.equity.iloc[0] == pytest.approx(10_000)
    assert r.equity.iloc[1] == pytest.approx(units * 12)
    assert r.equity.iloc[2] == pytest.approx(units * 15)


def test_sell_then_cost_accounting():
    P = panel({"BTC": [10, 10, 10, 10]}, opens={"BTC": [10, 10, 20, 10]})
    r = simulate(P, targets(P, {0: [1.0], 1: [0.0]}), cost=0.01, rule=ALWAYS)
    units = 10_000 / (10 * 1.01)
    assert r.equity.iloc[-1] == pytest.approx(units * 20 * 0.99)  # sold at day-2 open 20
    ep = r.episodes.iloc[0]
    assert ep["pnl"] == pytest.approx(units * 20 * 0.99 - 10_000)


def test_delisted_coin_liquidated_at_last_close():
    # DEAD trades 3 days then disappears; we hold it -> sold at its last close (2), not left in limbo
    P = panel({"BTC": [10] * 6, "DEAD": [10, 10, 2]})
    r = simulate(P, targets(P, {0: [0.0, 1.0]}), cost=0.0, rule=ALWAYS)
    assert r.equity.iloc[-1] == pytest.approx(10_000 * 2 / 10)
    assert r.weights["DEAD"].iloc[-1] == 0


def test_no_leverage_buys_scaled_to_cash():
    P = panel({"BTC": [10] * 3, "ETH": [10] * 3})
    r = simulate(P, targets(P, {0: [0.8, 0.8]}), cost=0.0, rule=ALWAYS)
    assert r.weights.iloc[-1].sum() == pytest.approx(1.0)


def test_band_rule():
    rule = band_rule(abs_band=0.10)
    cur, tgt = np.array([0.30, 0.30, 0.0, 0.05]), np.array([0.35, 0.45, 0.2, 0.0])
    assert rule(cur, tgt).tolist() == [False, True, True, True]   # small resize skipped; entry/exit always
    rule2 = band_rule(abs_band=0.03, rel_band=0.25, min_trade=0.01)
    assert rule2(np.array([0.08, 0.20]), np.array([0.105, 0.22])).tolist() == [True, False]


def test_core_score_by_hand():
    # steadily rising BTC: all 5 checks true -> score 1; vol tiny -> scale capped at 1; weight = 60%
    n = 260
    c = list(100 * 1.002 ** np.arange(n))
    P = panel({"BTC": c, "ETH": c})
    t = core_targets(P)
    sunday = [i for i, d in enumerate(P.dates) if d.weekday() == 6 and i > 205][0]
    assert t["BTC"].iloc[sunday] == pytest.approx(0.6) and t["ETH"].iloc[sunday] == pytest.approx(0.4)
    assert t["BTC"].iloc[sunday + 1 : sunday + 7].isna().all()  # only decided weekly


def test_donchian_entry_exit_by_hand():
    # one lookback of 4: prior 4-day high = 10 -> close 11 enters; prior 2-day low exit at close 8
    c = np.array([10, 10, 10, 10, 11, 12, 12, 8, 8], float)
    s = donchian_signal(c, c, c, c, lookbacks=(4,), atr_mult=100)
    assert s.tolist() == [0, 0, 0, 0, 1, 1, 1, 0, 0]


def test_signals_and_universe_have_no_lookahead():
    rng = np.random.default_rng(0)
    c = 100 * np.exp(np.cumsum(rng.normal(0, 0.03, 500)))
    base = donchian_signal(c, c, c, c)
    for k in (100, 300, 450):
        c2 = c.copy(); c2[k + 1:] *= 5
        assert np.array_equal(donchian_signal(c2, c2, c2, c2)[: k + 1], base[: k + 1])
    P = panel({"BTC": list(c), "A": list(c), "B": list(c * 2)}, vols={"BTC": [1] * 500, "A": [1] * 500, "B": [3] * 500})
    m = universe_mask(P, top=2, min_history=100)
    P2 = panel({"BTC": list(c), "A": list(c), "B": list(c * 2)}, vols={"BTC": [1] * 500, "A": [1] * 400 + [100] * 100, "B": [3] * 500})
    assert np.array_equal(universe_mask(P2, top=2, min_history=100)[:400], m[:400])


def test_stats_sharpe_and_drawdown():
    eq = pd.Series([100.0, 110, 55, 110], index=pd.date_range("2024-01-01", periods=4, tz="UTC"))
    from engine import Result
    s = stats(Result(eq, pd.DataFrame({"BTC": [1.0] * 4}, index=eq.index), 0.0, pd.DataFrame(), 0))
    assert s["max_dd"] == pytest.approx(-0.5)
