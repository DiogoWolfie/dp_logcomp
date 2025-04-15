from ast.node import Node

#NoBlc- nó do bloco
class NoBlc(Node):
    def __init__(self, children):
        super().__init__(None,children)

    def Evaluate(self, SymbolTable):
        result = None
        for c in self.children:
            result = c.Evaluate(SymbolTable)
        return result