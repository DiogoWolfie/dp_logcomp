from ast.node import Node

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

        if not hasattr(func_node, "params") or not hasattr(func_node, "block"):
            raise ValueError(f"{self.name} não é uma função válida")

        if len(self.args) != len(func_node.params):
            raise ValueError(f"Número incorreto de argumentos para a função '{self.name}'")

        local_table = symbol_table.__class__(parent=symbol_table)  # nova SymbolTable encadeada

        for param, arg in zip(func_node.params, self.args):
            tipo_arg, valor_arg = arg.Evaluate(symbol_table)
            local_table.create(param.value, tipo_arg)
            local_table.set(param.value, valor_arg)

        # Avalia o bloco e captura o retorno
        result = func_node.block.Evaluate(local_table)

        # Se a função tem tipo de retorno, verifica o tipo
        if func_node.return_type and func_node.return_type.value != "void":
            if result is None:
                raise ValueError(f"Função {self.name} deve retornar um valor")

            # Obtém o tipo do resultado
            if isinstance(result, tuple):
                result_type, result_value = result
            else:
                result_type = map_python_type(result)
                result_value = result

            # Verifica compatibilidade
            if func_node.return_type.value != result_type:
                raise ValueError(
                    f"Tipo de retorno incompatível em {self.name}: esperado {func_node.return_type.value}, obtido {result_type}"
                )

            return (result_type, result_value) if isinstance(result, tuple) else result

        return None

    def Generate(self, symbol_table):
        # Implementar geração de código depois
        pass
