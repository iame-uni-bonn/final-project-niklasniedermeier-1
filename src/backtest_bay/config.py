"""All the general configuration of the project."""

import itertools
from pathlib import Path

import pandas as pd

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()

BLD = ROOT.joinpath("bld").resolve()

# Configure input data
STOCKS = ["AAPL", "MSFT"]
START_DATES = ["2022-01-01"]
END_DATES = ["2025-01-01"]
INTERVALS = ["1d"]
STRATEGIES = ["bollinger", "macd", "roc", "rsi"]

INITIAL_CASH = 1000
TAC = 0.05
TRADE_PCT = 0.05

# Define PARAMS using input data
PARAMS = pd.DataFrame(
    list(itertools.product(STOCKS, START_DATES, END_DATES, INTERVALS, STRATEGIES)),
    columns=["stock", "start_date", "end_date", "interval", "strategy"],
)
