import json
import os
from typing import Literal, Union
from functools import cmp_to_key

Input = Union[int, list]
Pos = tuple[int, int]

def parse_pair(inp: str) -> list[Input]:
    return [json.loads(l) for l in inp.split('\n')]

def read_input (fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [(l, r) for [l, r] in [parse_pair(x) for x in f.read().split('\n\n')]]

indent = '  '
def compare(left: Input, right: Input, debug: bool = False, depth: int = 0) -> Literal[-1, 0, 1]:
    debug and print(f"{indent * depth}- Compare {left} vs {right}")
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        if left - right < 0:
            debug and print(f"{indent * (depth + 1)}- Left side is smaller, so inputs are in the right order")
            return -1
        else:
            debug and print(f"{indent * (depth + 1)}- Right side is smaller, so inputs are in the wrong order")
            return 1
    elif isinstance(left, list) and isinstance(right, list):
        for i in range(len(left)):
            if i >= len(right):
                debug and print(f"{indent * (depth + 1)}- Right side is shorter, so inputs are in the wrong order")
                return 1
            res = compare(left[i], right[i], debug, depth + 1)
            if res == 0:
                continue
            return res
        if len(left) == len(right):
            return 0
        debug and print(f"{indent * (depth + 1)}- Left side is shorter, so inputs are in the right order")
        return -1
    elif isinstance(left, int):
        debug and print(f"{indent * (depth + 1)}- Mixed types; convert left side to [{left}] and retry comparison")
        return compare([left], right, debug, depth + 1)
    else:
        debug and print(f"{indent * (depth + 1)}- Mixed types; convert right side to [{right}] and retry comparison")
        return compare(left, [right], debug, depth + 1)

def part1(data: list[tuple[Input, Input]]):
    s = 0
    for (i, [l, r]) in enumerate(data):
        if compare(l, r) <= 0:
            s += i + 1
    return s

def part2(data: list[tuple[Input, Input]]):
    packets = [[[2]], [[6]]]
    for (l, r) in data:
        packets.append(l)
        packets.append(r)

    sorted_packets = sorted(packets, key=cmp_to_key(compare))
    
    return (sorted_packets.index(packets[0]) + 1) * (sorted_packets.index(packets[1]) + 1)

data = read_input('input.txt')

print("Part 1: {}".format(part1(data)))
print("Part 2: {}".format(part2(data)))