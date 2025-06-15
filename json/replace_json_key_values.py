#!/usr/bin/env python3
""" Module: replace_json_key

	This module provides functionality to replace a specific key in a JSON
	document with a new value. It recursively searches through the JSON
	structure, both dictionaries and lists, to locate all occurrences of the
	target key, presents them to the user, and allows for an interactive
	selection of which occurrence to update.

	©2025, Ovais Quraishi
"""

import json
import os

def replace_json_key(json_doc, target_key, new_value):
    """Replace instances of 'target_key' in JSON after user selection.
		Shows numbered list of all matches and lets user choose which to replace.

		Args:
			json_doc: A valid JSON-formatted string
			target_key: The key whose value should be replaced
			new_value: The new value to set for the key (must be JSON-serializable)

		Returns:
			Modified JSON document as a string

		Raises:
			ValueError: If input is not valid JSON
    """

    try:
        data = json.loads(json_doc)
    except json.JSONDecodeError as e:
        raise ValueError("Input is not valid JSON") from e

    matched_keys = []

    def _collect_paths(data, current_path):
        if isinstance(data, dict):
            for key in list(data.keys()):
                new_path = current_path + [key]
                if key == target_key:
                    matched_keys.append(new_path)
                elif isinstance(data[key], (dict, list)):
                    _collect_paths(data[key], new_path)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                new_path = current_path + [idx]
                if isinstance(item, (dict, list)):
                    _collect_paths(item, new_path)

    _collect_paths(data, [])

    # if no matches found
    if not matched_keys:
        print(f"No instances of key '{target_key}' found in JSON.")
        return json_doc

    # show matched keys to user
    print("Found the following instances of key '{}':".format(target_key))
    for i, path in enumerate(matched_keys, 1):
        formatted_path = []
        for p in path:
            if isinstance(p, int):
                formatted_path.append(f"[{p}]")
            else:
                formatted_path.append(p)
        print("{}. {}".format(i, ">".join(str(segment) for segment in formatted_path)))

    # get user selection
    while True:
        try:
            selection = input("Enter the number of the key to replace (or 0 to cancel): ")
            if selection == '0':
                return json_doc  # Return original if user cancels
            selection_int = int(selection)
            if 1 <= selection_int <= len(matched_keys):
                break
            else:
                print(f"Please enter a number between 1 and {len(matched_keys)}.")
        except ValueError:
            print("Please enter a valid number.")

    # replace the selected key
    selected_path = matched_keys[selection_int - 1]
    current_data = data
    for step in selected_path[:-1]:
        if isinstance(current_data, dict):
            current_data = current_data[step]
        else:  # must be list for array indices
            current_data = current_data[step]

    # the last step is the target_key
    key_to_replace = selected_path[-1]
    current_data[key_to_replace] = new_value

    return json.dumps(data)

def main():

    import sys

    if len(sys.argv) != 3:
        print("Usage: ./replace_json_key_values.py <filename> <key_to_replace>")
        sys.exit(1)

    filename = sys.argv[1]
    key_to_replace = sys.argv[2]

    # check if file exists
    if not os.path.exists(filename):
        print(f"File '{filename}' does not exist.")
        sys.exit(1)

    try:
        with open(filename, 'r') as f:
            json_doc = f.read()
            data = json.loads(json_doc)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Failed to read or parse JSON from file '{filename}': {e}")
        sys.exit(1)

    new_value = input("Enter the new value for key '{}': ".format(key_to_replace))
    try:
        # try parsing it into valid JSON
        new_value_json = json.loads(new_value)
    except json.JSONDecodeError as e:
        print(f"Provided new value is not valid JSON: {e}")
        sys.exit(1)

    modified_json = replace_json_key(json_doc, key_to_replace, new_value_json)

    # save results to a new file with prefix "new_"
    output_filename = "new_" + filename
    try:
        with open(output_filename, 'w') as f:
            f.write(modified_json)
        print(f"Modified JSON saved to '{output_filename}'")
    except IOError as e:
        print(f"Failed to write modified JSON to file '{output_filename}': {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
