import streamlit as st
from market_orders import place_market_order
from limit_orders import place_limit_order
from advanced.twap import place_twap_orders

st.set_page_config(page_title="Binance Futures Bot", layout="centered")
st.title("📈 Binance Futures Testnet Bot")

# --- Sidebar Form ---
st.sidebar.header("⚙️ Trade Settings")

order_type = st.sidebar.selectbox("Order Type", ["MARKET", "LIMIT", "TWAP"])
symbol = st.sidebar.text_input("Symbol", "BTCUSDT")
side = st.sidebar.radio("Side", ["BUY", "SELL"])
quantity = st.sidebar.number_input("Quantity", min_value=0.001, step=0.001, value=0.002)

# Limit order price input
price = None
if order_type == "LIMIT":
    price = st.sidebar.number_input("Limit Price", min_value=0.0, step=1.0, value=58000.0)

# TWAP inputs
interval = None
parts = None
if order_type == "TWAP":
    parts = st.sidebar.number_input("Number of Parts", min_value=1, value=4)
    interval = st.sidebar.number_input("Interval (seconds)", min_value=1, value=5)

# --- Place Order ---
if st.sidebar.button("🟢 Place Order"):
    try:
        if order_type == "MARKET":
            order = place_market_order(symbol, side, quantity)
            st.success("✅ Market Order Placed!")
            st.json(order)

        elif order_type == "LIMIT":
            order = place_limit_order(symbol, side, quantity, price)
            st.success("✅ Limit Order Placed!")
            st.json(order)

        elif order_type == "TWAP":
            orders = place_twap_orders(symbol, side, quantity, parts, interval)
            st.success(f"✅ TWAP Order Placed ({parts} parts)!")
            st.json({"TWAP Orders": orders})

    except Exception as e:
        st.error(f"❌ Failed to place order: {e}")
