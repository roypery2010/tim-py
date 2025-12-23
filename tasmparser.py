from tasmlexer import *
from tim_py import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
    def generate_instructions(self):
        program = []
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            print(f"Token {i} is {token}")
            match token.token_type:
                case TokenType.TYPE_PUSH:
                    i += 1
                    token = self.tokens[i]
                    print(f"Token {i} is {token}")
                    val = int(token.text)
                    program.append(DEF_INST_PUSH(val))
                case TokenType.TYPE_POP:
                    program.append(DEF_INST_POP())
                case TokenType.TYPE_DUP:
                    program.append(DEF_INST_DUP())
                case TokenType.TYPE_INDUP:
                    i += 1
                    token = self.tokens[i]
                    val = int(token.text)
                    program.append(DEF_INST_INDUP(val))
                case TokenType.TYPE_SWAP:
                    program.append(DEF_INST_SWAP())
                case TokenType.TYPE_INSWAP:
                    i += 1
                    token = self.tokens[i]
                    val = int(token.text)
                    program.append(DEF_INST_INSWAP(val)) 
                case TokenType.TYPE_ADD:
                    program.append(DEF_INST_ADD())
                case TokenType.TYPE_SUB:
                    program.append(DEF_INST_SUB())
                case TokenType.TYPE_MUL :
                    program.append(DEF_INST_MUL())
                case TokenType.TYPE_DIV :
                    program.append(DEF_INST_DIV())
                case TokenType.TYPE_MOD :
                    program.append(DEF_INST_MOD())
                case TokenType.TYPE_CMPE :
                    program.append(DEF_INST_CMPE())
                case TokenType.TYPE_CMPNE :
                    program.append(DEF_INST_CMPNE())
                case TokenType.TYPE_CMPG :
                    program.append(DEF_INST_CMPG())
                case TokenType.TYPE_CMPL :
                    program.append(DEF_INST_CMPL())
                case TokenType.TYPE_CMPGE :
                    program.append(DEF_INST_CMPGE())
                case TokenType.TYPE_CMPLE :
                    program.append(DEF_INST_CMPLE())
                case TokenType.TYPE_JMP :
                    i += 1
                    token = self.tokens[i]
                    val = int(token.text)
                    program.append(DEF_INST_JMP(val)) 
                case TokenType.TYPE_ZJMP  :
                    i += 1
                    token = self.tokens[i]
                    val = int(token.text)
                    program.append(DEF_INST_ZJMP(val)) 
                case TokenType.TYPE_NZJMP :
                    i += 1
                    token = self.tokens[i]
                    val = int(token.text)
                    program.append(DEF_INST_NZJMP(val)) 
                case TokenType.TYPE_PRINT :
                    program.append(DEF_INST_PRINT())
                case TokenType.TYPE_INT :
                    assert False, "ERROR: Should not be INT"
                case TokenType.TYPE_HALT :
                    program.append(DEF_INST_HALT())
            i += 1
        return program
