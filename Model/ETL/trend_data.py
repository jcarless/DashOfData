from pytrends.request import TrendReq
import pandas as pd

pytrends = TrendReq(hl='en-US', tz=360)
kw_list = ["restaurant","yelp","restaurants near me","best restaurants","top restaurants"]

pytrends.build_payload(kw_list, cat=0, timeframe='2014-01-01 2018-11-01', geo='US', gprop='')
US_kisearch_df=pytrends.interest_over_time()
US_kisearch_df.head()

pytrends.build_payload(kw_list, cat=0, timeframe='2014-01-01 2018-11-01', geo='US-NY-501', gprop='')

NYC_kisearch_df=pytrends.interest_over_time()
df = NYC_kisearch_df
df["date"] = df.index
print(df["yelp"][0])


# for keyword in NYC_kisearch_df["yelp"]:
#     print(keyword)

# writer = pd.ExcelWriter('GoogleTrends_Restaurant Keyword Search.xlsx')
# NYC_kisearch_df.to_excel(writer,'NYC')
# US_kisearch_df.to_excel(writer,'US')
# writer.save