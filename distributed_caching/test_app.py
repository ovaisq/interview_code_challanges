#!/usr/bin/env python3
"""Sample program to test the caching service
   how-to:
        ./test_app.py
        Write Response: {'command': 'WRITE', 'status': 'SUCCESS', 'value': 'my_value'}
        Read Response: {'command': 'READ', 'status': 'SUCCESS', 'value': 'my_value'}
        Delete Response: {'command': 'DELETE', 'message': 'my_key Key deleted', 'status': 'SUCCESS'}
"""

import requests
import json
from config import get_config

# disable SSL certificate verification (for development only)
requests.packages.urllib3.disable_warnings()

# define the URL of the caching service endpoint
CACHE_URL = 'https://localhost:8000/cache'
LOGIN_URL = 'https://localhost:8000/login'

CONFIG = get_config()

def get_access_token(api_key):
    """Get JWT token
    """

    payload = {
        'api_key': api_key
    }
    response = requests.post(LOGIN_URL, json=payload, verify=False)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

def write_to_cache(key, value, access_token):
    """Write data to the cache
    """

    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    payload = {
        'command': 'WRITE',
        'key': key,
        'value': value
    }
    response = requests.post(CACHE_URL, headers=headers, json=payload, verify=False)
    return response.json()

def read_from_cache(key, access_token):
    """Read data from the cache
    """

    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    payload = {
        'command': 'READ',
        'key': key
    }
    response = requests.post(CACHE_URL, headers=headers, json=payload, verify=False)
    return response.json()

def delete_from_cache(key, access_token):
    """Delete data from the cache
    """

    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    payload = {
        'command': 'DELETE',
        'key': key
    }
    response = requests.post(CACHE_URL, headers=headers, json=payload, verify=False)
    return response.json()

if __name__ == "__main__":

    api_key = CONFIG.get('service','SRVC_SHARED_SECRET')

    # get JWT token
    access_token = get_access_token(api_key)
    if access_token:
        # write data to the cache
        write_response = write_to_cache('my_key', 'my_value', access_token)
        print("Write Response:", write_response)

        # read data from the cache
        read_response = read_from_cache('my_key', access_token)
        print("Read Response:", read_response)

        # delete data from the cache
        delete_response = delete_from_cache('my_key', access_token)
        print("Delete Response:", delete_response)
    else:
        print("Failed to obtain access token.")
