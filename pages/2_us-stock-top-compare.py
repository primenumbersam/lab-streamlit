# -*- coding: utf-8 -*-
# Copyright 2024-2025 Streamlit Inc.
# Licensed under the Apache License, Version 2.0 (see original repo)

import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

# Page Title
st.title(":material/query_stats: Stock Peer Analysis")
st.markdown("Easily compare stocks against others in their peer group.")

""  # Add some space.

cols = st.columns([1, 3])

STOCKS = [
    "AAPL", "ABBV", "ACN", "ADBE", "ADP", "AMD", "AMGN", "AMT", "AMZN", "APD",
    "AVGO", "AXP", "BA", "BK", "BKNG", "BMY", "BRK.B", "BSX", "C", "CAT",
    "CI", "CL", "CMCSA", "COST", "CRM", "CSCO", "CVX", "DE", "DHR", "DIS",
    "DUK", "ELV", "EOG", "EQR", "FDX", "GD", "GE", "GILD", "GOOG", "GOOGL",
    "HD", "HON", "HUM", "IBM", "ICE", "INTC", "ISRG", "JNJ", "JPM", "KO",
    "LIN", "LLY", "LMT", "LOW", "MA", "MCD", "MDLZ", "META", "MMC", "MO",
    "MRK", "MSFT", "NEE", "NFLX", "NKE", "NOW", "NVDA", "ORCL", "PEP", "PFE",
    "PG", "PLD", "PM", "PSA", "REGN", "RTX", "SBUX", "SCHW", "SLB", "SO",
    "SPGI", "T", "TJX", "TMO", "TSLA", "TXN", "UNH", "UNP", "UPS", "V",
    "VZ", "WFC", "WM", "WMT", "XOM"
]

DEFAULT_STOCKS = ["GOOGL","AMZN", "MSFT", "NVDA", "AAPL", "META", "TSLA"]


def stocks_to_str(stocks):
    return ",".join(stocks)


if "tickers_input" not in st.session_state:
    st.session_state.tickers_input = st.query_params.get(
        "stocks", stocks_to_str(DEFAULT_STOCKS)
    ).split(",")


# Callback to update query param when input changes
def update_query_param():
    if st.session_state.tickers_input:
        st.query_params["stocks"] = stocks_to_str(st.session_state.tickers_input)
    else:
        st.query_params.pop("stocks", None)


top_left_cell = cols[0].container(
    border=True, height="stretch", vertical_alignment="center"
)

with top_left_cell:
    # Selectbox for stock tickers
    tickers = st.multiselect(
        "Stock tickers",
        options=sorted(set(STOCKS) | set(st.session_state.tickers_input)),
        default=st.session_state.tickers_input,
        placeholder="Choose stocks to compare. Example: NVDA",
    )

# Time horizon selector
horizon_map = {
    "1 Months": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "5 Years": "5y",
    "10 Years": "10y",
    "20 Years": "20y",
}

with top_left_cell:
    # Buttons for picking time horizon
    horizon = st.pills(
        "Time horizon",
        options=list(horizon_map.keys()),
        default="6 Months",
    )

tickers = [t.upper() for t in tickers]

# Update query param when text input changes
if tickers:
    st.query_params["stocks"] = stocks_to_str(tickers)
else:
    # Clear the param if input is empty
    st.query_params.pop("stocks", None)

if not tickers:
    top_left_cell.info("Pick some stocks to compare", icon=":material/info:")
    st.stop()


right_cell = cols[1].container(
    border=True, height="stretch", vertical_alignment="center"
)


@st.cache_resource(show_spinner=False, ttl="6h")
def load_data(tickers, period):
    tickers_obj = yf.Tickers(tickers)
    data = tickers_obj.history(period=period)
    if data is None or data.empty:
        raise RuntimeError("YFinance returned no data.")
    return data["Close"]


# Load the data
try:
    with st.spinner("Loading stock data..."):
        data = load_data(tickers, horizon_map[horizon])
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

if data.empty:
    st.info("No data found for the selected tickers/period.")
    st.stop()

# Normalize prices (start at 1)
normalized = data.div(data.iloc[0])

latest_norm_values = {normalized[ticker].iat[-1]: ticker for ticker in tickers if not pd.isna(normalized[ticker].iat[-1])}
if not latest_norm_values:
    st.error("No valid normalized data available.")
    st.stop()

max_norm_value = max(latest_norm_values.items())
min_norm_value = min(latest_norm_values.items())

bottom_left_cell = cols[0].container(
    border=True, height="stretch", vertical_alignment="center"
)

with bottom_left_cell:
    col1, col2 = st.columns(2)
    col1.metric(
        "Best stock",
        max_norm_value[1],
        delta=f"{round((max_norm_value[0] - 1) * 100)}%",
    )
    col2.metric(
        "Worst stock",
        min_norm_value[1],
        delta=f"{round((min_norm_value[0] - 1) * 100)}%",
    )


# Plot normalized prices
with right_cell:
    st.altair_chart(
        alt.Chart(
            normalized.reset_index().melt(
                id_vars=["Date"], var_name="Stock", value_name="Normalized price"
            )
        )
        .mark_line()
        .encode(
            alt.X("Date:T"),
            alt.Y("Normalized price:Q").scale(zero=False),
            alt.Color("Stock:N"),
        )
        .properties(height=400),
        use_container_width=True
    )

st.divider()

# Plot individual stock vs peer average
st.header("Individual stocks vs peer average")
st.markdown("For the analysis below, the 'peer average' when analyzing stock X always excludes X itself.")

if len(tickers) <= 1:
    st.warning("Pick 2 or more tickers to compare them")
    st.stop()

NUM_COLS = 2
cols_grid = st.columns(NUM_COLS)

for i, ticker in enumerate(tickers):
    # Calculate peer average (excluding current stock)
    try:
        peers = normalized.drop(columns=[ticker])
        peer_avg = peers.mean(axis=1)

        # Create DataFrame with peer average.
        plot_data = pd.DataFrame(
            {
                "Date": normalized.index,
                ticker: normalized[ticker],
                "Peer average": peer_avg,
            }
        ).melt(id_vars=["Date"], var_name="Series", value_name="Price")

        chart = (
            alt.Chart(plot_data)
            .mark_line()
            .encode(
                alt.X("Date:T"),
                alt.Y("Price:Q").scale(zero=False),
                alt.Color(
                    "Series:N",
                    scale=alt.Scale(domain=[ticker, "Peer average"], range=["red", "gray"]),
                    legend=alt.Legend(orient="bottom"),
                ),
                alt.Tooltip(["Date", "Series", "Price"]),
            )
            .properties(title=f"{ticker} vs peer average", height=300)
        )

        with cols_grid[i % NUM_COLS]:
            with st.container(border=True):
                st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        continue

st.divider()
st.header("Raw data")
st.dataframe(data, use_container_width=True)
