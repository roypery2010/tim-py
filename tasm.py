from tasmlexer import *
from tim_py import *
from tasmparser import *
import sys


def main():
    argc = len(sys.argv)
    argv = sys.argv
    if (argc < 2):
        raise RuntimeError("Usage: %s <file_name.tasm-py>\n", argv[0])
    file_name = argv[1]
    lexer = Lexer(file_name)
    tokens = lexer.run()
    for token in tokens:
        print(token)
    parser = Parser(tokens)
    program = parser.generate_instructions()
    for inst in program:
        print(inst)
    machine = Machine(program)
    machine.run()
    write_program_to_file("machine.tim-py", program)
    
main()