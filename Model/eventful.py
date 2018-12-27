import requests
import datetime
from creds import apiKeys

distance = "3"
category = "sports"
     
def get_event(user_key, event_location , start_date, end_date, event_features, fname):
     
    data_lst = []  # output
    start_year = int(start_date[0:4])
    start_month = int(start_date[4:6])
    start_day = int(start_date[6:])
     
    end_year = int(end_date[0:4])
    end_month = int(end_date[4:6])
    end_day = int(end_date[6:])
     
    start_date = datetime.date(start_year, start_month, start_day)
    end_date = datetime.date(end_year, end_month, end_day)
    step = datetime.timedelta(days=1)
     
    while start_date <= end_date:
     
        date = str(start_date.year)
        if start_date.month < 10:
            date += '0' + str(start_date.month)
        else:
            date += str(start_date.month)
     
        if start_date.day < 10:
            date += '0' + str(start_date.day)
        else:
            date += str(start_date.day)
        date += "00"
        date += "-" + date
     
        url = "http://api.eventful.com/json/events/search?"
        url += "&app_key=" + user_key
        url += "&c=" + category
        url += "&location=" + event_location
        url += "&within=" + distance
        url += "&units=miles"
        url += "&date=" + date
        url += "&page_size=250"
        url += "&sort_order=date"
        url += "&sort_direction=descending"
     
        data = requests.get(url).json()
     
        try:
            for i in range(len(data["events"]["event"])):
                data_dict = {}
                for feature in event_features:
                    data_dict[feature] = data["events"]["event"][i][feature]
                data_lst.append(data_dict)
        except:
            pass
     
        # print(data_lst)
        start_date += step
        return data_lst
     
     
def main():
     
    user_key = apiKeys["eventful"]
    event_location = "10009"
    start_date = "20181111"
    end_date = "20181111"
    event_location = event_location.replace("-", " ")
    start_date = start_date
    end_date = end_date
    event_features = ["start_time"]
    event_features += ["city_name", "title"]
    event_fname = "events.csv"
     
    events = get_event(user_key, event_location, start_date, end_date, event_features, event_fname)
    for event in events:
        print("==========")
        print(event)
     
if __name__ == '__main__':
    main()