import sys
from prepro.prepro import PrePro
from parser.parser import Parser
from symtab.symboltable import SymbolTable
from code.Code import Code

def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                source = file.read()

            processed_source = PrePro(source).filtered_source
            result = Parser.run(processed_source)
            st = SymbolTable()
            #result.Evaluate(st)
            
            gen_code = result.Generate(st)
            Code.append(gen_code)
            Code.dump("saida.asm")


        except FileNotFoundError:
            sys.stderr.write(f"Erro: Arquivo '{filename}' não encontrado.\n")
        except ValueError as e:
            sys.stderr.write(str(e) + '\n')
    else:
        sys.stderr.write("nenhuma entrada à ser processada" + '\n')

if __name__ == "__main__":
    main()