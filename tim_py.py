from enum import Enum
import pickle

from tasmlexer import *

class Inst_Set(Enum):
    INST_NOP = 0
    INST_PUSH = 1
    INST_HALT = 2
    INST_POP = 3
    INST_DUP = 4
    INST_INDUP = 5
    INST_SWAP = 6
    INST_INSWAP = 7
    INST_ADD = 8
    INST_SUB = 9
    INST_MUL = 10
    INST_DIV = 11
    INST_MOD = 12
    INST_CMPE = 13
    INST_CMPNE = 14
    INST_CMPG = 15
    INST_CMPL = 16
    INST_CMPGE = 17
    INST_CMPLE = 18
    INST_JMP = 19
    INST_ZJMP  = 20
    INST_NZJMP = 21
    INST_PRINT = 22

class Inst:
    def __init__(self, inst_type, val=0):
        self.inst_type = inst_type      # instance attribute
        self.val = val
    def __str__(self):
        return f"Inst(type={self.inst_type}, val={self.val})"


def DEF_INST_PUSH(x):
    return Inst(Inst_Set.INST_PUSH, x)
def DEF_INST_NOP():
    return Inst(Inst_Set.INST_NOP)
def DEF_INST_HALT():
    return Inst(Inst_Set.INST_HALT)
def DEF_INST_POP():
    return Inst(Inst_Set.INST_POP)
def DEF_INST_DUP():
    return Inst(Inst_Set.INST_DUP)
def DEF_INST_INDUP(x):
    return Inst(Inst_Set.INST_INDUP, x)
def DEF_INST_SWAP():
    return Inst(Inst_Set.INST_SWAP)
def DEF_INST_INSWAP(x):
    return Inst(Inst_Set.INST_INSWAP, x)
def DEF_INST_ADD():
    return Inst(Inst_Set.INST_ADD)
def DEF_INST_SUB():
    return Inst(Inst_Set.INST_SUB)
def DEF_INST_MUL():
    return Inst(Inst_Set.INST_MUL)
def DEF_INST_DIV():
    return Inst(Inst_Set.INST_DIV)
def DEF_INST_MOD():
    return Inst(Inst_Set.INST_MOD)
def DEF_INST_CMPE():
    return Inst(Inst_Set.INST_CMPE)
def DEF_INST_CMPNE():
    return Inst(Inst_Set.INST_CMPNE)
def DEF_INST_CMPG():
    return Inst(Inst_Set.INST_CMPG)
def DEF_INST_CMPL():
    return Inst(Inst_Set.INST_CMPL)
def DEF_INST_CMPGE():
    return Inst(Inst_Set.INST_CMPGE)
def DEF_INST_CMPLE():
    return Inst(Inst_Set.INST_CMPLE)
def DEF_INST_JMP(x):
    return Inst(Inst_Set.INST_JMP, x)
def DEF_INST_ZJMP(x):
    return Inst(Inst_Set.INST_ZJMP, x)
def DEF_INST_NZJMP(x):
    return Inst(Inst_Set.INST_NZJMP, x)
def DEF_INST_PRINT():
    return Inst(Inst_Set.INST_PRINT)


MAX_STACK_SIZE = 1024

class Machine:
    def __init__(self, insts):
        self.instructions = insts
        self.stack = []
    def push(self, val):
        #print("push")
        if len(self.stack) >= MAX_STACK_SIZE:
            raise RuntimeError("ERROR: Stack Overflow")
        self.stack.append(val)

    def pop(self):
        #print("pop")
        if len(self.stack) <= 0:
            raise RuntimeError("ERROR: Stack Underflow")
        return self.stack.pop()
    def inswap(self, i):
        stack_size = len(self.stack)
        if (i >= stack_size or i < 0):
            raise RuntimeError("ERROR: Index out of range\n")
        self.stack[i], self.stack[stack_size - 1] = self.stack[stack_size - 1], self.stack[i]
    def indup(self, i):
        stack_size = len(self.stack)
        if (i >= stack_size or i < 0):
            raise RuntimeError("ERROR: Index out of range\n")
        self.push(self.stack[i])
    def print_stack(self):
        print("-----STACK")
        stack_size = len(self.stack)
        for i in range(stack_size - 1, -1, -1):
            print(f"{i} {self.stack[i]}")
        print("-----END OF STACK")
    def run(self):
        for ip in range(len(self.instructions)):
            inst = self.instructions[ip]
            match inst.inst_type:
                case Inst_Set.INST_PUSH:
                    self.push(inst.val)
                case Inst_Set.INST_NOP:
                    continue
                case Inst_Set.INST_POP:
                    self.pop()
                case Inst_Set.INST_DUP:
                    a = self.pop()
                    self.push(a)
                    self.push(a)
                case Inst_Set.INST_INDUP:
                    self.indup(inst.val)
                case Inst_Set.INST_SWAP:
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
                case Inst_Set.INST_INSWAP:
                    self.inswap(inst.val)
                case Inst_Set.INST_ADD:
                    a = self.pop()
                    b = self.pop()
                    self.push(a + b)
                case Inst_Set.INST_SUB:
                    a = self.pop()
                    b = self.pop()
                    self.push(a - b)
                case Inst_Set.INST_MUL:
                    a = self.pop()
                    b = self.pop()
                    self.push(a * b)
                case Inst_Set.INST_DIV:
                    a = self.pop()
                    b = self.pop()
                    if (b == 0):
                        raise RuntimeError("ERROR: Cannot divide by zero\n")
                    self.push(a // b)
                case Inst_Set.INST_DIV:
                    a = self.pop()
                    b = self.pop()
                    self.push(a % b)
                case Inst_Set.INST_CMPE:
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
                    if (a == b):
                        self.push(1)
                    else:
                        self.push(0)
                case Inst_Set.INST_CMPNE:
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
                    if (a != b):
                        self.push(1)
                    else:
                        self.push(0)
                case Inst_Set.INST_CMPG:
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
                    if (a > b):
                        self.push(1)
                    else:
                        self.push(0)
                case Inst_Set.INST_CMPL:
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
                    if (a < b):
                        self.push(1)
                    else:
                        self.push(0)
                case Inst_Set.INST_CMPGE:
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
                    if (a >= b):
                        self.push(1)
                    else:
                        self.push(0)
                case Inst_Set.INST_CMPLE:
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
                    if (a <= b):
                        self.push(1)
                    else:
                        self.push(0)
                case Inst_Set.INST_JMP:
                    ip = inst.val
                    if (ip + 1 >= len(self.instructions)):
                            print("JMP ERROR\n")
                            raise RuntimeError("ERROR: Cannot jump out of bounds\n")
                case Inst_Set.INST_ZJMP:
                    a = self.pop()
                    if (a == 0):
                        ip = inst.val
                        if (ip + 1 >= len(self.instructions)):
                            print("ZJMP ERROR\n")
                            raise RuntimeError("ERROR: Cannot jump out of bounds\n")
                case Inst_Set.INST_NZJMP:
                    a = self.pop()
                    if (a != 0):
                        ip = inst.val
                        if (ip + 1 >= len(self.instructions)):
                            print("NZJMP ERROR\n")
                            raise RuntimeError("ERROR: Cannot jump out of bounds\n")
                case Inst_Set.INST_PRINT:
                    a = self.pop()
                    print(a)
                case Inst_Set.INST_HALT:
                    break
                    
        self.print_stack()

def write_program_to_file(file_path, prog):
    with open(file_path, "wb") as f:
        pickle.dump(prog, f)

def read_program_from_file(file_path):
    with open(file_path, "rb") as f:
        instructions = pickle.load(f)
        return Machine(instructions)
