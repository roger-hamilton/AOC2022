from collections import namedtuple
from itertools import combinations
import os
import re

ValveWithConnections = tuple[str, int, list[str]]
Input = dict[str, ValveWithConnections]
Valve = namedtuple('Valve', ['name', 'flow_rate'])


def parse_line(line: str) -> ValveWithConnections:
    m = re.search(r'Valve (.*) has flow rate=(\d+); tunnels? leads? to valves? (.*)', line)
    [valve, flow_rate, tunnels] = m.groups()
    return (valve, int(flow_rate), tunnels.split(', '))

def read_input (fname: str) -> Input:
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return { x[0]: x for x in [parse_line(x) for x in f.read().split('\n')] }

def process(data: Input):
    cache: dict[str, tuple[int, int]] = {}
    def process_inner(data: Input, at: str, flow: int, minute: int, opened: set[str]):
        key = at + str(minute)
        print(f"{minute:3d}: {at} {flow} {opened}")
        d_flow = sum([data[k][1] for k in opened])
        if key in cache and cache[key][1] >= flow + d_flow * (30-minute):
            print(key, cache[key], flow)
            return cache[key][0]
        if minute >= 30:
            cache[key] = (flow, flow, opened)
            return flow
            
        flow += d_flow
        (valve, flow_rate, tunnels) = data[at]
        res = 0

        # don't open the valve
        res = max([process_inner(data, tunnel, flow, minute + 1, opened) for tunnel in tunnels])
        if not(valve in opened) and flow_rate > 0 and minute > 2:
            # open the valve
            res = max(res, *[process_inner(data, tunnel, flow + flow_rate + d_flow, minute + 2, opened.union([valve])) for tunnel in tunnels])

        cache[key] = (res, flow, opened)
        return res
    return process_inner(data, 'AA', 0, 0, set())


unvisted: set[Valve] = {}

shortest_paths = {}

def key(a, b):
    return tuple(sorted([a, b]))

def explore(shortest_paths: dict[tuple[str, str], int], start: ValveWithConnections, unvisited, turns=0, rate=0, flow=0, path=None, max_turns=30, paths=None):
    if len(unvisited) == 0:
        flow += (max_turns - turns) * rate
        paths.append((path, flow))
        return flow
    for v in unvisited:
        new_turns = shortest_paths.get(key(start[0], v[0]), 0) + 1
        if new_turns == 1 or turns + new_turns > max_turns:
            new_flow = (max_turns - turns) * rate
            paths.append((path, flow + new_flow))
            continue
        new_flow = rate * new_turns
        explore(shortest_paths, v, unvisited=unvisited - {v}, turns=turns + new_turns, rate=rate + v[1], flow=flow+new_flow, path=path + [v[0]], max_turns=max_turns, paths=paths)


def best(paths):
    max_flow = (None, 0)
    for p in paths:
        if p[1] > max_flow[1]:
            max_flow = p
    return max_flow


def build_shortest_paths(data: Input):
    for v in data.values():
        for t in v[2]:
            shortest_paths[key(v[0], t)] = 1
            new_paths = {}
            for p, l in shortest_paths.items():
                if t == p[0] and p[1] != v[0]:
                    k = key(p[1], v[0])
                elif t == p[1] and p[0] != v[0]:
                    k = key(p[0], v[0])
                else:
                    continue
                if k not in shortest_paths or l + 1 < shortest_paths[k]:
                    new_paths[k] = l + 1
            shortest_paths.update(new_paths)
    return shortest_paths

def part1(data: Input):
    shortest_paths = build_shortest_paths(data)
    paths = []
    unvisited = {Valve(name, rate) for (name, rate, _) in data.values() if rate != 0}
    explore(shortest_paths, data['AA'], unvisited, path=[], paths=paths)
    return best(paths)

def part2(data: Input):
    shortest_paths = build_shortest_paths(data)
    unvisited = {Valve(name, rate) for (name, rate, _) in data.values() if rate != 0}
    max_flow = 0
    for i in range(len(data)):
        print('Trying', i, 'valves')
        for c in combinations(unvisited, i):
            s1 = set(c)
            s2 = unvisited - s1
            paths = []
            explore(shortest_paths, data['AA'], unvisited=s1, max_turns=26, path=[], paths=paths)
            b1 = best(paths)
            paths = []
            explore(shortest_paths, data['AA'], unvisited=s2, max_turns=26, path=[], paths=paths)
            b2 = best(paths)
            if b1[1] + b2[1] > max_flow:
                max_flow = b1[1] + b2[1]

    return max_flow

data = read_input('input.txt')

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")