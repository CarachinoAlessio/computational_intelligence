import copy
import math
from collections import namedtuple
from typing import Tuple

from tqdm import tqdm
import random
from math import ceil
from nim_utils import play_n_matches
from task1_lib import gabriele, pure_random
from nimply import Nimply, Nim, cook_status_t2, sum_with_op
from operator import xor, and_, or_

Individual = namedtuple("Individual", ["genome", "fitness"])

NUM_MATCHES = 100
NUM_GENERATIONS = 30
NIM_SIZE = 10
POPULATION_SIZE = 50


def mutation(genome):
    child = copy.deepcopy(genome)
    outcome = random.random()
    gene = random.choice(list(genome.keys()))
    if outcome > .5:
        child[gene] = (genome[gene] + 1) / 2
    else:
        child[gene] = genome[gene] / 2

    return child


def cross_over(genome1, genome2):
    child = dict()
    genome1keys = sorted(genome1.keys())
    genome2keys = sorted(genome2.keys())
    split = random.randint(1, len(genome1keys) - 1)
    for g in genome1keys[:split]:
        child[g] = genome1[g]
    for g in genome2keys[split:]:
        child[g] = genome2[g]

    return child


def strategy_0(state: Nim, genome) -> Nimply:
    if state.k is None:
        k = 100000000
    else:
        k = state.k
    cooked = cook_status_t2(state)
    alpha = genome["alpha"]
    beta = genome["beta"]
    gamma = genome["gamma"]

    game_type = cooked["game_type"]
    over_avg_rows = cooked["over_avg_rows"]
    under_avg_rows = cooked["under_avg_rows"]

    if game_type == 'end':
        row = random.choices(
            [
                random.choice(over_avg_rows),
                random.choice(under_avg_rows)
            ],
            weights=[gamma, 1 - gamma],
            k=1)[0]

        num_objects = min(k, ceil(beta * state.rows[row]))

    else:

        row = random.choice([i for i, e in enumerate(state.rows) if e > 0])

        num_objects = min(k, ceil(alpha * state.rows[row]))

    return Nimply(row, num_objects)


def strategy_1(state: Nim, genome):
    if state.k is None:
        k = 100000000
    else:
        k = state.k

    cooked = cook_status_t2(state)
    alpha = genome["alpha"]
    beta = genome["beta"]
    if cooked["num_obj"] / cooked["active_rows_number"] * alpha > beta:
        if cooked["active_rows_number"] % 2 == 1:
            row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
            num_objects = min(state.rows[row], k)

        else:
            if state.rows[cooked["longest_row"]] > 1:
                row = random.choice([i for i, e in enumerate(state.rows) if e > 1])
                num_objects = min(state.rows[row] - 1, k)
            else:
                row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
                num_objects = min(state.rows[row], k)
    else:
        if cooked["active_rows_number"] % 2 == 1:
            row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
            num_objects = min(state.rows[row] - 1, k)

        else:
            if state.rows[cooked["shortest_row"]] > 1:
                row = random.choice([i for i, e in enumerate(state.rows) if e > 1])
                num_objects = min(state.rows[row] - 1, k)
            else:
                row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
                num_objects = min(state.rows[row], k)
    return Nimply(row, num_objects)


def strategy_2(state: Nim, genome):
    cooked = cook_status_t2(state)
    alpha = genome["alpha"]
    beta = genome["beta"]
    gamma = genome["gamma"]
    perc = genome["percentage"]
    max_e = state.rows[cooked["longest_row"]]
    op = random.choices([and_, or_, xor], k=1, weights=[alpha, beta, gamma])[0]
    possible_moves = sorted(cooked["possible_moves"], key=lambda i: abs((i[1] / max_e) - perc))

    count = 2*cooked["active_rows_number"]
    for _ in range(count):
        ply = possible_moves.pop()
        if count == 0:
            break
        tmp = copy.deepcopy(state)
        tmp.nimming(ply)
        if sum_with_op(tmp, op) == 0 or len(possible_moves) == 0:
            return ply

    return ply


strategy_ga = strategy_0


def w(genome: dict):
    wr1 = play_n_games(genome, gabriele)
    wr2 = play_n_games(genome, pure_random)
    if strategy_ga.__name__ == 'strategy_2':
        return 0.5 * wr1 + 0.5 * wr2
    else:
        return tuple((wr1, wr2))


def play_n_games(genome, strategy, opp_genome=None):
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            if player == 0:
                ply = strategy_ga(nim, genome)
            else:
                if opp_genome:
                    ply = strategy(nim, opp_genome)
                else:
                    ply = strategy(nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def tournament(population, tournament_size=5):
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)


def tournament2(population, tournament_size=5):
    candidates = random.choices(population, k=tournament_size)
    winrates = list()
    for i, candidate in enumerate(candidates):
        winrates.append(
            sum(
                play_n_matches(candidate.genome, c.genome, strategy_ga, strategy_ga)
                for index, c in enumerate(candidates) if i != index))

    return candidates[winrates.index(max(winrates))]


def generate_population(genome_parameters):
    population = list()
    print("[info] - Start generating the population")
    for _ in tqdm(range(POPULATION_SIZE)):
        genome = dict()
        for gene_name in genome_parameters:
            genome[gene_name] = random.random()
        population.append(Individual(genome, w(genome)))
    return population


def evolve(INITIAL_POPULATION):
    POPULATION = INITIAL_POPULATION
    if strategy_ga.__name__ == 'strategy_2':
        best = Individual(dict(alpha=0.5, beta=0.5, gamma=0.5, delta=0.5), 0)
    else:
        best = Individual(dict(alpha=0.5, beta=0.5, gamma=0.5, delta=0.5), (0, 0))


    offspring_size = 20
    print("[info] - Evolving...")
    for g in tqdm(range(NUM_GENERATIONS)):
        '''
        if g != 0 and g % 20 == 0:
            print(f"[info] - best.fitness = {best.fitness}")
            print(f"[info] - avg.fitness = {sum(i.fitness for i in POPULATION) / len(POPULATION)}")
        '''
        offspring = list()
        for i in range(offspring_size):
            outcome = random.random()
            if outcome < 0.3:
                p = tournament(POPULATION)
                o = mutation(p.genome)
            else:
                p1 = tournament(POPULATION)
                p2 = tournament(POPULATION)
                o = cross_over(p1.genome, p2.genome)
            f = w(o)
            offspring.append(Individual(o, f))
        POPULATION += offspring
        POPULATION = sorted(POPULATION, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]
        if POPULATION[0].fitness > best.fitness:
            best = copy.deepcopy(POPULATION[0])
    # best = tournament2(POPULATION[:5])
    # print(f"best.fitness = {best.fitness}")
    # print(f"avg.fitness = {sum(i.fitness for i in POPULATION)/len(POPULATION)}")
    print(f"[info] - Best genome found is {best.genome} with fitness: {best.fitness}")

    return best.genome


def run_GA(genome_parameters, strategy, num_gen):
    global NUM_GENERATIONS
    global strategy_ga
    NUM_GENERATIONS = num_gen

    strategy_ga = strategy
    population = generate_population(genome_parameters)
    return evolve(population)
