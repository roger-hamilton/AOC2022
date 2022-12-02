import os
from typing import Tuple

them = ['A', 'B', 'C']
me = ['X', 'Y', 'Z']

def parseLine(line: str):
    [a, b] = line.split(' ')
    return (them.index(a), me.index(b))

def readInput (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [parseLine(x) for x in f.read().split('\n')]

def scoreFor(item: Tuple[int, int]):
    (a, b) = item
    score = b + 1

    diff = b - a

    if diff == 0:
        score += 3
    elif diff == 1 or diff == -2:
        score += 6

    return score

def scoreFor2(item: Tuple[int, int]):
    (a, b) = item
    return (b * 3) + ((a + b + 2) % 3) + 1

def part1(data):
    return sum([scoreFor(x) for x in data])

def part2(data):
    return sum([scoreFor2(x) for x in data])

data = readInput('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))