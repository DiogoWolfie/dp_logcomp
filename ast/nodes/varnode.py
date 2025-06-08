from ast.node import Node

class VarNode(Node):
    def __init__(self, name, tipo):
        super().__init__(name, [])
        self.name = name
        self.tipo = tipo
    def Evaluate(self, SymbolTable):
        SymbolTable.create(self.name, self.tipo.value if hasattr(self.tipo, "value") else self.tipo)
        return None
    
    def Generate(self, SymbolTable):
        SymbolTable.create(self.value, self.type)
        offset = SymbolTable.get_offset(self.value)
        return f"""
            sub esp, 4;
            mov dword [ebp - {offset}], 0;
            """