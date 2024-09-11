from predictor import *
class gshare(Predictor):
    def __init__(self, index_size, history_size):
        super().__init__(index_size, history_size, "G-Shared")
        
        ## Inicialización de variables
        if self.history_size > self.PC_bits:
            self.history_size = self.PC_bits

        self.size_of_branch_table = 2**index_size

        #First index with PC, second index with GHR
        self.branch_table = [0 for _ in range(self.size_of_branch_table)]
        self.global_history_reg = "0" * self.history_size
        
    def predict(self, PC):
        PC_index = int(PC) % self.size_of_branch_table
        global_history_table = int(self.global_history_reg,2)
        table_index = PC_index ^ global_history_table

        branch_table_entry = self.branch_table[table_index]

        return "N" if branch_table_entry <= 1 else "T"

    def update(self, PC, result, prediction):
        if result == prediction:
            self.correct_predictions += 1
        PC_index = int(PC) % self.size_of_branch_table
        global_history_table = int(self.global_history_reg,2)
        table_index = PC_index ^ global_history_table
        branch_table_entry = self.branch_table[table_index]

        #Update entry accordingly
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry
        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1
        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry
        else:
            updated_branch_table_entry = branch_table_entry + 1
        self.branch_table[table_index] = updated_branch_table_entry

        #Update global history register
        if result == "T":
            self.global_history_reg = self.global_history_reg[-self.history_size+1:] + "1"
        else:
            self.global_history_reg = self.global_history_reg[-self.history_size+1:] + "0"

        self.amount_pcs += 1

        # Guardar un PC inventado
        if result == "T" and prediction == "T":
            self.btb.append(PC-16)