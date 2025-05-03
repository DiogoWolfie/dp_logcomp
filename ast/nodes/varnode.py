from ast.node import Node

class VarNode(Node):
    def __init__(self, value, type):
        super().__init__(value,[])
        self.value = value
        self.type = type
    def Evaluate(self, SymbolTable):
        _,tipo  = self.type.Evaluate(SymbolTable)
        SymbolTable.create(self.value, tipo)
        return None
    
    def Generate(self, SymbolTable):
        SymbolTable.create(self.value, self.type)
        offset = SymbolTable.get_offset(self.value)
        return f"""
            sub esp, 4
            mov dword [ebp - {offset}], 0"""