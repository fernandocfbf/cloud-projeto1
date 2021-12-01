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
    if url.split('/')[3] == 'users':
        username = input('username: ')
        email = input('email: ')
        #groups = input('groups: ')
        dictionaty = {"username": username, "email": email}
        print(dictionaty)
        tasks.post(url, dictionaty)
    elif url.split('/')[3] == 'groups':
        name = input('name: ')
        dictionaty = {"name": name}
        tasks.post(url, dictionaty, end='groups')
    else:
        create_log('Closing API')   
    

    
