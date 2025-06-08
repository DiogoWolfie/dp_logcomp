#criar um nó par ao if em go
from ast.node import Node

class IfNode(Node):
    def __init__(self, condition, block, else_block=None):
        super().__init__("if", [condition, block, else_block])
        self.condition = condition
        self.block = block
        self.else_block = else_block

    def Evaluate(self, SymbolTable):
        tipo, cond = self.condition.Evaluate(SymbolTable)

        if tipo != "bool":
            raise TypeError("A condição do if deve ser booleana")

        if cond:
            self.block.Evaluate(SymbolTable)
        elif self.else_block:
            self.else_block.Evaluate(SymbolTable)

        return None

    def Generate(self, st):
        
        else_label = f"else_{self.id}"
        end_label = f"endif_{self.id}"

        cond_code = self.condition.Generate(st)
        then_code = self.block.Generate(st)
        else_code = self.else_block.Generate(st) if self.else_block else ""

        return f"""
            {cond_code}
            cmp eax, 0
            je {else_label}
            {then_code}
            jmp {end_label}
            {else_label}:
            {else_code}
            {end_label}:"""
        
