import math

import pandas as pd


def backtest_signals(data, signals, initial_cash, tac, trade_pct, price_col="Close"):
    prices = data[price_col].squeeze()
    cash, holdings, shares = initial_cash, 0.0, 0
    assets = cash + holdings
    portfolio = []

    for price, signal in zip(prices, signals, strict=False):
        trade_vol = trade_pct * assets
        cash, shares = _execute_trade(signal, cash, price, shares, trade_vol, tac)
        assets, holdings = _update_portfolio(cash, shares, price)
        portfolio.append((price, signal, shares, holdings, cash, assets))

    portfolio = pd.DataFrame(
        portfolio,
        columns=["price", "signal", "shares", "holdings", "cash", "assets"],
        index=data.index,
    )
    return portfolio


def _execute_trade(signal, cash, price, shares, trade_vol, tac):
    buy_signal = 2
    sell_signal = 1

    if signal == buy_signal:
        cash, shares = _execute_buy(cash, price, shares, trade_vol, tac)

    elif signal == sell_signal:
        cash, shares = _execute_sell(cash, price, shares, trade_vol, tac)

    return cash, shares


def _execute_buy(cash, price, shares, trade_vol, tac):
    buy_shares = math.floor(trade_vol / (price * (1 + tac)))
    cost = buy_shares * price * (1 + tac)

    if not _is_buy_trade_affordable(buy_shares, cost, cash):
        return cash, shares

    cash -= cost
    shares += buy_shares
    return cash, shares


def _is_buy_trade_affordable(buy_shares, cost, cash):
    is_trade_vol_enough = buy_shares >= 1
    is_cash_enough = cash >= cost
    return is_trade_vol_enough and is_cash_enough


def _execute_sell(cash, price, shares, trade_vol, tac):
    sell_shares = math.floor(trade_vol / (price * (1 - tac)))

    if not _is_sell_trade_affordable(shares):
        return cash, shares

    sell_shares = min(sell_shares, shares)

    profit = sell_shares * price * (1 - tac)
    cash += profit
    shares -= sell_shares
    return cash, shares


def _is_sell_trade_affordable(shares):
    return shares >= 1


def _update_portfolio(cash, shares, price):
    holdings = shares * price
    assets = cash + holdings
    return assets, holdings
