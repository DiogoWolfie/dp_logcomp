from ast.node import Node

#BinOp - Operações binárias
class BinOp(Node):
    def __init__(self, value, children_left, children_right):
        super().__init__(value, [children_left,children_right])
    
    def Evaluate(self, SymbolTable):
        tipo1, val1 = self.children[0].Evaluate(SymbolTable)
        tipo2, val2 = self.children[1].Evaluate(SymbolTable)
        
        if tipo1 == "int" and tipo2 == "int":
            if self.value == 'PLUS':
                return ("int", val1 + val2)
            elif self.value == 'MINUS':
                return ("int", val1 - val2)
            elif self.value == 'MULT':
                return ("int", val1 * val2)
            elif self.value == 'DIV':
                return ("int", val1 // val2) # Divisão inteira
            elif self.value == "EQUAL_EQUAL":
                return ("bool", val1 == val2)
            elif self.value == "LESS":
                return ("bool", val1 < val2)
            elif self.value == "GREATER":
                return ("bool", val1 > val2)
        
        elif tipo1 =="bool" and tipo2 == "bool":
            if self.value == "AND":
                return ("bool", val1 and val2)
            elif self.value == "OR":
                return ("bool", val1 or val2)
            elif self.value == "EQUAL_EQUAL":
                return ("bool", val1 == val2)
        
        elif tipo1 =="string" and tipo2 == "string":
            if self.value == "PLUS":
                return ("string", str(val1) + str(val2))
            elif self.value == "LESS":
                return ("bool", val1 < val2)
            elif self.value == "GREATER":
                return ("bool", val1 > val2)
            elif self.value == "EQUAL_EQUAL":
                return ("bool", val1 == val2)
        
        elif (tipo1 == 'int' and tipo2 == "string") or (tipo2 == 'int' and tipo1 == "string") or (tipo1 == 'bool' and tipo2 == "string") or (tipo2 == 'bool' and tipo1 == "string"):
            if self.value == "PLUS":
                return ("string", str(val1) + str(val2))
            elif self.value == "LESS":
                return ("bool", val1 < val2)
            elif self.value == "GREATER":
                return ("bool", val1 > val2)
        
        raise ValueError(f"Operador binário desconhecido: {self.value}")
    
    def Generate(self, st):
        right_code = self.children[1].Generate(st)
        left_code = self.children[0].Generate(st)

        if self.value == "PLUS":
            return f"""
                    {right_code}
                    push eax;
                    {left_code}
                    pop ecx; 
                    add eax, ecx; binop para soma
                    """
        elif self.value == "MINUS":
            return f"""
                    {right_code}
                    push eax;
                    {left_code}
                    pop ecx; 
                    sub eax, ecx; binop para subtração
                    """
        elif self.value == "MULT":
            return f"""
                    {right_code}
                    push eax;
                    {left_code}
                    pop ecx; 
                    imul eax, ecx; binop para multiplicação
                    """
        elif self.value == "DIV":
            return f"""
                    {right_code}
                    push eax;
                    {left_code}
                    pop ecx;
                    cdq; Estende sinal de eax para edx:eax, divisao so funciona com edx
                    idiv ecx; binop para divisão
                    """
        
        elif self.value == "EQUAL_EQUAL":
            return f"""
                    {right_code}
                    push eax;
                    {left_code}
                    pop ecx;
                    cmp eax, ecx;
                    mov ecx, 1;
                    mov eax, 0;
                    cmove eax, ecx;
                    """
        elif self.value == "GREATER":
            return f"""
                    {right_code}
                    push eax;
                    {left_code}
                    pop ecx;
                    cmp eax, ecx;
                    mov ecx, 1;
                    mov eax, 0;
                    cmovg eax, ecx;
                    """
        elif self.value == "LESS":
            return f"""
                    {right_code}
                    push eax;
                    {left_code}
                    pop ecx;
                    cmp eax, ecx;
                    mov ecx, 1;
                    mov eax, 0;
                    cmovl eax, ecx;
                    """