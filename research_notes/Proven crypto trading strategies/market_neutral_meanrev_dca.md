# Market-Neutral, High-Win-Rate and DCA Crypto Strategies (research notes, Nov 2026)

Method note: all evidence below comes from web-search result excerpts. Direct page fetches failed because arxiv.org, bis.org, talos.com, blog.bitmex.com and quantpedia.com are not on this session's allowed network hosts. Figures are therefore as reported in search snippets, and some could not be checked against the primary text. Evidence labels: [OOS/live] means out-of-sample or live, [IS] means in-sample or backtest, [vendor] means exchange or affiliate marketing, [press] means a secondary news report.

## Funding-rate / basis carry: yields by year, papers, products, blow-up risks, US retail access

### Takeaway
Crypto carry has been large on average (about 7-10%+ p.a. across exchanges from 2019 to 2024, with peaks of 40-60% p.a. and spikes above 100% annualized in 2021). It compressed hard in 2025-2026, to roughly 3-5% (near or below T-bills), with long negative-funding stretches. By late October 2026 it had partly recovered to about 8%. The academic Sharpe ratios are high (1.8-3.5 for BTC perp arbitrage). The realised risks are venue failure, liquidation of the short leg, negative funding, and collateral or stablecoin depegs. US retail can access the trade on CME and, since July 2025, Coinbase's CFTC-regulated perpetual-style futures.

### Cited Findings
**Academic evidence**
- Schmeling, Schrimpf & Todorov, "Crypto carry", BIS Working Paper No. 1087: first published April 2023, revised October 2025, also CEPR DP 20719. Its main points:
  - Carry (futures minus spot) "can reach exceptionally high levels, sometimes exceeding 40% p.a." The BIS summary page says up to 60% p.a.
  - Carry averages above 10% annually.
  - It is driven by a volatile convenience yield from trend-chasing, attention-driven smaller investors seeking leveraged upside, plus scarce arbitrage capital.
  - High carry predicts future price crashes.
  - Interest-rate differentials explain little of it; press cites about 3%.
  — [BIS WP 1087](https://www.bis.org/publ/work1087.htm); [BIS pdf](https://www.bis.org/publ/work1087.pdf); [IDEAS/CEPR](https://ideas.repec.org/p/cpr/ceprdp/20719.html); [Cointelegraph](https://cointelegraph.com/news/smaller-investors-can-have-outsized-impact-on-crypto-investment-markets-bis-study)
- The same BIS paper (per a search snippet) puts the average annualized carry across exchanges at about 7% p.a. from April 2019 to July 2024. The ">10%" and "~7%" figures may come from different versions or samples. — [BIS pdf](https://www.bis.org/publ/work1087.pdf)
- He, Manela, Ross & von Wachter, "Fundamentals of Perpetual Futures", arXiv 2212.06888 (v1 December 2022, v6 August 2024). Its main points:
  - It derives no-arbitrage perp prices and bounds under trading costs.
  - Deviations from no-arbitrage prices are larger in crypto than in FX, comove across coins, and shrink over time.
  - A "random-maturity arbitrage" strategy on BTC perps has a Sharpe of 1.8 for retail with high trading costs, and up to 3.5 for market makers paying no fees. [IS, historical sample]
  — [arXiv abs](https://arxiv.org/abs/2212.06888v6); [v5 html](https://arxiv.org/html/2212.06888v5)

**Funding and basis levels by period**
- 2021: Binance and Bybit BTC funding rose above 0.1% per 8h, which is more than 100% annualized. The April and October 2021 tops both printed funding above 0.1% per 8h together with record open interest, which is a long-squeeze setup. — [Bitcoinist 2021 review](https://bitcoinist.com/bitcoin-funding-rates-in-2021/amp); [Sharpe.ai](https://www.sharpe.ai/funding-rate/bitcoin)
- BitMEX's 9-year XBTUSD funding analysis (2025 Q2 report) describes a 2021 peak of 0.07-0.1% per period during rallies. — [BitMEX blog](https://blog.bitmex.com/2025q2-derivatives-report) (excerpt only)
- Glassnode's convention: annualized perp funding = 8h rate × 3 × 365. Its cash-and-carry metric compares the 3-month rolling basis with perp funding. — [Glassnode workbench](https://studio.glassnode.com/workbench/btc-futures-annualized-yield)
- Early 2024: BTC perp funding and the 30-day futures basis peaked at 20-40% annualized. In 2026 they fell to roughly 3-5%, near or below Treasury yields. Talos links the shift to basis traders moving toward equity basis trades. — [Talos](https://www.talos.com/insights/following-the-funding-the-shift-towards-the-equity-basis-trade); [Longbridge repost](https://longbridge.com/en/news/305909666)
- 2026:
  - The 30-day average BTC funding rate was negative for 67 consecutive days through May 2026, the longest negative streak of the decade.
  - The CME basis was about 3% in August 2026, below the 3.8% two-year UST yield.
  - Funding recovered to about 8% annualized by end-October 2026.
  - Sygnum (outlook published 19 November 2026) expects carry to beat T-bills in 2027. That is a forecast.
  — [The Block, 2026-11-19](https://www.theblock.co/news/markets/2026-11-19-sygnum-bitcoin-carry-trades-beating-treasury-bills-2027-443547); [Bitcoinist](https://bitcoinist.com/bitcoin-could-soon-outperform-us-treasury-bills-without-a-price-rally-heres-how)
- Unwind of the CME basis trade:
  - Leveraged funds' CME net short fell about 89% from its December 2024 peak.
  - Nine hedge funds cut about 68,000 BTC (about $5.4B) of ETF and basis holdings between September 2025 and June 2026.
  - The CME basis was cited at about 4.8%, "little excess return over Treasuries once financing, margin and volatility are counted".
  — [HedgeCo, Nov 2026](https://hedgeco.net/news/11/2026/hedge-funds-have-unwound-most-of-the-bitcoin-basis-trade-as-cme-net-shorts-fell-89-from-their-peak.html); [CryptoBriefing](https://cryptobriefing.com/hedge-funds-unwind-bitcoin-basis-trade/). The 4.8% is a market calculation, not a CFTC figure. — [Altcoinbuzz](https://www.altcoinbuzz.io/is-bitcoin-s-cme-basis-trade-over-what-cftc-data-shows)

**Ethena-style products (live evidence)**
- Yield history [press / aggregators; figures conflict]:
  - sUSDe averaged about 18% APY in 2024 and ranged from 4% to 15% in 2025.
  - It averaged about 6.58% in the weeks before October 2025.
  - The mid-2026 average was about 3.91%.
  - In late October 2026 it was about 4.8-5.1% (DefiLlama).
  — [StablecoinInsider review](https://stablecoininsider.org/ethenas-staked-usde-stablecoin/); [StablecoinInsider Q1 2026](https://stablecoininsider.org/ethena-usde-q1-2026-report/); [CryptoTether](https://cryptotether.com/articles/why-ethena-susde-yield-is/)
- The 10-11 October 2025 crash (about $19B of liquidations):
  - USDe printed about $0.65 on Binance, about $0.92 on Bybit, and held near peg on Curve. Ethena blamed a Binance internal oracle issue.
  - USDe supply then fell from about $14B toward about $6B, with roughly $8.3B of net outflows, as leverage loops unwound.
  — [Cointelegraph via TradingView](https://www.tradingview.com/news/cointelegraph:4bc2a9faa094b:0-ethena-s-usde-loses-8-3b-since-october-crash-amid-loss-of-confidence/); [CoinMetrics](https://coinmetrics.substack.com/p/state-of-the-network-issue-335)
- Regulatory status: Forbes (June 2026) notes that USDe pays yield outside the GENIUS Act stablecoin framework. — [Forbes](https://www.forbes.com/sites/digital-assets/2026/06/15/ethenas-usde-pays-yield-legally-and-the-genius-act-has-no-answer-for-it/)

**US retail access**
- Coinbase launched US perpetual-style futures on 21 July 2025. Their features:
  - They are CFTC-regulated and trade on Coinbase Derivatives Exchange.
  - Contracts have 5-year expiries and trade 24/7, with up to 10x leverage.
  - Funding accrues hourly and settles twice daily.
  - The hourly rate comes from the average futures-spot premium, smoothed 75% current hour and 25% prior.
  - The nano BTC contract is 1/100 BTC.
  — [CoinDesk 2025-06-27](https://www.coindesk.com/business/2025/06/27/coinbase-sets-us-perpetual-style-futures-launch-as-ceo-says-firm-is-buying-bitcoin-weekly); [Coinbase Learn](https://www.coinbase.com/learn/futures/us-perpetual-style-futures-101); [Coinbase help: funding](https://help.coinbase.com/en/derivatives/perpetual-style-futures/funding-rate); [Kraken comparison](https://www.kraken.com/learn/kraken-vs-coinbase-futures)
- CoinGlass tracks funding for Coinbase venues. — [CoinGlass](https://www.coinglass.com/FundingRate/COINBASE)

### Inferences
- What a retail trader actually earns:
  - Retail costs push the trade toward the low end of the academic range (Sharpe 1.8 vs 3.5 for zero-fee market makers).
  - At 2026 levels of 3-5% gross, a retail cash-and-carry likely earns at or below T-bills after fees, the margin buffer held in low-yield collateral, and roll costs.
  - It is attractive mainly in euphoric regimes, which per BIS are exactly when crash risk is highest.
- How a US retail trader can run it:
  - Long spot or a spot ETF (Coinbase, Robinhood, Alpaca) plus short Coinbase Derivatives perp-style or dated futures, or short CME micro BTC futures through a futures broker.
  - The two legs sit at different entities, so margin is not netted, and a price spike can force the short leg to post margin or be liquidated while the spot gains sit elsewhere.
- Regime break: the edge structurally decayed after spot ETFs (January 2024) brought institutional arbitrage capital. That matches both the He et al. "deviations shrink over time" finding and the 2026 compression.
- Failure modes:
  - Exchange or custody failure. FTX (November 2022) is the canonical case of a hedged position losing its collateral; no source was retrieved here.
  - Short-leg liquidation in squeezes.
  - Prolonged negative funding (67 days in 2026).
  - Collateral or stablecoin depeg (USDe in October 2025).
  - Auto-deleveraging on offshore venues.

### Gaps
- A calendar-year average funding or basis series for 2021-2026 (for example Kaiko or Glassnode annual means) was not retrieved. Only peaks and point snapshots are available. A 2021 average near 30% is plausible but unverified.
- The He et al. and BIS full texts (sample periods, drawdowns, net-of-cost returns by year) could not be fetched.
- Whether US persons can use Coinbase International perps directly was not confirmed. The confirmed US route is Coinbase Derivatives perp-style futures.
- No sourced FTX-specific loss figures for basis traders were collected in this pass.

## Grid trading bots: evidence, win rate vs trend losses, returns

### Takeaway
No independent peer-reviewed study of retail grid-bot profitability was found. The evidence is vendor material and single backtests. These consistently show high trade-level win rates, with net results driven by the underlying's trend: grids lag buy-and-hold in uptrends and accumulate a losing inventory in downtrends.

### Cited Findings
- Pionex says well-configured grid and DCA bots on liquid pairs "consistently generate small gains in sideways and mildly trending markets". [vendor, unverified] — [Pionex blog](https://www.pionex.com/blog/15-reddit-questions-about-crypto-trading-bots-and-pionex-answered-with-real-data/)
- Pionex's "AI 2.0" grid release claims more accurate backtests and higher grid profit, but gives no independent figures. [vendor] — [Pionex AI 2.0](https://www.pionex.com/blog/botai2_en/)
- A user TradingView grid backtest on PIONEX:ETHUSDT.P had an 82.5% win rate and a net loss of −0.72%. [IS, single example] — [QuantTradingPro / TradingView](https://quanttradingpro.com/strategy/kbMsMwB8-Grid-Bot-Backtesting)
- If price breaks below the range, "grid profit may still show positive, but your overall position can be at a loss". Guides warn not to judge a futures grid by "Grid Profit" alone. — [Zenvest guide](https://zenvestai.com/learn/crypto-education/mastering-pionex-futures-grid-bot-guide/)
- In strong bull markets grids sell into strength and cap gains, so they underperform buy-and-hold. — [Bitconize](https://bitconize.com/articles/pionex-crypto-trading-bot-why/)
- A personal parallel test of Pionex bots reported 7-12% returns, which the author judged unremarkable. [anecdotal live] — [Automated Income Lifestyle](https://automatedincomelifestyle.substack.com/p/parallel-testing-crypto-trading-bot-strategies-7fa76c20fe85)
- Pionex launched an "Infinity Grid" variant aimed at rising markets. Its existence is itself an admission of the trend problem. — [TradersUnion](https://tradersunion.com/news/brokers-news/show/3091200-pionex-unveils-infinity-grid-bot/)

### Inferences
- How a grid makes and loses money:
  - It is effectively short volatility and short gamma: it harvests the range like a sequence of covered short strangles.
  - The high win rate comes from many small round-trip profits.
  - The losses come from inventory left unrealised outside the range: bags in a downtrend, missed upside in an uptrend.
- Spot-only US brokers (Coinbase Advanced, Alpaca crypto) let a retail user code a grid. Taker fees of roughly 0.4-0.6% at low Coinbase tiers would consume tight grid spacing, which was not verified in this pass. Offshore venues with near-zero fees (Pionex, Binance) are not available to US persons.

### Gaps
- No independent aggregated user-P&L statistics from Pionex, Binance or 3Commas were found. Binance's "bot leaderboard" style pages and any academic grid study were not retrieved.
- Coinbase and Alpaca fee schedules were not verified in this pass.

## Market making for retail: realistic or not?

### Takeaway
Largely not realistic as a durable edge. Academic tests on Binance perps find standard maker strategies highly unprofitable. Adverse selection is structural. Profits depend on maker rebates and scale or latency that retail lacks. No public dataset of retail Hummingbot P&L exists.

### Cited Findings
- "The Market Maker's Dilemma" (arXiv 2502.18625, February 2025) tested maker strategies on the Binance BTC perpetual:
  - Commonly cited strategies were "highly unprofitable".
  - A contrarian maker approach worked only in "Reversal" conditions.
  - Maker orders fill precisely when a taker arrives on the other side, so they face built-in adverse price moves.
  — [arXiv html](https://arxiv.org/html/2502.18625v2)
- Practitioners say maker rebates are needed to be profitable and margins are razor-thin. One example earned about 0.003% per fill in rebates, viable only at very large automated volume. [anecdotal] — [DEV Community](https://dev.to/trendrider/crypto-market-making-bots-how-they-actually-work-and-why-most-fail-2kn); [Cointelegraph](https://cointelegraph.com/explained/this-trader-turned-68k-into-15m-by-using-a-high-risk-strategy-heres-how)
- SEC DERA (January 2025) notes that uninformed retail flow is valuable to wholesalers because of its limited adverse selection. The implication is that a small quoter on a lit book disproportionately trades with informed flow. — [SEC DERA WP](https://www.sec.gov/files/dera_wp_payment-order-flow-2501.pdf)
- Hummingbot's own papers acknowledge that the software does not solve fragmentation and that maker contracts face adverse selection and monopolization risks. They report no user P&L. — [Hummingbot liquidity mining paper](https://docs.hummingbot.org/liquidity-mining.pdf)
- A dYdX liquidity-provider incentive review shows that rewards programs, not spread capture, were a key draw for LPs. — [arXiv 2307.03935](https://arxiv.org/pdf/2307.03935.pdf)

### Inferences
- On Coinbase or Alpaca at retail tiers, maker fees are positive rather than rebates, which removes the main margin source. Retail market making on US spot brokers is not a realistic edge. At best it is liquidity-mining-incentive harvesting on offshore or DEX venues, with token and smart-contract risk.

### Gaps
- No systematic retail market-maker P&L data were found.

## Short-term mean reversion (RSI(2), Bollinger, daily/weekly reversal) and decay after costs

### Takeaway
Academic short-horizon reversal in crypto is real but concentrated in small, illiquid coins. Large coins show weekly momentum instead. For BTC the intraday edge mostly disappears at about 2 bp of cost. Quantpedia's BTC out-of-sample test found the buy-the-low (MIN) rule degraded while the breakout (MAX) rule held up. No credible out-of-sample evidence supports RSI(2) or Bollinger reversion on BTC.

### Cited Findings
- "Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets" (ResearchGate, 2021): weekly reversal occurs only in small or illiquid coins, large and liquid coins show weekly momentum, and daily reversals come from illiquidity. — [ResearchGate](https://www.researchgate.net/publication/354881251_Up_or_down_Short-term_reversal_momentum_and_liquidity_effects_in_cryptocurrency_markets)
- "Trading volume and liquidity provision in cryptocurrency markets" (Journal of Banking & Finance, 2022): equal-weighted daily reversal earns much higher gross returns than value-weighted, the effect is stronger after low volume, and it is robust to linear costs. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0378426622001418)
- A Fairfield University paper finds losers beat winners at daily, weekly and monthly rebalancing, with a much smaller spread at daily frequency. — [Fairfield](https://digitalcommons.fairfield.edu/cgi/viewcontent.cgi?article=1249&context=business-facultypubs)
- Lagged momentum and reversal across day and overnight sessions in BTC and ETH (JRFM, 2026): the BTC mean daily return differential falls from 4.24 bp at zero cost to 0.14 bp at 2 bp cost. ETH decays less. — [JRFM 19(9):692](https://doi.org/10.3390/jrfm19090692)
- "Order flow and cryptocurrency returns" (Journal of Financial Markets, 2026) uses a break-even cost of return divided by turnover; one strategy had a break-even of 1.07%. — [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1386418126000029)
- Equity benchmark: short-term reversal profits shrink sharply after trading costs. — [EFMA 2011](https://www.efmaefm.org/0efmameetings/efma%20annual%20meetings/2011-Braga/papers/0259.pdf)
- Quantpedia's "Revisiting Trend-following and Mean-reversion Strategies in Bitcoin": "the MIN strategy [buying at short-term lows] is not performing as well as it did in the in-sample analysis. However, the MAX strategy remains very effective." [OOS] — [Quantpedia](https://quantpedia.com/?p=35597)
- A Coinpaprika grid search over RSI settings on 8 majors found only 2 of 88 configurations with a positive in-sample edge versus the benchmark, a mean edge of −4.44 pp, and only 43 out-of-sample signals for the best setting. [IS + small OOS] — [Coinpaprika](https://coinpaprika.com/education/backtest-crypto-strategy)
- SetupAlpha's trend filter plus RSI(2)<30 plus lower Bollinger Band setup on 500+ Binance USDT perps claims a Sharpe of about 2. Results are paywalled, and the OOS split and costs are unverified. [IS / unverified] — [SetupAlpha](https://setup4alpha.substack.com/p/this-is-how-an-algorithmic-crypto-realtest)

### Inferences
- Reversal premia in crypto mostly pay for liquidity provision in illiquid coins, which is the same economics as market making. Retail cannot capture them at Coinbase or Robinhood spreads and fees on a few large coins.
- For BTC and ETH, trend and breakout persistence dominates, so mean-reversion rules on large caps face a momentum headwind.

### Gaps
- No peer-reviewed RSI(2) or Bollinger out-of-sample study on BTC was found. Quantpedia's exact OOS figures (Sharpe, drawdown) could not be fetched.

## DCA variants: plain DCA vs lump sum vs MA-filtered vs MVRV-weighted

### Takeaway
No rigorous, peer-reviewed side-by-side comparison exists. Blog evidence suggests lump sum beats DCA in most BTC entry windows, since BTC drifted up. Simple MA-filtered "buy only below the 200-day" rules usually underperform plain DCA. MVRV-weighting showed only a modest edge (about 60% of rolling 1-year windows) in a self-published study. All of this evidence is in-sample.

### Cited Findings
- Lump sum beat 12-month DCA on about 73% of historical BTC entry dates. [IS, blog] — [SpotedCrypto](https://www.spotedcrypto.com/bitcoin-dca-strategy-guide/)
- DCA beat lump sum for 2018 bear-market entries, while lump sum won for 2020 entries. [IS] — [Coinerblog](https://coinerblog.com/dollar-cost-averaging-crypto/)
- Buying only when BTC is below its 200-day MA beat plain weekly DCA in just 3.9% of rolling 3-year periods. A "hold cash above the MA, catch up later" rule underperformed in nearly every case. [IS, blog] — [FrugalBC Substack](https://frugalbccrypto.substack.com/p/bitcoin-dca-backtest)
- An MVRV-weighted DCA model beat uniform DCA in about 60% of 2,557 rolling 1-year windows (composite score 55%). The author calls the edge modest and names MVRV the best single on-chain timing input. [IS, self-published, unverified code] — [Medium](https://medium.com/@thishan93/can-on-chain-data-actually-improve-bitcoin-dollar-cost-averaging-21cc096d5025)
- BTC fell below its 200-week MA in 2026 for the first time since October 2023. It has historically spent about 90% of the time above it, which makes 200-week-MA "buy zones" rare events. [press] — [CryptoBriefing](https://cryptobriefing.com/bitcoin-below-200-week-moving-average/)

### Inferences
- DCA is a risk and behaviour tool, not an alpha source. Its expected return trails lump sum in a rising asset.
- Valuation-weighted DCA (MVRV or 200-week MA) may add a small edge, but it rests on a few BTC cycles: about 3-4 independent observations, which is a heavy overfitting risk.
- All variants are fully available to US retail on Coinbase, Robinhood and Alpaca, where recurring-buy fees and spreads are the main cost.

### Gaps
- No search results covered value averaging on BTC.
- No out-of-sample or peer-reviewed comparison of MVRV- or MA-weighted DCA was found.

## Why high-win-rate strategies (small targets, wide stops) have negative skew and thin edges

### Takeaway
Expectancy, not win rate, decides profitability. Strategies that take small profits and tolerate large losses (grids, mean reversion with wide stops, short-vol and carry) produce many small wins and rare large losses: negative skew. Costs eat the most from small-target trades.

### Cited Findings
- Expectancy = win rate × average win − loss rate × average loss. A 70% win rate with an average win of 30 and an average loss of 70 has zero expectancy before costs. — [Paragon Signals](https://buttondown.com/Paragon-Signals/archive/a-70-win-rate-that-makes-exactly-0/)
- The break-even win rate is average loss ÷ (average win + average loss). Costs matter most with small targets and short holds. — [MQL5 blog](https://www.mql5.com/ja/blogs/post/775614)
- A 1DTE short-options backtest won 82.57% of 717 trades yet had negative expectancy. Dropping the 10 worst trades flipped it positive, and stops fired disproportionately in high-volatility regimes. [IS] — [jwplatta](https://jwplatta.github.io/posts/distribution-and-regime-effects-in-a-1dte-options-strategy)
- The February 2018 "Volmageddon" short-vol blow-up is the classic example of the many-small-wins, rare-catastrophe distribution. — [Curved Trading](https://curvedtrading.com/articles/en/trading/expected-value-trading-high-win-rate-losing-money/)
- Crypto-specific links:
  - The grid backtest above had an 82.5% win rate and lost money. — [QuantTradingPro](https://quanttradingpro.com/strategy/kbMsMwB8-Grid-Bot-Backtesting)
  - High crypto carry predicts crashes, which is negative skew in carry. — [BIS WP 1087](https://www.bis.org/publ/work1087.htm)

### Inferences
- Grid bots, mean-reversion scalps, Ethena-style carry and basis trades share one return profile: steady small gains, plus jump-to-default or trend losses (October 2025 USDe depeg, 2026 negative funding, range breaks). Reported win rates and smooth equity curves overstate the risk-adjusted edge unless tail events are in the sample.

### Gaps
- No peer-reviewed crypto-specific study quantifying the skew of high-win-rate retail strategies was found. Sources here are mostly practitioner blogs.
