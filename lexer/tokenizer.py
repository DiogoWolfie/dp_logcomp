from lexer.token import Token

#classe de tokenização - análise léxica
class Tokenizer:
    def __init__(self, source):
        self.source = source #código fonte
        self.position = 0 #posição atual que o tokenizer está separando
        self.next = None #o último token separado
        self.selectNext()

    def selectNext(self):
        
        palavras_reservadas = ["Println", "if", "else", "while", "for", "Scan", "||", "&&", "var", "int", "float", "string", "bool", "true", "false"] #palavras reservadas da linguagem

        #iginora todos os espaços em branco
        while self.position < len(self.source) and self.source[self.position] in [' ', '\t']:
            self.position += 1 

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        current_char = self.source[self.position]

        #procurando string
        if current_char == '"':
            self.position += 1  # pula o caractere inicial de aspas
            string_value = ''
            
            while self.position < len(self.source) and self.source[self.position] != '"':
                string_value += self.source[self.position]
                self.position += 1

            if self.position >= len(self.source):
                raise ValueError("String sem aspas de fechamento")

            self.position += 1  # pula a aspa de fechamento
            self.next = Token("STRING", string_value)
            return

        if current_char.isdigit():
            value = 0
            while self.position < len(self.source) and self.source[self.position].isdigit():
                value = value * 10 + int(self.source[self.position])
                self.position += 1
                if self.position < len(self.source) and (self.source[self.position].isalpha() or self.source[self.position] == "_"):
                    raise ValueError("Número seguido de letra ou underscore inválido")  
            self.next = Token("NUMBER", value)
            return
            
        elif current_char.isalpha() or current_char == "_":
            identifier = ''
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                identifier += self.source[self.position]
                self.position += 1

            if identifier in palavras_reservadas:
                if identifier == "if":
                    self.next = Token("IF", identifier)
                    return
                elif identifier == "else": 
                    self.next = Token("ELSE", identifier)
                    return
                elif identifier == "for":
                    self.next = Token("WHILE", identifier)
                    return
                elif identifier == "Println":
                    self.next= Token("PRINT", identifier)
                    return
                elif identifier == "Scan":
                    self.next= Token("READ", identifier)
                    return
                elif identifier == "var":
                    self.next = Token("VAR", identifier)
                    return
                elif identifier == "int":
                    self.next = Token("TYPE", identifier)
                    return
                elif identifier == "bool":
                    self.next = Token("TYPE", identifier)
                    return
                elif identifier == "string":
                    self.next = Token("TYPE", identifier)
                    return
                elif identifier == "true":
                    self.next = Token("BOOL", identifier)
                    return
                elif identifier == "false":
                    self.next = Token("BOOL", identifier)
                    return
            else:
                self.next= Token("IDENTIFIER", identifier)
                return

        elif current_char == '\n':
            self.next = Token("ENTER", 'enter')
            self.position += 1
            return

        elif current_char == "=":
            self.next = Token("EQUAL", current_char)
            self.position+=1
            if self.position < len(self.source) and self.source[self.position] == "=":
                self.next = Token("EQUAL_EQUAL", current_char + self.source[self.position])
                self.position+=1
                return

        elif current_char == "{":
            self.next = Token("OPEN_KEY", current_char)
            self.position+=1
            return

        elif current_char == "}":
            self.next = Token("CLOSE_KEY", current_char)
            self.position+=1
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
            return

        elif current_char == ")":
            self.next = Token("CLOSE_PAR", current_char)
            self.position+=1
            return
        
        elif current_char == "|":
            self.position+=1
            if self.position < len(self.source) and self.source[self.position] == "|":
                self.next = Token("OR", current_char + self.source[self.position])
                self.position+=1
                return
            
        
        elif current_char == "&":
            self.position+=1
            if self.position < len(self.source) and self.source[self.position] == "&":
                self.next = Token("AND", current_char + self.source[self.position])
                self.position+=1
                return
        
        elif current_char == "<":
            self.next = Token("LESS", current_char)
            self.position+=1
            return
        
        elif current_char == ">":
            self.next = Token("GREATER", current_char)
            self.position+=1
            return
        
        elif current_char == "!":
            self.next = Token("NOT", current_char)
            self.position+=1
            return
        

        else:
            raise ValueError(f"Token inesperado: {current_char}")