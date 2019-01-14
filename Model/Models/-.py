import numpy as np
import pandas as pd


##Create list of multiples

multiple_list=[]

for x in range(1,85):
    if x % 7==0:
        multiple_list.append(x)

max_multiple=max(multiple_list)




##loop through each column and add lag columns based on the 'multiple_list'        
for each_column in df.columns:
    for lag_multiple in multiple_list:
        df.loc[:,each_column+"_lag_"+str(lag_multiple)] = df[each_column].shift(lag_multiple)

##drop dependent variable column lags
df = df[df.columns[~df.columns.str.startswith('guests_lag_')]]

##remove NaN from lag shift based on max multiple
df=df.iloc[max_multiple:(-1*max_multiple)]



