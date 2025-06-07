from ast.node import Node
from RTE.RTE import ReturnException

class ReturnNode(Node):
    def __init__(self, expr):
        super().__init__("return", [expr])
        self.expr = expr

    def Evaluate(self, SymbolTable):
        if self.expr:
            result = self.expr.Evaluate(SymbolTable)
            if isinstance(result, tuple) and len(result) == 2:
                type_, value = result  # <-- tipo primeiro, valor depois
            else:
                value = result
                if isinstance(value, int):
                    type_ = "int"
                elif isinstance(value, str):
                    type_ = "string"
                elif isinstance(value, bool):
                    type_ = "bool"
                elif value is None:
                    type_ = "void"
                else:
                    type_ = "unknown"
        else:
            value = None
            type_ = "void"
        raise ReturnException(type_, value)
    
    def Generate(self, SymbolTable):
        pass