# Trend strategies v2: the research-backed approach, tested honestly

The two strategies ranked highest in [`reports/Proven crypto trading strategies.md`](../reports/Proven%20crypto%20trading%20strategies.md),
built exactly to the report's rules (fixed before testing, nothing tuned) and judged on its pass/fail criteria.
Full results: [reports/REPORT.md](reports/REPORT.md).

## Verdict

| | Development 2018–2023 | **Holdout 2023-11 → 2026-11** | Verdict |
|---|---|---|---|
| **BTC/ETH trend core** | Sharpe **1.00**, +25%/yr, max DD −33% | Sharpe **0.72**, +15%/yr, max DD **−28%** | ✅ **Build this one.** It beats vol-matched BTC by 0.31 Sharpe with half BTC's drawdown. It narrowly misses two stretch targets. |
| Donchian ensemble, top-20 coins | Sharpe 1.16, +54%/yr, max DD −62% | Sharpe 0.54, max DD −49%, 22× turnover | ❌ Fails 6 of 9 criteria and loses to the core. The altcoin sleeve doesn't pay for its costs. |
| BTC buy & hold | Sharpe 0.60, max DD −81% | Sharpe 0.57, max DD −53% | Benchmark |

**What the core does:** it holds less when trends weaken or volatility jumps, and moves fully to cash in downtrends.
It made money in 2025 (+10%) when BTC fell, and lost only 9% in 2026 so far vs BTC −31%. It trails BTC in strong
bull years (2024: +37% vs +121%). That trade-off is the point: about the same long-run return with much smaller crashes.

**Win rate is about 30–37%** with a profit factor of 2.3–3.1: winners are about 2.5× the size of losers. Every credible
source says this is what a working crypto system looks like. The 70%-win-rate systems earlier in this repo had thin
edges because the win rate came from where the target and stop sat, not from skill.

## BTC/ETH trend core: rules
- **Score** (BTC and ETH separately) = the average of 5 yes/no checks: close above the 50-, 100- and 200-day SMAs,
  the 20-day EMA above its level 20 days ago, and a positive 30-day return.
- **Weight** = allocation × score × min(1, 35% ÷ 30-day realized volatility). Allocation is 60% BTC and 40% ETH;
  the rest sits in cash.
- **Crash overlay:** halve exposure when the portfolio is more than 20% below its peak and BTC volatility is in its
  top decile.
- **Rebalance:** weekly on the Sunday close, trading at Monday's open. Only trade when a weight is off by more than
  10 percentage points; full exits always trade. That works out to about 3 round trips per coin per year.
- **Costs tested:** 0.35% per side (Alpaca) Sharpe 0.72, 0.70% per side Sharpe 0.61, Coinbase entry tier Sharpe 0.60.

## How the test avoids fooling itself
- The **universe has 78 price series, including dead coins** (LUNA, FTT, BSV, SRM, HNT, MATIC, XMR, EOS, WAVES, …).
  A coin is sold at its last price if its history ends while held. A reused ticker (LUNA after 2022) is split into
  separate coins.
- Every decision is made at the daily close and **filled at the next open, with costs on every dollar traded**.
  There is no leverage and no shorting.
- **Benchmarks:** BTC buy & hold, the BTC 200-day filter, and **BTC scaled to the same volatility**. The last one is
  the real test of whether the signal adds anything.
- 9 unit tests cover execution timing, costs, delisting, no leverage, the band rule, hand-checked signals and no
  look-ahead.

## Run it
```bash
python get_data.py          # BTC (Bitstamp 2013+) and 77 Binance series incl. delisted coins, fixed end date
python -m pytest -q tests   # 9 tests
python run.py               # reports/REPORT.md and reports/equity.png
```
*Research code, not financial advice. Paper-trade first.*
