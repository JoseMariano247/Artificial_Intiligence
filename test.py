from search import Problem

class Estado:

    def __init__(self, v3 = 0, v5 = 0):
        self.v3 = v3 # líquido existente na vasilha de 3 litros
        self.v5 = v5 # líquido existente na vasilha de 5 litros

    def encher_3(self):
        self.v3 = 3  # encher a vasilha de 3 litros

    def encher_5(self):
        self.v5 = 5  # encher a vasilha de 5 litros

    def verter_5_para_3(self):
        if self.v5 > 0:
            if self.v3 < 3:
                if self.v5 + self.v3 <= 3:
                    self.v3 += self.v5
                    self.v5 = 0
                else:
                    self.v5 -= (3 - self.v3)
                    self.v3 = 3
            else:
                self.v5 = 0

    def verter_3_para_5(self):
        if self.v3 > 0:
            if self.v5 < 5:
                if self.v3 + self.v5 <= 5:
                    self.v5 += self.v3
                    self.v3 = 0
                else:
                    self.v3 -= (5 - self.v5)
                    self.v5 = 5
            else:
                self.v3 = 0


    def esvaziar_3(self):
        self.v3 = 0  # esvaziar a vasilha de 3 litros
    
    def esvaziar_5(self):
        self.v5 = 0  # esvaziar a vasilha de 5 litros
  

class ProblemaVasilhas(Problem):

    def __init__(self, objetivo3, objetivo5):
        self.initial = Estado(0, 0) # inicialmente ambas as vasilhas
                                    # estão vazias
        self.objetivo3 = objetivo3
        self.objetivo5 = objetivo5

    def actions(self, estado: Estado) -> list:
        return ["encher_3", "encher_5",
                "verter_3_5", "verter_5_3",
                "esvaziar_3", "esvaziar_5"]

    
    def result(self, estado: Estado, acao) -> Estado:
        novo_estado = Estado(estado.v3, estado.v5)
        if acao == "encher_3":
            novo_estado.encher_3()
        elif acao == "encher_5":
            novo_estado.encher_5()
        elif acao == "verter_3_5":
            novo_estado.verter_3_para_5()
        elif acao == "verter_5_3":
            novo_estado.verter_5_para_3()
        elif acao == "esvaziar_3":
            novo_estado.esvaziar_3()
        elif acao == "esvaziar_5":
            novo_estado.esvaziar_5()
        else:
            raise ValueError(f"Ação desconhecida: {acao}")
        return novo_estado
    
    def goal_test(self, estado: Estado) -> bool:
        return estado.v3 == self.objetivo3 and estado.v5 == self.objetivo5
    
    def path_cost(self, c, estado1: Estado, acao, estado2: Estado) -> int:
        # A função de custo é constante, então não importa qual ação foi tomada
        return c + 1
    
    def h(self, node):
        # Heurística: número de litros restantes para atingir o objetivo
        return abs(self.objetivo3 - node.state.v3) + abs(self.objetivo5 - node.state.v5)