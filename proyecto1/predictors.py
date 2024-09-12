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
if opcion in [1, 2, 3]:
    btb_size = int(input("Ingrese el tamaño del BTB (por defecto 1024): ") or 1024)
    pht_size = int(input("Ingrese el tamaño del PHT (por defecto 1024): ") or 1024)
    step_by_step = input("¿Desea ver el modo paso a paso para BTB y PHT? (s/n): ").lower() == 's'
else:
    step_by_step = False  # El perceptrón no usa el modo paso a paso

# Inicializar el predictor seleccionado
if (opcion == 1):
    predictor = pshare(10, 10, btb_size, pht_size)
elif (opcion == 2):
    predictor = gshare(10, 10, btb_size, pht_size)
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

# Solicitar la selección de traces
trace_selection = int(input("Ingrese el número del trace (1-16) o 0 para todos: "))

# Obtener los traces a procesar
traces_to_process = procesar_traces(trace_selection)

# Función para mostrar información en modo paso a paso
# Mostrar paso a paso el BTB y el PHT si es requerido
def step_by_step_display(predictor, PC, result, prediction):
    print(f"\nPC: {PC}, Resultado real: {'T' if result == 1 else 'N'}, Predicción: {prediction}")
    print("BTB (Branch Target Buffer):", predictor.btb)
    if isinstance(predictor, gshare):
        print("PHT (Pattern History Table):", predictor.branch_table)
        print("Registro de historia global:", predictor.global_history_reg)
    elif isinstance(predictor, pshare):
        print("PHT (Pattern History Table):", predictor.local_history)
        print("Índices del PC:", predictor.PC_Index)

    input("\nPresione Enter para continuar...\n")

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

            # Si el modo paso a paso está activado, mostrar información adicional
            if step_by_step and (opcion == 1 or opcion == 2):
                step_by_step_display(predictor, PC, result, prediction)

# Imprimir resultados del predictor
predictor.print_results()

# Mostrar el BTB y PHT después de la ejecución (solo para GShare y PShare)
if opcion in [1, 2]:
    mostrar_btb_pht = input("¿Quieres ver el estado del BTB y PHT? (s/n): ").lower() == 's'
    if mostrar_btb_pht:
        predictor.print_results(show_btb_pht=mostrar_btb_pht)
