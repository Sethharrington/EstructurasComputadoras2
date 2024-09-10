import numpy as np

class PerceptronPredictor:
    def __init__(self, history_length, num_weights):
        self.name = "Perceptron"
        self.history_length = history_length
        self.num_weights = num_weights
        self.weights = {}  # Key: PC, Value: weight vector for that PC
        self.history = [0.0] * history_length  # Global history of branches (numeric: 1 for taken, 0 for not taken)
        self.bias = 1.0  # Bias term as float
        self.amount_pcs = 0  # Counter for number of branches
        self.t_result_t = 0  # Correct taken predictions
        self.n_result_n = 0  # Correct not-taken predictions

    def initialize_weights(self, PC):
        # Initialize weights for a given PC if not already done
        PC = str(PC)  # Ensure PC is treated as a string
        if PC not in self.weights:
            self.weights[PC] = np.zeros(self.history_length + 1, dtype=float)  # +1 for bias, initialized as float

    def predict(self, PC):
        PC = str(PC)  # Ensure PC is treated as a string
        self.initialize_weights(PC)
        weights = self.weights[PC]
        # Dot product of weights and history (including bias), forcing float conversion
        y = np.dot(weights[:-1], np.array(self.history, dtype=float)) + weights[-1] * float(self.bias)
        return 1 if y >= 0 else 0

    def update(self, PC, actual_outcome, prediction):
        PC = str(PC)  # Ensure PC is treated as a string
        self.initialize_weights(PC)
        weights = self.weights[PC]
        if prediction != actual_outcome:
            # Update the weights (Perceptron learning rule)
            for i in range(self.history_length):
                weights[i] += (1.0 if actual_outcome == 1 else -1.0) * self.history[i]
            # Update the bias
            weights[-1] += (1.0 if actual_outcome == 1 else -1.0) * self.bias
        # Update history
        self.history = [float(actual_outcome)] + self.history[:-1]

        # Update result counters
        self.amount_pcs += 1
        if prediction == actual_outcome:
            if prediction == 1:
                self.t_result_t += 1
            else:
                self.n_result_n += 1

    def process_trace(self, trace_file):
        total_predictions = 0
        correct_predictions = 0

        with open(trace_file, 'r') as file:
            for line in file:
                PC, outcome = line.split()
                # Convert 'T' to 1 and 'N' to 0
                outcome = 1 if outcome == '1' else 0
                prediction = self.predict(PC)
                if prediction == outcome:
                    correct_predictions += 1
                self.update(PC, outcome, prediction)
                total_predictions += 1

        accuracy = correct_predictions / total_predictions * 100
        return accuracy

    def print_predictor(self):
        print(f"\tTipo de predictor:\t\t\t{self.name}")

    def print_results(self):
        print(f"""Resultados:
        \t# branches:\t\t\t\t\t\t {self.amount_pcs}              
        \tPredicciones correctas: {(100*(self.t_result_t+self.n_result_n)/self.amount_pcs):.3f}%""")
