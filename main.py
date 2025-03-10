import sys
from abc import ABC, abstractmethod

#classe token/palavra
#será definida pelo seu tipo e seu valor
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

#classe de pré-processamento - retirar comentários (// no go)
class PrePro:
    def __init__(self, source):
        self.source = source
        self.filtered_source = self.filter()

    def filter(self):
        lines = self.source.split("\n")  # Divide em linhas
        clean_lines = []
        
        for line in lines:
            if "//" in line:
                line = line.split("//")[0]  
            clean_lines.append(line.strip())  

        return "\n".join(clean_lines)  
    

#classe de tokenização - análise léxica
class Tokenizer:
    def __init__(self, source):
        self.source = source #código fonte
        self.position = 0 #posição atual que o tokenizer está separando
        self.next = None #o último token separado
        self.selectNext()

    def selectNext(self):

        #iginora todos os espaços em branco
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1 

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        current_char = self.source[self.position]

        if current_char.isdigit():
            value = 0
            while self.position < len(self.source) and self.source[self.position].isdigit():
                value = value * 10 + int(self.source[self.position])
                self.position += 1
            self.next = Token("NUMBER", value)
            return
            
        elif current_char == '+':
            self.next = Token("PLUS", current_char)
            self.position += 1
            return

        elif current_char == '-':
            self.next = Token("MINUS", current_char)
            self.position += 1
            return
        
        elif current_char == '*':
            self.next = Token("MULT", current_char)
            self.position+=1
            return
        
        elif current_char == '/':
            self.next = Token("DIV", current_char)
            self.position+=1
            return
        
        elif current_char == "(":
            self.next = Token("OPEN_PAR",current_char)
            self.position+=1

        elif current_char == ")":
            self.next = Token("CLOSE_PAR", current_char)
            self.position+=1

        else:
            raise ValueError(f"Token inesperado: {current_char}")
        

"""AST - Abstract Syntax Tree"""
class Node(ABC):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self):
        pass
        
    pass

#BinOp - Operações binárias
class BinOp(Node):
    def __init__(self, value, children_left, children_right):
        super().__init__(value, [children_left,children_right])
    
    def Evaluate(self):
        if self.value == 'PLUS':
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == 'MINUS':
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == 'MULT':
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == 'DIV':
            return self.children[0].Evaluate() / self.children[1].Evaluate()
        

#UnOp - Operação unária
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, [children])
    
    def Evaluate(self):
        if self.value == "+":
            return self.children[0].Evaluate()
        elif self.value == "-":
            return -self.children[0].Evaluate()

#IntVal - Valor inteiro - não tem filho
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])
    
    def Evaluate(self):
        return self.value
    
#NoOp - sem operaação
class NoOp(Node):
    def __init__(self):
        super().__init__(0, [])
    def Evaluate(self):
        pass
    
"""Fim da AST"""


#análise sintática - checa a ordem das palavras
#talvez eu precise colocar um check aqui para o caso do próximo valor depois de um número seja um número tbm sem 
class Parser():
    tokenizer = None

    @staticmethod
    def factorExpression() -> Node:
        token = Parser.tokenizer.next  
        Parser.tokenizer.selectNext()

        if token.type == "NUMBER":
            return IntVal(token.value) 
        
        elif token.value == "+":  
            return UnOp("+", [Parser.factorExpression()])

        elif token.value == "-":
            return UnOp("-", [Parser.factorExpression()])

        elif token.value == "(":
            result = Parser.parseExpression()
            if Parser.tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("Parênteses não foi fechado")
            Parser.tokenizer.selectNext()  # Consumir `)`
            return result
        
        else:
            raise ValueError("Erro de entrada")

    @staticmethod
    def termExpression() -> Node:

        result = Parser.factorExpression()
        
        while Parser.tokenizer.next.type in ["MULT", "DIV"]:

            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()

            result =  BinOp(op,Parser.factorExpression(), result)
        
        return result


    @staticmethod
    def parseExpression() -> Node:
        
        result = Parser.termExpression()
        
        while Parser.tokenizer.next.type in ["MINUS", "PLUS"]:

            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()

            result =  BinOp(op,Parser.termExpression(), result)
        
        return result
        

    def run(source):
        Parser.tokenizer = Tokenizer(source)
        result = Parser.parseExpression()

        if Parser.tokenizer.next.type != "EOF":
            raise ValueError("Entrada não foi finalizada corretamente")

        return result.Evaluate() #chama os resultados da árvore

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                 source = file.read()

            # Passa o código pelo prepro
            prepro = PrePro(source)
            processed_source = prepro.filtered_source
            result = Parser.run(processed_source)
            print(result)

        except FileNotFoundError:
            sys.stderr.write(f"Erro: Arquivo '{filename}' não encontrado.\n")
        except ValueError as e:
            sys.stderr.write(str(e) + '\n')

    else:
        sys.stderr.write("nenhuma entrada à ser processada" + '\n')

if __name__=="__main__":
    main()
