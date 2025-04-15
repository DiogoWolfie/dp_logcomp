from ast.node import Node

#BinOp - Operações binárias
class BinOp(Node):
    def __init__(self, value, children_left, children_right):
        super().__init__(value, [children_left,children_right])
    
    def Evaluate(self, SymbolTable):
        if self.value == 'PLUS':
            return self.children[0].Evaluate(SymbolTable) + self.children[1].Evaluate(SymbolTable)
        elif self.value == 'MINUS':
            return self.children[0].Evaluate(SymbolTable) - self.children[1].Evaluate(SymbolTable)
        elif self.value == 'MULT':
            return self.children[0].Evaluate(SymbolTable) * self.children[1].Evaluate(SymbolTable)
        elif self.value == 'DIV':
            return self.children[0].Evaluate(SymbolTable) / self.children[1].Evaluate(SymbolTable)
        elif self.value == "EQUAL_EQUAL":
            return self.children[0].Evaluate(SymbolTable) == self.children[1].Evaluate(SymbolTable) #retorna booleano
        elif self.value == "LESS":
            return self.children[0].Evaluate(SymbolTable) < self.children[1].Evaluate(SymbolTable)
        elif self.value == "GREATER":
            return self.children[0].Evaluate(SymbolTable) > self.children[1].Evaluate(SymbolTable)
        elif self.value == "AND":
            return self.children[0].Evaluate(SymbolTable) and self.children[1].Evaluate(SymbolTable)
        elif self.value == "OR":
            return self.children[0].Evaluate(SymbolTable) or self.children[1].Evaluate(SymbolTable)
        