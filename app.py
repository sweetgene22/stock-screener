import streamlit as st
import yfinance as yf
import pandas as pd

st.title("AI Stock Screener")
st.write("Enter up to 5 stock tickers to analyze")

tickers_input = st.text_input("Enter tickers seperated by commas (e.g. AAPL, MSFT, NVDA)")

if tickers_input:
  tickers = [t.strip().upper() for t in tickers_input.split(",")]
  
  st.write("Pulling live data...")

  data = []
  for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    data.append({
      "Ticker": ticker,
      "Company": info.get("longName", "N/A"),
      "PE Ratio": round(info.get("trailingPE", 0), 2),
      "Profit Margin": round(info.get("profitMargins", 0) * 100, 2),
      "Revenue Growth": round(info.get("revenueGrowth", 0) * 100, 2),
    })
  df = pd.DataFrame(data)
  st.dataframe(df)
