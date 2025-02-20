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
    produces = BLD / f"{id_backtest}.pkl"

    @pytask.task(id=id_backtest)
    def task_backtest(scripts=scripts, data_path=data_path, produces=produces, row=row):
        data = pd.read_pickle(data_path)
        signals = generate_signals(data=data, method=row.strategy)
        portfolio = backtest_signals(
            data=data,
            signals=signals,
            initial_cash=INITIAL_CASH,
            tac=TAC,
            trade_pct=TRADE_PCT,
        )
        portfolio.to_pickle(produces)
