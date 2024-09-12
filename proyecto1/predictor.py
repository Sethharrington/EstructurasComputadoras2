class Predictor:
    def __init__(self, index_size, history_size, name):
        self.name = name

        # Contadores de predicciones
        self.amount_pcs = 0
        self.correct_predictions = 0
        
        ## Inicialización de variables
        self.PC_bits = index_size
        self.history_size = history_size
        self.PC_branch = 0
        self.PC_Index = [0] * (2 ** self.PC_bits)
        self.local_history = [0] * (2 ** self.history_size)

        self.btb = []

    def print_predictor(self):
        print(f"\tTipo de predictor:\t\t\t{self.name}")

    def print_results(self):
        print(f"""Resultados:
        \t# branches:\t\t\t\t\t\t {self.amount_pcs}              
        \tPredicciones correctas: {(100*(self.correct_predictions)/self.amount_pcs):.3f}%
        \t""")
        
    def predict(self, PC):
        pass    
    
    def update(self, PC, result, prediction):
        pass