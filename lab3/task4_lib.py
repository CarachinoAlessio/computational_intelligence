from RLAgent import Agent
import matplotlib.pyplot as plt

from nimply import Nim
from task1_lib import pure_random

NUM_MATCHES = 5000
NUM_GENERATIONS = 30
NIM_SIZE = 10


def task4_run():
    won = 0
    nim = Nim(NIM_SIZE, k=None)

    moveHistory = []
    indices = []

    for m in range(NUM_MATCHES):
        player = 0
        robot = Agent(nim, alpha=0.1, random_factor=0.4)
        while nim:
            if player == 0:
                _ = nim.get_reward()  # get the current state
                # choose an action (explore or exploit)
                action = robot.choose_action(nim)
                # maze.update_maze(action)  # update the maze according to the action
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
        if m % 50 == 0:
            print(f"{m}: {won}/{50}")
            if m == 0:
                continue
            winrate = won / 50 * 100
            moveHistory.append(winrate)
            indices.append(m)
            won = 0
        nim = Nim(NIM_SIZE, k=None)

    plt.ylabel('winrate %')
    plt.xlabel('# games')
    plt.ylim(0, 100)
    plt.plot(indices, moveHistory, "b")
    plt.show()
