import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_portfolio(portfolio, title, tac):
    """Main function to plot the portfolio performance and metrics."""
    portfolio_return = _calculate_portfolio_return(portfolio["assets"])
    annualized_return = _calculate_annualized_return(portfolio["assets"])
    buy_and_hold_return = _calculate_annualized_return(portfolio["Close"])
    trades = _calculate_trades(portfolio["shares"])

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.70, 0.30],
        vertical_spacing=0.2,
        specs=[[{"type": "xy"}], [{"type": "domain"}]],
    )

    for trace in _create_portfolio_traces(portfolio):
        fig.add_trace(trace, row=1, col=1)

    metrics_table = _create_metrics_table(
        portfolio_return, annualized_return, trades, buy_and_hold_return, tac
    )
    fig.add_trace(metrics_table, row=2, col=1)

    fig.update_layout(_create_plot_layout(title))

    return fig


def _calculate_portfolio_return(stock):
    """Calculate the total return of the stock."""
    initial_value = stock.iloc[0]
    final_value = stock.iloc[-1]
    total_return = (final_value / initial_value) - 1
    portfolio_return = total_return * 100
    return portfolio_return


def _calculate_annualized_return(stock):
    """Calculate the annualized return for a stock."""
    initial_value = stock.iloc[0]
    final_value = stock.iloc[-1]
    total_return = (final_value / initial_value) - 1

    years = _calculate_years(stock)
    annualized_return = ((1 + total_return) ** (1 / years) - 1) * 100

    return annualized_return


def _calculate_years(stock):
    """Calculate the number of years between the first and last date of a stock."""
    total_seconds = (stock.index[-1] - stock.index[0]).total_seconds()
    years = total_seconds / pd.Timedelta(days=365).total_seconds()
    return years


def _calculate_trades(shares):
    """Calculate the number of trades by counting changes in the shares held."""
    trades = shares.diff().ne(0).sum()
    return trades


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
    portfolio_return, annualized_return, trades, buy_and_hold_return, tac
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
                    "Total Return",
                    "Annualized Return",
                    "Trades",
                    "Assumed TAC",
                    "Benchmark: Annualized Buy and Hold Return",
                ],
                [
                    f"{portfolio_return:.2f}%",
                    f"{annualized_return:.2f}%",
                    trades,
                    f"{tac * 100:.2f}%",
                    f"{buy_and_hold_return:.2f}%",
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
