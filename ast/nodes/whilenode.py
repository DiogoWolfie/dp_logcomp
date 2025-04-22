from ast.node import Node

class WhileNode(Node): 
    def __init__(self, condition, block):
        super().__init__("while", [condition, block])
        self.condition = condition
        self.block = block

    def Evaluate(self, SymbolTable):
        while True:
            _, cond_value = self.condition.Evaluate(SymbolTable)  # Reavalia a cada iteração
            if not cond_value:  # Se condição for falsa, sai do loop
                break
            self.block.Evaluate(SymbolTable)
        return None

