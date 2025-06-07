from ast.node import Node

#String node, nó da string
class StrNode(Node):
    def __init__(self, value):
        super().__init__(value, [])
    
    def Evaluate(self, SymbolTable):
        return ("string", str(self.value))
    def Generate(self, SymbolTable):
        pass