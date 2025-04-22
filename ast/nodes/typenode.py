from ast.node import Node
class TypeNode(Node):
    def __init__(self, value):
        super().__init__(value,[])
    def Evaluate(self, SymbolTable):
        return ("type", self.value)