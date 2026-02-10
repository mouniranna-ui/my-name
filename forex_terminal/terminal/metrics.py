from __future__ import annotations

import numpy as np
import pandas as pd

from .utils import calculate_drawdown


def compute_metrics(trades: pd.DataFrame, equity_curve: pd.Series, starting_balance: float) -> tuple[dict, pd.DataFrame]:
    if equity_curve.empty:
        raise ValueError("Equity curve is empty.")

    ending_balance = float(equity_curve.iloc[-1])
    total_return_pct = ((ending_balance / starting_balance) - 1.0) * 100

    if trades.empty:
        base = {
            "Total return %": total_return_pct,
            "Win rate %": 0.0,
            "Profit factor": 0.0,
            "Average trade (USD)": 0.0,
            "Max drawdown %": float(calculate_drawdown(equity_curve).min() * 100),
            "Sharpe ratio": 0.0,
            "Expectancy (USD)": 0.0,
            "Number of trades": 0,
            "Longest win streak": 0,
            "Longest loss streak": 0,
        }
        return base, pd.DataFrame([base])

    pnl = trades["pnl_usd"].astype(float)
    wins = pnl[pnl > 0]
    losses = pnl[pnl < 0]
    win_rate = (len(wins) / len(pnl)) * 100 if len(pnl) else 0.0

    gross_profit = wins.sum()
    gross_loss = abs(losses.sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else np.inf

    avg_trade = pnl.mean()

    dd = calculate_drawdown(equity_curve)
    max_dd_pct = float(dd.min() * 100)

    # Assumption: returns are based on bar-to-bar equity changes. Annualization uses hourly bars (24*252).
    returns = equity_curve.pct_change().replace([np.inf, -np.inf], np.nan).dropna()
    sharpe = 0.0
    if not returns.empty and returns.std() > 0:
        sharpe = np.sqrt(24 * 252) * (returns.mean() / returns.std())

    avg_win = wins.mean() if len(wins) else 0.0
    avg_loss = abs(losses.mean()) if len(losses) else 0.0
    win_rate_dec = len(wins) / len(pnl)
    loss_rate_dec = len(losses) / len(pnl)
    expectancy = (avg_win * win_rate_dec) - (avg_loss * loss_rate_dec)

    signs = np.sign(pnl)
    win_streak = loss_streak = max_win_streak = max_loss_streak = 0
    for s in signs:
        if s > 0:
            win_streak += 1
            loss_streak = 0
        elif s < 0:
            loss_streak += 1
            win_streak = 0
        else:
            win_streak = 0
            loss_streak = 0
        max_win_streak = max(max_win_streak, win_streak)
        max_loss_streak = max(max_loss_streak, loss_streak)

    metrics = {
        "Total return %": float(total_return_pct),
        "Win rate %": float(win_rate),
        "Profit factor": float(profit_factor if np.isfinite(profit_factor) else 0.0),
        "Average trade (USD)": float(avg_trade),
        "Max drawdown %": max_dd_pct,
        "Sharpe ratio": float(sharpe),
        "Expectancy (USD)": float(expectancy),
        "Number of trades": int(len(trades)),
        "Longest win streak": int(max_win_streak),
        "Longest loss streak": int(max_loss_streak),
    }

    return metrics, pd.DataFrame([metrics])
