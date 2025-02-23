import pandas as pd
import pandas.testing as pdt
import pytest

from backtest_bay.backtest.backtest_signals import (
    _execute_buy,
    _execute_sell,
    _is_buy_trade_affordable,
    _is_sell_trade_affordable,
    _update_portfolio,
    _validate_initial_cash,
    _validate_price_col,
    _validate_tac,
    _validate_trade_pct,
    backtest_signals,
    merge_data_with_backtest_portfolio,
)


# tests for backtest_signals
def test_backtest_portfolio_correct_calculation():
    """Test backtest_portfolio for correct calculation."""
    index = pd.date_range("2023-01-01", periods=5, freq="D")
    data = pd.DataFrame({"Close": [10, 5, 10, 8, 10]}, index=index)

    # Only hold
    signals = pd.Series([0, 0, 0, 0, 0])
    portfolio = backtest_signals(
        data, signals, initial_cash=100, tac=0, trade_pct=1.0, price_col="Close"
    )
    expected_portfolio = pd.DataFrame(
        data={
            "price": [10, 5, 10, 8, 10],
            "signal": [0, 0, 0, 0, 0],
            "shares": [0, 0, 0, 0, 0],
            "holdings": [0, 0, 0, 0, 0],
            "cash": [100, 100, 100, 100, 100],
            "assets": [100, 100, 100, 100, 100],
        },
        index=index,
    )
    pdt.assert_frame_equal(portfolio, expected_portfolio)

    # Buy once
    signals = pd.Series([0, 2, 0, 0, 0])
    portfolio = backtest_signals(
        data, signals, initial_cash=100, tac=0, trade_pct=1.0, price_col="Close"
    )
    expected_portfolio = pd.DataFrame(
        data={
            "price": [10, 5, 10, 8, 10],
            "signal": [0, 2, 0, 0, 0],
            "shares": [0, 20, 20, 20, 20],
            "holdings": [0, 100, 200, 160, 200],
            "cash": [100, 0, 0, 0, 0],
            "assets": [100, 100, 200, 160, 200],
        },
        index=index,
    )
    pdt.assert_frame_equal(portfolio, expected_portfolio)

    # Buy and sell once
    signals = pd.Series([0, 2, 0, 0, 1])
    portfolio = backtest_signals(
        data, signals, initial_cash=100, tac=0, trade_pct=1.0, price_col="Close"
    )
    expected_portfolio = pd.DataFrame(
        data={
            "price": [10, 5, 10, 8, 10],
            "signal": [0, 2, 0, 0, 1],
            "shares": [0, 20, 20, 20, 4],
            "holdings": [0, 100, 200, 160, 40],
            "cash": [100, 0, 0, 0, 160],
            "assets": [100, 100, 200, 160, 200],
        },
        index=index,
    )
    pdt.assert_frame_equal(portfolio, expected_portfolio)


# tests for _is_buy_affordable
def test_is_buy_trade_affordable_enough_cash():
    """Test buying when there is enough cash."""
    affordable = _is_buy_trade_affordable(buy_shares=2, cost=10, cash=10)
    assert affordable


def test_is_buy_trade_affordable_not_enough_cash():
    """Test buying when there is not enough cash."""
    affordable = _is_buy_trade_affordable(buy_shares=2, cost=10, cash=9)
    assert not affordable


# tests for _execute_buy
def test_execute_buy_enough_cash():
    """Test buying when there is enough cash to purchase at least one share."""
    cash, shares = _execute_buy(cash=30, price=2, shares=2, trade_vol=30, tac=0.5)
    expected_cash, expected_shares = 0, 12
    assert cash == expected_cash
    assert shares == expected_shares


def test_execute_buy_to_less_cash():
    """Test buying when there isn't enough cash to purchase at least one share."""
    cash, shares = _execute_buy(cash=20, price=2, shares=2, trade_vol=30, tac=0.5)
    expected_cash, expected_shares = 20, 2
    assert cash == expected_cash
    assert shares == expected_shares


# tests for _is_sell_trade_affordable
def test_is_sell_trade_affordable_enough_shares():
    """Test selling when there are enough shares."""
    affordable = _is_sell_trade_affordable(shares=1)
    assert affordable


def test_is_sell_trade_affordable_not_enough_shares():
    """Test selling when there are not enough shares."""
    affordable = _is_sell_trade_affordable(shares=0)
    assert not affordable


# tests for _execute_sell
def test_execute_sell_enough_shares():
    """Test selling when there are enough shares."""
    cash, shares = _execute_sell(cash=40, price=2, shares=50, trade_vol=30, tac=0.5)
    expected_cash, expected_shares = 70, 20
    assert cash == expected_cash
    assert shares == expected_shares

    cash, shares = _execute_sell(cash=40, price=2, shares=8, trade_vol=30, tac=0.5)
    expected_cash, expected_shares = 48, 0
    assert cash == expected_cash
    assert shares == expected_shares


def test_execute_sell_not_enough_shares():
    """Test selling when there are not enough shares."""
    cash, shares = _execute_sell(cash=40, price=2, shares=0, trade_vol=30, tac=0.5)
    expected_cash, expected_shares = 40, 0
    assert cash == expected_cash
    assert shares == expected_shares


# tests for _update_portfolio
def test_update_portfolio_correct_calculation():
    """Test _update_portfolio for correct calculation."""
    assets, holdings = _update_portfolio(cash=100, shares=5, price=20)
    expected_assets, expected_holdings = 200, 100
    assert assets == expected_assets
    assert holdings == expected_holdings


# Tests for _validate_initial_cash
@pytest.mark.parametrize("initial_cash", [1000, 1000.50, 0.01])
def test_validate_initial_cash_valid_input(initial_cash):
    """Test valid initial_cash values."""
    _validate_initial_cash(initial_cash)


@pytest.mark.parametrize(
    ("initial_cash", "expected_error"),
    [
        (0, "initial_cash must be a positive number."),  # Zero value
        ("1000", "initial_cash must be a number, got str."),  # String
    ],
)
def test_validate_initial_cash_invalid_input(initial_cash, expected_error):
    """Test invalid initial_cash values."""
    with pytest.raises((TypeError, ValueError), match=expected_error):
        _validate_initial_cash(initial_cash)


# Tests for _validate_tac
@pytest.mark.parametrize("tac", [0, 0.05, 1])
def test_validate_tac_valid_input(tac):
    """Test valid tac values."""
    _validate_tac(tac)


@pytest.mark.parametrize(
    ("tac", "expected_error"),
    [
        (-0.01, "tac must be between 0 and 1."),
        (1.2, "tac must be between 0 and 1."),
        ("0.05", "tac must be a number, got str."),
    ],
)
def test_validate_tac_invalid_input(tac, expected_error):
    """Test invalid tac values."""
    with pytest.raises((TypeError, ValueError), match=expected_error):
        _validate_tac(tac)


# Tests for _validate_trade_pct
@pytest.mark.parametrize("trade_pct", [0.01, 0.5, 1.0])
def test_validate_trade_pct_valid_input(trade_pct):
    """Test valid trade_pct values."""
    _validate_trade_pct(trade_pct)


@pytest.mark.parametrize(
    ("trade_pct", "expected_error"),
    [
        (0.0, "trade_pct must be between 0 and 1. Zero is not possible."),
        (-1.0, "trade_pct must be between 0 and 1. Zero is not possible."),
        (1, "trade_pct must be a float, got int."),
    ],
)
def test_validate_trade_pct_invalid_input(trade_pct, expected_error):
    """Test invalid trade_pct values."""
    with pytest.raises((TypeError, ValueError), match=expected_error):
        _validate_trade_pct(trade_pct)


# Tests for _validate_price_col
@pytest.mark.parametrize(
    ("data", "price_col"),
    [
        (pd.DataFrame({"Close": [100, 101, 102]}), "Close"),
        (pd.DataFrame({"Open": [99, 100, 101], "Close": [100, 101, 102]}), "Close"),
        (pd.DataFrame({"Close": [100.5, 101.2, 102.1, 103.8]}), "Close"),
    ],
)
def test_validate_data_valid_input(data, price_col):
    """Test valid data input for _validate_data."""
    _validate_price_col(data, price_col)


# Tests for merge_data_with_backtest_portfolio
@pytest.mark.parametrize(
    ("data", "portfolio", "expected"),
    [
        (
            pd.DataFrame({"price": [10, 6]}, index=["2023-01-01", "2023-01-02"]),
            pd.DataFrame({"signal": [1, 0]}, index=["2023-01-01", "2023-01-02"]),
            pd.DataFrame(
                {"price": [10, 6], "signal": [1, 0]}, index=["2023-01-01", "2023-01-02"]
            ),
        ),
        (
            pd.DataFrame({"price": [5, 44]}, index=["2023-05-01", "2023-05-08"]),
            pd.DataFrame({"signal": [1, 1]}, index=["2023-05-01", "2023-05-08"]),
            pd.DataFrame(
                {"price": [5, 44], "signal": [1, 1]}, index=["2023-05-01", "2023-05-08"]
            ),
        ),
    ],
)
def test_merge_data_with_backtest_portfolio(data, portfolio, expected):
    "Test correct merge for merge_data_with_backtest_portfolio."
    result = merge_data_with_backtest_portfolio(data, portfolio)
    result.equals(expected)
