#!/usr/bin/env python3

def fizzbuzz(num_range):
	for i in range(1, num_range+1):
		if i % 3 == 0 and i % 5 == 0:
			print(f"{i}: FizzBuzz")
		elif i % 3 == 0:
			print(f"{i}: Fizz")
		elif i % 5 == 0:
			print(f"{i}: Buzz")
		else:
			print(f"{i}: No Match")


numrange = 100

fizzbuzz(numrange)
