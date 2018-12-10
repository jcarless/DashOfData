from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt

ts = TimeSeries(key='7WPQAG2NRC8PLFIZ', output_format='pandas')
# data, meta_data = ts.get_daily(symbol='NRN', outputsize='full')
data, meta_data = ts.get_daily(symbol='XLY', outputsize='full')

print(data.tail(5))
data['4. close'].plot()
plt.title('Intraday Times Series for the MSFT stock (1 min)')
plt.show()