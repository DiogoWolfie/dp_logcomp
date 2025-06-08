from ast.node import Node
from ast.nodes.funcdec import FuncDec
from ast.nodes.varnode import VarNode
from ast.nodes.returnnode import ReturnNode


class NoBlc(Node):
    def __init__(self, children, is_func_block=False):
        super().__init__(None, children)
        self.is_func_block = is_func_block

    def Evaluate(self, SymbolTable):
        # Não cria novo escopo se for bloco de função
        if self.is_func_block or SymbolTable._parent is None:
            local_table = SymbolTable
        else:
            local_table = SymbolTable.__class__(parent=SymbolTable)
            # Propaga o tipo de retorno esperado, se existir
            if hasattr(SymbolTable, "_expected_return_type"):
                local_table._expected_return_type = SymbolTable._expected_return_type
        for child in self.children:
            child.Evaluate(local_table)
        return None
            
    def Generate(self, st):
        code = ""
        for child in self.children:
            code += str(child.Generate(st))
        return code