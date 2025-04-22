from ast.node import Node

class BoolVal(Node):
    def __init__(self, value):
        super().__init__(value,[])
    def Evaluate(self, SymbolTable):
        return ("bool", bool(self.value))
    