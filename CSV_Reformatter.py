import pandas as pd
import sys
import re
import os


# Parse the initial arguments, make sure they're valid, return the input file path
def parse_args() -> str:
    if len(sys.argv) != 2:
        print(f'Inputs: {sys.argv[0]} | {sys.argv[1]}')
        sys.stderr.write(f'This script takes one parameter: path/to/csv | You currently have: {len(sys.argv)}')
        sys.stderr.write("Example: python3 ReadCSV.py path/to/csv")
        sys.exit(1)

    file_path = sys.argv[1]
    return file_path


# Check that the index requested by the user is greater than 0 and less than the highest column index
def check_bad_edges(user_data: list, columns_len: int) -> bool:
    for num in user_data:
        if int(num) < 0 or int(num) > columns_len:
            print(f"You entered an invalid number: {num} | Largest possible index: {columns_len}")
            exit()
        else:
            return True


def check_characters(value_list: list) -> bool:
    for s in value_list:
        for c in s:
            if c.isdigit() or c == ',' or c == '-':
                continue
            else:
                print(f"Invalid character {c}, expecting: positive integers, comma, or hyphen.")
                exit()
    return True


# Show the user all the column indexes and names, ask them which they want
# Take the list, strip all whitespace, split on comma, remove all empty strings
# Check for bad edge cases
def column_menu(column_len: int) -> list:
    print("Printing a list of column index and names")
    print("Create a list of indexes (ex: 1-5,7,12-15) and this script will output only data for those columns")
    print(*tuple_list, sep='\n')

    column_string = input("Enter the column index you'd like to grab\n")
    clean_col_list = [x for x in column_string.replace(" ", "").split(',') if x]
    character_list = re.split(",|-", ",".join(clean_col_list))
    if check_characters(character_list):
        if check_bad_edges(character_list, column_len):
            return clean_col_list


# Take list of user input, parse ranges and individual indexes, append to list, return list
def parse_user_list(user_indexes: list) -> list:
    output_list = []

    for x in user_indexes:
        if '-' in x:
            s = x.split("-")
            if int(s[-1]) == int(s[0]):
                continue
            if int(s[-1]) > int(s[0]):
                for n in range(int(s[0]), int(s[-1]) + 1):
                    output_list.append(n)
            else:
                for n in reversed(range(int(s[-1]), int(s[0]) + 1)):
                    output_list.append(n)
        else:
            output_list.append(int(x))

    return output_list


# Convert the input CSV file to a Pandas dataframe
def csv_to_dataframe(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    return pd.DataFrame(data)


# From the dataframe return a list of the columns
def grab_columns(dataframe: pd.DataFrame) -> list:
    return dataframe.columns.values.tolist()


# Take in user's requested indexes, grab those from the dataframe, write the dataframe to a CSV at the input file destination with _dataframe.csv postfix
def list_to_dataframe(in_list: list, dataf: pd.DataFrame, path: str):
    try:
        dataf = dataf[dataf.columns[in_list]]
    except IndexError as e:
        print(f"Invalid index: {e}")
        exit()

    dataf.to_csv(f"{path}_dataframe.csv", sep='\t', index=False)
    if os.path.exists(f"{path}_dataframe.csv"):
        print(f"Created file: {path}_dataframe.csv")
    else:
        print(f"Could not create file: {path}_dataframe.csv")


# Main
if __name__ == '__main__':
    input_path = parse_args()
    df = csv_to_dataframe(input_path)
    columns = grab_columns(df)
    tuple_list = tuple(((columns.index(x), x) for x in columns))
    user_indices = column_menu(len(columns) - 1)
    out_list = parse_user_list(user_indices)
    list_to_dataframe(out_list, df, input_path)
