import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timezone

symbol = 'uBTCUSD'

exchange = ccxt.phemex({
    'apiKey': 'YiJv9IfnhKl6clYcxsqJ6IgFstG6yOAfe0JbeAVI',
    'secret': 'YOUR_API_SECRET'
})

# Find daily SMA using historical data endpoint
def daily_sma():
    print('starting indis...')
    df_d = pd.DataFrame()

    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe='1d', limit=10)  # Replace with Phemex's specific parameters

        df_d = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

        # Convert timestamps to datetime objects (might require adjustments based on Phemex's response format)
        df_d['timestamp'] = pd.to_datetime(df_d['timestamp'], unit='ms')  # Assuming timestamps in milliseconds

        # ... rest of your code for processing df_d
    except ccxt.BaseError as e:
        print(f"Error fetching historical data: {e}")

def f15_sma():
    print('starting 15 min sma...')
    timeframe = '15m'
    num_bars = 100
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=num_bars)
    print(bars)
    df_f = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])


# Call the functions
daily_sma()
f15_sma()