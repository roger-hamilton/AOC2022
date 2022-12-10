import os
from typing import Literal

Inst = tuple[Literal['noop', 'addx'], int]

def parse_inst(p1: str) -> Inst:
    [op, *params] = p1.split(' ')
    if (op == 'addx'):
        return (op, int(params[0]))
    return (op, 0)

def read_input (fname: str) -> list[Inst]:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [parse_inst(x) for x in f.read().split('\n')]

class Program:
    def __init__(self, insts: list[Inst]):
        self.insts = insts
        self.inst_ptr = 0
        self.curr_inst = insts[0]
        self.inst_cycles = 2 if self.curr_inst[0] == 'addx' else 1
        self.state = 1
        self.cycles = 1

    def tick(self):
        self.inst_cycles -= 1
        self.cycles += 1
        if self.inst_cycles == 0:
            if self.curr_inst[0] == 'addx':
                self.state += self.curr_inst[1]
            self.inst_ptr+=1
            if self.inst_ptr >= len(self.insts):
                return False
            self.curr_inst = self.insts[self.inst_ptr]
            if self.curr_inst[0] == 'addx':
                self.inst_cycles = 2
            else:
                self.inst_cycles = 1
        return True
        
def part1(data: list[Inst]):
    prog = Program(data)
    res = []
    while prog.tick():
        if (prog.cycles - 20) % 40 == 0:
            res.append(prog.state * prog.cycles)
    return sum(res)

def part2(data: list[Inst]):
    prog = Program(data)
    out = ""
    for i in range(240):
        if i % 40 == 0:
            out += '\n'
        if abs((i % 40) - prog.state) <= 1:
            out += '#'
        else:
            out += ' '
        prog.tick()
    return out

data = read_input('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))