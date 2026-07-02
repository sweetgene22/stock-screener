import streamlit as st

st.title("Stock Screener")
st.write("Welcome to my AI-powered stock screener")

ticker = st.text_input("Enter a stock ticker (e.g. AAPL)")

if ticker:
  st.write(f"You entered: {ticker}")
