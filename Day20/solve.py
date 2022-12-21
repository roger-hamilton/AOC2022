import os
from typing import Callable, TypeVar

Input = list[int]
T = TypeVar('T')


def read_input(fname: str) -> Input:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname, ecoding='UTF8') as f:
        return [int(x) for x in f.read().split('\n')]


def from_zero(data: Input, idx: int) -> int:
    return data[(idx + data.index(0)) % len(data)]


def mix(data: list[T], order: list[T], f_amount=Callable[[T], int]):
    mixed = data.copy()
    for to_move in order:
        curr_index = mixed.index(to_move)
        mixed.remove(to_move)
        mixed.insert((curr_index + f_amount(to_move)) % len(mixed), to_move)
    return mixed


def first_index(data: list[T], pred: Callable[[T], bool]) -> T:
    for i, n in enumerate(data):
        if pred(n):
            return i
    raise ValueError('No element found')


def part1(data: Input):
    mixed = mix(list(enumerate(data)), list(enumerate(data)), lambda x: x[1])
    zero_idx = first_index(mixed, lambda x: x[1] == 0)
    return sum((
        mixed[(i + zero_idx) % len(mixed)][1]
        for i in [1000, 2000, 3000]))


def part2(data: Input):
    data2 = [i * 811589153 for i in data]
    order = list(enumerate(data2))
    mixed = list(enumerate(data2))
    for _ in range(10):
        mixed = mix(mixed, order, lambda x: x[1])

    zero_idx = first_index(mixed, lambda x: x[1] == 0)
    return sum((
        mixed[(i + zero_idx) % len(mixed)][1]
        for i in [1000, 2000, 3000]))


inp = read_input('input.txt')

print(f"Part 1: {part1(inp)}")
print(f"Part 2: {part2(inp)}")
