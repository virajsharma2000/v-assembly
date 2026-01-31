import os

file = input('Enter file: ')

executable_code = '\n'
empty_buffers = '\n'
data = '\n'
buffer_num = 1

with open(file, 'r') as f:
 for line in f.read().splitlines():
  tokenized_line = line.split()
  
  if tokenized_line[0] == 'assign' and tokenized_line[2] == 'as':
   variable_name = tokenized_line[1]
   expression = tokenized_line[3]

   if expression.isdigit():
    data += f'{variable_name} db {expression}\n'
   
   elif 'sum' in expression:
    arguments = tokenized_line[4].split(',')

    data += f'{variable_name} db 0\n'
    
    instructions = ''

    is_first_argument = True

    for argument in arguments:
     if is_first_argument:
      instructions += f'mov al, [{argument}]\n'

     else:
      instructions += f'add al, [{argument}]\n'
     
     is_first_argument = False

    instructions = instructions + f'mov [{variable_name}], al\n'
    executable_code += instructions

   else:
    data += f'{variable_name} db 0\n'
    executable_code += f'mov al, [{expression}]\nmov [{variable_name}], al\n'
  
  if tokenized_line[0] == 'give':
   empty_buffers += f'buffer{buffer_num} resb 1\n'
   executable_code += f'mov al, [{tokenized_line[1]}]\nadd al, \'0\'\nmov [buffer{buffer_num}], al\nmov rax, 1\nmov rdi, 1\nmov rsi, buffer{buffer_num}\nmov rdx, 1\nsyscall\n'
   buffer_num += 1

assembly_code = f'section .data\n{data}\nsection .bss\n{empty_buffers}section .text\nglobal _start:\n_start:\n{executable_code}'
assembly_code = assembly_code + '\nmov rax, 60\nsyscall\n'

with open('hello.asm', 'w') as f:
 f.write(assembly_code)

f.close()

os.system('nasm -f elf64 hello.asm -o hello.o')
os.system('ld hello.o -o hello')