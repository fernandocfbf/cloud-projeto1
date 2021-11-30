from datetime import datetime

from requests.sessions import merge_hooks

from functions.utils.create_log import create_log
from endpoints import tasks

method = input('GET/POST/DELETE: ')
if method == '':
    create_log('Closing API')   
    quit()
if method.lower() == 'get':
    url = input('url: ')
    tasks.get(url)
elif method.lower() == 'post':
    url = input('url: ')
    title = input('title: ')
    date = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    description = input('description: ')
    dictionaty = {'title': title, 'date': date, 'description': description}
    tasks.post(url, dictionaty)

    
