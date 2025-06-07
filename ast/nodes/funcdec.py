from ast.node import Node

class FuncDec(Node):
    def __init__(self, name, params, return_type, block):
        super().__init__(name, [*params, block])
        self.name = name
        self.params = params
        self.return_type = return_type
        self.block = block

    def Evaluate(self, symbol_table):
        # 1. Registra a função na tabela global
        symbol_table._table[self.name] = (
            self.return_type.value if self.return_type else "void",
            self,
            None
        )

        # 2. Cria novo escopo local para a função
        local_table = symbol_table.__class__(parent=symbol_table)

        # 3. Adiciona parâmetros na symbol table local
        for param in self.params:
            param.Evaluate(local_table)

        # 4. Avalia o corpo da função com a tabela local
        #self.block.Evaluate(local_table)

        return None


    def Generate(self, symbol_table):
        pass
