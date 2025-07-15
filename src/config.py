import os
import streamlit as st

load_dotenv()

API_KEY = st.secrets["binance"]["BINANCE_API_KEY"]
API_SECRET = st.secrets["binance"]["BINANCE_API_SECRET"]

if not API_KEY or not API_SECRET:
    raise ValueError("❌ API credentials not found in .env file.")
