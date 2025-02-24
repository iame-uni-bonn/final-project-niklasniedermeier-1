"""All the general configuration of the project."""

from pathlib import Path

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()

BLD = ROOT.joinpath("bld").resolve()

# Data source
STOCKS = ["AAPL", "MSFT"]
START_DATES = "2019-01-01"
END_DATES = "2025-01-01"
INTERVALS = "1d"

# Trading strategies
STRATEGIES = ["bollinger", "macd", "roc", "rsi"]

# Trading parameters
INITIAL_CASH = 1000000
TAC = 0.005
TRADE_PCT = 0.05
