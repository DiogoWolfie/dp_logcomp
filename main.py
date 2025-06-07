import sys
from prepro.prepro import PrePro
from parser.parser import Parser
from symtab.symboltable import SymbolTable
from ast.nodes.funccall import FuncCall
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

            # Avalia o bloco global para registrar funções e variáveis globais
            result.Evaluate(st)

            # Executa a função main
            main_call = FuncCall("main", [])
            main_call.Evaluate(st)

            #result.Evaluate(st)
            
            #gen_code = result.Generate(st)
            #Code.append(gen_code)
            #Code.dump("teste1.asm")


        except FileNotFoundError:
            sys.stderr.write(f"Erro: Arquivo '{filename}' não encontrado.\n")
        except ValueError as e:
            sys.stderr.write(str(e) + '\n')
    else:
        sys.stderr.write("nenhuma entrada à ser processada" + '\n')

if __name__ == "__main__":
    main()