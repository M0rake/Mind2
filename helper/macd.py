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