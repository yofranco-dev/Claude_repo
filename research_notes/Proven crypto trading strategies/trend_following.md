# Trend-Following / Time-Series Momentum in Bitcoin and Crypto (Breakouts, MA Filters, Vol Targeting)

Research method note (Nov 2026): Direct page fetches failed for papers.ssrn.com, ar5iv.labs.arxiv.org, cxoadvisory.com and research.grayscale.com, because those hosts are not on this session's network allowlist. Most figures below therefore come from search-engine excerpts of the primary sources (abstracts, the top of PDFs, and summary pages). Each figure is labelled with its evidence type: IS = in-sample backtest; OOS = out-of-sample or walk-forward; REPL = independent replication; BLOG = non-peer-reviewed or retail backtest. Treat exact decimals as "check against the PDF" wherever this is flagged.

## 1. Academic evidence on time-series momentum (TSMOM) in crypto, and which lookbacks work

### Takeaway
Peer-reviewed and NBER work consistently finds positive time-series momentum in BTC and crypto at short horizons: weekly returns predict the next 1-4 weeks, and 4-week momentum carries a factor premium. Moving-average rules of roughly 5-100 days add predictive power in and out of sample. Data-snooping-corrected tests (Hudson & Urquhart) still find many rules profitable, but one key caveat stands out: OOS predictability for Bitcoin itself has weakened, even where it persists in other coins. Lookbacks of 1-4 weeks up to about 2-3 months are where most academic evidence sits. Longer lookbacks (100-360 days) look more robust in the recent era (post-2021).

### Cited Findings
- Liu & Tsyvinski, "Risks and Returns of Cryptocurrency" (NBER w24877, 2018; later Review of Financial Studies 2021). They document a "strong time-series momentum effect". A positive current weekly BTC return "positively and statistically significantly predicts 1-week, 2-week, 3-week, and 4-week ahead returns". Investor-attention proxies also forecast returns. — [NBER w24877](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf); [NBER abstract](https://www.nber.org/papers/w24877)
- The same paper's robustness checks: the momentum effect shrinks somewhat when restricted to post-2013 data but stays significant. An OOS test that sets quintile cutoffs on the first two years still finds a strong momentum effect (OOS within the 2011-2018 sample). — [NBER w24877](https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)
- Liu, Tsyvinski & Wu, "Common Risk Factors in Cryptocurrency" (NBER w25882, 2019; later Journal of Finance 2022): 4-week momentum factors generate statistically significant long-short returns. Note that this is a cross-sectional factor result, not pure TSMOM. — [NBER w25882](https://www.nber.org/system/files/working_papers/w25882/w25882.pdf)
- Later work attributes crypto TSMOM to underreaction: coins with low attention (measured by Google search data) show stronger TSMOM. — [AUT ACFR paper, Time-Series and Cross-Sectional Momentum in the Cryptocurrency Market](https://acfr.aut.ac.nz/__data/assets/pdf_file/0009/918729/Time_Series_and_Cross_Sectional_Momentum_in_the_Cryptocurrency_Market_with_IA.pdf)
- Detzel, Liu, Strauss, Zhou & Zhu, "Learning and predictability via technical analysis: Evidence from bitcoin and stocks with hard-to-value fundamentals" (Financial Management 50(1), 2021, pp. 107-137; working-paper version Jan 2018 titled "Bitcoin: Predictability and Profitability via Technical Analysis"). They use ratios of price to 5-, 10-, 20-, 50- and 100-day moving averages. Strategies based on these ratios "generate an economically significant alpha and Sharpe ratio gains relative to buy-and-hold", and the predictive power holds in and out of sample. Their equilibrium model has TA arising from rational learning when fundamentals are hard to value. — [EconPapers/RePEc](https://econpapers.repec.org/RePEc:bla:finmgt:v:50:y:2021:i:1:p:107-137); [WUSTL profile](https://profiles.wustl.edu/en/publications/learning-and-predictability-via-technical-analysis-evidence-from-/)
- A CXO Advisory summary of this research gives a BTC buy-and-hold benchmark over the sample: annualised excess return 224%, volatility 111%, Sharpe 2.0, max drawdown -89.5%. This is a secondary summary and the sample ends around 2017-2018, so the exact figures are unverified. — [CXO Advisory (search excerpt)](https://www.cxoadvisory.com/?p=30879)
- Grobys, Ahmed & Sapkota, "Technical trading rules in the cryptocurrency market" (Finance Research Letters, 2020). The authors test variable moving-average rules of 20, 50, 100, 150 and 200 days on the 11 most-traded coins, 2016-2018. The 20-day rule worked best, with an excess return of 8.76% p.a. excluding Bitcoin. The implication is that BTC itself was harder to beat, while altcoins carried the edge. — [Univ. Vaasa repository PDF](https://osuva.uwasa.fi/bitstream/10024/11192/2/Osuva_%20Grobys_Ahmed_Sapkota_2020.pdf)
- Hudson & Urquhart, "Technical trading and cryptocurrencies" (Annals of Operations Research, 2019/2021). They test 14,919 rules (about 15,000) across 5 rule families on two BTC markets and three other coins. They find significant predictability and profitability in every class and coin. Risk-adjusted returns are "substantially higher" than buy-and-hold, "with protection against lengthy and severe drawdowns". A large share of rules survive multiple-hypothesis (data-snooping) corrections. Break-even costs are well above actual crypto costs. Caveat: one source reports no predictability for Bitcoin in the OOS period, although predictability remains in other cryptos. — [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1); [Reading open access](https://centaur.reading.ac.uk/85715)
- Corbet, Eraslan, Lucey & Sensoy (Finance Research Letters 31, 2019) use high-frequency BTC data. The variable-length MA rule performs best, and buy signals earn more than sell signals. — [IDEAS/RePEc](https://ideas.repec.org/a/eee/finlet/v31y2019icp32-37.html)
- Rozario, Holt, West & Ng, "A Decade of Evidence of Trend Following Investing in Cryptocurrencies" (arXiv 2009.12155 / SSRN 3697981, Sept 2020). They test SMA, EMA and double-EMA trend rules and report 255% annualised walk-forward returns (OOS walk-forward, 2011-2019 data dominated by early BTC). They find returns "reasonably robust" to the trend method and parameters, with commodity-like risk-adjusted returns and bear-market diversification versus equities. Their code is public (GitHub Globe-Research/bittrends). A secondary summary puts Sharpe at about 0.5-1.5, unverified. This paper assumed negligible fees, spread, slippage and market impact. — [arXiv abstract](https://arxiv.org/abs/2009.12155); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3697981); [Quantpedia search summary noting the cost assumption](https://arxiv.org/pdf/2009.12155)
- Le & Ruthbah (Monash Centre for Financial Studies), "Trend-following Strategies for Crypto Investors". TSMOM with shorter lookbacks gives a high Sharpe, but frequent rebalancing costs erode profits. Drawdown-controlled variants (30% risk exposure, short lookbacks) give a higher Sharpe and lower drawdown than buy-and-hold. The suggested lookbacks are 65 days for BTC and 20 days for ETH and the S&P. The strategies still worked after transaction costs. The exact tables were not retrieved. — [Monash PDF](https://www.monash.edu/__data/assets/pdf_file/0011/3744821/Trend-following-Strategies-for-Crypto-Investors.pdf); [Monash project page](https://www.monash.edu/business/mcfs/our-research/all-projects/investment-strategy/trend-following-strategies-for-crypto-investors)
- Shen, Urquhart & Wang, "Bitcoin intraday time-series momentum" (Financial Review, accepted 2021): the first half-hour return predicts the last half-hour. The best configuration has a Sharpe of about 1.15, with an OOS evaluation. — [Reading accepted version](https://centaur.reading.ac.uk/100181/3/21Sep2021Bitcoin%20Intraday%20Time-Series%20Momentum.R2.pdf)
- Huang, Sangiorgi & Urquhart, "Cryptocurrency Volume-Weighted Time Series Momentum" (SSRN 4825389, 2024): annualised Sharpe of 2.17. Whether this is OOS is not stated in the excerpt, so treat it as IS. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4825389)
- Howden & Andreev, "Risk-Managed Time-Series Momentum in Crypto Majors: Crash-State De-Risking and Drawdown Control" (SSRN 7115459, 2026). This is an OOS walk-forward test with the lookback fixed at 30 days. Net of 25 bps, Sharpe is 1.41 versus 0.70 for buy-and-hold, and a drawdown overlay lifts it to about 1.53. The authors explicitly address multiple testing and backtest overfitting. It is a recent working paper, not peer-reviewed. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7115459)
- A Polish "Cryptocurrency Factor Momentum" paper reports a TS-winner portfolio Sharpe of 1.16 from July 2018 onward. — [ICM open repository](https://open.icm.edu.pl/server/api/core/bitstreams/86a51c47-8cd3-4201-88ee-42f44fb89227/content)
- "AdaptiveTrend" (arXiv 2602.11708, Feb 2026) claims an OOS Sharpe of 2.41 over 2022-2024 across more than 150 pairs. This is a complex adaptive framework, not plain TSMOM, so treat it with caution. — [arXiv](https://arxiv.org/html/2602.11708v1)

### Inferences
- The strongest, most-replicated horizon is short to medium: 1-4 weeks (Liu-Tsyvinski) up to about 20-65 days (Grobys, Le-Ruthbah, Howden's 30-day). Longer windows (100-360 days) are more robust recently (see section 6).
- Altcoins appear to show more trend-rule profitability than BTC in several studies (Grobys excluding BTC; Hudson-Urquhart finding no BTC OOS predictability). This supports multi-coin trend portfolios over BTC-only.
- Sharpe numbers above about 2 come from IS or complex methods. Credible OOS, net-of-cost Sharpe ratios for simple rules cluster around 1.0-1.5.

### Gaps
- The exact Sharpe, max drawdown and CAGR tables from Detzel et al., Le & Ruthbah, and Rozario et al. could not be retrieved, because fetches were blocked.
- No AQR or Man Group paper dedicated specifically to crypto trend was found. Man's 2025 material is generic managed futures.
- The post-publication performance of the Liu-Tsyvinski 1-4 week signal (2019-2026) was not found in any formal replication. One GitHub research log reported weak 1-4 week momentum for BTC, ETH and XRP, but it is not citable as research ([GitHub PR](https://github.com/seungjae3908-source/seungjae20260713/pull/1499)).

## 2. Donchian / Turtle-style breakouts on BTC, ETH and baskets

### Takeaway
The best-documented breakout evidence is Zarattini, Pagani & Barbon (2025). It uses an ensemble of Donchian channels (lookbacks of 5-360 days) on a rotating, survivorship-bias-free top-20 coin universe, with 25% vol targeting. Results after fees: Sharpe above 1.5 and about 10.8% annualised alpha versus BTC (Jan 2015 to Mar 2025). Retail and blog Donchian backtests on BTC report profit factors of about 1.4-2.2 and win rates of about 35-50%. No live-fund track record of a pure Donchian crypto strategy was found.

### Cited Findings
- Zarattini, Pagani & Barbon, "Catching Crypto Trends; A Tactical Approach for Bitcoin and Altcoins" (SSRN 5209907; Swiss Finance Institute RP 25-80; 2025). The system aggregates multiple Donchian-channel trend models with different lookbacks into one signal, plus volatility-based sizing. On the top-20 rotational portfolio it achieves a Sharpe above 1.5 and 10.8% annualised alpha versus BTC, after fees. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5209907); [Concretum Group summary](https://concretumgroup.com/catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins/); [Barbon site](https://abarbon.com/papers/catching-crypto-trends); [RePEc](https://ideas.repec.org/p/chf/rpseri/rp2580.html)
- Implementation details from the summaries:
  - The base version is a daily ensemble over 5- to 360-day lookbacks, equally weighted.
  - Each open position is resized daily to a 25% annualised vol target, with leverage capped at 200%.
  - The universe is up to 20 liquid coins, rebalanced monthly.
  - The data are survivorship-bias-free, covering 21,616 crypto assets from Jan 2010 to mid-March 2025.
  - On one configuration CXO reports 18% net CAGR and 11% annualised net alpha versus BTC buy-and-hold (Jan 2015 to mid-Mar 2025), assuming 0.10% costs.
  - QuantifiedStrategies reports a "Combo" ensemble with 30% CAGR and Sharpe 1.58.
  - Sharpe is stable at about 1.5 across portfolio sizes.
  - The CAGR figures conflict (18% vs 30%), probably because they come from different configurations.
  - — [CXO Advisory](https://www.cxoadvisory.com/technical-trading/crypto-asset-trend-following-strategies/); [QuantifiedStrategies](https://www.quantifiedstrategies.com/?p=1192563)
- Decay finding in the same paper: long trends "remain statistically robust, but shorter trends have weakened in the recent era". — [Concretum/CXO summaries (search excerpt)](https://concretumgroup.com/catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins/)
- Independent replication (REPL, unverified GitHub project): 20.5% CAGR, Sharpe 1.21, max drawdown -20% at a 50% vol target, with "realistic costs". It confirms the Sharpe roughly but at a lower level than the paper. — [GitHub issue](https://github.com/zebadee2kk/DeFi-TraderStack-Agent/issues/137)
- BLOG results:
  - A BTC H4 Donchian system with EMA, ADX and ATR filters (Jan 2018 to Apr 2026) reports profit factor 2.16, win rate 48.6%, 146 trades (about 18 per year) and max balance drawdown 7.5%. — [MQL5 blog](https://www.mql5.com/en/blogs/post/770303)
  - A BTC "channel breakout" with dual trend confirmation (2018-2026) reports profit factor 1.40, win rate 69% and 353 trades, with a 13% drawdown. The high win rate is atypical for breakouts. — [MQL5 blog](https://www.mql5.com/en/blogs/post/770863)
  - A BNB/USDT Donchian breakout reports profit factor 1.58 and win rate 49.6%. — [DEV.to](https://dev.to/howiprompt/how-our-ai-agents-evolved-donchianbreak-on-bnbusdt-to-163-backtested-1-evolutions-511g)
  - Classic Donchian on ETFs (not crypto), for reference: win rate 51%, profit factor 2.7, 78 trades. — [QuantifiedStrategies Substack](https://quantifiedstrategies.substack.com/p/donchian-breakout-strategy)
  - Educational sources describe breakout win rates of about 30-40%, offset by large winners. They also warn that a long BTC uptrend punctuated by two crashes flatters 2017-2024 breakout backtests. — [Search excerpt summarising educational breakout pages, e.g. TradingView scripts](https://www.tradingview.com/script/YVaGAcV3)

### Inferences
- The ensemble-of-lookbacks approach (rather than one Turtle 20/55-day channel) plus vol sizing is the version with the strongest documented, survivorship-bias-free, net-of-fee evidence. However, it is still a backtest by the authors, and the paper was published in 2025, so there is almost no post-publication period yet.
- Win rate and payoff ratio for daily breakout systems on crypto: expect a 35-50% win rate with payoff ratios above 2. Blog systems with heavy filters push the win rate higher and the trade count lower.

### Gaps
- No peer-reviewed paper gives Turtle-rule (20/55-day, 2N stop) win-rate and payoff statistics on BTC or ETH.
- No live fund running a disclosed Donchian crypto strategy with audited returns was found.
- The max drawdown of the Zarattini top-20 portfolio was not retrieved.

## 3. Moving-average filters on BTC (price above 200D; 50/200; 20/100; 50D)

### Takeaway
Across many independent backtests, a long/cash MA filter on BTC reliably cuts maximum drawdown, typically by 13-27 percentage points (for example, from -77/-83% to -64/-70%) for single-asset daily rules. The CAGR outcome versus buy-and-hold is start-date dependent: often slightly lower over 2015/2016 to 2026, and slightly higher on 2018 to 2026. Shorter crossovers (short MA of about 10-30 days) gave the highest Sharpe in Grayscale's 2023 study. Combined with vol targeting, the drawdown reduction becomes far larger.

### Cited Findings
- Grayscale Research, "The Trend is Your Friend: Managing Bitcoin's Volatility with Momentum Signals" (updated 8/9/2023). It tests a 50-day MA filter and crossovers, including 20-day vs 100-day, long or cash only (no shorting). For crossovers, the highest Sharpe ratios occur with the short MA at about 10-30 days. Moving to cash below an MA may reduce drawdowns. Shorter MAs generate more signals and higher costs. The exhibit figures were not retrieved. — [Grayscale Research](https://research.grayscale.com/reports/the-trend-is-your-friend-managing-bitcoins-volatility-with-momentum-signals)
- An 11-year BTC study (BLOG): the 200D filter cut the worst drawdown from about 83% to 70% but returned 61.2% per year against 63.9% for buy-and-hold. Across MA lengths, the trend filter took 13-27 points off the worst fall. — [tradermarkus.com](https://tradermarkus.com/bitcoin-200-day-moving-average/)
- BTC 200D, 2018-2026 (BLOG): 26.1% CAGR versus 24.8% for buy-and-hold, with max drawdown -64.1% versus -76.6% (total return 548% vs 496%). — [boringedge.com](https://boringedge.com/bitcoin-200-day-moving-average-strategy-backtest/)
- Longer-record runs (BLOG, data to 13 Nov 2026):
  - 2016-2026 MA strategy: 56.03% per year, Sharpe 1.07, max drawdown -69.8%, versus buy-and-hold at 60.48% and Sharpe 1.04. It trails on CAGR but is equal or better on Sharpe.
  - 2015-2026 50/200 crossover: 49.97% versus 58.44% for buy-and-hold.
  - — [finzdata 50/200](https://data.finzdata.com/s/bitcoin-50-200-moving-average-trend-2a424b); [finzdata trend 50/200](https://data.finzdata.com/s/bitcoin-trend-50-200-moving-average-2f29cd)
- A cross-asset test (BLOG, 2026) concludes the 200D MA "is a drawdown tool, not a return booster". BTC's drawdown improvement (16%) was the smallest of the 5 assets tested. — [EdgeLab](https://edgelabtrading.com/blog/200-day-moving-average/)
- QuantConnect research: BTC 50-day MA with a 20-day rate-of-change signal gave Sharpe 0.838 (grid median 0.812). The 70-day MA row was worst (0.629-0.76), which indicates parameter sensitivity. — [QuantConnect forum 21195](https://www.quantconnect.com/research/21195/bitcoin-regime-signal-for-growth-equities/p1)
- Systematic Strategies Substack, "Can You Keep Bitcoin's Upside Without the 83% Drawdown?" (2017 to mid-2025):
  - A crypto trend rule cut the deepest loss from 84% to 15%, and plain volatility targeting captured most of that improvement.
  - The simple BTC 200D long/flat rule had a slightly better Sharpe and shallower drawdown than a diversified multi-horizon ensemble.
  - Conclusion: trend following "reshaped risk far more than it added return".
  - — [Systematic Strategies Substack](https://systematicstrategies.substack.com/p/can-you-keep-bitcoins-upside-without)

### Inferences
- For a long-only spot implementation, the evidence supports MA filters mainly as drawdown and Sharpe improvers, not CAGR improvers. Expect roughly buy-and-hold-like Sharpe (around 1.0-1.1 over 2016-2026), drawdowns still of -60 to -70% on the single-asset daily 200D rule, and fewer than 10 round-trips per year.
- The 84% to 15% drawdown reduction comes from adding vol targeting or ensembles, not from the 200D rule alone.

### Gaps
- No peer-reviewed paper gives clean 20/100 or 50/200 BTC statistics with post-2021 data. Grayscale's exhibit numbers and trade counts were not retrieved.
- Win rate and profit factor for BTC MA crossovers are not reported in the sources found. Typical trend-filter win rates (30-45%) are not confirmed here for BTC.

## 4. Volatility targeting / vol-scaled sizing in crypto

### Takeaway
Volatility scaling is the most consistently helpful ingredient. One peer-reviewed BTC study reports Sharpe rising from 0.72 to 1.21 and "virtually eliminat[ing] large crashes". Practitioner tests find vol targeting delivers most of the drawdown reduction usually credited to trend filters. Industry convention is about 20-25% annual vol targets (versus BTC's realised ~50-80%), which implies large cash holdings. That fits a long-only spot account.

### Cited Findings
- Moreira & Muir, "Volatility-Managed Portfolios" (Journal of Finance, 2017). Taking less risk when volatility is high raises alphas and Sharpe ratios, because volatility changes are not matched by proportional changes in expected returns. This study covers equity factors, not crypto. — [ResearchGate](https://www.researchgate.net/publication/315972283_Volatility-Managed_Portfolios)
- "Liquidity Shocks, Price Volatilities, and Risk-managed Strategy: Evidence from Bitcoin and Beyond" (Journal of Multinational Financial Management, 2022). It follows the Barroso & Santa-Clara (2015) vol-scaling approach and uses liquidity shocks to forecast BTC volatility. The risk-managed strategy "virtually eliminates large crashes" and lifts Sharpe to 1.21 from 0.72 for buy-and-hold. — [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S1042444X22000019)
- Zarattini et al. size each position daily to a 25% annualised vol target (leverage capped at 200%). This is core to their Sharpe above 1.5. — [CXO Advisory](https://www.cxoadvisory.com/technical-trading/crypto-asset-trend-following-strategies/)
- Systematic Strategies (2017 to mid-2025): plain vol targeting captured most of the drawdown improvement (84% to 15%) attributed to trend rules. — [Systematic Strategies Substack](https://systematicstrategies.substack.com/p/can-you-keep-bitcoins-upside-without)
- Howden & Andreev (2026): a crash-state de-risking and drawdown overlay raises the 30-day TSMOM Sharpe from 1.41 to about 1.53 net of 25 bps, OOS. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7115459)
- Le & Ruthbah: a 30% risk-exposure, drawdown-controlled TSMOM gives a higher Sharpe and lower drawdown than buy-and-hold. — [Monash PDF](https://www.monash.edu/__data/assets/pdf_file/0011/3744821/Trend-following-Strategies-for-Crypto-Investors.pdf)
- 20% is described as "the industry standard" vol target for crypto indices. — [arXiv 2603.23480](https://arxiv.org/pdf/2603.23480)
- BLOG: in a risk-parity portfolio with BTC at a 20% vol target, Sharpe rises from 1.28 to 1.49. — [Beyond Passive Substack](https://beyondpassive.substack.com/p/sizing-bitcoin-a-first-principles)

### Inferences
- In a long-only spot account, vol targeting with leverage capped at 1x works as "hold cash when vol is high". It reduces drawdowns robustly and likely improves Sharpe modestly, but lowers CAGR compared with a full BTC position in strong bull runs.
- Trend filter plus vol targeting appear complementary. Evidence on which contributes more is mixed: one practitioner credits vol targeting with most of the drawdown benefit.

### Gaps
- No peer-reviewed crypto replication of Moreira-Muir across a multi-coin universe with 2022-2026 data was found.

## 5. Multi-coin trend portfolios (trend on top-N coins, equal risk)

### Takeaway
The best evidence is Zarattini et al. (2025): a top-20 rotating, survivorship-bias-free universe with per-coin Donchian ensembles and vol sizing. Results: Sharpe about 1.5, stable across portfolio sizes, and about 10.8-11% annual alpha versus BTC net of fees. Older studies also find trend rules on altcoins more profitable than on BTC. Survivorship bias and altcoin liquidity are the main risks.

### Cited Findings
- Zarattini, Pagani & Barbon: top-20 portfolio Sharpe above 1.5, 10.8% alpha versus BTC after fees, and Sharpe "notably stable around 1.5 across various portfolio sizes". The sample covers 21,616 assets with no survivorship bias. — [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5209907); [QuantifiedStrategies](https://www.quantifiedstrategies.com/?p=1192563)
- Grobys et al.: across 11 coins, the 20-day MA rule earned 8.76% p.a. excess return excluding BTC (2016-2018). — [Vaasa PDF](https://osuva.uwasa.fi/bitstream/10024/11192/2/Osuva_%20Grobys_Ahmed_Sapkota_2020.pdf)
- Hudson & Urquhart: OOS predictability persists in non-BTC coins but not BTC. — [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1)
- A 2017 to mid-2025 practitioner test found the simple BTC-only 200D rule had a slightly better Sharpe and shallower drawdown than a diversified multi-horizon ensemble. This partly contradicts the multi-coin advantage. — [Systematic Strategies Substack](https://systematicstrategies.substack.com/p/can-you-keep-bitcoins-upside-without)
- Market-structure risk: Pantera described 2025 as "an exceptionally narrow market" where few tokens had positive returns. BTC was down about 6% for the year, the broad token market much more, and altcoins have been in a bear market since late 2024. — [CoinDesk, Jan 2026](https://www.coindesk.com/markets/2026/01/23/altcoins-have-been-in-a-bear-market-since-late-2024-pantera-says)

### Inferences
- A long-only, multi-coin trend portfolio would have sat largely in cash during the altcoin bear market from late 2024 into 2025. This limits losses but makes BTC-dominated exposure the main return source.
- On US spot brokers (Coinbase, Alpaca), the investable coin list is narrower than a top-20 global universe, so results will differ from the paper.

### Gaps
- No live, audited multi-coin crypto trend fund returns were found.

## 6. Does trend following still work after 2021? Decay, whipsaw and regimes

### Takeaway
The evidence is mixed. The longest-sample peer-reviewed paper (Zarattini et al., data to Mar 2025) finds that long-horizon trends remain robust while short-horizon trends have weakened in the recent era. BTC-only MA filters over 2016-2026 roughly match buy-and-hold on Sharpe and trail on CAGR. Two OOS working papers from 2026 (Howden & Andreev; AdaptiveTrend) still report net Sharpe ratios of about 1.4-2.4 covering 2022-2024, but they are unrefereed. 2022 (BTC down 65%) favoured long/cash rules, which sat out much of the decline. 2025 was described as a "whipsaw" year, including for traditional CTAs.

### Cited Findings
- Short trends have weakened in the recent era; long trends remain statistically robust. — [Concretum/CXO summary](https://concretumgroup.com/catching-crypto-trends-a-tactical-approach-for-bitcoin-and-altcoins/)
- Hudson & Urquhart found no BTC predictability in their OOS period, which is evidence of BTC-specific decay already pre-2020. — [Springer](https://link.springer.com/article/10.1007/s10479-019-03357-1)
- BTC MA strategies over 2016 to Nov 2026 trail buy-and-hold on CAGR (56.0% vs 60.5%) with similar Sharpe (1.07 vs 1.04). — [finzdata](https://data.finzdata.com/s/bitcoin-50-200-moving-average-trend-2a424b)
- 2022: BTC lost 65% (high about $47.5k in March, low about $15.7k in November). Failure to reclaim the 200D MA throughout was cited as confirming the bear market. This was a regime where a long/cash filter avoided most of the loss. That is an inference from price path plus the rule, not a cited backtest. — [CoinDesk 2022 Annual Review](https://downloads.coindesk.com/research/CoinDesk-Research-2022-Annual-Crypto-Review.pdf); [Yahoo/CryptoQuant](https://finance.yahoo.com/markets/crypto/articles/bitcoin-whales-pulling-back-activity-175854387.html)
- 2025-2026: Pantera called 2025 a "whipsaw" year, with BTC down about 6%. One 2026 article says BTC's 2025-26 decline was down 23% in 83 days, versus 6% over the same period in early 2022. — [CoinDesk Jan 2026](https://www.coindesk.com/markets/2026/01/23/altcoins-have-been-in-a-bear-market-since-late-2024-pantera-says); [The Block, May 2026](https://www.theblock.co/news/markets/2026-05-20-cryptoquant-bitcoin-bear-market-pattern-sentiment-extremely-bearish-402091)
- Traditional trend (Man Group): the rolling 12-month trend-following return was -18.6% as of 30 Apr 2025, driven by policy whipsaw. Over 25 years, the probability of a 20%+ drawdown is about 4 in 5. This covers broad managed futures, not crypto. — [Man Group](https://www.man.com/insights/is-this-time-different)
- A BTC-USD trend algorithm study for 2021-2025 shows max drawdown -36.6% (recovered), with concentration risk. — [ResearchGate](https://www.researchgate.net/publication/395400190_Performance_Analysis_of_a_BTC-USD_Trend-Following_Algorithm_A_Comprehensive_Quantitative_Study_2021-2025)
- 2026 OOS working papers: Howden & Andreev report net Sharpe 1.41 versus 0.70 for buy-and-hold ([SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7115459)). AdaptiveTrend reports OOS Sharpe 2.41 over 2022-2024 ([arXiv](https://arxiv.org/html/2602.11708v1)).

### Inferences
- The post-2021 edge appears to have shifted from "beats buy-and-hold on return" to "similar return with far smaller drawdowns", especially for BTC alone. Short lookbacks (under about 20 days) face the most decay and whipsaw.
- Choppy regimes (2019 mid-year, mid-2021, much of 2023's range, and 2025) produce whipsaw. Lookback ensembles and vol scaling mitigate this, but sourced per-year figures were not found.

### Gaps
- No sourced per-year returns for crypto trend strategies in 2019, 2022, 2025 or 2026 were found.
- No public crypto trend fund (for example, a CTA's crypto sleeve or an ETF using trend rules) with 2022-2026 live returns was found in these searches.

## 7. Costs and implementation: fees, slippage, long-only vs long/short

### Takeaway
Break-even costs for most rules are well above actual crypto costs (Hudson & Urquhart). The edge survives at 10-25 bps per trade for daily rules (Zarattini at 0.10%; Howden at 25 bps). Short-lookback, high-turnover variants are where costs bite. Most practitioner and Grayscale research uses long/cash, which matches long-only US spot brokers. Long-only also captures BTC's upward drift and avoids shorting costs.

### Cited Findings
- The break-even transaction costs of most rules are "substantially higher" than actual crypto market costs. — [Springer, Hudson & Urquhart](https://link.springer.com/article/10.1007/s10479-019-03357-1)
- Zarattini et al. results assume 0.10% costs (net 18% CAGR configuration). Howden & Andreev use 25 bps. — [CXO](https://www.cxoadvisory.com/technical-trading/crypto-asset-trend-following-strategies/); [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7115459)
- Le & Ruthbah: shorter lookbacks give a higher Sharpe, but rebalancing costs reduce profits. The strategies still performed well after costs. — [Monash PDF](https://www.monash.edu/__data/assets/pdf_file/0011/3744821/Trend-following-Strategies-for-Crypto-Investors.pdf)
- Grayscale considers only long/cash strategies, "rather than go short". Shorter MAs mean more signals and higher costs. — [Grayscale](https://research.grayscale.com/reports/the-trend-is-your-friend-managing-bitcoins-volatility-with-momentum-signals)
- Quantpedia designs a long-only BTC trend strategy because of BTC's long-term upward bias and because shorting crypto is complex and costly. — [Quantpedia](https://quantpedia.com/how-to-design-a-simple-multi-timeframe-trend-strategy-on-bitcoin/)
- Rozario et al. assumed negligible fees, spread, slippage and impact, so their 255% figure overstates net results. — [arXiv](https://arxiv.org/pdf/2009.12155)
- Corbet et al.: buy signals outperform sell signals, consistent with the long side carrying most of the edge. — [IDEAS](https://ideas.repec.org/a/eee/finlet/v31y2019icp32-37.html)

### Inferences
- With retail spot fees (Coinbase Advanced or Alpaca crypto taker fees are roughly 0.15-0.60% per side, depending on tier; not verified in this search), a daily or weekly signal with fewer than about 20 round-trips per year is likely viable. Intraday or short-lookback rules are much more cost-sensitive.
- Most published long/short Sharpe gains come from the short leg in 2018 and 2022. The long-only versions forgo that but avoid funding and borrow costs.

### Gaps
- No source gave a direct, same-study long-only versus long/short comparison for crypto with explicit costs.
- Actual retail fee schedules for Coinbase and Alpaca were not verified here.
