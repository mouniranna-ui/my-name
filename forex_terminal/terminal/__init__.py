"""Forex backtesting terminal package."""

from .backtest import BacktestResult, run_backtest
from .broker import BrokerConfig, MarketInfo

__all__ = ["BacktestResult", "run_backtest", "BrokerConfig", "MarketInfo"]
