from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def build_price_figure(df: pd.DataFrame, trades: pd.DataFrame, strategy_name: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price",
        )
    )

    if strategy_name == "MA Crossover":
        if "fast_ma" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["fast_ma"], mode="lines", name="Fast MA"))
        if "slow_ma" in df.columns:
            fig.add_trace(go.Scatter(x=df.index, y=df["slow_ma"], mode="lines", name="Slow MA"))

    if not trades.empty:
        fig.add_trace(
            go.Scatter(
                x=trades["entry_time"],
                y=trades["entry_price"],
                mode="markers",
                marker=dict(symbol="triangle-up", size=10, color="green"),
                name="Entry",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=trades["exit_time"],
                y=trades["exit_price"],
                mode="markers",
                marker=dict(symbol="x", size=10, color="red"),
                name="Exit",
            )
        )

    fig.update_layout(height=550, xaxis_rangeslider_visible=False, template="plotly_white")
    return fig


def build_rsi_figure(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    if "rsi" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["rsi"], mode="lines", name="RSI"))
        fig.add_hline(y=30, line_dash="dash", line_color="green")
        fig.add_hline(y=70, line_dash="dash", line_color="red")
    fig.update_layout(height=250, template="plotly_white", yaxis_title="RSI")
    return fig


def build_equity_figure(equity_curve: pd.Series) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=equity_curve.index, y=equity_curve.values, mode="lines", name="Equity"))
    fig.update_layout(height=300, template="plotly_white", yaxis_title="Balance")
    return fig
