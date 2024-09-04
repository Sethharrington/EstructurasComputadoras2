class gshared:
    def __init__(self, bits_to_index, global_history_size):
        self.name = "G-Shared"
        self.bits_to_index = bits_to_index
        self.size_of_branch_table = 2**bits_to_index
        self.global_history_size = global_history_size
        self.max_index_global_history = 2**self.global_history_size
        #First index with PC, second index with GHR
        self.branch_table = [0 for i in range(self.size_of_branch_table)]

        if self.global_history_size > self.bits_to_index:
            print("El tamaño del registro de historia es mayor que los bits para indexar la tabla se limitará el registro a "+str(self.bits_to_index)+ "bits")
            self.global_history_size = self.bits_to_index

        self.global_history_reg = ""
        for i in range(global_history_size):
            self.global_history_reg += "0"
        self.total_predictions = 0
        self.total_taken_pred_taken = 0
        self.total_taken_pred_not_taken = 0
        self.total_not_taken_pred_taken = 0
        self.total_not_taken_pred_not_taken = 0
        self.correct_predictions = 0

    def print_info(self):
        print("Parámetros del predictor:")
        print("\tTipo de predictor:\t\t\t\tG-Shared")
        print("\tEntradas en el Predictor:\t\t\t"+str(2**self.bits_to_index))
        print("\tTamaño de los registros de historia global:\t"+str(self.global_history_size))

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
        PC_index = int(PC) % self.size_of_branch_table
        GHR_index = int(self.global_history_reg,2)
        table_index = PC_index ^ GHR_index

        #print("Predict")
        #print(PC_index,GHR_index,table_index)
        #print(bin(PC_index),bin(GHR_index),bin(table_index))

        branch_table_entry = self.branch_table[table_index]

        #print(branch_table_entry)

        if branch_table_entry in [0,1]:
            return "N"
        else:
            return "T"

    def update(self, PC, result, prediction):
        PC_index = int(PC) % self.size_of_branch_table
        GHR_index = int(self.global_history_reg,2)
        table_index = PC_index ^ GHR_index

        #print("Update")
        #print(PC_index,GHR_index,table_index)
        #print(bin(PC_index),bin(GHR_index),bin(table_index))

        branch_table_entry = self.branch_table[table_index]
        #print(branch_table_entry)

        #Update entry accordingly
        if branch_table_entry == 0 and result == "N":
            updated_branch_table_entry = branch_table_entry
            #print(PC,GHR_index,branch_table_entry,updated_branch_table_entry,result,prediction)
        elif branch_table_entry != 0 and result == "N":
            updated_branch_table_entry = branch_table_entry - 1
            #print(PC,GHR_index,branch_table_entry,updated_branch_table_entry,result,prediction)
        elif branch_table_entry == 3 and result == "T":
            updated_branch_table_entry = branch_table_entry
            #print(PC,GHR_index,branch_table_entry,updated_branch_table_entry,result,prediction)
        else:
            updated_branch_table_entry = branch_table_entry + 1
            #print(PC,GHR_index,branch_table_entry,updated_branch_table_entry,result,prediction)
        self.branch_table[table_index] = updated_branch_table_entry
        #print(branch_table_entry)

        #Update GHR
        if result == "T":
            self.global_history_reg = self.global_history_reg[-self.global_history_size+1:] + "1"
        else:
            self.global_history_reg = self.global_history_reg[-self.global_history_size+1:] + "0"
        #print("GHR = "+self.global_history_reg)

        #Update stats
        if result == "T" and result == prediction:
            self.total_taken_pred_taken += 1
        elif result == "T" and result != prediction:
            self.total_taken_pred_not_taken += 1
        elif result == "N" and result == prediction:
            self.total_not_taken_pred_not_taken += 1
        else:
            self.total_not_taken_pred_taken += 1

        self.total_predictions += 1
