import requests
from functions.utils.create_log import create_log

def get(url):
    create_log('GET {0}'.format(url))
    response = requests.get(url)
    create_log('GET response {0}'.format(response))
    return response

def post(url, json):
    create_log('POST {0}'.format(url))
    response = requests.post(
        url=url,
        data={
            'title': json['title'],
            'pub_date': json['date'],
            'description': json['description']
        }
    )
    create_log('POST response {0}'.format(response))
    return response