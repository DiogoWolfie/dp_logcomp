
#classe Symbol Table
class SymbolTable():
    def __init__(self):
       self._table = {}

    def get(self,name):
        if name in self._table:
            return self._table[name] #retorna a tupla
        else:
            raise ValueError(f"variável {name} não está definida")
        
    #var x int
    def create(self, name, type):
        if name in self._table:
            raise ValueError(f"Variável '{name}' já foi declarada")
        self._table[name] = (type, None)

    #x = 3
    def set(self,name, value):
        if name not in self._table:
            raise ValueError(f"Variável '{name}' não foi declarada")
        type, _ = self._table[name]
        self._table[name] = (type, value)

    def get_type(self, name):
        type, _ = self._table[name]
        return type