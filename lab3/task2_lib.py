from tqdm import tqdm
from task1_lib import *

Individual = namedtuple("Individual", ["genome", "fitness"])

NUM_MATCHES = 100
NUM_GENERATIONS = 25
NIM_SIZE = 10
POPULATION_SIZE = 30


def mutation(genome):
    outcome = random.random()
    if outcome > .5:
        genome["alpha"] = genome["alpha"] + 1 / 2
    else:
        genome["alpha"] = genome["alpha"] / 2

    return genome


def cross_over(genome1, genome2):
    child = dict()
    child["alpha"] = (genome1["alpha"] + genome2["alpha"]) / 2
    return child


def strategy_ga(state: Nim, genome) -> Nimply:
    cooked = cook_status(state)
    alpha = genome["alpha"]
    if alpha > 0.5:

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
        row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
        num_objects = random.randint(1, state.rows[row])

    return Nimply(row, num_objects)


def w(genome: dict) -> float:
    won = 0

    for m in range(NUM_MATCHES):
        nim = Nim(NIM_SIZE)
        player = 0
        while nim:
            if player == 0:
                ply = strategy_ga(nim, genome)
            else:
                #ply = random.choice([gabriele, pure_random])(nim)
                ply = pure_random(nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / NUM_MATCHES


def tournament(population, tournament_size=2):
    return max(random.choices(population, k=tournament_size), key=lambda i: i.fitness)


def generate_population():
    population = list()
    print("[info] - Start generating the population")
    for _ in tqdm(range(POPULATION_SIZE)):
        genome = dict(alpha=random.random())
        population.append(Individual(genome, w(genome)))
    return population


def evolve(INITIAL_POPULATION):
    POPULATION = deepcopy(INITIAL_POPULATION)
    best = Individual(dict(alpha=0.5), 0)

    offspring_size = 10


    for _ in tqdm(range(NUM_GENERATIONS)):
        offspring = list()
        for i in range(offspring_size):
            outcome = random.random()
            if outcome < 0.5:
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
            best = POPULATION[0]

    print(f"solution: {best.genome}")
    return best.genome


def run_GA():
    population = generate_population()
    return evolve(population)



