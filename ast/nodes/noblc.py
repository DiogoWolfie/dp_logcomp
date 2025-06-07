from ast.node import Node
from ast.nodes.funcdec import FuncDec
from ast.nodes.varnode import VarNode
from ast.nodes.returnnode import ReturnNode


class NoBlc(Node):
    def __init__(self, children):
        super().__init__(None, children)

    # def Evaluate(self, SymbolTable):
    #     for child in self.children:
    #         # Se o filho é um ReturnNode, avalia e retorna imediatamente
    #         if isinstance(child, ReturnNode):
    #             return child.Evaluate(SymbolTable)
            
    #         # Caso contrário, avalia normalmente
    #         result = child.Evaluate(SymbolTable)
            
    #         # Se a avaliação do filho retornar um valor (ex.: chamada de função com return),
    #         # interrompe o bloco e propaga o resultado
    #         if result is not None:
    #             return result
   
    def Evaluate(self, SymbolTable):
        for child in self.children:
            child.Evaluate(SymbolTable)
        return None
            
    def Generate(self, st):
        code = ""
        for child in self.children:
            code += str(child.Generate(st))
        return code