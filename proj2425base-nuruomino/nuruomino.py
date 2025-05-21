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
        self.id = Nuruomino.state_id
        Nuruomino.state_id += 1

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


    def adjacent_regions_to_square(self, row:int, col:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com o quadrado no argumento."""
        adjacent_regions = set()
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i >= 0 and i < self.rows and j >= 0 and j < self.cols and (i != row or j != col):
                        adjacent_regions.add(self.matrix[i][j])
        return sorted(adjacent_regions)


    def adjacent_regions_to_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""       
        adjacent_regions = []
        for row, col in self.reg_to_coords[region]:
            for element in self.adjacent_regions_to_square(row, col):
                 if element != region and element not in adjacent_regions:
                    adjacent_regions.append(element)
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
        for r, c in adj:
            val.append(self.matrix[r,c])
        return val 

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        lines = []
        for line in stdin:
            if line.strip(): 
                row = line.strip().split()
                lines.append(row)
        matrix = np.array(lines)
        matrix = matrix.astype(int)
        return Board(matrix)

#### debugging    
"""
board = Board.parse_instance()
print(board.matrix)
print(board.reg_to_coords)
print(board.regions)
print(board.adjacent_regions_to_square(1,1))
print(board.adjacent_regions_to_regions(3))
print(board.adjacent_values(3))
print(board.adjacent_positions(3))
"""

class Nuruomino(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial. Recebe um objeto da classe Board
        que representa o tabuleiro inicial do problema."""
        self.board = board
        self.initial = NuruominoState(board)

    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        #action = [2, [L, [[0,0], [0,1], [1,0], [2,0]]]] 
        #TODO
        pass 

    def result(self, state: NuruominoState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        #A certa altura, é necessário desenvolver um check para ver se a ação é válida
        #e se não existe uma região adjacente à ação que já tenha sido preenchida. Também
        #é necessário verificar se os valores no board a serem preenchidos correspondem à peça.

        regions = self.board.matrix

        for i in range(self.rows):
            for j in range(self.cols):
                if regions[i][j] == action[0] and [i, j] in action[1][1]:
                    regions[i][j] = action[1][0]
                    
        
        pass 
        

    def goal_test(self, state: NuruominoState):
        board = state.board
        matrix = board.matrix
        pieces = {'L', 'I', 'T', 'S'}
        for region, coords in board.reg_to_coords.items():
            piece_in_region = False
            for i, j in coords:
                if matrix[i][j] in pieces: # if region has at least one piece 
                    piece_in_region = True
                    break  
            if not piece_in_region: # if region has no piece 
                return False  
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        board = node.state.board
        matrix = board.matrix
        pieces = {'L', 'I', 'T', 'S'}
        empty_regions = 0
        for region, coords in board.reg_to_coords.items():
            piece_in_region = False
            for i, j in coords:
                if matrix[i][j] in pieces:
                    piece_in_region = True
                    break
            if not piece_in_region:
                empty_regions += 1 
        return  empty_regions # number of empty regions in the board
