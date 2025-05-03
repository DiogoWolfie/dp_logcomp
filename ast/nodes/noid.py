from ast.node import Node

#NoId - identificador / variável
class NoId(Node):
    def __init__(self, value):
        super().__init__(value, [])
    
    def Evaluate(self, SymbolTable):
        return SymbolTable.get(self.value)
    
    def Generate(self, st):
        offset = st.get_offset(self.value)
        return f"mov eax, [ebp - {offset}]; generate no identificador"