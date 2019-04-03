from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas
from dod_model import test, train
from config_model import cols
from posData_preprocessing import posData

#FIT THE MODEL
from statsmodels.tsa.vector_ar.var_model import VAR
model = VAR(endog=train.values.tolist())
model_fit = model.fit()

# make prediction on validation
prediction = model_fit.forecast(model_fit.y, steps=len(test))

#converting predictions to dataframe
pred = pandas.DataFrame(index=range(0, len(prediction)),columns=cols)
pred.index = test.index
for j in range(0, 11):
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