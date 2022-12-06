import os

def readInput (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return f.read()

def findMarker(input: str, unique: int):
    for i in range(len(input) - (unique - 1)):
        if len(set(input[i:i + unique])) == unique:
            return i + unique
    return -1

def part1(data: str):
    return findMarker(data, 4)

def part2(data: str):
    return findMarker(data, 14)

data = readInput('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))