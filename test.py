import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the stock symbol and timeframe
ticker = "AAPL"
interval = "1m"

# Fetch historical data
data = yf.download(ticker, interval=interval, period="1d")

# Calculate a simple moving average (SMA)
sma = data["Close"].rolling(window=10).mean()

# Define a mean reversion strategy
def mean_reversion_strategy(data, sma):
    signals = pd.DataFrame(index=data.index)
    signals['position'] = 0

    # Use loc for assignment
    signals.loc[sma > data['Close'], 'position'] = 1
    signals.loc[sma < data['Close'], 'position'] = -1

    # Calculate buy and sell signals
    signals['buy'] = signals['position'].diff() == 1
    signals['sell'] = signals['position'].diff() == -1

    return signals

# Get the trading signals
signals = mean_reversion_strategy(data, sma)

# Calculate returns, cumulative returns, and profits
returns = data['Close'].pct_change()
strategy_returns = returns * signals['position'].shift(1)
cumulative_returns = (1 + strategy_returns).cumprod()
profits = cumulative_returns * 1000  # Assuming initial investment of $1000

# Print profits and buy/sell signals
print("Profits:", profits.iloc[-1])
print("Buy Signals:", signals['buy'].sum())
print("Sell Signals:", signals['sell'].sum())

# Plot the results
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(data['Close'], label='Price')
plt.plot(sma, label='SMA')
plt.legend()
plt.title("Price and SMA")

plt.subplot(2, 1, 2)
plt.plot(cumulative_returns)
plt.title("Cumulative Returns")

plt.tight_layout()
plt.show()