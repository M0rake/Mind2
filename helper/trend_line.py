import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange


#THIS IS A REGION AND NOT A LINE, KEEP THAT IN MIND

def add_moving_average(df: pd.DataFrame, window: int) -> pd.DataFrame:
    df['MA'] = df['3. low'].rolling(window=window).mean()
    return df

def resistance_line_finder_bearish(data1, data2):
    vec1 = []
    vec2 = []
    points = []
    in_order1 = sorted(data1)
    in_order2 = sorted(data2)

    def has_higher_number_sorted(target):
        left = 0
        right = len(in_order1) - 1

        while left <= right:
            mid = (left + right) // 2
            if in_order1[mid] > target:
                return True
            elif in_order1[mid] <= target:
                left = mid + 1
        return False

    def has_smaller_number_sorted(target):
        left = 0
        right = len(in_order2) - 1

        while left <= right:
            mid = (left + right) // 2
            if in_order2[mid] < target:
                return True
            elif in_order2[mid] >= target:
                right = mid - 1
        return False

    for i in range(len(data1)):
        vec1.append([i, data1[i]])
        vec2.append([i, data2[i]])

    half_points = []
    while vec1:
        if not has_higher_number_sorted(vec1[0][1]):
            half_points.append(vec1[0])
        try:
            in_order1.remove(vec1[0][1])
        except ValueError:
            print(f"Warning: {vec1[0][1]} not found in in_order1")
        vec1.pop(0)
    points.append(half_points)
    if len(half_points) > 2:
        half_points.pop()

    half_points = []
    while vec2:
        if not has_smaller_number_sorted(vec2[-1][1]):
            half_points.append(vec2[-1])
        try:
            in_order2.remove(vec2[-1][1])
        except ValueError:
            print(f"Warning: {vec2[-1][1]} not found in in_order2")
        vec2.pop()

    points.append(half_points)
    if len(half_points) > 2:
        half_points.pop()

    if len(points) == 0:
        return []
    answer = []
    for k in range(len(points)):
        model = LinearRegression()
        x = []
        for i in range(len(points[k])):
            x.append([points[k][i][0]])
        y = [point[1] for point in points[k]]
        model.fit(x, y)
        answer.append([model.intercept_, model.coef_[0]])

    return sorted(answer, key=lambda x: x[0], reverse=True)


def resistance_line_finder_bullish(data1, data2):
    vec1 = []
    vec2 = []
    points = []
    in_order1 = sorted(data1)
    in_order2 = sorted(data2)

    def has_higher_number_sorted(target):
        left = 0
        right = len(in_order1) - 1

        while left <= right:
            mid = (left + right) // 2
            if in_order1[mid] > target:
                return True
            elif in_order1[mid] <= target:
                left = mid + 1
        return False

    def has_smaller_number_sorted(target):
        left = 0
        right = len(in_order2) - 1

        while left <= right:
            mid = (left + right) // 2
            if in_order2[mid] < target:
                return True
            elif in_order2[mid] >= target:
                right = mid - 1
        return False

    for i in range(len(data1)):
        vec1.append([i, data1[i]])
        vec2.append([i, data2[i]])

    half_points = []
    while vec1:
        if not has_higher_number_sorted(vec1[-1][1]):
            half_points.append(vec1[-1])
        try:
            in_order1.remove(vec1[-1][1])
        except ValueError:
            print(f"Warning: {vec1[-1][1]} not found in in_order1")
        vec1.pop()
    points.append(half_points)
    if len(half_points) > 2:
        half_points.pop()

    half_points = []
    while vec2:
        if not has_smaller_number_sorted(vec2[0][1]):
            half_points.append(vec2[0])
        try:
            in_order2.remove(vec2[0][1])
        except ValueError:
            print(f"Warning: {vec2[0][1]} not found in in_order2")
        vec2.pop(0)
    points.append(half_points)
    if len(half_points) > 2:
        half_points.pop()

    if len(points) == 0:
        return []
    answer = []
    for k in range(len(points)):
        model = LinearRegression()
        x = []
        for i in range(len(points[k])):
            x.append([points[k][i][0]])
        y = [point[1] for point in points[k]]
        model.fit(x, y)
        answer.append([model.intercept_, model.coef_[0]])

    return sorted(answer, key=lambda x: x[0], reverse=True)


api_key = "F5L80GN4QX59LI4P"

ts = TimeSeries(key=api_key, output_format='pandas')

# Get intraday data
# data, meta_data = ts.get_intraday('DIA', interval='60min')
data, meta_data = ts.get_intraday('EURUSD', interval='60min')

# fx = ForeignExchange(key=api_key)
#
# # Fetch daily data
# data, meta_data = fx.get_currency_exchange_daily(from_symbol='EUR', to_symbol='USD')

# Convert 'date' column to datetime and set it as index
# data['date'] = data.index.astype('datetime64[s]')

# df = pd.DataFrame.from_dict(data, orient='index')
# df.index = pd.to_datetime(df.index)
# data = df.astype(float)

data.fillna(0, inplace=True)

# Convert non-numeric values to numeric format (if possible)
data = data.apply(pd.to_numeric, errors='coerce')

# Apply natural logarithm to numerical columns
data = np.log(data)

# test_data = [20, 19.5, 24, 18, 19, 15, 16.5, 17, 14, 16, 12, 14.5, 15, 10, 14, 14.5, 9, 12, 5, 9, 8.5, 2]
num = 200
test_data1 = data['1. open'].head(num).reset_index(drop=True)
test_data2 = data['4. close'].head(num).reset_index(drop=True)

# test_data = test_data[::-1]

coefficients = []

data = add_moving_average(data, 20)

if data['MA'].iloc[-1] - data['3. low'].iloc[-1] < 0:
    coefficients = resistance_line_finder_bearish(test_data1, test_data2)
    print("downward trend")
elif data['MA'].iloc[-1] - data['3. low'].iloc[-1] > 0:
    coefficients = resistance_line_finder_bullish(test_data1, test_data2)
    print("upward trend")
else:
    print("The market is trending!!")

# coefficients = calculate_trendlines(data)

# Plotting the test_data
plt.plot(test_data1, label='Test Data1')
plt.plot(test_data2, label='Test Data2')

# Plotting the lines
for i, coef in enumerate(coefficients):
    c, m = coef
    line = [m * x + c for x in range(len(test_data1))]
    plt.plot(line, label=f'Line {i + 1}')

# Adding labels and legend
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('Line Graphs')
plt.legend()

# Display the plot
plt.show()
