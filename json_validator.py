import argparse
import json


# Grab file path from CLI
def initialize_parser():
    parser = argparse.ArgumentParser(description="JSON Schema Type Checker")
    parser.add_argument('-f', dest="filepath", help="Path to JSON schema file")
    return parser.parse_args()


# Iterate through the schema line-by-line
# Create and return a dictionary where the key is the line itself and the value is the line number
#     I did it this way to possibly get a constant time lookup on lines but didn't find a way
#     to get the line itself while iterating, maybe in the future.
def populate_json_line_numbers(file_path: str) -> dict:
    json_file_line_numbers = {}
    with open(file_path) as f:
        for line_number, line in enumerate(f.readlines()):
            json_file_line_numbers[line] = line_number
        f.close()
    return json_file_line_numbers


# Grab the filepath, read the schema, return a dictionary representation
def load_json_schema(file_path: str) -> dict:
    with open(file_path) as f:
        schema = json.loads(f.read())
        return schema


# if "type" not in (d[k].keys())
#     Our primary check, we want to see if there's properties missing the type field
# "$ref" not in v.keys()
#     We don't want to flag on $ref tags, we check them through the recursive nature anyway
# k not in exclusion_list
#     We don't want to flag on "properties" or "definitions", they don't need types
# len(v) != 0 and any(d[k].values()) is True
#     Edge case where an empty dictionary value would flag. Unsure of the validity of an empty dict, handling it anyway
def check_validity(d, k, v):
    if "type" not in (d[k].keys()) and "$ref" not in v.keys() and k not in exclusion_list and len(v) != 0 and any(d[k].values()) is True:
        return True


# Check that the oneOf statement has a type value, if so return true.
def one_of(d):
    for x in d:
        if list(x.keys()) and list(x.keys())[0] == "type" and x.values() :
            return True
        else:
            return False


# Recursively iterate through the dictionary, check keys for validity
def key_check(d: dict, o_list: list) -> list:
    for k, v in d.items():
        if isinstance(v, dict):
            key_check(v, o_list)
            if "oneOf" in v.keys():
                if one_of(v['oneOf']) is True:
                    key_check(v, o_list)
                else:
                    o_list.append(k)
            elif check_validity(d, k, v) is True:
                o_list.append(k)
        else:
            pass
    return o_list


# Iterate through our line numbers to see which line the bad properties are at
# Print them to the console
# This could get expensive if there's a lot of bad values(O = n^2), going to ignore that
def line_number_lookup(list_to_find: list, line_dict: dict):
    for line, line_num in line_dict.items():
        for bad in list_to_find:
            if bad in line and ":" in line:
                print(f"Property missing type: {bad} | Line Number: {line_num + 1}")


# Main
if __name__ == '__main__':
    exclusion_list = ["properties", "definitions"]
    bad_props = []

    parsed_args = initialize_parser()
    json_line_numbers = populate_json_line_numbers(parsed_args.filepath)
    input_schema = load_json_schema(parsed_args.filepath)
    bad_values = key_check(input_schema, bad_props)
    line_number_lookup(bad_values, json_line_numbers)
