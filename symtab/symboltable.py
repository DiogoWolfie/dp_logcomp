
#classe Symbol Table
class SymbolTable():
    def __init__(self, parent=None):
       self._table = {}
       self._parent = parent
       self._current_offset = 0 #para pegar o slato da memória

    def get(self,name):
        if name in self._table:
            
            return self._table[name] #retorna a tupla
        elif self._parent:
            
            return self._parent.get(name)
        else:
            raise ValueError(f"variável {name} não está definida")
        
    #var x int
    def create(self, name, tipo):
        if name in self._table:
            raise ValueError(f"Variável '{name}' já foi declarada")
        self._current_offset += 4
        self._table[name] = (tipo, 0, self._current_offset)

    #x = 3
    def set(self,name, value):
        if name in self._table:
            type, _, offset = self._table[name]
            self._table[name] = (type, value, offset)
        elif self._parent:
            self._parent.set(name, value)
        else:
            raise ValueError(f"Variável '{name}' não foi declarada")

    def get_type(self, name):
        if name in self._table:
            type, _, _ = self._table[name]
            return type
        elif self._parent:
            return self._parent.get_type(name)
        else:
            raise ValueError(f"Variável '{name}' não foi declarada")

    def get_offset(self, name):
        if name in self._table:
            _, _, offset = self._table[name]
            return offset
        elif self._parent:
            return self._parent.get_offset(name)
        else:
            raise ValueError(f"Variável '{name}' não foi declarada")
        
    def create_function(self, name, func_node):
        if name in self._table:
            raise ValueError(f"Função '{name}' já foi declarada")
        # Armazena: (tipo de retorno, nó da função, None)
        return_type = func_node.return_type.value if func_node.return_type else "void"
        self._table[name] = (return_type, func_node, None)