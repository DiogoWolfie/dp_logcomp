from ast.node import Node
from ast.nodes.returnnode import ReturnNode
#NoBlc- nó do bloco
class NoBlc(Node):
    def __init__(self, children):
        super().__init__(None,children)

    def Evaluate(self, SymbolTable):
        result = None
        for c in self.children:
            result = c.Evaluate(SymbolTable)
            if isinstance(c, ReturnNode):
                return result
        return result
    
    def Generate(self, st):
        code = ""
        for child in self.children:
            code += str(child.Generate(st))
        return code