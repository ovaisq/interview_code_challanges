#!/usr/bin/env python3
"""To demonstrate data synchronization between multiple instances of the same
	service or different services using the caching service, we can create a
	Python function that updates or invalidates cached data based on changes
	made in the system.

	In this example, let's consider a scenario where a user's profile
	information is updated in one instance of the service, and we want to ensure
	that the updated profile information is synchronized across all instances.
	We'll create a function that updates the user's profile information in the
	backend data source and then notifies the caching service to invalidate
	the corresponding cached data for that user's profile.
"""

import requests
import json
from config import get_config

# Define the URL of the caching service endpoint with HTTPS
CACHE_URL = 'https://localhost:8000/cache'
LOGIN_URL = 'https://localhost:8000/login'

# Get config
CONFIG = get_config()

# API key
API_KEY = CONFIG.get('service','SRVC_SHARED_SECRET')

# Define the URL of the backend data source with HTTPS
BACKEND_URL = 'https://backend-service-url/profiles'


def get_access_token(api_key):
    """Get JWT token
    """

    payload = {'api_key': api_key}
    response = requests.post(LOGIN_URL, json=payload, verify=False)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

def update_profile(user_id, new_profile_data, access_token):
	"""Update user profile data, invalidate cache
	"""

    # 1: Update profile data in the backend data source
    response = update_backend_profile(user_id, new_profile_data, access_token)
    if response.status_code == 200:
        # 2: Invalidate cached profile data in the caching service
        invalidate_cached_profile(user_id, access_token)
        return True
    else:
        return False

def update_backend_profile(user_id, new_profile_data, access_token):
	"""Update user profile in backend
	"""

    url = f"{BACKEND_URL}/{user_id}"
    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    response = requests.put(url, headers=headers, json=new_profile_data)
    return response

def invalidate_cached_profile(user_id, access_token):
	"""Invalidate Cache data
	"""

    headers = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
    payload = {'command': 'DELETE', 'key': f"profile:{user_id}"}
    response = requests.post(CACHE_URL, headers=headers, json=payload, verify=False)
    return response.json()

if __name__ == "__main__":
    user_id = '123456'
    new_profile_data = {
        'name': 'Updated Name',
        'email': 'updated_email@example.com',
        'age': 30,
        # Add other fields as needed
    }

    # get access token
    access_token = get_access_token(API_KEY)
    if access_token:
        # update user profile
        success = update_profile(user_id, new_profile_data, access_token)
        if success:
            print("User profile updated successfully.")
        else:
            print("Failed to update user profile.")
    else:
        print("Failed to obtain access token.")

