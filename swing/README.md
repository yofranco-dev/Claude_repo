# Crypto swing breakout: 70% win rate, +10% per win, with stop loss and money management

| | Development 2018–2022 | **Final test 2023–2026** | Full history |
|---|---|---|---|
| Trades | 450 | 365 | 815 |
| **Win rate** | **71.3%** | **70.4%** | **70.9%** |
| Avg win / avg loss (per trade) | +10.2% / −20.2% | +10.2% / −20.1% | +10.2% / −20.2% |
| Profit factor | 1.26 | 1.20 | 1.23 |
| Account return (2% risk per trade) | +74% | +33% | +130% (+9.4%/yr) |
| Max account drawdown | −22% | −34% | −34% |

**Extra check on data it had never seen:** BTC alone, 2013–2016 (Bitstamp data, added later): **79.5% of 39 trades won**, profit factor 1.96.

Full details, by year, by coin, risk levels and sensitivity: [reports/REPORT.md](reports/REPORT.md).

## Rules
- **Universe:** 20 large-cap coins, Binance spot, daily candles.
- **Entry:** the coin closes above its 20-day high **and** above its 200-day average, **and** BTC is above its
  200-day average. Buy at the next day's open.
- **Take profit:** +10.5%, about +10% after costs. **Stop loss:** −20%. **Time stop:** 90 days.
- **Money management:** risk 2% of the account per trade, so each position is 10% of equity. At most 8 open
  positions, no leverage. A win adds about +1% to the account and a loss costs about −2%.
- **Costs:** 0.10% fee + 0.05% slippage per side. Gaps fill at the worse open price. If the stop and target are
  inside the same candle, the stop is counted first.

## What you should know
- **70% winners and +30–100% winners don't come together.** The sensitivity table shows win rate falling as
  the target rises: about 60% at +20% and about 50% at +30%. The 70% comes from a target that's closer than the stop.
- **It earns less than holding BTC** (+130% vs about +420% since 2018) but avoided the −77% to −83% BTC crashes.
  It sat in cash through 2018 and 2022.
- **2025 was a losing year** (58% win rate, −19%). Expect losing streaks.
- **Bias warnings:** the coin list is today's survivors, and I saw 2023–26 results while choosing the entry type.
  Real results will likely be worse. Paper-trade before using real money.

## Run it
```bash
pip install -r ../requirements.txt
python fetch.py                         # download daily candles for the basket
python -m pytest -q tests               # 15 hand-checked tests: exits, gaps, sizing, caps, no look-ahead
python report.py                        # rebuild reports/REPORT.md, trades.csv and equity.png
python portfolio.py --risk 0.01         # try a different risk per trade
python scan_today.py --equity 10000     # today's signals with stop, target and size (prints only, no orders)
```

*Research code, not financial advice.*
