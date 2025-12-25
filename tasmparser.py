from tasmlexer import *
from tim_py import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def generate_instructions(self):
        program = []
        labels = {}  # label → instruction index

        # PASS 1: collect label definitions
        for token in self.tokens:
            if token.token_type == TokenType.TYPE_LABEL_DEF:
                labels[token.text] = len(program)
            elif token.token_type == TokenType.TYPE_PUSH:
                program.append(None)
            elif token.token_type == TokenType.TYPE_INDUP:
                program.append(None)
            elif token.token_type == TokenType.TYPE_INSWAP:
                program.append(None)
            elif token.token_type in (
                TokenType.TYPE_POP, TokenType.TYPE_DUP, TokenType.TYPE_SWAP,
                TokenType.TYPE_ADD, TokenType.TYPE_SUB, TokenType.TYPE_MUL,
                TokenType.TYPE_DIV, TokenType.TYPE_MOD, TokenType.TYPE_CMPE,
                TokenType.TYPE_CMPNE, TokenType.TYPE_CMPG, TokenType.TYPE_CMPL,
                TokenType.TYPE_CMPGE, TokenType.TYPE_CMPLE, TokenType.TYPE_PRINT,
                TokenType.TYPE_HALT
            ):
                program.append(None)
            elif token.token_type in (
                TokenType.TYPE_JMP, TokenType.TYPE_ZJMP, TokenType.TYPE_NZJMP
            ):
                program.append(None)

        # PASS 2: generate instructions + resolve jumps
        i = 0
        inst_index = 0

        while i < len(self.tokens):
            token = self.tokens[i]
            print(f"Parsing {token}")

            match token.token_type:
                case TokenType.TYPE_LABEL_DEF:
                    pass

                case TokenType.TYPE_PUSH:
                    i += 1
                    val = int(self.tokens[i].text)
                    program[inst_index] = DEF_INST_PUSH(val)
                    inst_index += 1

                case TokenType.TYPE_POP:
                    program[inst_index] = DEF_INST_POP()
                    inst_index += 1

                case TokenType.TYPE_DUP:
                    program[inst_index] = DEF_INST_DUP()
                    inst_index += 1

                case TokenType.TYPE_SWAP:
                    program[inst_index] = DEF_INST_SWAP()
                    inst_index += 1

                case TokenType.TYPE_INDUP:
                    i += 1
                    val = int(self.tokens[i].text)
                    program[inst_index] = DEF_INST_INDUP(val)
                    inst_index += 1

                case TokenType.TYPE_INSWAP:
                    i += 1
                    val = int(self.tokens[i].text)
                    program[inst_index] = DEF_INST_INSWAP(val)
                    inst_index += 1

                case TokenType.TYPE_ADD:
                    program[inst_index] = DEF_INST_ADD()
                    inst_index += 1

                case TokenType.TYPE_SUB:
                    program[inst_index] = DEF_INST_SUB()
                    inst_index += 1

                case TokenType.TYPE_MUL:
                    program[inst_index] = DEF_INST_MUL()
                    inst_index += 1

                case TokenType.TYPE_DIV:
                    program[inst_index] = DEF_INST_DIV()
                    inst_index += 1

                case TokenType.TYPE_MOD:
                    program[inst_index] = DEF_INST_MOD()
                    inst_index += 1

                case TokenType.TYPE_CMPE:
                    program[inst_index] = DEF_INST_CMPE()
                    inst_index += 1

                case TokenType.TYPE_CMPNE:
                    program[inst_index] = DEF_INST_CMPNE()
                    inst_index += 1

                case TokenType.TYPE_CMPG:
                    program[inst_index] = DEF_INST_CMPG()
                    inst_index += 1

                case TokenType.TYPE_CMPL:
                    program[inst_index] = DEF_INST_CMPL()
                    inst_index += 1

                case TokenType.TYPE_CMPGE:
                    program[inst_index] = DEF_INST_CMPGE()
                    inst_index += 1

                case TokenType.TYPE_CMPLE:
                    program[inst_index] = DEF_INST_CMPLE()
                    inst_index += 1

                case TokenType.TYPE_PRINT:
                    program[inst_index] = DEF_INST_PRINT()
                    inst_index += 1

                case TokenType.TYPE_HALT:
                    program[inst_index] = DEF_INST_HALT()
                    inst_index += 1

                case TokenType.TYPE_JMP:
                    i += 1
                    label = self.tokens[i].text
                    if label not in labels:
                        raise ValueError(f"Unknown label '{label}' in JMP")
                    program[inst_index] = DEF_INST_JMP(labels[label])
                    inst_index += 1

                case TokenType.TYPE_ZJMP:
                    i += 1
                    label = self.tokens[i].text
                    if label not in labels:
                        raise ValueError(f"Unknown label '{label}' in ZJMP")
                    program[inst_index] = DEF_INST_ZJMP(labels[label])
                    inst_index += 1

                case TokenType.TYPE_NZJMP:
                    i += 1
                    label = self.tokens[i].text
                    if label not in labels:
                        raise ValueError(f"Unknown label '{label}' in NZJMP")
                    program[inst_index] = DEF_INST_NZJMP(labels[label])
                    inst_index += 1

            i += 1

        # remove placeholders
        return [inst for inst in program if inst is not None]
