import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def tiny():
    """8 sessions, hand-checked with SMA(3).

    day : 0   1   2   3   4   5   6   7
    open: 10  10  10  12  15  13  9   10
    close:10  10  10  13  14  9   8   12
    SMA3:  -   -  10  11 12.33 12 10.33 9.67
    target(close>SMA): 0 0 0 1 1 0 0 1   (days 0-1 are warm-up)
    => buy at day-4 open (15), sell at day-6 open (9); day-7 signal has no next session.
    """
    o = [10, 10, 10, 12, 15, 13, 9, 10]
    c = [10, 10, 10, 13, 14, 9, 8, 12]
    idx = pd.date_range("2024-01-01", periods=8, freq="D", tz="UTC", name="date")
    return pd.DataFrame({"open": o, "high": [max(a, b) + 1 for a, b in zip(o, c)],
                         "low": [min(a, b) - 1 for a, b in zip(o, c)], "close": c,
                         "volume": [100.0] * 8}, index=idx).astype(float)
