import os
import re
from itertools import combinations

Pos = tuple[int, int]
Becon = Pos
Sensor = tuple[Pos, int]
Input = tuple[list[Sensor], set[Becon]]

def parse_sensor(inp: str) -> tuple[Pos, Pos]:
    m = re.search(r'x=(-?\d+), y=(-?\d+).*x=(-?\d+), y=(-?\d+)', inp)
    [sx, sy, bx, by] = m.groups()
    return ((int(sx), int(sy)), (int(bx), int(by)))

def read_input (fname: str) -> Input:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        items = [parse_sensor(x) for x in f.read().split('\n')]
        sensors = [(s, dist(s, b)) for (s, b) in items]
        becons = [b for (s, b) in items]
        return (sensors, set(becons))

def dist(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_in_range(pos: Pos, sensor: Sensor) -> bool:
    (s, r) = sensor
    return dist(s, pos) <= r

def merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    ranges = sorted(ranges, key=lambda r: r[0])
    res = []
    for (r1, r2) in ranges:
        if len(res) == 0:
            res.append((r1, r2))
        else:
            (l1, l2) = res[-1]
            if l2 + 1 == r1:
                res[-1] = (l1, r2)
            elif l2 >= r1 and l2 <= r2:
                res[-1] = (l1, r2)
            elif l2 > r2:
                pass
            else:
                res.append((r1, r2))
    return res

def find_ranges(sensors: list[Sensor], target: int) -> list[tuple[int, int]]:
    sensors_in_range = [s for s in sensors if is_in_range((s[0][0], target), s)]
    sensors_with_widths = [(s, s[1] - dist(s[0], (s[0][0], target))) for s in sensors_in_range]
    ranges = [(s[0][0] - w, s[0][0] + w) for (s, w) in sensors_with_widths]
    return merge_ranges(ranges)

def part1(data: Input, y_val: int = 2_000_000):
    (sensors, becons) = data
    merged = find_ranges(sensors, y_val)
    line_coverage = sum([r[1] - r[0] + 1 for r in merged])
    becons_on_line = [b for b in becons if b[1] == y_val]
    return line_coverage - len(becons_on_line)

def part2(data: Input):
    (sensors, _) = data
    pairs = [(s1, s2) for s1, s2 in combinations(sensors, 2) if dist(s1[0], s2[0]) == s1[1] + s2[1] + 2]
    assert(len(pairs) == 2)
    x = 0
    for (s1, s2) in pairs:
        (s1, d1), (s2, _) = sorted([s1, s2], key=lambda s: s[0][0])
        if (s1[1] < s2[1]):
            x += s1[1] + (s1[0] + d1 + 1)
            y = (s1[1] + (s1[0] + d1 + 1)) - (x // 2)
        else:
            x -= s1[1] - (s1[0] + d1 + 1)
            y = (s1[1] - (s1[0] + d1 + 1)) + (x // 2)
    return (x // 2) * 4_000_000 + y

data = read_input('input.txt')

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")