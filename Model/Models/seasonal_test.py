import dod_model
train = dod_model.train
test = dod_model.test

#Seasonal
train['guests'] = train['guests'].dropna()
n=7
train['guests_diff'] = train['guests'] - train['guests'].shift(n)
train['guests_diff'].dropna().plot()

train['temp'] = train['temp'].dropna()
n=7
train['temp_diff'] = train['temp'] - train['temp'].shift(n)
train['temp_diff'].dropna().plot()

train['guests'] = train['guests'].fillna(0)
train['temp'] = train['temp'].fillna(0)
      
train['temp'] = int(train['temp'])