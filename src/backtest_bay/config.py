"""Configuration file for backtesting trading strategies.

Parameters:
    STOCKS (list of str): List of stock symbols to fetch data for.
    START_DATE (str): Start date for fetching historical stock data
        (format: "YYYY-MM-DD").
    END_DATE (str): End date for fetching historical stock data (format: "YYYY-MM-DD").
    INTERVAL (str): Time interval for stock data (e.g., "1d", "1wk", "1mo").
    STRATEGIES (list of str): List of trading strategies to evaluate.
        Possible values: ["bollinger", "macd", "roc", "rsi"].
    INITIAL_CASH (int): Initial amount of cash available for trading.
    TAC (float): Transaction cost per trade, represented as a fraction
        (e.g., 0.005 for 0.5%).
    TRADE_PCT (float): Percentage of available capital to invest per trade
        (e.g., 0.05 for 5%).
"""

from pathlib import Path

SRC = Path(__file__).parent.resolve()
ROOT = SRC.joinpath("..", "..").resolve()

BLD = ROOT.joinpath("bld").resolve()

# Data source
STOCKS = ["AAPL", "MSFT"]
START_DATE = "2019-01-01"
END_DATE = "2025-01-01"
INTERVAL = "1d"

# Trading strategies
STRATEGIES = ["bollinger", "macd", "roc", "rsi"]

# Trading parameters
INITIAL_CASH = 1000000
TAC = 0.005
TRADE_PCT = 0.05
