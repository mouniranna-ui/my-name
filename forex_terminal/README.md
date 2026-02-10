# Forex Backtesting Terminal

A Streamlit-based Forex backtesting terminal for rule-based strategies with realistic trading costs, SL/TP execution, risk-based sizing, and analytics.

## Setup

```bash
cd forex_terminal
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

## CSV Format

Input CSV must include:
- `time`
- `open`
- `high`
- `low`
- `close`
- `volume` (optional)

`time` is parsed as datetime, used as index, and data is sorted ascending.

## Backtest Assumptions

- Entry timing is **next candle open**.
- Spread + slippage are applied to executed entry/exit prices.
- Commission is charged **per side** (entry and exit) via `commission_per_lot`.
- Stop-loss is mandatory for each trade and position size is risk-based:
  - `lots = (balance * risk_pct) / (SL_pips * pip_value_per_lot)`
  - clamped to 0.01–10 lots.
- If both SL and TP hit in the same candle, **SL is applied first** (conservative).
- One open position at a time (MVP).

## Strategies

1. MA Crossover
   - Long on fast MA crossing above slow MA.
   - Short on fast MA crossing below slow MA.
2. RSI Reversion
   - Long when RSI < buy threshold.
   - Short when RSI > sell threshold.

## Outputs

- The `outputs/` folder is created automatically by the app.
- Trade exports are saved as timestamped CSV files in `outputs/`.
