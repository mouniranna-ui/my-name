from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .broker import (
    BrokerConfig,
    MarketInfo,
    apply_entry_price,
    apply_exit_price,
    commission_for_trade,
    estimate_pip_value_per_lot,
    pips_to_price,
    price_to_pips,
)
from .strategy import BaseStrategy
from .utils import validate_ohlc


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    trades: pd.DataFrame
    summary: dict
    data_with_indicators: pd.DataFrame


def _clamp_lots(lots: float, min_lot: float = 0.01, max_lot: float = 10.0) -> float:
    return max(min_lot, min(max_lot, lots))


def run_backtest(
    df: pd.DataFrame,
    strategy: BaseStrategy,
    symbol: str,
    broker_config: BrokerConfig,
    risk_pct: float,
    sl_pips: float,
    tp_pips: float | None = None,
    allow_short: bool = True,
    entry_timing: str = "next_open",
) -> BacktestResult:
    validate_ohlc(df)
    if entry_timing != "next_open":
        raise ValueError("Only entry_timing='next_open' is supported in MVP.")
    if sl_pips <= 0:
        raise ValueError("sl_pips must be > 0.")

    market = MarketInfo(symbol=symbol)
    pip_size = market.pip_size or broker_config.default_pip_size

    data = strategy.compute_indicators(df)
    data["signal"] = strategy.generate_signals(data)

    balance = float(broker_config.initial_balance)
    equity_curve = pd.Series(index=data.index, dtype=float)
    trade_rows: list[dict] = []

    open_pos: dict | None = None

    for i in range(1, len(data)):
        ts = data.index[i]
        row = data.iloc[i]
        prev_signal = int(data["signal"].iloc[i - 1])

        if open_pos is not None:
            side = open_pos["side"]
            exit_reason = None
            raw_exit_price = None

            if side == 1:
                sl_hit = row["low"] <= open_pos["sl_price"]
                tp_hit = open_pos["tp_price"] is not None and row["high"] >= open_pos["tp_price"]
                if sl_hit:
                    exit_reason = "SL"
                    raw_exit_price = open_pos["sl_price"]
                elif tp_hit:
                    exit_reason = "TP"
                    raw_exit_price = open_pos["tp_price"]
            else:
                sl_hit = row["high"] >= open_pos["sl_price"]
                tp_hit = open_pos["tp_price"] is not None and row["low"] <= open_pos["tp_price"]
                if sl_hit:
                    exit_reason = "SL"
                    raw_exit_price = open_pos["sl_price"]
                elif tp_hit:
                    exit_reason = "TP"
                    raw_exit_price = open_pos["tp_price"]

            if exit_reason is not None and raw_exit_price is not None:
                executed_exit = apply_exit_price(raw_exit_price, side, broker_config, pip_size)
                px_diff = (executed_exit - open_pos["entry_price"]) * side
                pip_diff = price_to_pips(px_diff, pip_size)
                pip_value = estimate_pip_value_per_lot(symbol, raw_exit_price, broker_config.lot_size)
                gross_pnl = pip_diff * pip_value * open_pos["size_lots"]
                fees = commission_for_trade(open_pos["size_lots"], broker_config)
                pnl = gross_pnl - fees
                balance += pnl

                spread_slip_pips = broker_config.spread_pips + 2 * broker_config.slippage_pips
                spread_slip_cost = spread_slip_pips * pip_value * open_pos["size_lots"]

                trade_rows.append(
                    {
                        "entry_time": open_pos["entry_time"],
                        "exit_time": ts,
                        "direction": "long" if side == 1 else "short",
                        "entry_price": open_pos["entry_price"],
                        "exit_price": executed_exit,
                        "sl_price": open_pos["sl_price"],
                        "tp_price": open_pos["tp_price"],
                        "size_lots": open_pos["size_lots"],
                        "pnl_usd": pnl,
                        "pnl_pips": pip_diff,
                        "fees_usd": fees,
                        "spread_slippage_cost_est_usd": spread_slip_cost,
                        "exit_reason": exit_reason,
                    }
                )
                open_pos = None

        if open_pos is None:
            side = 0
            if prev_signal == 1:
                side = 1
            elif prev_signal == -1 and allow_short:
                side = -1

            if side != 0:
                base_entry_price = row["open"]
                entry_price = apply_entry_price(base_entry_price, side, broker_config, pip_size)
                sl_price = entry_price - pips_to_price(sl_pips, pip_size) if side == 1 else entry_price + pips_to_price(sl_pips, pip_size)
                tp_price = None
                if tp_pips and tp_pips > 0:
                    tp_price = entry_price + pips_to_price(tp_pips, pip_size) if side == 1 else entry_price - pips_to_price(tp_pips, pip_size)

                pip_value = estimate_pip_value_per_lot(symbol, entry_price, broker_config.lot_size)
                risk_usd = max(0.0, balance * risk_pct)
                size_lots = _clamp_lots(risk_usd / (sl_pips * max(pip_value, 1e-9)))

                open_pos = {
                    "side": side,
                    "entry_time": ts,
                    "entry_price": entry_price,
                    "sl_price": sl_price,
                    "tp_price": tp_price,
                    "size_lots": size_lots,
                }

        equity_curve.iloc[i] = balance

    if len(data) > 0:
        equity_curve.iloc[0] = broker_config.initial_balance
    equity_curve = equity_curve.ffill().fillna(broker_config.initial_balance)

    trades = pd.DataFrame(trade_rows)
    summary = {
        "starting_balance": broker_config.initial_balance,
        "ending_balance": float(equity_curve.iloc[-1]) if not equity_curve.empty else broker_config.initial_balance,
        "total_trades": int(len(trades)),
        "entry_timing": entry_timing,
        "sl_tp_same_candle_policy": "SL-first (conservative)",
    }

    return BacktestResult(equity_curve=equity_curve, trades=trades, summary=summary, data_with_indicators=data)
