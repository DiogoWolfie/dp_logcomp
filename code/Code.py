class Code:
    instructions = []

    @staticmethod
    def append(code: str) -> None:
        Code.instructions.append(code)
        
    @staticmethod
    def dump(filename: str) -> None:
        with open(filename, 'w', encoding='utf-8') as file:
            # Escrever o cabeçalho: até início do código gerado
            header="""
            section .data
                format_out : db "%d" , 10 , 0 ; format do printf
                format_in : db "%d" , 0 ; format do scanf
                scan_int : dd 0 ; 32−bits integer
            
            section .text
                extern printf ; usar _printf para Windows
                extern scanf ; usar _scanf para Windows
                ; extern _ExitProcess@4 ; usar para Windows
                global _start ; início do programa ld
            
            _start:
            push ebp ; guarda o EBP
            mov ebp , esp ; zera a pilha"""
            file.write(header.strip() + "\n")  # Remove espaços extras e adiciona \n
            # Escreve as instruções armazenadas
            file.write("\n".join(Code.instructions) + "\n")

            # Escrever as instruções finais: após término do código gerado
            rodape="""
            mov esp, ebp ; reestabelece a pilha
            pop ebp

            ;chamada da interrupcao de saida (linux)
            mov eax, 1
            xor ebx, ebx
            int 0x80
            ; Para Windows :
            ; push dword 0
            ; call _ExitProcess@4"""

            file.write(rodape.strip() + "\n")  # Remove espaços extras e adiciona \n