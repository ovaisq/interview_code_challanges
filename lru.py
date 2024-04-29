#!/usr/bin/env python3
"""In this implementation, we use an OrderedDict to maintain the order of keys according to their usage.
The get method retrieves the value associated with a key while promoting it to the end, and the put
method adds or updates a key-value pair while managing the cache size and evicting the least recently
used item if necessary.
"""
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key in self.cache:
            # Move the accessed item to the end to indicate it's the most recently used
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return None

    def put(self, key, value):
        if key in self.cache:
            # Update the value and move the key to the end
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # Remove the least recently used item (the first item)
            self.cache.popitem(last=False)

        self.cache[key] = value

    def __str__(self):
        return str(self.cache)

# Example usage
cache = LRUCache(3)

cache.put(1, 'one')
cache.put(2, 'two')
cache.put(3, 'three')

print(cache)  # Output: OrderedDict([(1, 'one'), (2, 'two'), (3, 'three')])

cache.get(2)
print(cache)  # Output: OrderedDict([(1, 'one'), (3, 'three'), (2, 'two')])

cache.put(4, 'four')  # This will remove the least recently used item 'one'
print(cache)  # Output: OrderedDict([(3, 'three'), (2, 'two'), (4, 'four')])

