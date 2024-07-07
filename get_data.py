import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange

# Your Alpha Vantage API key
api_key = 'YOUR_API_KEY'

# Create a ForeignExchange object
fx = ForeignExchange(key=api_key)

# Fetch daily data
data, meta_data = fx.get_currency_exchange_daily(from_symbol='EUR', to_symbol='USD')

# Convert to DataFrame for easier manipulation
df = pd.DataFrame.from_dict(data, orient='index')
df.index = pd.to_datetime(df.index)
df = df.astype(float)

# Sort the DataFrame by date to ensure the most recent data is at the end
df = df.sort_index()

# Specify the start date
start_date = '2021-05-15'

# Filter the DataFrame from the specified start date
df_filtered = df.loc[start_date:]

# Optional: Limit to the most recent 200 entries
df_recent_200 = df_filtered.tail(200)

# Display the filtered DataFrame
print(df_recent_200)
