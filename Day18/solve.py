from collections import namedtuple
import os
import re
from itertools import combinations
from typing import Literal

Vec3 = namedtuple('Vec3', ['x', 'y', 'z'])
Input = list[Vec3]

def read_input (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [Vec3(*[int(i) for i in x.split(',')]) for x in f.read().split('\n')]


def faces(pos: Vec3):
    (x, y, z) = pos
    off = 0.5
    return [
        Vec3(x + off, y, z),
        Vec3(x - off, y, z),
        Vec3(x, y + off, z),
        Vec3(x, y - off, z),
        Vec3(x, y, z + off),
        Vec3(x, y, z - off),
    ]



def build_reachablity(data: Input):
    # start at origin
    to_visit = [Vec3(0, 0, 0)]
    visited = set()
    reachable = set()
    max_x = max([x for (x, y, z) in data]) + 1
    max_y = max([y for (x, y, z) in data]) + 1
    max_z = max([z for (x, y, z) in data]) + 1
    while to_visit:
        pos = to_visit.pop()
        if pos in visited:
            continue
        visited.add(pos)
        for (x, y, z) in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            px = pos.x + x
            py = pos.y + y
            pz = pos.z + z
            if px < 0 or py < 0 or pz < 0:
                continue
            if px > max_x or py > max_y or pz > max_z:
                continue
            new_pos = Vec3(px, py, pz)
            if new_pos not in data:
                reachable.add(new_pos)
                to_visit.append(new_pos)
    return reachable

def part1(data: Input):
    all_faces = set()
    for pos in data:
        all_faces = all_faces ^ set(faces(pos))
    return len(all_faces)

def part2(data: Input):
    unreachable = build_unreachable(data)

    all_faces = set()
    for pos in data:
        all_faces = all_faces ^ set(faces(pos))
    return len(all_faces - unreachable)

def build_unreachable(data: Input):
    reachable = build_reachablity(data)
    max_x = max([x for (x, y, z) in data]) + 1
    max_y = max([y for (x, y, z) in data]) + 1
    max_z = max([z for (x, y, z) in data]) + 1
    volume = set([Vec3(x, y, z) for x in range(max_x) for y in range(max_y) for z in range(max_z)])
    unreachable = volume - set(data) - reachable
    unreachable_faces = set()
    for pos in unreachable:
        unreachable_faces |= set(faces(pos))
    return unreachable_faces

data = read_input('input.txt')

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")