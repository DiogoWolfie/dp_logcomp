section .data
                format_out : db "%d" , 10 , 0 ; format do printf
                format_in : db "%d" , 0 ; format do scanf
                scan_int : dd 0 ; 32−bits integer
            
            section .text
                extern printf ; usar _printf para Windows
                extern scanf ; usar _scanf para Windows
                ; extern _ExitProcess@4 ; usar para Windows
                global main ; início do programa
            
            main:
            push ebp ; guarda o EBP
            mov ebp , esp ; zera a pilha

            sub esp, 4;
            mov dword [ebp - 4], 0;
            
                
            ;Geracao do scan()
            push scan_int
            push format_in
            call scanf
            add esp, 8
            mov eax, [scan_int];
                mov [ebp - 4], eax;None
            sub esp, 4;
            mov dword [ebp - 8], 0;
            
                mov eax, 4;
                mov [ebp - 8], eax;None
            
                    mov eax, [ebp - 8]; generate no identificador
                    push eax;
                    mov eax, [ebp - 4]; generate no identificador
                    pop ecx;
                    cmp eax, ecx;
                    mov ecx, 1;
                    mov eax, 0;
                    cmovl eax, ecx;
                    
            cmp eax, 0
            je else_24
            
            mov eax, [ebp - 8]; generate no identificador
            push eax ; Empilha os argumentos para chamar a funcao
            push format_out ; Dizendo para o printf que é um inteiro
            call printf ; Chamada da função
            add esp, 8 ; Remove os argumentos da pilha
            jmp endif_24
            else_24:
            
            
                    mov eax, [ebp - 8]; generate no identificador
                    push eax;
                    mov eax, [ebp - 4]; generate no identificador
                    pop ecx; 
                    imul eax, ecx; binop para multiplicação
                    
            push eax ; Empilha os argumentos para chamar a funcao
            push format_out ; Dizendo para o printf que é um inteiro
            call printf ; Chamada da função
            add esp, 8 ; Remove os argumentos da pilha
            endif_24:mov esp, ebp ; reestabelece a pilha
            pop ebp

            ;chamada da interrupcao de saida (linux)
            mov eax, 1
            xor ebx, ebx
            int 0x80
            ; Para Windows :
            ; push dword 0
            ; call _ExitProcess@4
