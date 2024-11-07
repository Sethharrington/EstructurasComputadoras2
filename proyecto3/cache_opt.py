from math import log2, floor

class CacheOpt:
    def __init__(self, cache_capacity, cache_assoc, block_size, cache_name=""):
        self.name = cache_name
        self.total_access = 0
        self.total_misses = 0
        self.total_reads = 0
        self.total_read_misses = 0
        self.total_writes = 0
        self.total_write_misses = 0
        self.cache_capacity = int(cache_capacity)
        self.cache_assoc = int(cache_assoc)
        self.block_size = int(block_size)
        self.byte_offset_size = int(log2(self.block_size))
        self.num_sets = int((self.cache_capacity * 1024) / (self.block_size * self.cache_assoc))
        self.index_size = int(log2(self.num_sets))
        self.valid_table = [[False] * self.cache_assoc for _ in range(self.num_sets)]
        self.tag_table = [[0] * self.cache_assoc for _ in range(self.num_sets)]
        self.replace_table = [[i for i in range(self.cache_assoc)] for _ in range(self.num_sets)]
        self.last_address = None  # Para detectar accesos secuenciales

    def print_info(self):
        print("Parámetros del caché:")
        print(f"\tCapacidad:\t\t{self.cache_capacity} kB")
        print(f"\tAssociatividad:\t\t{self.cache_assoc}")
        print(f"\tTamaño de Bloque:\t{self.block_size} B")

    def print_stats(self):
        miss_rate = f"{((100.0 * self.total_misses) / self.total_access):.3f}" if self.total_access > 0 else "0.000"
        result_str = (f"Resultados de la simulación\n"
                      f"\tAccesos totales: {self.total_access}\n"
                      f"\tMisses totales: {self.total_misses}\n"
                      f"\tMiss Rate: {miss_rate}%")
        print(result_str)

    def access(self, ls, address):
        index_ = int((address // (2 ** self.byte_offset_size)) % (2 ** self.index_size))
        tag = int(address // (2 ** (self.byte_offset_size + self.index_size)))

        cache_index = self.find(index_, tag)

        if cache_index == -1:  # Miss
            self.total_misses += 1
            self.bring_to_cache(index_, tag)
            if ls == 0:
                self.total_read_misses += 1
            else:
                self.total_write_misses += 1
        else:  # Hit
            self.replace_table[index_].remove(cache_index)
            self.replace_table[index_].insert(0, cache_index)

        # Detectar acceso secuencial y hacer prefetch agresivo
        if self.last_address is not None:
            next_address = self.last_address + self.block_size
            second_next_address = next_address + self.block_size
            self.prefetch(next_address)
            self.prefetch(second_next_address)

        self.last_address = address
        self.total_access += 1
        if ls == 0:
            self.total_reads += 1
        else:
            self.total_writes += 1

    def find(self, index_, tag):
        for i in range(self.cache_assoc):
            if self.valid_table[index_][i] and self.tag_table[index_][i] == tag:
                return i
        return -1

    def bring_to_cache(self, index_, tag):
        index_to_replace = self.replace_table[index_].pop()
        self.replace_table[index_].insert(0, index_to_replace)
        self.valid_table[index_][index_to_replace] = True
        self.tag_table[index_][index_to_replace] = tag

    def prefetch(self, address):
        """
        Prefetching agresivo: intenta cargar más de un bloque futuro.
        """
        index_ = int((address // (2 ** self.byte_offset_size)) % (2 ** self.index_size))
        tag = int(address // (2 ** (self.byte_offset_size + self.index_size)))

        if self.find(index_, tag) == -1:
            self.bring_to_cache(index_, tag)

    def save_results(self, filename, trace):
        miss_rate = f"{((100.0 * self.total_misses) / self.total_access):.3f}" if self.total_access > 0 else "0.000"
        result_str = (f"{trace},{self.name},{self.cache_capacity},{self.cache_assoc},"
                      f"{self.block_size},{self.total_access},{self.total_misses},{miss_rate}%\n")
        with open(filename, 'a') as f:
            f.write(result_str)
