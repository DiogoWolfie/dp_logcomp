from ast.node import Node

#NoPrt - nó do print
class NoPrt(Node):
    def __init__(self, children):
        super().__init__(None, children)
    def Evaluate(self, SymbolTable):
        children = self.children if isinstance(self.children, list) else [self.children]
        for child in children:
            result = child.Evaluate(SymbolTable)
            if isinstance(result, tuple):
                if len(result) == 3:
                    _, valor, _ = result
                elif len(result) == 2:
                    _, valor = result
                else:
                    valor = result
            else:
                valor = result
            print(str(valor).lower())
        return None
    
    def Generate(self, st):
        return f"""
            {self.children.Generate(st)}
            push eax ; Empilha os argumentos para chamar a funcao
            push format_out ; Dizendo para o printf que é um inteiro
            call printf ; Chamada da função
            add esp, 8 ; Remove os argumentos da pilha"""