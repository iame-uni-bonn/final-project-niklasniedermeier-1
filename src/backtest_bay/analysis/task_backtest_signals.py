import pandas as pd
import pytask

from backtest_bay.analysis.backtest_signals import backtest_signals
from backtest_bay.analysis.generate_signals import generate_signals
from backtest_bay.config import BLD, INITIAL_CASH, PARAMS, SRC, TAC, TRADE_PCT

scripts = [
    SRC / "config.py",
    SRC / "analysis" / "generate_signals.py",
    SRC / "analysis" / "backtest_signals.py",
]

for row in PARAMS.itertuples(index=False):
    id_backtest = (
        f"{row.stock}_{row.start_date}_{row.end_date}_" f"{row.interval}_{row.strategy}"
    )
    data_path = BLD / f"{row.stock}_{row.start_date}_{row.end_date}_{row.interval}.pkl"
    data = pd.read_pickle(data_path)
    produces = BLD / f"{id_backtest}.pkl"

    signals = generate_signals(data, row.strategy)

    @pytask.task(id=id_backtest)
    def task_backtest_signals(
        data=data,
        signals=signals,
        initial_cash=INITIAL_CASH,
        tac=TAC,
        investment_pct=TRADE_PCT,
        scripts=scripts,
        data_path=data_path,
        produces=produces,
    ):
        portfolio = backtest_signals(data, signals, initial_cash, tac, investment_pct)
        portfolio.to_pickle(produces)
