from itertools import cycle
import os
from typing import Literal

Dir = Literal['<', '>']
Input = list[Dir]
Rocks = list[int]

def read_input(fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [x for x in f.read()]

class Pile:
    __peices = [
        [
            int('0011110', 2),
        ],
        [
            int('0001000', 2),
            int('0011100', 2),
            int('0001000', 2),
        ],
        [
            int('0000100', 2),
            int('0000100', 2),
            int('0011100', 2),
        ],
        [
            int('0010000', 2),
            int('0010000', 2),
            int('0010000', 2),
            int('0010000', 2),
        ],
        [
            int('0011000', 2),
            int('0011000', 2),
        ],
    ]

    def __init__(self, directions: Input) -> None:
        self.directions = cycle(directions)
        self.peice = cycle(self.__peices)
        self.pile: Rocks = []

    def can_shift(self, direction: Dir, level: int, rock: Rocks):
        for i, rock_row in enumerate(rock):
            pile_row = self.pile[level + i]
            if direction == '>' and ((rock_row & 1) or (rock_row >> 1 & pile_row)):
                return False
            if direction == '<' and ((rock_row & 2 ** 6) or (rock_row << 1 & pile_row)):
                return False
        return True

    def can_fall(self, level: int, rock: Rocks):
        for r in range(len(rock)):
            if (level + r >= len(self.pile) - 1) or (rock[r] & self.pile[level + r + 1]):
                return False
        return True

    def drop_next(self, debug: bool = False):
        rock = next(self.peice).copy()
        self.pile = [0] * (3 + len(rock)) + self.pile
        for level in range(len(self.pile)):
            debug and self.dump(level, rock)
            dir = next(self.directions)

            if self.can_shift(dir, level, rock):
                for r in range(len(rock)):
                    rock[r] = rock[r] >> 1 if dir == '>' else rock[r] << 1
            if not self.can_fall(level, rock):
                for r in range(len(rock)):
                    self.pile[level + r] |= rock[r]

                while self.pile[0] == 0:
                    self.pile.pop(0)

                debug and self.dump()
                return self

    def dump(self, level: int = 0, rock: Rocks = None):
        lines = []
        has_entry = True
        for i, row in enumerate(self.pile):
            if row != 0:
                has_entry = True
            line = list(reversed(['#' if c == '1' else '.' for c in format(row, '07b')]))
            if rock and i >= level and i < level + len(rock):
                has_entry = True
                for d in range(7):
                    if rock[i - level] & 2 ** d:
                        line[d] = '@'
            if has_entry:
                lines.append(f"{i:2d}:|{''.join(reversed(line))}|")
        lines.append(f"   +{''.join(['-' for _ in range(7)])}+")
        print('\n'.join(lines))
        print()

    @property
    def height(self):
        return len(self.pile)

    def __str__(self):
        lines = []
        for r in self.pile:
            lines.append(f"|{''.join(['#' if c == '1' else '.' for c in format(r, '07b')])}|")
        lines.append(f"+{''.join(['-' for _ in range(7)])}+")
        return '\n'.join(lines)

def find_pattern(data: list[int]):
    for prefix in range(len(data)):
        print(f'checking prefix len {prefix}')
        search = data[prefix:]
        for pattern_length in range(2, len(search) // 2):
            target = search[:pattern_length]
            for offset in range(pattern_length, len(search) - pattern_length, pattern_length):
                if search[offset:offset + pattern_length] != target:
                    break
            else:  # little known feature of python - only executed if the loop ended normally (no break)
                return data[:prefix], target
    return [], []

def part1(data: Input):
    pile = Pile(data)
    for _ in range(2022):
        pile.drop_next()
    return pile.height

def part2(data: Input):
    pile = Pile(data)

    sample_size = max(len(data) * 4, 10_000)

    heights = []
    for _ in range(sample_size):
        prev = pile.height
        pile.drop_next()
        heights.append(pile.height - prev)

    print(f'found {len(heights)} height deltas')

    prefix, pattern = find_pattern(heights)
    l_pre = len(prefix)
    l_pat = len(pattern)

    print(f'after {l_pre} steps, a repeating pattern of size {l_pat} is found')
    n_rocks = 1_000_000_000_000
    return sum(prefix) + (sum(pattern) * ((n_rocks - l_pre) // l_pat)) + sum(pattern[:((n_rocks - l_pre) % l_pat)])


data = read_input('input.txt')

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
