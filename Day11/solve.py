import os
from typing import Callable, Literal, Optional

class Monkey:
    def __init__(self, items: list[int], op: Callable[[int], int], test_val: int, if_true: int, if_false: int):
        self.items = items
        self.op = op
        self.test_val = test_val
        self.test = lambda x: if_true if x % test_val == 0 else if_false
        self.inspeced_count = 0

    def accept_item(self, item: int):
        self.items.append(item)

    def process_items(self, div: int = 3) -> list[tuple[int, int]]:
        res = [(i, self.test(i)) for i in [self.op(x) // div for x in self.items]]
        self.inspeced_count += len(self.items)
        self.items = []
        return res

def parse_monkey(p1: str) -> Monkey:
    [itemsLine, operationLine, testLine, trueLine, falseLine] = [t.strip() for t in p1.split('\n')][1:]
    items = [int(x) for x in itemsLine.split(': ')[1].split(', ')]

    [operand, val] = operationLine.split(' ')[-2:]
    def op(x):
        v = int(val) if val != 'old' else x
        return x + v if operand == '+' else x * v

    test_val = int(testLine.split(' ')[3])
    if_true = int(trueLine.split(' ')[-1])
    if_false = int(falseLine.split(' ')[-1])

    return Monkey(items, op, test_val, if_true, if_false)

def read_input (fname: str) -> list[Monkey]:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [parse_monkey(x) for x in f.read().split('\n\n')]

def take_turn(monkeys: list[Monkey], div: int = 3, common_div: Optional[int] = None):
    for m in monkeys:
        for (item, to_monkey) in m.process_items(div):
            item //= div
            if common_div != None:
                item %= common_div
            monkeys[to_monkey].accept_item(item)

def part1(data: list[Monkey]):
    for _ in range(20):
        take_turn(data)

    data.sort(key=lambda x: x.inspeced_count, reverse=True)
    return data[0].inspeced_count * data[1].inspeced_count

def mul(items: list[int]) -> int:
    res = 1
    for i in items:
        res *= i
    return res

def part2(data: list[Monkey]):
    # observation:
    #   the worry numbers can be kept small-ish by mod-ing by the multiple of all test values
    common_div = mul([d.test_val for d in data])
    for _ in range(10000):
        take_turn(data, 1, common_div)

    data.sort(key=lambda x: x.inspeced_count, reverse=True)
    return data[0].inspeced_count * data[1].inspeced_count

data = read_input('input.txt')
print("Part 1: {}".format(part1(data)))
data = read_input('input.txt')
print("Part 2: {}".format(part2(data)))