import pytest

from backtest_bay.data.download_data import _validate_symbol


# Tests for _validate_symbol
def test_validate_symbol_valid_cases():
    assert _validate_symbol("AAPL") is None
    assert _validate_symbol("MSFT") is None


def test_validate_symbol_invalid_symbol():
    with pytest.raises(ValueError, match="Invalid symbol: 'INVALID'"):
        _validate_symbol("INVALID")


def test_validate_symbol_empty_string():
    with pytest.raises(ValueError, match="Invalid symbol: ''"):
        _validate_symbol("")


def test_validate_symbol_non_string():
    with pytest.raises(ValueError, match="Symbol must be a non-empty string."):
        _validate_symbol(123)
