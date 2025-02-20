import numpy as np
import pandas as pd
import pytest

from backtest_bay.analysis.generate_signals import (
    _bollinger_signals,
    _macd_signals,
    _roc_signals,
    _rsi_signals,
    _validate_input_method,
    _validate_input_num_std_dev,
    _validate_input_window,
    _validate_window_relationships,
)


# Tests for _bollinger_signals
def test_bollinger_signals_correct_calculation():
    # do nothing
    prices = pd.Series([100, 100, 100, 100, 100])
    signals = _bollinger_signals(prices, window=2, num_std_dev=0.5)
    expected = pd.Series([0] * 5)
    pd.testing.assert_series_equal(signals, expected)

    # buy signal
    prices = pd.Series([100, 100, 50, 50, 50])
    signals = _bollinger_signals(prices, window=2, num_std_dev=0.5)
    expected = pd.Series([0, 0, 0, 2, 0])
    pd.testing.assert_series_equal(signals, expected)

    # sell signal
    prices = pd.Series([100, 100, 200, 200, 200])
    signals = _bollinger_signals(prices, window=2, num_std_dev=0.5)
    expected = pd.Series([0, 0, 0, 1, 0])
    pd.testing.assert_series_equal(signals, expected)


def test_bollinger_signals_window_effect():
    prices = pd.Series(np.linspace(100, 200, 25))
    signals_small_window = _bollinger_signals(prices, window=2, num_std_dev=1)
    signals_large_window = _bollinger_signals(prices, window=20, num_std_dev=1)
    assert not signals_small_window.equals(signals_large_window)


def test_bollinger_signals_single_price():
    prices = pd.Series([100])
    signals = _bollinger_signals(prices, window=20, num_std_dev=2)
    expected = pd.Series([0])
    pd.testing.assert_series_equal(signals, expected)


# Tests for _macd_signals
def test_macd_signals_correct_calculation():
    # do nothing
    prices = pd.Series([1] * 7)
    signals = _macd_signals(prices, short_window=2, long_window=3, signal_window=2)
    expected = pd.Series([0] * 7)
    pd.testing.assert_series_equal(signals, expected)

    # buy signal
    prices = pd.Series([1, 4, 8, 10, 12, 15, 20])
    signals = _macd_signals(prices, short_window=2, long_window=3, signal_window=2)
    expected = pd.Series([0, 0, 2, 2, 2, 2, 2])
    pd.testing.assert_series_equal(signals, expected)

    # sell signal
    prices = pd.Series([20, 15, 12, 10, 8, 4, 1])
    signals = _macd_signals(prices, short_window=2, long_window=3, signal_window=2)
    expected = pd.Series([0, 0, 1, 1, 1, 1, 1])
    pd.testing.assert_series_equal(signals, expected)


def test_macd_signals_window_effect():
    prices = pd.Series([1, 2, 1, 1, 2, 5, 4, 2, 4, 2, 1] * 5)
    window_1 = _macd_signals(prices, short_window=4, long_window=10, signal_window=4)
    window_2 = _macd_signals(prices, short_window=4, long_window=15, signal_window=4)
    window_3 = _macd_signals(prices, short_window=4, long_window=10, signal_window=2)
    assert not window_1.equals(window_2)
    assert not window_1.equals(window_3)
    assert not window_2.equals(window_3)


def test_macd_signals_single_price():
    prices = pd.Series([100])
    signals = _macd_signals(prices, short_window=2, long_window=3, signal_window=2)
    expected = pd.Series([0])
    pd.testing.assert_series_equal(signals, expected)


# Tests for _roc_signals
def test_roc_signlas_correct_calculation():
    # do nothing
    prices = pd.Series([1] * 4)
    signals = _roc_signals(prices, window=2)
    expected = pd.Series([0] * 4)
    pd.testing.assert_series_equal(signals, expected)

    # buy signal
    prices = pd.Series([2, 3, 3, 3])
    signals = _roc_signals(prices, window=2)
    expected = pd.Series([0, 0, 2, 0])
    pd.testing.assert_series_equal(signals, expected)

    # sell signal
    prices = pd.Series([2, 1, 1, 1])
    signals = _roc_signals(prices, window=2)
    expected = pd.Series([0, 0, 1, 0])
    pd.testing.assert_series_equal(signals, expected)


def test_roc_signals_window_effect():
    prices = pd.Series([2, 1, 1, 1])
    window_1 = _roc_signals(prices, window=2)
    window_2 = _roc_signals(prices, window=3)
    assert not window_1.equals(window_2)


def test_roc_signals_single_price():
    prices = pd.Series([1])
    signals = _roc_signals(prices, window=2)
    expected = pd.Series([0])
    pd.testing.assert_series_equal(signals, expected)


# Tests for _rsi_signals
def test_rsi_signlas_correct_calculation():
    # do nothing
    prices = pd.Series([1] * 4)
    signals = _rsi_signals(prices, window=2)
    expected = pd.Series([0] * 4)
    pd.testing.assert_series_equal(signals, expected)

    # buy
    prices = pd.Series([3, 2, 1, 0])
    signals = _rsi_signals(prices, window=2)
    expected = pd.Series([0, 0, 2, 2])
    pd.testing.assert_series_equal(signals, expected)

    # sell
    prices = pd.Series([0, 1, 2, 3])
    signals = _rsi_signals(prices, window=2)
    expected = pd.Series([0, 0, 1, 1])
    pd.testing.assert_series_equal(signals, expected)


def test_rsi_signals_window_effect():
    prices = pd.Series([5, 1, 2, 3, 4, 5])
    window_1 = _rsi_signals(prices, window=2)
    window_2 = _rsi_signals(prices, window=3)
    assert not window_1.equals(window_2)


def test_rsi_signals_single_price():
    prices = pd.Series([100])
    signals = _rsi_signals(prices, window=2)
    expected = pd.Series([0])
    pd.testing.assert_series_equal(signals, expected)


# Tests for _validate_window
def test_validate_input_window_valid_input():
    window = 10
    _validate_input_window(window)


def test_validate_input_window_invalid_input():
    window = "invalid"
    match = f"'window' must be an integer, got {type(window).__name__}."
    with pytest.raises(TypeError, match=match):
        _validate_input_window(window)

    window = 10.2
    match = f"'window' must be an integer, got {type(window).__name__}."
    with pytest.raises(TypeError, match=match):
        _validate_input_window(window)

    window = 1
    match = f"'window' must be greater than 1, got {window}."
    with pytest.raises(ValueError, match=match):
        _validate_input_window(window)


# Tests for _validate_input_num_std_dev
def test_validate_input_num_std_dev_valid_input():
    num_std_dev = 1
    _validate_input_num_std_dev(num_std_dev)
    num_std_dev = 1.2
    _validate_input_num_std_dev(num_std_dev)


def test_validate_input_num_std_dev_invalid_input():
    num_std_dev = "invalid"
    match = f"'num_std_dev' must be a number, got {type(num_std_dev).__name__}."
    with pytest.raises(TypeError, match=match):
        _validate_input_num_std_dev(num_std_dev)

    num_std_dev = -1
    match = f"'num_std_dev' must be a positive number, got {num_std_dev}."
    with pytest.raises(ValueError, match=match):
        _validate_input_num_std_dev(num_std_dev)


# Tests for _validate_window_relationships
def test_validate_window_relationships_valid_relation():
    short_window = 5
    long_window = 15
    signal_window = 5
    _validate_window_relationships(short_window, long_window, signal_window)


def test_validate_window_relationships_invalid_relation():
    short_window = 5
    long_window = 15
    signal_window = 6

    match = (
        "'signal_window' must be less than or equal to 'short_window',"
        f"got signal_window={signal_window} and short_window={short_window}."
    )
    with pytest.raises(ValueError, match=match):
        _validate_window_relationships(short_window, long_window, signal_window)

    short_window = 4
    long_window = 2
    signal_window = 4

    match = (
        "'short_window' must be less than 'long_window', "
        f"got short_window={short_window} and long_window={long_window}."
    )
    with pytest.raises(ValueError, match=match):
        _validate_window_relationships(short_window, long_window, signal_window)


# Tests for _validate_input_method
@pytest.mark.parametrize("method", ["bollinger", "macd", "roc", "rsi"])
def test_validate_input_method_valid_input(method):
    _validate_input_method(method)


@pytest.mark.parametrize("method", [123, 3.14, True, None])
def test_validate_input_method_invalid_type(method):
    match = f"Invalid type for method: expected str, got {type(method).__name__}."
    with pytest.raises(TypeError, match=match):
        _validate_input_method(method)


@pytest.mark.parametrize("method", ["invalid", "BoLLinger", "rsi_signal", ""])
def test_validate_input_method_invalid_value(method):
    match = f"Invalid method '{method}'."
    with pytest.raises(ValueError, match=match):
        _validate_input_method(method)
