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

def isSubsetOf(a: set, b: set):
    return a.issubset(b) or b.issubset(a)

def part1(data: list[tuple[set, set]]):
    return len(list(filter(lambda x: isSubsetOf(x[0], x[1]), data)))

def part2(data: list[tuple[set[str], set[str]]]):
    return len(list(filter(lambda x: len(set(x[0]).intersection(set(x[1]))) > 0, data)))

data = readInput('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))