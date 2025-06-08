from ast.node import Node



class FuncDec(Node):
    def __init__(self, name, params, return_type, block):
        super().__init__(name, [*params, block])
        self.name = name
        self.params = params
        self.return_type = return_type
        self.block = block
    def Evaluate(self, SymbolTable):
        SymbolTable.create_function(self.name, self)
        return None


    def Generate(self, symbol_table):
        pass
