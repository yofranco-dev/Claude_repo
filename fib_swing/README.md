# Fibonacci swing breakout: 3 Fibonacci take-profits, BTC-dominance rotation, data from 2013

**Result: fails the 70% target on the untouched final test.** It's kept here because the test was done properly
and the failure is informative.

| | Development 2013–2022 (tuned here) | **Final test 2023–2026** |
|---|---|---|
| Trades | 158 | 129 |
| Win rate | 79.1% | **62.0%** |
| Avg win / avg loss | +19.1% / −29.0% | +14.2% / −27.0% |
| Profit factor | 2.49 | **0.86** (losing) |
| Account return (2% risk) | +169% | −16% |

## What's in it
- **Data back to 2013:** BTC/USD daily from Bitstamp (`fetch.py`), plus 19 alts from Binance (2017+). There is no
  free alt history before 2017, and most of these coins didn't exist yet.
- **Three Fibonacci take-profits:** measured from the prior swing low to swing high, at the 1.618 / 2.618 / 4.236
  extensions. A third is sold at each. The stop moves to breakeven after TP1 and to TP1 after TP2. The initial stop
  sits at the swing low, capped at −30%.
- **BTC-dominance rotation:** alts are traded only when dominance is falling and the alt is outperforming BTC.
  With no free BTC.D history, `dominance.py` builds a proxy from an index of the alts' prices in BTC. To use the
  real series, export TradingView `CRYPTOCAP:BTC.D` (daily) to `data/BTC.D.csv`. The proxy made results *worse*
  in development, so the optimizer turned it off.
- **Money management:** 2% of the account at risk per trade, positions capped at 25%, at most 8, no leverage.

## How it was tested
`optimize.py` tried 1,152 combinations of breakout length, Fibonacci sets, stop level, stop cap, minimum TP1
distance, scale-out weights and dominance on/off, **on 2013–2022 only**. The selection rule was fixed in advance:
TP1 ≥ +10%, win rate ≥ 70%, at least 150 trades, then the highest profit factor. `report.py` then ran the winner
once on 2023–2026.

## Why it failed (and what that means)
Searching 1,152 combinations on development data finds settings that fit the past. The 79% didn't carry forward.
The simpler fixed-target system in [`../swing`](../swing/README.md) (+10% target, −20% stop) held up better. It won
70.4% in 2023–26 and **79.5% of 39 BTC trades in 2013–2016**, data it had never seen.

## Run it
```bash
python fetch.py               # BTC daily since 2013 from Bitstamp (alts come from ../swing/data)
python -m pytest -q tests     # 9 tests: Fibonacci math, 3-stage exits, trailing, gaps, same-candle worst case, 2% sizing
python optimize.py            # development-only grid search -> reports/grid_dev.csv, chosen_rules.json
python report.py              # one run on the test period -> reports/REPORT.md, trades.csv, equity.png
```
*Research code, not financial advice.*
