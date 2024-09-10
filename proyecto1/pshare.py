class pshare:
    def __init__(self, index_size, history_size):
        self.name = "P-Shared"

        # Contadores de predicciones
        self.amount_pcs = 0
        
        ## Inicialización de variables
        self.PC_branch = 0
        self.PC_bits = index_size
        self.history_size = history_size
        self.PC_Index = [0] * (2 ** self.PC_bits)
        self.local_history = [0] * (2 ** self.history_size)
    
    def print_predictor(self):
        print(f"\tTipo de predictor:\t\t\t{self.name}")

    def print_results(self):
        print(f"""Resultados:
        \t# branches:\t\t\t\t\t\t {self.amount_pcs}              
        \tPredicciones correctas: {(100*(self.t_result_t+self.n_result_n)/self.amount_pcs):.3f}%""")
        
    def predict(self, PC):
        ## Predicción
        ## Se toma el PC y se hace un and con una máscara de bits para obtener el índice
        self.PC_branch = int(PC) & int((self.PC_bits)*"1", 2)

        ## Se retorna la predicción, si el contador es mayor o igual a 2 se predice T, de lo contrario N
        ## es saturado a 2 bits       
        return "T" if self.local_history[self.PC_Index[self.PC_branch]] > 1 else "N"
        
    def update(self, PC, result, prediction):
        self.PC_branch = int(PC) & int((self.PC_bits)*"1", 2)
        ## Actualizamos el contador de predicciones
        self.amount_pcs += 1    
        self.correct_predictions = 100*(self.t_result_t+self.n_result_n)/self.amount_pcs
        ## Actualizamos los predictores
        if result == 'T':
            self.local_history[self.PC_Index[self.PC_branch]] = self.local_history[self.PC_Index[self.PC_branch]] + 1 if self.local_history[self.PC_Index[self.PC_branch]] < 3 else 3
            self.PC_Index[self.PC_branch] = ((self.PC_Index[self.PC_branch] << 1) | int((self.history_size-1)*'0'+'1', 2)) & int(self.history_size*'1', 2)
        else:
            self.local_history[self.PC_Index[self.PC_branch]] = self.local_history[self.PC_Index[self.PC_branch]] - 1 if self.local_history[self.PC_Index[self.PC_branch]] > 0 else 0
            self.PC_Index[self.PC_branch] = ((self.PC_Index[self.PC_branch] << 1) | int((self.history_size)*'0', 2)) & int(self.history_size*'1', 2)