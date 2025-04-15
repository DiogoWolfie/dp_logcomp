from ast.node import Node

#NoId - identificador / variável
class NoId(Node):
    def __init__(self, value):
        super().__init__(value, [])
    
    def Evaluate(self, SymbolTable):
        return SymbolTable.get(self.value)