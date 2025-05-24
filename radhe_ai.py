# Radhe Trade Brain AI - V1
# Streamlit based AI Trading Tool (Chapters 1 to 8 logic)

import streamlit as st
import yfinance as yf
import pandas as pd
import talib
from datetime import datetime, timedelta

# Page Config
st.set_page_config(page_title="Radhe Trade Brain AI", layout="centered")
st.title("📈 Radhe Trade Brain AI - V1")
st.markdown("""
A simple AI-powered tool based on basic technical indicators like RSI, MACD, MA etc.
Enter a stock symbol (e.g., RELIANCE.NS) and get signals.
""")

# Input
symbol = st.text_input("Enter Stock Symbol (e.g., TCS.NS):", "RELIANCE.NS")
start_date = st.date_input("Start Date", datetime.today() - timedelta(days=180))
end_date = st.date_input("End Date", datetime.today())

if st.button("🔍 Analyze"):
    try:
        data = yf.download(symbol, start=start_date, end=end_date)

        if data.empty:
            st.error("No data found. Check the symbol.")
        else:
            st.success("Data Loaded Successfully!")
            st.line_chart(data['Close'], use_container_width=True)

            # Indicators
            data['RSI'] = talib.RSI(data['Close'])
            data['MACD'], data['MACD_signal'], _ = talib.MACD(data['Close'])
            data['MA50'] = talib.SMA(data['Close'], timeperiod=50)
            data['MA200'] = talib.SMA(data['Close'], timeperiod=200)

            latest = data.iloc[-1]

            st.subheader("📊 Indicator Values")
            st.write(f"**RSI:** {latest['RSI']:.2f}")
            st.write(f"**MACD:** {latest['MACD']:.2f} | Signal: {latest['MACD_signal']:.2f}")
            st.write(f"**MA50:** {latest['MA50']:.2f} | **MA200:** {latest['MA200']:.2f}")

            # Signal Logic (Chapter 8 simplified)
            st.subheader("🔔 Signal")
            signal = "Hold"

            if latest['RSI'] < 30 and latest['MACD'] > latest['MACD_signal'] and latest['Close'] > latest['MA50']:
                signal = "Strong Buy"
            elif latest['RSI'] > 70 and latest['MACD'] < latest['MACD_signal'] and latest['Close'] < latest['MA50']:
                signal = "Strong Sell"

            st.markdown(f"### 📌 Recommendation: **{signal}**")

    except Exception as e:
        st.error(f"Error: {str(e)}")
