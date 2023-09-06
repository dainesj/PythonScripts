import argparse
import json


def initialize_parser():
    parser = argparse.ArgumentParser(description="JSON Schema Type Checker")
    parser.add_argument('-f', dest="filepath", help="Path to JSON schema file")
    return parser.parse_args()


def populate_json_line_numbers(file_path: str) -> dict:
    json_file_line_numbers = {}
    with open(file_path) as f:
        for line_number, line in enumerate(f.readlines()):
            json_file_line_numbers[line] = line_number
        f.close()
    return json_file_line_numbers


def load_json_schema(file_path: str) -> dict:
    with open(file_path) as f:
        schema = json.loads(f.read())
        return schema


def key_check(d: dict, o_list: list) -> list:
    for k, v in d.items():
        if isinstance(v, dict):
            key_check(v, o_list)
            if "type" not in (d[k].keys()) and "$ref" not in v.keys() and k not in exclusion_list and len(v) != 0 and any(d[k].values()) is True:
                o_list.append(k)
        else:
            pass
    return o_list


if __name__ == '__main__':
    exclusion_list = ["properties", "definitions"]
    bad_props = []

    parsed_args = initialize_parser()
    json_line_numbers = populate_json_line_numbers(parsed_args.filepath)
    input_schema = load_json_schema(parsed_args.filepath)
    bad_values = key_check(input_schema, bad_props)

    for line, line_num in json_line_numbers.items():
        for bad in bad_values:
            if bad in line and ":" in line:
                print(f"Property missing type: {bad} | Line Number: {line_num + 1}")
