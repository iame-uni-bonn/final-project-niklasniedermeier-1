from datetime import datetime

import yfinance as yf


def download_data(symbol, interval, start_date, end_date):
    _validate_input(symbol, interval, start_date, end_date)
    data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
    _validate_output(data, symbol, start_date, end_date, interval)
    return data


def _validate_input(symbol, interval, start_date, end_date):
    _validate_symbol(symbol)
    _validate_interval(interval)
    _validate_date_format(start_date)
    _validate_date_format(end_date)
    _validate_date_range(start_date, end_date)


def _validate_symbol(symbol):
    is_symbol_string = isinstance(symbol, str)
    if not is_symbol_string:
        error_msg = "Symbol must be a non-empty string."
        raise TypeError(error_msg)


def _validate_interval(interval):
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
    if not isinstance(date_str, str):
        error_msg = "Date must be a string in 'YYYY-MM-DD' format."
        raise TypeError(error_msg)
    try:
        datetime.fromisoformat(date_str)
    except ValueError as e:
        error_msg = "Date must be in 'YYYY-MM-DD' format."
        raise ValueError(error_msg) from e


def _validate_date_range(start_date, end_date):
    if start_date > end_date:
        error_msg = "Start date must be before end date."
        raise ValueError(error_msg)


def _validate_output(data, symbol, start_date, end_date, interval):
    if data.empty:
        error_msg = (
            f"No data found for {symbol} between {start_date} and {end_date} "
            f"with interval '{interval}'."
        )
        raise ValueError(error_msg)
