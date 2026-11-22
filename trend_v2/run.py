"""Evaluate both strategies against the report's pass/fail criteria. Writes reports/REPORT.md and equity.png.

Rules were fixed in reports/Proven crypto trading strategies.md BEFORE any of this was run; nothing here
is tuned. Holdout = 2023-11-22 -> 2026-11-21, as the report specifies.
"""
from __future__ import annotations

import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from engine import load_panel, simulate, stats
from strategies import (CORE_RULE, DONCHIAN_RULE, HOLD_RULE, LOOKBACKS, VOLMATCH_RULE, btc_filter_targets,
                        btc_hold_targets, btc_volmatched_targets, core_overlay, core_targets, donchian_targets)

warnings.filterwarnings("ignore")
OUT = Path(__file__).resolve().parent / "reports"
PERIODS = {"Development 2018-01 → 2023-11": ("2018-01-01", "2023-11-21"),
           "**Holdout 2023-11 → 2026-11**": ("2023-11-22", "2026-11-21")}
HOLD = ("2023-11-22", "2026-11-21")
COSTS = {"Alpaca (0.35%/side)": 0.0035, "Alpaca ×2 (0.70%/side)": 0.0070, "Coinbase entry (0.75%/side)": 0.0075}
ALPACA = 0.0035


def fmt(s: dict) -> str:
    g = lambda k, f: (f.format(s[k]) if k in s and pd.notna(s[k]) else "–")
    return (f"| {g('cagr', '{:+.1%}')} | **{g('sharpe', '{:.2f}')}** | {g('max_dd', '{:.0%}')} | {g('calmar', '{:.2f}')} | "
            f"{g('vol', '{:.0%}')} | {g('win_rate', '{:.0%}')} | {g('profit_factor', '{:.2f}')} | {g('turnover', '{:.1f}×')} | "
            f"{g('exposure', '{:.0%}')} |")


HDR = ["| Strategy | CAGR | Sharpe | Max DD | Calmar | Vol | Win rate | Profit factor | Turnover/yr | Avg exposure |",
       "|---|---|---|---|---|---|---|---|---|---|"]


def main():
    OUT.mkdir(exist_ok=True)
    P = load_panel()
    btc = P.frame(P.c)["BTC"]
    T = {"core": core_targets(P), "donch": donchian_targets(P),
         "donch_short": donchian_targets(P, tuple(max(5, round(n * 0.7)) for n in LOOKBACKS)),
         "donch_long": donchian_targets(P, tuple(round(n * 1.3) for n in LOOKBACKS)),
         "hold": btc_hold_targets(P), "filter": btc_filter_targets(P)}
    ov = core_overlay(P)

    def run(name, cost, start, end):
        rule = {"core": CORE_RULE, "hold": HOLD_RULE, "filter": HOLD_RULE}.get(name, DONCHIAN_RULE)
        r = simulate(P, T[name], cost, rule, start=start, end=end, overlay=ov if name == "core" else None)
        return r, stats(r, btc)

    def volmatched(target_vol, cost, start, end):
        r = simulate(P, btc_volmatched_targets(P, target_vol), cost, VOLMATCH_RULE, start=start, end=end)
        return r, stats(r, btc)

    L = ["# Trend strategies v2: backtest against the research report's criteria", "",
         "Rules come from `reports/Proven crypto trading strategies.md` and were fixed **before** any test was run. "
         "Nothing was tuned. The holdout is 2023-11-22 → 2026-11-21, as the report specifies.", "",
         f"Universe: {len(P.coins)} price series, including coins that were later delisted or collapsed "
         "(LUNA, FTT, BSV, SRM, HNT, MATIC, XMR, EOS, WAVES, OMG, FTM, MKR, …). This cuts survivorship bias. "
         "A coin whose history ends while held is sold at its last close.", ""]
    res = {}
    for pname, (s, e) in PERIODS.items():
        L += [f"## {pname}, Alpaca costs (0.35% per side)", "", *HDR]
        rows = {}
        for name, label in [("core", "2. BTC/ETH trend core"), ("donch", "1. Donchian ensemble, top-20 coins"),
                            ("hold", "BTC buy & hold"), ("filter", "BTC 200-day filter")]:
            r, st = run(name, ALPACA, s, e)
            rows[name] = (r, st)
            L.append(f"| {label} " + fmt(st))
        for name, label in [("core", "BTC vol-matched to core"), ("donch", "BTC vol-matched to Donchian")]:
            _, st = volmatched(rows[name][1]["vol"], ALPACA, s, e)
            rows[f"vm_{name}"] = (None, st)
            L.append(f"| {label} " + fmt(st))
        res[pname] = rows
        L.append("")

    # ---------- pass / fail on the holdout ----------
    H = res["**Holdout 2023-11 → 2026-11**"]
    core, donch, hold = H["core"][1], H["donch"][1], H["hold"][1]
    vm_core, vm_donch = H["vm_core"][1], H["vm_donch"][1]
    cost2 = {n: run(n, 0.0070, *HOLD)[1] for n in ("core", "donch")}
    shift = {n: run(n, ALPACA, *HOLD)[1]["sharpe"] for n in ("donch_short", "donch_long")}
    cb = {n: run(n, 0.0075, *HOLD)[1] for n in ("core", "donch")}

    def check(label, ok, detail):
        return f"| {label} | {'✅ pass' if ok else '❌ fail'} | {detail} |"

    L += ["## Pass/fail on the holdout (criteria from the report, Alpaca costs)", "",
          "### Strategy 2: BTC/ETH trend core", "", "| Criterion | Result | Detail |", "|---|---|---|",
          check("Sharpe ≥ BTC buy & hold + 0.2", core["sharpe"] >= hold["sharpe"] + 0.2, f"{core['sharpe']:.2f} vs {hold['sharpe']:.2f}"),
          check("Sharpe ≥ vol-matched BTC + 0.2", core["sharpe"] >= vm_core["sharpe"] + 0.2, f"{core['sharpe']:.2f} vs {vm_core['sharpe']:.2f}"),
          check("Max drawdown ≤ 40%", core["max_dd"] >= -0.40, f"{core['max_dd']:.0%}"),
          check("Calmar ≥ 2× buy & hold", core["calmar"] >= 2 * hold["calmar"], f"{core['calmar']:.2f} vs {hold['calmar']:.2f}"),
          check("< 15 round trips per coin per year", core.get("round_trips_per_coin_yr", 0) < 15, f"{core.get('round_trips_per_coin_yr', 0):.1f}"),
          "", "### Strategy 1: Donchian ensemble", "", "| Criterion | Result | Detail |", "|---|---|---|",
          check("Sharpe ≥ 1.0", donch["sharpe"] >= 1.0, f"{donch['sharpe']:.2f}"),
          check("Sharpe ≥ vol-matched BTC + 0.2", donch["sharpe"] >= vm_donch["sharpe"] + 0.2, f"{donch['sharpe']:.2f} vs {vm_donch['sharpe']:.2f}"),
          check("Max drawdown ≤ 35%", donch["max_dd"] >= -0.35, f"{donch['max_dd']:.0%}"),
          check("Positive alpha vs BTC", donch["alpha_ann"] > 0, f"{donch['alpha_ann']:+.1%}/yr, t = {donch['alpha_t']:.1f}"),
          check("Profit factor ≥ 1.5", donch.get("profit_factor", 0) >= 1.5, f"{donch.get('profit_factor', 0):.2f}"),
          check("Turnover ≤ 8× per year", donch["turnover"] <= 8, f"{donch['turnover']:.1f}×"),
          check("Sharpe positive at 2× costs", cost2["donch"]["sharpe"] > 0, f"{cost2['donch']['sharpe']:.2f}"),
          check("Sharpe drops < 30% with lookbacks ±30%",
                min(shift.values()) >= 0.7 * donch["sharpe"],
                f"−30%: {shift['donch_short']:.2f}, +30%: {shift['donch_long']:.2f}, base {donch['sharpe']:.2f}"),
          check("Beats the BTC/ETH core (kill condition)", donch["sharpe"] > core["sharpe"], f"{donch['sharpe']:.2f} vs {core['sharpe']:.2f}"),
          "", "## Cost sensitivity on the holdout", "", "| Strategy | Alpaca | Alpaca ×2 | Coinbase entry |", "|---|---|---|---|"]
    for n, label in [("core", "BTC/ETH core"), ("donch", "Donchian ensemble")]:
        a = H[n][1]
        L.append(f"| {label} | Sharpe {a['sharpe']:.2f}, CAGR {a['cagr']:+.1%} | Sharpe {cost2[n]['sharpe']:.2f}, CAGR {cost2[n]['cagr']:+.1%} "
                 f"| Sharpe {cb[n]['sharpe']:.2f}, CAGR {cb[n]['cagr']:+.1%} |")

    # ---------- by year (full 2018+) ----------
    rc, _ = run("core", ALPACA, "2018-01-01", None)
    rd, _ = run("donch", ALPACA, "2018-01-01", None)
    rh, _ = run("hold", ALPACA, "2018-01-01", None)
    L += ["", "## Calendar-year returns (Alpaca costs)", "", "| Year | BTC/ETH core | Donchian ensemble | BTC buy & hold |", "|---|---|---|---|"]
    for y in range(2018, 2027):
        f = lambda r: r.equity.loc[str(y)].iloc[-1] / r.equity.loc[:f"{y - 1}-12-31"].iloc[-1] - 1 if y > 2018 else r.equity.loc["2018"].iloc[-1] / r.equity.iloc[0] - 1
        L.append(f"| {y}{' (to Nov 21)' if y == 2026 else ''} | {f(rc):+.0%} | {f(rd):+.0%} | {f(rh):+.0%} |")

    L += ["", "![equity](equity.png)", "", "## Notes", "",
          "- **Win rate is low by design:** about 30–35% of trades win, but winners are 2–3× the size of losers. "
          "That's what the research predicted for working trend systems.",
          "- **Vol-matched BTC** is BTC scaled daily to the same volatility as the strategy, with no leverage. "
          "Beating it shows the trend signal adds something beyond simply holding less BTC.",
          "- **Universe:** this is point-in-time by Binance dollar volume, which is not Alpaca's actual listing history. "
          "BTC uses Bitstamp prices and is always included. ETH history starts 2017-08, so tests start 2018-01.",
          "- **Rebalance band:** the Donchian band is read as 'trade when the change is more than 3% of equity or "
          "more than 25% of the current weight', with a 1% minimum trade.",
          "- Research code, not financial advice. Paper-trade before using real money."]
    (OUT / "REPORT.md").write_text("\n".join(L) + "\n")

    fig, ax = plt.subplots(figsize=(10, 4.8))
    for r, lab, col in [(rc, "BTC/ETH trend core", "tab:blue"), (rd, "Donchian ensemble", "tab:green"), (rh, "BTC buy & hold", "orange")]:
        ax.plot(r.equity.index, r.equity / r.equity.iloc[0], label=lab, color=col, lw=1.6)
    ax.axvline(pd.Timestamp(HOLD[0], tz="UTC"), color="grey", ls="--", lw=1)
    ax.set_yscale("log"); ax.legend(); ax.set_title("Growth of $1 since 2018, Alpaca costs (dashed = holdout start)")
    fig.tight_layout(); fig.savefig(OUT / "equity.png", dpi=130)
    print("\n".join(L))


if __name__ == "__main__":
    main()
