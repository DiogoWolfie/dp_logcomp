from ast.node import Node

#NoAt - Nó de atribuição = só escreve na symbol table, logo o identifier é realmente apenas uma string
class NoAt(Node):
    def __init__(self, identifier, children):
        super().__init__(None, children)  # valor semântico pode ser None
        self.identifier = identifier     # <--- AQUI está o fix

    def Evaluate(self, SymbolTable):
        SymbolTable.set(self.identifier, self.children.Evaluate(SymbolTable))
        return None