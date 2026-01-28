section .bss
 buffer resb 5

section .data
 password db "KESHAVJAGTAP"
 success_message db "you won", 10

section .text
global _start
_start:
 mov rbx, 0
 
 mov rax, 0
 mov rdi, 0
 mov rsi, buffer
 mov rdx, 12
 syscall
 
 compare_equal:
  mov al, [buffer + rbx]
  mov cl, [password + rbx]
  cmp al, cl
  jne exit
  inc rbx
  cmp rbx, 12
  jne compare_equal
  
 mov rax, 1
 mov rdi, 1
 mov rsi, success_message
 mov rdx, 9
 syscall

 exit:
  mov rax, 60
  syscall

