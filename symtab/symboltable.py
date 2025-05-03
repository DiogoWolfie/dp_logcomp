
#classe Symbol Table
class SymbolTable():
    def __init__(self):
       self._table = {}
       self._current_offset = 0 #para pegar o slato da memória

    def get(self,name):
        if name in self._table:
            return self._table[name] #retorna a tupla
        else:
            raise ValueError(f"variável {name} não está definida")
        
    #var x int
    def create(self, name, type):
        if name in self._table:
            raise ValueError(f"Variável '{name}' já foi declarada")
        self._current_offset += 4
        self._table[name] = (type, 0, self._current_offset) #definindo valor inicial como zero para evitar lixo de memória

    #x = 3
    def set(self,name, value):
        if name not in self._table:
            raise ValueError(f"Variável '{name}' não foi declarada")
        type, _, offset = self._table[name]
        self._table[name] = (type, value, offset)

    def get_type(self, name):
        type, _ = self._table[name]
        return type

    def get_offset(self, name):
        _, _, offset = self._table[name]
        return offset