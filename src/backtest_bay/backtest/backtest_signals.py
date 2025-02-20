import math

import pandas as pd


def backtest_signals(data, signals, initial_cash, tac, trade_pct, price_col="Close"):
    """Backtest trading signals to simulate portfolio performance.

    Args:
        data (pd.DataFrame): DataFrame containing asset price data.
            - Must include a column specified by `price_col` (default: 'Close').
            - The index should be datetime or sequential for portfolio tracking.
        signals (pd.Series): Series of trading signals.
            - 2: Buy Signal
            - 1: Sell Signal
            - 0: Do Nothing
        initial_cash (int, float): Initial cash available for trading.
        tac (int, float): Transaction cost as a percentage (e.g., 0.05 for 5%).
        trade_pct (float): Percentage of 'initial_cash' to trade per signal.
        price_col (str): Column name for the asset's price. Default is 'Close'.

    Returns:
        pd.DataFrame: Portfolio performance over time with columns:
            - 'price': The price of the stock.
            - 'signal': Trading signal used (2: Buy, 1: Sell, 0: Do Nothing).
            - 'shares': Number of shares.
            - 'holdings': Total value of shares (price * shares)
            - 'cash': Cash.
            - 'assets': Portfolio value (cash + holdings).
    """
    _validate_backtest_signals_input(
        data, signals, initial_cash, tac, trade_pct, price_col
    )

    prices = data[price_col].squeeze()
    cash, holdings, shares = initial_cash, 0.0, 0
    assets = cash + holdings
    portfolio = []

    for price, signal in zip(prices, signals, strict=False):
        trade_vol = trade_pct * assets
        cash, shares = _execute_trade(signal, cash, price, shares, trade_vol, tac)
        assets, holdings = _update_portfolio(cash, shares, price)
        portfolio.append((price, signal, shares, holdings, cash, assets))

    portfolio = pd.DataFrame(
        portfolio,
        columns=["price", "signal", "shares", "holdings", "cash", "assets"],
        index=data.index,
    )
    return portfolio


def _execute_trade(signal, cash, price, shares, trade_vol, tac):
    """Execute a trade based on the trading signal.

    Args:
        signal (int): Current trading signal.
        cash (int, float): Current cash.
        price (float): Current price of the stock.
        shares (int): Current shares.
        trade_vol (float): Volume of portfolio to trade.
        tac (int, float): Transaction cost.

    Returns:
        tuple: Updated cash and shares after the trade.
    """
    buy_signal = 2
    sell_signal = 1

    if signal == buy_signal:
        cash, shares = _execute_buy(cash, price, shares, trade_vol, tac)

    elif signal == sell_signal:
        cash, shares = _execute_sell(cash, price, shares, trade_vol, tac)

    return cash, shares


def _execute_buy(cash, price, shares, trade_vol, tac):
    """Execute a buy trade.

    Args:
        cash (int, float): Current cash.
        price (float): Current price of the asset.
        shares (int): Current shares.
        trade_vol (float): Volume of portfolio to trade.
        tac (float): Transaction cost.

    Returns:
        tuple: Updated cash and shares after the buy trade.
            - cash (float): Remaining cash after the trade.
            - shares (int): Updated number of shares held.
    """
    buy_shares = math.floor(trade_vol / (price * (1 + tac)))
    cost = buy_shares * price * (1 + tac)

    if not _is_buy_trade_affordable(buy_shares, cost, cash):
        return cash, shares

    cash -= cost
    shares += buy_shares
    return cash, shares


def _is_buy_trade_affordable(buy_shares, cost, cash):
    """Check if the buy trade is affordable.

    Args:
        buy_shares (int): Number of shares to buy.
        cost (int, float): Total cost of the shares.
        cash (int, float): Current cash.

    Returns:
        bool: True if the trade is affordable, False otherwise.
    """
    is_trade_vol_enough = buy_shares >= 1
    is_cash_enough = cash >= cost
    return is_trade_vol_enough and is_cash_enough


def _execute_sell(cash, price, shares, trade_vol, tac):
    """Execute a sell trade.

    Args:
        cash (float): Current cash.
        price (float): Current price.
        shares (int):  Current shares.
        trade_vol (float): Volume of portfolio to trade.
        tac (float): Transaction cost.

    Returns:
        tuple: Updated cash and shares after the sell trade.
            - cash (float): Updated cash.
            - shares (int): Updated shares.
    """
    sell_shares = math.floor(trade_vol / (price * (1 - tac)))

    if not _is_sell_trade_affordable(shares):
        return cash, shares

    sell_shares = min(sell_shares, shares)

    profit = sell_shares * price * (1 - tac)
    cash += profit
    shares -= sell_shares
    return cash, shares


def _is_sell_trade_affordable(shares):
    """Checks if there are enough shares to sell."""
    return shares >= 1


def _update_portfolio(cash, shares, price):
    """Updates holdings and assets after trade."""
    holdings = shares * price
    assets = cash + holdings
    return assets, holdings


def _validate_backtest_signals_input(
    data, signals, initial_cash, tac, trade_pct, price_col
):
    """Validates input for backtesting signals."""
    _validate_data(data, price_col)
    _validate_signals(signals, data, price_col)
    _validate_initial_cash(initial_cash)
    _validate_tac(tac)
    _validate_trade_pct(trade_pct)


def _validate_data(data, price_col):
    """Validate the input data for backtesting.

    Args:
        data (pd.DataFrame): DataFrame containing stock data.
        price_col (str): Column name for the stock price.

    Raises:
        TypeError: If data is not a pandas DataFrame.
        ValueError: If the price column is missing or contains non-numeric values.
    """
    if not isinstance(data, pd.DataFrame):
        error_msg = f"data must be a pandas DataFrame, got {type(data).__name__}."
        raise TypeError(error_msg)

    if price_col not in data.columns:
        error_msg = f"data must contain a '{price_col}' column."
        raise ValueError(error_msg)

    if not pd.api.types.is_numeric_dtype(data[price_col].squeeze()):
        error_msg = f"The '{price_col}' column must contain numeric values."
        raise ValueError(error_msg)


def _validate_signals(signals, data, price_col):
    """Validate the trading signals.

    Args:
        signals (pd.Series): Trading signals for backtesting.
        data (pd.DataFrame): DataFrame containing stock data.
        price_col (str): Column name for the stock price.

    Raises:
        TypeError: If signals is not a pandas Series.
        ValueError: If signals contain invalid values.
        ValueError: If signals do not match the length of the price column.
    """
    if not isinstance(signals, pd.Series):
        error_msg = f"signals must be a pandas Series, got {type(signals).__name__}."
        raise TypeError(error_msg)

    if not all(isinstance(signal, int) for signal in signals):
        error_msg = "signals must contain only integers."
        raise ValueError(error_msg)

    if not all(signal in [0, 1, 2] for signal in signals):
        error_msg = "signals must contain only 0 (Hold), 1 (Sell), or 2 (Buy)."
        raise ValueError(error_msg)

    if len(signals) != len(data[price_col]):
        error_msg = f"signals must have the same length as the '{price_col}' column."
        raise ValueError(error_msg)


def _validate_initial_cash(initial_cash):
    """Validate the initial cash value for backtesting.

    Args:
        initial_cash (int or float): The initial cash available for trading.

    Raises:
        TypeError: If initial_cash is not an integer or float.
        ValueError: If initial_cash is not positive.
    """
    if not isinstance(initial_cash, int | float):
        error_msg = f"initial_cash must be a number, got {type(initial_cash).__name__}."
        raise TypeError(error_msg)
    if initial_cash <= 0:
        error_msg = "initial_cash must be a positive number."
        raise ValueError(error_msg)


def _validate_tac(tac):
    """Validate the transaction cost (tac) for backtesting.

    Args:
        tac (int or float): Transaction cost as a percentage.

    Raises:
        TypeError: If tac is not an integer or float.
        ValueError: If tac is negative or greater than 1.
    """
    if not isinstance(tac, int | float):
        error_msg = f"tac must be a number, got {type(tac).__name__}."
        raise TypeError(error_msg)

    if not (0 <= tac <= 1):
        error_msg = "tac must be between 0 and 1."
        raise ValueError(error_msg)


def _validate_trade_pct(trade_pct):
    """Validate the trade percentage (trade_pct) for backtesting.

    Args:
        trade_pct (float): Trade percentage of total assets per trade.

    Raises:
        TypeError: If trade_pct is not a float.
        ValueError: If trade_pct is not between 0 and 1.
    """
    if not isinstance(trade_pct, float):
        error_msg = f"trade_pct must be a float, got {type(trade_pct).__name__}."
        raise TypeError(error_msg)

    if not (0 < trade_pct <= 1):
        error_msg = "trade_pct must be between 0 and 1. Zero is not possible."
        raise ValueError(error_msg)
