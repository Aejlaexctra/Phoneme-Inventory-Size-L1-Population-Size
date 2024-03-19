import numpy as np
import csv
import os
import pandas as pd

# File paths, switch directories between Phoible, AA, ER, JIPA, lapsyd, RA, saphon, upsid, EA
def get_data(DATABASE):
    DATA_DIR = ''
    PHOIBLE_DATA_PATH = os.path.join(DATA_DIR, 'Data/cldf-datasets-inventory-study-d09fbf9/' + DATABASE + '-data.tsv')
    PHOIBLE_LANGUAGES_PATH = os.path.join(DATA_DIR, 'Data/cldf-datasets-inventory-study-d09fbf9/phoible/cldf/languages.csv')
    GLOBAL_PREDICTORS_PATH = os.path.join(DATA_DIR, 'Data/Global predictors of language endangerment and the future of linguistic diversity Data.xlsx')
    GLOTTOCODE_MACROAREA_PATH = os.path.join(DATA_DIR, 'Data/languages_and_dialects_geo.csv')
    FAMILY_LANGUAGES_PATH = os.path.join(DATA_DIR, 'Code/Output/Family_Data.csv')
    OUTPUT_CSV_PATH = os.path.join(DATA_DIR, 'Code/Output/' + DATABASE + '-data_UPDATED.csv')

    # Load the CSV file once and reuse the connection
    df = pd.read_csv(PHOIBLE_LANGUAGES_PATH)
    # Create a dictionary for quick lookups
    glottocode_to_iso_dict = dict(zip(df['Glottocode'], df['ISO639P3code']))
    df = pd.read_csv(FAMILY_LANGUAGES_PATH)
    # Create a dictionary for quick lookups
    glottocode_to_family_dict = dict(zip(df['Glottocode'], df['Family']))
    # Load the Excel file once and reuse the connection
    df = pd.read_excel(GLOBAL_PREDICTORS_PATH, sheet_name='Supplementary data 1')
    # Create a dictionary for quick lookups
    iso_to_population_dict = dict(zip(df['ISO'], df['L1_pop']))
    # Load the Excel file once and reuse the connection
    df = pd.read_csv(GLOTTOCODE_MACROAREA_PATH)
    # Create a dictionary for quick lookups
    glottocode_to_macroarea_dict = dict(zip(df['glottocode'], df['macroarea']))

    # Function to get column values for csv and tsv, defaults to tsv but can switch to csv (change in delimiter /t)
    def get_sv_column_values(file_path, column_name, is_tsv = True):
        
        with open(file_path, 'r', newline='', encoding='utf-8') as file:
            if is_tsv:
                reader = csv.DictReader(file, delimiter='\t')
            else:
                reader = csv.DictReader(file)

            # Check if the specified column exists in the TSV file
            if column_name not in reader.fieldnames:
                print(f"Column '{column_name}' not found in the TSV file.")
                return []

            # Extract the values from the specified column
            column_values = [row[column_name] for row in reader]

        return column_values

    def get_xlsx_column_values(file_path, sheet_name, column_name):
        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file_path, sheet_name=sheet_name)

            # Check if the specified column exists in the DataFrame
            if column_name not in df.columns:
                print(f"Column '{column_name}' not found in the Excel file.")
            else:
                # Extract the values from the specified column
                return df[column_name].tolist()

        except FileNotFoundError:
            print(f"Excel file not found at '{file_path}'.")
        except pd.errors.EmptyDataError:
            print(f"The specified sheet '{sheet_name}' is empty.")
        except Exception as e:
            print(f"An error occurred: {e}")

    # Get indexes of value in array
    def get_indexes(array, value_to_find):
        return [index for index, value in enumerate(array) if value == value_to_find]

    # Merge repeated languages together with average value
    def merge_rows(ordered_set, index_column, value_column):
        adjusted_column = np.zeros([len(ordered_set)])
        for i in range(len(ordered_set)):
            # Value to find
            value_to_find = ordered_set[i]
            # Using list comprehension to get indexes
            indexes = get_indexes(index_column,value_to_find)
            # Get sum of value:
            value_sum = 0
            for index in indexes:
                if value_column[index]:
                    value_sum += float(value_column[index])
            # Average value
            value_average = value_sum / len(indexes)
            # Insert average
            adjusted_column[i] = value_average
        return adjusted_column

    # Searches through KINBANK_Languages path and gets corresponding family to given glottocode
    def glottocode_to_family(glottocode):
        return glottocode_to_family_dict.get(glottocode, None)

    # Searches through phoible_languages_path and gets a corresponding iso to a given glottocode
    def glottocode_to_iso(glottocode):
        return glottocode_to_iso_dict.get(glottocode, None)

    # Searches through global_predictors_path and gets a corresponding L1_pop_size to a given iso
    def iso_to_L1population_size(iso):
        return iso_to_population_dict.get(iso, None)

    # Searches through glottocode_macroarea_path and gets a corresponding macroarea to a given glottocode
    def glottocode_to_macroarea(glottocode):
        return glottocode_to_macroarea_dict.get(glottocode, None)
    
    # Get Glottocode column values from Phoible_data
    glottocode_column_phoible_data = get_sv_column_values(PHOIBLE_DATA_PATH, 'Glottocode')
    # print(f"Glottocode column values: {glottocode_column}")

    # Get Latitude column values
    latitude_column = get_sv_column_values(PHOIBLE_DATA_PATH, 'Latitude')

    # Get Longitude column values
    longitude_column = get_sv_column_values(PHOIBLE_DATA_PATH, 'Longitude')

    # Get Sounds column values
    sounds_column = get_sv_column_values(PHOIBLE_DATA_PATH, 'Sounds')
    # print(f"Sounds column values: {sounds_column}")

    # Get Consonants column values
    consonants_column = get_sv_column_values(PHOIBLE_DATA_PATH, 'Consonants')

    # Get Vowels column values
    vowels_column = get_sv_column_values(PHOIBLE_DATA_PATH, 'Vowels')

    # Get ordered set, prevent duplicate entries
    glottocode_set_dict = dict.fromkeys(glottocode_column_phoible_data)
    glottocode_ordered_set = list(glottocode_set_dict.keys())

    # Adjust rows to account for duplicates, average for latitude and longitude, see if wrong to do this too.
    adjusted_latitude_count = merge_rows(glottocode_ordered_set,glottocode_column_phoible_data,latitude_column)
    adjusted_longitude_count = merge_rows(glottocode_ordered_set,glottocode_column_phoible_data,longitude_column)
    adjusted_sounds_count = merge_rows(glottocode_ordered_set,glottocode_column_phoible_data,sounds_column)
    adjusted_consonants_count = merge_rows(glottocode_ordered_set,glottocode_column_phoible_data,consonants_column)
    adjusted_vowels_count = merge_rows(glottocode_ordered_set,glottocode_column_phoible_data,vowels_column)

    # get ISO column
    iso_column = np.zeros_like(glottocode_ordered_set)
    for i in range(len(glottocode_ordered_set)):
        iso_column[i] = glottocode_to_iso(glottocode_ordered_set[i])
        print("Step 1: " + str(i) +"/" + str(len(glottocode_ordered_set)) + " glottocode to ISO converted", end='\r')
            
    # get L1_pop size
    L1_pop_column = np.zeros_like(iso_column)
    for i in range(len(iso_column)):
        L1_pop_column[i] = iso_to_L1population_size(iso_column[i])
        print("Step 2: " + str(i) +"/" + str(len(glottocode_ordered_set)) + " ISO to L1_pop size converted", end='\r')

    # Get families
    family_column = np.zeros_like(iso_column)
    for i in range(len(iso_column)):
        family_column[i] = glottocode_to_family(glottocode_ordered_set[i])
        print("Step 3: " + str(i) +"/" + str(len(glottocode_ordered_set)) + " glottocode to families converted", end='\r')
        
    # Get families
    macroarea_column = np.zeros_like(iso_column)
    for i in range(len(iso_column)):
        macroarea_column[i] = glottocode_to_macroarea(glottocode_ordered_set[i])
        print("Step 4: " + str(i) +"/" + str(len(glottocode_ordered_set)) + " glottocode to macroarea converted", end='\r')

    # Zip the arrays together to create rows
    rows = zip(glottocode_ordered_set, iso_column, macroarea_column, family_column, L1_pop_column, adjusted_latitude_count, adjusted_longitude_count, adjusted_sounds_count, adjusted_consonants_count, adjusted_vowels_count)

    # Write the rows to the new CSV file
    with open(OUTPUT_CSV_PATH, 'w', newline='', encoding='utf-8') as new_file:
        writer = csv.writer(new_file)
        
        # Write header
        writer.writerow(['Glottocode', 'ISO639P3', 'Macroarea', 'Family', 'L1_pop', 'Latitude', 'Longitude','Sounds','Consonants','Vowels'])
        
        # Write rows
        writer.writerows(rows)

    print(f"New CSV file created at {OUTPUT_CSV_PATH}")

databases = ["PHOIBLE", "UPSID", "LAPSYD", "JIPA", "AA", "ER", "RA", "SAPHON", "EA"]

# Update all databases
for data in databases:
    get_data(data)