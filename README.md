# Crypto Backtester: RSI(2) Pullback Strategy

A backtest of a high-win-rate, mean-reversion crypto strategy. It runs on real Binance 4-hour candles
for BTC, ETH, SOL, BNB and XRP (2019 to today) and charges fees and slippage on every trade.
Parameters are tuned only on 2019–2022 data and then tested on 2023 onward, which they never saw.

## Results at a glance (target: 70% win rate)

| Strategy | In-sample win rate (2019–22) | Out-of-sample win rate (2023–now) | Out-of-sample profit factor | Verdict |
|---|---|---|---|---|
| A: RSI(2) pullback, exit on SMA cross ([report](reports/REPORT.md)) | 71.2% | **57.3%** | 0.85 | ❌ fails out-of-sample, loses money |
| B: RSI(2) pullback, fixed ATR take-profit, settings picked by the pre-set rule ([report](reports/VARIANT_B.md)) | 70.9% | **62.3%** | 0.81 | ❌ fails out-of-sample, loses money |
| B with a tight 0.5×ATR take-profit and 4×ATR stop | 92.0% | **89.0%** | 1.15 | ⚠️ passes on win rate, but only about +0.09% per trade after costs |

**Bottom line:** a 70%+ win rate on crypto is easy to reach by taking small profits and allowing large losses.
It does **not** mean the strategy makes money. Of the 32 settings with a 70%+ in-sample win rate, 27 kept 70%+
out-of-sample, but only 4 were profitable. All 4 made less than 0.1% per trade. Read the reports before trading any of this.

> **Newer:** see [`trend_bot/`](trend_bot/README.md) for the end-to-end trend bot (data → rule → backtest → dry run).

## Run it

```bash
pip install -r requirements.txt
cd src
python fetch_data.py      # downloads 4h candles to data/ (public Binance API, no key needed)
python validate.py        # Strategy A: in-sample optimisation, out-of-sample test, walk-forward -> reports/REPORT.md
python tp_variant.py      # Strategy B: take-profit variant -> reports/VARIANT_B.md
```

## How the backtest avoids fooling itself
- **No look-ahead:** signals use closed candles only, and every fill happens at the next candle's open.
- **Costs:** 0.10% fee and 0.05% slippage per side, about 0.3% per round trip.
- **Out-of-sample test:** parameters are chosen on 2019–2022 only; 2023 onward is the test.
- **Walk-forward (Strategy A):** each year is re-optimised on all prior data only, then traded.
- **Intrabar exits (Strategy B):** if the stop and the target fall inside the same candle, the stop is assumed to hit first.

## Files
- `src/fetch_data.py`: data downloader
- `src/backtest.py`: indicators, backtest engine and performance stats
- `src/validate.py`: Strategy A validation and report
- `src/tp_variant.py`: Strategy B and the full transparency table
- `reports/`: generated reports, trade logs (CSV) and the equity chart

*Research code only, not financial advice. Past performance does not predict future results.*
