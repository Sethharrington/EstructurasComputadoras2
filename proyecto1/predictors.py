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

# Create the predictor
print("------- Menu de predictores -----")
print("1. Pshare",
        "2. Gshre",
        "3. Tournament",
        "4. Perceptron",
        "5. Terminar programa",
        sep='\n')
opcion = int(input("Ingrese una opción: "))
if (opcion == 1):
    predictor = pshare(10, 10)
elif (opcion == 2):
    predictor = gshare(10, 10)
elif (opcion == 3):
    predictor = tournament(10, 10)
elif (opcion == 4):
    predictor = PerceptronPredictor(history_length=8, num_weights=8)  # Initialize perceptron predictor
elif (opcion == 5):
    print("\nPrograma finalizado...")
    exit()
else:
    print("Opción no válida")
    exit()

predictor.print_predictor()
# Iterate over the traces
for trace in traces:
    DEBUG = True
    if (DEBUG):
        i = 0
    with open(trace_path + trace, 'r') as trace_fh:
        for line in trace_fh:
            line = line.rstrip()
            PC, result = line.split(" ")
            # Convert '1' to 1 (Taken) and '0' to 0 (Not Taken)
            result = 1 if result == "1" else 0

            PC = int(PC, 16)
            prediction = predictor.predict(PC)
            predictor.update(PC, result, prediction)

            if (DEBUG):
                i += 1
                if i == 10:
                    break
predictor.print_results()
