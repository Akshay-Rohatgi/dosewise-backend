import requests
import datetime 

def date_difference_in_days(date_str1, date_str2):
    date1 = datetime.strptime(date_str1, '%Y-%m-%d')
    date2 = datetime.strptime(date_str2, '%Y-%m-%d')

    difference_in_days = (date2 - date1).days

    return difference_in_days

def get_data(url):
    response = requests.get(url)
    return response.json()

