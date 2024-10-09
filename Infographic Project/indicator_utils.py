import pandas as pd

def calculate_sma(data, window=20):
    return data['close_price'].rolling(window=window).mean()

def calculate_ema(data, window=20):
    return data['close_price'].ewm(span=window, adjust=False).mean()

def calculate_bollinger_bands(data, window=20, num_std_dev=2):
    sma = calculate_sma(data, window)
    std_dev = data['close_price'].rolling(window=window).std()
    upper_band = sma + (std_dev * num_std_dev)
    lower_band = sma - (std_dev * num_std_dev)
    return sma, upper_band, lower_band

def calculate_keltner_channels(data, window=20, atr_multiplier=2):
    typical_price = (data['high_price'] + data['low_price'] + data['close_price']) / 3
    ema_typical_price = typical_price.ewm(span=window, adjust=False).mean()
    atr = calculate_atr(data, window=window)
    upper_channel = ema_typical_price + atr_multiplier * atr
    lower_channel = ema_typical_price - atr_multiplier * atr
    return ema_typical_price, upper_channel, lower_channel

def calculate_envelopes(data, window=20, deviation=0.1):
    sma = data['close_price'].rolling(window=window).mean()
    upper_envelope = sma * (1 + deviation)
    lower_envelope = sma * (1 - deviation)
    return upper_envelope, lower_envelope

def calculate_atr(data, window=14):
    high_low = data['high_price'] - data['low_price']
    high_close_prev = abs(data['high_price'] - data['close_price'].shift(1))
    low_close_prev = abs(data['low_price'] - data['close_price'].shift(1))
    true_range = pd.concat([high_low, high_close_prev, low_close_prev], axis=1).max(axis=1)
    atr = true_range.ewm(span=window, adjust=False).mean()
    return atr


def calculate_price_channels(data, window=20):
    high_channel = data['high_price'].rolling(window=window).max()
    low_channel = data['low_price'].rolling(window=window).min()
    return high_channel, low_channel

