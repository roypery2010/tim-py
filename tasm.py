import sys
import pickle
from tasmparser import Parser
from tasmlexer import Lexer
from tim_py import *

class TASM:
    def __init__(self, filename):
        self.filename = filename

    def assemble(self):
        # 1. Lex
        lexer = Lexer(self.filename)
        tokens = lexer.run()

        print("\n--- TOKENS ---")
        for t in tokens:
            print(t)

        # 2. Parse + resolve labels
        parser = Parser(tokens)
        instructions = parser.generate_instructions()

        print("\n--- INSTRUCTIONS ---")
        for inst in instructions:
            print(inst)

        # 3. Final program = list of real TIM-PY Inst objects
        program = [inst for inst in instructions if inst is not None]
        return program

def save_tim_file(program, out_file):
    # Save as pickled binary so read_program_from_file() works
    with open(out_file, "wb") as f:
        pickle.dump(program, f)

    print(f"\nSaved TIM-PY program to: {out_file} (binary pickle)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tasm.py <file.tasm>")
        sys.exit(1)

    source = sys.argv[1]

    # Output file: same name but .tim-py
    if "." in source:
        out = source.rsplit(".", 1)[0] + ".tim-py"
    else:
        out = source + ".tim-py"

    tasm = TASM(source)
    program = tasm.assemble()
    save_tim_file(program, out)
