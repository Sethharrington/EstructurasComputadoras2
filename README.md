
# Proyecto de Predicción de Saltos

Este proyecto implementa diferentes esquemas de predicción de saltos en un entorno de simulación en Python. La idea principal es predecir si una instrucción condicional (salto) será tomada o no, utilizando varios algoritmos de predicción como **gshare**, **pshare**, **torneo**, y un **perceptrón**.

## Archivos del Proyecto

### 1. gshare.py
Implementa un predictor **gshare**, que combina el registro de historial global con parte de la dirección del PC (Program Counter) para hacer predicciones.

- **Clases y métodos**:
    - `__init__(self, index_size, history_size)`: Inicializa el predictor `gshare` con una tabla de ramas (`branch_table`) indexada por el PC y el registro de historial global (GHR).
    - `predict(self, PC)`: Calcula la predicción de salto tomando el XOR entre el PC y el historial global.
    - `update(self, PC, result, prediction)`: Actualiza la tabla de predicción con base en el resultado real del salto y ajusta el historial global.
    - `print_predictor(self)`: Muestra el tipo de predictor.
    - `print_results(self)`: Imprime los resultados finales con la tasa de predicciones correctas.

### 2. pshare.py
Implementa un predictor **pshare**, que utiliza un historial local por cada PC (en lugar del historial global) para hacer las predicciones.

- **Clases y métodos**:
    - `__init__(self, index_size, history_size)`: Inicializa la tabla de historial local y la tabla de predicción basada en PC.
    - `predict(self, PC)`: Predice si el salto será tomado o no, basado en el historial local asociado a ese PC.
    - `update(self, PC, result, prediction)`: Actualiza el historial y la tabla de predicción con base en el resultado real del salto.
    - `print_predictor(self)`: Muestra el tipo de predictor.
    - `print_results(self)`: Imprime los resultados finales con la tasa de predicciones correctas.

### 3. tournament.py
Implementa un **predictor de torneo**, que combina los predictores `gshare` y `pshare`. Un contador de selección determina cuál de los dos predictores será utilizado en cada momento.

- **Clases y métodos**:
    - `__init__(self, index_size, history_size)`: Inicializa tanto el predictor `pshare` como el `gshare` y un contador de selección de predictor.
    - `predict(self, PC)`: Decide qué predictor usar basado en el contador de selección y devuelve la predicción.
    - `update(self, PC, result, prediction)`: Actualiza los predictores y ajusta el contador de selección basado en los resultados de ambos predictores.
    - `print_predictor(self)`: Muestra el tipo de predictor.
    - `print_results(self)`: Imprime los resultados con la tasa de predicciones correctas.

### 4. perceptron_predictor.py
Implementa un predictor basado en **perceptrón**, un modelo más avanzado que utiliza un vector de pesos para hacer las predicciones. Este es un predictor no lineal que puede aprender patrones más complejos.

- **Clases y métodos**:
    - `__init__(self, history_length, num_weights)`: Inicializa el perceptrón con un vector de pesos para cada PC y un historial de saltos global.
    - `predict(self, PC)`: Calcula la predicción utilizando un producto punto entre los pesos y el historial.
    - `update(self, PC, actual_outcome, prediction)`: Ajusta los pesos del perceptrón utilizando la regla de aprendizaje del perceptrón.
    - `print_predictor(self)`: Muestra el tipo de predictor.
    - `print_results(self)`: Imprime los resultados con la tasa de predicciones correctas.

### 5. predictors.py
Es el **archivo principal** del proyecto. Proporciona una interfaz de selección de predictores (gshare, pshare, torneo o perceptrón), procesa archivos de trazas, y muestra los resultados.

- **Descripción del flujo**:
    - El programa inicia mostrando un menú para elegir el predictor.
    - Dependiendo de la opción elegida, se inicializa uno de los predictores implementados.
    - El programa luego lee los archivos de trazas (con direcciones y resultados de saltos) y utiliza el predictor seleccionado para hacer predicciones y actualizaciones.
    - Al finalizar el procesamiento de las trazas, el programa muestra la tasa de predicciones correctas.

## Funcionamiento Conceptual

Este proyecto simula predictores de saltos, los cuales son componentes importantes en la arquitectura de procesadores modernos. El objetivo es mejorar la eficiencia al predecir correctamente si una instrucción de salto será tomada o no. Esto permite que los procesadores continúen ejecutando instrucciones sin esperar a que se resuelva un salto.

### Esquemas de predicción:
1. **gshare**: Utiliza una combinación del historial global de saltos y el PC para indexar una tabla de predicciones. Es uno de los predictores más comunes en procesadores modernos.
2. **pshare**: En lugar de utilizar un historial global, este predictor utiliza un historial local para cada PC, permitiendo predicciones más específicas a cada dirección de salto.
3. **Torneo (tournament)**: Combina los predictores `gshare` y `pshare`, seleccionando el mejor predictor basado en su desempeño en saltos anteriores.
4. **Perceptrón**: Implementa un modelo de aprendizaje más avanzado basado en pesos, lo que le permite captar patrones más complejos en el comportamiento de los saltos.

## Uso

1. Descarga los archivos del proyecto.
2. Asegúrate de tener instaladas todas las dependencias necesarias (`numpy` para el perceptrón).
3. Coloca los archivos de trazas en el directorio adecuado.
4. Ejecuta el archivo `predictors.py` para comenzar y selecciona el predictor de tu preferencia.

