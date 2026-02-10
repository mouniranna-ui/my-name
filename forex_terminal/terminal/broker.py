from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class BrokerConfig:
    initial_balance: float = 10000.0
    spread_pips: float = 1.2
    slippage_pips: float = 0.2
    commission_per_lot: float = 0.0
    leverage: float = 30
    lot_size: int = 100000
    default_pip_size: float = 0.0001


@dataclass(slots=True)
class MarketInfo:
    symbol: str
    pip_size: float | None = None

    def __post_init__(self) -> None:
        if self.pip_size is None:
            self.pip_size = 0.01 if "JPY" in self.symbol.upper() else 0.0001


def pips_to_price(pips: float, pip_size: float) -> float:
    return pips * pip_size


def price_to_pips(price_diff: float, pip_size: float) -> float:
    return price_diff / pip_size


def estimate_pip_value_per_lot(symbol: str, price: float, lot_size: int = 100000) -> float:
    """Approximate pip value in quote currency (USD for XXXUSD pairs).

    Assumption for MVP:
      - For most major pairs with USD as quote (e.g. EURUSD), pip value is pip_size * lot_size.
      - For JPY quote pairs, convert by dividing by current price.
      - For other pairs we still use quote-currency value as approximation.
    """
    pip_size = 0.01 if "JPY" in symbol.upper() else 0.0001
    if "JPY" in symbol.upper():
        return (pip_size / max(price, 1e-9)) * lot_size
    return pip_size * lot_size


def apply_entry_price(base_price: float, side: int, cfg: BrokerConfig, pip_size: float) -> float:
    spread_half = pips_to_price(cfg.spread_pips / 2.0, pip_size)
    slippage = pips_to_price(cfg.slippage_pips, pip_size)
    if side > 0:  # BUY
        return base_price + spread_half + slippage
    return base_price - spread_half - slippage


def apply_exit_price(base_price: float, side: int, cfg: BrokerConfig, pip_size: float) -> float:
    spread_half = pips_to_price(cfg.spread_pips / 2.0, pip_size)
    slippage = pips_to_price(cfg.slippage_pips, pip_size)
    if side > 0:  # closing BUY => SELL
        return base_price - spread_half - slippage
    return base_price + spread_half + slippage


def commission_for_trade(size_lots: float, cfg: BrokerConfig) -> float:
    """Commission model: per-side commission, charged both on entry and exit."""
    return 2.0 * cfg.commission_per_lot * size_lots
