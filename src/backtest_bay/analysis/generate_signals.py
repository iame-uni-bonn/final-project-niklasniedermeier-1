import pandas as pd


def generate_signals(data, method, **kwargs):
    """Derive trading signals using the specified method and parameters.

    Args:
        data (pd.DataFrame): DataFrame containing asset price data
            (must include 'Close' column).
        method (str): The signal generation method. Currently supported:
             - 'bollinger_bands': Uses Bollinger Bands for signal generation.
        **kwargs: Additional parameters specific to the chosen method.

    Returns:
        pd.Series: Trading signals (2: buy, 1: sell, 0: do nothing).
    """
    _validate_input_method(method)
    closing_prices = data["Close"].squeeze()

    if method == "bollinger":
        signal = _bollinger_signals(prices=closing_prices, **kwargs)
    if method == "macd":
        signal = _macd_signals(prices=closing_prices, **kwargs)
    if method == "roc":
        signal = _roc_signals(prices=closing_prices, **kwargs)
    if method == "rsi":
        signal = _rsi_signals(prices=closing_prices, **kwargs)
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
    _validate_input_bollinger_signals(window, num_std_dev)

    moving_avg = prices.rolling(window=window).mean()
    std_dev = prices.rolling(window=window).std()
    upper_band = moving_avg + (num_std_dev * std_dev)
    lower_band = moving_avg - (num_std_dev * std_dev)

    signals = pd.Series(0, index=prices.index)
    signals.loc[prices < lower_band] = 2
    signals.loc[prices > upper_band] = 1

    signals = signals.shift(periods=1, fill_value=0)
    return signals


def _macd_signals(prices, short_window=12, long_window=26, signal_window=9):
    """Generate trading signals based on the MACD indicator.

    A buy signal (2) is generated when the MACD line crosses above the Signal Line.
    A sell signal (1) is generated when the MACD line crosses below the Signal Line.

    Args:
        prices (pd.Series): Series of asset prices.
        short_window (int): Window size for the short EMA (default: 12).
        long_window (int): Window size for the long EMA (default: 26).
        signal_window (int): Window size for the signal line EMA (default: 9).

    Returns:
        pd.Series: Trading signals (2: buy, 1: sell, 0: do nothing).
    """
    _validate_input_macd_signals(short_window, long_window, signal_window)

    short_ema = prices.ewm(span=short_window, adjust=False).mean()
    long_ema = prices.ewm(span=long_window, adjust=False).mean()
    macd_line = short_ema - long_ema
    signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()

    signals = pd.Series(0, index=prices.index)
    signals.loc[macd_line > signal_line] = 2
    signals.loc[macd_line < signal_line] = 1

    signals = signals.shift(periods=1, fill_value=0)
    return signals


def _roc_signals(prices, window=10):
    """Generate trading signals based on the Rate of Change (ROC) indicator.

    A buy signal (2) is generated when the ROC is positive,
    and a sell signal (1) is generated when the ROC is negative.

    Args:
        prices (pd.Series): Series of asset prices.
        window (int): Window size for computing the ROC.

    Returns:
        pd.Series: Trading signals (2: buy, 1: sell, 0: do nothing).
    """
    _validate_input_window(window)

    roc = prices.pct_change(periods=window - 1)

    signals = pd.Series(0, index=prices.index, dtype=int)
    signals.loc[roc > 0] = 2
    signals.loc[roc < 0] = 1

    signals = signals.shift(periods=1, fill_value=0)
    return signals


def _rsi_signals(prices, window=14):
    """Generate trading signals based on the Relative Strength Index (RSI).

    A buy signal (2) is generated when RSI is below 30 (oversold),
    and a sell signal (1) is generated when RSI is above 70 (overbought).

    Args:
        prices (pd.Series): Series of asset prices.
        window (int): Window size for computing RSI.

    Returns:
        pd.Series: Trading signals (2: buy, 1: sell, 0: do nothing).
    """
    _validate_input_window(window)

    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    signals = pd.Series(0, index=prices.index, dtype=int)
    upper_cutoff = 70
    lower_cutoff = 30
    signals.loc[rsi < lower_cutoff] = 2
    signals.loc[rsi > upper_cutoff] = 1

    signals = signals.shift(periods=1, fill_value=0)
    return signals


def _validate_input_method(method):
    """Validate the input method for the `generate_signals` function.

    Args:
        method (str): The signal generation method.

    Raises:
        TypeError: If the method is not a string.
        ValueError: If the method is not one of the supported methods.
    """
    if not isinstance(method, str):
        error_msg = (
            f"Invalid type for method: expected str, got {type(method).__name__}."
        )
        raise TypeError(error_msg)

    supported_methods = ["bollinger", "macd", "roc", "rsi"]

    if method not in supported_methods:
        error_msg = (
            f"Invalid method '{method}'. "
            f"Supported methods are: {', '.join(supported_methods)}."
        )
        raise ValueError(error_msg)


def _validate_input_bollinger_signals(window, num_std_dev):
    """Validate inputs for the Bollinger Bands trading signal function.

    Args:
        window (int): Window size for moving average.
        num_std_dev (int, float): Number of standard deviations for the bands.
    """
    _validate_input_window(window)
    _validate_input_num_std_dev(num_std_dev)


def _validate_input_macd_signals(short_window, long_window, signal_window):
    """Validate inputs for the MACD trading signal function.

    Args:
        short_window (int): Window size for the short-term EMA.
        long_window (int): Window size for the long-term EMA.
        signal_window (int): Window size for the signal line EMA.
    """
    _validate_input_window(short_window)
    _validate_input_window(long_window)
    _validate_input_window(signal_window)
    _validate_window_relationships(short_window, long_window, signal_window)


def _validate_input_window(window):
    """Validate the window parameter.

    Args:
        window (int): Window size for moving average.

    Raises:
        TypeError: If window is not an integer.
        ValueError: If window is not greater than 1.
    """
    if not isinstance(window, int):
        error_msg = f"'window' must be an integer, got {type(window).__name__}."
        raise TypeError(error_msg)

    if window <= 1:
        error_msg = f"'window' must be greater than 1, got {window}."
        raise ValueError(error_msg)


def _validate_input_num_std_dev(num_std_dev):
    """Validate the num_std_dev parameter for Bollinger Bands.

    Args:
        num_std_dev (int, float): Number of standard deviations for the bands.

    Raises:
        TypeError: If num_std_dev is not a number.
        ValueError: If num_std_dev is not positive.
    """
    if not isinstance(num_std_dev, int | float):
        error_msg = f"'num_std_dev' must be a number, got {type(num_std_dev).__name__}."
        raise TypeError(error_msg)

    if num_std_dev <= 0:
        error_msg = f"'num_std_dev' must be a positive number, got {num_std_dev}."
        raise ValueError(error_msg)


def _validate_window_relationships(short_window, long_window, signal_window):
    """Validate logical relationships between MACD windows.

    Args:
        short_window (int): Window size for the short-term EMA.
        long_window (int): Window size for the long-term EMA.
        signal_window (int): Window size for the signal line EMA.

    Raises:
        ValueError: If:
            - `short_window` is greater than or equal to `long_window`.
            - `signal_window` is greater than `short_window`.
    """
    if short_window >= long_window:
        error_msg = (
            "'short_window' must be less than 'long_window', "
            f"got short_window={short_window} and long_window={long_window}."
        )
        raise ValueError(error_msg)

    if signal_window > short_window:
        error_msg = (
            "'signal_window' must be less than or equal to 'short_window',"
            f"got signal_window={signal_window} and short_window={short_window}."
        )
        raise ValueError(error_msg)
