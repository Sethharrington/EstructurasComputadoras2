import py7zr
import os
from pshare import *
from gshare import *
from tournament import *
from perceptron_predictor import PerceptronPredictor  # Importando el predictor Perceptron

# Variables de ruta
pathfile = "traces.7z"
trace_path = "traces/"

# Verificar si la carpeta de traces existe y extraer los archivos si es necesario
if (not os.path.exists(trace_path)):
    with py7zr.SevenZipFile(pathfile, 'r') as trace_fh:
        trace_fh.extractall(path="./proyecto1/")

# Listar los traces disponibles
traces = os.listdir(trace_path)
traces.sort()

# Menú para seleccionar predictores
print("------- Menú de predictores -----")
print("1. Pshare",
      "2. Gshare",
      "3. Tournament",
      "4. Perceptron",
      "5. Terminar programa",
      sep='\n')

# Usuario selecciona una opción
opcion = int(input("Ingrese una opción: "))

# Inicializar el predictor adecuado según la opción seleccionada
if (opcion == 1):
    predictor = pshare(10, 10)
elif (opcion == 2):
    predictor = gshare(10, 10)
elif (opcion == 3):
    predictor = tournament(10, 10)
elif (opcion == 4):
    predictor = PerceptronPredictor(history_length=8, num_weights=8)
elif (opcion == 5):
    print("\nPrograma finalizado...")
    exit()
else:
    print("Opción no válida.")
    exit()

# Nueva selección de trace por parte del usuario
print("\n--- Selección de Trace ---")
print("Ingrese un número del 1 al 16 para seleccionar un trace específico, o ingrese 0 para ejecutar todos los traces.")
trace_selection = int(input("Seleccione el trace: "))

# Función para procesar los traces
def procesar_traces(trace_selection):
    # Si el usuario selecciona 0, usar todos los traces
    if trace_selection == 0:
        traces_to_run = traces
    else:
        # Si selecciona un número entre 1 y 16, seleccionamos el trace correspondiente
        trace_number = f"trace_{str(trace_selection).zfill(2)}"
        if trace_number in traces:
            traces_to_run = [trace_number]
        else:
            print(f"El trace {trace_number} no existe.")
            exit()
    
    return traces_to_run

# Obtener los traces a procesar
traces_to_process = procesar_traces(trace_selection)

# Ejecutar el predictor para cada trace seleccionado
for trace in traces_to_process:
    with open(trace_path + trace, 'r') as trace_fh:
        for line in trace_fh:
            line = line.rstrip()
            PC, result = line.split(" ")
            result = int(result)  # Mantener 1 para Taken y 0 para Not Taken
            PC = int(PC, 16)
            prediction = predictor.predict(PC)
            predictor.update(PC, result, prediction)

# Imprimir resultados del predictor
predictor.print_results()
