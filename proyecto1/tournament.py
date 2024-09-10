from pshare, gshare import *


class tournament:
    def __init__(self, bits_to_index, local_history_size):
        self.name = "tournament"

        # Contadores de predicciones
        self.total_predictions = 0
        self.correct_predictions = 0

        #
        self.result_pshare = ''
        self.result_gshare = ''
        
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
        print("\t# branches tomados predichos correctamente:\t\t"+str(self.total_taken_pred_taken))
        print("\t# branches tomados predichos incorrectamente:\t\t"+str(self.total_taken_pred_not_taken))
        print("\t# branches no tomados predichos correctamente:\t\t"+str(self.total_not_taken_pred_not_taken))
        print("\t# branches no tomados predichos incorrectamente:\t"+str(self.total_not_taken_pred_taken))
        self.correct_predictions = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        formatted_perc = "{:.3f}".format(self.correct_predictions)
        print("\t% predicciones correctas:\t\t\t\t"+str(formatted_perc)+"%")

    def predict(self, PC):
        ## Predicción
        self.result_pshare = pshare.predict(PC)
        self.result_gshare = gshare.predict(PC)
        
        ## Se toma el PC y se hace un and con una máscara de bits para obtener el índice
        self.PC_branch = int(PC) & int((self.PC_bits)*"1", 2)

        ## Se retorna la predicción, si el contador es mayor o igual a 2 se predice T, de lo contrario N
        ## es saturado a 2 bits
        if self.local_history[self.PC_Index[self.PC_branch]] > 1:
            return "T"
        else:
            return "N"
        
    def update(self, PC, result, prediction):
        

        self.PC_branch = int(PC) & int((self.PC_bits)*"1", 2)
        ## Actualizamos el contador de predicciones
        if result == "T" and prediction == "T":
            self.total_taken_pred_taken += 1
        elif result == "T" and prediction == "N":
            self.total_taken_pred_not_taken += 1
        elif result == "N" and prediction == "T":
            self.total_not_taken_pred_taken += 1
        elif result == "N" and prediction == "N":
            self.total_not_taken_pred_not_taken += 1
        self.total_predictions += 1    
        self.correct_predictions = 100*(self.total_taken_pred_taken+self.total_not_taken_pred_not_taken)/self.total_predictions
        ## Actualizamos los predictores
        if result == 'T':
            self.local_history[self.PC_Index[self.PC_branch]] = self.local_history[self.PC_Index[self.PC_branch]] + 1 if self.local_history[self.PC_Index[self.PC_branch]] < 3 else 3
            self.PC_Index[self.PC_branch] = ((self.PC_Index[self.PC_branch] << 1) | int((self.local_history_bits-1)*'0'+'1', 2)) & int(self.local_history_bits*'1', 2)
        else:
            self.local_history[self.PC_Index[self.PC_branch]] = self.local_history[self.PC_Index[self.PC_branch]] - 1 if self.local_history[self.PC_Index[self.PC_branch]] > 0 else 0
            self.PC_Index[self.PC_branch] = ((self.PC_Index[self.PC_branch] << 1) | int((self.local_history_bits)*'0', 2)) & int(self.local_history_bits*'1', 2)
