from tim_py import *

class Token:
    def __init__(self, token_type, text, line, char):
        self.token_type = token_type
        self.text = text
        self.line = line
        self.char = char
        
class TokenType(Enum):
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


def get_token_type(name):
    match name:
        case "nop":
            return TokenType.TYPE_NOP
        case "push":
            return TokenType.TYPE_PUSH
        case "pop":
            return TokenType.TYPE_POP
        case "dup":
            return TokenType.TYPE_DUP
        case "indup":
            return TokenType.TYPE_INDUP
        case "swap":
            return TokenType.TYPE_SWAP
        case "inswap":
            return TokenType.TYPE_INSWAP
        case "add":
            return TokenType.TYPE_ADD
        case "sub":
            return TokenType.TYPE_SUB
        case "mul":
            return TokenType.TYPE_MUL
        case "div":
            return TokenType.TYPE_DIV
        case "mod":
            return TokenType.TYPE_MOD
        case "cmpe":
            return TokenType.TYPE_CMPE
        case "cmpne":
            return TokenType.TYPE_CMPNE
        case "cmpg":
            return TokenType.TYPE_CMPG
        case "cmpl":
            return TokenType.TYPE_CMPL
        case "cmpge":
            return TokenType.TYPE_CMPGE
        case "cmple":
            return TokenType.TYPE_CMPLE
        case "jmp":
            return TokenType.TYPE_JMP
        case "zjmp":
            return TokenType.TYPE_ZJMP
        case "nzjmp":
            return TokenType.TYPE_NZJMP
        case "print":
            return TokenType.TYPE_PRINT
        case "int":
            return TokenType.TYPE_INT
        case "halt":
            return TokenType.TYPE_HALT
        case _:
            return -1

def lexer(path):
    tokens = []

    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            stripped = line.strip()

            # skip empty lines or comments
            if not stripped or stripped.startswith("#"):
                continue

            # We need to track character positions, so we scan manually
            index = 0
            length = len(line)

            while index < length:
                ch = line[index]

                # skip whitespace
                if ch.isspace():
                    index += 1
                    continue

                start_col = index + 1  # 1-based column number

                # read a word (keyword or number)
                start = index
                while index < length and not line[index].isspace():
                    index += 1

                part = line[start:index].strip().lower()
                if part.isdigit() or (part.startswith("-") and part[1:].isdigit()):
                        tokens.append({
                            "token_type": TokenType.TYPE_INT,
                            "text": part,
                            "line": line_num,
                            "col": start_col,
                        })
                        continue
                token_type = get_token_type(part)
                if token_type == -1:
                    raise ValueError(
                            f"Unknown token '{part}' at line {line_num}, column {start_col}"
                    )

                tokens.append({
                            "token_type": token_type,
                            "text": part,
                            "line": line_num,
                            "col": start_col,
                })
                
                # classify token
                
                

    return tokens