import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.options.mode.copy_on_write = True
pd.options.future.infer_string = True
pd.options.plotting.backend = "plotly"


def plot_portfolio(portfolio, title, tac, cash):
    """Main function to plot the portfolio performance and metrics."""
    portfolio_return = _calculate_portfolio_return(portfolio["assets"])
    annualized_return = _calculate_annualized_return(portfolio["assets"])
    annualized_volatility = _calculate_annualized_volatility(portfolio["assets"])

    # Benchmark: Buy and Hold Strategy
    portfolio["buy_and_hold"] = _buy_and_hold_strategy(cash, portfolio["Close"])
    buy_and_hold_return = _calculate_annualized_return(portfolio["buy_and_hold"])
    buy_and_hold_volatility = _calculate_annualized_volatility(
        portfolio["buy_and_hold"]
    )

    trades = _calculate_trades(portfolio["shares"])
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.60, 0.40],
        vertical_spacing=0.15,
        specs=[[{"type": "xy"}], [{"type": "domain"}]],
    )

    for trace in _create_portfolio_traces(portfolio):
        fig.add_trace(trace, row=1, col=1)

    metrics_table = _create_metrics_table(
        portfolio_return,
        annualized_return,
        annualized_volatility,
        trades,
        buy_and_hold_return,
        buy_and_hold_volatility,
        tac,
    )
    fig.add_trace(metrics_table, row=2, col=1)

    fig.update_layout(_create_plot_layout(title))

    return fig


def _create_portfolio_traces(portfolio):
    """Create Plotly traces for cash and assets over time."""
    traces = [
        go.Scatter(x=portfolio.index, y=portfolio["cash"], mode="lines", name="Cash"),
        go.Scatter(
            x=portfolio.index,
            y=portfolio["assets"],
            mode="lines",
            name="Assets (Cash + Holdings)",
        ),
    ]
    return traces


def _create_metrics_table(
    portfolio_return,
    annualized_return,
    annualized_volatility,
    trades,
    buy_and_hold_return,
    buy_and_hold_volatility,
    tac,
):
    """Create a Plotly table for the portfolio metrics."""
    table = go.Table(
        header={
            "values": ["Metric", "Value"],
            "fill_color": "lightgrey",
            "align": "center",
        },
        cells={
            "values": [
                [
                    "Total Strategy Return",
                    "Annualized Strategy Return",
                    "Annualized Strategy Volatility",
                    "Trades",
                    "Assumed TAC",
                    "Annualized Buy and Hold Return",
                    "Annualized Buy and Hold Volatility",
                ],
                [
                    f"{portfolio_return:.2f}%",
                    f"{annualized_return:.2f}%",
                    f"{annualized_volatility:.2f}%",
                    trades,
                    f"{tac * 100:.2f}%",
                    f"{buy_and_hold_return:.2f}%",
                    f"{buy_and_hold_volatility:.2f}%",
                ],
            ],
            "align": "left",
        },
    )
    return table


def _create_plot_layout(title):
    """Create the layout configuration for the Plotly figure."""
    layout = {
        "title": title,
        "xaxis_title": "Date",
        "yaxis_title": "Value",
        "legend_title": "Portfolio Components",
        "template": "plotly",
    }
    return layout


def _calculate_portfolio_return(stock):
    """Calculate the total return of the stock."""
    initial_value = stock.iloc[0]
    final_value = stock.iloc[-1]

    if initial_value == 0:
        return float("nan")

    total_return = (final_value / initial_value) - 1
    portfolio_return = total_return * 100
    return portfolio_return


def _calculate_annualized_return(stock):
    """Calculate the annualized return for a stock."""
    total_return = _calculate_portfolio_return(stock) / 100
    years = _calculate_years(stock.index)

    if years == 0:
        return 0

    annualized_return = ((1 + total_return) ** (1 / years) - 1) * 100
    return annualized_return


def _calculate_years(stock_index):
    """Calculate the number of years between the first and last date of a stock."""
    total_seconds = (stock_index[-1] - stock_index[0]).total_seconds()
    years = total_seconds / pd.Timedelta(days=365).total_seconds()
    return years


def _calculate_trades(shares):
    """Calculate the number of trades by counting changes in the shares held."""
    trades = shares.diff().fillna(0).ne(0).sum()
    return trades


def _calculate_annualized_volatility(stock):
    if len(stock) <= 1:
        return 0

    daily_log_returns = np.log(stock / stock.shift(1)).dropna()
    daily_volatility = daily_log_returns.std()
    years = _calculate_years(stock.index)
    days_per_year = 365 / years

    if years == 0:
        return 0

    annualized_volatility = daily_volatility * np.sqrt(days_per_year) * 100
    return annualized_volatility


def _buy_and_hold_strategy(initial_cash, prices):
    first_price = prices.iloc[0]

    if first_price == 0:
        return 0

    shares = np.floor(initial_cash / first_price)
    return shares * prices
