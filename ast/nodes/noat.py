from ast.node import Node

#NoAt - Nó de atribuição = só escreve na symbol table, logo o identifier é realmente apenas uma string
#estou considerando que ess enó só vai exisitir depois do nó varnode (var x int)
class NoAt(Node):
    def __init__(self, name, expr):
        super().__init__(name, [expr])
        self.name = name
    def Evaluate(self, SymbolTable):
        tipo, valor = self.children[0].Evaluate(SymbolTable)
        var_tipo = SymbolTable.get_type(self.name)
        
        if tipo != var_tipo:
            raise ValueError(f"Tipo declarado diferente do tipo do atribuido")
        SymbolTable.set(self.name, valor)
        return None
           
    def Generate(self, SymbolTable):
        valor_code = self.valor.Generate(SymbolTable)
        offset = SymbolTable.get_offset(self.identifier)
        return f"""
            {valor_code}
            mov [ebp - {offset}], eax
        """
    