import csv
import os.path
import sys
from collections import defaultdict



def split_by_column(input_file, output_prefix, column_number, output_folder):
    with open(input_file, 'r', newline='') as infile:
        lines = infile.readlines()

    header_section = lines[1:4]
    number_of_columns = int(header_section[1].split('=')[1].strip())
    column_names = [name.strip() for name in header_section[2].split('=')[1].strip('[]').split(',')]

    try:
        column_name = column_names[column_number - 1]
    except IndexError:
        print(f"Error: Column number {column_number} is out of range.")
        return

    data_dict = defaultdict(list)

    for line in lines[5:]:
        if not line.strip():
            continue

        row = line.strip().split(';')

        row = [value if value else "NA" for value in row]

        if len(row) == number_of_columns:
            key = row[column_number - 1]

            if row not in data_dict[key]:
                data_dict[key].append(row)


    for key, rows in data_dict.items():
        output_file = os.path.join(output_folder , f"{output_prefix}_{key}")

        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=';')

            writer.writerow(column_names)

            for i in range(0, len(rows), 300):
                writer.writerows(rows[i:i + 300])

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file> <output_prefix> <column_number>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_prefix = sys.argv[2]
    column_number = int(sys.argv[3])

    output_folder = "out_files"  # Specify the output folder name
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    split_by_column(input_file, output_prefix, column_number,output_folder )
