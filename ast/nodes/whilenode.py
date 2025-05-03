from ast.node import Node

class WhileNode(Node): 
    def __init__(self, condition, block):
        super().__init__("while", [condition, block])
        self.condition = condition
        self.block = block

    def Evaluate(self, SymbolTable):
        while True:
            cond_type, cond_value = self.condition.Evaluate(SymbolTable)  # Reavalia a cada iteração
            if cond_type != "bool":  # Verificação crucial
                raise ValueError(f"condição do for deve ser bool, encontrado {cond_type}")
            if not cond_value:  # Se condição for falsa, sai do loop
                break
            self.block.Evaluate(SymbolTable)
        return None

    def Generate(self, st):
        if self.id is None:
            print(f"[ERRO] Nó {type(self).__name__} está com id=None")
        start_label = f"loop_{self.id}"
        end_label = f"exit_{self.id}"

        cond_code = self.condition.Generate(st)
        block_code = self.block.Generate(st)

        return f"""
        {start_label}:
            {cond_code}
            cmp eax, 0
            je {end_label}
            {block_code}
            jmp {start_label}
        {end_label}:"""
