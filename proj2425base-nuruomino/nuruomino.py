# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

from sys import stdin
import numpy as np 
from search import Problem, Node

# Grupo 4:
# 102451 José Mariano
# 102994 Maria Maló


#fazer um dicionário que a cada região, dá a coordenada. Assim, é facil
#dar check nas acoes por regioes e poupa muito tempo computacional pq testa-se
#de cada vez se a ação é válida ou não.

class NuruominoState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NuruominoState.state_id
        NuruominoState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""

    def __init__(self, matrix):
        """Construtor da classe Board. Recebe uma matriz que representa o tabuleiro."""
        self.matrix = matrix
        self.rows, self.cols = matrix.shape
        aux_reg = np.unique(matrix)
        self.regions = aux_reg[type(aux_reg) == int]
        self.reg_to_coords = {}
        for i in range(self.rows):
            for j in range(self.cols):
                reg = self.matrix[i, j]
                if reg not in self.reg_to_coords:
                    self.reg_to_coords[reg] = []
                self.reg_to_coords[reg].append((i, j))
        self.reg_to_coords = dict(sorted(self.reg_to_coords.items()))

        self.coords_to_reg = {}
        for i in range(self.rows):
            for j in range(self.cols):
                reg = self.matrix[i, j]
                self.coords_to_reg[(i, j)] = reg

        

        self.possible_pieces = {
            0: ["L", [[0, 0], [1, 0], [2, 0], [2, 1]]],
            1: ["L", [[2, 0], [0, 1], [1, 1], [2, 1]]],
            2: ["L", [[0, 0], [1, 0], [2, 0], [0, 1]]],
            3: ["L", [[0, 0], [0, 1], [1, 1], [2, 1]]],
            4: ["S" ,[[0, 0], [1, 0], [1, 1], [2, 1]]],
            5: ["S" ,[[1, 0], [2, 0], [0, 1], [1, 1]]],
            6: ["T" ,[[0, 0], [1, 0], [2, 0], [1, 1]]],
            7: ["T" ,[[1, 0], [0, 1], [1, 1], [2, 1]]],
            8: ["L", [[0, 0], [1, 0], [0, 1], [0, 2]]],
            9: ["L", [[0, 0], [0, 1], [0, 2], [1, 2]]],
            10: ["L", [[0, 0], [1, 0], [1, 1], [1, 2]]],
            11: ["L", [[1, 0], [1, 1], [0, 2], [1, 2]]],
            12: ["S" ,[[1, 0], [0, 1], [1, 1], [0, 2]]],
            13: ["S" ,[[0, 0], [0, 1], [1, 1], [1, 2]]],
            14: ["T" ,[[1, 0], [0, 1], [1, 1], [1, 2]]],
            15: ["T" ,[[0, 0], [0, 2], [1, 1], [0, 2]]],
            16: ["I" ,[[0, 0], [0, 1], [0, 2], [0, 3]]],
            17: ["I" ,[[0, 0], [1, 0], [2, 0], [3, 0]]],
        }
        
        self.size = len(self.possible_pieces)

    def copy(self):
        """Creates a deep copy of the board object."""
        new_matrix = np.copy(self.matrix)
        return Board(new_matrix)
    
    def adjacent_regions_to_square(self, row:int, col:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com o quadrado no argumento."""
        adjacent_regions = set() # we use set as it does not allow repeated values
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i >= 0 and i < self.rows and j >= 0 and j < self.cols and (i != row or j != col):
                        adjacent_regions.add(self.matrix[i][j])
        return list(sorted(adjacent_regions))


    def adjacent_regions_to_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""       
        adjacent_regions = set()
        for row, col in self.reg_to_coords[region]:
            for element in self.adjacent_regions_to_square(row, col):
                 if element != region and element not in adjacent_regions:
                    adjacent_regions.add(element)
        return list(sorted(adjacent_regions))


    def adjacent_positions(self, region: int) -> list:
        """Devolve as posições adjacentes à região, em todas as direções, incluindo diagonais."""
        positions = set()
        for row, col in self.reg_to_coords[region]:
            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):
                    if 0 <= i < self.rows and 0 <= j < self.cols and (i != row or j != col):
                        if self.matrix[i][j] != region:
                            positions.add((i, j))
        return list(sorted(positions))

            
    def adjacent_values(self, region:int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
        adj = self.adjacent_positions(region)
        val = []
        for row, col in adj:
            val.append(self.matrix[row,col])
        return val 

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split(:)
        """
        lines = []
        for line in stdin:
            if line.strip(): 
                row = line.strip().split()
                lines.append(row)
        matrix = np.array(lines)
        #matrix = matrix.astype(int)
        return Board(matrix)

#### debugging    



class Nuruomino(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial. Recebe um objeto da classe Board
        que representa o tabuleiro inicial do problema."""
        self.board = board
        #self.initial = NuruominoState(board)


    #ok now we need to implement a auxiliary function that will give if a piece is touching
    #one from another region. There are functions that will give us the regions for each coordinate so
    #maybe we can use that, it seems easy.

    #nao te esquecas de copiar o metodo de verificar que nao ha pecas iguais adjacentes
    def actions(self):
        """Retorna uma lista de ações que podem ser executadas a partir do estado passado como argumento."""
        #action = [2, [[0,0], [0,1], [1,0], [2,0]]]
        #If region.count() ==4, fill it with the only fitting piece
        
        possible_actions = []
        
        for region in self.board.regions:
            store_reg = region
            region = self.board.reg_to_coords[region]
            min_row = 10000
            max_row = -1
            min_col = 10000
            max_col = -1
            for coord in region:
                if coord[0] < min_row:
                    min_row = coord[0]
                if coord[0] > max_row:
                    max_row = coord[0]
                if coord[1] < min_col:
                    min_col = coord[1]
                if coord[1] > max_col:
                    max_col = coord[1]


            if len(region) == 4:
                piece = None #Nah sei :(. Acho que nao preciso. E vou deixar aqui jic.
                action = [store_reg, region] #precisa de ser alterado. Fixar o primeiro ponto a zero zero e subtrair o valor como ja pensaste antes.
                #precisa muuuuito de ser alterado
                possible_actions.append(action)
            elif len(region) < 4:
                none = 0
            
            else:
                dis_ver = max_row - min_row
                dis_hor = max_col - min_col
                coords_square = [[0, 0], [dis_ver, 0], [0, dis_hor], [dis_ver, dis_hor]]

                #Vamos dividir os tipos de quadrados em 3 tipos:
                #1. 3x2
                #2. 2x3
                #3. 1x4 / 4x1
                
                for l in range(8):
                    
                    if dis_ver == 2 and dis_hor == 1:
                    #3x2
                        piece = self.board.possible_pieces[l][1]
                        type_piece = self.board.possible_pieces[l][0]
                        
                        i = 0
                        for element in piece:
                            if self.board.coords_to_reg[(element[0]+min_row, element[1]+min_col)] == store_reg and type_piece not in self.adjacent_regions_to_square(element[0]+dis_ver, element[1]+dis_hor): #<- copiar esta parte
                                i += 1
                        if i == 4:
                            action = [region, self.board.possible_pieces[l]]
                            possible_actions.append(action)
                    else:
                        
                        for disy in range(dis_ver - 2):
                            for disx in range(dis_hor - 1):
                                piece = self.board.possible_pieces[l][1]
                                i = 0
                                for element in piece:
                  
                                    if self.board.coords_to_reg[(element[0]+min_row+disy, element[1]+min_col+disx)] == store_reg:
                                        i += 1
                                        print(i)

                                if i == 4:
                                    action = [region, self.board.possible_pieces[l]]
                                    possible_actions.append(action)

                for j in range(8):

                    if dis_ver == 1 and dis_hor == 2:
                        
                    #2x3
                        piece = self.board.possible_pieces[j + 8][1]
                        i = 0
                        for element in piece:
                            if self.board.coords_to_reg[(element[0]+min_row, element[1]+min_col)] == store_reg:
                                i += 1
                        if i == 4:
                            action = [region, self.board.possible_pieces[j + 8]]
                            possible_actions.append(action)

                    else:
                       
                        for disy in range(dis_ver - 1):
                            for disx in range(dis_hor - 2):
                                piece = self.board.possible_pieces[j + 8][1]
                                i = 0
                                for element in piece:
                                    if self.board.coords_to_reg[(element[0]+min_row+disy, element[1]+min_col+disx)] == store_reg:
                                        i += 1
                                        print(i)
                                if i == 4:
                                    action = [region, self.board.possible_pieces[j + 8]]
                                    possible_actions.append(action)
                    
                #Agora para o caso de 1x4 e 4x1
                if dis_ver == 1 and dis_hor == 4:
                    #1x4
                    piece = self.board.possible_pieces[16][1]
                    i = 0
                    for element in piece:
                        if self.board.coords_to_reg[(element[0]+min_row, element[1]+min_col)] == store_reg:
                            i += 1
                    if i == 4:
                        action = [region, self.board.possible_pieces[16]]
                        possible_actions.append(action)

                elif dis_ver == 4 and dis_hor == 1:
                    #4x1
                    piece = self.board.possible_pieces[17][1]
                    i = 0
                    for element in piece:
                        if self.board.coords_to_reg[(element[0]+min_row, element[1]+min_col)] == store_reg:
                            i += 1
                    if i == 4:
                        action = [region, self.board.possible_pieces[17]]
                        possible_actions.append(action)

                else:
                    for disy in range(dis_ver - 1):
                        for disx in range(dis_hor - 4):
                            piece = self.board.possible_pieces[16][1]
                            i = 0
                            for element in piece:
                                if self.board.coords_to_reg[(element[0]+min_row+disy, element[1]+min_col+disx)] == store_reg:
                                    i += 1
                            if i == 4:
                                action = [region, self.board.possible_pieces[16]]
                                possible_actions.append(action)
                    for disy in range(dis_ver - 4):
                        for disx in range(dis_hor - 1):
                            piece = self.board.possible_pieces[17][1]
                            i = 0
                            for element in piece:
                                if self.board.coords_to_reg[(element[0]+min_row+disy, element[1]+min_col+disx)] == store_reg:
                                    i += 1
                            if i == 4:
                                action = [region, self.possible_pieces[17]]
                                possible_actions.append(action)


        return possible_actions

    def result(self, state: NuruominoState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        #A certa altura, é necessário desenvolver um check para ver se a ação é válida
        #e se não existe uma região adjacente à ação que já tenha sido preenchida. Também
        #é necessário verificar se os valores no board a serem preenchidos correspondem à peça.
        if action in self.possible_actions:
            region = action[0]
            piece = action[1]
            piece_coord = action[2]
            board_updated = state.board.coords_to_reg.copy()

            for i, j in piece_coord:
                board_updated[(i, j)] = piece

            new_board = Board(board_updated)
            return NuruominoState(new_board)

        

    def goal_test(self, state: NuruominoState): 
        # This function states if the goal was reached, by checking if all regions are filled.
        board = state.board
        matrix = board.matrix
        pieces = {'L', 'I', 'T', 'S'} # allowed pieces in the game
        for region, coords in board.coords_to_reg.items():
            piece_in_region = False
            for i, j in coords:
                if matrix[i][j] in pieces: # if region has at least one piece 
                    piece_in_region = True
                    break  
            if not piece_in_region: # if region has no piece return false 
                return False  
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # This function measures how close a node is to the goal, measuring the number of regions to be filled yet.
        board = node.state.board
        matrix = board.matrix
        pieces = {'L', 'I', 'T', 'S'}
        unfilled_regions = 0
        for region, coords in board.reg_to_coords.items():
            piece_in_region = False
            for i, j in coords:
                if matrix[i][j] in pieces:
                    piece_in_region = True
                    break
            if not piece_in_region:
                unfilled_regions += 1 
        return  unfilled_regions # number of unfilled regions in the board 


board = Board.parse_instance()
state = NuruominoState(board)

problem = Nuruomino(board)
action = [1, 'L', [(0, 0), (1, 0), (1, 1), (1, 2)]]
problem.possible_actions = [action]
new_state = problem.result(state, action)
print(new_state)