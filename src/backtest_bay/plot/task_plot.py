"""This script deploys a task to plot the backtested portfolio and trading signals."""

import itertools

import pandas as pd
import pytask

from backtest_bay.config import (
    BLD,
    END_DATES,
    INITIAL_CASH,
    INTERVALS,
    SRC,
    START_DATES,
    STOCKS,
    STRATEGIES,
    TAC,
)
from backtest_bay.plot.plot_portfolio import plot_portfolio
from backtest_bay.plot.plot_signals import plot_signals

scripts = [
    SRC / "config.py",
    SRC / "plot" / "plot_signals.py",
    SRC / "plot" / "plot_portfolio.py",
]

params_to_plot = pd.DataFrame(
    list(
        itertools.product(STOCKS, [START_DATES], [END_DATES], [INTERVALS], STRATEGIES)
    ),
    columns=["stock", "start_date", "end_date", "interval", "strategy"],
)

for row in params_to_plot.itertuples(index=False):
    id_backtest = (
        f"{row.stock}_{row.start_date}_{row.end_date}_{row.interval}_{row.strategy}"
    )
    backtest_path = BLD / "backtest" / f"{id_backtest}.pkl"
    plot_path = f"{row.stock}_{row.start_date}_{row.end_date}_{row.interval}"
    produces = {
        "plot_signals": BLD / "plot" / plot_path / f"plot_signals_{row.strategy}.html",
        "plot_portfolio": BLD
        / "plot"
        / plot_path
        / f"plot_portfolio_{row.strategy}.html",
    }

    @pytask.task(id=id_backtest)
    def task_plot(
        scripts=scripts,
        backtest_path=backtest_path,
        produces=produces,
        id_backtest=id_backtest,
    ):
        """Task to plot the backtested portfolio and trading signals."""
        portfolio = pd.read_pickle(backtest_path)
        fig = plot_signals(portfolio, id_backtest)
        fig.write_html(produces.get("plot_signals"))
        fig = plot_portfolio(portfolio, id_backtest, TAC, INITIAL_CASH)
        fig.write_html(produces.get("plot_portfolio"))
