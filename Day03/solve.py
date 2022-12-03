import os

def splitInput(input: str):
    l = len(input)
    return (set(input[:l//2]), set(input[l//2:]))

def readInput (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [splitInput(x) for x in f.read().split('\n')]

def priority(a: str):
    return ord(a) - ord('A') + 27 if a < 'a' else ord(a) - ord('a') + 1

def part1(data: list[tuple[set[str], set[str]]]):
    return sum([priority(x) for x in [list(a.intersection(b))[0] for (a, b) in data]])

def part2(data: list[tuple[set[str], set[str]]]):
    d2 = [a.union(b) for (a, b) in data]
    return sum([priority(list(set.intersection(*d2[i:i+3]))[0]) for i in range(0, len(d2), 3)])

data = readInput('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))