from binance.enums import *
from src.client_setup import get_binance_client
import logging

# Set up logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize Binance testnet client
client = get_binance_client()

def place_market_order(symbol, side, quantity):
    """
    Places a market order on the Binance Futures Testnet.

    :param symbol: Trading pair (e.g., BTCUSDT)
    :param side: 'BUY' or 'SELL'
    :param quantity: Order quantity (e.g., 0.01)
    :return: Order response dict
    """
    try:
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=SIDE_BUY if side.upper() == 'BUY' else SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=quantity
        )
        logging.info(f"✅ Market Order Placed: {order}")
        return order

    except Exception as e:
        logging.error(f"❌ Market Order Failed: {e}")
        raise
