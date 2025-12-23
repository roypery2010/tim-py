from tasmlexer import *
from tim_py import *
program = [
    DEF_INST_PUSH(1),
    DEF_INST_PUSH(4),
    DEF_INST_PUSH(6),
    DEF_INST_PUSH(8),
    DEF_INST_PUSH(10),
    DEF_INST_PUSH(12),
    DEF_INST_INDUP(2),
    DEF_INST_PRINT(),
]

    

def main():
    lexer = Lexer("test.tasm-py")
    tokens = lexer.run()
    for token in tokens:
        print(token)
    #machine = Machine(insts)
    #write_program_to_file("test.tim-py", program)
    #machine = read_program_from_file("test.tim-py")
    #Machine.run()

main()