# Main file to implement the main functionality of the program.
# In this file, the input is read, the model is trained, and the results are saved.
# The code is structured to allow for easy modification and extension in the future.   

# Import necessary files and libraries

import nuruomino

print("Exemplo 1: \n")

board = nuruomino.Board.parse_instance()
print(board.adjacent_regions_to_regions(1))
print(board.adjacent_regions_to_regions(3))

print("\n \nExemplo 2: \n")