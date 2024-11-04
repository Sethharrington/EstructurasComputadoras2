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
        self.valid_table = [[False for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]
        self.tag_table = [[0 for _ in range(self.cache_assoc)] for _ in range(self.num_sets)]
        self.replace_table = [[k for k in range(self.cache_assoc)] for _ in range(self.num_sets)]
        
        self.result_str = ""
        self.pending_requests = []  # Cola para solicitudes pendientes por misses

    def print_info(self):
        """
        Imprime la información de los parámetros de la caché.
        """
        print("Parámetros del caché:")
        print("\tCapacidad:\t\t\t" + str(self.cache_capacity) + "kB")
        print("\tAssociatividad:\t\t\t" + str(self.cache_assoc))
        print("\tTamaño de Bloque:\t\t\t" + str(self.block_size) + "B")

    def print_stats(self):
        """
        Imprime los resultados de la simulación.
        """
        print("Resultados de la simulación")
        try:
            miss_rate = f"{((100.0 * self.total_misses) / self.total_access):.3f}"
        except ZeroDivisionError:
            miss_rate = "0.000"
        self.result_str += f"\tAccesos: {self.total_access}\n\tMisses: {self.total_misses}\n\tMiss Rate: {miss_rate}%"
        print(self.result_str)

    def access(self, ls, address):
        """
        Realiza un acceso a la caché, gestionando hits y misses.
        """
        # Se separa el address en offset, index y tag
        offset = int(address % (2 ** self.byte_offset_size))
        index_ = int(floor(address / (2 ** self.byte_offset_size)) % (2 ** self.index_size))
        tag = int(floor(address / (2 ** (self.byte_offset_size + self.index_size))))

        # Verifica si el bloque está en caché
        isFound = self.find(index_, tag)
        result = False

        # Maneja el miss: Si el bloque no está, registra el miss y agrega a pendientes
        if isFound == -1:
            self.total_misses += 1
            self.pending_requests.append((index_, tag))  # Agrega el miss a la cola
            if ls == 0:
                self.total_read_misses += 1
            else:
                self.total_write_misses += 1
            result = True
        else:
            # Maneja el hit: Si el bloque está, actualiza la tabla de reemplazo y resuelve el hit
            index_to_replace = self.tag_table[index_].index(tag)
            self.replace_table[index_].remove(index_to_replace)
            self.replace_table[index_].insert(0, index_to_replace)

        # Permite continuar con hits mientras hay misses pendientes
        self.total_access += 1
        if ls == 0:
            self.total_reads += 1
        else:
            self.total_writes += 1
        return result

    def find(self, index_, tag):
        """
        Busca el tag en el set indicado por el index, si se encuentra retorna el índice en la caché, sino retorna -1.
        """
        for cache_index in range(self.cache_assoc):
            if self.valid_table[index_][cache_index] and (self.tag_table[index_][cache_index] == tag):
                return cache_index
        return -1

    def bring_to_cache(self, index_, value):
        """
        Trae un nuevo bloque a la caché en caso de un miss y actualiza la tabla de reemplazo.
        """
        # Se busca un espacio en la caché para guardar el tag
        index_to_replace = self.replace_table[index_][self.cache_assoc - 1]
        self.replace_table[index_].remove(index_to_replace)
        self.replace_table[index_].insert(0, index_to_replace)
        self.valid_table[index_][index_to_replace] = True
        self.tag_table[index_][index_to_replace] = value

    def process_pending_requests(self):
        """
        Procesa cada solicitud pendiente y la trae a caché cuando el bloque faltante está listo.
        """
        for (index_, tag) in self.pending_requests:
            self.bring_to_cache(index_, tag)  # Trae el bloque a la caché
        self.pending_requests.clear()  # Borra la cola una vez que se han resuelto

    def save_results(self, filename, trace):
        """
        Guarda los resultados de la simulación en un archivo.
        """
        with open(filename, 'a') as f:
            f.write(f"{trace},{self.name},{self.cache_capacity},{self.cache_assoc},{self.block_size},{self.result_str}\n")
