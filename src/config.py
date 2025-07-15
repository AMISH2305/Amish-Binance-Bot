import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = BINANCE_API_KEY
API_SECRET = BINANCE_API_SECRET

if not API_KEY or not API_SECRET:
    raise ValueError("❌ API credentials not found in .env file.")
