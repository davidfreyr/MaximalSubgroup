import numpy as np
from collections import Counter
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup
from sympy.combinatorics.perm_groups import PermutationGroup

def conv_to_mat(poset_line):
    # Split the line and convert to integers
    parts = list(map(int, poset_line.strip().split()))
    n = parts[0]  # Number of points
    relations = [(part // 10, part % 10) for part in parts[2:]]  # Extracting relations

    # Initialize the adjacency matrix with zeros and set diagonal to 1
    adj_matrix = np.eye(n, dtype=int)

    # Fill in the matrix for direct relations (b <= a)
    for b, a in relations:
        adj_matrix[a][b] = 1

    # Compute the transitive closure
    for k in range(n):
        for i in range(n):
            for j in range(n):
                adj_matrix[i][j] = adj_matrix[i][j] or (adj_matrix[i][k] and adj_matrix[k][j])

    return adj_matrix


def string_to_matrix(matrix_string):
    """
    Convert a matrix in string format back to a list of lists (2D list), more robustly.
    """
    # Split by lines and filter out empty lines or lines that only contain brackets
    rows = [row.strip() for row in matrix_string.strip().split("\n") if row.strip().strip('[],')]
    # Convert each row string back to a list of integers
    matrix = []
    for row in rows:
        # Clean row string and split into numbers, ensuring to remove any trailing characters like ']' that could cause parsing errors
        clean_row = row.strip('[],')
        numbers = clean_row.split(", ")
        matrix_row = [int(num) for num in numbers]
        matrix.append(matrix_row)
    return matrix


def elementList(myArr):
    elementsList = []
    start = 0
    for x in range(len(myArr)):
        elementsList += [start]
        start += 1
    return elementsList


def permutationGroup(myArr):
    generators = SymmetricGroup(len(myArr))
    permutations = list(generators.generate_schreier_sims(af=True))
    return permutations


def automorphisms(myArr):  
    posetArr = np.array(myArr)
    possibleMaps = permutationGroup(myArr)
    autCount = 0
    elements = elementList(myArr)
    auts = []

    for permutation in possibleMaps:
        possiblePoset = np.array(myArr)
        # swap cols
        possiblePoset[:] = possiblePoset[:, permutation]
        # swap rows
        possiblePoset[elements] = possiblePoset[permutation]

        if (possiblePoset == posetArr).all():
            autCount += 1
            auts.append(permutation)
            #print(permutation)

    return auts



n = 7
"""
Don't actually need to run this again since I've already computed it

# Read all posets from the document
with open(f'Raw/hasse{n}.txt', 'r') as file:
    posets_raw = file.readlines()

# Process each poset from the document with the correct handling
matrices_final = [conv_to_mat(line) for line in posets_raw]

# Prepare the text representation of all matrices, separated by semicolons
matrices_text_final_semicolon = ";\n".join(
    ["[" + ",\n".join(["[" + ", ".join(map(str, row)) + "]" for row in matrix]) + "]" for matrix in matrices_final]
)

# Save the final corrected matrices to a file with semicolons
output_path_final_semicolon = f'Processed/mat{n}.txt'
with open(output_path_final_semicolon, 'w') as file:
    file.write(matrices_text_final_semicolon)
"""


# Read the file content
with open(f'Processed/mat{n}.txt', 'r') as file:
    file_content = file.read()

# Split the content into individual strings
matrix_strings = file_content.split(";\n")

# Initialize a list to hold the matrices as lists of lists
matrices = []

# Convert each matrix string to a list of lists
for matrix_string in matrix_strings:
    matrix = string_to_matrix(matrix_string)
    matrices.append(matrix)

groups = []
c_found = False

# Processing
for matrix in matrices:
    G = automorphisms(matrix)
    for i in range(len(G)):
        G[i] = Permutation(G[i])

    if len(G) == 8:
        groups.append(G)
        group = PermutationGroup(G)
        print(f"Group of order 8: {matrix}")