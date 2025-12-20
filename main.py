from enum import Enum

class Inst_Set(Enum):
    INST_PUSH = 1
    INST_POP = 2
    INST_ADD = 3
    INST_SUB = 4
    INST_MUL = 5
    INST_DIV = 6
    INST_PRINT = 7

class Inst:
    def __init__(self, inst_type, val=0):
        self.inst_type = inst_type      # instance attribute
        self.val = val

def DEF_INST_PUSH(x):
    return Inst(Inst_Set.INST_PUSH, x)
def DEF_INST_POP():
    return Inst(Inst_Set.INST_POP)
def DEF_INST_ADD():
    return Inst(Inst_Set.INST_ADD)
def DEF_INST_SUB():
    return Inst(Inst_Set.INST_SUB)
def DEF_INST_MUL():
    return Inst(Inst_Set.INST_MUL)
def DEF_INST_DIV():
    return Inst(Inst_Set.INST_DIV)
def DEF_INST_PRINT():
    return Inst(Inst_Set.INST_PRINT)

program = [
    DEF_INST_PUSH(5), 
    DEF_INST_PUSH(10),
    DEF_INST_PRINT()
] 
PROGRAM_SIZE = len(program)

MAX_STACK_SIZE = 1024

stack = []

def push(val):
    #print("push")
    if len(stack) >= MAX_STACK_SIZE:
        raise RuntimeError("ERROR: Stack Overflow")
    stack.append(val)

def pop():
    #print("pop")
    if len(stack) <= 0:
        raise RuntimeError("ERROR: Stack Underflow")
    return stack.pop()    

def main():
    for inst in program:
        match inst.inst_type:
            case Inst_Set.INST_PUSH:
                push(inst.val)
            case Inst_Set.INST_POP:
                pop()
            case Inst_Set.INST_ADD:
                a = pop()
                b = pop()
                push(a + b)
            case Inst_Set.INST_SUB:
                a = pop()
                b = pop()
                push(b - a)
            case Inst_Set.INST_MUL:
                a = pop()
                b = pop()
                push(a * b)
            case Inst_Set.INST_DIV:
                a = pop()
                b = pop()
                push(b // a)
            case Inst_Set.INST_PRINT:
                a = pop()
                print(a)
        print(stack)

main()