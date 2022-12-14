import os

Path = list[tuple[int, int]]
Input = list[Path]

def parse_path(inp: str) -> Path:
    res = []
    for l in inp.split(' -> '):
        [x, y] = l.split(',')
        res.append((int(x), int(y)))
    return res

def read_input (fname: str) -> Input:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [parse_path(x) for x in f.read().split('\n')]

class Grid:
    def __init__(self, input: Input, with_floor: bool = False):
        self.max_y = max([max([y for (x, y) in p]) for p in input]) + 2
        self.with_floor = with_floor
        self.grid = {}
        self.last_path = {}
        for p in input:
            last = None
            for (x, y) in p:
                self.grid[(x, y)] = '#'
                if last is not None:
                    (lx, ly) = last
                    if lx == x:
                        for i in range(min(ly, y), max(ly, y) + 1):
                            self.grid[(x, i)] = '#'
                    else:
                        for i in range(min(lx, x), max(lx, x) + 1):
                            self.grid[(i, y)] = '#'
                last = (x, y)

    def __str__(self) -> str:
        min_x = min([x for (x, y) in self.grid])
        max_x = max([x for (x, y) in self.grid])
        res = '-' * (max_x - min_x) + '\n'

        full_grid = self.grid.copy()
        for pos in self.last_path:
            if pos not in full_grid:
                full_grid[pos] = self.last_path[pos]
        for y in range(self.max_y):
            for x in range(min_x, max_x + 1):
                res += full_grid.get((x, y), ' ')
            res += '\n'
        return res.strip()

    def drop_sand(self):
        (x, y) = (500, 0)
        self.last_path = {}
        while y < self.max_y:
            # drop straight down
            while y < self.max_y and (x, y) not in self.grid:
                self.last_path[(x, y)] = '|'
                if self.with_floor and y == self.max_y - 1:
                    self.grid[(x, y)] = 'o'
                    return True
                y += 1
            if (x - 1, y) not in self.grid:
                self.last_path[(x, y - 1)] = '<'
                x -= 1
                continue
            if (x + 1, y) not in self.grid:
                self.last_path[(x, y - 1)] = '>'
                x += 1
                continue
            self.grid[(x, y - 1)] = 'o'
            return (500, 0) not in self.grid
        return False

def part1(data: Input):
    grid = Grid(data)
    count = 0
    while grid.drop_sand():
        count += 1
    return count

def part2(data: Input):
    grid = Grid(data, with_floor=True)
    count = 0
    while grid.drop_sand():
        count += 1
    # need to add one because the last drop is not counted
    return count + 1

data = read_input('input.txt')

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part1(data)}")