import pandas as pd
import sys


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print(f'Inputs: {sys.argv[0]} | {sys.argv[1]}')
        sys.stderr.write(f'This script takes one parameter: path/to/csv | You currently have: {len(sys.argv)}')
        sys.stderr.write("Example: python3 CSV_Reformatter.py path/to/csv")
        sys.exit(1)

    input_path = sys.argv[1]

    # Loads the CSV into a dataframe, correlates the column index with the column name for easier identification
    # Ask the user which indexes they want. The script expects: #,#,#,#,# as input. No edge checking, cba
    # Takes the user's input list, gets only those columns from the dataframe and returns: filename_dataframe.csv
    def grab_columns(path: str):
        data = pd.read_csv(path)
        df = pd.DataFrame(data)
        columns = df.columns.values.tolist()
        tuple_list = tuple(((columns.index(x), x) for x in columns))
        print("Printing a list of column index and names")
        print("Create a list of indexes (ex: 1,2,3,4,5) and this script will output only data for those columns")
        for x in tuple_list:
            print(x)
        column_list = input("Enter the column index you'd like to grab\n")
        index_list = [int(x) for x in column_list.split(',')]
        print(f"Your column list: {index_list}")
        df = df[df.columns[index_list]]
        df.to_csv(f"{path}_dataframe.csv", sep='\t')

    grab_columns(input_path)
