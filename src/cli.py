from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.client_setup import get_binance_client
import logging

# Configure logging to append to bot.log
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize Binance client
client = get_binance_client()

def show_balance():
    try:
        balance = client.futures_account_balance()
        usdt = next(b for b in balance if b['asset'] == 'USDT')
        print(f"💰 Your USDT Balance: {usdt['balance']}")
        logging.info(f"Checked balance: {usdt['balance']}")
    except Exception as e:
        print("❌ Failed to retrieve balance.")
        logging.error(f"Balance fetch error: {e}")

def main():
    print("=== Binance Futures Testnet Bot ===")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Place Market Order")
        print("2. Place Limit Order")
        print("3. Check Balance")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            symbol = input("Enter trading pair (e.g. BTCUSDT): ").upper()
            side = input("Enter side (BUY or SELL): ").upper()
            quantity = float(input("Enter quantity: "))
            try:
                order = place_market_order(symbol, side, quantity)
                print("✅ Market order placed.")
                print("📝 Order ID:", order['orderId'])
            except Exception as e:
                print("❌ Failed to place market order:", e)

        elif choice == '2':
            symbol = input("Enter trading pair (e.g. BTCUSDT): ").upper()
            side = input("Enter side (BUY or SELL): ").upper()
            quantity = float(input("Enter quantity: "))
            price = input("Enter limit price: ")
            try:
                order = place_limit_order(symbol, side, quantity, price)
                print("✅ Limit order placed.")
                print("📝 Order ID:", order['orderId'])
            except Exception as e:
                print("❌ Failed to place limit order:", e)

        elif choice == '3':
            show_balance()

        elif choice == '4':
            print("👋 Exiting. See you again!")
            break

        else:
            print("❗ Invalid input. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()

