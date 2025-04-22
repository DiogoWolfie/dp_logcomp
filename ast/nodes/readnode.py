from ast.node import Node

class ReadNode(Node):
    def __init__(self):
        super().__init__(None, [])
    
    def Evaluate(self, st):
        # Lê do terminal e converte para inteiro
        return ("int",int(input()))