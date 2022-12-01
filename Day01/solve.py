import os

def readInput (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [[int(p) for p in x.split('\n')] for x in f.read().split('\n\n')]

def part1 (data: list[list[int]]):
    return max([sum(x) for x in data])

def part2 (data: list[list[int]]):
    return sum(sorted([sum(x) for x in data], reverse=True)[0:3])

data = readInput('input.txt')
print("Part 1: ", part1(data))
print("Part 2: ", part2(data))