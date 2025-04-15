# from ast.node import Node
# #preciso construir um nó par ao read em go	

# class ReadNode(Node):
#     def __init__(self, variable):
#         super().__init__("read", [variable])
#         self.variable = variable

#     def Evaluate(self, SymbolTable):
#         # Read a value from the input and store it in the variable
#         value = input(f"Enter value for {self.variable.name}: ")
#         SymbolTable.SetValue(self.variable.name, value)
#         return None
from ast.node import Node

class ReadNode(Node):
    def __init__(self):
        super().__init__(None, [])
    
    def Evaluate(self, st):
        # Lê do terminal e converte para inteiro
        return int(input("> "))