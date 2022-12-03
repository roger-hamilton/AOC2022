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
    # merge the 2 sets
    d2 = [a.union(b) for (a, b) in data]
    # group in chunks of 3
    d3 = [d2[i:i+3] for i in range(0, len(d2), 3)]
    
    return sum([priority(x) for x in [list(set.intersection(*x))[0] for x in d3]])

data = readInput('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))