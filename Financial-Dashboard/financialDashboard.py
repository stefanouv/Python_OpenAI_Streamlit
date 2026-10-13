import streamlit as st
import os
from openai import OpenAI
import yfinance as yf
from datetime import date
import plotly.graph_objects as go
import numpy as np

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="Financial Dashboard", layout="wide")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Missing OPENAI_API_KEY")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("📊 Advanced Financial Comparative Analysis Tool")

# ----------------------------
# FUNCTIONS
# ----------------------------
def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def get_company_info(ticker):
    try:
        t = yf.Ticker(ticker)
        return t.info
    except:
        return {}


def safe_value(x):
    return x if x is not None else "N/A"


def plot_candlestick(data, title):
    fig = go.Figure(data=[
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"]
        )
    ])
    fig.update_layout(title=title)
    return fig


# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.header("User Inputs")

stock1 = st.sidebar.text_input("Stock 1", "AAPL").upper()
stock2 = st.sidebar.text_input("Stock 2", "GOOGL").upper()

start_date = st.sidebar.date_input("Start Date", date(2024, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

metric = st.sidebar.selectbox(
    "Select Metric",
    ["Open", "High", "Low", "Close", "Volume"]
)

chart_type = st.sidebar.selectbox(
    "Chart Type",
    ["Line", "Bar"]
)

# ----------------------------
# DATA FETCH
# ----------------------------
data1 = get_stock_data(stock1, start_date, end_date)
data2 = get_stock_data(stock2, start_date, end_date)

# FIX columns from yfinance (VERY IMPORTANT)
data1.columns = data1.columns.map(lambda x: x[0] if isinstance(x, tuple) else x)
data2.columns = data2.columns.map(lambda x: x[0] if isinstance(x, tuple) else x)

info1 = get_company_info(stock1)
info2 = get_company_info(stock2)

# ----------------------------
# VALIDATION
# ----------------------------
if data1.empty or data2.empty:
    st.error("Invalid ticker or no data available.")
    st.stop()

# ----------------------------
# LAYOUT
# ----------------------------
col1, col2 = st.columns(2)

# ============================
# STOCK 1
# ============================
with col1:
    st.subheader(stock1)

    st.dataframe(data1.tail())

    if chart_type == "Line":
        st.line_chart(data1[metric])
    else:
        st.bar_chart(data1[metric])

    data1["MA20"] = data1["Close"].rolling(20).mean()
    st.line_chart(data1[["Close", "MA20"]])

    st.plotly_chart(plot_candlestick(data1, f"{stock1} Candlestick"))

    st.metric("Last Close", round(data1["Close"].iloc[-1], 2))
    st.metric("Max Price", round(data1["High"].max(), 2))
    st.metric("Min Price", round(data1["Low"].min(), 2))
    st.metric("Avg Close", round(data1["Close"].mean(), 2))

    st.write("### Company Info")
    st.write("Sector:", safe_value(info1.get("sector")))
    st.write("Industry:", safe_value(info1.get("industry")))
    st.write("Market Cap:", safe_value(info1.get("marketCap")))
    st.write("P/E Ratio:", safe_value(info1.get("trailingPE")))
    st.write("Dividend Yield:", safe_value(info1.get("dividendYield")))

# ============================
# STOCK 2
# ============================
with col2:
    st.subheader(stock2)

    st.dataframe(data2.tail())

    if chart_type == "Line":
        st.line_chart(data2[metric])
    else:
        st.bar_chart(data2[metric])

    data2["MA20"] = data2["Close"].rolling(20).mean()
    st.line_chart(data2[["Close", "MA20"]])

    st.plotly_chart(plot_candlestick(data2, f"{stock2} Candlestick"))

    st.metric("Last Close", round(data2["Close"].iloc[-1], 2))
    st.metric("Max Price", round(data2["High"].max(), 2))
    st.metric("Min Price", round(data2["Low"].min(), 2))
    st.metric("Avg Close", round(data2["Close"].mean(), 2))

    st.write("### Company Info")
    st.write("Sector:", safe_value(info2.get("sector")))
    st.write("Industry:", safe_value(info2.get("industry")))
    st.write("Market Cap:", safe_value(info2.get("marketCap")))
    st.write("P/E Ratio:", safe_value(info2.get("trailingPE")))
    st.write("Dividend Yield:", safe_value(info2.get("dividendYield")))

# ----------------------------
# COMPARISON CHART
# ----------------------------
st.subheader("📈 Direct Comparison")

compare = data1["Close"].rename(stock1)
compare2 = data2["Close"].rename(stock2)

merged = compare.to_frame().join(compare2, how="inner")

st.line_chart(merged)

# ----------------------------
# RETURNS + VOLATILITY
# ----------------------------

st.subheader("📊 Risk & Performance Metrics")

data1["Daily Return"] = data1["Close"].pct_change()
data2["Daily Return"] = data2["Close"].pct_change()

vol1 = data1["Daily Return"].std()
vol2 = data2["Daily Return"].std()

vol1 = 0 if np.isnan(vol1) else vol1
vol2 = 0 if np.isnan(vol2) else vol2

col3, col4 = st.columns(2)

with col3:
    st.metric("Volatility (Stock 1)", round(vol1, 5))
    st.line_chart(data1["Daily Return"])

with col4:
    st.metric("Volatility (Stock 2)", round(vol2, 5))
    st.line_chart(data2["Daily Return"])


# ----------------------------
# DOWNLOAD CSV
# ----------------------------

st.subheader("⬇️ Download Data")

col5, col6 = st.columns(2)

with col5:
    st.download_button(
        f"Download {stock1} CSV",
        data1.to_csv().encode(),
        file_name=f"{stock1}_data.csv",
        mime="text/csv"
    )

with col6:
    st.download_button(
        f"Download {stock2} CSV",
        data2.to_csv().encode(),
        file_name=f"{stock2}_data.csv",
        mime="text/csv"
    )


# ----------------------------
# AI ANALYSIS
# ----------------------------

st.subheader("🤖 AI Comparative Analysis")

if st.button("Generate AI Report"):

    st.info("📌 All analysis is based on historical market data from yfinance and does not constitute financial advice.")

    with st.spinner("Analyzing financial data..."):

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": """
                You are a senior financial analyst and portfolio manager.

                Use ONLY the provided data.

                Return a structured Markdown report:

                ## 1. Overview
                ## 2. Price Performance Comparison
                ## 3. Volatility & Risk Analysis
                ## 4. Key Financial Insights
                ## 5. Strengths vs Weaknesses
                ## 6. Final Recommendation

                At the end:
                - Give Buy / Hold / Sell for each stock
                - One short justification each

                Be precise, analytical, and avoid generic statements.
                """
                },
                {
                    "role": "user",
                    "content": f"""
Stock 1 ({stock1}):
{data1.tail(10).to_string()}

Stock 2 ({stock2}):
{data2.tail(10).to_string()}
"""
                }
            ]
        )

        st.markdown(response.choices[0].message.content)

# ----------------------------
# FINAL NOTE / SUBMISSION READY
# ----------------------------

st.success("✅ Dashboard fully loaded — ready for submission")

st.markdown("""
    ---
    ⚠️ **Disclaimer:** This tool is for educational purposes only and does not constitute financial advice.
    """)