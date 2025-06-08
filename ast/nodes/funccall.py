from ast.node import Node
from RTE.RTE import ReturnException

def map_python_type(value):
    if isinstance(value, int):
        return "int"
    if isinstance(value, str):
        return "string"
    if isinstance(value, bool):
        return "bool"
    if value is None:
        return "void"
    return "unknown"

class FuncCall(Node):
    def __init__(self, name, args):
        super().__init__(name, args)
        self.name = name
        self.args = args

    def Evaluate(self, symbol_table):
        tipo, func_node, _ = symbol_table.get(self.name)
        local_table = symbol_table.__class__(parent=symbol_table)

        # Cria e define os parâmetros na tabela local
        for param, arg in zip(func_node.params, self.args):
            tipo_arg, valor_arg = arg.Evaluate(symbol_table)
            local_table.create(param.value, param.tipo if hasattr(param, "tipo") else tipo_arg)
            local_table.set(param.value, valor_arg)

        try:
            func_node.block.Evaluate(local_table)
            # Só exige return se não for void
            if func_node.return_type and func_node.return_type.value != "void":
                raise ValueError(f"Função {self.name} deve retornar um valor")
            return ("void", None)
        except ReturnException as ret:
            result_type = ret.type
            result_value = ret.value

        if func_node.return_type and func_node.return_type.value != result_type:
            raise ValueError(
                f"Tipo de retorno incompatível em {self.name}: esperado {func_node.return_type.value}, obtido {result_type}"
            )
        return (result_type, result_value)

    def Generate(self, symbol_table):
        # Implementar geração de código depois
        pass