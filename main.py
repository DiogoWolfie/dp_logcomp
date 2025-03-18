import sys
from abc import ABC, abstractmethod
import re

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
        lines = self.source.split("\n")
        clean_lines = []
        
        for line in lines:
            if "//" in line:
                line = line.split("//")[0]  # Remove comentário
            clean_lines.append(line)  # NÃO usar strip() aqui!

        return "\n".join(clean_lines)  
    

#classe de tokenização - análise léxica
class Tokenizer:
    def __init__(self, source):
        self.source = source #código fonte
        self.position = 0 #posição atual que o tokenizer está separando
        self.next = None #o último token separado
        self.selectNext()

    def selectNext(self):
        
        palavras_reservadas = ["Println"] #por enquanto é só essa

        #iginora todos os espaços em branco
        while self.position < len(self.source) and self.source[self.position] in [' ', '\t']:
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
            
        elif current_char.isalpha():
            p = re.compile(r'[A-Za-z][A-Za-z0-9_]*(?!\=)')
            identifier = ''
            while self.position < len(self.source) and p.match(self.source[self.position]):
                identifier += self.source[self.position] #espero que funcione
                self.position+=1
            if identifier in palavras_reservadas:
                self.next= Token("PRINT", identifier)
            else:
                self.next= Token("IDENTIFIER", identifier)
            pass

        elif current_char == '\n':
            self.next = Token("ENTER", 'enter')
            self.position += 1

        elif current_char == "=":
            self.next = Token("EQUAL", current_char)
            self.position+=1

        elif current_char == "{":
            self.next = Token("OPEN_KEY", current_char)
            self.position+=1

        elif current_char == "}":
            self.next = Token("CLOSE_KEY", current_char)
            self.position+=1

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
        


#classe Symbol Table
class SymbolTable():
    def __init__(self):
       self._table = {}

    def get(self,name):
        if name in self._table:
            return self._table[name]
        else:
            raise ValueError(f"variável {name} não está definida")
      
    def set(self,name,value):
        self._table[name]= value



"""AST - Abstract Syntax Tree"""
class Node(ABC):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self, SymbolTable):
        pass
        
    pass


#BinOp - Operações binárias
class BinOp(Node):
    def __init__(self, value, children_left, children_right):
        super().__init__(value, [children_left,children_right])
    
    def Evaluate(self, SymbolTable):
        if self.value == 'PLUS':
            return self.children[0].Evaluate(SymbolTable) + self.children[1].Evaluate(SymbolTable)
        elif self.value == 'MINUS':
            return self.children[0].Evaluate(SymbolTable) - self.children[1].Evaluate(SymbolTable)
        elif self.value == 'MULT':
            return self.children[0].Evaluate(SymbolTable) * self.children[1].Evaluate(SymbolTable)
        elif self.value == 'DIV':
            return self.children[0].Evaluate(SymbolTable) / self.children[1].Evaluate(SymbolTable)
        

#UnOp - Operação unária
class UnOp(Node):
    def __init__(self, value, children):
        super().__init__(value, children)
    
    def Evaluate(self, SymbolTable):
        if self.value == "+":
            return self.children.Evaluate(SymbolTable)
        elif self.value == "-":
            return -self.children.Evaluate(SymbolTable)
        

#IntVal - Valor inteiro - não tem filho
class IntVal(Node):
    def __init__(self, value):
        super().__init__(value, [])
    
    def Evaluate(self, SymbolTable):
        return self.value
    

#NoOp - sem operaação
class NoOp(Node):
    def __init__(self):
        super().__init__(None, [])
    def Evaluate(self, SymbolTable):
        pass
    

#NoId - identificador / variável
class NoId(Node):
    def __init__(self, value):
        super().__init__(value, [])
    
    def Evaluate(self, SymbolTable):
        return SymbolTable.get(self.value)

#NoAt - Nó de atribuição = só escreve na symbol table, logo o identifier é realmente apenas uma string
class NoAt(Node):
    def __init__(self, identifier, children):
        super().__init__(None, children)  # valor semântico pode ser None
        self.identifier = identifier     # <--- AQUI está o fix

    def Evaluate(self, SymbolTable):
        SymbolTable.set(self.identifier, self.children.Evaluate(SymbolTable))
        return None

#NoPrt - nó do print
class NoPrt(Node):
    def __init__(self, children):
        super().__init__(None,children)
    def Evaluate(self, SymbolTable):
        return print(self.children.Evaluate(SymbolTable))

#NoBlc- nó do bloco
class NoBlc(Node):
    def __init__(self, children):
        super().__init__(None,children)

    def Evaluate(self, SymbolTable):
        result = None
        for c in self.children:
            result = c.Evaluate(SymbolTable)
        return result
        
    
"""Fim da AST"""


#análise sintática - checa a ordem das palavras
#talvez eu precise colocar um check aqui para o caso do próximo valor depois de um número seja um número tbm sem 
class Parser():
    tokenizer = None

    @staticmethod
    def Block() -> Node:
        token = Parser.tokenizer.next
        statements = []
        Parser.tokenizer.selectNext()

        if token.type == "OPEN_KEY":
        
            if Parser.tokenizer.next.type == "ENTER":
                Parser.tokenizer.selectNext()
                while Parser.tokenizer.next.type != "CLOSE_KEY":
                    stmt = Parser.Statement()
                    statements.append(stmt)
            else:
                raise ValueError("esperado ENTER após {")
            
            Parser.tokenizer.selectNext()#acredito que irá consumir o }
            return NoBlc(statements)
        
        else:
            raise ValueError("Erro na incialização do bloco, sem {")
    
    @staticmethod
    def Statement() -> Node:
        #no momento que chama do statement o token atual é \n
        result = None
        
        #caso 1: é um blocok vazio
        if Parser.tokenizer.next.type == "ENTER":
            return NoOp()
        
        #caso 2: tem um identificador que precisa ser seguido de um =
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            indentifier = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()#consome o identificador

            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()  # consome o '='
                result = NoAt(indentifier, Parser.parseExpression())

                #checo se o proximo é realemtne um \n
                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise ValueError("faltou quebra de linha entre as atribuições")
            
            else:
                raise ValueError("identificador sem atribuição")
            
        #caso 3: é um print:
        elif Parser.tokenizer.next.type == "PRINT":
            Parser.tokenizer.selectNext() #consome o print

            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext() #preciso consimir o abre parenteses do print
                result = NoPrt(Parser.parseExpression())
        
                if Parser.tokenizer.next.type != "CLOSE_PAR":
                    raise ValueError("print não fechou parênteses")
                Parser.tokenizer.selectNext() #consome )

                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise ValueError("print sem quebra de linha")
            else:
                raise ValueError("print sem abre parênteses")


    @staticmethod
    def factorExpression() -> Node:
        token = Parser.tokenizer.next  
        Parser.tokenizer.selectNext()

        if token.type == "NUMBER":
            return IntVal(token.value) 
        
        elif token.value == "+":  
            return UnOp("+", Parser.factorExpression())

        elif token.value == "-":
            return UnOp("-", Parser.factorExpression())

        elif token.value == "(":
            
            result = Parser.parseExpression()
            if Parser.tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("Parênteses não foi fechado")

            Parser.tokenizer.selectNext()  # Consumir `)`
            return result
        
        elif token.type == "IDENTIFIER":
            return NoId(token.value)

        else:
            raise ValueError("Erro de entrada")

    @staticmethod
    def termExpression() -> Node:

        result = Parser.factorExpression() 
        while Parser.tokenizer.next.type in ["MULT", "DIV"]:

            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()

            result =  BinOp(op,result,Parser.factorExpression())
        
        return result


    @staticmethod
    def parseExpression() -> Node:
        
        result = Parser.termExpression()
      
        while Parser.tokenizer.next.type in ["MINUS", "PLUS"]:

            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()

            result =  BinOp(op,result,Parser.termExpression())
    
        return result
        

    def run(source):
        Parser.tokenizer = Tokenizer(source)
        result = Parser.Block()

        if Parser.tokenizer.next.type != "EOF":
            raise ValueError("Entrada não foi finalizada corretamente")

        return result #chama os resultados da árvore

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
            st = SymbolTable()
            result.Evaluate(st) #é para printar o resultado

        except FileNotFoundError:
            sys.stderr.write(f"Erro: Arquivo '{filename}' não encontrado.\n")
        except ValueError as e:
            sys.stderr.write(str(e) + '\n')

    else:
        sys.stderr.write("nenhuma entrada à ser processada" + '\n')

if __name__=="__main__":
    main()
