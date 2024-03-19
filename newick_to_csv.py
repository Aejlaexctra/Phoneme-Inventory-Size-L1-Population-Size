import numpy as np
import csv
import os
from Bio import Phylo
import pandas as pd

# File paths
DATA_DIR = ''
GLOTTOCODE_TREE_PATH = os.path.join(DATA_DIR, 'Data/tree_glottolog_newick.txt')
OUTPUT_CSV_PATH = os.path.join(DATA_DIR, 'Code/Output/Family_Data.csv')

def extract_between_chars(input_string, char1, char2):
    start_index = input_string.find(char1) + 1
    end_index = input_string.find(char2, start_index)
    
    if start_index != -1 and end_index != -1:
        result = input_string[start_index:end_index]
        return result
    else:
        return None

phylogeny = {} # Dictionary, Key == Family, Value = Children

# Open the Newick file containing multiple trees
with open(GLOTTOCODE_TREE_PATH) as file:
    # Parse the file
    trees = Phylo.parse(file, 'newick')

    # Iterate over each tree and get the root node, as well as leaves
    for tree in trees:
        root = extract_between_chars(str(tree.clade),'[',']') 
                
        # # Get all terminal nodes (leaves)
        # raw_leaves = tree.get_terminals()
        
        # # Apply function to every element in the list using list comprehension
        # result_leaves = [extract_between_chars(str(leaf),'[',']') for leaf in raw_leaves]
        
        # # Add children and root to phylogeny
        # phylogeny[root] = result_leaves

        
        # Get all nodes except root
        all_nodes = tree.find_elements(target=lambda x: x != tree.root)
        result_nodes = [extract_between_chars(str(leaf),'[',']') for leaf in all_nodes]
        
        # Add children and root to phylogeny
        phylogeny[root] = result_nodes

# Calculate the total number of entries
entries = sum(len(value) for value in phylogeny.values())

# Initiliase columns
language_column = np.empty(shape = entries, dtype='<U10')
family_column = np.empty(shape = entries, dtype='<U10')

# progress counter
progress_counter = 0

# Transcribe phylogeny into arrays
for key, value in phylogeny.items():
    length = len(value)
    language_column[progress_counter : progress_counter + length] = value
    family_column[progress_counter : progress_counter + length] = key
    progress_counter += length

# Zip the arrays together to create rows
rows = zip(language_column, family_column)

# Write the rows to the new CSV file
with open(OUTPUT_CSV_PATH, 'w', newline='', encoding='utf-8') as new_file:
    writer = csv.writer(new_file)
    
    # Write header
    writer.writerow(['Glottocode', 'Family'])
    
    # Write rows
    writer.writerows(rows)

print(f"New CSV file created at {OUTPUT_CSV_PATH}")
