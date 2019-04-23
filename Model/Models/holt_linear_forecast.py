import os
import sys
sys.path.append("Model/PreProcessing")
sys.path.append("Model/Models")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(
        "/Users/jerome/Documents/NYU/Capstone/DashOfData/Model/Models"
)
from posData_preprocessing import get_posData
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.api import Holt

# # NY
# account_id = 1
# city_id = 5128581
# start_date = '2014-03-01'
# end_date = '2018-05-01'

# CT
account_id = 2
city_id = 4843564
start_date = '2018-01-02'
end_date = '2019-01-30'

posData = get_posData(account_id, start_date, end_date)

def train_test_split(data, n_test):
    return data[:-n_test], data[-n_test:]

# Target variable
target_variable = pd.DataFrame(posData.guests)

# days to forecast
n_test = 7

# Split target variable into training/test set
train, test = train_test_split(target_variable, n_test)

#Model 6
y_hat_avg = test.copy()

fit1 = Holt(np.asarray(train['guests'])).fit(smoothing_level = 0.3,smoothing_slope = 0.1)
y_hat_avg['Holt_linear'] = fit1.forecast(len(test))

plt.figure(figsize=(16,8))
plt.plot(test['guests'], label='Test')
plt.plot(y_hat_avg['Holt_linear'], label='Holt_linear')
plt.title("CT Holt's Linear Trend")
plt.legend(loc='best')
plt.show()

from sklearn.metrics import mean_squared_error
from math import sqrt
rms = sqrt(mean_squared_error(test.guests, y_hat_avg.Holt_linear))
print(rms)