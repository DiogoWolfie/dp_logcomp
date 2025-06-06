from ast.node import Node
from ast.nodes.funcdec import FuncDec

class FuncCall(Node):
    def __init__(self, name, args):
        super().__init__(name, args)
        self.name = name
        self.args = args

    def Evaluate(self, SymbolTable):
        func_type, func_node = SymbolTable.get(self.name)
        # talvez devo checar se func_node é realmente uma função 
      
        if not hasattr(func_node, "params") or not hasattr(func_node, "block"):
            raise ValueError(f"{self.name} não é uma função")
        if len(self.args) != len(func_node.params):
            raise ValueError("Número de argumentos incorreto")
        # Cria nova SymbolTable encadeada
        local_table = SymbolTable(parent=SymbolTable)
        # Atribui argumentos
        for param, arg in zip(func_node.params, self.args):
            tipo, valor = arg.Evaluate(SymbolTable)
            local_table.create(param.value, tipo)
            local_table.set(param.value, valor)
        # Executa bloco
        result = func_node.block.Evaluate(local_table)
        # Compara tipo de retorno
        if func_node.return_type and func_node.return_type.value != "void":
            if isinstance(result, tuple):
                result_type, _ = result
            else:
                result_type = type(result).__name__
            if func_node.return_type.value != result_type:
                raise ValueError(f"Tipo de retorno incompatível em {self.name}: esperado {func_node.return_type.value}, obtido {result_type}")
            return result
        return None