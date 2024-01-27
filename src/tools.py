import requests
import datetime 

def date_difference_in_days(date_str1, date_str2):
    date1 = datetime.datetime.strptime(date_str1, '%Y-%d-%m')
    date2 = datetime.datetime.strptime(date_str2, '%Y-%d-%m')

    difference_in_days = (date2 - date1).days

    return difference_in_days

def date_difference_in_hours(date_str1, date_str2):
    date1 = datetime.datetime.strptime(date_str1, '%Y-%d-%m')
    date2 = datetime.datetime.strptime(date_str2, '%Y-%d-%m')

    difference_in_hours = (date2 - date1).total_seconds() / 3600

    return difference_in_hours

def get_data(url):
    response = requests.get(url)
    return response.json()

