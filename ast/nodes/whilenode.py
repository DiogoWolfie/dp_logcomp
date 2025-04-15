from ast.node import Node

class WhileNode(Node): 
    def __init__(self, condition, block):
        super().__init__("while", [condition, block])
        self.condition = condition
        self.block = block

    def Evaluate(self, SymbolTable):
        while self.condition.Evaluate(SymbolTable):
            self.block.Evaluate(SymbolTable)
        return None