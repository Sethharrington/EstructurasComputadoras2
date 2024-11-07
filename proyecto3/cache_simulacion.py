import gzip
from cache_opt import CacheOpt
from cache_no_opt import CacheNoOpt

# Función para obtener el tamaño de la caché
def select_cache_capacity():
    print("Selecciona el tamaño de la caché en KB:")
    print("1. 32 KB")
    print("2. 64 KB")
    print("3. 128 KB")
    choice = input("Elige una opción (1/2/3): ").strip()
    return { '1': 32, '2': 64, '3': 128 }.get(choice, 64)  # Default a 64 KB si la entrada no es válida

# Función para obtener el tamaño de bloque
def select_block_size():
    print("Selecciona el tamaño del bloque en B:")
    print("1. 32 B")
    print("2. 64 B")
    print("3. 128 B")
    choice = input("Elige una opción (1/2/3): ").strip()
    return { '1': 32, '2': 64, '3': 128 }.get(choice, 32)  # Default a 32 B si la entrada no es válida

# Función para obtener la asociatividad de la caché
def select_cache_assoc():
    print("Selecciona la asociatividad de la caché:")
    print("1. 4")
    print("2. 8")
    print("3. 16")
    choice = input("Elige una opción (1/2/3): ").strip()
    return { '1': 4, '2': 8, '3': 16 }.get(choice, 4)  # Default a 4 si la entrada no es válida

# Selección de los parámetros de la caché
cache_capacity = select_cache_capacity()
block_size = select_block_size()
cache_assoc = select_cache_assoc()

# Selección de la versión de caché (optimizada o sin optimización)
opt_choice = input("¿Quieres usar la versión optimizada? (s/n): ").strip().lower()

if opt_choice == 's':
    cache = CacheOpt(cache_capacity, cache_assoc, block_size)
else:
    cache = CacheNoOpt(cache_capacity, cache_assoc, block_size)

cache.print_info()

file_path = "trace.gz"  # Ruta del archivo trace

# Se lee el archivo trace y se procesa
with gzip.open(file_path, 'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        _, ls, address, _ = line.split(" ")
        address = int(address, 16)
        cache.access(int(ls), address)

cache.print_stats()


