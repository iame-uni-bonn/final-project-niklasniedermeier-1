import pandas as pd
import pytest

from backtest_bay.data.download_data import (
    _validate_date_format,
    _validate_date_range,
    _validate_interval,
    _validate_output,
    _validate_symbol,
)


# Tests for _validate_symbol
def test_validate_symbol_valid_cases():
    _validate_symbol("AAPL")


def test_validate_symbol_invalid_invalid_symbol():
    with pytest.raises(ValueError, match="Invalid symbol: 'INVALID'"):
        _validate_symbol("INVALID")


def test_validate_symbol_invalid_empty_string():
    with pytest.raises(ValueError, match="Invalid symbol: ''"):
        _validate_symbol("")


def test_validate_symbol_invalid_non_string():
    with pytest.raises(TypeError, match="Symbol must be a non-empty string."):
        _validate_symbol(123)


# Tests for _validate_date_format
@pytest.mark.parametrize(
    "interval",
    [
        "1m",
        "2m",
        "5m",
        "15m",
        "30m",
        "60m",
        "90m",
        "1h",
        "1d",
        "5d",
        "1wk",
        "1mo",
        "3mo",
    ],
)
def test_validate_interval_valid(interval):
    _validate_interval(interval)


def test_validate_interval_invalid():
    with pytest.raises(ValueError, match="Invalid interval.*"):
        _validate_interval("10m")


@pytest.mark.parametrize("invalid_interval", [None, "", " "])
def test_validate_interval_edge_cases(invalid_interval):
    with pytest.raises(ValueError, match="Invalid interval.*"):
        _validate_interval(invalid_interval)


# tests for _validate_date_format
@pytest.mark.parametrize(
    "valid_date",
    [
        "2023-01-01",
        "1999-12-31",
        "2024-02-29",  # Leap year
    ],
)
def test_validate_date_format_valid(valid_date):
    _validate_date_format(valid_date)


@pytest.mark.parametrize(
    "invalid_date",
    [
        "01-01-2023",  # Incorrect format
        "2023-13-01",  # Invalid month
        "2023-02-30",  # Invalid day
    ],
)
def test_validate_date_format_invalid(invalid_date):
    with pytest.raises(ValueError, match="Date must be in 'YYYY-MM-DD' format."):
        _validate_date_format(invalid_date)


def test_validate_date_format_non_string():
    match = "Date must be a string in 'YYYY-MM-DD' format."
    with pytest.raises(TypeError, match=match):
        _validate_date_format(12345)


# tests for _validate_date_range
def test_valid_date_range():
    _validate_date_range("2024-01-01", "2024-12-31")


def test_invalid_date_range():
    with pytest.raises(ValueError, match="Start date must be before end date."):
        _validate_date_range("2024-12-31", "2024-01-01")


# tests for _validate_output
def test_validate_output_valid_input():
    # generate typical Yahoo Finance output format
    symbol = "AAPL"
    arrays = [
        ["Close", "High", "Low", "Open", "Volume"],
        [symbol, symbol, symbol, symbol, symbol],
    ]
    index = pd.MultiIndex.from_tuples(
        list(zip(*arrays, strict=False)), names=["Price", "Ticker"]
    )

    data = pd.DataFrame(
        [[1, 10, 1, 4, 500], [2, 8, 2, 4, 500], [2, 4, 2, 5, 400], [3, 6, 2, 4, 200]],
        index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]),
        columns=index,
    )
    data.index.name = "Date"

    _validate_output(data, symbol, "2024-01-02", "2024-01-05", "1d")


def test_validate_output_empty_input():
    # generate typical Yahoo Finance output format
    symbol = "AAPL"
    arrays = [
        ["Close", "High", "Low", "Open", "Volume"],
        [symbol, symbol, symbol, symbol, symbol],
    ]
    index = pd.MultiIndex.from_tuples(
        list(zip(*arrays, strict=False)), names=["Price", "Ticker"]
    )

    empty_data = pd.DataFrame(columns=index)

    empty_data.index.name = "Date"

    match = "No data found for AAPL between 1800-01-01 and 1800-05-01."
    with pytest.raises(ValueError, match=match):
        _validate_output(empty_data, symbol, "1800-01-01", "1800-05-01", "1d")
