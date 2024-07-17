import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from helper import macd
from helper import trend_line


def get_data(data):
    data.fillna(0, inplace=True)
    data = data.apply(pd.to_numeric, errors='coerce')
    data = np.log(data)
    data = macd.calculate_macd(data)
    data = trend_line.add_moving_average(data, window_H1)
    open_data = data[open_variable].head(window_H1)
    close_data = data[close_variable].head(window_H1)
    return data, open_data, close_data


coefficients = []
levels = []
window_H1 = 30
api_key = "F5L80GN4QX59LI4P"
open_variable = '1. open'
close_variable = '4. close'

ts = TimeSeries(key=api_key, output_format='pandas')
# data_H1, meta_data = ts.get_intraday('DIA', interval='60min')
#1 Hour data
data_H1, meta_data = ts.get_intraday('NDX', interval='60min')
data_H1, open_data_H1, close_data_H1 = get_data(data_H1)

###

#30 minute data
data_M30, meta_data = ts.get_intraday('NDX', interval='30min')
data_M30, open_data_M30, close_data_M30 = get_data(data_M30)
###


#5 minute data
data_M5, meta_data = ts.get_intraday('NDX', interval='5min')
data_M5, open_data_M5, close_data_M5 = get_data(data_M5)
###

#Higher time frame
if data_H1['MA-DIFF'].head(window_H1).mean() < 0:
    coefficients = trend_line.resistance_line_finder_bearish(open_data_H1, close_data_H1)
    levels = trend_line.fibonacci_retracement(data_H1.reset_index(drop=True).head(window_H1), -1)
    print("downward trend")
elif data_H1['MA-DIFF'].head(window_H1).mean() > 0:
    coefficients = trend_line.resistance_line_finder_bullish(open_data_H1, close_data_H1)
    levels = trend_line.fibonacci_retracement(data_H1.reset_index(drop=True).head(window_H1), 1)
    print("upward trend")
else:
    print("The market is trending!!")


#Make main engine!!