def lags(df, name):
    import pandas as pd
    df = df.rename(columns={
                            'index_name': name+"_index_name", 
                            'symbol': name, 
                            'close': name+"_close"
                            })
    
    ##Create list of multiples
    
    multiple_list=[]
    
    for x in range(1,85):
        if x % 7==0:
            multiple_list.append(x)
    
    max_multiple=max(multiple_list)
    
    
    #loop through each column and add lag columns based on the 'multiple_list'        
    for each_column in df.columns:
        for lag_multiple in multiple_list:
            df.loc[:,each_column+"_lag_"+str(lag_multiple)] = df[each_column].shift(lag_multiple)
    
    #drop dependent variable column lags
    df = df[df.columns[~df.columns.str.startswith('symbol_lag_')]]
    df = df[df.columns[~df.columns.str.startswith('index_name_lag_')]]
    
    #remove NaN from lag shift based on max multiple
    df=df.iloc[max_multiple:]
    
    df = pd.concat([df[df.columns[2]], df[df.columns[27:38]]], axis=1)
    return df.astype("float")

if __name__ == "__main__":
    import sys
    sys.path.append("Model/PreProcessing")
    from indicies_preprocessing import get_marketData
    marketData = get_marketData()

    lag = lags(marketData[0], marketData[0]["symbol"][0])

