import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries

def calculate_macd(df, short_window=12, long_window=26):
    closing_price = '4. close'
    if closing_price not in df.columns:
        raise ValueError("DataFrame must contain a 'closing_price' column")

    # Define the column names
    ema_short_col = 'EMA_short'
    ema_long_col = 'EMA_long'
    macd_col = 'MACD'

    # Remove columns if they already exist
    for col in [ema_short_col, ema_long_col, macd_col]:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)

    # Calculate the short-term EMA
    df[ema_short_col] = df[closing_price].ewm(span=short_window, adjust=False).mean()

    # Calculate the long-term EMA
    df[ema_long_col] = df[closing_price].ewm(span=long_window, adjust=False).mean()

    # Calculate the MACD
    df[macd_col] = df[ema_short_col] - df[ema_long_col]

    return df


api_key = "F5L80GN4QX59LI4P"

ts = TimeSeries(key=api_key, output_format='pandas')


data, meta_data = ts.get_intraday('EURUSD', interval='60min')

data.fillna(0, inplace=True)

data = data.apply(pd.to_numeric, errors='coerce')

data = np.log(data)

data = calculate_macd(data.head())

print(data)

