from predictor import *
# Código de gshare con depuración
class gshare(Predictor):
    def __init__(self, index_size, history_size):
        super().__init__(index_size, history_size, "G-Shared")
        
        # Inicialización de variables
        if self.history_size > self.PC_bits:
            self.history_size = self.PC_bits

        self.size_of_branch_table = 2**index_size

        # Inicialización de la tabla de predicciones y registro de historia global
        self.branch_table = [1 for _ in range(self.size_of_branch_table)]  # Iniciar en estado débilmente tomado
        self.global_history_reg = "0" * self.history_size  # Inicialización del registro de historia global
        
    def predict(self, PC):
        # Cálculo del índice utilizando XOR entre el PC y el registro de historia global
        PC_index = int(PC) % self.size_of_branch_table
        global_history_table = int(self.global_history_reg, 2)
        table_index = PC_index ^ global_history_table

        branch_table_entry = self.branch_table[table_index]
        # Predicción: si el valor es menor o igual a 1 (débilmente o fuertemente no tomado), devuelve "N"
        return "N" if branch_table_entry <= 1 else "T"

    def update(self, PC, result, prediction):
        # Convertir result a "T" o "N" para asegurar que el predictor funcione correctamente
        result = "T" if result == 1 else "N"
        
        # Contador de predicciones correctas
        if result == prediction:
            self.correct_predictions += 1

        # Cálculo del índice para acceder a la tabla de predicciones
        PC_index = int(PC) % self.size_of_branch_table
        global_history_table = int(self.global_history_reg, 2)
        table_index = PC_index ^ global_history_table
        branch_table_entry = self.branch_table[table_index]

        # Actualización de la tabla de predicciones según el resultado
        if result == "N":
            if branch_table_entry > 0:  # Decrementar si no está ya en el estado más bajo
                branch_table_entry -= 1
        elif result == "T":
            if branch_table_entry < 3:  # Incrementar si no está ya en el estado más alto
                branch_table_entry += 1

        # Actualización de la tabla
        self.branch_table[table_index] = branch_table_entry

        # Actualización del registro de historia global (agregar el resultado al final del historial)
        if result == "T":
            self.global_history_reg = self.global_history_reg[-self.history_size+1:] + "1"
        else:
            self.global_history_reg = self.global_history_reg[-self.history_size+1:] + "0"

        self.amount_pcs += 1  # Incrementar el número de predicciones
