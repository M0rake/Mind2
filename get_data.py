from alpha_vantage.timeseries import TimeSeries
import numpy as np
import pandas as pd

api_key = "F5L80GN4QX59LI4P"

ts = TimeSeries(key=api_key, output_format='pandas')

# Get intraday data
data, meta_data = ts.get_intraday('EURUSD', interval='5min')

# Convert 'date' column to datetime and set it as index
data['date'] = data.index.astype('datetime64[s]')

data.fillna(0, inplace=True)

# Convert non-numeric values to numeric format (if possible)
data = data.apply(pd.to_numeric, errors='coerce')

# Apply natural logarithm to numerical columns
data = np.log(data)
#
# data.to_csv('data.txt', sep='\t', index=False)
# Reset the index and drop the existing index column
data_reset_index = data.reset_index(drop=True)

# Extract the '2. high' column and convert its values to float
high_values = data_reset_index['2. high'].head().astype(float)

print(high_values)
