import numpy as np
import csv
from collections import Counter

tsv_file_path = ''
csv_file_path = ''
column_name = 'Glottocode'

with open(csv_file_path, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # Check if the specified column exists in the TSV file
    if column_name not in reader.fieldnames:
        print(f"Column '{column_name}' not found in the TSV file.")
    else:
        # Extract the values from the specified column
        glottocode_column = [row[column_name] for row in reader]

        # Print or use the values in the column
        # print(f"{column_name} column values: {glottocode_column}")


# Use Counter to get frequencies
value_frequencies = Counter(glottocode_column)

# Print the frequencies
for value, frequency in value_frequencies.items():
    #if frequency != 1:
    print(f"{value}: {frequency} times")