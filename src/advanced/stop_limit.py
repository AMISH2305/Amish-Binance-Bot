from binance.enums import SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
from client_setup import get_binance_client
import logging

# Setup logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

client = get_binance_client()

def place_stop_limit_order(symbol, side, quantity, stop_price, limit_price):
    """
    Places a STOP_LIMIT order on Binance Futures Testnet.

    Args:
        symbol (str): e.g., "BTCUSDT"
        side (str): "BUY" or "SELL"
        quantity (float): Quantity to trade
        stop_price (float or str): Trigger price
        limit_price (float or str): Final limit order price once triggered

    Returns:
        dict: API response
    """
    try:
        order = client.futures_create_order(
            symbol=symbol.upper(),
            side=SIDE_BUY if side.upper() == 'BUY' else SIDE_SELL,
            type="STOP",  # For futures use STOP_MARKET or STOP
            stopPrice=str(stop_price),
            price=str(limit_price),
            quantity=quantity,
            timeInForce=TIME_IN_FORCE_GTC,
            workingType="CONTRACT_PRICE"  # Optional: 'MARK_PRICE' also allowed
        )
        logging.info(f"✅ Stop-Limit Order Placed: {order}")
        return order

    except Exception as e:
        logging.error(f"❌ Stop-Limit Order Failed: {e}")
        raise
