from __future__ import annotations

from pathlib import Path

import streamlit as st

from terminal.backtest import run_backtest
from terminal.broker import BrokerConfig
from terminal.data import load_csv
from terminal.metrics import compute_metrics
from terminal.plotting import build_equity_figure, build_price_figure, build_rsi_figure
from terminal.strategy import MACrossoverStrategy, RSIReversionStrategy
from terminal.utils import timestamp_string

st.set_page_config(page_title="Forex Backtesting Terminal", layout="wide")
st.title("Forex Backtesting Terminal")

base_dir = Path(__file__).parent
data_dir = base_dir / "data"
outputs_dir = base_dir / "outputs"
outputs_dir.mkdir(parents=True, exist_ok=True)

csv_files = sorted(data_dir.glob("*.csv"))
if not csv_files:
    st.error("No CSV files found in data/ directory.")
    st.stop()

with st.sidebar:
    st.header("Configuration")
    selected_csv = st.selectbox("CSV file", [f.name for f in csv_files])
    symbol_default = Path(selected_csv).stem.split("_")[1] if "_" in Path(selected_csv).stem else "EURUSD"
    symbol = st.text_input("Symbol", value=symbol_default)

    strategy_name = st.selectbox("Strategy", ["MA Crossover", "RSI Reversion"])

    strategy_params = {}
    if strategy_name == "MA Crossover":
        strategy_params["fast_ma"] = st.number_input("Fast MA", min_value=2, max_value=500, value=20)
        strategy_params["slow_ma"] = st.number_input("Slow MA", min_value=3, max_value=800, value=50)
    else:
        strategy_params["rsi_period"] = st.number_input("RSI period", min_value=2, max_value=100, value=14)
        strategy_params["buy_th"] = st.slider("RSI buy threshold", min_value=1, max_value=50, value=30)
        strategy_params["sell_th"] = st.slider("RSI sell threshold", min_value=50, max_value=99, value=70)

    st.subheader("Risk")
    risk_pct = st.number_input("Risk % per trade", min_value=0.001, max_value=0.2, value=0.01, step=0.001)
    sl_pips = st.number_input("SL pips", min_value=1.0, max_value=500.0, value=20.0)
    tp_pips = st.number_input("TP pips (0 to disable)", min_value=0.0, max_value=1000.0, value=30.0)
    allow_short = st.toggle("Allow shorts", value=True)

    st.subheader("Costs")
    spread_pips = st.number_input("Spread (pips)", min_value=0.0, max_value=20.0, value=1.2, step=0.1)
    slippage_pips = st.number_input("Slippage (pips)", min_value=0.0, max_value=10.0, value=0.2, step=0.1)
    commission_per_lot = st.number_input("Commission per lot per side (USD)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

    run_bt = st.button("Run Backtest", type="primary")

if run_bt:
    try:
        df = load_csv(str(data_dir / selected_csv))
        strategy = (
            MACrossoverStrategy(params=strategy_params)
            if strategy_name == "MA Crossover"
            else RSIReversionStrategy(params=strategy_params)
        )
        broker = BrokerConfig(
            spread_pips=float(spread_pips),
            slippage_pips=float(slippage_pips),
            commission_per_lot=float(commission_per_lot),
        )

        result = run_backtest(
            df=df,
            strategy=strategy,
            symbol=symbol,
            broker_config=broker,
            risk_pct=float(risk_pct),
            sl_pips=float(sl_pips),
            tp_pips=float(tp_pips) if tp_pips > 0 else None,
            allow_short=allow_short,
            entry_timing="next_open",
        )

        metrics_dict, metrics_df = compute_metrics(result.trades, result.equity_curve, broker.initial_balance)

        st.subheader("Price + Trades")
        st.plotly_chart(build_price_figure(result.data_with_indicators, result.trades, strategy_name), use_container_width=True)

        if strategy_name == "RSI Reversion":
            st.subheader("RSI")
            st.plotly_chart(build_rsi_figure(result.data_with_indicators), use_container_width=True)

        st.subheader("Equity Curve")
        st.plotly_chart(build_equity_figure(result.equity_curve), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Metrics")
            st.dataframe(metrics_df, use_container_width=True)
        with col2:
            st.subheader("Summary")
            st.json(result.summary | {"symbol": symbol, "strategy": strategy.name})

        st.subheader("Trades")
        st.dataframe(result.trades, use_container_width=True)

        if not result.trades.empty:
            ts = timestamp_string()
            output_file = outputs_dir / f"trades_{symbol}_{strategy_name.replace(' ', '_')}_{ts}.csv"
            csv_data = result.trades.to_csv(index=False).encode("utf-8")
            output_file.write_bytes(csv_data)

            st.download_button(
                "Download trades CSV",
                data=csv_data,
                file_name=output_file.name,
                mime="text/csv",
            )
            st.caption(f"Saved to {output_file}")

        st.success("Backtest completed.")
        st.metric("Ending balance", f"${metrics_dict.get('Total return %', 0):.2f}% return")

    except Exception as exc:
        st.error(f"Backtest failed: {exc}")
else:
    st.info("Configure settings and click Run Backtest.")
