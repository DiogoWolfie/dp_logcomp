from lexer.tokenizer import Tokenizer
from ast.nodes.noblc import NoBlc
from ast.nodes.noop import NoOp
from ast.nodes.noat import NoAt
from ast.nodes.noprt import NoPrt
from ast.nodes.noid import NoId
from ast.nodes.intval import IntVal
from ast.nodes.unop import UnOp
from ast.nodes.binop import BinOp
from ast.nodes.whilenode import WhileNode
from ast.nodes.ifnode import IfNode
from ast.nodes.readnode import ReadNode
from ast.node import Node

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

        result = None
        
        #caso 1: é um blocok vazio
        if Parser.tokenizer.next.type == "ENTER":
            Parser.tokenizer.selectNext()
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

        #caso 4: é um while
        elif Parser.tokenizer.next.type == "WHILE":
            Parser.tokenizer.selectNext() #consome o while

            result = WhileNode(Parser.BExpression(), Parser.Block())
            if Parser.tokenizer.next.type == "ENTER":
                Parser.tokenizer.selectNext()
                return result
            else:
                raise ValueError("while sem quebra de linha") 
        
        #caso 5: é um if - tem que considerar o else tbm
        elif Parser.tokenizer.next.type == "IF":
            Parser.tokenizer.selectNext() #consumir o if

            result = IfNode(Parser.BExpression(), Parser.Block())
            #caso tenha um else:
            maybe_else = Parser.tokenizer.next.type
            if maybe_else == "ELSE":
                result = IfNode(Parser.BExpression(), Parser.Block(), Parser.Block())

                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise ValueError("else sem quebra de linha")
            else:
                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise ValueError("if sem quebra de linha")


        else:
            raise ValueError("statemente mal inicalizado")


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
        
        elif token.type == "NOT":
            return UnOp(token.value, Parser.factorExpression()) #se der ruim, trocar por token.type

        elif token.value == "(":
            
            result = Parser.BExpression()
            if Parser.tokenizer.next.type != "CLOSE_PAR":
                raise ValueError("Parênteses não foi fechado")

            Parser.tokenizer.selectNext()  # Consumir `)`
            return result
        
        elif token.type == "IDENTIFIER":
            return NoId(token.value)

        elif token.type == "READ":
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != "CLOSE_PAR":
                    raise ValueError("read não fechou parênteses")
                Parser.tokenizer.selectNext()
                return ReadNode(token.value)
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
    
    @staticmethod
    def RelExpression() -> Node:
        result = Parser.parseExpression()

        while Parser.tokenizer.next.type in ["EQUAL_EQUAL", "LESS", "GREATER"]:
            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            result = BinOp(op, result, Parser.parseExpression())
        return result


    @staticmethod
    def BTerm() -> Node:
        result = Parser.RelExpression()

        while Parser.tokenizer.next.type == "AND":
            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            result = BinOp(op, result, Parser.RelExpression())
        return result

    @staticmethod
    def BExpression() -> Node:
        result = Parser.BTerm()

        while Parser.tokenizer.next.type == "OR":
            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()
            result = BinOp(op, result, Parser.BTerm())
        return result
        

    def run(source):
        Parser.tokenizer = Tokenizer(source)
        result = Parser.Block()

        if Parser.tokenizer.next.type != "EOF":
            raise ValueError("Entrada não foi finalizada corretamente")

        return result #chama os resultados da árvore