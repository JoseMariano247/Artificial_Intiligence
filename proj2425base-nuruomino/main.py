# Main file to implement the main functionality of the program.
# In this file, the input is read, the model is trained, and the results are saved.
# The code is structured to allow for easy modification and extension in the future.   

# Import necessary files and libraries

import nuruomino

print("Exemplo 1: \n")

board = nuruomino.Board.parse_instance()

#print(board.aux_list_coords(1, 1))

problem = nuruomino.Nuruomino(board)

#problem.actions()

print(board.reg_to_values)

print("\n \nExemplo 2: \n")