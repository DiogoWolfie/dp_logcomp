from ast.node import Node

#NoAt - Nó de atribuição = só escreve na symbol table, logo o identifier é realmente apenas uma string
class NoAt(Node):
    def __init__(self, identifier, tipo, valor):
        super().__init__(None, [tipo,valor]) 
        self.identifier = identifier     
        self.tipo = tipo 
        self.valor = valor

    def Evaluate(self, SymbolTable):
        
        tipo = self.tipo.Evaluate(SymbolTable)
        valor = self.valor.Evaluate(SymbolTable)

        if tipo[1] != valor[0]:
            raise ValueError(f"Erro de tipo: {tipo[0]} não é igual a {valor[0]}")
        else:
            SymbolTable.create(self.identifier, tipo[1])
            SymbolTable.set(self.identifier, valor[1])
            return None