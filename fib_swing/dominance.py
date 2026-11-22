"""BTC dominance series.

Preferred: a real BTC.D export (e.g. TradingView CRYPTOCAP:BTC.D, daily) saved as
data/BTC.D.csv with columns `time` (or `date`) and `close`.

Fallback proxy: BTC dominance moves opposite to alts' performance in BTC terms, so
    proxy = -log(equal-weight index of ALT/BTC prices)
The index averages each day's ALT/BTC log return over the alts trading that day, so coins
can join as they list. A rising proxy means BTC is outperforming (dominance rising).
The proxy uses this basket only (no market caps or stablecoins), so it is an approximation.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

REAL_BTCD = Path(__file__).resolve().parent / "data" / "BTC.D.csv"


def load_real(path: Path = REAL_BTCD) -> pd.Series | None:
    if not path.exists():
        return None
    df = pd.read_csv(path)
    tcol = "time" if "time" in df.columns else "date"
    t = df[tcol]
    idx = pd.to_datetime(t, unit="s", utc=True) if np.issubdtype(t.dtype, np.number) else pd.to_datetime(t, utc=True)
    return pd.Series(df["close"].to_numpy(float), index=idx.dt.normalize(), name="btc_d").sort_index()


def proxy(dfs: dict[str, pd.DataFrame]) -> pd.Series:
    btc = dfs["BTC"]["close"]
    rets = []
    for k, df in dfs.items():
        if k == "BTC":
            continue
        rel = (df["close"] / btc.reindex(df.index)).dropna()
        rets.append(np.log(rel).diff().rename(k))
    r = pd.concat(rets, axis=1).reindex(btc.index)
    alt_index = r.mean(axis=1, skipna=True).fillna(0).cumsum()
    first = r.notna().any(axis=1).idxmax()
    return (-alt_index).where(btc.index >= first).rename("btc_d_proxy")


def get(dfs: dict[str, pd.DataFrame]) -> tuple[pd.Series, str]:
    real = load_real()
    if real is not None:
        return real, "real BTC.D (data/BTC.D.csv)"
    return proxy(dfs), "proxy from ALT/BTC index (no BTC.D file found)"
