from ast.node import Node

#NoPrt - nó do print
class NoPrt(Node):
    def __init__(self, children):
        super().__init__(None,children)
    def Evaluate(self, SymbolTable):
        tipo, valor = self.children.Evaluate(SymbolTable)
        return print(valor)