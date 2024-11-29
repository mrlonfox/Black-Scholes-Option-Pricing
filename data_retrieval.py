"""Data fetching"""

import yfinance as yf
import numpy as np

def get_stock_data(ticker):
    """
    Fetches the current stock price for the given ticker.
    :param ticker: Stock ticker symbol.
    :return: Current stock price (Spot Price).
    """
    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d")['Close'][0]
    return current_price

def calculate_volatility(ticker, lookback_period=252):
    """
    Calculates the historical volatility of a stock based on its past prices.
    :param ticker: Stock ticker symbol.
    :param lookback_period: Number of days to calculate historical 
    volatility (default: 252 trading days).
    :return: Annualized historical volatility (σ).
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=f"{lookback_period}d")['Close']
    log_returns = np.log(data / data.shift(1)).dropna()
    volatility = np.std(log_returns) * np.sqrt(252)
    return volatility
