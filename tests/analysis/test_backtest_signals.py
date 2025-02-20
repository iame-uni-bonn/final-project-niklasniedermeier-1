import pandas as pd
import pandas.testing as pdt

from backtest_bay.analysis.backtest_signals import (
    _execute_buy,
    _execute_sell,
    _is_buy_trade_affordable,
    _is_sell_trade_affordable,
    _update_portfolio,
    backtest_signals,
)


# tests for _is_buy_affordable
def test_is_buy_trade_affordable_enough_cash():
    """Test buying when there is enough cash."""
    affordable = _is_buy_trade_affordable(buy_shares=2, cost=10, cash=10)
    assert affordable


def test_is_buy_trade_affordable_not_enough_cash():
    """Test buying when there is not enough cash."""
    affordable = _is_buy_trade_affordable(buy_shares=2, cost=10, cash=9)
    assert not affordable


def test_is_buy_trade_affordable_not_enough_shares():
    """Test buying when buy shares are less than 1."""
    affordable = _is_buy_trade_affordable(buy_shares=0.1, cost=10, cash=9)
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
