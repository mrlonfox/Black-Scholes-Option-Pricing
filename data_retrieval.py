# Data fetching
import yfinance as yf

def get_stock_data(ticker):
    """
    Fetches the current stock price for the given ticker.
    :param ticker: Stock ticker symbol.
    :return: Current stock price (Spot Price).
    """
    stock = yf.Ticker(ticker)
    current_price = stock.history(period="1d")['Close'][0] 
    return current_price


