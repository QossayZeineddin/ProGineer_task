import csv
import os.path
import sys
from collections import defaultdict

# Constants
CHUNK_SIZE = 300
HEADER_LINES = slice(1, 4)
DATA_START_LINE = 5

def split_and_write_by_column(input_file, column_number, output_folder):
    # Read the file lines by lines and store them in a list
    with open(input_file, 'r', newline='') as infile:
        lines = infile.readlines()

    # Get header info
    header_section = lines[HEADER_LINES]
    # Number of columns
    number_of_columns = int(header_section[1].split('=')[1].strip())
    # Names of columns
    column_names = [name.strip() for name in header_section[2].split('=')[1].strip('[]').split(',')]

    # Handle if the input number to split the columns is out of index
    try:
        column_name = column_names[column_number - 1]
    except IndexError:
        print(f"Error: Column number {column_number} is out of range.")
        return

    data_dict = defaultdict(list)

    for line in lines[DATA_START_LINE:]:
        # Remove the empty line
        if line.strip():
            row = [value if value and value != ' ' else "NA" for value in line.strip().split(';')]

            # Check if the row length is correct
            if len(row) == number_of_columns:
                key = row[column_number - 1]

                # Remove duplicate lines
                if row not in data_dict[key]:
                    data_dict[key].append(row)

    # Write the data from a dictionary to its correct file each file 300 row
    for key, rows in data_dict.items():
        output_file_number = 1
        for i in range(0, len(rows), CHUNK_SIZE):
            output_file_path = os.path.join(output_folder, f"datafile_{key}_part{output_file_number}.csv")
            with open(output_file_path, 'w', newline='') as outfile:
                writer = csv.writer(outfile, delimiter=';')
                writer.writerow(column_names)
                writer.writerows(rows[i:i + CHUNK_SIZE])
            output_file_number += 1

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Error: Incorrect number of arguments. Usage: python script.py <input_file> <column_number>")
        sys.exit(1)

    input_file = sys.argv[1]

    # Handle the exception if the casting fails
    try:
        column_number = int(sys.argv[2])
    except ValueError:
        exit("Error: Could not convert the string to an integer.")

    # Specify the output folder name
    output_folder = "out_files"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    split_and_write_by_column(input_file, column_number, output_folder)
