
# JSON Key Replacer

A Python tool to update the value of a specified key within a JSON document.
This script recursively searches through nested dictionaries and lists, displays
all occurrences of the target key with their access paths, and allows you to
interactively choose which occurrence to modify.

## Features

- **Recursive Traversal:** Searches through both dictionaries and lists in your JSON.
- **Interactive Selection:** Lists each found instance of the target key along with its path.
- **Easy Integration:** Importable as a module for use in other projects.
- **Robust Error Handling:** Validates the input JSON and handles invalid entries gracefully.

## Usage

1. **Run Directly**

   Open your terminal and run:
 
       $ ./replace_json_key_values.py
       Original JSON:
       {"a":1,"b":{"a":2,"c":[{"a":3},{"d":{"a":4}}]}}
       Found the following instances of key 'a':
       1. a
       2. b>a
       3. b>c>[0]>a
       4. b>c>[1]>d>a
       Enter the number of the key to replace (or 0 to cancel): 2

       Modified JSON (after user selection):
       {"a": 1, "b": {"a": {"a": 99, "b": {"z": 200}}, "c": [{"a": 3}, {"d": {"a": 4}}]}}

2. **Interactive Prompt**

   The script will display all occurrences of the target key (in this example, "a") along with a numbered list.
   Enter the number corresponding to the occurrence you wish to update or enter `0` to cancel.

3. **Output**

   The script prints both the original and modified JSON documents.

## Installation

No external libraries are required beyond Python’s standard library. Simply ensure that you have Python 3 installed,
then run the script as shown above.

## Author
©2025, Ovais Quraishi
