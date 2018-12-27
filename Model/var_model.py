import numpy as np
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas
from dod_model import test, train, cols
from posData_preprocessing import posData

#Log transform
#train["guests"] = train["guests"].mask(train["guests"] == 0, 0.0001)
train['guests_log'] = np.log(train['guests'])
train['guests_log_diff'] = train['guests_log'] - train['guests_log'].shift(1)
train['guests_log_diff'] = train['guests_log_diff'].dropna()
#train['guests_log_diff'].dropna().plot()

train['temp_log'] = np.log(train['temp'])
train['temp_log_diff'] = train['temp_log'] - train['temp_log'].shift(1)
train['temp_log_diff'] = train['temp_log_diff'].dropna()
train["temp_log_diff"][0] = 0
train["guests_log_diff"][0] = 0
#train['temp_log_diff'].dropna().plot()

#FIT THE MODEL
from statsmodels.tsa.vector_ar.var_model import VAR
model = VAR(endog=train.values.tolist())
model_fit = model.fit()

# make prediction on validation
prediction = model_fit.forecast(model_fit.y, steps=len(test))

#converting predictions to dataframe
pred = pandas.DataFrame(index=range(0,len(prediction)),columns=cols)
pred.index = test.index
for j in range(0,6):
    for i in range(0, len(prediction)):
       pred.iloc[i][j] = prediction[i][j]


#check rmse
for i in cols:
    print('rmse value for', i, 'is : ', sqrt(mean_squared_error(pred[i], test[i])))
    
#make final predictions
model = VAR(endog=posData.values.tolist())
model_fit = model.fit()
yhat = model_fit.forecast(model_fit.y, steps=1)
print(yhat)
    
yhat = pandas.DataFrame(yhat, columns=cols)

pred["guests"].plot()
test["guests"].plot()