from pshare import *
from gshare import *
from predictor import *
class tournament(Predictor):
    def __init__(self, bits_to_index, local_history_size, btb_size=1024, pht_size=1024):
        super().__init__(bits_to_index, local_history_size, "Tournament", btb_size, pht_size)
        self.pshare = pshare(bits_to_index, local_history_size, btb_size, pht_size)
        self.gshare = gshare(bits_to_index, local_history_size, btb_size, pht_size)

        self.tournament_selection = 1  
                                        ## 00: 0 -> Strong Pshare  
                                        ## 01: 1 -> Weak Pshare  
                                        ## 10: 2 -> Weak Gshare  
                                        ## 11: 3 -> Strong Gshare
        self.pshare_prediction = ''
        self.gshare_prediction = ''
        
        # Inicialización de variables
        self.PC_branch = 0
        self.local_history_bits = local_history_size

    def predict(self, PC):
        ## Predicción
        self.pshare_prediction = self.pshare.predict(PC)
        self.gshare_prediction = self.gshare.predict(PC)

        return self.pshare_prediction if self.tournament_selection <= 1 else self.gshare_prediction # Retorna la predicción del predictor seleccionado
        
    def update(self, PC, result, prediction):
        result = "T" if result == 1 else "N"                                            # Convertimos result para asegurarnos de que es 'T' o 'N'
        
        # Actualizamos la selección del predictor
        if result == self.pshare_prediction and result != self.gshare_prediction:       # Si pshare predice bien y gshare mal
            if self.tournament_selection > 0:
                self.tournament_selection -= 1
        elif result != self.pshare_prediction and result == self.gshare_prediction:     # Si pshare predice mal y gshare bien
            if self.tournament_selection < 3:
                self.tournament_selection += 1
        
        self.amount_pcs += 1  
        # Actualizamos el contador de predicciones correctas
        if result == prediction:
            self.correct_predictions += 1

        self.btb.append(PC-16)                                                          # Guardar un PC inventado

        # Actualizamos los predictores
        self.pshare.update(PC, result, prediction) 
        self.gshare.update(PC, result, prediction)