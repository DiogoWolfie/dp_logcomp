from ast.node import Node

#UnOp - Operação unária
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, SymbolTable):
        if self.value == "+":
            return self.children.Evaluate(SymbolTable)
        elif self.value == "-":
            return -self.children.Evaluate(SymbolTable)
        elif self.value == "!":
            return not self.children.Evaluate(SymbolTable) #booleano