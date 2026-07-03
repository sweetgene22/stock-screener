import streamlit as st
import yfinance as yf
import pandas as pd

st.title("AI Stock Screener")
st.write("Enter stock tickers to analyze and score them automatically")

tickers_input = st.text_input("Enter tickers separated by commas (e.g. AAPL,MSFT,GOOGL)")

if tickers_input:
    tickers = [t.strip().upper() for t in tickers_input.split(",")]
    st.write("Pulling live data...")
    data = []

    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            pe = round(info.get("trailingPE", 0), 2)
            margin = round(info.get("profitMargins", 0) * 100, 2)
            growth = round(info.get("revenueGrowth", 0) * 100, 2)
            score = 0
            if 0 < pe < 25: score += 3
            elif pe < 35: score += 1
            if margin > 20: score += 3
            elif margin > 10: score += 1
            if growth > 15: score += 3
            elif growth > 5: score += 1
            if score >= 8: rating = "Strong Buy"
            elif score >= 5: rating = "Buy"
            elif score >= 3: rating = "Hold"
            else: rating = "Avoid"
            data.append({
                "Ticker": ticker,
                "Company": info.get("longName", "N/A"),
                "Current Price": price,
                "PE Ratio": pe,
                "Profit Margin %": margin,
                "Revenue Growth %": growth,
                "Score": score,
                "Rating": rating
            })
        except:
            st.warning(f"Could not fetch data for {ticker}")

    if data:
        df = pd.DataFrame(data).sort_values("Score", ascending=False)

        def color_rating(val):
            if val == "Strong Buy":
                return "background-color: green; color: white"
            elif val == "Buy":
                return "background-color: steelblue; color: white"
            elif val == "Hold":
                return "background-color: orange; color: white"
            else:
                return "background-color: red; color: white"

        styled_df = df.style.map(color_rating, subset=["Rating"])
        st.dataframe(styled_df)

        st.subheader("Summary")
        st.write(f"Strong Buys: {len(df[df['Rating'] == 'Strong Buy'])}")
        st.write(f"Buys: {len(df[df['Rating'] == 'Buy'])}")
        st.write(f"Avoid: {len(df[df['Rating'] == 'Avoid'])}")

        st.subheader("Score Comparison")
        st.bar_chart(df.set_index("Ticker")["Score"])
   




