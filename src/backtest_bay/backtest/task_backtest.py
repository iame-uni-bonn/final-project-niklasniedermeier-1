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
    data_path = (
        BLD / "data" / f"{row.stock}_{row.start_date}_{row.end_date}_{row.interval}.pkl"
    )
    produces = BLD / "backtest" / f"{id_backtest}.pkl"
    strategy = row.strategy

    @pytask.task(id=id_backtest)
    def task_backtest(
        scripts=scripts, data_path=data_path, produces=produces, strategy=strategy
    ):
        data = pd.read_pickle(data_path)
        signals = generate_signals(data=data, method=strategy)
        portfolio = backtest_signals(
            data=data,
            signals=signals,
            initial_cash=INITIAL_CASH,
            tac=TAC,
            trade_pct=TRADE_PCT,
        )
        portfolio.to_pickle(produces)
