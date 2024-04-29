#!/usr/bin/env python3
""" Iterates over a list of integers and combines them into
    pairs whose sum matches a given target value. Assumes multiple
    pairs whose sum matches the target.
"""

def get_pairs(nums, target):
    """ Find pairs of number that when added matches a given sum value
    """

    
    num_set = set()
    result = []
    for i in range(len(nums)):
        complement = target - nums[i]
        if complement in num_set:
            result.append((complement, nums[i]))
        num_set.add(nums[i])
    return result


nums = [1, 2, 3, 5, 6, 8, 9, 11, 19, 27, 28, 29, 34]
target = 11

result = get_pairs(nums, target)
print(result) 
