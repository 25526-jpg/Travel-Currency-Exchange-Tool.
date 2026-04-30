import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(
    page_title="🌍 Travel Currency Converter",
    page_icon="💱",
    layout="wide"
)

# -------------------------------
# CUSTOM STYLING
# -------------------------------
st.markdown("""
    <style>
    .main {
        background: linear-gradient(120deg, #84fab0, #8fd3f4);
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        color: #000;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# TITLE
# -------------------------------
st.markdown('<p class="title">💱 Travel Currency Exchange App ✈️</p>', unsafe_allow_html=True)

# -------------------------------
# API FUNCTION
# -------------------------------
@st.cache_data(ttl=3600)
def get_rates(base="USD"):
    url = f"https://api.exchangerate-api.com/v4/latest/{base}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# -------------------------------
# CURRENCY LIST
# -------------------------------
currencies = [
    "USD", "EUR", "INR", "GBP", "JPY", "AUD", "CAD",
    "CHF", "CNY", "SGD", "NZD", "AED", "ZAR"
]

# -------------------------------
# USER INPUT
# -------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    base_currency = st.selectbox("🏠 From Currency", currencies, index=2)

with col2:
    target_currency = st.selectbox("🌍 To Currency", currencies, index=0)

with col3:
    amount = st.number_input("💰 Amount", min_value=0.0, value=100.0)

# -------------------------------
# FETCH DATA
# -------------------------------
data = get_rates(base_currency)

if data:
    rates = data["rates"]

    if target_currency in rates:
        converted = amount * rates[target_currency]

        # RESULT
        st.markdown(
            f'<div class="result-box">{amount} {base_currency} = {converted:.2f} {target_currency}</div>',
            unsafe_allow_html=True
        )

    # -------------------------------
    # SWAP BUTTON
    # -------------------------------
    if st.button("🔄 Swap Currencies"):
        base_currency, target_currency = target_currency, base_currency

    # -------------------------------
    # TABLE VIEW
    # -------------------------------
    st.subheader("📊 Exchange Rates Table")
    df = pd.DataFrame(list(rates.items()), columns=["Currency", "Rate"])
    st.dataframe(df)

    # -------------------------------
    # CHART
    # -------------------------------
    st.subheader("📈 Top Currency Comparison")
    top_df = df.sort_values(by="Rate", ascending=False).head(10)

    fig = px.bar(
        top_df,
        x="Currency",
        y="Rate",
        color="Currency",
        title="Top 10 Currency Rates"
    )
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # TRAVEL TIP
    # -------------------------------
    st.info("✈️ Travel Tip: Always carry some local cash when visiting a new country!")

else:
    st.error("⚠️ Failed to fetch exchange rates. Please try again later.")
