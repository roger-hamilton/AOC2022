import os
import re

def parseStackLine(str: str):
    stack = [str[i:i+4] for i in range(0, len(str), 4)]
    return [x[1] if x[0] == '[' else None for x in stack]

def parseStack(str: str):
    lines = [parseStackLine(x) for x in str.split('\n')[:-1]]
    width = max([len(x) for x in lines])
    return [[x[i] for x in lines if x[i] != None] for i in range(width)]

def parseInst(str: str):
    lines = str.split('\n')
    result = []
    for i in range(len(lines)):
        m = re.search(r'move (\d+) from (\d+) to (\d+)', lines[i])
        result.append((int(m.group(1)), int(m.group(2)) - 1, int(m.group(3)) - 1))
    return result

def readInput (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        [stack, inst] = f.read().split('\n\n')
        return (parseStack(stack), parseInst(inst))

def doMove(stack: list[list[str]], inst: tuple[int, int, int], reverse: bool = False):
    (count, source, destination) = inst
    toMove = stack[source][0:count]
    if reverse:
        toMove.reverse()
    stack[destination] = toMove + stack[destination]
    stack[source] = stack[source][count:]
    return stack

def part1(data: tuple[list[list[str]], list[tuple[int, int, int]]]):
    (stack, insts) = data
    stack = [x.copy() for x in stack]
    for i in insts:
        stack = doMove(stack, i, reverse=True)
    return ''.join([x[0] for x in stack])

def part2(data: list[tuple[set, set]]):
    (stack, insts) = data
    stack = [x.copy() for x in stack]
    for i in insts:
        stack = doMove(stack, i)
    return ''.join([x[0] for x in stack])

data = readInput('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))