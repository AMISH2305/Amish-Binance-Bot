import time
from binance.enums import SIDE_BUY, SIDE_SELL
from client_setup import get_binance_client
import logging

# Setup logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

client = get_binance_client()

def place_twap_orders(symbol, side, total_quantity, chunks, interval_sec):
    """
    Places a TWAP-style order by splitting into smaller market orders.

    Args:
        symbol (str): e.g., BTCUSDT
        side (str): BUY or SELL
        total_quantity (float): Total order quantity
        chunks (int): Number of smaller orders
        interval_sec (int): Time between orders (in seconds)

    Returns:
        list: Order responses
    """
    qty_per_order = round(total_quantity / chunks, 6)
    responses = []

    print(f"\n🔁 Executing TWAP: {chunks} x {qty_per_order} {side} orders every {interval_sec} sec\n")

    for i in range(chunks):
        try:
            order = client.futures_create_order(
                symbol=symbol.upper(),
                side=SIDE_BUY if side.upper() == 'BUY' else SIDE_SELL,
                type="MARKET",
                quantity=qty_per_order
            )
            logging.info(f"✅ TWAP Order {i+1}/{chunks}: {order}")
            print(f"✅ Placed order {i+1}/{chunks} | Order ID: {order['orderId']}")
            responses.append(order)

        except Exception as e:
            logging.error(f"❌ TWAP Order {i+1} Failed: {e}")
            print(f"❌ Failed order {i+1}: {e}")

        if i < chunks - 1:
            time.sleep(interval_sec)

    return responses
