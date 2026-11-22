# Crypto Cross-Sectional Momentum, BTC-Dominance Rotation, and On-Chain Cycle Indicators as Trading Signals

Research date: November 2026. Method note: direct page fetches were blocked in this session (arxiv.org, quantitative.cz, bgeometrics.com, bitcoinmagazine.com failed DNS under the network allowlist), so the findings below come from search-result abstracts and excerpts, not full-text reads. Figures should be checked against the primary PDFs before anyone relies on them. In-sample-only claims are labelled **[IN-SAMPLE]**. Practitioner or blog claims are labelled **[PRACTITIONER]**.

## Q1. Cross-sectional crypto momentum (rank coins by past 1-4 week / 1-3 month return): what do papers find, and do long-only vs long-short, size/liquidity and survivorship matter?

### Takeaway
The headline academic result, Liu, Tsyvinski & Wu (JF 2022), finds strong 1-4 week momentum of about 2.5-4.1%/week long-short **[IN-SAMPLE, roughly 2014-2018]**. Later and more careful work splits sharply. Momentum is concentrated in larger coins, costs eat much of it, much of the alpha sits on the short leg (which a US spot long-only investor cannot trade), and it suffers severe crashes. After correcting for survivorship bias, one study finds no positive momentum-return link at all. The 2025 update by the same author group still reports significant positive momentum on a sample through Sept 2025. The evidence is real but fragile, and it is weakest in exactly the implementable form: long-only, large-cap, net of costs.

### Cited Findings
**Liu, Tsyvinski & Wu (2022), "Common Risk Factors in Cryptocurrency," Journal of Finance 77(2):1133-1177; NBER WP 25882, May 2019**
- A three-factor model (crypto market CMKT, size CSMB, momentum CMOM) explains the excess returns of nine successful zero-investment strategies — [NBER](https://www.nber.org/papers/w25882); [EconPapers JF record](https://econpapers.repec.org/RePEc:bla:jfinan:v:77:y:2022:i:2:p:1133-1177)
- Long-short momentum excess weekly returns: 2.7% (1-week lookback), 3.3% (2-week), 4.1% (3-week), 2.5% (4-week) **[IN-SAMPLE]** — [NBER PDF](https://www.nber.org/papers/w25882.pdf); [Alpha Architect summary](https://alphaarchitect.com/factors-investing-in-cryptocurrency/)
- Size split: below-median-size coins show an insignificant 0.6%/week momentum return, while above-median coins show a significant 4.2%/week. Momentum "performs strongly for the larger coins" (those above $10M market cap) — [NBER WP PDF](https://www.nber.org/system/files/working_papers/w25882/w25882.pdf)
- The authors note that small coins are more illiquid and that "selling is either not possible or limited for most of the coins," which is a short-leg implementability caveat — [NBER WP PDF](https://www.nber.org/system/files/working_papers/w25882/w25882.pdf)
- Earlier Liu & Tsyvinski (NBER 24877, 2018) found strong *time-series* momentum, with momentum and investor-attention proxies as the consistent crypto-specific return drivers — [NBER w24877](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)

**Post-publication update: "Cryptocurrency as an Investable Asset Class: Coming of Age" (arXiv 2510.14435, Oct 2025; search snippets attribute it to Borri, Liu, Tsyvinski & Wu, not verified from full text)**
- On a longer sample to September 2025, including post-2020, a small number of predictors still drive the cross-section. Momentum long-short is significantly positive, while size and value long-short returns are "significantly negative" (sign convention not verified). A value factor is added to make a four-factor model — [arXiv 2510.14435](https://arxiv.org/pdf/2510.14435); [Quantpedia summary](https://quantpedia.com/cryptocurrency-as-an-investable-asset-class-10-lessons/)
- This is the closest thing to an out-of-sample extension of LTW. It comes from the same author group, though, and is not an independent replication.

**Contrary / skeptical evidence**
- Grobys & Sapkota (2019, Economics Letters): 143 coins, monthly data 2014-2018, no significant cross-sectional momentum; monthly results lean toward reversal — [ResearchGate](https://www.researchgate.net/publication/332178134_Cryptocurrencies_and_momentum); [EconPapers](https://econpapers.repec.org/article/eeeecolet/v_3a180_3ay_3a2019_3ai_3ac_3ap_3a6-10.htm)
- Shen et al. (2020): insignificant negative momentum returns over 2013-2019 (as cited in Grobys et al. 2025) — [Springer FMPM](https://link.springer.com/article/10.1007/s11408-025-00474-9)
- Grobys, Kolari, Sandretto, Shahzad & Aijo (2025), "Cryptocurrency momentum has (not) its moments," Financial Markets and Portfolio Management 39(4): a value-weighted momentum portfolio earned about −3.40%/week. The worst 1% of payoffs ran roughly −155% to −297% (long-short, so losses beyond −100% are possible; the exact definition is not verified). Volatility management mitigates crashes, but average returns stay negative. The authors argue the payoff variance may be undefined (heavy tails). Momentum is linked mainly to large caps, and a single coin can distort results. Daily reversals are attributed to the illiquidity of most coins. The remaining coins, a small fraction of market cap, show negative average momentum payoffs — [Springer](https://link.springer.com/article/10.1007/s11408-025-00474-9); [RePEc](https://ideas.repec.org/a/kap/fmktpm/v39y2025i4d10.1007_s11408-025-00474-9.html); [ResearchGate](https://www.researchgate.net/publication/380467146_Cryptocurrency_momentum_has_not_its_moments)
- "Cryptocurrency anomalies and economic constraints" (IRFA 2024): momentum prevails in larger cryptocurrencies but "incurs substantial trading costs and extracts alphas largely from short positions" — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1057521924001509)
- "Cryptocurrency Factor Momentum" (authors not verified): asks whether factor-momentum profits are driven by small, illiquid coins and short-sale constraints. The results change when illiquid coins are excluded before factor construction — [ICM repository](https://open.icm.edu.pl/server/api/core/bitstreams/86a51c47-8cd3-4201-88ee-42f44fb89227/content)

**Supportive with costs**
- A working paper on a top-5% (large-cap) universe reports five long-short portfolios beating the market after transaction costs; the best, a (14-day formation, 5-day holding) portfolio, has Sharpe 1.40 (sample window unclear) — [AUT ACFR working paper](https://acfr.aut.ac.nz/__data/assets/pdf_file/0009/918729/Time_Series_and_Cross_Sectional_Momentum_in_the_Cryptocurrency_Market_with_IA.pdf)
- Fieberg, Liedtke, Poddig, Walker & Zaremba, "A Trend Factor for the Cross-Section of Cryptocurrency Returns," JFQA 60(7):3116-3153 (2025): CTREND, a machine-learning combination of price/volume technical indicators on more than 3,000 coins. It predicts returns, is not subsumed by known factors, is robust across subperiods and market states, "survives transaction costs and persists in big and liquid coins" — [Cambridge/JFQA](https://www.cambridge.org/core/journals/journal-of-financial-and-quantitative-analysis/article/trend-factor-for-the-cross-section-of-cryptocurrency-returns/4C1509ACBA33D5DCAF0AC24379148178); [JFQA PDF](https://jfqa.org/wp-content/uploads/2024/09/24955-trend-factor-cross-section-crypto-returns.pdf)
- Re-examination: "The Cryptocurrency Trend Factor Revisited" (arXiv 2611.01951, Nov 2026). The CTREND advantage holds after a timing correction but "weakens under a more comprehensive one, materially reducing risk-adjusted performance and exposing dependence on the asset universe" — [arXiv 2611.01951](https://arxiv.org/pdf/2611.01951)
- Stop-loss rules and risk-managed momentum have been studied as crash mitigants — [ScienceDirect, stop-loss](https://www.sciencedirect.com/science/article/abs/pii/S2214635023000473); [ScienceDirect, risk-managed momentum, FRL 2025](https://www.sciencedirect.com/science/article/abs/pii/S1544612325011377)

**Survivorship bias**
- Ammann, Burdorf, Liebi & Stöckl (2022), "Survivorship and Delisting Bias in Cryptocurrency Markets": 3,904 coins, 2014-2021, Coin Metrics data. Annualized bias is 0.93% for value-weighted portfolios and 62.19% for equal-weighted ones. The size premium survives but is overstated by about 50% in survivor-only samples. After correction, **momentum and market beta show no positive relation to returns**. A non-trivial share of published crypto anomaly evidence may be an artefact of data truncation — [SSRN 4287573](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4287573); [Stöckl publication page](https://www.sebastianstoeckl.com/publications/wp2022_liebi_survivorship/)

**Practitioner out-of-sample replications [PRACTITIONER, not peer-reviewed]**
- One GitHub backtest reports momentum gross Sharpe of 1.12 before 2023 and −0.68 after 2023. In 2025-2026 out-of-sample testing it found significant gross alpha that was destroyed by turnover at 20 bps cost — [GitHub Gautam-Kanna/crypto-momentum-reversal](https://github.com/Gautam-Kanna/crypto-momentum-reversal)
- Another reports a 2024-2025 out-of-sample Sharpe of 0.41 with t-stat 0.82 (not significant) — [GitHub prams2104/crypto-momentum-backtest](https://github.com/prams2104/crypto-momentum-backtest)
- A Substack post: "Crypto momentum has beautiful returns and catastrophic crashes" — [tommijohnsen Substack](https://tommijohnsen.substack.com/p/crypto-momentum-has-beautiful-returns)

### Inferences
- The LTW 2.5-4.1%/week figures come from a 2014-2018 sample with heavy small/mid-cap weight, and they are gross, long-short returns. They are not a realistic expectation for a long-only top-20 spot portfolio.
- Two strands disagree. Value-weighted, survivorship-corrected and crash-aware studies (Ammann et al.; Grobys et al. 2025) find weak or negative momentum. The LTW group's own 2025 extension still finds positive momentum. A neutral reading: momentum exists, has fat-tailed crash risk, depends on universe construction, and its net long-only premium is unproven.
- Because the alpha sits largely on the short side, a US spot account (no shorting) captures at most the long leg. In crypto that long leg is heavily correlated with simple market beta and trend.
- Weekly rebalancing of a top-N sort produces high turnover, so at 10-50 bps per side, costs are first-order.

### Gaps
- I could not find an independent, explicitly out-of-sample *long-only* large-cap momentum study with net returns, drawdowns and turnover for 2022-2026.
- I could not retrieve Borri et al. 2025 Table 2 Panel B (post-2020 subsample magnitudes).
- No confirmed turnover or win-rate figures for academic momentum portfolios.
- The Dobrynskaya paper's exact return figures were not retrieved; see Q2.

## Q2. Short-term reversal vs momentum horizons in crypto

### Takeaway
The broad pattern: momentum up to about 2-4 weeks, then reversal beyond about one month, a much faster switch than in equities. Daily and weekly reversal is concentrated in small, illiquid coins, while momentum lives in the large caps.

### Cited Findings
- Dobrynskaya (2023, Journal of Alternative Investments): about 2,000 of the largest coins, 2014-2020. Momentum appears at horizons up to 2-4 weeks and reversal beyond one month, and the reversal strengthens as formation and holding periods lengthen. The switch happens after about one month, much faster than in equities — [HSE conference PDF](https://conference.hse.ru/files/download_file_ex?hash=FAE0AB2DC7A67656E89A0B1CB27D8C7D&id=3B5EE9A5-0B18-458A-9458-B4ED0F6C6664); [ResearchGate](https://www.researchgate.net/publication/369536471_Cryptocurrency_Momentum_and_Reversal)
- Grobys & Sapkota (2019): monthly data show reversal rather than momentum — [ResearchGate](https://www.researchgate.net/publication/332178134_Cryptocurrencies_and_momentum)
- Grobys et al. (2025): daily reversals stem from the illiquidity of most traded coins — [Springer](https://link.springer.com/article/10.1007/s11408-025-00474-9)
- Quantpedia summary of the research: reversal tends to appear in the smallest cryptos and momentum in the largest — [Quantpedia: Trend-following and Mean-reversion in Bitcoin](https://quantpedia.com/trend-following-and-mean-reversion-in-bitcoin/)
- Fičura, "Impact of size and volume on cryptocurrency momentum and reversal" (2023) studies size and volume conditioning of both effects (full text not retrieved) — [quantitative.cz PDF](https://quantitative.cz/wp-content/uploads/2023/09/impact_of_size_and_volume_on_cryptocurrency_momentum_and_reversal.pdf)
- "Up or down? Short-term reversal, momentum, and liquidity effects in cryptocurrency markets" (IRFA 2021) covers the same horizon and liquidity interaction (details not retrieved) — [ResearchGate](https://www.researchgate.net/publication/354881251_Up_or_down_Short-term_reversal_momentum_and_liquidity_effects_in_cryptocurrency_markets)
- A Quantpedia Premium weekly-rebalanced crypto strategy reports an indicative 80.3% return with 61.33% volatility on a 2020-2026 backtest. Short-term reversal is reported significant at 1%, with Sharpe up to 1.69 (paywalled, unverified) **[PRACTITIONER/IN-SAMPLE]** — [Quantpedia Premium Update](https://vvv.quantpedia.com/quantpedia-premium-update-july-30th/)

### Inferences
- In large caps, a 1-4 week lookback with 1-week hold sits in the momentum zone, and 1-3 month lookbacks drift toward reversal. That conflicts with the equity-style 12-1 month rule.
- Reversal profits in small coins are probably hard to harvest given spreads, illiquidity and the absence of shorting.

### Gaps
- No net-of-cost reversal results for liquid coins on US-accessible venues were found.

## Q3. BTC dominance / ETH-BTC / alt-season rotation

### Takeaway
I found no rigorous, peer-reviewed or reproducible backtest of a BTC-dominance rotation rule. The evidence is anecdotal and practitioner material with inconsistent thresholds and only 3-4 cycles to learn from, so overfitting risk is extreme.

### Cited Findings
- The Ledger Mind claims a dominance-based strategy captured 70%+ of alt-season gains and avoided 60%+ of bear losses, "backtested on 2017-2021 data." It also claims an ETH/BTC leading rule entered alt seasons 2-4 weeks early. Its rules include profit-taking when BTC.D < 45%. There are no trade logs, costs or holdout **[PRACTITIONER, IN-SAMPLE, unverified]** — [The Ledger Mind](https://theledgermind.com/altcoin-season-vs/)
- Thresholds vary across sources: below 50% and ideally near 40%; a sustained break below 54%; or below 55% — [Nexo](https://nexo.com/blog/bitcoin-dominance-altcoin-season-signals); [Phemex](https://phemex.com/blogs/bitcoin-dominance-altcoin-season); [SpotedCrypto](https://www.spotedcrypto.com/btc-dominance-altcoin-season/)
- Bybit x Block Scholes quarterly report on alt season and Bitcoin's evolving role. Alt seasons historically came about 230 days after the halving, with a 2-6 month lag after the three major dominance peaks since 2019 — [Block Scholes](https://www.blockscholes.com/research/bybit-x-block-scholes-quarterly-report-altcoin-season-and-the-evolving-role-of-bitcoin)
- 2026 pages describe BTC dominance around 56-60% and an Altcoin Season Index near 30-40, meaning no broad alt season fired in the 2024-2026 cycle (page dates inconsistent) — [Bitcoin Foundation page, Oct 2026](https://bitcoinfoundation.org/news/altcoins/understanding-altcoin-season-in-2026-what-are-altcoin-market-cycles/); [BlockEden forum](https://blockeden.xyz/forum/t/altcoin-season-index-at-40-my-strategy-for-the-coming-rotation/237)

### Inferences
- With dominance staying high through the 2024-2025 bull run and the 2026 drawdown, a "hold BTC while dominance rises" rule would have kept investors mostly in BTC, which was the better choice. An alts-on-falling-dominance rule would rarely have triggered, or would have produced whipsaws.
- Dominance is distorted by stablecoin growth (stablecoins count in total market cap) and by new-token issuance. That makes long-history comparability questionable.

### Gaps
- I found no source documenting a clean, free historical BTC.D series and its construction (CoinMarketCap/TradingView CRYPTOCAP:BTC.D are commonly used, but this was not verified here).
- No out-of-sample or net-of-cost dominance-rotation study exists in the sources I found.

## Q4. On-chain cycle indicators (MVRV Z-score, NUPL, Puell, Pi Cycle, 200WMA, realized price, S2F): predictive power and 2024-2026 performance

### Takeaway
I found no academic out-of-sample test of MVRV, NUPL or Puell as return predictors. The evidence is descriptive and from vendors. The classic top thresholds, calibrated on 2013/2017/2021, failed in the 2025 cycle: MVRV-Z peaked far below 7, NUPL never sustained above 0.75, and Pi Cycle never crossed at the October 2025 top (about $124-126k). Stock-to-flow was falsified in 2021-2022. Bottom-side anchors (200WMA, realized price) were breached again in 2026: as of 21-22 Nov 2026, BTC trades about $55-58k, below the 200WMA (about $68k) and near or around realized price (about $54k). Overfitting on 3-4 cycles is the central concern.

### Cited Findings
**2025 top: signals did not fire [PRACTITIONER sources]**
- At the October 2025 peak the MVRV Z-Score was about 2.5. The cycle's highest reading was about 3.4 in December 2024, versus 7+ at earlier tops — [BGeometrics, Oct 2026](https://bgeometrics.com/blog/2026-10-mvrv-z-score-explained/) (via search excerpt)
- A separate reconstruction puts the MVRV-Z in neutral territory on the day of the top — [NodeWitness FAQ](https://nodewitness.com/en/faq/)
- During October 2025 the Z-Score stayed clear of the red zone, NUPL never sustained readings above 0.75, and Pi Cycle never crossed. Fixed thresholds were calibrated before ETF and treasury-company demand — [bit.com](https://www.bit.com/knowledge-hub/mvrv-explained)
- Bitcoin Magazine, "Why Bitcoin Price Top Indicators Failed This Cycle," attributes the failure to compressed volatility and a larger market base, and suggests recalibrating Z-score on a shorter rolling window — [Bitcoin Magazine](https://bitcoinmagazine.com/markets/why-bitcoin-price-top-indicators-failed)
- Pi Cycle (111DMA crossing 2×350DMA) flagged the 2013 and 2017 tops within days and the April 2021 top (cross about 12 April; peak 14 April at about $63-65k). It **missed** the higher Nov 2021 peak (about $69k, 10 Nov 2021), where the ratio "barely touched 1." It did not fire in 2024-2025 — [Samara AG](https://www.samara-ag.com/market-insights/bitcoin-pi-cycle-top-indicator); [Coldhardsats](https://coldhardsats.com/indicators); [TradingView Pi Cycle ideas](https://www.tradingview.com/ideas/picycletop); [Blockchain.com chart](https://www.blockchain.com/en/explorer/charts/pi-cycle-top-indicator)
- So Pi Cycle's record is 3 hits (2013, 2017, April 2021), 1 partial (the April 2021 signal came before a higher high) and 1 total miss (2025). That is a tiny sample.

**Stock-to-flow**
- PlanB's S2F projected about $98k (Nov 2021) and $135k (Dec 2021). BTC closed 2021 below $100k. On 18 June 2022 BTC hit about $17.6k, breaching S2F's lower band for the first time. Vitalik Buterin: "Stock-to-flow is really not looking good now." PlanB maintained the model was "intact" — [FXStreet](https://fxstreet.com/cryptocurrencies/news/bitcoin-stock-to-flow-model-invalidated-as-btc-closes-2021-below-100-000-202201010939); [Cointelegraph](https://cointelegraph.com/news/stock-to-flow-model-possibly-invalidated-as-bitcoin-price-loses-30k); [CryptoSlate](https://cryptoslate.com/planbs-stock-to-flow-model-off-by-130k-bitcoin-trades-below-trend-since-2021/)
- Critics argue S2F ignores demand, so it is a supply-only model — [Cointelegraph opinion](https://cointelegraph.com/opinion/three-reasons-why-planb-s-stock-to-flow-model-is-not-reliable)

**2026 bear: bottom indicators (as of Nov 2026)**
- June 2026: BTC touched its 200WMA at about $61.3k, and more than half of supply was in unrealized loss ("supply in loss overtakes profit," described as a hallmark of past bottoms) — [CoinDesk, 4 Jun 2026](https://www.coindesk.com/markets/2026/06/04/this-bitcoin-metric-has-marked-every-bear-market-bottom-and-it-s-just-flashed-again)
- July 2026: a thesis that about $58k on 1 July 2026 could be the bear low (described as unconfirmed) — [CoinJuice](https://coinjuice.com/research-hub/bitcoin-bear-market-bottom-july-2026)
- Nov 2026: BTC at about $57.8k, below a 200WMA of about $68k, after a 204-day death cross. Another report says BTC hit $55k on 21 Nov 2026, a two-year low and the second break below the 200WMA this cycle — [Yahoo Finance](https://finance.yahoo.com/markets/crypto/articles/bitcoin-breaks-200-week-sma-143215312.html); [World Today News](https://world-today-news.com/bitcoin-dropped-to-55000-on-november-21-2026-marking-its-lowest-valuation-in-over-two-years)
- Realized price is about $53.6-54k, per Fidelity-cited data. The MVRV Z-Score is trending toward undervalued but, per that report, has not reached prior cycle-bottom levels. One aggregator reading of about 0.22-0.27 is low-confidence — [Coinpedia](https://coinpedia.org/news/bitcoin-bear-market-bottom-2026-is-60000-the-floor-or-is-october-the-real-low/); [KuCoin news](https://www.kucoin.com/news/flash/bitcoin-metrics-and-halving-calendar-suggest-bottom-not-yet-confirmed); [Amberdata](https://blog.amberdata.io/onchain-valuation-what-bitcoins-realized-price-says-about-2026)
- Historically BTC traded below realized price in every major bear, and the long-term anchors have been breached only during outright capitulation — [21Shares](https://www.21shares.com/en-eu/insights/bitcoin-cycle-bottom-2026-entry-point); [SpotedCrypto](https://www.spotedcrypto.com/bitcoin-200wma-bear-bottom-signal-2026/)
- Vendor research (Fidelity Digital Assets Signals Reports) gives qualitative positive/neutral/negative labels per metric (MVRV, Puell and others) with no backtest statistics — [Fidelity Q3 2024](https://www.fidelitydigitalassets.com/sites/g/files/djuvja3256/files/acquiadam/FDA%20Q3%202024%20Signals%20Report.pdf); [Fidelity Q2 2025](https://www.fidelitydigitalassets.com/sites/g/files/djuvja3256/files/acquiadam/FDA_US_UK_Q2_2025_SignalsReport_1213721.2.0.pdf)
- 21Shares newsletter on whether the cycle had peaked (2025) — [21Shares #256](https://www.21shares.com/en-us/research/newsletter-issue-256)
- Academic lead: a 2026 arXiv survey of Bitcoin price prediction keeps only studies with explicit out-of-sample evaluation. Whether it covers on-chain valuation ratios was not verified — [arXiv 2606.00071](https://arxiv.org/pdf/2606.00071)

### Inferences
- Top signals using fixed thresholds look like products of fitting 2-3 data points. In 2025 they would have kept a holder fully invested through the top and into a roughly 55% drawdown (about $126k to about $55k). Each new cycle has shown lower peak readings (diminishing amplitude), so the thresholds keep drifting.
- Bottom-zone indicators (price at or below realized price, MVRV-Z near 0 or below, 200WMA) have historically marked good multi-year *accumulation zones*, but not precise lows: the 200WMA broke in 2022 and again in 2026. As a slow-moving DCA or allocation tilt they are more defensible than as timing triggers.
- Out of only about 4 BTC cycles, any multi-parameter cycle-indicator model is heavily overfit by construction.

### Gaps
- I found no peer-reviewed out-of-sample predictive-regression test of MVRV, NUPL or Puell.
- No Puell Multiple-specific reading at the 2025 top was found.
- No Glassnode, CryptoQuant or Checkonchain primary posts were retrieved (fetches blocked). The exact 2025 peak date and price varies by source ($124-126k, early Oct 2025).
- Whether the 2026 bear has bottomed is unknown as of 22 Nov 2026.

## Q5. Relative-strength rotation between BTC, ETH and cash (dual-momentum style)

### Takeaway
Only practitioner backtests exist. They suggest the absolute-momentum (cash) filter does most of the drawdown work, but a 4-week BTC/ETH/cash rotation still had roughly an −86% max drawdown, about the same as buy-and-hold. No peer-reviewed or live record was found.

### Cited Findings
- FinzData: each week, hold whichever of BTC or ETH has the higher 4-week return, or cash if both are negative. 2017-2026: about 43%/yr, slightly above an unspecified benchmark. Max drawdown about −86% versus about −87% for the benchmark **[PRACTITIONER, IN-SAMPLE, costs unspecified]** — [FinzData](https://data.finzdata.com/s/bitcoin-vs-ether-dual-momentum-4-week-cash-when-both-fall-32cfb7)
- Valuelytica BTC/gold/cash rotation: max drawdown 18%, Calmar 1.03. A GQResearch replication found the "BTC" series was actually GBTC, whose premium/discount cushioned the worst drawdown by about 7 percentage points. Spot BTC had an 86% drawdown in the same window. Deleting the relative-momentum ranking *improved* results, while removing the cash switch doubled drawdown — [Valuelytica](https://valuelytica.substack.com/p/golden-dual-momentum-rotation); [GQResearch, "Dual Momentum Without the Dual"](https://gqresearch.substack.com/p/dual-momentum-without-the-dual)
- Freqtrade dual-momentum on crypto futures: +117% over 4 years in backtest, max drawdown about 19%, walk-forward validated. The author says the roughly 90-day forward dry-run is "nowhere near enough" to confirm — [Backtests Not Signals](https://backtestsnotsignals.substack.com/p/117-in-4-years-dual-momentum-on-crypto); [Week 42 update](https://backtestsnotsignals.substack.com/p/freqtrade-dual-and-reversion-portfolio-465)
- An equity counterexample: an absolute-momentum gate on stock/ETF rotation worsened max drawdown (−33.4% to −35.7%) and nearly halved CAGR — [chat2invest](https://www.chat2invest.com/research/dual-momentum-absolute-gate)

### Inferences
- BTC and ETH are highly correlated, so the relative leg adds little. Any value comes from the time-series trend/cash filter, which links to the separate trend-following literature (covered by other researchers).
- Short lookbacks (4 weeks) do not avoid crash drawdowns. Drawdown control likely needs longer trend filters or volatility targeting.

### Gaps
- No live or audited track record of BTC/ETH/cash rotation was found.
- No turnover or cost-sensitivity numbers were found for these specific rules.

## Q6. Costs, capacity, and long-only spot implementation (US brokers)

### Takeaway
On US retail spot venues, shorting is unavailable and coin lists are small, about 20 coins on Alpaca. The short-leg-dependent, small-coin-dependent academic momentum premia therefore largely can't be harvested. Only a long-only, large-cap version is feasible, and that is the version with the weakest evidence.

### Cited Findings
- Alpaca crypto spot: crypto cannot be sold short or bought on margin. Order types are market, limit and stop-limit (gtc/ioc). The per-trade fee is volume- and order-type-dependent, posted end of day — [Alpaca Crypto Spot Trading docs](https://docs.alpaca.markets/docs/crypto-trading); [Alpaca crypto fees](https://docs.alpaca.markets/docs/crypto-fees)
- Alpaca USD-pair coins on one support page: AAVE, AVAX, BAT, BCH, BTC, CRV, DOGE, DOT, ETH, GRT, LINK, LTC, MKR, SHIB, SUSHI, UNI, USDC, USDT, XTZ, YFI. Other pages cite about 20 coins and 56 pairs (the list may be outdated; the live asset API is authoritative) — [Alpaca supported coin pairs](https://alpaca.markets/support/what-are-the-supported-coins-pairs)
- The academic momentum alpha comes "largely from short positions" with "substantial trading costs" — [ScienceDirect IRFA 2024](https://www.sciencedirect.com/science/article/abs/pii/S1057521924001509)
- LTW: shorting is impossible or limited for most coins — [NBER WP PDF](https://www.nber.org/system/files/working_papers/w25882/w25882.pdf)
- At 20 bps per trade, a practitioner weekly momentum strategy's gross alpha was destroyed by turnover [PRACTITIONER] — [GitHub](https://github.com/Gautam-Kanna/crypto-momentum-reversal)
- Survivorship: equal-weighted crypto backtests are inflated by about 62%/yr versus about 0.9%/yr value-weighted — [SSRN 4287573](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4287573)

### Inferences
- A realistic US long-only implementation has a universe of about 15-20 liquid coins, value- or volatility-weighted, rebalanced weekly or slower. It should be benchmarked against BTC buy-and-hold and a simple BTC trend filter. Expect most of its return to be market beta.
- Capacity is not a binding constraint for a retail account in BTC/ETH/SOL-class coins. It binds quickly in the small-coin tail where the academic premia sit.

### Gaps
- No exact current Alpaca or Coinbase fee tiers were retrieved (Alpaca and Coinbase Advanced taker fees are commonly cited in the tens of bps for low volume, but this was not verified here).
- No Coinbase asset-list or shorting documentation was retrieved.
- No Kaiko or CoinMetrics spread/slippage figures by coin were found.
