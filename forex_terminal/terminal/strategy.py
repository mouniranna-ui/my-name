from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class BaseStrategy:
    name: str
    params: dict = field(default_factory=dict)

    def compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        raise NotImplementedError

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        raise NotImplementedError


@dataclass
class MACrossoverStrategy(BaseStrategy):
    name: str = "MA Crossover"
    params: dict = field(default_factory=lambda: {"fast_ma": 20, "slow_ma": 50})

    def compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        fast = int(self.params.get("fast_ma", 20))
        slow = int(self.params.get("slow_ma", 50))
        out["fast_ma"] = out["close"].rolling(fast, min_periods=fast).mean()
        out["slow_ma"] = out["close"].rolling(slow, min_periods=slow).mean()
        return out

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        fast = df["fast_ma"]
        slow = df["slow_ma"]
        prev_fast = fast.shift(1)
        prev_slow = slow.shift(1)

        long_cross = (fast > slow) & (prev_fast <= prev_slow)
        short_cross = (fast < slow) & (prev_fast >= prev_slow)

        signal = pd.Series(0, index=df.index, dtype=int)
        signal.loc[long_cross] = 1
        signal.loc[short_cross] = -1
        return signal


@dataclass
class RSIReversionStrategy(BaseStrategy):
    name: str = "RSI Reversion"
    params: dict = field(
        default_factory=lambda: {"rsi_period": 14, "buy_th": 30.0, "sell_th": 70.0}
    )

    @staticmethod
    def _rsi(close: pd.Series, period: int) -> pd.Series:
        delta = close.diff()
        gains = delta.clip(lower=0)
        losses = -delta.clip(upper=0)

        avg_gain = gains.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
        avg_loss = losses.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()

        rs = avg_gain / avg_loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        return rsi.fillna(50)

    def compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        period = int(self.params.get("rsi_period", 14))
        out["rsi"] = self._rsi(out["close"], period)
        return out

    def generate_signals(self, df: pd.DataFrame) -> pd.Series:
        buy_th = float(self.params.get("buy_th", 30.0))
        sell_th = float(self.params.get("sell_th", 70.0))
        rsi = df["rsi"]
        signal = pd.Series(0, index=df.index, dtype=int)
        signal.loc[rsi < buy_th] = 1
        signal.loc[rsi > sell_th] = -1
        return signal
