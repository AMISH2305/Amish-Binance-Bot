from binance.enums import SIDE_BUY, SIDE_SELL, TIME_IN_FORCE_GTC
from src.client_setup import get_binance_client
import logging

# Setup logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

client = get_binance_client()

def place_oco_simulated(symbol, side, quantity, take_profit_price, stop_price):
    """
    Simulates an OCO order for Futures by placing:
    - a LIMIT take-profit order
    - a STOP_MARKET stop-loss order

    Args:
        symbol (str): e.g. BTCUSDT
        side (str): BUY or SELL
        quantity (float): order size
        take_profit_price (float): profit target
        stop_price (float): stop-loss trigger

    Returns:
        dict: dict with both order responses
    """
    try:
        # Take-Profit Limit Order
        tp_order = client.futures_create_order(
            symbol=symbol.upper(),
            side=SIDE_SELL if side.upper() == 'BUY' else SIDE_BUY,
            type="LIMIT",
            quantity=quantity,
            price=str(take_profit_price),
            timeInForce=TIME_IN_FORCE_GTC
        )

        # Stop-Loss Market Order
        sl_order = client.futures_create_order(
            symbol=symbol.upper(),
            side=SIDE_SELL if side.upper() == 'BUY' else SIDE_BUY,
            type="STOP_MARKET",
            stopPrice=str(stop_price),
            quantity=quantity,
            workingType="CONTRACT_PRICE"
        )

        logging.info(f"✅ OCO simulated - TP: {tp_order['orderId']}, SL: {sl_order['orderId']}")
        return {"take_profit_order": tp_order, "stop_loss_order": sl_order}

    except Exception as e:
        logging.error(f"❌ OCO Simulation Failed: {e}")
        raise
