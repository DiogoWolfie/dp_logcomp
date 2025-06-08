from ast.node import Node
from ast.nodes.noid import NoId

class DeclaracaoComValor(Node):
    def __init__(self, name, expr, tipo):
        super().__init__("DECLARACAO_COM_VALOR", [NoId(name), expr])
        self.name = name
        self.tipo = tipo

    def Evaluate(self, SymbolTable):
        tipo_valor, valor = self.children[1].Evaluate(SymbolTable)
        tipo_esperado = self.tipo.value if hasattr(self.tipo, "value") else self.tipo
        if tipo_valor != tipo_esperado:
            raise ValueError("Tipo declarado diferente do tipo do atribuido")
        SymbolTable.create(self.name, tipo_esperado)
        SymbolTable.set(self.name, valor)
        return (tipo_valor, valor)

    def Generate(self, SymbolTable):
        pass