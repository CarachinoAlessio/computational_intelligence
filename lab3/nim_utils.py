import logging
from typing import Callable

from nimply import *


def play_match(strategy1, strategy2, nim_size, k_size=None):
    strategy = (strategy1, strategy2)

    nim = Nim(nim_size, k_size)
    logging.debug(f"status: Initial board  -> {nim}")
    player = 0
    while nim:
        ply = strategy[player](nim)
        nim.nimming(ply)
        print(f"status: After player {player} -> {nim}")
        player = 1 - player
    winner = 1 - player
    print(f"status: Player {winner} won!")


def evaluate(strategy: Callable, opponent_strategy: Callable, num_matches=1000, nim_size=10, k_size=None) -> float:
    opponent = (strategy, opponent_strategy)
    won = 0

    for m in range(num_matches):
        nim = Nim(nim_size, k=k_size)
        player = 0
        while nim:
            ply = opponent[player](nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / num_matches


def evaluate_GA(genome, strategy_ga, opponent_strategy: Callable, num_matches=1000, nim_size=10, k_size=None):
    won = 0

    for m in range(num_matches):
        nim = Nim(nim_size, k=k_size)
        player = 0
        while nim:
            if player == 0:
                ply = strategy_ga(nim, genome)
            else:
                ply = opponent_strategy(nim)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / num_matches


def play_n_matches(genome1, genome2, strategy1, strategy2, num_matches=10, nim_size=10, k_size=None):
    won = 0

    for m in range(num_matches):
        nim = Nim(nim_size, k=k_size)
        player = 0
        while nim:
            if player == 0:
                ply = strategy1(nim, genome1)
            else:
                ply = strategy2(nim, genome2)
            nim.nimming(ply)
            player = 1 - player
        if player == 1:
            won += 1
    return won / num_matches
