import numpy as np
import pandas as pd
import pytest

from backtest_bay.plot.plot_portfolio import (
    _calculate_annualized_return,
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
    """Check if calculated return equals expected value."""
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
    result = _calculate_trades(shares)
    assert result == expected
