import ccxt
import pandas as pd
import numpy as np
from datetime import datetime, timezone

symbol = 'uBTCUSD'

exchange = ccxt.phemex({
    'apiKey': 'YiJv9IfnhKl6clYcxsqJ6IgFstG6yOAfe0JbeAVI',
    'secret': 'YOUR_API_SECRET'
})


def daily_sma(timeframe='1h', num_bars_per_call=1000):
    """
    Calculates daily SMA using smaller timeframes with pagination.

    Args:
        timeframe (str, optional): Timeframe to use for fetching data (e.g., '1h'). Defaults to '1h'.
        num_bars_per_call (int, optional): Number of bars to fetch per API call. Defaults to 1000.
    """

    print('starting daily SMA...')
    df_d = pd.DataFrame()
    start_time = None

    while True:
        try:
            # Fetch data with pagination
            if not start_time:
                bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=num_bars_per_call)
            else:
                # Use the last timestamp from the previous call
                last_timestamp = df_d['timestamp'].iloc[-1]
                bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=last_timestamp)

            if not bars:
                # No more data available
                break

            df_temp = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])

            # Convert timestamps to datetime objects (adjust based on Phemex's format)
            df_temp['timestamp'] = pd.to_datetime(df_temp['timestamp'], unit='ns')  # Assuming nanoseconds

            df_d = pd.concat([df_d, df_temp], ignore_index=True)
            start_time = df_temp['timestamp'].iloc[-1]  # Update start time for next call

        except TypeError as e:
            print(f"Error converting timestamps: {e}")
            print(f"Unit returned by exchange.parseTimeframe(timeframe): {exchange.parseTimeframe(timeframe)}")
            break

    # Check if data covers at least one day
    if len(df_d) > 0 and df_d['timestamp'].dt.day.nunique() >= 1:
        # Ensure timestamp is datetime64 and check for duplicates
        df_d['timestamp'] = pd.to_datetime(df_d['timestamp'])
        if not df_d['timestamp'].is_unique:  # Check if no duplicates
            print("Timestamp index has duplicates. Ensure unique timestamps for resampling.")
        else:
            # Calculate daily SMA based on OHLC data
            daily_sma = df_d['close'].resample('D').mean()
            print(f"Daily SMA calculated successfully!")
    else:
        print("Insufficient data to calculate daily SMA. Consider adjusting timeframe or num_bars_per_call.")

    # ... rest of your code for processing daily_sma


def f15_sma():
    print('starting 15 min sma...')
    timeframe = '15m'
    num_bars = 100
    bars = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=num_bars)
    print(bars)
    df_