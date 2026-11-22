# Trend bot (crypto): version 1

The smallest end-to-end version of a rules-based trading system: **data → rule → backtest → dry run**.
It has no broker connection, no API keys and no AI layer yet. It's adapted for crypto: BTC/USDT daily candles,
where a "session" is one UTC day because crypto trades 24/7.

**Rule:** after each daily close, target 100% long if the close is above its 200-session simple moving average,
otherwise cash. It recalculates daily but only trades when the target changes. This is a deliberately simple test
rule, not a claim that it's profitable.

## Backtest results (BTC/USDT, 0.10% fee + 0.05% slippage per side)

| Period | Return | CAGR | Max drawdown | Buy & hold return | B&H max drawdown | Win rate |
|---|---|---|---|---|---|---|
| Development, 2018-03 → 2024-11 | +703% | +36.4% | −64% | +753% | −77% | 22% |
| **Final test, 2024-11 → 2026-11** (never used to choose rules) | **−20%** | −10.4% | **−32%** | −39% | −53% | 20% |
| Full history | +546% | +23.9% | −64% | +422% | −77% | 24% |

Full trade list: [reports/REPORT.md](reports/REPORT.md).

**Honest read:** the rule's value is that it **steps aside during downtrends**. It roughly matched buy & hold
in the bull years, lost about half as much in the 2024–26 test period, and had smaller drawdowns throughout.
Its win rate is only about 22%, far from the 70% target set earlier. That's normal for trend-following:
many small whipsaw losses, a few large winning trends. See `../reports/` for why chasing a 70% win rate
on its own led to strategies that lost money.

## Run it

```bash
pip install -r ../requirements.txt
cd trend_bot
python -m pytest -q                 # 24 hand-calculated tests
python backtest.py                  # rebuilds reports/REPORT.md from the frozen research CSV
python dry_run.py                   # downloads fresh data, validates it, prints the intended order
python dry_run.py --record          # same, and records the order ID in ledger.json (idempotent)
touch PAUSE                         # pause switch: dry_run refuses to plan orders until removed
```
Costs are configurable: `python backtest.py --fee 0.0006 --slippage 0.001`.

## Layout
| File | Role |
|---|---|
| `data.py` | Downloads daily candles from Binance's public API. Validates for duplicates, gaps, NaN, invalid prices and stale data. Keeps a **frozen research copy** (`data/research/`, committed) separate from **fresh data** (`data/live/`, ignored by git). |
| `strategy.py` | `target_positions()`: pure function, completed bars in, target out, with no look-ahead. |
| `backtest.py` | Next-open fills, fees, slippage, buy & hold comparison, development and holdout periods. |
| `dry_run.py` | Prints the intended order. Deterministic client order ID per session, so a second run can't duplicate it. Blocks on stale data, unexpected position, unknown order status or the pause switch. |
| `tests/` | Hand-calculated 8-day dataset; proves fills happen at the next open, never the signal close; future bars can't change past signals; the warm-up period doesn't trade; costs are applied on both sides; data checks and dry-run safety. |

## Next steps (in order)
1. **Paper broker:** add an Alpaca paper adapter (it supports crypto) behind `dry_run.plan()`. Keep credentials
   in an env file outside this repo, reject any non-paper endpoint, and look up orders by client order ID before
   retrying a timed-out submit.
2. **Scheduling and alerts:** run shortly after 00:00 UTC daily and send Telegram alerts on any `blocked` result.
   Test missed runs, restarts, rejected orders and partial fills.
3. **Compare paper fills with the backtest:** paper trading doesn't model market impact or latency, so treat it
   as a check that the system behaves as intended, not proof of profit.
4. **AI layer (last):** log an LLM's opinion next to each signal **without letting it change orders**, then
   compare it with the rules-only results.

*Research code, not financial advice.*
