from binance.enums import SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
from client_setup import get_binance_client
import logging

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

client = get_binance_client()

def place_grid_orders(symbol, side, quantity, lower_price, upper_price, grid_levels):
    """
    Places grid limit orders in a defined price range.

    Args:
        symbol (str): e.g., BTCUSDT
        side (str): "BUY" or "SELL"
        quantity (float): order size for each level
        lower_price (float): lower bound of grid
        upper_price (float): upper bound of grid
        grid_levels (int): number of grid orders

    Returns:
        list: API responses
    """
    price_step = (upper_price - lower_price) / (grid_levels - 1)
    orders = []

    print(f"📈 Placing {grid_levels} {'BUY' if side=='BUY' else 'SELL'} grid orders from {lower_price} to {upper_price}")

    for i in range(grid_levels):
        price = round(lower_price + (i * price_step), 2)

        try:
            order = client.futures_create_order(
                symbol=symbol.upper(),
                side=SIDE_BUY if side.upper() == "BUY" else SIDE_SELL,
                type="LIMIT",
                price=str(price),
                quantity=quantity,
                timeInForce=TIME_IN_FORCE_GTC
            )
            logging.info(f"✅ Grid Order Placed at {price}: {order}")
            print(f"✅ Order {i+1}/{grid_levels} @ {price}")
            orders.append(order)

        except Exception as e:
            logging.error(f"❌ Grid Order Failed at {price}: {e}")
            print(f"❌ Failed @ {price}: {e}")

    return orders
