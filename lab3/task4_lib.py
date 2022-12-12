from RLAgent import Agent
import matplotlib.pyplot as plt
from tqdm import tqdm

from nimply import Nim
from task1_lib import pure_random, optimal_strategy
from RL_libs import Q_agent

NUM_MATCHES = 5000
NIM_SIZE = 5


def task4_run(params):
    won = 0
    nim = Nim(NIM_SIZE, k=None)
    max_wr = (0, -1)
    moveHistory = []
    indices = []
    robot = Agent(nim, alpha=params['alpha'], random_factor=params['random_factor'])
    for m in range(NUM_MATCHES):
        player = 0
        while nim:
            if player == 0:
                _ = nim.get_reward()  # get the current state
                # choose an action (explore or exploit)
                action = robot.choose_action(nim)
                nim.nimming(action)
                reward = nim.get_reward()  # get the new state and reward
                # update the robot memory with state and reward
                robot.update_state_history(action, reward)

            else:
                ply = pure_random(nim)
                nim.nimming(ply)

            player = 1 - player
        if player == 1:
            won += 1
        robot.learn()  # robot should learn after every episode
        # get a history of number of steps taken to plot later
        if m % 100 == 0:
            if m == 0:
                continue
            print(f"{m}: {won}/{100}")
            winrate = won / m * 100
            moveHistory.append(winrate)
            indices.append(m)
            won = 0
            if max_wr[0] < winrate:
                max_wr = (winrate, m)
        nim = Nim(NIM_SIZE, k=None)

    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.ylim(0, 100)
    plt.plot(indices, moveHistory, "b")
    plt.show()


def task4_Q(hyperparams):
    won = 0
    status = None
    nim = Nim(NIM_SIZE, k=None)
    max_wr = (0, -1)
    moveHistory = []
    indices = []
    q_agent = Q_agent(nim, hyperparams)
    for m in tqdm(range(NUM_MATCHES)):
        player = 0
        # q_agent = Q_agent(nim, hyperparams)
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
            # print(f"{m}: {won}/{100}")
            winrate = won / 100 * 100
            moveHistory.append(winrate)
            indices.append(m)
            won = 0
            if max_wr[0] < winrate:
                max_wr = (winrate, m)
        nim = Nim(NIM_SIZE, k=None)

    print('max winrate: ', max_wr)
    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.ylim(0, 100)
    plt.plot(indices, moveHistory, "b")
    plt.show()


def task4_Q_optimal(hyperparams, iterations: int):
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

    print('max winrate: ', max_wr)
    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.ylim(0, 100)
    plt.plot(indices, moveHistory, "b")
    plt.show()