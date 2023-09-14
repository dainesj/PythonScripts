import argparse
import json


# Initializes an argument parser to grab the file path of the JSON schema file from the command line.
def initialize_parser():
    parser = argparse.ArgumentParser(description="JSON Schema Type Checker")
    parser.add_argument('-f', dest="filepath", help="Path to JSON schema file")
    return parser.parse_args()


# Iterate through the schema line-by-line
# Create and return a dictionary where the key is the line itself and the value is the line number
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
    if "type" not in (d[k].keys()) and "$ref" not in v.keys() and k not in exclusion_list and len(v) != 0 and any(
            d[k].values()) is True:
        return True


# Check that the oneOf statement has a type value, if so return true.
def one_of(d):
    for x in d:
        if list(x.keys()) and list(x.keys())[0] == "type" and x.values():
            return True
        else:
            return False


# Check objects which have an internal properties field, data structure here is tuple hence x[1] to go get value, x[0] would get key
def property_check(d):
    bad_list = []
    for x in d.items():
        if bool(x[1]) is False or list(x[1].keys())[0] == "$ref" or x[1] == "$ref":
            pass
        elif x[1] or list(x[1].keys())[0] == "type":
            pass
        else:
            print(f"First: {x[1]}\nSecond:{list(x[1].keys())[0]}\n")
            bad_list.append(x[0])

    if bad_list:
        return bad_list
    else:
        return True


# Recursively iterate through the dictionary, check keys for validity
def key_check(d: dict, o_list: list) -> list:
    for key, val in d.items():
        if isinstance(val, dict):
            key_check(val, o_list)
            if "oneOf" in val.keys():
                if one_of(val['oneOf']) is True:
                    key_check(val, o_list)
                else:
                    o_list.append(key)
            elif "properties" in val.keys():
                if property_check(val['properties']) is True:
                    key_check(val, o_list)
                else:
                    o_list += property_check(val['properties'])

            elif check_validity(d, key, val) is True:
                o_list.append(key)
        else:
            pass
    return o_list


# Iterate through our line numbers to see which line the bad properties are at
# Print them to the console
# This could get expensive if there's a lot of bad values(O = n^2), going to ignore that
def line_number_lookup(list_to_find: list, line_dict: dict):
    for line, line_num in line_dict.items():
        for bad in list_to_find:
            if bad in line and f'"{bad}"' == line.strip().split(':')[0]:
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
