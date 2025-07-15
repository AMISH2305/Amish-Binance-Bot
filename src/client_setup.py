from binance.client import Client
from config import API_KEY, API_SECRET

def get_binance_client(testnet=True):
    client = Client(API_KEY, API_SECRET)
    if testnet:
        client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
    return client
