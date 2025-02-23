import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"


def plot_signals(df, title):
    """Create Plotly figure to plot trading signals."""
    df["signal_plot"] = _map_signals_for_plotting(df["signal"])

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.1
    )

    fig.add_trace(
        _create_candlestick_trace(df[["Open", "High", "Low", "Close"]]), row=1, col=1
    )

    buy_trace, sell_trace = _create_signal_traces(df["signal_plot"])
    fig.add_trace(buy_trace, row=2, col=1)
    fig.add_trace(sell_trace, row=2, col=1)

    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Stock",
        xaxis_rangeslider_visible=False,
        legend_title="Legend",
    )

    fig.update_yaxes(
        title_text="Signal",
        row=2,
        col=1,
        tickvals=[-1, 0, 1],
        ticktext=["Sell", "Hold", "Buy"],
    )

    return fig


def _map_signals_for_plotting(signal):
    """Map signals to -1, 0, 1 for plotting."""
    signal_mapping = {0: 0, 1: -1, 2: 1}
    return signal.map(signal_mapping)


def _create_candlestick_trace(df):
    """Create candlestick trace for stock data."""
    return go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Stock",
    )


def _create_signal_traces(signal_plot):
    """Create signal bar traces for buy and sell signals."""
    buy_signals = signal_plot > 0
    buy_trace = go.Bar(
        x=signal_plot.index[buy_signals],
        y=signal_plot[buy_signals],
        marker_color="green",
        name="Buy Signal",
    )

    sell_signals = signal_plot < 0
    sell_trace = go.Bar(
        x=signal_plot.index[sell_signals],
        y=signal_plot[sell_signals],
        marker_color="red",
        name="Sell Signal",
    )

    return buy_trace, sell_trace
