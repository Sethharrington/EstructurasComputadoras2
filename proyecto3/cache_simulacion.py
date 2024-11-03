import gzip
from cache import *

cache_capacity = 64                             # Cache capacity
block_size = 32                                 # Block size
cache_assoc = 4                                 # Cache associativity
file_path = "./proyecto3/trace.gz"              # Trace file

# Se crea una instancia de la clase cache
cache = cache(cache_capacity, cache_assoc, block_size)

# Se imprime la información de la cache
cache.print_info()

# i = 0 #SOLO PARA DEBUG
# Se lee el archivo trace
with gzip.open(file_path,'rt') as trace_fh:

    # Se recorre el archivo trace
    for line in trace_fh:
        line = line.rstrip()

        # Se obtienen los valores de la línea
        hash, ls, address, ic  = line.split(" ") # hash, load/store, address, instruction count

        # Se convierte la dirección a entero
        address = int(address, 16) # Convertir de hexadecimal a entero

        # Se simula el acceso a la cache
        cache.access(ls, address) # Se accede a la cache
        # i += 1
        # if i == 10:
        #     break

# Se imprimen los resultados de la simulación
cache.print_stats()
