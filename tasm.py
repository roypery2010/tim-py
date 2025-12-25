from tasmlexer import Lexer
from tasmparser import Parser
from tim_py import write_program_to_file

import sys

def convert(path):
    # Lex
    tokens = Lexer(path).run()

    # Parse → TIM instruction objects
    insts = Parser(tokens).generate_instructions()

    # Write .tim file (pickle format)
    out = path.replace(".tasm", ".tim")
    write_program_to_file(out, insts)

    print(f"Converted {path} → {out}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tasm.py file.tasm")
        sys.exit(1)
    convert(sys.argv[1])
