import math

import pandas as pd


def execute_buy(cash, price, shares, trade_vol, tac):
    buy_shares = math.floor(trade_vol / (price * (1 + tac)))
    if buy_shares < 1:
        return cash, shares
    cost = buy_shares * price * (1 + tac)
    if cost > cash:
        return cash, shares
    cash -= cost
    shares += buy_shares
    return cash, shares


def execute_sell(cash, price, shares, trade_vol, tac):
    sell_shares = math.floor(trade_vol / (price * (1 - tac)))

    if sell_shares > shares:
        if shares < 1:
            return cash, shares
        sell_shares = shares

    profit = sell_shares * price * (1 - tac)
    cash += profit
    shares -= sell_shares
    return cash, shares


def update_portfolio(cash, shares, price):
    holdings = shares * price
    assets = cash + holdings
    return assets, holdings


def backtest_signals(data, signals, initial_cash, tac, trade_pct, price_col="Close"):
    prices = data[price_col].squeeze()
    cash, holdings, shares = initial_cash, 0.0, 0
    assets = cash + holdings
    portfolio = []

    buy_signal = 2
    sell_signal = 1

    for price, signal in zip(prices, signals, strict=False):
        trade_vol = trade_pct * assets

        if signal == buy_signal:
            cash, shares = execute_buy(cash, price, shares, trade_vol, tac)

        elif signal == sell_signal:
            cash, shares = execute_sell(cash, price, shares, trade_vol, tac)

        assets, holdings = update_portfolio(cash, shares, price)
        portfolio.append((cash, holdings, shares, assets, signal, price))

    portfolio = pd.DataFrame(
        portfolio, columns=["cash", "holdings", "shares", "total", "signal", "price"]
    )
    return portfolio
