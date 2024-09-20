from predictor import *
import random

class pshare(Predictor):
    def __init__(self, index_size, history_size, btb_size, pht_size):
        super().__init__(index_size, history_size, "P-Shared")

        # Inicialización del BTB y PHT
        self.btb = [0] * btb_size
        self.local_history = [0] * pht_size  # PHT

    def predict(self, PC):
        self.PC_branch = int(PC) & int((self.PC_bits) * "1", 2)

        return "T" if self.local_history[self.PC_Index[self.PC_branch]] > 1 else "N"

    def update(self, PC, result, prediction):
        if result == 1:
            result_str = "T"
        elif result == 0:
            result_str = "N"
        else:
            result_str = result

        if result_str == prediction:
            self.correct_predictions += 1

        self.amount_pcs += 1

        if result_str == "T":
            self.local_history[self.PC_Index[self.PC_branch]] = min(3, self.local_history[self.PC_Index[self.PC_branch]] + 1)
            self.PC_Index[self.PC_branch] = ((self.PC_Index[
                self.PC_branch] << 1) | 1) & int(self.history_size * '1', 2)
        else:
            self.local_history[self.PC_Index[self.PC_branch]] = max(0, self.local_history[self.PC_Index[self.PC_branch]] - 1)
            self.PC_Index[self.PC_branch] = (self.PC_Index[self.PC_branch] << 1) & int(self.history_size * '1', 2)

        # Actualizar el BTB con una dirección de salto aleatoria cuando el resultado sea "Taken"
        if result_str == "T":
            btb_index = int(PC) % len(self.btb)
            if self.btb[btb_index] is None:
                self.btb[btb_index] = random.randint(1000, 10000)  # Generar una dirección de salto aleatoria
            else:
                self.btb[btb_index] = random.randint(1000, 10000)  # Reemplazar la dirección existente con una nueva aleatoria
