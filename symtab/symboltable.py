
#classe Symbol Table
class SymbolTable():
    def __init__(self):
       self._table = {}

    def get(self,name):
        if name in self._table:
            return self._table[name]
        else:
            raise ValueError(f"variável {name} não está definida")
      
    def set(self,name,value):
        self._table[name]= value