"""Price calculation"""

from scipy.stats import norm
import numpy as np

def calculate_call_put_price(s, k, t, sigma, r):
    """
    Calculates the prices of a European call and put option using the Black-Scholes model.
    :param s: Spot Price (current stock price).
    :param k: Strike Price.
    :param t: Time to maturity (in years).
    :param sigma: Volatility (standard deviation of returns).
    :param r: Risk-free interest rate (annualized).
    :return: Call option price and put option price.
    """
    d1 = (np.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
    d2 = d1 - sigma * np.sqrt(t)

    call_price = s * norm.cdf(d1) - k * np.exp(-r * t) * norm.cdf(d2)
    put_price = k * np.exp(-r * t) * norm.cdf(-d2) - s * norm.cdf(-d1)

    return call_price, put_price
