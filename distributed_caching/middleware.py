#!/usr/bin/env python3
"""Example that integrates the caching service as a middleware between
    the client-facing service and the backend data sources
"""

import requests
import json
from config import get_config

# disable SSL certificate verification (for development only)
requests.packages.urllib3.disable_warnings()

# Define the URL of the caching service endpoint
CACHE_URL = 'https://localhost:5000/cache'
LOGIN_URL = 'https://localhost:5000/login'

CONFIG = get_config()

# API key 
API_KEY = CONFIG.get('service','SRVC_SHARED_SECRET')

def get_access_token(api_key):
    """Get JWT token
    """

    payload = {'api_key': api_key}
    response = requests.post(LOGIN_URL, json=payload, verify=False)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

def write_to_cache(key, value, access_token):
    """Write data to the cache
    """

    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    payload = {'command': 'WRITE', 'key': key, 'value': value}
    response = requests.post(CACHE_URL, headers=headers, json=payload, verify=False)
    return response.json()

def read_from_cache(key, access_token):
    """Read data from the cache
    """

    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    payload = {'command': 'READ', 'key': key}
    response = requests.post(CACHE_URL, headers=headers, json=payload, verify=False)
    return response.json()

def fetch_from_backend(key):
	"""Get data from backend
	"""

    #TODO 
    pass
    response = requests.get(BACKEND_URL + '/' + key, verify=False)
    return response

def get_data_from_cache_or_backend(key):
	"""Get data from cache or the backend
	"""

    access_token = get_access_token(API_KEY)
    if access_token:
        cache_response = read_from_cache(key, access_token)
        if cache_response.get('status') == 'SUCCESS':
            return cache_response['value']
        else:
            backend_response = fetch_from_backend(key)
            if backend_response.status_code == 200:
                cache_response = write_to_cache(key, backend_response.json(), access_token)
                if cache_response.get('status') == 'SUCCESS':
                    return backend_response.json()
                else:
                    return None  # Failed to cache data
            else:
                return None  # Failed to fetch data from backend
    else:
        return None  # Failed to obtain access token

if __name__ == "__main__":
    key = 'example_key'
    data = get_data_from_cache_or_backend(key) #TODO
    if data is not None:
        print("Data:", data)
    else:
        print("Failed to retrieve data.")

