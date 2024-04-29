#!/usr/bin/env python3

import requests
import cachetools

# Initialize a cache with a maximum size and a TTL (time-to-live) for cached items
cache = cachetools.LRUCache(maxsize=1000)  # Cache up to 1000 items for 1 hour

# Function to make an API request with caching
def api_request_with_cache(url):
    # Check if the response is already cached
    if url in cache:
        print("Using cached response for", url)
        return cache[url]

    # If not cached, make the API request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Cache the response for future use
        cache[url] = response
        return response
    else:
        print("API request failed with status code:", response.status_code)
        return None

# Example usage
if __name__ == "__main__":
    api_url = "https://api.example.com/data"

    # Make an API request with caching
    response = api_request_with_cache(api_url)

    if response:
        data = response.json()
        print("API response data:", data)
