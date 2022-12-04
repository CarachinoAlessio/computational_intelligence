import random
from nimply import *


def pure_random(state: Nim) -> Nimply:
    row = random.choice([r for r, c in enumerate(state.rows) if c > 0])
    num_objects = random.randint(1, state.rows[row])
    return Nimply(row, num_objects)


def gabriele(state: Nim) -> Nimply:
    """Pick always the maximum possible number of the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.rows) for o in range(1, c + 1)]
    return Nimply(*max(possible_moves, key=lambda m: (-m[0], m[1])))


def optimal_strategy(state: Nim) -> Nimply:
    data = cook_status_t1(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0), random.choice(data["brute_force"]))[0]


def fixed_rules_strategy(state: Nim) -> Nimply:
    cooked = cook_status_t1(state)

    if cooked["active_rows_number"] % 2 == 1:
        row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
        num_objects = state.rows[row]

    else:
        if state.rows[cooked["longest_row"]] > 1:
            row = random.choice([i for i, e in enumerate(state.rows) if e > 1])
            num_objects = state.rows[row]-1
        else:
            row = random.choice([i for i, e in enumerate(state.rows) if e > 0])
            num_objects = state.rows[row]

    return Nimply(row, num_objects)