import streamlit as st
import plotly.graph_objects as go
from utils.stock_data import fetch_stock_data, calculate_indicators
from streamlit_autorefresh import st_autorefresh


st.set_page_config(page_title="Stock Market Dashboard", layout="wide")

st.title("📈 Real-Time Stock Market Dashboard")

# Sidebar
st.sidebar.header("Settings")

symbol = st.sidebar.selectbox(
    "Select Stock",
    ["AAPL", "TSLA", "MSFT", "INFY.NS"]
)

refresh_rate = st.sidebar.selectbox(
    "Refresh Interval",
    ["30 sec", "60 sec", "120 sec"]
)

interval_map = {
    "30 sec": 30,
    "60 sec": 60,
    "120 sec": 120
}

st_autorefresh(
    interval=interval_map[refresh_rate] * 1000,
    key="auto_refresh"
)

show_sma = st.sidebar.checkbox("Show SMA")
show_ema = st.sidebar.checkbox("Show EMA")


# Fetch and process data
with st.spinner("Fetching live stock data..."):
    data = fetch_stock_data(symbol, period="5d", interval="5m")

if data is None:
    st.error("Could not fetch stock data.")
    st.stop()

data = calculate_indicators(data)

latest_price = data["Close"].iloc[-1]
st.metric(label=f"{symbol} Price", value=f"${latest_price:.2f}")

# ----- PRICE CHART -----
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=data["Datetime"],
    y=data["Close"],
    mode="lines",
    name="Close Price"
))

if show_sma:
    fig.add_trace(go.Scatter(
        x=data["Datetime"],
        y=data["SMA_20"],
        mode="lines",
        name="SMA 20"
    ))

if show_ema:
    fig.add_trace(go.Scatter(
        x=data["Datetime"],
        y=data["EMA_20"],
        mode="lines",
        name="EMA 20"
    ))

fig.update_layout(
    title="Stock Price Chart",
    xaxis_title="Time",
    yaxis_title="Price"
)

st.plotly_chart(fig, width="stretch")

# ----- VOLUME CHART -----
st.subheader("Volume")

vol_fig = go.Figure()
vol_fig.add_trace(go.Bar(
    x=data["Datetime"],
    y=data["Volume"],
    name="Volume"
))

vol_fig.update_layout(
    xaxis_title="Time",
    yaxis_title="Volume"
)

st.plotly_chart(vol_fig, width="stretch")

# ----- RSI -----
st.subheader("RSI Indicator")

rsi_fig = go.Figure()
rsi_fig.add_trace(go.Scatter(
    x=data["Datetime"],
    y=data["RSI"],
    mode="lines",
    name="RSI"
))

rsi_fig.update_layout(
    yaxis=dict(range=[0, 100]),
    xaxis_title="Time",
    yaxis_title="RSI"
)

st.plotly_chart(rsi_fig, width="stretch")

# Auto refresh every 60 seconds
st_autorefresh(interval=60 * 1000, key="stock_refresh")
