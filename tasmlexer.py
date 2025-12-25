from tim_py import *
from enum import Enum

MAX_TOKEN_STACK_SIZE = 1024

class Token:
    def __init__(self, token_type, text, line, char):
        self.token_type = token_type
        self.text = text
        self.line = line
        self.char = char

    def __str__(self):
        return f"Token(type={self.token_type}, text={self.text!r}, line={self.line}, char={self.char})"

class TokenType(Enum):
    TYPE_NONE = -1
    TYPE_NOP = 0
    TYPE_PUSH = 1
    TYPE_POP = 3
    TYPE_DUP = 4
    TYPE_INDUP = 5
    TYPE_SWAP = 6
    TYPE_INSWAP = 7
    TYPE_ADD = 8
    TYPE_SUB = 9
    TYPE_MUL = 10
    TYPE_DIV = 11
    TYPE_MOD = 12
    TYPE_CMPE = 13
    TYPE_CMPNE = 14
    TYPE_CMPG = 15
    TYPE_CMPL = 16
    TYPE_CMPGE = 17
    TYPE_CMPLE = 18
    TYPE_JMP = 19
    TYPE_ZJMP  = 20
    TYPE_NZJMP = 21
    TYPE_PRINT = 22
    TYPE_INT = 23
    TYPE_HALT = 24
    TYPE_LABEL = 25
    TYPE_LABEL_DEF = 26

def get_token_type(name):
    match name:
        case "nop": return TokenType.TYPE_NOP
        case "push": return TokenType.TYPE_PUSH
        case "pop": return TokenType.TYPE_POP
        case "dup": return TokenType.TYPE_DUP
        case "indup": return TokenType.TYPE_INDUP
        case "swap": return TokenType.TYPE_SWAP
        case "inswap": return TokenType.TYPE_INSWAP
        case "add": return TokenType.TYPE_ADD
        case "sub": return TokenType.TYPE_SUB
        case "mul": return TokenType.TYPE_MUL
        case "div": return TokenType.TYPE_DIV
        case "mod": return TokenType.TYPE_MOD
        case "cmpe": return TokenType.TYPE_CMPE
        case "cmpne": return TokenType.TYPE_CMPNE
        case "cmpg": return TokenType.TYPE_CMPG
        case "cmpl": return TokenType.TYPE_CMPL
        case "cmpge": return TokenType.TYPE_CMPGE
        case "cmple": return TokenType.TYPE_CMPLE
        case "jmp": return TokenType.TYPE_JMP
        case "zjmp": return TokenType.TYPE_ZJMP
        case "nzjmp": return TokenType.TYPE_NZJMP
        case "print": return TokenType.TYPE_PRINT
        case "halt": return TokenType.TYPE_HALT
        case _: return TokenType.TYPE_NONE

class Lexer:
    def __init__(self, filename):
        self.tokens = []
        self.filename = filename

    def run(self):
        self.tokens = []

        with open(self.filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue

                index = 0
                length = len(line)

                while index < length:
                    if line[index].isspace():
                        index += 1
                        continue

                    start_col = index + 1
                    start = index
                    while index < length and not line[index].isspace():
                        index += 1

                    part = line[start:index].strip().lower()

                    # LABEL DEF
                    if part.endswith(":") and part[:-1].isidentifier():
                        self.tokens.append(Token(TokenType.TYPE_LABEL_DEF, part[:-1], line_num, start_col))
                        continue

                    # INT
                    if part.isdigit() or (part.startswith("-") and part[1:].isdigit()):
                        self.tokens.append(Token(TokenType.TYPE_INT, part, line_num, start_col))
                        continue

                    # KEYWORD OR LABEL REF
                    token_type = get_token_type(part)
                    if token_type == TokenType.TYPE_NONE:
                        # treat as label reference if it's identifier
                        if part.isidentifier():
                            self.tokens.append(Token(TokenType.TYPE_LABEL, part, line_num, start_col))
                        else:
                            raise ValueError(f"Unknown token '{part}' at line {line_num}, column {start_col}")
                    else:
                        self.tokens.append(Token(token_type, part, line_num, start_col))

        return self.tokens
