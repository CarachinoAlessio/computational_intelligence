import copy
from collections import namedtuple
from tqdm import tqdm
import random
from math import ceil
from nim_utils import play_n_matches
from task1_lib import gabriele, pure_random
from nimply import Nimply, Nim, cook_status_t2

Individual = namedtuple("Individual", ["genome", "fitness"])

NUM_MATCHES = 50
NUM_GENERATIONS = 100
NIM_SIZE = 10
POPULATION_SIZE = 30


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


def strategy_ga(state: Nim, genome) -> Nimply:
    cooked = cook_status_t2(state)
    alpha = genome["alpha"]
    beta = genome["beta"]
    gamma = genome["gamma"]

    outcome = random.choices([True, False], weights=[gamma, 1 - gamma], k=1)[0]
    if cooked["game_type"] == "end":
        row = random.choices(
                [
                    random.choice(cooked["over_avg_rows"]),
                    random.choice(cooked["under_avg_rows"])
                ],
                weights=[alpha, 1 - alpha],
                k=1)[0]


        num_objects = ceil(beta * state.rows[row])
    else:
        if outcome:

            if cooked["active_rows_number"] % 2 == 1:
                row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
                num_objects = state.rows[row]

            else:
                if state.rows[cooked["longest_row"]] > 1:
                    row = random.choice([i for i, e in enumerate(state.rows) if e > 1])
                    num_objects = state.rows[row] - 1
                else:
                    row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
                    num_objects = state.rows[row]
        else:
            row = random.choices(
                [
                    random.choice(cooked["over_avg_rows"]),
                    random.choice(cooked["under_avg_rows"])
                ],
                weights=[alpha, 1 - alpha],
                k=1)[0]

            '''
            num_objects = random.choices(
                [
                    1,
                    random.randint(1, state.rows[row])
                ],
                weights=[beta, 1 - beta],
                k=1)[0]
            '''
            num_objects = ceil(beta * state.rows[row])

    return Nimply(row, num_objects)


'''
def strategy_ga(state: Nim, genome) -> Nimply:
    cooked = cook_status_t2(state)
    alpha = genome["alpha"]
    beta = genome["beta"]

    row = random.choices(
        [
            random.choice(cooked["over_avg_rows"]),
            random.choice(cooked["under_avg_rows"])
        ],
        weights=[alpha, 1 - alpha],
        k=1)[0]

    num_objects = random.choices(
        [
            1,
            random.randint(1, state.rows[row])
        ],
        weights=[beta, 1 - beta],
        k=1)[0]

    return Nimply(row, num_objects)
'''


'''
def strategy_ga(state: Nim, genome) -> Nimply:
    cooked = cook_status_t2(state)
    alpha = genome["alpha"]
    beta = genome["beta"]

    row = random.choices(
        [
            random.choice(cooked["over_avg_rows"]),
            random.choice(cooked["under_avg_rows"])
        ],
        weights=[alpha, 1 - alpha],
        k=1)[0]

    num_objects = random.choices(
        [
            1,
            random.randint(1, state.rows[row])
        ],
        weights=[beta, 1 - beta],
        k=1)[0]

    return Nimply(row, num_objects)
'''

'''
def strategy_ga(state: Nim, genome) -> Nimply:
    cooked = cook_status_t2(state)
    alpha = genome["alpha"]
    beta = genome["beta"]
    gamma = genome["gamma"]
    outcome = random.choices([True, False], weights=[gamma, 1 - gamma], k=1)[0]

    if outcome:

        if cooked["active_rows_number"] % 2 == 1:
            row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
            num_objects = state.rows[row]

        else:
            if state.rows[cooked["longest_row"]] > 1:
                row = random.choice([i for i, e in enumerate(state.rows) if e > 1])
                num_objects = state.rows[row] - 1
            else:
                row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
                num_objects = state.rows[row]
    else:
        row = random.choices(
            [
                random.choice(cooked["over_avg_rows"]),
                random.choice(cooked["under_avg_rows"])
            ],
            weights=[alpha, 1 - alpha],
            k=1)[0]

        num_objects = random.choices(
            [
                1,
                random.randint(1, state.rows[row])
            ],
            weights=[beta, 1 - beta],
            k=1)[0]

    return Nimply(row, num_objects)
'''

def w(genome: dict) -> float:
    wr1 = play_n_games(genome, gabriele)
    wr2 = play_n_games(genome, pure_random)
    return (wr1, wr2)


def play_n_games(genome, strategy):
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            if player == 0:
                ply = strategy_ga(nim, genome)
            else:
                ply = strategy(nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES

def tournament(population, tournament_size=2):
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


def generate_population():
    population = list()
    print("[info] - Start generating the population")
    for _ in tqdm(range(POPULATION_SIZE)):
        genome = dict(alpha=random.random(), beta=random.random(), gamma=random.random())
        population.append(Individual(genome, w(genome)))
    return population


def evolve(INITIAL_POPULATION):
    POPULATION = INITIAL_POPULATION
    best = Individual(dict(alpha=0.5, beta=0.5, gamma=0.5), (0,0))

    offspring_size = 10
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
            if outcome < 0.15:
                p = tournament2(POPULATION)
                o = mutation(p.genome)
            else:
                p1 = tournament2(POPULATION)
                p2 = tournament2(POPULATION)
                o = cross_over(p1.genome, p2.genome)
            f = w(o)
            offspring.append(Individual(o, f))
        POPULATION += offspring
        POPULATION = sorted(POPULATION, key=lambda i: i.fitness, reverse=True)[:POPULATION_SIZE]
        if POPULATION[0].fitness > best.fitness:
            best = copy.deepcopy(POPULATION[0])
    best = tournament2(POPULATION[:5])
        # print(f"best.fitness = {best.fitness}")
        # print(f"avg.fitness = {sum(i.fitness for i in POPULATION)/len(POPULATION)}")
    print(f"[info] - Best genome found is {best.genome} with fitness: {best.fitness}")

    return best.genome


def run_GA():
    population = generate_population()
    return evolve(population)
