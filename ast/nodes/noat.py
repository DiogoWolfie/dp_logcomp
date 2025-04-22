from ast.node import Node

#NoAt - Nó de atribuição = só escreve na symbol table, logo o identifier é realmente apenas uma string
class NoAt(Node):
    def __init__(self, identifier, valor):
        super().__init__(None, []) 
        self.identifier = identifier     
        self.valor = valor

    def Evaluate(self, SymbolTable):
        
        tipo, val = self.valor.Evaluate(SymbolTable)
        tipo_na_tabela = SymbolTable.get_type(self.identifier)
        if tipo != tipo_na_tabela:
            raise ValueError("tipo declarado diferente do tipo do atribuido")
        else:
            SymbolTable.set(self.identifier, val)
        return None
           