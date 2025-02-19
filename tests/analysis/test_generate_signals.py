import numpy as np
import pandas as pd

from backtest_bay.analysis.generate_signals import _bollinger_signals


# Tests for _bollinger_signals
def test_bollinger_signals_constant_prices():
    prices = pd.Series([100] * 30)
    signals = _bollinger_signals(prices, window=20, num_std_dev=2)
    expected = pd.Series([0] * 30, index=prices.index)
    pd.testing.assert_series_equal(signals, expected)


def test_bollinger_signals_buy_signal():
    prices = pd.Series([100] * 20 + [90] + [100])
    signals = _bollinger_signals(prices, window=20, num_std_dev=2)
    buy_signal = 2
    assert signals.iloc[-1] == buy_signal


def test_bollinger_signals_sell_signal():
    prices = pd.Series([100] * 20 + [110] + [100])
    signals = _bollinger_signals(prices, window=20, num_std_dev=2)
    assert signals.iloc[-1] == 1


def test_bollinger_signals_window_effect():
    prices = pd.Series(np.linspace(100, 200, 25))
    signals_small_window = _bollinger_signals(prices, window=2, num_std_dev=1)
    signals_large_window = _bollinger_signals(prices, window=20, num_std_dev=1)
    assert not signals_small_window.equals(signals_large_window)


def test_bollinger_signals_single_price():
    prices = pd.Series([100])
    signals = _bollinger_signals(prices, window=20, num_std_dev=2)
    expected = pd.Series([0], index=prices.index)
    pd.testing.assert_series_equal(signals, expected)
