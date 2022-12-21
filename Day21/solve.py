import os
from typing import Callable
import cvxpy as cp

Input = dict[str, str]

def read_input(fname: str) -> Input:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname, encoding='UTF8') as f:
        return {name: op for name, op in [x.split(': ') for x in f.read().split('\n')]}


ops: dict[str, Callable] = {
    '*': lambda x, y: x * y,
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '/': lambda x, y: x / y,
    '==': lambda x, y: x == y,
}

def resolve(val: str, data: Input, calc_terminal: Callable[[str], any]):
    term = calc_terminal(val)
    if term is not None:
        return term
    if val in data:
        return resolve(data[val], data, calc_terminal)

    left_raw, op, right_raw = val.split(' ')

    left = resolve(left_raw, data, calc_terminal)
    right = resolve(right_raw, data, calc_terminal)

    return ops[op](left, right)

def part1(data: Input):
    return int(resolve(data['root'], inp, lambda val: int(val) if val.isdecimal() else None))

def part2(data: Input):
    humn = cp.Variable(name='humn', integer=True)
    root_left, _, root_right = data['root'].split(' ')
    constraint = resolve(f'{root_left} == {root_right}', data, lambda val: humn if val == 'humn' else cp.Constant(int(val)) if val.isdecimal() else None)
    return int(cp.Problem(cp.Maximize(humn), [constraint]).solve())


inp = read_input('input.txt')

print(f"Part 1: {part1(inp)}")
print(f"Part 2: {part2(inp)}")
