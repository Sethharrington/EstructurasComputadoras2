from pshare import *
from gshare import *


class tournament:
    def __init__(self, bits_to_index, local_history_size):
        self.name = "tournament"
        self.pshare = pshare(bits_to_index, local_history_size)
        self.gshare = gshare(bits_to_index, local_history_size)
        # Contadores de predicciones
        self.total_predictions = 0
        self.correct_predictions = 0
        self.correct_predictions_rate = 0

        #
        self.tournament_selection = 1
            ## 00: 0 -> Strong Pshare
            ## 01: 1 -> Weak Pshare
            ## 10: 2 -> Weak Gshare
            ## 11: 3 -> Strong Gshare
        self.pshare_prediction = ''
        self.gshare_prediction = ''
        
        # Inicialización de variables
        self.PC_branch = 0
        self.PC_bits = bits_to_index
        self.local_history_bits = local_history_size
        self.PC_Index = [0] * (2 ** self.PC_bits)
        self.local_history = [0] * (2 ** self.local_history_bits)
    
    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\tP-Shared")

    def print_stats(self):
        print("Resultados de la simulación")
        print("\t# branches:\t\t\t\t\t\t"+str(self.total_predictions))
        self.correct_predictions_rate = 100*self.correct_predictions_rate/self.total_predictions
        formatted_perc = "{:.3f}".format(self.correct_predictions)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    def predict(self, PC):
        ## Predicción
        self.pshare_prediction = self.pshare.predict(PC)
        self.gshare_prediction = self.gshare.predict(PC)

        # Si el contador es 0 o 1 se retorna la predicción de pshare de lo contrario se retorna la predicción de gshare
        if self.tournament_selection <= 1:
            return self.pshare_prediction
        else:
            return self.gshare_prediction
        
    def update(self, PC, result, prediction):
        # Actualizamos la selección del predictor
        if ((result == self.pshare_result and result == self.gshare_result)
            or ((result != self.pshare_result and result != self.gshare_result))): # Si ambos predicen bien
                self.tournament_selection = self.tournament_selection
        elif (result == self.pshare_result and result != self.gshare_result): # Si pshare predice bien y gshare mal
            # Si el contador es 0 no se hace nada porque ya está en el estado de pshare
            if(self.tournament_selection > 0):
                self.tournament_selection -=1 
        elif (result != self.pshare_result and result == self.gshare_result): # Si pshare predice mal y gshare bien
            # Si el contador es 3 no se hace nada porque ya está en el estado de gshare
            if(self.tournament_selection < 3):
                self.tournament_selection +=1
        
        # Actualizamos el contador de predicciones
        if result == prediction:
            self.correct_predictions += 1
        self.total_predictions += 1

        # Actualizamos los predictores
        self.pshare.update(PC, result, prediction)
        self.gshare.update(PC, result, prediction)