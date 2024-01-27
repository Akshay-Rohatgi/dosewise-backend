import requests

def get_data(url):
    response = requests.get(url)
    return response.json()