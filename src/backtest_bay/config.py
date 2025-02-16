"""All the general configuration of the project."""

from pathlib import Path

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()

BLD = ROOT.joinpath("bld").resolve()

# Configure input data
STOCKS = ["AAPL", "MSFT"]
START_DATES = ["2022-01-01", "2022-01-01"]
END_DATES = ["2025-01-01", "2025-01-01"]
INTERVALS = ["1d", "1d"]
