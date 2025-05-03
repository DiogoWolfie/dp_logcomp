from ast.node import Node

class ReadNode(Node):
    def __init__(self):
        super().__init__(None, [])
    
    def Evaluate(self, st):
        # Lê do terminal e converte para inteiro
        return ("int",int(input()))
    
    def Generate(self, st):
        return f"""
                ; Scanln
                push scan_int ; endereço de memória de suporte
                push format_in ; formato de entrada (int)
                call scanf
                add esp, 8 ; Remove os argumentos da pilha
                mov eax, dword [scan_int] ; retorna o valor lido em EAX"""