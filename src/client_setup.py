from binance.client import Client
from src.config import API_KEY, API_SECRET

def get_binance_client(testnet=True):
    client = Client(API_KEY, API_SECRET)
    if testnet:
        client.API_URL = "https://testnet.binancefuture.com/fapi"
        client.ping()
    return client
