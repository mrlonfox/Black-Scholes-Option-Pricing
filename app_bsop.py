"""Dashboard"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from requests.exceptions import HTTPError  # Third-party imports
from blackscholes import calculate_call_put_price  # Local imports
from data_retrieval import get_stock_data, calculate_volatility

st.title("Black-Scholes Options Pricing Model with Live Data")
st.write("Analyze options pricing using real-time data from Yahoo Finance.")

st.sidebar.header("Inputs")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL")

SPOT_PRICE = None
VOLATILITY = None

if ticker:
    try:
        SPOT_PRICE = get_stock_data(ticker)
        st.sidebar.write(f"**Current Spot Price ({ticker.upper()}):** ${SPOT_PRICE:.2f}")
    except HTTPError:
        st.sidebar.error("Unable to fetch data. Please check your internet connection.")
    except KeyError:
        st.sidebar.error("Invalid ticker. Please enter a valid stock symbol.")
    except ValueError:
        st.sidebar.error("Data retrieval failed due to invalid inputs.")
    except Exception as e:
        st.sidebar.error("An unexpected error occurred.")
        print(f"Unexpected error: {e}")

strike_price = st.sidebar.number_input("Strike Price", value=SPOT_PRICE if SPOT_PRICE else 100.0)
time_to_maturity = st.sidebar.number_input("Time to Maturity (in years)", value=1.0, step=0.1)

if SPOT_PRICE:
    try:
        VOLATILITY = calculate_volatility(ticker)
        st.sidebar.write(f"**Estimated Volatility (σ):** {VOLATILITY:.2%}")
    except HTTPError:
        st.sidebar.warning("Unable to calculate volatility. Please check your internet connection.")
        VOLATILITY = st.sidebar.slider("Volatility (σ)", 0.0, 1.0, 0.2)
    except Exception as e:
        st.sidebar.warning("An unexpected error occurred. Adjust volatility manually.")
        VOLATILITY = st.sidebar.slider("Volatility (σ)", 0.0, 1.0, 0.2)
else:
    VOLATILITY = st.sidebar.slider("Volatility (σ)", 0.0, 1.0, 0.2)

risk_free_rate = st.sidebar.slider("Risk-Free Interest Rate (%)", 0.0, 10.0, 5.0, step=0.1) / 100

if SPOT_PRICE and VOLATILITY:
    call_price, put_price = calculate_call_put_price(
        SPOT_PRICE, strike_price, time_to_maturity, VOLATILITY, risk_free_rate
    )
    st.metric("Call Option Price", f"${call_price:.2f}")
    st.metric("Put Option Price", f"${put_price:.2f}")
else:
    st.warning("Please provide a valid ticker to calculate option prices.")

def generate_heatmap(spot_prices, volatilities, strike, maturity, rate):
    """
    Generates a heatmap of call option prices for varying spot prices and volatilities.
    """
    heatmap_data = []
    for spot_price in spot_prices:
        row = []
        for volatility in volatilities:
            call_option_price, _ = calculate_call_put_price(
                spot_price, strike, maturity, volatility, rate
            )
            row.append(call_option_price)
        heatmap_data.append(row)

    fig, ax = plt.subplots(figsize=(8, 6))
    c = ax.imshow(
        heatmap_data,
        extent=(volatilities[0], volatilities[-1], spot_prices[0], spot_prices[-1]),
        origin="lower",
        aspect="auto",
        cmap="viridis",
    )
    fig.colorbar(c, label="Call Option Price")
    ax.set_xlabel("Volatility (σ)")
    ax.set_ylabel("Spot Price (S)")
    ax.set_title("Call Option Price Heatmap")
    return fig

if SPOT_PRICE:
    st.write("### Call Option Price Heatmap")
    spot_range = np.linspace(0.8 * SPOT_PRICE, 1.2 * SPOT_PRICE, 50)
    volatility_range = np.linspace(0.1, 0.5, 50)

    heatmap_fig = generate_heatmap(
        spot_range, volatility_range, strike_price, time_to_maturity, risk_free_rate
    )
    st.pyplot(heatmap_fig)
else:
    st.warning("Spot price is required to generate the heatmap. Please provide a valid ticker.")
