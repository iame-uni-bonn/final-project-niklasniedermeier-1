# BacktestBay

BacktestBay is a Python-based framework for backtesting trading strategies. It leverages
[yfinance](https://pypi.org/project/yfinance/) for importing financial data.

## Getting Started

To get started, first clone the repository using the following command:

```bash
git clone repository-url
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

## Configuration

BacktestBay enables the configuration of input parameters through
[config.py](https://github.com/iame-uni-bonn/final-project-niklasniedermeier-1/blob/main/src/backtest_bay/config.py).

First, the data source is specified in more detail in the configuration file:

```python
STOCKS = ["AAPL", "MSFT"]
START_DATE = "2019-01-01"
END_DATE = "2025-01-01"
INTERVAL = "1d"
```

Multiple valid symbols from [yfinance](https://pypi.org/project/yfinance/) can be added
to the `STOCKS` list. `START_DATE` and `END_DATE` define the time range for the price
history of the selected `STOCKS` at a specified `INTERVAL`. The available options for
`INTERVAL` are listed at the end of the README file.

In the next step, multiple trading strategies can be added to the `STRATEGIES` list:

```python
STRATEGIES = ["bollinger", "macd", "roc", "rsi"]
```

Each trading strategy is backtested on the stocks specified in the `STOCKS` list. The
following trading strategies are currently implemented:

- 'bollinger':
  [Bollinger Bands](https://www.investopedia.com/terms/b/bollingerbands.asp)
- 'macd':
  [Moving Average Convergence Divergence](https://www.investopedia.com/terms/m/macd.asp)
- 'roc': [Rate of Change](https://www.investopedia.com/terms/p/pricerateofchange.asp)
- 'rsi': [Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp)

Finally, additional backtesting parameters can be specified

```python
INITIAL_CASH = 1000000
TAC = 0.005
TRADE_PCT = 0.05
```

providing users with greater control and flexibility in their backtesting process.
`INITIAL_CASH` specifies the amount of cash available at the start. `TAC` specifies the
transaction costs as a percentage of the traded volume. `TRADE_PCT` indicates the
percentage of the current portfolio allocated for trading.

The initialization of the project with `pytask` creates a `bld/plot` folder in the
repository, where two analyses are generated for each stock in `STOCKS`:

- **`portfolio`**: Shows the development of the portfolio over time, including
  performance metrics.
- **`signals`**: Provides a detailed analysis of the signals in relation to the price
  trend.

## Project Structure

The project structure in `src/backtest_bay` is as follows:

- **`download_data`**: Contains functions to download `STOCKS`.
- **`backtest`**: Develops functions to generate trading signals and backtest them.
- **`plot`**: Plots portfolio performance.

## yfinance Download Intervals and Maximum History

| INTERVAL | Description | Maximum History Available           |
| -------- | ----------- | ----------------------------------- |
| `1m`     | 1 minute    | **7 days**                          |
| `2m`     | 2 minutes   | **60 days**                         |
| `5m`     | 5 minutes   | **60 days**                         |
| `15m`    | 15 minutes  | **60 days**                         |
| `30m`    | 30 minutes  | **60 days**                         |
| `60m`    | 60 minutes  | **730 days (2 years)**              |
| `90m`    | 90 minutes  | **730 days (2 years)**              |
| `1h`     | 1 hour      | **730 days (2 years)**              |
| `1d`     | 1 day       | **Max available (up to 50+ years)** |
| `5d`     | 5 days      | **Max available (up to 50+ years)** |
| `1wk`    | 1 week      | **Max available (up to 50+ years)** |
| `1mo`    | 1 month     | **Max available (up to 50+ years)** |
| `3mo`    | 3 months    | **Max available (up to 50+ years)** |

### Notes:

- Intraday data (`< 1d`) is typically only available for the last **60 days**, except
  for `1m`, which is limited to the last **7 days**.
- Daily, weekly, and monthly data can be downloaded for the maximum history available,
  which may go back **50+ years** depending on the stock.
- For intervals `60m`, `90m`, and `1h`, data is available for up to **2 years**.
- These limitations are set by Yahoo Finance, and attempting to request more data than
  allowed will result in an error or incomplete data.
