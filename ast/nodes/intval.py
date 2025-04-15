from ast.node import Node

#IntVal - Valor inteiro - não tem filho
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])
    
    def Evaluate(self, SymbolTable):
        return self.value