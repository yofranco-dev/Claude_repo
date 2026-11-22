# Trade trends, size by volatility, forget 70%

One family of systematic crypto strategies has held up out of sample, after costs and across independent researchers: **trend following (time-series momentum, Donchian breakouts, moving-average filters) combined with volatility-targeted position sizing, held long or in cash**. The best evidence, a survivorship-bias-free ensemble of Donchian channels on a rotating top-20 coin universe, reports a **Sharpe above 1.5 and about 10.8% a year of alpha over BTC after fees** (2015 to 2025). Credible out-of-sample, net-of-cost Sharpe ratios for simple trend rules cluster around **1.0 to 1.5**. Live fund and ETF records are humbler. Trend systems mostly **reshape risk rather than add return**: they cut drawdowns sharply, roughly match BTC on Sharpe, and trail it in bull markets. Short lookbacks have also decayed since 2021. Nearly everything else on your list fails for a long-only US spot account at 0.15-0.60% per side:
- Cross-sectional momentum's edge comes largely from the short side.
- BTC-dominance rotation and on-chain top signals rest on three or four cycles.
- Carry needs derivatives and has compressed to near T-bill yields.
- Grid bots and market making need fee rebates, and grids lose in trends.
- Mean reversion lives in illiquid small coins.
- DCA variants are risk-management tools, not alpha.

The 70%-win-rate, large-win goal conflicts directly with this evidence. The trend systems that work win only **28-50% of trades** and earn their money from rare large winners. Your +10%/-20% breakout is almost exactly what a market with no edge produces geometrically. The recommendation below is to build a vol-targeted, multi-coin trend ensemble. The bar is beating vol-matched BTC, not beating BTC's raw CAGR.

## Trend following is the edge that survives out of sample

Academic support for crypto trend persistence is broad and has been replicated.

**Time-series momentum.** Liu & Tsyvinski found that a positive weekly BTC return "positively and statistically significantly predicts 1-week, 2-week, 3-week, and 4-week ahead returns." The effect held in an out-of-sample split inside their 2011-2018 sample ([NBER w24877](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)).

**Moving-average rules.** Detzel et al. showed that ratios of price to its 5- to 100-day moving averages produce economically significant alpha and Sharpe gains over buy-and-hold, in and out of sample ([EconPapers](https://econpapers.repec.org/RePEc:bla:finmgt:v:50:y:2021:i:1:p:107-137)).

**Data-snooping tests.** Hudson & Urquhart tested about 15,000 technical rules and found that a large share survive multiple-hypothesis corrections. Break-even transaction costs were "substantially higher" than actual crypto costs ([Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1)). The same work carries a warning that recurs throughout this evidence: **BTC itself showed no predictability in their out-of-sample period, while other coins did.** That matches Grobys et al. In that study, a 20-day MA rule earned **8.76% a year of excess return excluding BTC** across 11 coins ([Univ. Vaasa](https://osuva.uwasa.fi/bitstream/10024/11192/2/Osuva_%20Grobys_Ahmed_Sapkota_2020.pdf)).

### The strongest study is a Donchian ensemble with vol targeting

The most implementable evidence comes from Zarattini, Pagani & Barbon (2025). Their system works as follows ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5209907); [CXO Advisory](https://www.cxoadvisory.com/technical-trading/crypto-asset-trend-following-strategies/)):
- It averages Donchian-channel trend signals over lookbacks from **5 to 360 days**.
- It resizes each position daily to a **25% annualized volatility target**.
- It rotates a universe of up to 20 liquid coins monthly.
- It tests on survivorship-bias-free data covering 21,616 assets.

The results are a **Sharpe of about 1.5, stable across portfolio sizes**, and 10.8-11% a year of net alpha over BTC. CXO reports one configuration at **18% net CAGR assuming 0.10% costs** ([CXO Advisory](https://www.cxoadvisory.com/technical-trading/crypto-asset-trend-following-strategies/)). An unverified independent replication got a lower but consistent **Sharpe of 1.21 with a -20% maximum drawdown** at a 50% vol target ([GitHub](https://github.com/zebadee2kk/DeFi-TraderStack-Agent/issues/137)). The paper's key decay finding is that **long trends "remain statistically robust, but shorter trends have weakened in the recent era"** ([Concretum](https://concretumgroup.com/catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins/)).

Two 2026 walk-forward working papers point the same way, though neither is refereed:
- Howden & Andreev fixed a 30-day TSMOM lookback in advance. They report a **net Sharpe of 1.41 versus 0.70 for buy-and-hold at 25 bps of cost**, and about 1.53 with a crash-state de-risking overlay ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7115459)).
- Monash researchers found that drawdown-controlled TSMOM (65-day lookback for BTC, 20-day for ETH) beat buy-and-hold on Sharpe and drawdown after costs. Shorter lookbacks lost more to rebalancing costs ([Monash](https://www.monash.edu/__data/assets/pdf_file/0011/3744821/Trend-following-Strategies-for-Crypto-Investors.pdf)).

### Moving-average filters cut drawdowns but do not add return

Your own 200-day result matches the literature. Across independent backtests, a BTC long/cash MA filter **takes 13-27 points off the worst drawdown** but leaves CAGR near buy-and-hold. One test found 61.2% versus 63.9% a year, with the worst fall cut from about 83% to 70% ([tradermarkus](https://tradermarkus.com/bitcoin-200-day-moving-average/)). Over 2016-2026, an MA strategy returned **56.0% a year with a Sharpe of 1.07, against 60.5% and 1.04 for buy-and-hold** ([finzdata](https://data.finzdata.com/s/bitcoin-50-200-moving-average-trend-2a424b)).

Volatility targeting moves the needle more. A peer-reviewed BTC study lifted the Sharpe from **0.72 to 1.21** and "virtually eliminat[ed] large crashes" ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1042444X22000019)). A practitioner study over 2017 to mid-2025 found that trend rules cut BTC's deepest loss from **84% to 15%**, and that **plain volatility targeting captured most of that improvement**. Its conclusion was that trend following "reshaped risk far more than it added return" ([Systematic Strategies](https://systematicstrategies.substack.com/p/can-you-keep-bitcoins-upside-without)). For your bot, this means any trend result must be compared against BTC scaled to the same volatility. Otherwise you cannot tell whether the signal adds anything beyond holding less BTC.

| Approach | Best evidence | Evidence quality | Net Sharpe (reported) | Drawdown effect | Decay / caveat |
|---|---|---|---|---|---|
| Donchian ensemble, top-20 coins, 25% vol target | Zarattini et al. 2025 | Survivorship-free backtest, net of 0.10% costs, one replication | ~1.5 (replication 1.21) | Replication -20% at 50% vol target | Short lookbacks weakened; almost no post-publication period |
| TSMOM 20-65 day, BTC/ETH | Howden & Andreev 2026; Monash | Walk-forward, net of 25 bps; unrefereed | 1.41-1.53 vs 0.70 buy-and-hold | Lower than buy-and-hold | Rebalancing costs bite at short lookbacks |
| 200-day / 50-200 MA filter on BTC | Multiple blogs, Grayscale | Many independent in-sample backtests | ~1.07 vs 1.04 buy-and-hold | -64% to -70% vs -77% to -83% | Trails buy-and-hold CAGR on most start dates |
| Vol targeting alone | J. Multinational Fin. Mgmt 2022 | Peer-reviewed | 1.21 vs 0.72 | "Virtually eliminates large crashes" | Gives up CAGR in strong bull runs |

## Live money confirms smaller drawdowns, not BTC-beating returns

Real-money records are the stress test, and they temper the backtests.

**Hedge fund indices.** In Galaxy VisionTrack's net-of-fee indices, **quant funds lost 26.6% in 2022 against 57.4% for fundamental funds** ([VisionTrack](https://visiontrack.galaxy.com/indices/)). Quant directional funds were the best category in 2024 at **+53.7%, but BTC gained about 120%** ([Bloomberg](https://www.bloomberg.com/news/articles/2025-01-15/crypto-hedge-funds-had-a-great-2024-but-failed-to-beat-bitcoin)). Directional funds then lost **10.1% in 2025**, and quant directional was **down 6.4% in 2026 year-to-date** ([The Block](https://www.theblock.co/post/403128/the-funding-how-crypto-hedge-funds-are-navigating-weak-markets)). Bloomberg reported that "choppy crypto markets punished trend-following funds in 2025," and that the early-2026 selloff "offered a reprieve" ([Bloomberg](https://www.bloomberg.com/news/articles/2026-02-27/crypto-trend-following-trade-finds-relief-after-sharp-selloff)).

**Trend ETFs.** These have not beaten spot BTC either. Global X BTRN returned **+4.37% NAV in its first year** ([Global X](https://globalxetfs.com/?p=18201)), though it fell less than its category over one year (-25.4% vs -31.7%) ([KoalaGains](https://koalagains.com/etfs/NYSEARCA/BTRN/performance-returns)). Both products carry fees near 0.9% and futures roll costs. A spot implementation avoids those costs.

**Market-neutral funds.** The one category that is consistently positive in live data is market neutral, at about **19% annualized over three years**. Its returns come mostly from basis, funding and arbitrage capture ([The Block](https://www.theblock.co/post/403128/the-funding-how-crypto-hedge-funds-are-navigating-weak-markets)), and those need derivatives your setup lacks.

**Retail outcomes.** The baseline is grim. The BIS found that a majority of crypto-app users in nearly all of 95 economies lost money on bitcoin over 2015-2022 ([BIS](https://www.bis.org/publ/bisbull69.htm)). In a vendor study of more than 100,000 accounts, only **48% of copy-trading followers were profitable** ([KuCoin](https://www.kucoin.com/blog/ua-is-crypto-copytrading-profitable-in-2026)). By that standard, a bot that matches BTC's return with half the drawdown already beats the median trader.

**Diversification.** Man AHL adds a structural point: a single crypto market's trend Sharpe is "positive but small." Risk-adjusted returns improve with diversification and **peak at about 10-15 coins** ([Man Institute](https://www.man.com/maninstitute/in-crypto-we-trend)). This supports a multi-coin design. The regime risk is real, though. Altcoins have been in a bear market since late 2024, and 2025 was "an exceptionally narrow market" ([CoinDesk](https://www.coindesk.com/markets/2026/01/23/altcoins-have-been-in-a-bear-market-since-late-2024-pantera-says)).

## Most other strategies fail the long-only spot test

**Cross-sectional momentum.** The headline Liu-Tsyvinski-Wu figures of **2.5-4.1% a week** are gross, long-short and in-sample for 2014-2018 ([NBER](https://www.nber.org/papers/w25882.pdf)). The authors' own 2025 extension still finds positive momentum through September 2025 ([arXiv](https://arxiv.org/pdf/2510.14435)). Later work cuts against the effect on several fronts:
- Momentum "extracts alphas largely from short positions" and "incurs substantial trading costs" ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1057521924001509)).
- After correcting for survivorship and delisting, **momentum shows no positive relation to returns**. Equal-weighted backtests are inflated by about **62% a year** ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4287573)).
- A value-weighted test found about **-3.4% a week** with extreme crash tails ([Springer](https://link.springer.com/article/10.1007/s11408-025-00474-9)).
- One practitioner replication found a gross Sharpe of 1.12 before 2023 and -0.68 after, with alpha destroyed by turnover at 20 bps ([GitHub](https://github.com/Gautam-Kanna/crypto-momentum-reversal)).

For a long-only account, the long leg is mostly market beta plus trend, which you already capture with time-series trend.

**BTC-dominance and alt-season rotation.** There is no peer-reviewed or reproducible backtest. The claims are in-sample on 2017-2021, use inconsistent thresholds (40%, 50%, 54%, 55%), and come without trade logs ([The Ledger Mind](https://theledgermind.com/altcoin-season-vs/)). Dominance stayed around 56-60% through the 2024-2026 cycle, so no broad alt season ever fired ([Bitcoin Foundation](https://bitcoinfoundation.org/news/altcoins/understanding-altcoin-season-in-2026-what-are-altcoin-market-cycles/)). A 4-week BTC/ETH/cash dual-momentum rotation still suffered about **-86% maximum drawdown**, close to buy-and-hold ([FinzData](https://data.finzdata.com/s/bitcoin-vs-ether-dual-momentum-4-week-cash-when-both-fall-32cfb7)). In another replication, removing the relative-momentum ranking *improved* results, while removing the cash switch doubled the drawdown ([GQResearch](https://gqresearch.substack.com/p/dual-momentum-without-the-dual)). In other words, the trend filter does the work.

**On-chain top indicators.** These failed in the 2025 cycle. At the October 2025 peak (about $126k), the **MVRV Z-score was about 2.5, against 7+ at earlier tops**. NUPL never sustained readings above 0.75, and Pi Cycle never crossed ([BGeometrics](https://bgeometrics.com/blog/2026-10-mvrv-z-score-explained/); [bit.com](https://www.bit.com/knowledge-hub/mvrv-explained)). Stock-to-flow broke its lower band in June 2022 ([Cointelegraph](https://cointelegraph.com/news/stock-to-flow-model-possibly-invalidated-as-bitcoin-price-loses-30k)). Bottom-zone anchors are better accumulation guides than timing triggers, because they also break. In November 2026, BTC sits at about $55-58k, **below the 200-week MA (about $68k)** and near realized price (about $54k) ([Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/bitcoin-breaks-200-week-sma-143215312.html); [Amberdata](https://blog.amberdata.io/onchain-valuation-what-bitcoins-realized-price-says-about-2026)). With three or four cycles of data, any calibrated threshold is overfit almost by construction.

**Funding and basis carry.** This is the most real market-neutral edge. Carry averages above 10% a year, sometimes exceeds 40%, and **high carry predicts crashes** ([BIS WP 1087](https://www.bis.org/publ/work1087.htm)). Perp arbitrage Sharpe ratios run from **1.8 for high-cost retail to 3.5 for zero-fee market makers** ([arXiv](https://arxiv.org/abs/2212.06888v6)). But carry compressed to **about 3-5% in 2026, near or below Treasury yields**, with a record 67-day negative-funding streak ([Talos](https://www.talos.com/insights/following-the-funding-the-shift-towards-the-equity-basis-trade); [The Block](https://www.theblock.co/news/markets/2026-11-19-sygnum-bitcoin-carry-trades-beating-treasury-bills-2027-443547)). Running it also needs a short futures leg, which Alpaca and Coinbase spot accounts cannot hold.

**Grid bots and market making.** Neither has independent profitability evidence. A grid backtest with an **82.5% win rate lost 0.72%** ([QuantTradingPro](https://quanttradingpro.com/strategy/kbMsMwB8-Grid-Bot-Backtesting)). Grids cap upside in bull runs and accumulate losing inventory in downtrends ([Bitconize](https://bitconize.com/articles/pionex-crypto-trading-bot-why/)). Standard maker strategies on Binance BTC perps were "highly unprofitable" because of structural adverse selection ([arXiv](https://arxiv.org/html/2502.18625v2)). Retail-tier maker fees are positive rather than rebates, which removes the margin entirely.

**Mean reversion.** Short-horizon reversal exists only in small, illiquid coins. Large coins show weekly *momentum* ([ResearchGate](https://www.researchgate.net/publication/354881251_Up_or_down_Short-term_reversal_momentum_and_liquidity_effects_in_cryptocurrency_markets)). BTC's day/overnight reversal edge falls from **4.24 bp to 0.14 bp at just 2 bp of cost** ([JRFM](https://doi.org/10.3390/jrfm19090692)). Quantpedia's out-of-sample BTC test found that buy-the-low degraded while the breakout rule held ([Quantpedia](https://quantpedia.com/?p=35597)). An RSI grid search found only **2 of 88 configurations with a positive in-sample edge** ([Coinpaprika](https://coinpaprika.com/education/backtest-crypto-strategy)).

**DCA variants.** Lump sum beat 12-month DCA on about **73% of BTC entry dates** ([SpotedCrypto](https://www.spotedcrypto.com/bitcoin-dca-strategy-guide/)). Buying only below the 200-day MA beat plain DCA in just **3.9% of rolling 3-year periods** ([FrugalBC](https://frugalbccrypto.substack.com/p/bitcoin-dca-backtest)). MVRV-weighting won about 60% of rolling 1-year windows in a self-published, in-sample study ([Medium](https://medium.com/@thishan93/can-on-chain-data-actually-improve-bitcoin-dollar-cost-averaging-21cc096d5025)).

| Strategy | Works for many traders with OOS/live proof? | Fits long-only US spot at 0.15-0.6%/side? | Verdict |
|---|---|---|---|
| Multi-coin trend + vol targeting | Yes (backtests, replications; live funds cut drawdowns) | Yes, at low turnover | Build |
| BTC/ETH trend filter + vol targeting | Yes, as risk reducer | Yes | Build (core / benchmark) |
| Cross-sectional momentum | Contested; short-leg and small-cap driven | Long leg only, high turnover | Skip, or test as a tilt only |
| BTC dominance / alt rotation | No | Yes, but no evidence | Skip |
| On-chain top/bottom timing | No; top signals failed in 2025 | Yes | Use as slow DCA tilt only |
| Funding/basis carry | Yes, live market-neutral funds | No (needs shorts), yield ~T-bills in 2026 | Not available |
| Grid bots | No independent evidence | Fees kill tight grids | Skip |
| Market making | No for retail | No rebates | Skip |
| Mean reversion on majors | No; momentum dominates large caps | Costs exceed edge | Skip |
| DCA / valuation-weighted DCA | Lump sum usually wins; tilt edge modest, in-sample | Yes | Accumulation tool only |

## A 70% win rate with large wins contradicts the evidence

Win rate is a property of where you place the target and the stop, not a measure of edge. For a price path with no drift or predictability, the probability of reaching +a before -b is roughly b/(a+b). Your **+10% target with a -20% stop therefore wins about 66.7% of the time with zero edge**. Your observed ~70% means roughly 3 percentage points of real edge, part of which is BTC's upward drift. That gives a gross expectancy of 0.7×10 − 0.3×20 = **+1.0% per trade and a profit factor of 7/6 ≈ 1.17**, matching your measured ~1.2.

Costs then eat most of what is left. Alpaca's tier-1 fees are 0.15% maker and 0.25% taker; Coinbase's entry tier is 0.40% maker and 0.60% taker ([Alpaca](https://docs.alpaca.markets/docs/crypto-fees); [Coinbase](https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees)):
- At a ~0.5% taker round trip on Alpaca, the break-even win rate rises to **68.3%**.
- At a 1.2% round trip on Coinbase, it rises to **70.7%**. At that tier your setup has negative expectancy.

The fact that it lagged BTC buy-and-hold at ~9% a year is what the arithmetic predicts. This is the general rule that expectancy, not hit rate, determines profit ([Paragon Signals](https://buttondown.com/Paragon-Signals/archive/a-70-win-rate-that-makes-exactly-0/)). A short-options system that won **82.6% of 717 trades still had negative expectancy** until its ten worst trades were removed ([jwplatta](https://jwplatta.github.io/posts/distribution-and-regime-effects-in-a-1dte-options-strategy)).

The strategies that do work have the opposite shape. A 4,791-trade crypto trend backtest **won only 28% of trades, but average winners were +44.7% and average losers -9.7%** ([altFINS](https://altfins.com/knowledge-base/which-trading-strategy-works-crypto-stocks-forex-backtest)). That works out to about +5.5% expectancy per trade and a profit factor near 1.8. A BTC MA study found win rates of about **17-39%** ([notp1ssed](https://notp1ssed.github.io/portfolio/assets/docs/002_TrendFollowing_Strategy_bitcoin.html)), and Donchian blog systems report **35-50% win rates with profit factors of 1.4-2.2** ([MQL5](https://www.mql5.com/en/blogs/post/770303)). Potters & Bouchaud show formally that trend followers "lose more often than they gain" yet profit because winners are held longer and run further ([arXiv](https://arxiv.org/abs/physics/0508104)).

Wins of 10-100% require letting trades run, which requires accepting many small losses. A 70% hit rate requires the reverse: cut winners short and give losers room. You can have one or the other, not both, without an edge far larger than any documented. The metrics worth optimizing are **profit factor above 1.5, Sharpe, maximum drawdown, and alpha against vol-matched BTC**. Expect a win rate of 35-50%.

## Costs on Alpaca and Coinbase decide what is implementable

Turnover is the binding constraint. At Coinbase's entry taker fee, **50 round trips a year costs about 60% of capital; at Alpaca's taker fee, about 25%** ([Alpaca](https://docs.alpaca.markets/docs/trading/crypto-trading/); [Coinbase](https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees)). The published edges were measured at 0.10-0.25% per trade, which is below Coinbase's retail tier. Fee level therefore tips Alpaca, or Coinbase with maker-only limit orders, from marginal to viable. It also explains why short lookbacks, the first casualty of decay, must go.

Several platform details matter for the design:
- **Alpaca's coin list.** It held about 20 coins (BTC, ETH, AVAX, LINK, DOT, LTC, BCH, UNI, AAVE, DOGE, SHIB and others), plus 11 added in May 2026, including ADA and ARB ([Alpaca](https://alpaca.markets/support/what-are-the-supported-coins-pairs); [Crowdfund Insider](https://www.crowdfundinsider.com/2026/05/280485-alpaca-expands-crypto-portfolio-with-cardano-ondo-arbitrum-other-digital-assets/)). Your backtest universe must therefore be point-in-time, not today's list.
- **Alpaca order types.** Crypto supports only market, limit and stop-limit orders, with no bracket orders. Coinbase supports attached take-profit/stop-loss brackets ([Alpaca](https://docs.alpaca.markets/us/docs/crypto-orders.md); [Coinbase CDP](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/guides/orders)). Daily-close signals executed with limit orders suit both.
- **Taxes.** As of November 2026, the wash-sale rule still does not apply to directly held crypto, though bills are pending ([CoinTracking](https://cointracking.info/blog/crypto-tax-loss-harvesting-bitcoin-drawdown-2026)). Every rebalance is a taxable event, which is another argument for low turnover.

## Three strategies to build and backtest, ranked

All three share one backtest discipline:
- **Data.** Use daily closes, signal at the close, and fill at the next bar's open plus slippage. Use a point-in-time universe that includes coins later delisted, because survivorship inflates equal-weighted crypto results enormously ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4287573)).
- **Out-of-sample protocol.** Fix parameters before looking at 2023-11 to 2026-11, which becomes the holdout. Ensembles of lookbacks avoid picking a single best parameter.
- **Benchmarks.** Report results against three benchmarks: BTC buy-and-hold, your existing BTC 200-day filter, and **BTC scaled daily to the same realized volatility as the strategy**. The last one is the real test.
- **Costs.** Assume **0.35% per side on Alpaca** (0.25% taker plus 0.10% spread/slippage) and **0.75% per side on Coinbase entry tier**, then rerun at double those costs.

**1. Multi-coin Donchian-ensemble trend with volatility targeting (long/cash).** This adapts Zarattini et al. to US spot.
- *Universe.* Coins tradable on your broker at each date, excluding stablecoins, filtered to the top 15-20 by 30-day median dollar volume and reselected monthly. Require at least 365 days of history.
- *Signal.* For each coin, run seven sub-models with lookbacks N ∈ {20, 30, 60, 90, 150, 250, 360}. The 5- and 10-day lookbacks are dropped because they decayed and are cost-heavy. Each sub-model goes long when the close exceeds the prior N-day high, and exits when the close falls below the prior N/2-day low or below a trailing stop at 2.5× ATR(20) under the highest close since entry. The coin's signal is the fraction of sub-models that are long (0 to 1).
- *Sizing.* Raw weight = signal × (20% / the coin's 60-day realized annualized volatility). Cap each coin at 20% of equity, and scale the book down so total exposure never exceeds 100% (no leverage). The remainder sits in USD cash.
- *Rebalance.* Recompute daily. Trade only when a coin's target weight moves by more than 25% of its current weight, or more than 3% of equity, to suppress churn. Use limit orders at the touch on Coinbase to pay maker fees.
- *Success.* All of the following must hold on the holdout, net of costs:
  - Sharpe of at least 1.0 and at least 0.2 above vol-matched BTC.
  - Maximum drawdown of 35% or less.
  - Positive alpha in a regression on BTC returns.
  - Profit factor of at least 1.5.
  - One-way turnover of no more than about 8× capital a year (no more than about 5× on Coinbase).
  - Sharpe still positive at double costs, and falling by less than 30% when the lookback set is shifted ±30%.
- *Kill condition.* If it fails to beat the BTC/ETH-only version below, the altcoin sleeve is not paying for its costs. Expect a 35-50% win rate and long stretches in cash. In the 2024-2026 altcoin bear, mostly cash or BTC is the correct behavior, not a bug.

**2. BTC/ETH multi-horizon trend core with volatility targeting.** This is simpler and cheaper. It doubles as the ablation benchmark for strategy 1 and as the fallback if the altcoin sleeve fails.
- *Signal.* For BTC and ETH separately, the trend score is the average of five binary checks: close above the 50-, 100- and 200-day SMAs, close above the 20-day EMA's level of 20 days earlier, and a positive 30-day return. Each check scores 0 or 1. This blends the 30-day TSMOM ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7115459)) with the long MA filters you already tested.
- *Sizing.* Weight = score × min(1, 35% / 30-day realized volatility), with BTC getting 60% of capital and ETH 40%. Add a crash overlay that halves exposure when the portfolio is down more than 20% from its high and the 30-day volatility is in the top decile.
- *Rebalance.* Check weekly, with a 10-percentage-point band.
- *Success.* All of the following on the holdout, net of costs:
  - Sharpe at least 0.2 above BTC buy-and-hold and above vol-matched BTC.
  - Maximum drawdown of 40% or less, against BTC's roughly -77%.
  - Calmar ratio at least double buy-and-hold's.
  - Fewer than 15 round trips per coin per year.

A lower CAGR than buy-and-hold in bull years is acceptable. Failing on Sharpe against vol-matched BTC is not, because it would mean the trend signal adds nothing beyond de-levering.

**3. Valuation-tilted DCA accumulation sleeve (optional, lowest priority).** This is only for capital you intend to hold long-term anyway.
- *Rules.* Make a base weekly BTC buy. Scale it ×2 when price is below the 200-week MA or the MVRV Z-score is below 0, and ×0.5 when MVRV-Z is above 3. Never sell.
- *Rationale and timing.* The evidence is modest and in-sample ([Medium](https://medium.com/@thishan93/can-on-chain-data-actually-improve-bitcoin-dollar-cost-averaging-21cc096d5025)), but costs are trivial and the current regime puts it in its ×2 zone.
- *Success.* It beats plain weekly DCA in at least 60% of rolling 2-year windows on data not used to set the thresholds. Test it with the 2013-2017 cycle held out if you calibrate on later data.

## Conclusion

The goal should change from "win often" to "lose small, stay in big trends, and hold less when volatility spikes." Documented crypto edges are trend persistence and volatility clustering, not high hit rates. Because volatility targeting alone delivers much of the drawdown benefit, the honest test of any trend bot is whether it beats BTC scaled to the same risk. That test is stricter than your earlier comparisons and more informative.

Two caveats deserve weight. First, the strongest backtest (Zarattini et al.) has almost no post-publication history, and live trend funds lost money in the choppy 2025 market. Second, the figures here come mostly from abstracts and summaries rather than full-text tables, so verify the key numbers against the primary PDFs before relying on them. Build strategy 2 first as the benchmark. Then accept strategy 1 only if the altcoin sleeve adds Sharpe after costs. On Coinbase's entry tier, consider whether Alpaca's lower fees alone are worth more than any signal refinement.
