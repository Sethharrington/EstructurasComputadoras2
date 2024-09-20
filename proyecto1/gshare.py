from predictor import *
# Código de gshare con depuración
import random
class gshare(Predictor):
    def __init__(self, index_size, history_size, btb_size, pht_size):
        super().__init__(index_size, history_size, "G-Shared")

        # Inicialización del BTB y PHT
        self.btb = [0] * btb_size
        self.size_of_branch_table = pht_size
        self.branch_table = [1 for _ in range(self.size_of_branch_table)]  # PHT (Pattern History Table)
        self.global_history_reg = "0" * self.history_size

    def predict(self, PC):
        PC_index = int(PC) % self.size_of_branch_table
        global_history_table = int(self.global_history_reg, 2)
        table_index = PC_index ^ global_history_table
        branch_table_entry = self.branch_table[table_index]

        return "N" if branch_table_entry <= 1 else "T"

    def update(self, PC, result, prediction):
        if result == 1:
            result_str = "T"
        elif result == 0:
            result_str = "N"
        else:
            result_str = result
        
        if result_str == prediction:
            self.correct_predictions += 1

        PC_index = int(PC) % self.size_of_branch_table
        global_history_table = int(self.global_history_reg, 2)
        table_index = PC_index ^ global_history_table
        branch_table_entry = self.branch_table[table_index]

        # Actualización del PHT (Pattern History Table)
        if result_str == "N":
            if branch_table_entry > 0:
                branch_table_entry -= 1
        elif result_str == "T":
            if branch_table_entry < 3:
                branch_table_entry += 1

        self.branch_table[table_index] = branch_table_entry

        # Actualización del registro de historia global
        if result_str == "T":
            self.global_history_reg = self.global_history_reg[-self.history_size+1:] + "1"
        else:
            self.global_history_reg = self.global_history_reg[-self.history_size+1:] + "0"

        # Actualizar el BTB con una dirección de salto aleatoria cuando el resultado sea "Taken"
        if result_str == "T":
            btb_index = int(PC) % len(self.btb)
            if self.btb[btb_index] is None:
                self.btb[btb_index] = random.randint(1000, 10000)  # Generar una dirección de salto aleatoria
            else:
                self.btb[btb_index] = random.randint(1000, 10000)  # Reemplazar la dirección existente con una nueva aleatoria

        self.amount_pcs += 1
