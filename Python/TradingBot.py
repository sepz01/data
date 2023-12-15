import pandas as pd
import numpy as np

# Fetch candlestick data from a CSV file
def fetch_candlestick_data(csv_file_path):
    data = pd.read_csv(csv_file_path, parse_dates=True, index_col='Date')
    return data

# RSI Calculation
def calculate_rsi(data, period=29):
    # Assuming 'data' is a DataFrame with a 'Close' column
    close_prices = data['Close']
    delta = close_prices.diff()
    gains = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    losses = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gains / losses
    rsi = 100 - (100 / (1 + rs))
    return rsi

# MACD Calculation
def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    short_ema = data.ewm(span=short_period, adjust=False).mean()
    long_ema = data.ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=signal_period, adjust=False).mean()
    return macd, signal_line

# Moving Average Calculation
def calculate_moving_average(data, period=20):
    return data.rolling(window=period).mean()

# Variance Calculation
def calculate_variance(data, period=30):
    return data.rolling(window=period).var()

# Interpret Market Signals
def interpret_signals(rsi, macd, signal_line, moving_average, variance):
    signals = {
        'rsi_signal': 'Buy' if rsi[-1] < 30 else 'Sell' if rsi[-1] > 70 else 'Neutral',
        'macd_signal': 'Buy' if macd[-1] > signal_line[-1] else 'Sell' if macd[-1] < signal_line[-1] else 'Neutral',
        'ma_trend': 'Up' if moving_average[-1] > moving_average[-5] else 'Down',
        'market_variance': variance[-1]
    }
    return signals

# Strategy Selection
def select_strategy(signals):
    some_threshold = 0.2  # Example threshold for market variance
    if signals['market_variance'] > some_threshold:
        return 'MACD' if signals['macd_signal'] != 'Neutral' else 'RSI'
    if signals['ma_trend'] == 'Up':
        return 'Running Average' if signals['macd_signal'] == 'Buy' else 'RSI'
    return 'RSI'

# Trading Decision
def make_decision(strategy, signals):
    if strategy == 'RSI':
        return signals['rsi_signal']
    elif strategy == 'MACD':
        return signals['macd_signal']
    elif strategy == 'Running Average':
        return 'Buy' if signals['ma_trend'] == 'Up' else 'Sell'
    else:
        return 'Hold'

# Buy Method
def buy(price, amount, strategy):
    print(f"Buying {amount} units at {price} using {strategy} strategy.")
    # Add logic to execute a buy order through an exchange API

# Sell Method
def sell(price, amount, strategy):
    print(f"Selling {amount} units at {price} using {strategy} strategy.")
    # Add logic to execute a sell order through an exchange API

# Profit Maximization
def maximize_profit(strategy, data, current_price):
    if strategy == "RSI":
        target_buy_price = current_price * 0.95
        target_sell_price = current_price * 1.05
    elif strategy == "MACD":
        target_buy_price = current_price * 0.90
        target_sell_price = current_price * 1.10
    else:
        target_buy_price = current_price * 0.97
        target_sell_price = current_price * 1.03
    return target_buy_price, target_sell_price

# Main Function
def main(csv_file_path):
    data = fetch_candlestick_data(csv_file_path)
    current_price = data['Close'].iloc[-1]
    amount_to_trade = 1  # Example amount

    rsi = calculate_rsi(data['Close'])
    macd, signal_line = calculate_macd(data['Close'])
    moving_average = calculate_moving_average(data['Close'])
    variance = calculate_variance(data['Close'])

    signals = interpret_signals(rsi, macd, signal_line, moving_average, variance)
    strategy = select_strategy(signals)
    decision = make_decision(strategy, signals)

    print(f"Selected Strategy: {strategy}")
    print(f"Trading Decision: {decision}")

    target_buy_price, target_sell_price = maximize_profit(strategy, data, current_price)

    if decision == "Buy":
        buy(target_buy_price, amount_to_trade, strategy)
    elif decision == "Sell":
        sell(target_sell_price, amount_to_trade, strategy)

if __name__ == "__main__":
    csv_file_path = '/Users/sepand69/Desktop/Codes/cleaned_sample_history.csv'    # Replace with your CSV file path
    main(csv_file_path)