import py7zr
import os
from pshare import *
from gshare import *
from tournament import *
from perceptron_predictor import PerceptronPredictor  # Importing Perceptron Predictor

pathfile = "traces.7z"
trace_path = "traces/"

# Check if traces folder exists 
# Open the 7z file and extract the traces
if (not os.path.exists(trace_path)):
    with py7zr.SevenZipFile(pathfile,'r') as trace_fh:
        trace_fh.extractall(path="./proyecto1/")

# List the traces
traces = os.listdir(trace_path)
traces.sort()

# Menu for Selecting Predictors
print("------- Menu de predictores -----")
print("1. Pshare",
        "2. Gshre",
        "3. Tournament",
        "4. Perceptron",
        "5. Terminar programa",
        sep='\n')

# user to select an option
opcion = int(input("Ingrese una opción: "))
# Initialize the appropriate predictor based on the user's selection
if (opcion == 1):
    # Initialize Pshare predictor with parameters
    predictor = pshare(10, 10)
elif (opcion == 2):
    # Initialize Gshare predictor with parameters
    predictor = gshare(10, 10)
elif (opcion == 3):
    # Initialize Tournament predictor with parameters
    predictor = tournament(10, 10)
elif (opcion == 4):
    # Initialize Perceptron predictor with parameters
    predictor = PerceptronPredictor(history_length=8, num_weights=8)  # Initialize perceptron predictor
elif (opcion == 5):
    # Print a message and exit
    print("\nPrograma finalizado...")
    exit() # Exit the program
else:
    print("Opción no válida")
    exit() # Exit the program

# Print the configuration
predictor.print_predictor()
# Iterate over the traces
for trace in traces:
    DEBUG = True # Enable debugging mode
    if (DEBUG):
        i = 0 # Initialize a counter for debugging

    # Open the current trace file in read mode
    with open(trace_path + trace, 'r') as trace_fh:
        # Process each line in the trace file
        for line in trace_fh:
            line = line.rstrip()# Remove any trailing whitespace characters
            # Split the line into the program counter (PC) and the branch result
            PC, result = line.split(" ") 
            # Convert '1' to 1 (Taken) and '0' to 0 (Not Taken)
            result = 1 if result == "1" else 0
            # Convert the program counter from hexadecimal to an integer
            PC = int(PC, 16)
            # Predict the outcome of the branch using the selected predictor
            prediction = predictor.predict(PC)
            # Update the predictor with the actual outcome and the prediction
            predictor.update(PC, result, prediction)
             # If debugging is enabled, break after 10 iterations
            if (DEBUG):
                i += 1
                if i == 10:
                    break
# Print the final results or statistics of the predictor's performance
predictor.print_results()
