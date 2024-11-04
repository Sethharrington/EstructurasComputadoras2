from math import log2 ,floor

class CacheNoOpt :
    def __init__ (self, cache_capacity, cache_assoc , block_size, cache_name = "" ):
        self.name = cache_name
        self.total_access =0 
        self.total_misses =0 
        self.total_reads =0 
        self.total_read_misses =0 
        self.total_writes =0 
        self.total_write_misses =0 
        self.cache_capacity =int (cache_capacity )
        self.cache_assoc =int ( cache_assoc )
        self.block_size =int ( block_size )
        self.byte_offset_size =log2(self.block_size )
        self.num_sets =int ((self.cache_capacity *1024 )/(self.block_size *self.cache_assoc ))
        self.index_size =int (log2 (self.num_sets ))
        self.valid_table =[[False for i in range (self.cache_assoc )]for l in range (self.num_sets )]
        self.tag_table =[[0 for j in range (self.cache_assoc )]for m in range (self.num_sets )]
        self.replace_table =[[k for k in range(self.cache_assoc )]for n in range (self.num_sets )]
        
        self.result_str = ""

    def print_info (self):
        """
        """
        print ("Parámetros del caché:")
        print ("\tCapacidad:\t\t\t"+str (self.cache_capacity )+"kB")
        print ("\tAssociatividad:\t\t\t"+str (self.cache_assoc ))
        print ("\tTamaño de Bloque:\t\t\t"+str (self.block_size )+"B")
    
    def print_stats (self):
        """
        """
        print ("Resultados de la simulación")
        try:
            miss_rate = f"{((100.0 *self.total_misses )/self.total_access):.3f}"
        except ZeroDivisionError:
            miss_rate = "0.000"
        self.result_str +=f"\tAccesos: {self.total_access}\n\tMisses: {self.total_misses}\n\tMiss Rate: {miss_rate}%"
        print(self.result_str)
    
    def access (self, ls ,address):
        """
        """
        # Se separa el address en offset, index y tag
        offset =int(address%(2 **self.byte_offset_size ))
        index_ =int(floor(address/(2 **self.byte_offset_size ))%(2 **self.index_size ))
        tag =int(floor(address/(2 **(self.byte_offset_size +self.index_size))))

        # Se busca el tag en la cache
        isFound =self.find(index_ ,tag )
        result =False 

        # Si no se encuentra el tag en la cache se guarda en la cache
        if isFound ==-1 :
            self.bring_to_cache(index_ ,tag )
            self.total_misses +=1 
            if ls ==0:
                self.total_read_misses +=1 
            else :
                self.total_write_misses +=1 
            result =True 
        else:
            # Si se encuentra el tag en la cache se actualiza la tabla de reemplazo con politica LRU
            index_to_replace = self.tag_table[index_].index(tag)
            self.replace_table[index_].remove(index_to_replace)
            self.replace_table[index_].insert(0, index_to_replace)
            
        
        # Se incrementan los contadores de accesos
        self.total_access +=1 
        if ls ==0:
            self.total_reads +=1 
        else:
            self.total_writes +=1 
        return result 
    
    def find (self, index_ ,tag ):
        """
        """
        # Se busca el tag en el set indicado por el index, si se encuentra se retorna el indice de la cache, si no, se retorna -1
        for cache_index in range(self.cache_assoc):
            if self.valid_table[index_][cache_index] and (self.tag_table[index_][cache_index]==tag ):
                return cache_index 
        return -1 
    
    def bring_to_cache (self, index_ ,value ):
        """
        """
        # Se busca un espacio en la cache para guardar el tag
        # Se victimiza el indice menos untilizado
        index_to_replace = self.replace_table[index_][self.cache_assoc-1]
        self.replace_table[index_].remove(index_to_replace)
        self.replace_table[index_].insert(0, index_to_replace)
        self.valid_table[index_][index_to_replace]=True 
        self.tag_table[index_][index_to_replace]=value 

    def save_results (self, filename, trace):
        """
        """
        # Se abre un archivo para guardar los resultados, se escribe la información de la simulación y se cierra el archivo (se guarda en modo append)
        f =open (filename ,'a')
        f.write(f"{trace},{self.name},{self.cache_capacity},{self.cache_assoc},{self.block_size},{self.repl_policy},{self.result_str}\n")
        f.close () 