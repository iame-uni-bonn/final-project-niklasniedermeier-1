import numpy as np
import pandas as pd


def generate_signals(data, method, **kwargs):
    """Derive trading signals using the specified method and parameters.

    Args:
        data (pd.DataFrame): DataFrame containing asset price data
            (must include 'Close' column).
        method (str): The signal generation method. Currently supported:
             - 'bollinger_bands': Uses Bollinger Bands for signal generation.
        **kwargs: Additional parameters specific to the chosen method
            (e.g., window size, number of standard deviations).

    Returns:
        pd.Series: Trading signals (2: buy, 1: sell, 0: do nothing).
    """
    if method == "flip":
        signal = _flip_signals(prices=data["Close"].squeeze())
    if method == "bollinger":
        signal = _bollinger_signals(prices=data["Close"].squeeze(), **kwargs)
    return signal


def _bollinger_signals(prices, window=20, num_std_dev=2):
    """Generate anticyclical trading signals based on Bollinger Bands.

    Bollinger Bands are computed using a moving average and standard deviations
    to identify overbought (sell signal) and oversold (buy signal) conditions.

    Args:
        prices (pd.Series): Series of asset prices.
        window (int): Window size for Bollinger Bands calculation (default is 20).
        num_std_dev (float): Number of standard deviations for the bands (default is 2).

    Returns:
        pd.Series: Trading signals (2: buy, 1: sell, 0: do nothing).
    """
    moving_avg = prices.rolling(window=window).mean().fillna(0)
    std_dev = prices.rolling(window=window).std()
    upper_band = moving_avg + (num_std_dev * std_dev)
    lower_band = moving_avg - (num_std_dev * std_dev)

    signals = pd.Series(0, index=prices.index)
    signals[prices < lower_band] = 2
    signals[prices > upper_band] = 1

    signals = _shift_signals_to_right(signals)
    return pd.Series(signals, index=prices.index)


def _flip_signals(prices):
    """Generate trading signals based on price changes from the previous price.

    Args:
        prices (np.Series): Series of asset prices without index.

    Returns:
        np.ndarray: Trading signals (2: buy if previous price is lower,
                    1: sell if previous price is higher,
                    0: do nothing for the first price).
    """
    price_diff = np.diff(prices, prepend=prices.iloc[0])
    signals = np.zeros(len(prices), dtype=int)
    signals[1:][price_diff[1:] > 0] = 1
    signals[1:][price_diff[1:] < 0] = 2
    return signals


def _shift_signals_to_right(signals, shift=1):
    return np.concatenate(([0] * shift, signals[:-shift]))
