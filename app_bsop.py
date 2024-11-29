"""Dashboard"""

import streamlit as st
from blackscholes import calculate_call_put_price
from data_retrieval import get_stock_data, calculate_volatility

st.title("Black-Scholes Options Pricing Model with Live Data")
st.write("Analyze options pricing using real-time data from Yahoo Finance.")
