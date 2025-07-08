# Binance Futures Testnet Trading Bot 🤖

A simplified trading bot built using the Binance Futures Testnet API. This bot can execute market, limit, and advanced orders including Stop-Limit, OCO, TWAP, and Grid strategies.

---

## ✅ Features

- Place market and limit orders on USDT-M Futures
- Simulated OCO orders (take-profit and stop-loss)
- Time-based TWAP execution
- Grid trading strategy with adjustable levels
- Logging of API activity (`bot.log`)
- CLI and GUI (Streamlit) interfaces

---

## 🛠️ Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install python-binance python-dotenv

```


## API SETUP:
To run the bot, you'll need Binance Testnet API credentials.

Go to the Binance Futures Testnet:
https://testnet.binancefuture.com

Log in and generate an API Key and Secret

In your project folder, create a file named .env and add:

```bash
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_api_secret

```
Never upload your .env file publicly — it's used locally to keep your keys secure.




## How to Run the Bot (CLI)

Market Order
```bash
src/market_orders.py BTCUSDT BUY 0.01
```
Limit Order
```bash
src/limit_orders.py BTCUSDT SELL 0.01 58500
```
TWAP Strategy
```bash
src/advanced/twap.py
```


## How to Run the Streamlit UI
```bash
streamlit run streamlit_app.py
```
This will open an interactive web UI where you can select:

Order type (Market, Limit, TWAP)

Symbol, quantity, and price

Place live testnet orders and view results

