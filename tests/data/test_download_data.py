import pandas as pd
import pytest

from backtest_bay.data.download_data import (
    _validate_data_empty,
    _validate_data_index_datetime,
    _validate_data_multiindex,
    _validate_data_numeric,
    _validate_data_type_dataframe,
    _validate_date_format,
    _validate_date_range,
    _validate_interval,
    _validate_symbol,
)


# Tests for _validate_symbol
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


# Test for _validate_data_type_dataframe
@pytest.mark.parametrize(
    "data",
    [
        pd.DataFrame({"Close": [100, 101], "Open": [99, 100]}),
        pd.DataFrame({"A": [], "B": []}),
    ],
)
def test_validate_data_type_dataframe_valid(data):
    """Test _validate_data_type_dataframe with valid DataFrame inputs."""
    _validate_data_type_dataframe(data)


@pytest.mark.parametrize("data", [[], {}, "string", 123, None])
def test_validate_data_type_dataframe_invalid(data):
    """Test _validate_data_type_dataframe with invalid inputs."""
    with pytest.raises(TypeError):
        _validate_data_type_dataframe(data)


# Test for _validate_data_empty
@pytest.mark.parametrize(
    "data",
    [
        pd.DataFrame({"Close": [100, 101], "Open": [99, 100]}),
        pd.DataFrame({"A": [1], "B": [2]}),
    ],
)
def test_validate_data_empty_valid(data):
    """Test _validate_data_empty with non-empty DataFrames."""
    _validate_data_empty(data, "AAPL", "2022-01-01", "2022-12-31", "1d")


@pytest.mark.parametrize(
    "data", [pd.DataFrame({"Close": [], "Open": []}), pd.DataFrame()]
)
def test_validate_data_empty_invalid(data):
    """Test _validate_data_empty with empty DataFrames."""
    match = (
        "No data found for AAPL between 2022-01-01 and 2022-12-31 with interval '1d'."
    )
    with pytest.raises(ValueError, match=match):
        _validate_data_empty(data, "AAPL", "2022-01-01", "2022-12-31", "1d")


# Test for _validate_data_index_datetime
@pytest.mark.parametrize(
    "index",
    [
        pd.DatetimeIndex(["2022-01-01", "2022-01-02"]),
        pd.DatetimeIndex(pd.date_range("2022-01-01", periods=3)),
    ],
)
def test_validate_data_index_datetime_valid(index):
    """Test _validate_data_index_datetime with valid DatetimeIndex."""
    _validate_data_index_datetime(index)


@pytest.mark.parametrize(
    "index",
    [
        pd.Index([1, 2, 3]),
        pd.Index(["a", "b", "c"]),
        pd.RangeIndex(0, 5),
        [1, 2, 3],
        None,
    ],
)
def test_validate_data_index_datetime_invalid(index):
    """Test _validate_data_index_datetime with invalid indexes."""
    with pytest.raises(TypeError):
        _validate_data_index_datetime(index)


# Test for _validate_data_multiindex
def test_validate_data_multiindex_valid():
    """Test _validate_data_multiindex with valid MultiIndex."""
    # Define input: Valid MultiIndex DataFrame with fixed, smaller values
    arrays = [["Close", "Open", "High", "Low"], ["AAPL", "AAPL", "AAPL", "AAPL"]]
    index = pd.MultiIndex.from_arrays(arrays, names=["Type", "Ticker"])

    # Smaller fixed dataset
    data = [[100, 99, 101, 98], [101, 100, 102, 99], [102, 101, 103, 100]]

    df = pd.DataFrame(data, columns=index)

    # Perform test
    _validate_data_multiindex(df.columns)


# Test for _validate_data_numeric
@pytest.mark.parametrize(
    "data",
    [
        pd.DataFrame(
            {
                "Close": [100.0, 101.0],
                "Open": [99.0, 100.0],
                "High": [101.0, 102.0],
                "Low": [98.0, 99.0],
            }
        ),
        pd.DataFrame(
            {"Close": [1, 2, 3], "Open": [4, 5, 6], "High": [7, 8, 9], "Low": [0, 1, 2]}
        ),
    ],
)
def test_validate_data_numeric_valid(data):
    """Test _validate_data_numeric with numeric columns."""
    _validate_data_numeric(data)


@pytest.mark.parametrize(
    ("data", "expected_error"),
    [
        (
            pd.DataFrame(
                {
                    "Close": ["100", "101"],
                    "Open": [99, 100],
                    "High": [101.0, 102.0],
                    "Low": [98.0, 99.0],
                }
            ),
            "The following columns must contain numeric values: Close.",
        ),
        (
            pd.DataFrame(
                {
                    "Close": [100, 101],
                    "Open": ["99", "100"],
                    "High": [101, 102],
                    "Low": [98, 99],
                }
            ),
            "The following columns must contain numeric values: Open.",
        ),
        (
            pd.DataFrame(
                {
                    "Close": [100, 101],
                    "Open": [99, 100],
                    "High": [101, 102],
                    "Low": ["98", "99"],
                }
            ),
            "The following columns must contain numeric values: Low.",
        ),
    ],
)
def test_validate_data_numeric_invalid(data, expected_error):
    """Test _validate_data_numeric with non-numeric columns."""
    with pytest.raises(ValueError, match=expected_error):
        _validate_data_numeric(data)
