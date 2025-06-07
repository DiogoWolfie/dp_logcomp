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
from ast.nodes.strnode import StrNode
from ast.nodes.boolval import BoolVal
from ast.nodes.typenode import TypeNode
from ast.nodes.varnode import VarNode 
from ast.node import Node
from ast.nodes.funcdec import FuncDec
from ast.nodes.funccall import FuncCall
from ast.nodes.returnnode import ReturnNode

#análise sintática - checa a ordem das palavras
#talvez eu precise colocar um check aqui para o caso do próximo valor depois de um número seja um número tbm sem 
class Parser():
    tokenizer = None

    @staticmethod
    def parseProgram():
        nodes = []
        while Parser.tokenizer.next.type in ("FUNC", "VAR", "IDENTIFIER", "PRINT", "RETURN", "IF", "WHILE", "ENTER"):
            if Parser.tokenizer.next.type == "ENTER":
                Parser.tokenizer.selectNext()
                continue
            elif Parser.tokenizer.next.type == "FUNC":
                print("função a ser contruida")
                nodes.append(Parser.parseFuncDeclaration())
            else:
                print("variavel global a ser montada")
                stmt = Parser.VarDeclaration()
                if stmt is not None:
                    nodes.append(stmt)
        return NoBlc(nodes)  # ou o nó de bloco que você usa

    @staticmethod
    def Block() -> Node:
        token = Parser.tokenizer.next  # Primeiro verifica o token atual
        
        if token.type != "OPEN_KEY":
            raise ValueError("Erro na inicialização do bloco, sem {")
        
        Parser.tokenizer.selectNext()  # Só então consome o "{"
        statements = []
        
        if Parser.tokenizer.next.type == "ENTER":
            Parser.tokenizer.selectNext()
            while Parser.tokenizer.next.type != "CLOSE_KEY":
                stmt = Parser.Statement()
                statements.append(stmt)
        else:
            raise ValueError("esperado ENTER após {")
        
        Parser.tokenizer.selectNext()  # Consome o "}"
        return NoBlc(statements)
    
    @staticmethod
    def parseFuncDeclaration():
        #preciso checar se o próximo token é func
        if Parser.tokenizer.next.type != "FUNC":
            raise ValueError("Esperado 'func' para declaração de função")
        # Se for, consome o token
        Parser.tokenizer.selectNext()  # consome 'func'
        if Parser.tokenizer.next.type != "IDENTIFIER":
            raise ValueError("Esperado nome da função")
        
        func_name = Parser.tokenizer.next.value
        print(f"nome da função {func_name}")
        Parser.tokenizer.selectNext()
        if Parser.tokenizer.next.type != "OPEN_PAR":
            raise ValueError("Esperado '(' após nome da função")
        
        Parser.tokenizer.selectNext()#consome (
        params = []
        while Parser.tokenizer.next.type != "CLOSE_PAR":
            param_name = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type != "TYPE":
                raise ValueError("Esperado tipo do parâmetro")
            param_type = TypeNode(Parser.tokenizer.next.value)
            params.append(VarNode(param_name, param_type))
            Parser.tokenizer.selectNext()
            if Parser.tokenizer.next.type == "COMMA":
                Parser.tokenizer.selectNext()
        Parser.tokenizer.selectNext()  # consome ')'
        if Parser.tokenizer.next.type == "TYPE":
            return_type = TypeNode(Parser.tokenizer.next.value)
            Parser.tokenizer.selectNext()
        else:
            return_type = None
        block = Parser.Block()
        return FuncDec(func_name, params, return_type, block)

    @staticmethod
    def VarDeclaration() -> Node:
        result = None
        if Parser.tokenizer.next.type != "VAR":
            print(f"deveria ser um var mas é um {Parser.tokenizer.next.type}")
            raise ValueError("declaração errada de variável")
        Parser.tokenizer.selectNext() #consumir o VAR
        if Parser.tokenizer.next.type != "IDENTIFIER":
            raise ValueError("Esperado nome da variavel")
        
        identifier = Parser.tokenizer.next.value
        print(f"variavel global {identifier}")
        Parser.tokenizer.selectNext() #consome o identificador
        if Parser.tokenizer.next.type != "TYPE":
            raise ValueError("Esperado tipo da variavel")
        tipo = TypeNode(Parser.tokenizer.next.value)
        Parser.tokenizer.selectNext() #consumo o tipo

        var_node = VarNode(identifier, tipo)

        if Parser.tokenizer.next.type == "EQUAL":
            Parser.tokenizer.selectNext()
            return NoBlc([var_node, NoAt(identifier, Parser.BExpression())])

        return var_node
                


    @staticmethod
    def Statement() -> Node:

        result = None
        
        #caso 1: é um blocok vazio
        if Parser.tokenizer.next.type == "ENTER":
            Parser.tokenizer.selectNext()
            return NoOp()
        
        #caso 2: tem um identificador que precisa ser seguido de um =
        elif Parser.tokenizer.next.type == "IDENTIFIER":
            identifier = Parser.tokenizer.next.value
            print(f"identificador {identifier}")
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type == "EQUAL":
                Parser.tokenizer.selectNext()
                result = NoAt(identifier, Parser.BExpression())
                print("nó de atribuição do caso 2")
                print(f"token atual: {Parser.tokenizer.next.value}")
                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise ValueError("Esperado ENTER após instrução")

            elif Parser.tokenizer.next.type == "OPEN_PAR":
                # chamada de função
                print(f"Chamada de função: {identifier}")
                args = []
                Parser.tokenizer.selectNext()  # consome (
                while Parser.tokenizer.next.type != "CLOSE_PAR":
                    args.append(Parser.BExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                        args.append(Parser.BExpression())

                if Parser.tokenizer.next.type != "CLOSE_PAR":
                    raise ValueError("Parênteses da chamada de função não fechado")
                Parser.tokenizer.selectNext()  # consome )
                result = FuncCall(identifier, args)

                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                    return result
                else:
                    raise ValueError("Esperado ENTER após chamada de função")

            else:
                raise ValueError("Identificador mal utilizado")

            # if Parser.tokenizer.next.type == "ENTER":
            #     Parser.tokenizer.selectNext()
            #     return result
            # else:
            #     raise ValueError("Esperado ENTER após instrução")

            
        #caso 3: é um print:
        elif Parser.tokenizer.next.type == "PRINT":
            Parser.tokenizer.selectNext() #consome o print

            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext() #preciso consimir o abre parenteses do print
                result = NoPrt(Parser.BExpression())
        
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
            Parser.tokenizer.selectNext()
            condition = Parser.BExpression()
            if_block = Parser.Block()
            
            if Parser.tokenizer.next.type == "ELSE":
                Parser.tokenizer.selectNext()
                else_block = Parser.Block()
                result = IfNode(condition, if_block, else_block)
            else:
                result = IfNode(condition, if_block)
            
            if Parser.tokenizer.next.type == "ENTER":
                Parser.tokenizer.selectNext()
                return result
            else:
                raise ValueError("if/else sem quebra de linha")
            

        #caso 6: é return
        elif Parser.tokenizer.next.type == "RETURN":
            Parser.tokenizer.selectNext()  # consome 'return'

            # Se o próximo for ENTER ou CLOSE_KEY, é um return vazio
            if Parser.tokenizer.next.type in ["ENTER", "CLOSE_KEY"]:
                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                return ReturnNode(None)

            # Caso contrário, espera uma expressão de retorno
            result = ReturnNode(Parser.BExpression())

            # Após a expressão, espera-se ENTER ou CLOSE_KEY
            if Parser.tokenizer.next.type in ["ENTER", "CLOSE_KEY"]:
                if Parser.tokenizer.next.type == "ENTER":
                    Parser.tokenizer.selectNext()
                return result
            else:
                raise ValueError("return deve ser seguido por quebra de linha ou fim de bloco")
                                    
        #caso 7: var
        elif Parser.tokenizer.next.type == "VAR":
            return Parser.VarDeclaration()

        #caso 9: block
        elif Parser.tokenizer.next.type == "OPEN_KEY":
            return Parser.Block()


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
            identifier = token.value
            # Verifica se é uma chamada de função
            if Parser.tokenizer.next.type == "OPEN_PAR":
                args = []
                Parser.tokenizer.selectNext()  # consome '('
                while Parser.tokenizer.next.type != "CLOSE_PAR":
                    args.append(Parser.BExpression())
                    if Parser.tokenizer.next.type == "COMMA":
                        Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != "CLOSE_PAR":
                    raise ValueError("Parênteses da chamada de função não fechado")
                Parser.tokenizer.selectNext()  # consome ')'
                return FuncCall(identifier, args)
            else:
                return NoId(identifier)


        elif token.type == "STRING":
            return StrNode(token.value)
        
        #variavel true ou false
        elif token.type == "BOOL":
            return BoolVal(token.value)



        elif token.type == "READ":
            if Parser.tokenizer.next.type == "OPEN_PAR":
                Parser.tokenizer.selectNext()
                if Parser.tokenizer.next.type != "CLOSE_PAR":
                    raise ValueError("read não fechou parênteses")
            
                Parser.tokenizer.selectNext()
                return ReadNode()
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
        result = Parser.parseProgram()

        if Parser.tokenizer.next.type != "EOF":
            print(f"Erro: Entrada não finalizada corretamente, próximo token: {Parser.tokenizer.next.type}")
            raise ValueError("Entrada não foi finalizada corretamente")

        return result #chama os resultados da árvore