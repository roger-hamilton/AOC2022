import os

# Learned about type aliases! (from https://mypy.readthedocs.io/en/stable/kinds_of_types.html#type-aliases)
Pos = tuple[int, int]
State = list[Pos]
Move = tuple[str, int]

def read_input (fname: str) -> list[Move]:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [(dir, int(s))
                for [dir, s]
                in [l.split(' ') for l in f.read().split('\n')]]

def follow(source: Pos, target: Pos) -> Pos:
    if abs(target[0] - source[0]) > 1 or abs(target[1] - source[1]) > 1:
        if target[0] > source[0]:
            source = (source[0] + 1, source[1])
        if target[0] < source[0]:
            source = (source[0] - 1, source[1])
        if target[1] > source[1]:
            source = (source[0], source[1] + 1)
        if target[1] < source[1]:
            source = (source[0], source[1] - 1)
    return source

def move(state: State, move: Move) -> tuple[State, set[Pos]]:
    [h, *t] = state
    (dir, dist) = move
    visited = set([t[-1]])
    while dist > 0:
        if dir == 'U':
            h = (h[0], h[1] + 1)
        elif dir == 'D':
            h = (h[0], h[1] - 1)
        elif dir == 'L':
            h = (h[0] - 1, h[1])
        elif dir == 'R':
            h = (h[0] + 1, h[1])
        
        prev = h
        new_t: list[Pos] = []
        for p in t:
            prev = follow(p, prev)
            new_t.append(prev)
        
        t = new_t
        visited.add(t[-1])
        dist -= 1
    return ([h, *t], visited)

def simulate(moves: list[Move], length: int) -> tuple[State, set[Pos]]:
    state = [(0, 0) for _ in range(length)]
    visited = set()
    for mv in moves:
        (state, new_visited) = move(state, mv)
        visited = visited.union(new_visited)
    return (state, visited)

def part1(data: list[Move]):
    (_, visited) = simulate(data, 2)
    return len(visited)

def part2(data: list[Move]):
    (_, visited) = simulate(data, 10)
    return len(visited)

data = read_input('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))