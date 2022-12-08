import os
from typing import TypeVar, Callable

class Tree:
    def __init__(self, value: int, pos: tuple[int, int]):
        self.value = value
        self.pos = pos
    
    def __repr__(self):
        return str(self.value)

def parse_line(line: str, y: int) -> list[Tree]:
    return [Tree(int(line[x]), (x, y)) for x in range(len(line))]

def read_input (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        data = f.read().split('\n')
        return [parse_line(data[y], y) for y in range(len(data))]

def get_cols(data: list[list[int]]):
    return [[x[i] for x in data] for i in range(len(data[0]))]

def visible_1d(data: list[int]):
    max = -1
    seen = set()
    for i in data:
        if i.value > max:
            max = i.value
            seen.add(i.pos)
    return seen

def visible_2d(data: list[list[int]]):
    cols = get_cols(data)
    rev_data = [[d[x] for x in range(len(d) - 1, -1, -1)] for d in data]
    rev_cols = [[c2[x] for x in range(len(c2) - 1, -1, -1)] for c2 in cols]
    return set.union(*[visible_1d(x) for x in (data + cols + rev_data + rev_cols)])

T = TypeVar('T')
def take_until(lst: list[T], pred: Callable[[T], bool]) -> list[T]:
    for i in range(len(lst)):
        if pred(lst[i]):
            return lst[0:min(i + 1, len(lst))]
    return lst

def scenic_score(data: list[list[int]], pos: tuple[int, int]):
    cols = get_cols(data)
    right = data[pos[1]][pos[0]+1:]
    left = data[pos[1]][0:pos[0]]
    left.reverse()
    down = cols[pos[0]][pos[1]+1:]
    up = cols[pos[0]][0:pos[1]]
    up.reverse()
    
    max = data[pos[1]][pos[0]].value
    gte_max = lambda x: x.value >= max

    right = take_until(right, gte_max)
    left = take_until(left, gte_max)
    down = take_until(down, gte_max)
    up = take_until(up, gte_max)

    return len(left) * len(right) * len(up) * len(down)

def part1(data: list[list[int]]):
    return len(visible_2d(data))

def part2(data: list[list[int]]):
    poss = [(x, y) for y in range(len(data)) for x in range(len(data[y]))]
    return max([scenic_score(data, pos) for pos in poss])

data = read_input('input.txt')

scenic_score(data, (2, 1))

print("Part 1: {}".format(part1(data))) # 1138 - too low
print("Part 2: {}".format(part2(data)))