from tasmlexer import *
from tim_py import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def generate_instructions(self):
        label_map = {}
        
        # PASS 1: Collect label definitions
        for token in self.tokens:
            if token.token_type == TokenType.TYPE_LABEL_DEF:
                label_map[token.text] = token.line
                token.token_type = TokenType.TYPE_NOP

        # PASS 2: Resolve label references
        for token in self.tokens:
            if token.token_type == TokenType.TYPE_LABEL:
                label = token.text
                if label not in label_map:
                    raise ValueError(f"Unknown label '{label}'")
                line = label_map[label]
                token.token_type = TokenType.TYPE_INT
                token.text = str(line)

        # PASS 3: Generate instructions
        program = []
        i = 0

        while i < len(self.tokens):
            token = self.tokens[i]

            match token.token_type:
                case TokenType.TYPE_PUSH:
                    i += 1
                    if i >= len(self.tokens):
                        raise ValueError(f"Missing argument for PUSH at line {token.line}")
                    val_token = self.tokens[i]
                    val = val_token.val()  # works for INT, FLOAT
                    program.append(DEF_INST_PUSH(val))
                    print(f"PUSH: {val} (from '{val_token.text}') at line {token.line}")

                case TokenType.TYPE_POP:
                    program.append(DEF_INST_POP())
                    print(f"POP at line {token.line}")

                case TokenType.TYPE_DUP:
                    program.append(DEF_INST_DUP())
                    print(f"DUP at line {token.line}")

                case TokenType.TYPE_SWAP:
                    program.append(DEF_INST_SWAP())
                    print(f"SWAP at line {token.line}")

                case TokenType.TYPE_INDUP:
                    i += 1
                    val = int(self.tokens[i].text)
                    program.append(DEF_INST_INDUP(val))
                    print(f"INDUP {val} at line {token.line}")

                case TokenType.TYPE_INSWAP:
                    i += 1
                    val = int(self.tokens[i].text)
                    program.append(DEF_INST_INSWAP(val))
                    print(f"INSWAP {val} at line {token.line}")

                case TokenType.TYPE_ADD:
                    program.append(DEF_INST_ADD())
                    print(f"ADD at line {token.line}")

                case TokenType.TYPE_SUB:
                    program.append(DEF_INST_SUB())
                    print(f"SUB at line {token.line}")

                case TokenType.TYPE_MUL:
                    program.append(DEF_INST_MUL())
                    print(f"MUL at line {token.line}")

                case TokenType.TYPE_DIV:
                    program.append(DEF_INST_DIV())
                    print(f"DIV at line {token.line}")

                case TokenType.TYPE_MOD:
                    program.append(DEF_INST_MOD())
                    print(f"MOD at line {token.line}")

                case TokenType.TYPE_CMPE:
                    program.append(DEF_INST_CMPE())
                    print(f"CMPE at line {token.line}")

                case TokenType.TYPE_CMPNE:
                    program.append(DEF_INST_CMPNE())
                    print(f"CMPNE at line {token.line}")

                case TokenType.TYPE_CMPG:
                    program.append(DEF_INST_CMPG())
                    print(f"CMPG at line {token.line}")

                case TokenType.TYPE_CMPL:
                    program.append(DEF_INST_CMPL())
                    print(f"CMPL at line {token.line}")

                case TokenType.TYPE_CMPGE:
                    program.append(DEF_INST_CMPGE())
                    print(f"CMPGE at line {token.line}")

                case TokenType.TYPE_CMPLE:
                    program.append(DEF_INST_CMPLE())
                    print(f"CMPLE at line {token.line}")

                case TokenType.TYPE_PRINT:
                    program.append(DEF_INST_PRINT())
                    print(f"PRINT at line {token.line}")

                case TokenType.TYPE_HALT:
                    program.append(DEF_INST_HALT())
                    print(f"HALT at line {token.line}")

                case TokenType.TYPE_JMP:
                    i += 1
                    val = int(self.tokens[i].text)
                    program.append(DEF_INST_JMP(val))
                    print(f"JMP {val} at line {token.line}")

                case TokenType.TYPE_ZJMP:
                    i += 1
                    val = int(self.tokens[i].text)
                    program.append(DEF_INST_ZJMP(val))
                    print(f"ZJMP {val} at line {token.line}")

                case TokenType.TYPE_NZJMP:
                    i += 1
                    val = int(self.tokens[i].text)
                    program.append(DEF_INST_NZJMP(val))
                    print(f"NZJMP {val} at line {token.line}")

            i += 1

        return [inst for inst in program if inst is not None]
