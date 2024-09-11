from predictor import *
class pshare(Predictor):
    def __init__(self, index_size, history_size):
        super().__init__(index_size, history_size, "P-Shared")

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
        if result == prediction:
            self.correct_predictions += 1

        self.amount_pcs += 1    

        ## Actualizamos los predictores
        if result == 'T':
            self.local_history[self.PC_Index[self.PC_branch]] = self.local_history[
                self.PC_Index[self.PC_branch]] + 1 if self.local_history[self.PC_Index[self.PC_branch]] < 3 else 3
            self.PC_Index[self.PC_branch] = ((self.PC_Index[
                self.PC_branch] << 1) | int((self.history_size-1)*'0'+'1', 2)) & int(self.history_size*'1', 2)
        else:
            self.local_history[self.PC_Index[self.PC_branch]] = self.local_history[
                self.PC_Index[self.PC_branch]] - 1 if self.local_history[self.PC_Index[self.PC_branch]] > 0 else 0
            self.PC_Index[self.PC_branch] = ((self.PC_Index[
                self.PC_branch] << 1) | int((self.history_size)*'0', 2)) & int(self.history_size*'1', 2)
        
        # Guardar un PC inventado
        if result == "T" and prediction == "T":
            self.btb.append(PC-16)