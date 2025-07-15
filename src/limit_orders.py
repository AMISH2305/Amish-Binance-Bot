from binance.enums import *
from src.client_setup import get_binance_client
import logging

# Set up logging to bot.log
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize Binance Futures testnet client
client = get_binance_client()

def place_limit_order(symbol, side, quantity, price):
    """
    Places a LIMIT order on Binance Futures Testnet.

    Args:
        symbol (str): Trading pair, e.g. "BTCUSDT"
        side (str): "BUY" or "SELL"
        quantity (float): Quantity to buy/sell
        price (float or str): Limit price

    Returns:
        dict: Order confirmation response
    """
    try:
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=SIDE_BUY if side.upper() == 'BUY' else SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            quantity=quantity,
            price=str(price),  # Binance API expects price as string
            timeInForce=TIME_IN_FORCE_GTC  # Good Till Canceled
        )
        logging.info(f"✅ Limit Order Placed: {order}")
        return order

    except Exception as e:
        logging.error(f"❌ Limit Order Failed: {e}")
        raise

