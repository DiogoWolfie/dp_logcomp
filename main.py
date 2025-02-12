import sys

#classe token/palavra
#será definida pelo seu tipo e seu valor
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value


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

        else:
            raise ValueError(f"Token inesperado: {current_char}")
        

#análise sintática - checa a ordem das palavras
class Parser():
    tokenizer = None

    @staticmethod
    def parseExpression():
        
        #checa o primeiro número
        if Parser.tokenizer.next.type == "NUMBER":
            result = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
        else:
            raise ValueError("Esperado um número no início da espressão")
            
        while Parser.tokenizer.next.type in ["PLUS", "MINUS"]:
            op = Parser.tokenizer.next.type
            Parser.tokenizer.selectNext()

            if Parser.tokenizer.next.type != "NUMBER":
                raise ValueError("Esperado um número após o operador")

            num = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()

            # Aplica a operação
            if op == "PLUS":
                result += num
            elif op == "MINUS":
                result -= num

        return result
        

    def run(source):
        Parser.tokenizer = Tokenizer(source)
        result = Parser.parseExpression()

        if Parser.tokenizer.next.type != "EOF":
            raise ValueError("Entrada não foi finalizada corretamente")

        return result

def main():
    if len(sys.argv) > 1 :
        source = "".join(sys.argv[1:])

        try:
            result = Parser.run(source)
            print(result)
        except ValueError as e:
            print(f"erro {e}")
    
    else:
        raise ValueError("não forneceu nenhuma espressão")

if __name__=="__main__":
    main()
