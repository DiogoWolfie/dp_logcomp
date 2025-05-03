from ast.node import Node

#NoAt - Nó de atribuição = só escreve na symbol table, logo o identifier é realmente apenas uma string
#estou considerando que ess enó só vai exisitir depois do nó varnode (var x int)
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
           
    def Generate(self, SymbolTable):
        valor_code = self.valor.Generate(SymbolTable)
        if valor_code is None:
            raise ValueError("Erro interno: valor da atribuição retornou None em Generate()")

        offset = SymbolTable.get_offset(self.identifier)
        return f"""
            {valor_code}
            mov [ebp - {offset}], eax
        """
    