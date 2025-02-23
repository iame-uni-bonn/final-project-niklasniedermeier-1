# BacktestBay: Evaluation of Trading Strategies

BacktestBay is a Python-based framework for backtesting trading strategies. It leverages
`yfinance` for importing financial data.

## Configuration

BacktestBay enables the configuration of input parameters through
[config.py](https://github.com/iame-uni-bonn/final-project-niklasniedermeier-1/blob/main/src/backtest_bay/config.py).

This configuration file allows for the customization of data source settings

```python
STOCKS = ["AAPL", "MSFT"]  # List of stock symbols from yfinance
START_DATES = ["2019-01-01"]  # Start date for historical data ("YYYY-MM_DD")
END_DATES = ["2025-01-01"]  # End date for historical data ("YYYY-MM_DD")
INTERVALS = ["1d"]  # Data frequency (e.g., daily)
```

and the choice of trading strategies

```python
STRATEGIES = ["bollinger", "macd", "roc", "rsi"]
```

as well as the adjustment of trading parameters

```python
INITIAL_CASH = 1000000  # Initial capital for trading
TAC = 0.005  # Transaction cost
TRADE_PCT = 0.05  # Percentage of current portfolio used per trade
```

providing users with enhanced control and flexibility in their backtesting process.

The following trading strategies are currently implemented

- 'bollinger':
  [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)
- 'macd':
  [Moving Average Convergence Divergence](https://www.investopedia.com/terms/m/macd.asp)
- 'roc': [Rate of Change](https://www.investopedia.com/terms/p/pricerateofchange.asp)
- 'rsi': [Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp)

## Getting Started

To get started, first clone the repository using the following command:

```bash
git clone <repository-url>
```

Next, create and activate the environment by navigating to the directory containing
`environment.yml` and running:

```bash
mamba env create -f environment.yml
mamba activate backtest_bay
```

Once the environment is set up, initialize the project by typing the following in the
project directory:

```bash
pytask
```
