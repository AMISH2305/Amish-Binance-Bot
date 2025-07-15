from binance.client import Client
from src.config import API_KEY, API_SECRET
import logging

def get_binance_client(testnet=True):
    """
    Create and return a Binance client configured for testnet or mainnet
    """
    try:
        # Validate API credentials
        if not API_KEY or not API_SECRET:
            raise ValueError("API_KEY and API_SECRET must be provided")
        
        if testnet:
            # For Binance Futures Testnet
            client = Client(API_KEY, API_SECRET, testnet=True)
            # Set the correct testnet URL
            client.API_URL = 'https://testnet.binancefuture.com'
            client.FUTURES_URL = 'https://testnet.binancefuture.com'
        else:
            # For mainnet
            client = Client(API_KEY, API_SECRET)
        
        # Test connection
        try:
            client.ping()
            print("Successfully connected to Binance API")
        except Exception as ping_error:
            print(f"Warning: Ping failed - {ping_error}")
            # Don't raise here, let the calling code handle it
        
        return client
        
    except Exception as e:
        print(f"Error creating Binance client: {e}")
        raise e
