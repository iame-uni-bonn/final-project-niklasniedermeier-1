import pandas as pd
import pytask

from backtest_bay.backtest.backtest_signals import backtest_signals
from backtest_bay.backtest.generate_signals import generate_signals
from backtest_bay.config import BLD, INITIAL_CASH, PARAMS, SRC, TAC, TRADE_PCT

scripts = [
    SRC / "config.py",
    SRC / "backtest" / "generate_signals.py",
    SRC / "backtest" / "backtest_signals.py",
]

for row in PARAMS.itertuples(index=False):
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
        stock_data = pd.read_pickle(stock_data_path)
        signals = generate_signals(data=stock_data, method=strategy)
        backtested_portfolio = backtest_signals(
            data=stock_data,
            signals=signals,
            initial_cash=INITIAL_CASH,
            tac=TAC,
            trade_pct=TRADE_PCT,
        )

        merged_portfolio = _merge_stock_data_with_portfolio(
            stock_data, backtested_portfolio
        )

        merged_portfolio.to_pickle(produces)


def _merge_stock_data_with_portfolio(data, portfolio):
    """Merge data with portfolio using the index.

    Args:
        data (pd.DataFrame): DataFrame with downloaded data.
        portfolio (pd.DataFrame): DataFrame to be merged with data using the index.

    Returns:
        pd.DataFrame: Merged DataFrame.
    """
    data.columns = data.columns.droplevel(1)
    return data.merge(portfolio, how="left", left_index=True, right_index=True)
