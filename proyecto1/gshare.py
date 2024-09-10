class gshare:
    def __init__(self, index_size, history_size):
        self.name = "G-Shared"
        self.index_size = index_size
        self.size_of_branch_table = 2**index_size
        self.history_size = history_size
        self.max_index_global_history = 2**self.history_size

        #First index with PC, second index with GHR
        self.branch_table = [0 for i in range(self.size_of_branch_table)]
        if self.history_size > self.index_size:
            print("El tamaño del registro de historia es mayor que los bits para indexar la tabla se limitará el registro a "+str(self.index_size)+ "bits")
            self.history_size = self.index_size
        self.global_history_reg = ""
        for i in range(history_size):
            self.global_history_reg += "0"
        self.amount_pcs = 0
        self.correct_predictions = 0

    def print_predictor(self):
        print(f"\tTipo de predictor:\t\t\t{self.name}")

    def print_results(self):
        print(f"""Resultados:
        \t# branches:\t\t\t\t\t\t {self.amount_pcs}              
        \tPredicciones correctas: {(100*(self.t_result_t+self.n_result_n)/self.amount_pcs):.3f}%""")

    def predict(self, PC):
        PC_index = int(PC) % self.size_of_branch_table
        GHR_index = int(self.global_history_reg,2)
        table_index = PC_index ^ GHR_index

        branch_table_entry = self.branch_table[table_index]

        return "N" if branch_table_entry in [0,1] else "T"

    def update(self, PC, result, prediction):
        PC_index = int(PC) % self.size_of_branch_table
        GHR_index = int(self.global_history_reg,2)
        table_index = PC_index ^ GHR_index

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

        #Update GHR
        if result == "T":
            self.global_history_reg = self.global_history_reg[-self.history_size+1:] + "1"
        else:
            self.global_history_reg = self.global_history_reg[-self.history_size+1:] + "0"

        self.amount_pcs += 1
