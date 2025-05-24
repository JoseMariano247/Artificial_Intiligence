# Main file to implement the main functionality of the program.
# In this file, the input is read, the model is trained, and the results are saved.
# The code is structured to allow for easy modification and extension in the future.   

# Import necessary files and libraries

import nuruomino

print("Exemplo 1: \n")

board = nuruomino.Board.parse_instance()
problem = nuruomino.Nuruomino(board)
print(problem.actions())
#print(board.adjacent_regions_to_square(2,1))
#print(board.adjacent_regions_to_square(1,2))
#print(board.reg_to_coords)

print("\n \nExemplo 2: \n")