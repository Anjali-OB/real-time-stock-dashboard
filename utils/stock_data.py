import yfinance as yf
import pandas as pd
import streamlit as st


@st.cache_data(ttl=60)
def fetch_stock_data(symbol, period="1d", interval="1m"):
    stock = yf.Ticker(symbol)
    data = stock.history(period=period, interval=interval)

    if data.empty:
        return None

    data.reset_index(inplace=True)
    return data


def calculate_indicators(df):
    # Simple Moving Average (SMA)
    df["SMA_20"] = df["Close"].rolling(window=20).mean()

    # Exponential Moving Average (EMA)
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()

    # RSI Calculation
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    return df
