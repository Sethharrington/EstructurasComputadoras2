import gzip
from cache_opt import *
from cache_no_opt import *

cache_capacity = 64
block_size = 32
cache_assoc = 4
file_path = "trace.gz"

# Selección de la versión de caché
opt_choice = input("¿Quieres usar la versión optimizada? (s/n): ").strip().lower()

if opt_choice == 's':
    cache = CacheOpt(cache_capacity, cache_assoc, block_size)
else:
    cache = CacheNoOpt(cache_capacity, cache_assoc, block_size)

cache.print_info()

with gzip.open(file_path, 'rt') as trace_fh:
    for line in trace_fh:
        line = line.rstrip()
        _, ls, address, _ = line.split(" ")
        address = int(address, 16)
        cache.access(int(ls), address)

        if opt_choice == 's' and cache.total_access % 100 == 0:
            cache.process_pending_requests()

if opt_choice == 's':
    cache.process_pending_requests()

cache.print_stats()
