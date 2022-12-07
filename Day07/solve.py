import os

def parseLines(lines: list[str]):
    dirs = {}
    currentDir = ''
    i = 0
    while i < len(lines):
        line = lines[i]
        if line[:4] == '$ cd':
            dir = line[5:]
            if dir == '..':
                currentDir = currentDir[:currentDir[:-1].rfind('/')] + '/'
            else:
                if dir == '/':
                    dir = ''
                currentDir += dir + '/'
            if currentDir not in dirs:
                dirs[currentDir] = []
        elif line[:4] == '$ ls':
            i+=1
            while i < len(lines) and lines[i][0] != '$':
                if (lines[i][:3] == 'dir'):
                    dirs[currentDir].append(('dir', os.path.join(currentDir, lines[i][4:] + '/')))
                else:
                    [size, name] = lines[i].split(' ')
                    dirs[currentDir].append((int(size), name))
                i+=1
            i-=1
        
        i+=1
    return dirs

def readInput (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return parseLines(f.read().split('\n'))

def sizeOf(dirs: dict, dir: str) -> int:
    size = 0
    for item in dirs[dir]:
        if item[0] == 'dir':
            size += sizeOf(dirs, item[1])
        else:
            size += item[0]
    return size

def part1(data: dict):
    sizes = [sizeOf(data, x) for x in data.keys()]
    sizes = [x for x in sizes if x <= 100000]
    return sum(sizes)

def part2(data: str):
    used = sizeOf(data, '/')
    free = 70000000 - used
    needed = 30000000 - free
    candidates = [x for x in [sizeOf(data, x) for x in data.keys()] if x >= needed]
    return min(candidates)

data = readInput('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))