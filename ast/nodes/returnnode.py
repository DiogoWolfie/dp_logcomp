from ast.node import Node

class ReturnNode(Node):
    def __init__(self, expr):
        super().__init__("return", [expr])
        self.expr = expr

    def Evaluate(self, SymbolTable):
        return self.expr.Evaluate(SymbolTable)
    
    def Generate(self, SymbolTable):
        pass