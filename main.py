from enum import Enum
import pickle

class Inst_Set(Enum):
    INST_PUSH = 1
    INST_POP = 2
    INST_DUP = 3
    INST_SWAP = 4
    INST_ADD = 5
    INST_SUB = 6
    INST_MUL = 7
    INST_DIV = 8
    INST_PRINT = 9

class Inst:
    def __init__(self, inst_type, val=0):
        self.inst_type = inst_type      # instance attribute
        self.val = val

def DEF_INST_PUSH(x):
    return Inst(Inst_Set.INST_PUSH, x)
def DEF_INST_POP():
    return Inst(Inst_Set.INST_POP)
def DEF_INST_DUP():
    return Inst(Inst_Set.INST_DUP)
def DEF_INST_SWAP():
    return Inst(Inst_Set.INST_SWAP)
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
    def run(self):
        for inst in self.instructions:
            match inst.inst_type:
                case Inst_Set.INST_PUSH:
                    self.push(inst.val)
                case Inst_Set.INST_POP:
                    self.self.pop()
                case Inst_Set.INST_DUP:
                    a = self.pop()
                    self.push(a)
                    self.push(a)
                case Inst_Set.INST_SWAP:
                    a = self.pop()
                    b = self.pop()
                    self.push(a)
                    self.push(b)
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
                case Inst_Set.INST_PRINT:
                    a = self.pop()
                    print(a)
            print(self.stack)

program = [
    DEF_INST_PUSH(1),
    DEF_INST_PUSH(2),
    DEF_INST_PUSH(3),
    DEF_INST_PUSH(4),
    DEF_INST_PUSH(5),
    DEF_INST_SWAP(),
    DEF_INST_ADD(),
    DEF_INST_SWAP(),
    DEF_INST_PRINT()
] 
PROGRAM_SIZE = len(program)

MAX_STACK_SIZE = 1024

stack = []


def write_program_to_file(file_path, prog):
    with open(file_path, "wb") as f:
        pickle.dump(prog, f)
def read_program_from_file(file_path):
    with open(file_path, "rb") as f:
        instructions = pickle.load(f)
        return Machine(instructions)
    

def main():
    write_program_to_file("test.tim-py", program)
    machine = read_program_from_file("test.tim-py")
    machine.run()

main()