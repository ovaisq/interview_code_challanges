#!/usr/bin/env python3
# cache_client.py
# ©2024, Ovais Quraishi

""" An example client for the caching service 
"""

import jwt
import logging
import os
import redis
import requests
import time

# Import required local modules

from config import get_config

get_config()

def cache_api(endpoint_url, payload=None):
    """Call a protected API endpoint with a JSON payload.
    """

    caching_srvc_login_url = os.environ['caching_srvc_login_url']
    caching_srvc_secret = os.environ['caching_srvc_secret']
    caching_srvc_headers = {"Content-Type": "application/json"}
    caching_srvc_payload = {
                            "client_id" : "rollama",
                            "api_key" : caching_srvc_secret,
                            "grant_type": "client_credentials"
                           }
    curr_token = get_jwt_token(caching_srvc_login_url, caching_srvc_payload, caching_srvc_headers)
    
    url = f"{endpoint_url}"
    headers = {
               "Authorization": f"Bearer {curr_token}",
               "Content-Type": "application/json"
              }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_json = response.json()
        return response_json  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error calling protected API: {e}")
        raise

def get_jwt_token(srvc_url, srvc_payload, headers):
    """Fetch JWT token using the provided authentication payload.
    """

    response = requests.post(srvc_url, json=srvc_payload, headers=headers)
    response.raise_for_status()  # Raise error for bad HTTP response
    token_data = response.json()
    
    return token_data['access_token']

def check_and_refresh_token(jwt_token):
    """Check if a JWT token has expired and refresh it using get_jwt_token if necessary.
    """
    
    try:
        # Decode the token without verifying the signature
        decoded_token = jwt.decode(jwt_token, options={"verify_signature": False})

        # Extract expiration time (exp claim)
        expiration_time = decoded_token.get("exp")

        if not expiration_time:
            raise ValueError("Expiration time ('exp') claim not found in the token.")

        # Compare the current time with the expiration time
        current_time = time.time()
        
        if current_time > expiration_time:
            # Token is expired; fetch a new one using the get_jwt_token function
            print("Token has expired. Fetching a new token...")
            return get_jwt_token()
        
        # Token is still valid
        return jwt_token
    
    except jwt.InvalidTokenError:
        raise ValueError("Invalid JWT token.")  # Raise an exception for invalid tokens

def configure_redis_client() -> redis.StrictRedis:
    """Configure and return a Redis client instance.
        Meant for direct queries to Redis
    """
    
    host = os.environ['redis_host']
    port = os.environ['redis_port']
    password = os.environ['redis_password']

    return redis.StrictRedis(host=host, port=port, password=password)

def add_key(key):
    """Add a key to a set in Redis"""

    caching_srvc_crud_url = os.environ['caching_srvc_crud_url']
    
    if lookup_key(key):
        info_message = f'{key} already exists'
        logging.info(info_message)
        return False
    else:
        data_payload = {"command": "WRITE", "key": key, "value" : "", "expire" : 2592000} #Expires in 30 days
        json_resp = cache_api(caching_srvc_crud_url, payload=data_payload)
        if json_resp['status'] == 'SUCCESS':
            info_message = f'{key} added'
            logging.info(info_message)
            return True

def del_key(key):
    """Invalidate cache by deleting the key in Redis"""
    
    caching_srvc_crud_url = os.environ['caching_srvc_crud_url']
    
    if lookup_key(key):
        data_payload = {"command": "DELETE", "key": key}
        json_resp = cache_api(caching_srvc_crud_url, payload=data_payload)
        if json_resp['status'] == 'SUCCESS':
            info_message = f'{key} added'
            logging.info(info_message)
            return True
        else:
            info_message = f'{key} deletion appears to have failed. Retry again later'
            logging.error(info_message)
            return False
    else:
        info_message = f'{key} does not exist. Nothing to delete'
        logging.info(info_message)
        return False
    
def lookup_key(key):
    """Look up if a key exists"""
    
    caching_srvc_crud_url = os.environ['caching_srvc_crud_url']
    
    data_payload = {"command": "READ", "key": key}
    json_resp = cache_api(caching_srvc_crud_url, payload=data_payload)
    if json_resp['status'] == 'SUCCESS':
        return True
    else:
        return False

def get_set_contents(set_name):
    """Get contents of a redis set as a list"""
    
    # this is now left for backwards compatibility
    old_byte_list = configure_redis_client().smembers(set_name)
    old_string_list = [z.decode('utf-8') for z in old_byte_list] # bytes to string
    
    # now use keys instead of sets
    byte_list = list(configure_redis_client().scan_iter(set_name + '*'))
    string_list = [y.decode('utf-8') for y in byte_list] # bytes to string
    
    # update list with just the ids 
    for index, value in enumerate(string_list):
        if set_name in value:
            string_list[index] = value.replace(set_name + '_', '')
    
    # merge old redis set and new keys list
    content_list = old_string_list + string_list
    
    return content_list