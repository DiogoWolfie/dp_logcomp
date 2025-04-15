#criar um nó par ao if em go
from ast.node import Node

class IfNode(Node):
    def __init__(self, condition, block, else_block=None):
        super().__init__("if", [condition, block, else_block])
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def Evaluate(self, SymbolTable):
        if self.condition.Evaluate(SymbolTable):
            self.block.Evaluate(SymbolTable)
        elif self.else_block is not None:
            self.else_block.Evaluate(SymbolTable)
        return None