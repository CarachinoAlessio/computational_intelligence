import matplotlib.pyplot as plt
from tqdm import tqdm
from RL_libs.Memory import Save
from nimply import Nim
from task1_lib import pure_random, optimal_strategy
from RL_libs import Q_agent
import logging


def task4_Q(hyperparams, NIM_SIZE, iterations: int):
    won = 0
    status = None
    nim = Nim(NIM_SIZE, k=None)
    max_wr = (0, -1)
    moveHistory = []
    indices = []
    q_agent = Q_agent(nim, hyperparams)
    for m in tqdm(range(iterations)):
        player = 0
        while nim:
            if player == 0:
                action = q_agent.Q_move(nim)
                nim.nimming(action)
                q_agent.Q_post(nim, status)
            else:
                ply = pure_random(nim)
                nim.nimming(ply)

            player = 1 - player
        if player == 1:
            won += 1
            status = 'win'
        else:
            status = 'lose'
        q_agent.Q_post(nim, status=status)
        status = None
        # get a history of number of steps taken to plot later
        if m % 100 == 0:
            if m == 0:
                continue
            #print(f"{m}: {won}/{100}")
            winrate = won / 100 * 100
            moveHistory.append(winrate)
            indices.append(m)
            won = 0
            if max_wr[0] < winrate:
                max_wr = (winrate, m)
        nim = Nim(NIM_SIZE, k=None)

    logging.info(f'max winrate: {max_wr}')
    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.ylim(0, 100)
    plt.plot(indices, moveHistory, "b")
    plt.show()


def task4_Q_optimal(hyperparams, NIM_SIZE, iterations: int):
    won = 0
    status = None
    nim = Nim(NIM_SIZE, k=None)
    max_wr = (0, -1)
    moveHistory = []
    indices = []
    q_agent = Q_agent(nim, hyperparams)
    for m in tqdm(range(iterations)):
        player = 0
        # q_agent = Q_agent(nim, hyperparams)
        while nim:
            if player == 0:
                action = q_agent.Q_move(nim)
                nim.nimming(action)
                q_agent.Q_post(nim, status)
            else:
                ply = optimal_strategy(nim)
                nim.nimming(ply)

            player = 1 - player
        if player == 1:
            won += 1
            status = 'win'
        else:
            status = 'lose'
        q_agent.Q_post(nim, status=status)
        status = None
        # get a history of number of steps taken to plot later
        if m % 100 == 0:
            if m == 0:
                continue
            #print(f"{m}: {won}/{100}")
            winrate = won / 100 * 100
            moveHistory.append(winrate)
            indices.append(m)
            won = 0
            if max_wr[0] < winrate:
                max_wr = (winrate, m)
        nim = Nim(NIM_SIZE, k=None)

    Save(q_agent.Q, 'Q_data.dat')

    logging.info(f'max winrate: {max_wr}')
    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.ylim(0, 100)
    plt.plot(indices, moveHistory, "b")
    plt.show()