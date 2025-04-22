from ast.node import Node

#UnOp - Operação unária
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, SymbolTable):
        tipo, val = self.children.Evaluate(SymbolTable)
        if tipo == "int":
            if self.value == "+":
                return ("int",val)
            elif self.value == "-":
                return ("int",-val)
            elif self.value == "!":
                raise ValueError("Operador '!' não pode ser aplicado a um inteiro")
        elif tipo == "bool":
            if self.value == "+":
                raise ValueError("Operador '+' não pode ser aplicado a um booleano")
            elif self.value == "-":
                raise ValueError("Operador '-' não pode ser aplicado a um booleano")
            elif self.value == "!":
                return ("bool",not val)