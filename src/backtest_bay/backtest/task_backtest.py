"""This script deploys a task to generate trading signals and backtest them."""

import itertools

import pandas as pd
import pytask

from backtest_bay.backtest.backtest_signals import (
    backtest_signals,
    merge_data_with_backtest_portfolio,
)
from backtest_bay.backtest.generate_signals import generate_signals
from backtest_bay.config import (
    BLD,
    END_DATE,
    INITIAL_CASH,
    INTERVAL,
    SRC,
    START_DATE,
    STOCKS,
    STRATEGIES,
    TAC,
    TRADE_PCT,
)

scripts = [
    SRC / "config.py",
    SRC / "backtest" / "generate_signals.py",
    SRC / "backtest" / "backtest_signals.py",
]

params_to_backtest = pd.DataFrame(
    list(itertools.product(STOCKS, [START_DATE], [END_DATE], [INTERVAL], STRATEGIES)),
    columns=["stock", "start_date", "end_date", "interval", "strategy"],
)


for row in params_to_backtest.itertuples(index=False):
    id_backtest = (
        f"{row.stock}_{row.start_date}_{row.end_date}_" f"{row.interval}_{row.strategy}"
    )
    stock_data_path = (
        BLD / "data" / f"{row.stock}_{row.start_date}_{row.end_date}_{row.interval}.pkl"
    )
    produces = BLD / "backtest" / f"{id_backtest}.pkl"
    strategy = row.strategy

    @pytask.task(id=id_backtest)
    def task_backtest(
        scripts=scripts,
        stock_data_path=stock_data_path,
        produces=produces,
        strategy=strategy,
    ):
        """Task to generate signals, backtest and store results it in the bld folder."""
        stock_data = pd.read_pickle(stock_data_path)
        signals = generate_signals(data=stock_data, method=strategy)
        backtested_portfolio = backtest_signals(
            data=stock_data,
            signals=signals,
            initial_cash=INITIAL_CASH,
            tac=TAC,
            trade_pct=TRADE_PCT,
        )

        merged_portfolio = merge_data_with_backtest_portfolio(
            stock_data, backtested_portfolio
        )

        merged_portfolio.to_pickle(produces)
