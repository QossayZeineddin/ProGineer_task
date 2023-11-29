import csv
import os.path
from collections import defaultdict
import re

# Constants
CHUNK_SIZE = 300
DELIMITER = ';'


def get_valid_file_name():
    while True:
        input_file = input("Please enter the name of the file (without .csv): ")
        input_file = f"{input_file}.csv"

        if not os.path.exists(input_file):
            print("File Not Found! Please enter a valid file name.")
        else:
            return input_file


def parse_header(lines):
    header_start_line = None
    header_end_line = None
    data_start_line = None
    for i, line in enumerate(lines):
        if re.match(r"<HEADER>", line.strip()):
            header_start_line = i
        elif re.match(r"</HEADER>", line.strip()):
            header_end_line = i
        elif re.match(r"<BOD>", line.strip()):
            data_start_line = i
            break

    if header_start_line is None or header_end_line is None:
        raise ValueError("Header not found in the CSV file.")

    header_section = lines[header_start_line + 1: header_end_line]
    return header_section, data_start_line if header_end_line > header_start_line and data_start_line > header_end_line else None





def write_files_to_outfolder(data_dict, column_names):
    # Write the data from a dictionary to its correct file each file 300 row
    for key, rows in data_dict.items():
        output_file_number = 1
        for i in range(0, len(rows), CHUNK_SIZE):
            output_file_path = os.path.join(output_folder, f"datafile_{key}_part{output_file_number}.csv")
            with open(output_file_path, 'w', newline='') as outfile:
                writer = csv.writer(outfile, delimiter=DELIMITER)
                writer.writerow(column_names)
                writer.writerows(rows[i:i + CHUNK_SIZE])
            output_file_number += 1


def split_and_write_by_column(input_file, column_number, output_folder):
    with open(input_file, 'r', newline='') as infile:
        lines = infile.readlines()

    # Get header info
    header_section, DATA_START_LINE = parse_header(lines)
    # Number of columns
    number_of_columns = int(header_section[1].split('=')[1].strip())
    # Names of columns
    column_names = [name.strip() for name in header_section[2].split('=')[1].strip('[]').split(',')]

    # Check if the input number to split the columns is out of index
    if 1 <= column_number <= len(column_names):
        column_name = column_names[column_number - 1]
    else:
        raise IndexError(
            f"Error: Column number {column_number} is out of range. Available columns: {len(column_names)}")

    data_dict = defaultdict(list)

    for line in lines[DATA_START_LINE:]:
        # Remove the empty line
        if line.strip():
            row = [value if value and value != ' ' else "NA" for value in line.strip().split(DELIMITER)]

            # Check if the row length is correct
            if len(row) == number_of_columns:
                key = row[column_number - 1]

                # Remove duplicate lines
                if row not in data_dict[key]:
                    data_dict[key].append(row)
    write_files_to_outfolder(data_dict, column_names)
    print("Done")


if __name__ == "__main__":
    # Get a valid file name
    input_file = get_valid_file_name()

    # Handle the exception if the casting fails
    try:
        column_number = int(input("Please enter the number of columns: "))
    except ValueError as e:
        exit(f" Could not convert the string to an integer.\nThe Error is: {e}")

    # Specify the output folder name
    output_folder = "out_files"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    split_and_write_by_column(input_file, column_number, output_folder)
