from collections import namedtuple
import os
import re
import cvxpy as cp
import numpy as np


Recipe = namedtuple('Recipe', ['ore', 'clay', 'obsidian', 'geode'])
Bots = namedtuple('Bots', ['ore', 'clay', 'obsidian', 'geode'])
Materials = namedtuple('Materials', ['ore', 'clay', 'obsidian', 'geode'])
Blueprint = namedtuple('Blueprint', ['id', 'recipes'])
Input = list[Blueprint]


class Blueprint:
    def __init__(self, id: int, ore: Recipe, clay: Recipe, obsidian: Recipe, geode: Recipe):
        self.id = id
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode


def parse_blueprint(line: str):
    id, ore_ore_cost, clay_ore_cost, ob_ore_cost, ob_clay_cost, geode_ore_cost, geode_ob_cost = re.findall(r'\d+', line)
    return Blueprint(
        int(id),
        Recipe(int(ore_ore_cost), 0, 0, 0),
        Recipe(int(clay_ore_cost), 0, 0, 0),
        Recipe(int(ob_ore_cost), int(ob_clay_cost), 0, 0),
        Recipe(int(geode_ore_cost), 0, int(geode_ob_cost), 0),
    )


def read_input(fname: str):
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    with open(fname) as f:
        return [parse_blueprint(x) for x in f.read().split('\n')]

def optimize_blueprint(blueprint: Blueprint, time: int):
    cost_matrix = np.array([
        [blueprint.ore.ore, blueprint.clay.ore, blueprint.obsidian.ore, blueprint.geode.ore],
        [blueprint.ore.clay, blueprint.clay.clay, blueprint.obsidian.clay, blueprint.geode.clay],
        [blueprint.ore.obsidian, blueprint.clay.obsidian, blueprint.obsidian.obsidian, blueprint.geode.obsidian],
        [blueprint.ore.geode, blueprint.clay.geode, blueprint.obsidian.geode, blueprint.geode.geode],
    ])

    resource_variables = []
    robot_variables = []
    production_variables = []
    constraints = []
    for i in range(time + 1):
        resources = cp.Variable(4)
        robots = cp.Variable(4)
        production_decisions = cp.Variable(4, boolean=True)

        if i == 0:
            # start with no resources
            constraints.append(resources == 0)
            # start with 1 ore bot
            constraints.append(robots[0] == 1)
            # start with no other bots
            constraints.append(robots[1:] == 0)
            # start with no production
            constraints.append(production_decisions == 0)
        else:
            prev_resources = resource_variables[-1]
            # new robots = old robots + produced robots
            constraints.append(robots == robot_variables[-1] + production_variables[-1])
            # at most produce 1 new bot
            constraints.append(cp.sum(production_decisions) <= 1)
            # have enough resources to produce new bot
            constraints.append(cost_matrix @ production_decisions <= prev_resources)
            # new resources = old resources + robots - cost of new robots
            constraints.append(resources == (prev_resources + robots - (cost_matrix @ production_decisions)))

        robot_variables.append(robots)
        resource_variables.append(resources)
        production_variables.append(production_decisions)

    objective = cp.Maximize(resource_variables[-1][3])  # maximize geodes
    prob = cp.Problem(objective, constraints)
    prob.solve()
    return prob.value

def part1(data: Input):
    return sum((bp.id * optimize_blueprint(bp, 24) for bp in data))


def part2(data: Input):
    mul = 1
    for bp in data[:3]:
        mul *= optimize_blueprint(bp, 32)
    return mul


data = read_input('test.txt')

print(f"Part 1: {part1(data)}")
print(f"Part 2: {part2(data)}")
