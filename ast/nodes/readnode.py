from ast.node import Node

class ReadNode(Node):
    def __init__(self):
        super().__init__(None, [])
    
    def Evaluate(self, st):
        # Lê do terminal e converte para inteiro
        return ("int",int(input()))
    
    def Generate(self, st):
        return """
            ;Geracao do scan()
            push scan_int
            push format_in
            call scanf
            add esp, 8
            mov eax, [scan_int]"""