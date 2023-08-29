import pandas as pd
import sys
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


# Show the user all the column indexes and names, ask them which they want
# Take the list, strip all whitespace, split on comma
# Check for bad edge cases
def column_menu(tup_list: tuple, column_length: int) -> list:
    print("Printing a list of column index and names")
    print("Create a list of indexes (ex: 1-5,7,12-15) and this script will output only data for those columns")
    print(*tuple_list, sep='\n')

    column_list = input("Enter the column index you'd like to grab\n")
    return [x for x in column_list.replace(" ", "").split(',')]


# Take list of user input, parse ranges and individual indexes, append to list, return list
def parse_user_list(user_indexes: list) -> list:
    output_list = []
    try:
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
    except ValueError as e:
        print(f"This script expects positive integers, commas, or hyphens.\n {e}")
        exit()

    return output_list


# Convert the input CSV file to a Pandas dataframe
def csv_to_dataframe(path: str) -> pd.DataFrame:
    data = pd.read_csv(path)
    dataframe = pd.DataFrame(data)
    return dataframe


# From the dataframe return a list of the columns
def grab_columns(dataframe: pd.DataFrame) -> list:
    column_list = dataframe.columns.values.tolist()
    return column_list


# Take in user's requested indexes, grab those from the dataframe, write the dataframe to a CSV at present working directory with _dataframe.csv postfix
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
    user_indices = column_menu(tuple_list, len(columns) - 1)
    out_list = parse_user_list(user_indices)
    list_to_dataframe(out_list, df, input_path)
