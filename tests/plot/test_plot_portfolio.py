import numpy as np
import pandas as pd
import pytest

from backtest_bay.plot.plot_portfolio import (
    _buy_and_hold_strategy,
    _calculate_annualized_return,
    _calculate_annualized_volatility,
    _calculate_portfolio_return,
    _calculate_trades,
    _calculate_years,
)


# Tests for _calculate_portfolio_return
@pytest.mark.parametrize(
    ("stock", "expected_return"),
    [
        (pd.Series([100]), 0.0),
        (pd.Series([100, 150]), 50.0),
        (pd.Series([200, 100]), -50.0),
        (pd.Series([100, 100]), 0.0),
        (pd.Series([50, 75, 100]), 100.0),
    ],
)
def test_calculate_portfolio_return_valid_calculation(stock, expected_return):
    """Test if _calculate_portfolio_return returns the correct return value."""
    result = _calculate_portfolio_return(stock)
    assert result == expected_return


# Tests for _calculate_years
@pytest.mark.parametrize(
    ("index", "expected"),
    [
        (pd.to_datetime(["2020-01-01", "2020-12-31"]), 1),
        (pd.to_datetime(["2020-01-01", "2020-07-01"]), 0.5),
        (pd.to_datetime(["2010-01-01", "2020-01-01"]), 10),
        (pd.to_datetime(["2020-01-01", "2020-01-01"]), 0),
        (pd.to_datetime(["2020-01-01  00:00:00", "2020-01-01  12:00:00"]), 0.5 / 365),
    ],
)
def test_calculate_years(index, expected):
    """Test if _calculate_years correctly computes the number of years."""
    result = _calculate_years(index)
    assert np.isclose(result, expected, atol=1e-2)


# Tests for _calculate_annualized_return
@pytest.mark.parametrize(
    ("stock", "expected"),
    [
        (
            pd.Series(
                [100, 100, 100],
                index=pd.to_datetime(["2020-01-01", "2020-07-01", "2021-01-01"]),
            ),
            0,
        ),
        (
            pd.Series([100, 110], index=pd.to_datetime(["2020-01-01", "2021-01-01"])),
            10.00,
        ),
        (
            pd.Series([200, 100], index=pd.to_datetime(["2020-01-01", "2021-01-01"])),
            -50.00,
        ),
        (
            pd.Series([100, 200], index=pd.to_datetime(["2018-01-01", "2021-01-01"])),
            round(((200 / 100) ** (1 / 3) - 1) * 100, 2),
        ),
    ],
)
def test_calculate_annualized_return(stock, expected):
    """Test if _calculate_annualized_return correctly calculates annualized returns."""
    result = _calculate_annualized_return(stock)
    assert np.isclose(result, expected, atol=1e-1)


# Tests for _calculate_trades
@pytest.mark.parametrize(
    ("shares", "expected"),
    [
        (pd.Series([10, 10, 10, 10]), 0),
        (pd.Series([0, 10, 0, 10, 0]), 4),
        (pd.Series([0, -10, 0, 0, 0]), 2),
    ],
)
def test_calculate_trades(shares, expected):
    """Test if _calculate_trades correctly counts the number of trades."""
    result = _calculate_trades(shares)
    assert result == expected


# Tests for _calculate_annualized_volatility
@pytest.mark.parametrize(
    ("stock_prices", "expected_volatility"),
    [
        ([100, 100, 100, 100, 100], 0),
        ([100, 101, 102, 103, 104], pytest.approx(2.26, rel=1e-2)),
        ([100], 0),
    ],
)
def test_calculate_annualized_volatility(stock_prices, expected_volatility):
    """Test if _calculate_annualized_volatility correctly calculates annualized
    volatility."""
    stock = pd.Series(
        stock_prices, index=pd.date_range(start="2022-01-01", periods=len(stock_prices))
    )
    result = _calculate_annualized_volatility(stock)
    assert result == expected_volatility


# Tests for _buy_and_hold_strategy
@pytest.mark.parametrize(
    ("initial_cash", "prices", "expected"),
    [
        # Enough cash
        (105, pd.Series([10, 12, 15, 18]), pd.Series([105.0, 125.0, 155.0, 185.0])),
        #  Not enough cash to buy even one share
        (5, pd.Series([10, 12, 15, 18]), pd.Series([5.0, 5.0, 5.0, 5.0])),
        # Cash exactly enough to buy one share
        (10, pd.Series([10, 12, 15, 18]), pd.Series([10.0, 12.0, 15.0, 18.0])),
    ],
)
def test_buy_and_hold_strategy_correct_calculation(initial_cash, prices, expected):
    """Test if _buy_and_hold_strategy correctly calculates buy and hold strategy."""
    result = _buy_and_hold_strategy(initial_cash, prices)
    pd.testing.assert_series_equal(result, expected)
