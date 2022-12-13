import os
from typing import TypeVar

Input = list[list[int]]
Pos = tuple[int, int]

def parse_line(line: str) -> list[int]:
    a = ord('a')
    return [ord(x) - a for x in line.strip()]

def read_input (fname: str) -> tuple[Input, Pos, Pos]:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        data = [parse_line(x) for x in f.read().split('\n')]
        start_val = ord('S') - ord('a')
        end_val = ord('E') - ord('a')
        start = (0, 0)
        end = (0, 0)

        for y in range(len(data)):
            for x in range(len(data[0])):
                if (data[y][x] == start_val):
                    start = (x, y)
                elif (data[y][x] == end_val):
                    end = (x, y)
        
        data[start[1]][start[0]] = 0
        data[end[1]][end[0]] = ord('z') - ord('a')

        return data, start, end

def neighbors(data: Input, pos: Pos) -> list[Pos]:
    x, y = pos
    curr = data[y][x] + 1
    result = []

    if x > 0 and data[y][x - 1] <= curr:
        result.append((x - 1, y))
    if x < len(data[pos[1]]) - 1 and data[y][x + 1] <= curr:
        result.append((x + 1, y))
    if y > 0 and data[y - 1][x] <= curr:
        result.append((x, y - 1))
    if y < len(data) - 1 and data[y + 1][x] <= curr:
        result.append((x, y + 1))
    return result

def dijkstra(data: Input, start: Pos, end: Pos):
    visited = set()
    distances = {start: 0}
    previous = {}
    while len(visited) < len(data) * len(data[0]):
        if (len(distances) == 0):
            return None
        current = min(distances, key=distances.get)
        if current == end:
            break
        visited.add(current)
        for neighbor in neighbors(data, current):
            if neighbor in visited:
                continue
            new_distance = distances[current] + 1
            if neighbor not in distances or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current
        del distances[current]

    path = []
    current = end
    while current != start:
        path.append(current)
        current = previous[current]

    return path

def part1(data: Input, start: Pos, end: Pos):
    path = dijkstra(data, start, end)
    return len(path)

def part2(data: Input, end: Pos):
    startings = [(x, y) for y in range(len(data)) for x in range(len(data[0])) if data[y][x] == 0]

    min_path = []
    for start in startings:
        path = dijkstra(data, start, end)
        if path is None:
            continue

        if len(min_path) == 0 or len(path) < len(min_path):
            min_path = path

    return len(min_path)

data, start, end = read_input('input.txt')
print("Part 1: {}".format(part1(data, start, end)))
print("Part 2: {}".format(part2(data, end)))