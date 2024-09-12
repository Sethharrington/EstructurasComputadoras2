class Predictor:
    def __init__(self, index_size, history_size, name, btb_size=1024, pht_size=1024):
        self.name = name
        self.amount_pcs = 0
        self.correct_predictions = 0
        self.PC_bits = index_size
        self.history_size = history_size
        self.btb_size = btb_size  # Nuevo parámetro
        self.pht_size = pht_size  # Nuevo parámetro

        # Inicialización del BTB y PHT según los tamaños dados
        self.PC_Index = [0] * btb_size
        self.local_history = [0] * pht_size

        # Inicialización del BTB con 0 para seguimiento más claro
        self.btb = [0] * btb_size  # Lista que simula el BTB

    def print_predictor(self):
        print(f"\tTipo de predictor:\t\t\t{self.name}")

    def print_results(self, show_btb_pht=False):
        """
        Imprime los resultados del predictor. Si 'show_btb_pht' es True,
        también imprime el estado del BTB y del PHT.
        """
        print(f"""Resultados:
        \t# branches:\t\t\t\t\t\t {self.amount_pcs}              
        \tPredicciones correctas: {(100 * (self.correct_predictions) / self.amount_pcs):.3f}%""")
        
        if show_btb_pht:
            print(f"\nBTB (Branch Target Buffer): {self.btb}")
            print(f"PHT (Pattern History Table): {self.local_history}")

    def predict(self, PC):
        pass    

    def update(self, PC, result, prediction):
        pass

    # Método para mostrar el BTB y PHT paso a paso
    def step_by_step_display(self):
        print(f"BTB (Branch Target Buffer): {self.btb}")
        print(f"PHT (Pattern History Table): {self.local_history}")


