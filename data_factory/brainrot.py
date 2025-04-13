import csv
import os

def split_csv_file(input_file, output_prefix, lines_per_file=2000):
    """
    Splits a large CSV file into smaller files with a specified number of lines.

    Args:
        input_file (str): Path to the input CSV file.
        output_prefix (str): Prefix for the output files (e.g., "eng2mti").
        lines_per_file (int): Number of lines per smaller file (default is 2000).
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)  # Read the header row
            
            file_count = 1
            line_count = 0
            output_file = f"{output_prefix}-{file_count}.csv"
            out_csv = open(output_file, 'w', newline='', encoding='utf-8')
            csv_writer = csv.writer(out_csv)
            csv_writer.writerow(headers)  # Write the header to the first file

            for row in csv_reader:
                if line_count == lines_per_file:
                    # Close the current file and start a new one
                    out_csv.close()
                    file_count += 1
                    line_count = 0
                    output_file = f"{output_prefix}-{file_count}.csv"
                    out_csv = open(output_file, 'w', newline='', encoding='utf-8')
                    csv_writer = csv.writer(out_csv)
                    csv_writer.writerow(headers)  # Write header to the new file

                csv_writer.writerow(row)
                line_count += 1

            # Close the last file
            out_csv.close()
            print(f"CSV file split into {file_count} smaller files successfully!")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_file = "train-00000-of-00001.csv"  # Replace with the path to your large CSV file
output_prefix = "eng2mti"  # Prefix for output files
lines_per_file = 2000  # Number of lines per smaller file

split_csv_file(input_file, output_prefix, lines_per_file)