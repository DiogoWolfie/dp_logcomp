from ast.node import Node

#NoOp - sem operaação
class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])
    def Evaluate(self, SymbolTable):
        pass
    def Generate(self, SymbolTable):
        return "; noop"