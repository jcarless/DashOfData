import matplotlib.pyplot as plt
import matplotlib.style as style
from posData_preprocessing import get_posData
from weatherData_preprocessing import get_weatherData

## NY
#account_id = 1
#city_id = 5128581
#start_date = '2014-03-01'
#end_date = '2018-05-01'

# CT
account_id = 2
city_id = 4843564
start_date = '2018-01-02'
end_date = '2019-01-30'

posData = get_posData(account_id, start_date, end_date)
weatherData = get_weatherData(city_id, start_date, end_date)

#style.use('fivethirtyeight')
#
#plt.hist(posData["guests_log_diff"])
#plt.title("Histogram of Guest Log Diff - Connecticut")
#plt.grid(False)
#plt.show()

posData["total_sales"].plot()
posData["guests"].plot()

