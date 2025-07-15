import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.twap import place_twap_orders

# Page config
st.set_page_config(
    page_title="Binance Futures Bot", 
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4037 0%, #99f2c8 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🚀 Binance Futures Testnet Trading Bot</h1>
    <p>Advanced Trading Interface for Crypto Futures</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'pnl_data' not in st.session_state:
    st.session_state.pnl_data = []

# Sidebar Configuration
st.sidebar.markdown("## ⚙️ Trading Configuration")

# Trading Settings
with st.sidebar.expander("📊 Order Settings", expanded=True):
    order_type = st.selectbox("Order Type", ["MARKET", "LIMIT", "TWAP"], help="Select your preferred order type")
    symbol = st.text_input("Symbol", "BTCUSDT", help="Trading pair symbol")
    side = st.radio("Side", ["BUY", "SELL"], horizontal=True)
    quantity = st.number_input("Quantity", min_value=0.001, step=0.001, value=0.002, help="Order quantity")

# Conditional inputs
price = None
if order_type == "LIMIT":
    price = st.sidebar.number_input("Limit Price", min_value=0.0, step=1.0, value=58000.0, help="Price for limit order")

interval = None
parts = None
if order_type == "TWAP":
    parts = st.sidebar.number_input("Number of Parts", min_value=1, value=4, help="Split order into parts")
    interval = st.sidebar.number_input("Interval (seconds)", min_value=1, value=5, help="Time between each part")

# Risk Management
with st.sidebar.expander("⚠️ Risk Management", expanded=False):
    use_stop_loss = st.checkbox("Enable Stop Loss")
    stop_loss_price = st.number_input("Stop Loss Price", min_value=0.0, step=1.0, value=55000.0, disabled=not use_stop_loss)
    use_take_profit = st.checkbox("Enable Take Profit")
    take_profit_price = st.number_input("Take Profit Price", min_value=0.0, step=1.0, value=62000.0, disabled=not use_take_profit)

# Main Content Layout
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.markdown("### 📈 Trading Dashboard")
    
    # Market Overview Cards
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("💰 Account Balance", "$10,000", "+$250")
    
    with metric_col2:
        st.metric("📊 Open Positions", "3", "+1")
    
    with metric_col3:
        st.metric("📈 Total P&L", "+$1,250", "+5.2%")
    
    with metric_col4:
        st.metric("🔄 24h Volume", "$5,420", "+12.3%")
    
    # Price Chart (Mock data for demonstration)
    st.markdown("#### 📊 Price Chart")
    
    # Generate mock price data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='D')
    prices = [58000 + i*100 + (i**2)*10 for i in range(len(dates))]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=prices, mode='lines', name='Price', line=dict(color='#1f77b4')))
    fig.update_layout(
        title=f"{symbol} Price Movement",
        xaxis_title="Date",
        yaxis_title="Price (USDT)",
        height=400,
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 🎯 Quick Actions")
    
    # Order Placement
    if st.button("🟢 Place Order", type="primary", use_container_width=True):
        try:
            order_result = None
            if order_type == "MARKET":
                order_result = place_market_order(symbol, side, quantity)
                st.success("✅ Market Order Placed!")
            elif order_type == "LIMIT":
                order_result = place_limit_order(symbol, side, quantity, price)
                st.success("✅ Limit Order Placed!")
            elif order_type == "TWAP":
                order_result = place_twap_orders(symbol, side, quantity, parts, interval)
                st.success(f"✅ TWAP Order Placed ({parts} parts)!")
            
            # Add to trade history
            if order_result:
                st.session_state.trade_history.append({
                    'Time': datetime.now().strftime('%H:%M:%S'),
                    'Symbol': symbol,
                    'Side': side,
                    'Type': order_type,
                    'Quantity': quantity,
                    'Price': price if price else 'Market',
                    'Status': 'Filled'
                })
                
                with st.expander("📋 Order Details"):
                    st.json(order_result)
                    
        except Exception as e:
            st.error(f"❌ Failed to place order: {e}")
    
    # Quick Action Buttons
    st.markdown("#### ⚡ Quick Actions")
    
    col_buy, col_sell = st.columns(2)
    with col_buy:
        if st.button("🚀 Quick Buy", use_container_width=True):
            st.info("Quick buy feature coming soon!")
    
    with col_sell:
        if st.button("📉 Quick Sell", use_container_width=True):
            st.info("Quick sell feature coming soon!")
    
    # Position Management
    st.markdown("#### 🎛️ Position Management")
    if st.button("📊 View Positions", use_container_width=True):
        st.info("Position viewer coming soon!")
    
    if st.button("🔄 Close All Positions", use_container_width=True):
        st.warning("This will close all open positions!")

with col3:
    st.markdown("### 📊 Market Info")
    
    # Market Statistics
    st.markdown("#### 📈 Market Stats")
    market_data = {
        "24h High": "$59,450",
        "24h Low": "$57,200",
        "24h Volume": "45,231 BTC",
        "Market Cap": "$1.2T",
        "Funding Rate": "0.0125%"
    }
    
    for key, value in market_data.items():
        st.markdown(f"**{key}:** {value}")
    
    # Order Book (Mock data)
    st.markdown("#### 📚 Order Book")
    
    # Mock order book data
    bids = [58000 - i*10 for i in range(5)]
    asks = [58050 + i*10 for i in range(5)]
    quantities = [0.5, 0.3, 0.8, 0.2, 0.6]
    
    order_book_data = {
        'Bid Price': bids,
        'Bid Qty': quantities,
        'Ask Price': asks,
        'Ask Qty': quantities
    }
    
    df_orderbook = pd.DataFrame(order_book_data)
    st.dataframe(df_orderbook, use_container_width=True, height=200)

# Bottom Section
st.markdown("---")

# Trade History and Analytics
history_col, analytics_col = st.columns([3, 2])

with history_col:
    st.markdown("### 📝 Trade History")
    
    if st.session_state.trade_history:
        df_history = pd.DataFrame(st.session_state.trade_history)
        st.dataframe(df_history, use_container_width=True)
        
        # Download trade history
        csv = df_history.to_csv(index=False)
        st.download_button(
            label="📥 Download Trade History",
            data=csv,
            file_name=f"trade_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No trades executed yet. Start trading to see your history here!")

with analytics_col:
    st.markdown("### 📊 Performance Analytics")
    
    # Mock performance data
    performance_data = {
        'Metric': ['Win Rate', 'Total Trades', 'Avg. Trade Size', 'Best Trade', 'Worst Trade'],
        'Value': ['68.5%', '42', '0.025 BTC', '+$450', '-$120']
    }
    
    df_performance = pd.DataFrame(performance_data)
    st.table(df_performance)
    
    # P&L Chart
    st.markdown("#### 💹 P&L Chart")
    pnl_values = [100, 150, 120, 200, 180, 250, 300]
    
    # Create simple date labels
    pnl_dates = [datetime.now() - timedelta(days=i) for i in range(len(pnl_values)-1, -1, -1)]
    
    # Use Plotly Graph Objects instead of Express
    fig_pnl = go.Figure()
    fig_pnl.add_trace(go.Scatter(
        x=pnl_dates, 
        y=pnl_values, 
        mode='lines+markers',
        name='P&L',
        line=dict(color='#00cc44', width=3),
        marker=dict(size=6)
    ))
    
    fig_pnl.update_layout(
        title="7-Day P&L Performance",
        xaxis_title="Date",
        yaxis_title="P&L (USD)",
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig_pnl, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>⚠️ <strong>Testnet Environment</strong> - No real money involved</p>
    <p>🔒 Trading responsibly with proper risk management</p>
    <p>📞 Need help? Contact support or check documentation</p>
</div>
""", unsafe_allow_html=True)

# Auto-refresh option
if st.sidebar.checkbox("🔄 Auto Refresh (5s)"):
    time.sleep(5)
    st.rerun()

# Debug info (can be removed in production)
with st.sidebar.expander("🔧 Debug Info", expanded=False):
    st.write("Session State:", st.session_state)
    st.write("Current Time:", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
