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
        if len(self.args) != len(func_node.params):
            raise ValueError(f"Número de argumentos errado para função '{self.name}'")
        
        local_table = symbol_table.__class__(parent=symbol_table)

        # Cria e define os parâmetros na tabela local
        for param, arg in zip(func_node.params, self.args):
            tipo_arg, valor_arg = arg.Evaluate(symbol_table)
            tipo_param = param.tipo if hasattr(param, "tipo") else param
            tipo_param = tipo_param.value if hasattr(tipo_param, "value") else tipo_param
            if tipo_arg != tipo_param:
                raise ValueError(f"Tipo de argumento errado em '{self.name}': esperado {tipo_param}, recebido {tipo_arg}")
            local_table.create(param.value, param.tipo if hasattr(param, "tipo") else tipo_arg)
            local_table.set(param.value, valor_arg)

        # Injeta o tipo de retorno esperado para o ReturnNode
        local_table._expected_return_type = func_node.return_type.value if func_node.return_type else "void"

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