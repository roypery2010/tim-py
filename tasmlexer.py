from tim_py import *
from enum import Enum

MAX_TOKEN_STACK_SIZE = 1024

class Token:
    def __init__(self, token_type, text, line, char):
        self.token_type = token_type
        self.text = text
        self.line = line
        self.char = char

    def val(self):
        match self.token_type:
            case TokenType.TYPE_INT:
                return int(self.text)
            case TokenType.TYPE_FLOAT:
                return float(self.text)
            case _:
                raise ValueError(f"Not a number {self.text}")

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
    TYPE_FLOAT = 27
    TYPE_CHAR = 28  # kept for reference

def get_token_type(name):
    match name.lower():
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

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_char(s):
    """Return True if s is a single printable character or quoted char/escape."""
    if len(s) == 1 and s.isprintable():
        return True
    if len(s) == 3 and s.startswith("'") and s.endswith("'"):
        return True
    if len(s) == 4 and s.startswith("'") and s.endswith("'") and s[1] == "\\":
        return True
    return False

def char_to_value(s):
    """Convert char token to numeric value for push."""
    if len(s) == 1:
        return ord(s)
    if len(s) == 3 and s.startswith("'") and s.endswith("'"):
        return ord(s[1])
    if len(s) == 4 and s.startswith("'") and s.endswith("'") and s[1] == "\\":
        esc_map = {'n': '\n', 't': '\t', '\\': '\\', "'": "'"}
        if s[2] not in esc_map:
            raise ValueError(f"Unknown escape sequence {s}")
        return ord(esc_map[s[2]])
    raise ValueError(f"Invalid char literal {s}")

class Lexer:
    def __init__(self, filename):
        self.tokens = []
        self.filename = filename

    def run(self):
        self.tokens = []

        with open(self.filename, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                if not line.strip() or line.strip().startswith("#"):
                    continue

                index = 0
                length = len(line)

                while index < length:
                    if line[index].isspace():
                        index += 1
                        continue

                    start_col = index
                    start = index

                    while index < length and not line[index].isspace():
                        index += 1

                    part = line[start:index].strip()

                    # LABEL DEF
                    if part.endswith(":") and part[:-1].isidentifier():
                        self.tokens.append(Token(TokenType.TYPE_LABEL_DEF, part[:-1], line_num, start_col))
                        continue

                    # KEYWORD
                    token_type = get_token_type(part.lower())
                    if token_type != TokenType.TYPE_NONE:
                        self.tokens.append(Token(token_type, part, line_num, start_col))

                        # Special handling: push argument
                        if token_type == TokenType.TYPE_PUSH:
                            # Skip whitespace
                            while index < length and line[index].isspace():
                                index += 1
                            arg_start = index
                            arg_end = index
                            while arg_end < length and not line[arg_end].isspace():
                                arg_end += 1
                            arg_part = line[arg_start:arg_end].strip()
                            index = arg_end

                            if is_int(arg_part):
                                self.tokens.append(Token(TokenType.TYPE_INT, arg_part, line_num, arg_start))
                            elif is_float(arg_part):
                                self.tokens.append(Token(TokenType.TYPE_FLOAT, arg_part, line_num, arg_start))
                            elif is_char(arg_part):
                                val = char_to_value(arg_part)
                                self.tokens.append(Token(TokenType.TYPE_INT, str(val), line_num, arg_start))
                            else:
                                raise ValueError(f"Invalid push argument '{arg_part}' at line {line_num}, char {arg_start}")
                        continue

                    # NUMBER
                    if is_float(part):
                        self.tokens.append(Token(TokenType.TYPE_FLOAT, part, line_num, start_col))
                        continue

                    if is_int(part):
                        self.tokens.append(Token(TokenType.TYPE_INT, part, line_num, start_col))
                        continue

                    # CHAR
                    if is_char(part):
                        self.tokens.append(Token(TokenType.TYPE_CHAR, part, line_num, start_col))
                        continue

                    # LABEL REFERENCE
                    if part.isidentifier():
                        self.tokens.append(Token(TokenType.TYPE_LABEL, part, line_num, start_col))
                    else:
                        raise ValueError(f"Unknown token '{part}' at line {line_num}, char {start_col}")

        return self.tokens
