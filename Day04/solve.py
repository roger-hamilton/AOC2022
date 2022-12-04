import os

def parsePair(str: str):
    [l, r] = str.split('-')
    return set(range(int(l), int(r)+1))

def parseLine (line: str):
    [l, r] = line.split(',')
    return (parsePair(l), parsePair(r))

def readInput (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [parseLine(x) for x in f.read().split('\n')]

def part1(data: list[tuple[set, set]]):
    return len([1 for (a, b) in data if a.issubset(b) or b.issubset(a)])

def part2(data: list[tuple[set, set]]):
    return len([1 for (a, b) in data if len(a.intersection(b)) > 0])

data = readInput('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))