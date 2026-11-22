"""Strategies from reports/Proven crypto trading strategies.md (rules fixed before testing), plus benchmarks.

All targets are decided at a daily close and executed by engine.simulate at the next open.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from engine import Panel, band_rule


def realized_vol(close: pd.DataFrame, n: int) -> pd.DataFrame:
    return np.log(close).diff().rolling(n, min_periods=n).std() * np.sqrt(365)


# ---------------------------------------------------------------- Strategy 2: BTC/ETH core
def core_targets(P: Panel, vol_target=0.35, alloc=None, weekday=6) -> pd.DataFrame:
    """Score = mean of 5 checks: close > SMA50, > SMA100, > SMA200, EMA20 > EMA20 20 days earlier,
    30-day return > 0. Weight = alloc x score x min(1, vol_target / 30-day vol). Weekly (Sunday close)."""
    alloc = alloc or {"BTC": 0.6, "ETH": 0.4}
    C = P.frame(P.c)
    out = pd.DataFrame(np.nan, index=P.dates, columns=P.coins)
    for k, a in alloc.items():
        c = C[k]
        ema = c.ewm(span=20, adjust=False).mean()
        checks = pd.concat([c > c.rolling(n, min_periods=n).mean() for n in (50, 100, 200)] +
                           [ema > ema.shift(20), c / c.shift(30) - 1 > 0], axis=1).astype(float)
        score = checks.mean(axis=1).where(c.rolling(200, min_periods=200).mean().notna())
        vol = realized_vol(c.to_frame(), 30)[k]
        out[k] = a * score * np.minimum(1.0, vol_target / vol)
    out[out.index.weekday != weekday] = np.nan
    return out


def core_overlay(P: Panel, dd_limit=-0.20, q=0.90):
    """Halve exposure when the portfolio is >20% below its peak AND BTC 30-day vol is in its top decile
    (decile measured on history up to that day only)."""
    v = realized_vol(P.frame(P.c)[["BTC"]], 30)["BTC"]
    thresh = v.expanding(min_periods=365).quantile(q).to_numpy()
    v = v.to_numpy()

    def f(t, eq_hist):
        eq = np.asarray(eq_hist)
        dd = eq[-1] / eq.max() - 1
        hot = not np.isnan(thresh[t]) and v[t] > thresh[t]
        return 0.5 if (dd < dd_limit and hot) else 1.0
    return f


CORE_RULE = band_rule(abs_band=0.10)


# ---------------------------------------------------------------- Strategy 1: Donchian ensemble
LOOKBACKS = (20, 30, 60, 90, 150, 250, 360)


def atr(h, l, c, n=20):
    pc = np.roll(c, 1); pc[0] = np.nan
    tr = np.nanmax(np.vstack([h - l, np.abs(h - pc), np.abs(l - pc)]), axis=0)
    return pd.Series(tr).ewm(alpha=1 / n, adjust=False, ignore_na=True).mean().to_numpy()


def donchian_signal(o, h, l, c, lookbacks=LOOKBACKS, atr_mult=2.5) -> np.ndarray:
    """Fraction (0..1) of sub-models long at each close. Sub-model N: enter when close > prior N-day high;
    exit when close < prior N/2-day low or close < (highest close since entry - atr_mult x ATR20)."""
    H, L, C = pd.Series(h), pd.Series(l), pd.Series(c)
    a = atr(h, l, c)
    sig = np.zeros(len(c))
    for n in lookbacks:
        hh = H.rolling(n, min_periods=n).max().shift(1).to_numpy()
        ll = L.rolling(max(n // 2, 2), min_periods=max(n // 2, 2)).min().shift(1).to_numpy()
        state, peak = 0, 0.0
        for t in range(len(c)):
            x = c[t]
            if np.isnan(x):
                sig[t] += state
                continue
            if state == 0:
                if not np.isnan(hh[t]) and x > hh[t]:
                    state, peak = 1, x
            else:
                peak = max(peak, x)
                if (not np.isnan(ll[t]) and x < ll[t]) or x < peak - atr_mult * a[t]:
                    state = 0
            sig[t] += state
    return sig / len(lookbacks)


def universe_mask(P: Panel, top=20, min_history=365, always=("BTC",)) -> np.ndarray:
    """Point-in-time membership, reselected on the first day of each month: top `top` coins by 30-day
    median dollar volume among coins with >= min_history days of data and trading that day.
    BTC is always a member (Bitstamp BTC volume understates its real liquidity)."""
    dv = P.frame(P.c * P.v).rolling(30, min_periods=20).median().to_numpy()
    T, K = P.c.shape
    mask = np.zeros((T, K), bool)
    month = None
    cur = np.zeros(K, bool)
    for t in range(T):
        m = (P.dates[t].year, P.dates[t].month)
        if m != month:
            month = m
            age = t - P.first_idx
            ok = (age >= min_history) & ~np.isnan(P.c[t]) & ~np.isnan(dv[t])
            score = np.where(ok, dv[t], -np.inf)
            cur = np.zeros(K, bool)
            for j in np.argsort(-score)[:top]:
                if np.isfinite(score[j]):
                    cur[j] = True
            for k in always:
                j = P.coins.index(k)
                cur[j] = not np.isnan(P.c[t, j])
        mask[t] = cur & (P.last_idx >= t)
    return mask


def donchian_targets(P: Panel, lookbacks=LOOKBACKS, vol_target=0.20, cap=0.20, top=20) -> pd.DataFrame:
    T, K = P.c.shape
    sig = np.column_stack([donchian_signal(P.o[:, j], P.h[:, j], P.l[:, j], P.c[:, j], lookbacks) for j in range(K)])
    vol = realized_vol(P.frame(P.c), 60).to_numpy()
    w = np.minimum(sig * vol_target / vol, cap)
    w = np.where(np.isnan(w), 0.0, w) * universe_mask(P, top)
    gross = w.sum(axis=1, keepdims=True)
    w = np.where(gross > 1, w / np.maximum(gross, 1e-12), w)
    return pd.DataFrame(w, index=P.dates, columns=P.coins)


DONCHIAN_RULE = band_rule(abs_band=0.03, rel_band=0.25, min_trade=0.01)


# ---------------------------------------------------------------- Benchmarks
def btc_hold_targets(P: Panel) -> pd.DataFrame:
    out = pd.DataFrame(np.nan, index=P.dates, columns=P.coins)
    out["BTC"] = 1.0
    return out


def btc_filter_targets(P: Panel, n=200) -> pd.DataFrame:
    c = P.frame(P.c)["BTC"]
    out = pd.DataFrame(np.nan, index=P.dates, columns=P.coins)
    out["BTC"] = (c > c.rolling(n, min_periods=n).mean()).astype(float)
    return out


def btc_volmatched_targets(P: Panel, target_vol: float) -> pd.DataFrame:
    """BTC scaled daily so its expected vol matches the strategy's realized vol (no leverage)."""
    v = realized_vol(P.frame(P.c)[["BTC"]], 30)["BTC"]
    out = pd.DataFrame(np.nan, index=P.dates, columns=P.coins)
    out["BTC"] = np.minimum(1.0, target_vol / v)
    return out


HOLD_RULE = band_rule()                       # only full entries/exits
VOLMATCH_RULE = band_rule(abs_band=0.05)
