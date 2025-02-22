from datetime import datetime

import pandas as pd
import yfinance as yf


def download_data(symbol, interval, start_date, end_date):
    """Download historical stock data and validate it.

    This function downloads historical stock data for a given symbol, date range,
    and interval using the yfinance library. The input parameters and the downloaded
    data are validated to ensure they meet the required criteria.

    Args:
        symbol (str): Stock symbol to download data for (e.g., 'AAPL' for Apple).
        interval (str): Data interval (e.g., '1d' for daily, '1h' for hourly).
        start_date (str): Start date for the data in 'YYYY-MM-DD' format.
        end_date (str): End date for the data in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: DataFrame containing the downloaded stock data.
    """
    _validate_input(symbol, interval, start_date, end_date)
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    _validate_data(data, symbol, start_date, end_date, interval)
    data.columns = _remove_multiindex_from_cols(data.columns)
    return data


def _validate_input(symbol, interval, start_date, end_date):
    """Validate symbol, interval, and date inputs."""
    _validate_symbol(symbol)
    _validate_interval(interval)
    _validate_date_format(start_date)
    _validate_date_format(end_date)
    _validate_date_range(start_date, end_date)


def _validate_symbol(symbol):
    """Check if symbol is a non-empty string."""
    is_symbol_string = isinstance(symbol, str)
    if not is_symbol_string:
        error_msg = "Symbol must be a non-empty string."
        raise TypeError(error_msg)


def _validate_interval(interval):
    """Validate if interval is within the allowed set."""
    valid_intervals = {
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
    }
    if interval not in valid_intervals:
        error_msg = f"Invalid interval. Choose from {', '.join(valid_intervals)}."
        raise ValueError(error_msg)


def _validate_date_format(date_str):
    """Check if date string is in 'YYYY-MM-DD' format."""
    if not isinstance(date_str, str):
        error_msg = "Date must be a string in 'YYYY-MM-DD' format."
        raise TypeError(error_msg)
    try:
        datetime.fromisoformat(date_str)
    except ValueError as e:
        error_msg = "Date must be in 'YYYY-MM-DD' format."
        raise ValueError(error_msg) from e


def _validate_date_range(start_date, end_date):
    """Ensure start date is before end date."""
    if start_date > end_date:
        error_msg = "Start date must be before end date."
        raise ValueError(error_msg)


def _validate_data(data, symbol, start_date, end_date, interval):
    """Validate the downloaded data.

    Args:
        data (pd.DataFrame): DataFrame containing stock data.
        symbol (str): Stock symbol for the data.
        start_date (str): Start date for the data.
        end_date (str): End date for the data.
        interval (str): Interval for the data.

    Raises:
        TypeError: If data is not a pandas DataFrame or index is not a DatetimeIndex.
        ValueError: If required columns are missing or contain non-numeric values.
        ValueError: If the DataFrame is empty.
    """
    _validate_data_type_dataframe(data)
    _validate_data_empty(data, symbol, start_date, end_date, interval)
    _validate_data_index_datetime(data.index)
    _validate_data_multiindex(data.columns)
    _validate_data_numeric(data)


def _validate_data_type_dataframe(data):
    """Check if the input is a pandas DataFrame."""
    if not isinstance(data, pd.DataFrame):
        error_msg = f"data must be a pandas DataFrame, got {type(data).__name__}."
        raise TypeError(error_msg)


def _validate_data_empty(data, symbol, start_date, end_date, interval):
    """Check if the DataFrame is empty."""
    if data.empty:
        error_msg = (
            f"No data found for {symbol} between {start_date} and {end_date} "
            f"with interval '{interval}'."
        )
        raise ValueError(error_msg)


def _validate_data_index_datetime(index):
    """Check if the index is of type DatetimeIndex."""
    if not isinstance(index, pd.DatetimeIndex):
        error_msg = (
            f"data index must be a pandas DatetimeIndex, got {type(index).__name__}."
        )
        raise TypeError(error_msg)


def _validate_data_multiindex(columns):
    """Check if the columns have the required MultiIndex.

    Args:
        columns (pd.MultiIndex): MultiIndex of DataFrame columns.

    Raises:
        ValueError: If the MultiIndex is not present, does not have exactly two levels,
                    or if required columns are missing from level 0.
    """
    required_cols = {"Close", "Open", "High", "Low"}

    if not isinstance(columns, pd.MultiIndex):
        error_msg = "DataFrame must have a MultiIndex for columns."
        raise TypeError(error_msg)

    yfinance_index_levels = 2
    if columns.nlevels != yfinance_index_levels:
        error_msg = (
            f"MultiIndex must have exactly 2 levels, got {columns.nlevels} levels."
        )
        raise ValueError(error_msg)

    level_0_values = set(columns.get_level_values(0))
    missing_cols = required_cols - level_0_values
    if missing_cols:
        error_msg = (
            "Level 0 of MultiIndex must contain the following columns: "
            f"{', '.join(missing_cols)}."
        )
        raise ValueError(error_msg)


def _validate_data_numeric(data):
    """Check if the required columns contain numeric values."""
    required_cols = ["Close", "Open", "High", "Low"]
    non_numeric_cols = [
        col
        for col in required_cols
        if not pd.api.types.is_numeric_dtype(data[col].squeeze())
    ]

    if non_numeric_cols:
        error_msg = (
            "The following columns must contain numeric values: "
            f"{', '.join(non_numeric_cols)}."
        )
        raise ValueError(error_msg)


def _remove_multiindex_from_cols(cols):
    """Remove MultiIndex from columns but retain level 0 as column names."""
    cols = cols.get_level_values(0)
    return cols
